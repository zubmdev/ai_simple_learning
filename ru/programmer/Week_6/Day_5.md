# День 5: Daily Mission — Complete MVP 🚀

**Трек:** 👨‍💻 Программист | **Время:** 50 минут

---

## 🎯 Цель дня

Завершить MVP проекта, проведя финальную проверку и подготовку к production.

---

## MVP Completion Checklist

### Функционал:

```
[ ] Все core features реализованы
[ ] API endpoints работают
[ ] Database schema корректна
[ ] Authentication/Authorization работает
[ ] Error handling покрыт
[ ] Input validation есть
```

### Код:

```
[ ] TypeScript без any
[ ] ESLint проходит
[ ] Тесты > 70% coverage
[ ] Нет hardcoded secrets
[ ] Logging настроен
[ ] Error tracking интегрирован
```

### Infrastructure:

```
[ ] Dockerfile оптимизирован
[ ] docker-compose работает
[ ] CI/CD pipeline настроен
[ ] Environment variables документированы
[ ] Database migrations работают
```

---

## Final Code Review

### Промпт:

```
@Files: (все файлы проекта)

Проведи финальный code review:

1. Security Issues
   - SQL injection
   - XSS
   - CSRF
   - Secrets in code
   - Input validation

2. Performance Issues
   - N+1 queries
   - Missing indexes
   - Unnecessary computations

3. Code Quality
   - DRY violations
   - SOLID violations
   - Magic numbers/strings
   - Missing error handling

4. Architecture
   - Layer violations
   - Tight coupling
   - Missing abstractions

Для каждого issue предложи исправление.
```

---

## Performance Optimization

### Промпт:

```
@Files: src/infrastructure/repositories/*.ts

Оптимизируй производительность:

1. Добавь database indexes
2. Реализуй caching (Redis)
3. Оптимизируй queries
4. Добавь pagination
5. Реализуй connection pooling

Создай:
1. prisma/migrations/add_indexes.sql
2. src/infrastructure/cache/RedisCache.ts
3. Обнови repositories с caching
```

### Пример:

**add_indexes.sql:**

```sql
-- User indexes
CREATE INDEX idx_user_email ON "User"(email);
CREATE INDEX idx_user_created_at ON "User"("createdAt");

-- Post indexes
CREATE INDEX idx_post_author ON "Post"("authorId");
CREATE INDEX idx_post_created_at ON "Post"("createdAt" DESC);
CREATE INDEX idx_post_status ON "Post"(status);

-- Composite indexes
CREATE INDEX idx_post_author_status ON "Post"("authorId", status);
```

**RedisCache.ts:**

```typescript
import Redis from 'ioredis';

export class RedisCache {
  private redis: Redis;

  constructor() {
    this.redis = new Redis(process.env.REDIS_URL);
  }

  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }

  async set(key: string, value: any, ttl = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}
```

**CachedRepository:**

```typescript
export class CachedUserRepository implements IUserRepository {
  constructor(
    private repo: UserRepository,
    private cache: RedisCache
  ) {}

  async findById(id: string): Promise<User | null> {
    const cacheKey = `user:${id}`;
    
    const cached = await this.cache.get<User>(cacheKey);
    if (cached) return cached;

    const user = await this.repo.findById(id);
    if (user) {
      await this.cache.set(cacheKey, user);
    }
    
    return user;
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    const user = await this.repo.update(id, data);
    await this.cache.invalidate(`user:${id}`);
    return user;
  }
}
```

---

## Security Hardening

### Промпт:

```
@Files: src/presentation/middleware/*.ts

Усиль безопасность:

1. Добавь helmet middleware
2. Настрой CORS правильно
3. Добавь rate limiting
4. Реализуй request validation
5. Добавь security headers
6. Настрой JWT refresh tokens

Создай:
1. src/presentation/middleware/security.ts
2. Обнови app.ts
```

### Пример:

**security.ts:**

```typescript
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';

export const securityMiddleware = [
  // Security headers
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
      },
    },
  }),

  // CORS
  cors({
    origin: process.env.CORS_ORIGINS?.split(',') || [],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
  }),

  // Rate limiting
  rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // 100 requests per window
    message: 'Too many requests, please try again later',
  }),

  // Additional headers
  (req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    next();
  },
];
```

