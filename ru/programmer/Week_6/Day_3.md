# День 3: Feature-First Development Workflow 🎯

**Трек:** 👨‍💻 Программист | **Время:** 40 минут

---

## 🎯 Цель дня

Освоить feature-first подход к разработке через AI-промпты.

---

## Feature-First Approach

### Принцип:

```
One Feature = One Vertical Slice

┌────────────────────────────────┐
│         Feature: "Login"        │
│                                 │
│  ┌─────────────────────────┐   │
│  │ UI (Login Form)         │   │
│  └───────────┬─────────────┘   │
│              ▼                  │
│  ┌─────────────────────────┐   │
│  │ API (POST /auth/login)  │   │
│  └───────────┬─────────────┘   │
│              ▼                  │
│  ┌─────────────────────────┐   │
│  │ Service (AuthService)   │   │
│  └───────────┬─────────────┘   │
│              ▼                  │
│  ┌─────────────────────────┐   │
│  │ Repository (UserRepo)   │   │
│  └───────────┬─────────────┘   │
│              ▼                  │
│  ┌─────────────────────────┐   │
│  │ Database (Users Table)  │   │
│  └─────────────────────────┘   │
└────────────────────────────────┘

Создаём ВСЁ сразу для ОДНОЙ фичи.
```

---

## Feature Development Prompt

### Структура промпта:

```
@Context: [существующие файлы]

Реализуй фичу: [название]

Требования:
- [функциональные требования]
- [валидация]
- [обработка ошибок]

Создай:
1. API endpoint
2. Service layer
3. Repository layer
4. Validation schemas
5. Tests (unit + integration)

Используй существующую архитектуру.
```

---

## Практический пример: User Registration

### Промпт:

```
@Files: src/app.ts, src/domain/entities/User.ts, prisma/schema.prisma

Реализуй фичу: User Registration

Требования:
- POST /api/auth/register
- Email (валидация формата, уникальность)
- Password (минимум 8 символов, хеширование bcrypt)
- Name (2-50 символов)

Создай:
1. src/presentation/routes/auth.routes.ts
2. src/presentation/controllers/AuthController.ts
3. src/application/use-cases/RegisterUser.ts
4. src/infrastructure/repositories/UserRepository.ts
5. src/presentation/validators/register.validator.ts
6. tests/auth/register.test.ts

Обработай ошибки:
- Email уже существует
- Невалидные данные
- Ошибка БД

Верни JWT токен после успешной регистрации.
```

### Ожидаемый результат:

**auth.routes.ts:**

```typescript
import { Router } from 'express';
import { AuthController } from '../controllers/AuthController';
import { validateRequest } from '../middleware/validateRequest';
import { registerValidator } from '../validators/register.validator';

const router = Router();
const authController = new AuthController();

router.post(
  '/register',
  registerValidator,
  validateRequest,
  authController.register
);

export default router;
```

**RegisterUser.ts (Use Case):**

```typescript
import { IUserRepository } from '../../domain/repositories/IUserRepository';
import { IAuthService } from '../interfaces/IAuthService';
import { User } from '../../domain/entities/User';
import bcrypt from 'bcrypt';
import { z } from 'zod';

export class RegisterUser {
  constructor(
    private userRepo: IUserRepository,
    private authService: IAuthService
  ) {}

  async execute(data: RegisterUserDTO): Promise<{ user: User; token: string }> {
    // Check if email exists
    const existing = await this.userRepo.findByEmail(data.email);
    if (existing) {
      throw new Error('Email already registered');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(data.password, 10);

    // Create user
    const user = await this.userRepo.create({
      email: data.email,
      password: hashedPassword,
      name: data.name
    });

    // Generate token
    const token = this.authService.generateToken(user);

    return { user, token };
  }
}

export const RegisterUserDTO = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2).max(50)
});

export type RegisterUserDTO = z.infer<typeof RegisterUserDTO>;
```

**register.test.ts:**

```typescript
import request from 'supertest';
import app from '../../src/app';
import { prisma } from '../../src/infrastructure/database/prisma';

describe('POST /api/auth/register', () => {
  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  it('should register a new user', async () => {
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User'
      });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('token');
    expect(response.body.user.email).toBe('test@example.com');
  });

  it('should reject duplicate email', async () => {
    // Create first user
    await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User'
      });

    // Try duplicate
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'password456',
        name: 'Another User'
      });

    expect(response.status).toBe(400);
    expect(response.body.error).toBe('Email already registered');
  });

  it('should validate password length', async () => {
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'short',
        name: 'Test User'
      });

    expect(response.status).toBe(400);
  });
});
```

---

## Iterative Refinement

### После первой реализации:

```
Протестируй и скажи:
1. Что работает?
2. Что можно улучшить?
3. Какие edge cases не покрыты?
4. Какие тесты добавить?
```

### Улучшения:

```
@Files: (только что созданные файлы)

Улучши регистрацию:
1. Добавь rate limiting (5 запросов в минуту)
2. Добавь логирование действий
3. Добавь email verification (заглушка)
4. Улучши обработку ошибок (custom error classes)
5. Добавь integration тесты

Не ломай существующий код.
```

---

## Feature Checklist

### Для каждой фичи:

```
[ ] API endpoint создан
[ ] Валидация работает
[ ] Business logic реализована
[ ] Repository интегрирован
[ ] Unit тесты написаны
[ ] Integration тесты написаны
[ ] Error handling покрыт
[ ] Documentation обновлена
[ ] Manual testing пройден
```

---

## Feature Branch Workflow

### Git workflow с AI:

```
Создай git workflow для фичи "User Registration":

1. Создай ветку
2. Коммить изменения
3. Напиши PR description
4. Что нужно проверить в code review?
```

Пример:

```bash
git checkout -b feature/user-registration
git add .
git commit -m "feat(auth): implement user registration

- Add POST /api/auth/register endpoint
- Validate email, password, name
- Hash passwords with bcrypt
- Return JWT token
- Add unit and integration tests

Closes #42"

git push -u origin feature/user-registration
```

**PR Template:**

```markdown
## Description
Implements user registration with email/password.

## Changes
- [x] API endpoint
- [x] Validation
- [x] Password hashing
- [x] JWT token generation
- [x] Tests

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing done

## Checklist for Reviewer
- [ ] Code follows architecture patterns
- [ ] All tests pass
- [ ] Error handling is proper
- [ ] No security issues
- [ ] Documentation updated
```

---

## Практика

### Задание:

Реализуй одну фичу полностью:

```
Варианты:
1. Create Post (для блога)
2. Send Message (для чата)
3. Place Order (для e-commerce)

Требования:
- Full vertical slice
- Tests
- Error handling
- Git branch
```

---

## Checklist дня ✅

- [ ] Понял feature-first подход
- [ ] Создал промпт для фичи
- [ ] Реализовал все слои
- [ ] Написал тесты
- [ ] Провёл рефакторинг
- [ ] Создал PR

---

📚 [На следующий день →](./Day_4.md)
