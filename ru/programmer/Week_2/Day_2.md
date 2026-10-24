# День 2: Zero-shot vs Few-shot 🎯

**Трек:** 👨‍💻 Программист | **Время:** 20 минут

---

## 🔬 Zero-shot

**Определение:** Просишь AI выполнить задачу без примеров.

```
Напиши функцию для конвертации JSON в XML.
```

**Когда использовать:**
- Стандартные задачи
- Не важен специфический стиль
- Быстрый прототип

---

## 🔬 Few-shot

**Определение:** Даёшь 1-3 примера для показа желаемого стиля.

```python
Напиши функцию в таком стиле:

Пример 1:
def read_file(path: str) -> str:
    """Читает файл и возвращает содержимое."""
    import logging
    logging.info(f"Reading: {path}")
    with open(path, 'r') as f:
        return f.read()

Пример 2:
def write_file(path: str, content: str) -> None:
    """Записывает содержимое в файл."""
    import logging
    logging.info(f"Writing: {path}")
    with open(path, 'w') as f:
        f.write(content)

Теперь напиши функцию append_to_file(path: str, content: str) -> None
```

**Когда использовать:**
- Нужен специфический стиль
- Консистентность в проекте
- Нестандартные требования

---

## 📊 Сравнение

| Аспект | Zero-shot | Few-shot |
|--------|-----------|----------|
| Скорость написания | ⚡ Быстро | 🐢 Медленно |
| Контроль стиля | ❌ Нет | ✅ Полный |
| Консистентность | ⚠️ Средняя | ✅ Высокая |
| Сложность | 🟢 Низкая | 🟡 Средняя |

---

## 💡 Best Practice

### Правило 3 примеров

```
1 пример: показывает стиль
2 примера: подтверждает паттерн
3 примера: закрепляет понимание
```

### Пример для проекта

```python
# Создай файл style_examples.md в проекте

def get_user_by_id(user_id: int) -> User | None:
    """Получает пользователя по ID.
    
    Args:
        user_id: ID пользователя
        
    Returns:
        User если найден, иначе None
    """
    return db.query(User).filter_by(id=user_id).first()

def get_user_by_email(email: str) -> User | None:
    """Получает пользователя по email.
    
    Args:
        email: Email пользователя
        
    Returns:
        User если найден, иначе None
    """
    return db.query(User).filter_by(email=email).first()
```

Используй этот файл как reference для Few-shot промптов.

---

## ✅ Checklist

- [ ] Понял разницу Zero-shot и Few-shot
- [ ] Создал Few-shot промпт для своего проекта
- [ ] Сохранил примеры стиля в отдельный файл

---

📚 [На предыдущий день ←](./Day_1.md) | [На следующий день →](./Day_3.md)