---

## Monitoring & Logging

### Промпт:

```
Настрой monitoring и logging:

1. Winston logger с уровнями
2. Structured logging (JSON)
3. Error tracking (Sentry)
4. Performance monitoring (APM)
5. Health check endpoints

Создай:
1. src/infrastructure/logging/Logger.ts
2. src/presentation/routes/health.routes.ts
3. Обнови error handling
```

### Пример:

**Logger.ts:**

```typescript
import winston from 'winston';
import { format } from 'winston';

const { combine, timestamp, printf, json } = format;

const logFormat = printf(({ level, message, timestamp, ...metadata }) => {
  return JSON.stringify({
    level,
    message,
    timestamp,
    ...metadata,
  });
});

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: combine(timestamp(), json(), logFormat),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ],
});
```

**health.routes.ts:**

```typescript
import { Router } from 'express';
import { prisma } from '../../infrastructure/database/prisma';

const router = Router();

router.get('/health', async (req, res) => {
  const checks = {
    server: 'ok',
    database: 'ok',
    redis: 'ok',
  };

  try {
    await prisma.$queryRaw`SELECT 1`;
  } catch (error) {
    checks.database = 'error';
  }

  // Check Redis
  try {
    await redis.ping();
  } catch (error) {
    checks.redis = 'error';
  }

  const allOk = Object.values(checks).every(v => v === 'ok');
  
  res.status(allOk ? 200 : 503).json({
    status: allOk ? 'healthy' : 'unhealthy',
    timestamp: new Date().toISOString(),
    checks,
  });
});

export default router;
```

---

## Documentation

### API Documentation:

```
Сгенерируй OpenAPI/Swagger документацию:

1. Установи swagger-jsdoc и swagger-ui
2. Создай API specs
3. Добавь examples
4. Сгенерируй клиентские SDK
```

### README:

```markdown
# Project Name

Brief description of the project.

## Architecture

Brief architecture overview.

## Setup

### Prerequisites
- Node.js 20+
- PostgreSQL 15+
- Redis 7+

### Installation

\`\`\`bash
make install
make db:migrate
make dev
\`\`\`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| REDIS_URL | Redis connection string | Yes |
| JWT_SECRET | JWT signing secret | Yes |
| PORT | Server port (default: 3000) | No |

## API Documentation

Run server and visit `/api-docs`

## Testing

\`\`\`bash
make test        # Unit tests
make test:integration  # Integration tests
\`\`\`

## Deployment

\`\`\`bash
make docker-build
make docker-up
\`\`\`

## Monitoring

- Health check: `GET /health`
- Metrics: `GET /metrics` (Prometheus format)
- Logs: `logs/` directory

## License

MIT
```

---

## Deployment Checklist

```
Pre-deployment:
[ ] All tests pass
[ ] Code coverage > 70%
[ ] Security audit done
[ ] Performance tested
[ ] Documentation complete

Deployment:
[ ] Environment variables set
[ ] Database migrated
[ ] SSL certificates configured
[ ] CDN configured (if needed)
[ ] Monitoring alerts set

Post-deployment:
[ ] Health checks passing
[ ] Logs flowing
[ ] Error tracking working
[ ] Performance baseline established
```

---

## Практика

### Задание:

Завершить MVP:

```
1. Проведи code review
2. Добавь оптимизации
3. Усиль безопасность
4. Настрой monitoring
5. Напиши документацию
6. Задеплой (staging/production)
```

---

## Checklist недели ✅

- [ ] Спроектировал архитектуру
- [ ] Создал scaffolding
- [ ] Реализовал features
- [ ] Интегрировал компоненты
- [ ] Оптимизировал производительность
- [ ] Усилил безопасность
- [ ] Настроил monitoring
- [ ] Написал документацию
- [ ] Задеплоил MVP

---

## 🎉 Поздравляем!

Ты создал production-ready MVP используя Vibe Coding!

**Следующая неделя:** AI Debugging & Refactoring.

---

📚 [На следующую неделю →](../Week_7.md)
