# День 4: Создаём свои Rules для проекта ⚙️

**Трек:** 🌱 Начинающий | **Время:** 45 минут

---

## 🎯 Цель дня

Создать персонализированные Rules для конкретного проекта.

---

## Часть 1: Анализ проекта

### Прежде чем создавать Rules

Ответь на вопросы:

```
1. Какой язык программирования?
2. Какой фреймворк?
3. Какой стиль кода?
4. Какая структура проекта?
5. Какие библиотеки используешь?
6. Какие есть conventions?
```

### Пример анализа

```
Проект: E-commerce API

Язык: Python 3.11
Фреймворк: FastAPI
База данных: PostgreSQL + SQLAlchemy
Стили:
- Type hints везде
- Async/await
- Pydantic schemas
- Google docstrings
Структура:
- api/ — endpoints
- models/ — SQLAlchemy models
- schemas/ — Pydantic schemas
- services/ — business logic
- utils/ — helpers
```

---

## Часть 2: Шаблон Rules для проекта

### Базовый шаблон

```json
{
  "rules": [
    {
      "name": "Project Context",
      "rule": "This is a FastAPI e-commerce API project. Structure: api/, models/, schemas/, services/, utils/. Use PostgreSQL with SQLAlchemy."
    },
    {
      "name": "Code Style",
      "rule": "Python 3.11+. Use type hints everywhere. Use async/await. Use Pydantic v2 for schemas. Use Google-style docstrings."
    },
    {
      "name": "API Endpoints",
      "rule": "Create endpoints in api/ folder. Use APIRouter. Include response_model. Add proper HTTP status codes. Use dependency injection."
    },
    {
      "name": "Database",
      "rule": "Use SQLAlchemy async. Create models in models/ folder. Use Alembic for migrations. Use relationship() for foreign keys."
    },
    {
      "name": "Response Format",
      "rule": "Be concise. Show code first. Use bullet points for lists. Maximum 3 sentences explanation. Respond in Russian."
    }
  ]
}
```

---

## Часть 3: Практика — создаём Rules

### Упражнение 1: Rules для Flask проекта

```json
{
  "rules": [
    {
      "name": "Flask Setup",
      "rule": "Use Flask 3.0+. Use Blueprints for routes. Use Flask-SQLAlchemy for database. Use Flask-Migrate for migrations."
    },
    {
      "name": "Project Structure",
      "rule": "app/__init__.py for factory. app/routes/ for blueprints. app/models/ for SQLAlchemy models. app/templates/ for Jinja2. app/static/ for CSS/JS."
    },
    {
      "name": "Code Style",
      "rule": "Use type hints. Use f-strings. Keep routes under 20 lines. Use services for business logic. Don't repeat yourself."
    }
  ]
}
```

### Упражнение 2: Rules для React проекта

```json
{
  "rules": [
    {
      "name": "React Setup",
      "rule": "Use React 18+ with hooks. Use TypeScript. Use functional components only. Use Tailwind CSS for styling."
    },
    {
      "name": "Project Structure",
      "rule": "src/components/ for reusable components. src/pages/ for page components. src/hooks/ for custom hooks. src/utils/ for helpers. src/types/ for TypeScript types."
    },
    {
      "name": "Component Style",
      "rule": "Use arrow functions for components. Use destructuring for props. Use named exports. Keep components under 100 lines. Extract complex logic to hooks."
    },
    {
      "name": "State Management",
      "rule": "Use useState for local state. Use useContext for global state. Use React Query for server state. Use URL state for filters/pagination."
    }
  ]
}
```

### Упражнение 3: Rules для Django проекта

```json
{
  "rules": [
    {
      "name": "Django Setup",
      "rule": "Use Django 5.0+. Use Django REST Framework for APIs. Use PostgreSQL. Use Celery for async tasks."
    },
    {
      "name": "Project Structure",
      "rule": "apps/ for Django apps. core/ for shared utilities. config/ for settings. Each app has: models.py, views.py, serializers.py, urls.py, tests.py."
    },
    {
      "name": "Code Style",
      "rule": "Follow Django naming conventions. Use class-based views. Use serializers for validation. Use select_related/prefetch_related for queries."
    },
    {
      "name": "Testing",
      "rule": "Use pytest-django. Use factory_boy for test data. Aim for 90% coverage. Test views, models, and serializers separately."
    }
  ]
}
```

---

## Часть 4: Продвинутые Rules

### Rule: Автоматические импорты

