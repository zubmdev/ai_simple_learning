# День 5: Daily Mission — настраиваем Rules и тестируем 🎯

**Трек:** 🌱 Начинающий | **Время:** 50 минут

---

## 🎯 Миссия дня

Настроить Rules для реального проекта и протестировать, как @Codebase + Rules работают вместе.

---

## Часть 1: Подготовка проекта

### Вариант А: Используй свой проект

Если есть проект, используй его.

### Вариант Б: Создай новый проект

```bash
mkdir blog-api
cd blog-api
```

Создай структуру:

```
blog-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── posts.py
│   │   └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── post.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── post.py
│   │   └── user.py
│   └── services/
│       ├── __init__.py
│       └── auth.py
└── requirements.txt
```

---

## Часть 2: Создание Rules

### Шаг 1: Открой config.json

```
Ctrl+L → ⚙️ → Open config.json
```

### Шаг 2: Добавь Rules

```json
{
  "models": [
    {
      "title": "Groq GPT-OSS 20B",
      "provider": "groq",
      "model": "openai/gpt-oss-20b",
      "apiKey": "${GROQ_API_KEY}"
    }
  ],
  "rules": [
    {
      "name": "Project Context",
      "rule": "Blog API on FastAPI with PostgreSQL. JWT auth. RESTful design. Async code. Structure: app/api/, app/models/, app/schemas/, app/services/."
    },
    {
      "name": "Tech Stack",
      "rule": "Python 3.11+, FastAPI, SQLAlchemy 2.0 async, Pydantic v2, Alembic, pytest, JWT (python-jose), bcrypt (passlib)."
    },
    {
      "name": "Code Style",
      "rule": "Always use type hints. Use async/await. Use dependency injection. Pydantic for validation. Google docstrings. Meaningful names."
    },
    {
      "name": "API Design",
      "rule": "RESTful: GET /posts, POST /posts, GET /posts/{id}, PUT /posts/{id}, DELETE /posts/{id}. Pagination for lists. Proper HTTP status codes."
    },
    {
      "name": "Security",
      "rule": "JWT authentication. Password hashing with bcrypt. Environment variables for secrets. Input validation. SQL injection prevention."
    },
    {
      "name": "Response Format",
      "rule": "Be concise. Code first, then brief explanation. Maximum 3 sentences. Russian language. Bullet points for lists."
    },
    {
      "name": "No Obvious Comments",
      "rule": "Don't write comments for self-explanatory code. Only comment complex logic or non-obvious decisions."
    }
  ]
}
```

### Шаг 3: Сохрани и перезапусти

```
Ctrl+S → Перезапусти VS Code
```

---

## Часть 3: Тест 1 — Создание модели

### Промпт

```
@Codebase

Создай модель Comment для комментариев к постам.
Комментарий принадлежит посту и пользователю.
```

### Ожидаемый результат

ИИ должен создать:
- SQLAlchemy async модель
- Type hints
- Правильные relationships
- Без очевидных комментариев
- Краткое объяснение на русском

### Проверка

```python
# Должно быть что-то вроде:

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Comment(Base):
    __tablename__ = "comments"

    id: int = Column(Integer, primary_key=True, index=True)
    content: str = Column(String(1000), nullable=False)
    post_id: int = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
```

---

## Часть 4: Тест 2 — Создание endpoint

### Промпт

```
@Codebase

Создай endpoint для создания комментария к посту.
Требуется авторизация.
```

### Ожидаемый результат

ИИ должен:
- Использовать FastAPI router
- Создать async функцию
- Добавить авторизацию (dependency)
- Использовать Pydantic schema
- Обработать ошибки
- Кратко объяснить

### Проверка

```python
# Должно быть что-то вроде:

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Создаёт комментарий к посту."""
    # Check if post exists...
    comment = Comment(**comment_data.model_dump(), user_id=current_user.id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment
```

---

## Часть 5: Тест 3 — Поиск и рефакторинг

### Промпт

```
@Codebase

Найди все места, где используется модель Post.
Покажи:
1. Где импортируется
2. Где используется в запросах
3. Где используется в schemas

Предложи улучшения для оптимизации запросов.
```

### Ожидаемый результат

ИИ должен:
- Найти все импорты Post
- Найти все запросы к Post
- Найти использование в schemas
- Предложить оптимизации (select_related и т.д.)

