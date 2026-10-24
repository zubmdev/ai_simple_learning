# День 3: Rules & System Prompts 📋

**Трек:** 👨‍💻 Программист | **Время:** 20 минут

---

## 🎯 Цель

Понять Rules (системные инструкции) и создать базовый набор.

---

## 💡 Что такое Rules?

**Rules** — инструкции, которые ИИ получает ПЕРЕД каждым ответом.

```
Without Rules:
User: "Напиши функцию"
AI: *пишет без type hints, без docstring*

With Rules:
User: "Напиши функцию"
AI: *пишет с type hints и docstring автоматически*
```

---

## 🔧 Где хранить Rules

### Option 1: config.json

```json
{
  "models": [...],
  "rules": [
    {
      "name": "Code Style",
      "rule": "Use type hints, async/await, Google docstrings."
    }
  ]
}
```

### Option 2: .continuerules

```
# .continuerules в корне проекта

Always use type hints.
Use async/await for I/O.
Google-style docstrings.
Be concise.
```

---

## 📋 Примеры Rules

### Code Style

```json
{
  "name": "Python Style",
  "rule": "Python 3.11+ syntax. Type hints everywhere. async/await for I/O. Google docstrings. PEP 8. Max line length 88."
}
```

### Framework

```json
{
  "name": "FastAPI",
  "rule": "Use FastAPI with Pydantic v2. SQLAlchemy 2.0 async. Alembic migrations. Dependency injection. Proper HTTP status codes."
}
```

### Response Format

```json
{
  "name": "Concise",
  "rule": "Code first. Maximum 3 sentences explanation. No obvious comments. Bullet points for lists. Russian language."
}
```

### Testing

```json
{
  "name": "Testing",
  "rule": "Always write pytest tests. Use fixtures. Parametrize for multiple cases. Aim for 90% coverage."
}
```

---

## 🛠️ Практика

### Создай базовый набор Rules

**1. Открой config.json:**

```
Ctrl+L → ⚙️ → Open config.json
```

**2. Добавь Rules:**

```json
{
  "rules": [
    {
      "name": "Project Context",
      "rule": "FastAPI blog API. PostgreSQL. JWT auth. Structure: api/, models/, schemas/, services/."
    },
    {
      "name": "Tech Stack",
      "rule": "Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic, pytest, JWT."
    },
    {
      "name": "Code Style",
      "rule": "Type hints everywhere. async/await. Google docstrings. No obvious comments."
    },
    {
      "name": "Response",
      "rule": "Concise. Code first. Max 3 sentences. Russian language."
    }
  ]
}
```

**3. Сохрани и протестируй:**

```
Напиши функцию для получения списка постов с pagination.
```

**4. Проверь:**

- [ ] Type hints есть?
- [ ] async/await есть?
- [ ] Docstring есть?
- [ ] Краткий ответ на русском?

---

## 📊 Rules vs Prompt

| Аспект | Rules | Prompt |
|--------|-------|--------|
| Применение | Всегда | Один раз |
| Контекст | Автоматически | Вручную |
| Место | config.json | Чат |

### Когда использовать

```
Rules:
✅ Правила проекта (стиль, фреймворк)
✅ Формат ответа
✅ Повторяющиеся требования

Prompt:
✅ Конкретная задача
✅ Временные требования
✅ Специфический контекст
```

---

## 💡 Best Practices

### 1. Ограничь количество

```
❌ 50+ Rules → ИИ путается
✅ 5-10 Rules → Чётко следует
```

### 2. Избегай противоречий

```
❌ Rule 1: "Use sync"
   Rule 2: "Always async"

✅ Убедись в consistency
```

### 3. Будь конкретным

```
❌ "Write good code"
✅ "Type hints, async/await, handle errors"
```

---

## Checklist ✅

- [ ] Понял что такое Rules
- [ ] Узнал где хранить
- [ ] Создал базовый набор
- [ ] Протестировал
- [ ] Увидел разницу

---

📚 [На предыдущий день ←](./Day_2.md) | [На следующий день →](./Day_4.md)
