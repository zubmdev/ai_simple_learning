# День 4: Component Integration Patterns 🔗

**Трек:** 👨‍💻 Программист | **Время:** 35 минут

---

## 🎯 Цель дня

Освоить паттерны интеграции компонентов через контекст и AI-промпты.

---

## Integration Challenges

### Типичные проблемы:

```
1. Dependency Injection
2. Shared State
3. Event Communication
4. API Contracts
5. Data Consistency
```

---

## Pattern 1: Dependency Injection

### Проблема:

```
Сервис A зависит от сервиса B.
Как их связать?
```

### Промпт:

```
@Files: src/application/use-cases/*.ts

Настрой Dependency Injection для всех use cases.

Используй:
- InversifyJS или tsyringe
- Interface для каждого сервиса
- Container configuration

Создай:
1. src/infrastructure/di/container.ts
2. src/infrastructure/di/types.ts
3. Обнови все use cases для DI
```

### Результат:

**types.ts:**

```typescript
export const TYPES = {
  UserRepository: Symbol.for('UserRepository'),
  PostRepository: Symbol.for('PostRepository'),
  AuthService: Symbol.for('AuthService'),
  EmailService: Symbol.for('EmailService'),
  Logger: Symbol.for('Logger')
};
```

**container.ts:**

```typescript
import { container } from 'tsyringe';
import { TYPES } from './types';
import { UserRepository } from '../repositories/UserRepository';
import { PostRepository } from '../repositories/PostRepository';
import { JWTAuthService } from '../auth/JWTAuthService';
import { SMTPEmailService } from '../email/SMTPEmailService';
import { ConsoleLogger } from '../logging/ConsoleLogger';

export function configureContainer() {
  container.register(TYPES.UserRepository, { useClass: UserRepository });
  container.register(TYPES.PostRepository, { useClass: PostRepository });
  container.register(TYPES.AuthService, { useClass: JWTAuthService });
  container.register(TYPES.EmailService, { useClass: SMTPEmailService });
  container.register(TYPES.Logger, { useClass: ConsoleLogger });
}
```

**Use Case с DI:**

```typescript
import { inject, injectable } from 'tsyringe';
import { TYPES } from '../../infrastructure/di/types';

@injectable()
export class RegisterUser {
  constructor(
    @inject(TYPES.UserRepository) private userRepo: IUserRepository,
    @inject(TYPES.AuthService) private authService: IAuthService,
    @inject(TYPES.EmailService) private emailService: IEmailService
  ) {}

  async execute(data: RegisterUserDTO) {
    // ...
    await this.emailService.sendWelcomeEmail(user.email);
    // ...
  }
}
```

---

## Pattern 2: Event-Driven Integration

### Проблема:

```
При регистрации нужно:
1. Создать пользователя
2. Отправить email
3. Создать дефолтные настройки
4. Залогировать действие
```

### Промпт:

```
@Files: src/application/use-cases/RegisterUser.ts

Реализуй event-driven подход:
1. Event Emitter (Node.js built-in или EventEmitter3)
2. Events: UserRegistered, EmailSent, SettingsCreated
3. Event Handlers (listeners)
4. Раздели responsibilities

Создай:
1. src/domain/events/EventEmitter.ts
2. src/domain/events/UserEvents.ts
3. src/application/handlers/*.ts
```

### Результат:

**EventEmitter.ts:**

```typescript
import EventEmitter from 'events';

class EventManager extends EventEmitter {
  private static instance: EventManager;

  static getInstance(): EventManager {
    if (!EventManager.instance) {
      EventManager.instance = new EventManager();
    }
    return EventManager.instance;
  }
}

export const eventManager = EventManager.getInstance();
```

**UserEvents.ts:**

```typescript
import { User } from '../entities/User';

export interface UserRegisteredEvent {
  type: 'UserRegistered';
  payload: {
    user: User;
    timestamp: Date;
  };
}

export const emitUserRegistered = (user: User) => {
  eventManager.emit('UserRegistered', {
    type: 'UserRegistered',
    payload: { user, timestamp: new Date() }
  });
};
```

**RegisterUser.ts (updated):**

```typescript
async execute(data: RegisterUserDTO) {
  const user = await this.userRepo.create({...});
  
  // Emit event instead of direct calls
  emitUserRegistered(user);
  
  return { user, token };
}
```

**handlers/UserEventHandler.ts:**

```typescript
import { eventManager } from '../../domain/events/EventEmitter';

export class UserEventHandler {
  constructor(
    private emailService: IEmailService,
    private settingsService: ISettingsService,
    private logger: ILogger
  ) {
    this.setupListeners();
  }

  private setupListeners() {
    eventManager.on('UserRegistered', async (event) => {
      const { user } = event.payload;
      
      // Send welcome email
      await this.emailService.sendWelcomeEmail(user.email);
      
      // Create default settings
      await this.settingsService.createDefault(user.id);
      
      // Log
      this.logger.info(`User registered: ${user.email}`);
    });
  }
}
```

