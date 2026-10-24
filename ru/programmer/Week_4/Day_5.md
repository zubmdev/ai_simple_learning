# День 5: Практика — Rules + @Codebase 🎯

**Трек:** 👨‍💻 Программист | **Время:** 30 минут

---

## 🎯 Миссия

Настроить Rules и протестировать с @Codebase на реальном проекте.

---

## 📋 Задачи

1. Создать Rules для проекта
2. Протестировать @Codebase + Rules
3. Сравнить До/После

---

## 🛠️ Практика

### Шаг 1: Подготовка проекта

**Вариант А:** Используй свой проект

**Вариант Б:** Создай новый

```bash
mkdir blog-api && cd blog-api
```

Структура:

```
blog-api/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── posts.py
│   │   └── users.py
│   ├── models/
│   │   ├── post.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── post.py
│   │   └── user.py
│   └── services/
│       └── auth.py
```

---

### Шаг 2: Создай Rules

**config.json:**

```json
{
  "rules": [
    {
      "name": "Project",
      "rule": "FastAPI blog API. PostgreSQL + SQLAlchemy 2.0 async. JWT auth. RESTful. Structure: api/, models/, schemas/, services/."
    },
    {
      "name": "Tech Stack",
      "rule": "Python 3.11+, FastAPI, SQLAlchemy 2.0 async, Pydantic v2, Alembic, pytest, JWT (python-jose), bcrypt."
    },
    {
      "name": "Code Style",
      "rule": "Type hints everywhere. async/await. Google docstrings. Dependency injection. No obvious comments."
    },
    {
      "name": "API Design",
      "rule": "RESTful: GET /posts, POST /posts, GET /posts/{id}. Pagination for lists. Proper HTTP status codes. Pydantic response models."
    },
    {
      "name": "Response",
      "rule": "Concise. Code first. Max 3 sentences. Russian language. Bullet points for lists."
    }
  ]
}
```

---

### Шаг 3: Тесты

#### Тест 1: Создание модели

**Without Rules:**
```
Промпт: "Создай модель Comment"

ИИ: *может написать без type hints, без async*
```

**With Rules:**
```
@Codebase

Создай модель Comment для комментариев к постам.
```

**Ожидается:**
- SQLAlchemy async модель
- Type hints
- Relationships
- Краткое объяснение на русском

---

#### Тест 2: Создание endpoint

```
@Codebase

Создай endpoint POST /comments для создания комментария.
Требуется авторизация.
```

**Ожидается:**
- FastAPI router
- async функция
- JWT auth dependency
- Pydantic schema
- Обработка ошибок

---

#### Тест 3: Поиск + модификация

```
@Codebase

Найди все места, где используется модель Post.
Добавь поле views (int) с default=0.
Обнови все связанные schemas и endpoints.
```

**Ожидается:**
- Найти все использования Post
- Обновить модель
- Обновить schemas
- Обновить endpoints

---

### Шаг 4: Сравнение

| Аспект | До Rules | После Rules |
|--------|----------|-------------|
| Type hints | ❌ Иногда | ✅ Всегда |
| async/await | ❌ Иногда | ✅ Всегда |
| Docstrings | ❌ Редко | ✅ Всегда |
| Краткость | ❌ Длинно | ✅ Кратко |
| Язык | ❌ Mix | ✅ Русский |

---

## 📊 Итоги 4 недель

### Неделя 1: Основы
- Vibe Coding философия
- Continue.dev setup
- Выбор модели
- Первые программы

### Неделя 2: Промпт-инжиниринг
- P.T.C.F. модель
- Zero-shot vs Few-shot
- Chain of Thought
- AI Debugging

### Неделя 3: Контекст
- Context Engineering
- @Files, @Folder, @Terminal
- Чтение legacy кода
- AI Debugging workflow

### Неделя 4: RAG & Rules
- RAG (@Codebase)
- Rules
- Персонализация
- Комбинация техник

---

## 🎉 Ключевые навыки

```
✅ Промпт-инжиниринг (P.T.C.F., CoT, Few-shot)
✅ Контекст-инжиниринг (Context Bloat, Providers)
✅ RAG (@Codebase для больших проектов)
✅ Rules (персонализация AI под проект)
✅ AI Debugging (автоматизация решения проблем)
✅ Legacy Code Reading (понимание чужого кода)
```

---

## Checklist ✅

- [ ] Создал Rules для проекта
- [ ] Тест 1: Модель через @Codebase
- [ ] Тест 2: Endpoint через @Codebase
- [ ] Тест 3: Поиск + модификация
- [ ] Увидел разницу До/После Rules

---

📚 [На предыдущий день ←](./Day_4.md)
