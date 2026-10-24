# День 1: Context is King — Context Bloat 👑

**Трек:** 👨‍💻 Программист | **Время:** 20 минут

---

## 💡 Главная идея

```
Context = информация, которую ИИ "видит"
Quality of Context → Quality of Response
```

---

## 📊 Context Bloat Problem

### Определение

Context Bloat — перегрузка ИИ ненужной информацией.

### Метрики

| Размер контекста | Время ответа | Качество |
|------------------|--------------|----------|
| 1 файл | ⚡ Быстро | ⭐⭐⭐⭐⭐ |
| 5 файлов | 🚶 Нормально | ⭐⭐⭐⭐ |
| 20 файлов | 🐢 Медленно | ⭐⭐⭐ |
| 100 файлов | 💀 Очень медленно | ⭐⭐ |

### Почему качество падает?

```
Больше файлов → ИИ теряет фокус
Больше токенов → Выше вероятность галлюцинаций
Дольше обработка → Timeout на некоторых API
```

---

## 🔬 Правило оптимального контекста

### Formula

```
Optimal Context = Relevant Files + Minimal Overhead
```

### Алгоритм выбора

```
1. Какой файл правишь? → Добавь
2. Какие файлы он импортирует? → Добавь
3. Нужна конфигурация? → Добавь
4. Остальное? → НЕ добавляй
```

### Пример

```python
# Задача: Изменить функцию get_user в main.py

# main.py импортирует:
from models import User
from database import get_db
from config import settings

# Оптимальный контекст:
@Files: main.py, models.py, database.py
# config.py НЕ нужен, если не меняешь настройки
```

---

## 📋 Практика

### Задача: Определи нужный контекст

#### Кейс 1: Добавить поле в модель

```
Задача: Добавить поле phone в User model

Контекст:
✅ models/user.py
✅ migrations/ (если используешь Alembic)
❌ tests/ (не нужно для изменения модели)
❌ api/ (не нужно для изменения модели)
```

#### Кейс 2: Изменить API endpoint

```
Задача: Добавить pagination в GET /users

Контекст:
✅ api/users.py
✅ schemas/user.py (response model)
✅ services/user.py (если есть business logic)
❌ frontend/ (не связано)
```

#### Кейс 3: Исправить баг

```
Задача: Ошибка "File too large" при upload

Контекст:
✅ upload.py (функция upload)
✅ middleware.py (если есть проверки)
✅ config.py (лимиты размера)
❌ CSS/HTML (не связано с backend)
```

---

## ⚡ Quick Reference

### Когда что использовать

| Контекст | Инструмент |
|----------|------------|
| 1-3 конкретных файла | `@Files` |
| Модуль/папка | `@Folder` |
| Ошибка из терминала | `@Terminal` |
| Не знаешь, где код | `@Codebase` (завтра) |

---

## 💡 Pro Tips

### Tip 1: Check imports

```python
# В файле, который правишь:
from models import User, Post
from services import EmailService

# → Добавь models.py и services.py в контекст
```

### Tip 2: Dependency tree

```
main.py → database.py → config.py

Если правишь database.py:
✅ database.py, config.py
❌ main.py (это downstream)
```

### Tip 3: Tests are separate

```
Код: main.py
Тесты: test_main.py

При изменении кода:
✅ main.py
⏳ test_main.py (ПОСЛЕ изменения кода)
```

---

## Checklist ✅

- [ ] Понял Context Bloat
- [ ] Усвоил правило 3 файлов
- [ ] Попрактиковался определять контекст

---

📚 [На следующий день →](./Day_2.md)