---

## Pattern 3: API Contract Validation

### Проблема:

```
Frontend и Backend должны использовать одинаковые типы.
```

### Промпт:

```
Создай shared types между frontend и backend:

1. Определи API contract в отдельном пакете
2. Используй Zod schemas
3. Генерируй TypeScript типы
4. Валидируй request/response

Структура:
packages/
├── shared-types/
│   ├── schemas/
│   ├── types/
│   └── package.json
```

### Результат:

**schemas/auth.schema.ts:**

```typescript
import { z } from 'zod';

export const RegisterRequestSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  name: z.string().min(2).max(50)
});

export const RegisterResponseSchema = z.object({
  user: z.object({
    id: z.string(),
    email: z.string(),
    name: z.string()
  }),
  token: z.string()
});

export type RegisterRequest = z.infer<typeof RegisterRequestSchema>;
export type RegisterResponse = z.infer<typeof RegisterResponseSchema>;
```

**Backend usage:**

```typescript
import { RegisterRequest, RegisterResponse } from '@app/shared-types';

async register(req: Request, res: Response): Promise<void> {
  const data: RegisterRequest = req.body;
  // ...
  const response: RegisterResponse = { user, token };
  res.json(response);
}
```

**Frontend usage:**

```typescript
import { RegisterRequest, RegisterResponse } from '@app/shared-types';

async function register(data: RegisterRequest): Promise<RegisterResponse> {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify(data)
  });
  return response.json();
}
```

---

## Pattern 4: Transaction Management

### Проблема:

```
Несколько операций должны быть атомарными.
```

### Промпт:

```
@Files: src/infrastructure/database/prisma.ts

Реализуй transaction management:
1. Unit of Work pattern
2. Transaction decorator
3. Automatic rollback

Пример: Order creation:
- Create order
- Update inventory
- Charge payment
- Send email

Всё или ничего.
```

### Результат:

**TransactionManager.ts:**

```typescript
import { PrismaClient } from '@prisma/client';

export class TransactionManager {
  constructor(private prisma: PrismaClient) {}

  async run<T>(callback: (tx: PrismaClient) => Promise<T>): Promise<T> {
    return this.prisma.$transaction(async (tx) => {
      return callback(tx as PrismaClient);
    });
  }
}
```

**CreateOrder.ts:**

```typescript
async execute(data: CreateOrderDTO) {
  return this.txManager.run(async (tx) => {
    // Create order
    const order = await tx.order.create({...});
    
    // Update inventory
    await tx.product.update({
      where: { id: data.productId },
      data: { stock: { decrement: data.quantity } }
    });
    
    // Charge payment
    await this.paymentService.charge(data.payment);
    
    // Send email
    await this.emailService.sendOrderConfirmation(order);
    
    return order;
  });
}
```

---

## Integration Testing

### Промпт:

```
@Files: (все файлы фичи)

Напиши integration тесты:
1. Test all layers together
2. Mock external services (email, payment)
3. Test database transactions
4. Test event handlers
5. Test error scenarios
```

### Результат:

```typescript
describe('User Registration Integration', () => {
  it('should complete full registration flow', async () => {
    const emailService = { sendWelcomeEmail: jest.fn() };
    const settingsService = { createDefault: jest.fn() };
    
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'password123',
        name: 'Test'
      });

    expect(response.status).toBe(201);
    
    // Verify user created
    const user = await prisma.user.findUnique({
      where: { email: 'test@example.com' }
    });
    expect(user).toBeTruthy();
    
    // Verify event handlers called
    await waitForEvents();
    expect(emailService.sendWelcomeEmail).toHaveBeenCalled();
    expect(settingsService.createDefault).toHaveBeenCalled();
  });
});
```

---

## Практика

### Задание:

Интегрируй 2-3 компонента:

```
Пример: User Registration + Email + Settings

1. Настрой DI
2. Добавь events
3. Настрой transactions
4. Напиши integration тесты
```

---

## Checklist дня ✅

- [ ] Настроил Dependency Injection
- [ ] Реализовал Event-Driven интеграцию
- [ ] Создал shared API contracts
- [ ] Настроил Transaction Management
- [ ] Написал integration тесты

---

## 🎯 Миссия

Свяжи два компонента своего проекта через событие вместо прямого вызова (например, «пользователь зарегистрировался» → отправка email) и закрой связку integration-тестом.

**Готово, когда:** прямой вызов email-сервиса из use case удалён, событие публикуется, а integration-тест с моком проходит зелёным.

---

📚 [На следующий день →](./Day_5.md)
