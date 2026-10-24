# День 1: Architecture Design via AI Prompts 📐

**Трек:** 👨‍💻 Программист | **Время:** 30 минут

---

## 🎯 Цель дня

Спроектировать архитектуру проекта через AI-prompts, применяя лучшие практики.

---

## Архитектурный промптинг

### Структура архитектурного промпта:

```
Context → Requirements → Constraints → Questions
```

### Пример:

```
Я создаю [тип приложения].
Технологический стек: [перечисли].
Требования: [функциональные и нефункциональные].

Спроектируй архитектуру:
1. Выбери паттерн (MVC, Clean Architecture, etc.)
2. Определи слои/модули
3. Опиши data flow
4. Предложи структуру директорий
5. Укажи ключевые зависимости

Объясни выбор каждого решения.
```

---

## Практический пример: REST API

### Промпт:

```
Создаю REST API для блога.
Стек: Node.js, Express, PostgreSQL, TypeScript.

Требования:
- CRUD для постов и комментариев
- JWT аутентификация
- Rate limiting
- Валидация запросов

Спроектируй архитектуру по принципам Clean Architecture.
```

### Ожидаемый ответ:

```
📊 Architecture: Clean Architecture

├── src/
│   ├── domain/          # Entities & Business Rules
│   │   ├── entities/
│   │   │   ├── Post.ts
│   │   │   └── Comment.ts
│   │   └── repositories/
│   │       ├── IPostRepository.ts
│   │       └── ICommentRepository.ts
│   │
│   ├── application/     # Use Cases
│   │   ├── use-cases/
│   │   │   ├── CreatePost.ts
│   │   │   ├── GetPosts.ts
│   │   │   └── ...
│   │   └── interfaces/
│   │       └── IAuthService.ts
│   │
│   ├── infrastructure/  # External Services
│   │   ├── database/
│   │   │   ├── PostgreSQLConnection.ts
│   │   │   └── repositories/
│   │   ├── auth/
│   │   │   └── JWTAuthService.ts
│   │   └── middleware/
│   │       ├── auth.ts
│   │       └── rateLimiter.ts
│   │
│   └── presentation/    # Controllers & Routes
│       ├── controllers/
│       │   ├── PostController.ts
│       │   └── AuthController.ts
│       ├── routes/
│       └── validators/
│
├── tests/
├── docs/
└── package.json
```

---

## Ключевые архитектурные вопросы

### Всегда спрашивай ИИ:

```
1. Why this pattern? (Почему этот паттерн?)
2. Trade-offs? (Компромиссы?)
3. Scalability? (Масштабируемость?)
4. Testing strategy? (Стратегия тестирования?)
5. Security considerations? (Безопасность?)
```

### Пример промпта:

```
@Architecture (ссылка на предыдущий ответ)

Объясни:
1. Почему Clean Architecture, а не MVC?
2. Какие trade-offs этого подхода?
3. Как будет масштабироваться?
4. Как тестировать каждый слой?
5. Какие риски безопасности?
```

---

## Decision Documentation

### Создай ADR (Architecture Decision Record):

```
Создай ADR для выбора архитектуры.
```

Пример:

```markdown
# ADR-001: Clean Architecture для Blog API

## Status
Accepted

## Context
REST API для блога с требованиями:
- Maintainability
- Testability
- Scalability

## Decision
Используем Clean Architecture с 4 слоями:
1. Domain (entities, business rules)
2. Application (use cases)
3. Infrastructure (external services)
4. Presentation (controllers)

## Consequences

### Positive
- Независимость от фреймворков
- Легко тестировать (mock repositories)
- Понятные границы ответственности

### Negative
- Больше boilerplate кода
- Высокий порог входа для junior разработчиков

## Alternatives Considered
1. MVC - проще, но хуже testability
2. Hexagonal Architecture - похоже, но сложнее

## References
- Clean Architecture by Robert Martin
```

---

## Практика

### Задание:

Выбери проект и спроектируй архитектуру:

```
Варианты:
1. Telegram Bot (Node.js + TypeScript)
2. CLI Tool (Python + Click)
3. Real-time Chat (Node.js + WebSocket)
4. E-commerce API (Python + FastAPI)
```

### Шаги:

```
1. Опиши requirements
2. Попроси ИИ спроектировать архитектуру
3. Задай уточняющие вопросы
4. Документируй решения (ADR)
```

---

## Checklist дня ✅

- [ ] Понял структуру архитектурного промпта
- [ ] Получил архитектуру от ИИ
- [ ] Задал вопросы о trade-offs
- [ ] Создал ADR документ
- [ ] Утвердил финальную архитектуру

---

📚 [На следующий день →](./Day_2.md)
