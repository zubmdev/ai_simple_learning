# День 4: Custom Rules for Project ⚙️

**Трек:** 👨‍💻 Программист | **Время:** 25 минут

---

## 🎯 Цель

Создать персонализированные Rules для конкретного проекта.

---

## 📋 Анализ проекта

### Вопросы для Rules

```
1. Какой язык?
2. Какой фреймворк?
3. Какая база данных?
4. Какой стиль кода?
5. Какая структура проекта?
6. Какие conventions?
```

---

## 🛠️ Примеры Rules для разных стеков

### FastAPI + PostgreSQL

```json
{
  "rules": [
    {
      "name": "Project",
      "rule": "FastAPI REST API. PostgreSQL + SQLAlchemy 2.0 async. JWT auth. Pydantic v2. Structure: api/, models/, schemas/, services/."
    },
    {
      "name": "Code",
      "rule": "Python 3.11+. Type hints everywhere. async/await. Google docstrings. Dependency injection."
    },
    {
      "name": "API",
      "rule": "RESTful endpoints. APIRouter. response_model. Proper status codes. Pagination for lists."
    },
    {
      "name": "DB",
      "rule": "SQLAlchemy async. Relationships. Alembic migrations. select() syntax. eager loading."
    },
    {
      "name": "Response",
      "rule": "Concise. Code first. Max 3 sentences. Russian. No obvious comments."
    }
  ]
}
```

### Django + DRF

```json
{
  "rules": [
    {
      "name": "Project",
      "rule": "Django 5.0 + DRF. PostgreSQL. Celery. Structure: apps/, core/, config/."
    },
    {
      "name": "Code",
      "rule": "Django conventions. Class-based views. Serializers. select_related/prefetch_related."
    },
    {
      "name": "API",
      "rule": "ViewSets. Routers. Permissions. Throttling. Versioning."
    }
  ]
}
```

### React + TypeScript

```json
{
  "rules": [
    {
      "name": "Project",
      "rule": "React 18 + TypeScript. Tailwind CSS. React Query. Structure: components/, pages/, hooks/, utils/."
    },
    {
      "name": "Code",
      "rule": "Functional components only. Hooks. Named exports. Destructuring. TypeScript strict mode."
    },
    {
      "name": "Style",
      "rule": "Tailwind CSS. Mobile-first. Responsive. Dark mode support."
    }
  ]
}
```

---

## 🧠 Продвинутые Rules

### Автоматические импорты

```json
{
  "name": "Imports",
  "rule": "Always include necessary imports. For FastAPI: from fastapi import FastAPI, APIRouter, Depends, HTTPException. For Pydantic: from pydantic import BaseModel. For SQLAlchemy: from sqlalchemy import Column, Integer, String, ForeignKey."
}
```

### Error Handling

```json
{
  "name": "Errors",
  "rule": "Always handle exceptions. Use HTTPException for APIs. Log errors. Return proper status codes: 400 bad request, 404 not found, 500 server error."
}
```

### Security

```json
{
  "name": "Security",
  "rule": "Never hardcode secrets. Use env variables. Validate all inputs. Parameterized queries. No eval/exec."
}
```

---

## 🛠️ Практика

### Задание: Создай Rules для своего проекта

**1. Проанализируй проект:**

```
Мой проект: ____________
Язык: ____________
Фреймворк: ____________
База данных: ____________
Структура: ____________
```

**2. Создай Rules:**

```json
{
  "rules": [
    {
      "name": "Project",
      "rule": "[Опиши проект]"
    },
    {
      "name": "Tech Stack",
      "rule": "[Перечисли технологии]"
    },
    {
      "name": "Code Style",
      "rule": "[Опиши стиль]"
    },
    {
      "name": "Response",
      "rule": "[Формат ответа]"
    }
  ]
}
```

**3. Протестируй:**

```
Тест 1: "Создай модель User"
→ Проверь: type hints, async, docstring

Тест 2: "Создай endpoint для регистрации"
→ Проверь: FastAPI, Pydantic, auth

Тест 3: "Напиши тест для login"
→ Проверь: pytest, fixtures, coverage
```

---

## 📊 Проверка Rules

### Checklist

| Rule | Проверка | ✅/❌ |
|------|----------|-------|
| Project Context | ИИ использует правильную структуру | |
| Tech Stack | ИИ использует правильные библиотеки | |
| Code Style | ИИ следует стилю | |
| Response Format | ИИ отвечает в нужном формате | |

---

## Checklist ✅

- [ ] Проанализировал проект
- [ ] Создал персонализированные Rules
- [ ] Протестировал с разными промптами
- [ ] Убедился, что ИИ следует Rules

---

📚 [На предыдущий день ←](./Day_3.md) | [На следующий день →](./Day_5.md)