```json
{
  "name": "Auto Imports",
  "rule": "Always include necessary imports in code snippets. For FastAPI: from fastapi import FastAPI, APIRouter, Depends, HTTPException. For Pydantic: from pydantic import BaseModel. For SQLAlchemy: from sqlalchemy import Column, Integer, String, ForeignKey."
}
```

### Rule: Обработка ошибок

```json
{
  "name": "Error Handling",
  "rule": "Always include try/except for database operations. Use HTTPException for API errors. Log errors with structlog. Return proper HTTP status codes: 400 for bad request, 404 for not found, 500 for server error."
}
```

### Rule: Тесты

```json
{
  "name": "Testing Requirements",
  "rule": "Always write pytest tests for new code. Include test for happy path. Include test for edge cases. Include test for error cases. Use fixtures for setup. Use parameterize for multiple cases."
}
```

### Rule: Документация

```json
{
  "name": "Documentation",
  "rule": "Add docstrings to all public functions. Use Google format. Include Args, Returns, Raises, Examples. Update README.md for new features. Add type hints for all parameters."
}
```

---

## Часть 5: Практика — полный пример

### Задача

Создай Rules для проекта блога на FastAPI.

### Решение

```json
{
  "rules": [
    {
      "name": "Project Context",
      "rule": "Blog API on FastAPI. PostgreSQL database. JWT authentication. RESTful API. Features: posts, comments, users, tags, categories."
    },
    {
      "name": "Tech Stack",
      "rule": "Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic, pytest, JWT (python-jose), password hashing (passlib)."
    },
    {
      "name": "Project Structure",
      "rule": "app/main.py - entry point. app/api/ - routers. app/models/ - SQLAlchemy models. app/schemas/ - Pydantic schemas. app/services/ - business logic. app/core/ - config, security. app/db/ - database session."
    },
    {
      "name": "Code Style",
      "rule": "Use type hints everywhere. Use async/await for database. Use dependency injection. Use Pydantic for validation. Follow PEP 8. Use meaningful names."
    },
    {
      "name": "API Design",
      "rule": "RESTful conventions: GET /posts, POST /posts, GET /posts/{id}, PUT /posts/{id}, DELETE /posts/{id}. Use HTTP status codes correctly. Include pagination for lists. Include filtering and sorting."
    },
    {
      "name": "Security",
      "rule": "JWT for authentication. Hash passwords with bcrypt. Validate all inputs. Use environment variables for secrets. SQL injection prevention with SQLAlchemy."
    },
    {
      "name": "Response Format",
      "rule": "Be concise. Show code first, then brief explanation. Maximum 3 sentences. Use Russian language. Use bullet points for lists."
    }
  ]
}
```

---

## Часть 6: Тестирование Rules

### Как проверить, что Rules работают

**Тест 1: Простой запрос**

```
Напиши модель Post для блога.
```

**Ожидаемый результат:**
- SQLAlchemy async модель
- Type hints
- Поля: id, title, content, author_id, created_at
- Правильные импорты

**Тест 2: Создание endpoint**

```
Создай endpoint для получения списка постов.
```

**Ожидаемый результат:**
- FastAPI router
- async функция
- Pagination
- Pydantic response model
- Краткое объяснение на русском

**Тест 3: Сложная логика**

```
Добавь функционал: пользователь может лайкнуть пост.
```

**Ожидаемый результат:**
- Новая модель Like
- Endpoint для лайка
- Проверка авторизации
- Обработка ошибок

---

## Часть 7: Типичные ошибки

### ❌ Ошибка 1: Слишком много Rules

```
❌ 50+ Rules → ИИ путается
✅ 5-10 Rules → ИИ следует чётко
```

### ❌ Ошибка 2: Противоречивые Rules

```
❌ Rule 1: "Use sync functions"
   Rule 2: "Always use async/await"
   
✅ Убедись, что Rules не противоречат друг другу
```

### ❌ Ошибка 3: Слишком общие Rules

```
❌ "Write good code"
✅ "Use type hints, async/await, and handle errors"
```

---

## Checklist дня ✅

- [ ] Проанализировал свой проект
- [ ] Создал базовый шаблон Rules
- [ ] Создал Rules для конкретного стека
- [ ] Добавил продвинутые Rules
- [ ] Протестировал Rules с разными промптами
- [ ] Убедился, что ИИ следует Rules

---

## Что дальше?

**Завтра (День 5):** Daily Mission! Настроим Rules для реального проекта и протестируем с @Codebase.

**Домашнее задание:**
- Создай полный набор Rules для своего проекта
- Протестируй 5 разных промптов
- Запиши, что изменилось в ответах ИИ

---

📚 [На предыдущий день ←](./Day_3.md) | [На следующий день →](./Day_5.md)