---

## Часть 6: Тест 4 — Добавление функционала

### Промпт

```
@Codebase

Добавь систему тегов для постов:
1. Модель Tag (name, slug)
2. Many-to-many связь Post ↔ Tag
3. Endpoint для добавления тегов к посту
4. Endpoint для поиска постов по тегу

Обнови связанные файлы.
```

### Ожидаемый результат

ИИ должен:
- Создать модель Tag
- Создать association table
- Обновить модель Post
- Создать endpoints
- Обновить schemas

---

## Часть 7: Финальная проверка

### Чек-лист Rules

Проверь, что ИИ следует Rules:

| Rule | Проверка | ✅/❌ |
|------|----------|-------|
| Project Context | ИИ использует правильную структуру папок | |
| Tech Stack | ИИ использует FastAPI + SQLAlchemy async | |
| Code Style | ИИ добавляет type hints | |
| API Design | ИИ создаёт RESTful endpoints | |
| Security | ИИ добавляет авторизацию | |
| Response Format | ИИ отвечает кратко на русском | |
| No Obvious Comments | ИИ не пишет `# create comment` над строкой `comment = Comment()` | |

### Если Rules не работают

1. Проверь, что config.json сохранён
2. Перезапусти VS Code
3. Проверь JSON синтаксис (валидный JSON?)
4. Убедись, что Rules в правильном месте

---

## Часть 8: Сравнение До/После Rules

### До Rules

```
Промпт: "Создай endpoint для постов"

ИИ: "Конечно! Я создам endpoint для постов.
     Для этого нам понадобится FastAPI...
     [длинное объяснение]
     
     Вот код:
     ```python
     # Create a post endpoint
     def create_post(post):  # No type hints
         return post
     ```
     Этот код делает..."
```

### После Rules

```
Промпт: "Создай endpoint для постов"

ИИ: "```python
     @router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
     async def create_post(
         post_data: PostCreate,
         db: AsyncSession = Depends(get_db),
         current_user: User = Depends(get_current_user)
     ) -> PostResponse:
         post = Post(**post_data.model_dump(), author_id=current_user.id)
         db.add(post)
         await db.commit()
         await db.refresh(post)
         return post
     ```
     
     Endpoint создаёт пост с авторизацией."
```

---

## 🎉 Итоги недели 4

### Что ты узнал:

| День | Навык |
|------|-------|
| 1 | RAG — автоматический поиск файлов |
| 2 | @Codebase — поиск и понимание кода |
| 3 | Rules — системные инструкции для ИИ |
| 4 | Создание персонализированных Rules |
| 5 | Практика: Rules + @Codebase вместе |

### Ключевые принципы:

```
✅ RAG — ИИ-библиотекарь, сам находит нужный код
✅ @Codebase — автоматический поиск по проекту
✅ Rules — инструкции, которые ИИ следует всегда
✅ Комбинация Rules + @Codebase = максимум эффективности
✅ Локальные модели медленнее при RAG, но приватны
```

---

## 📊 Итоги 4 недель

### Неделя 1: Основы
- Философия Vibe Coding
- Установка Continue.dev
- Выбор модели
- Первые программы

### Неделя 2: Промпт-инжиниринг
- P.T.C.F. модель
- Zero-shot vs Few-shot
- Chain of Thought
- AI Debugging

### Неделя 3: Инженерия контекста
- Context is King
- @Files, @Folder, @Terminal
- Чтение чужого кода
- Работа с терминалом

### Неделя 4: Продвинутый контекст
- RAG (@Codebase)
- Rules
- Персонализация ИИ
- Комбинация техник

---

## Что дальше?

**Недели 5-8:** (Coming Soon)
- MCP (Model Context Protocol)
- Real Project Build
- AI Debugging & Refactoring
- Final Project

---

## Checklist дня ✅

- [ ] Создал Rules для проекта
- [ ] Тест 1: Создание модели
- [ ] Тест 2: Создание endpoint
- [ ] Тест 3: Поиск и рефакторинг
- [ ] Тест 4: Добавление функционала
- [ ] Проверил, что ИИ следует Rules
- [ ] Увидел разницу До/После Rules

---

📚 [На предыдущий день ←](./Day_4.md)
