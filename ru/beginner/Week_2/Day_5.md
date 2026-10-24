# День 5: Daily Mission — Улучшаем скрипт из Недели 1 🚀

Поздравляю! Ты дошёл до финального дня второй недели. Сегодня мы применим все знания о промпт-инжиниринге на практике — улучшим ASCII-арт генератор из Недели 1.

---

## 🎯 Цель дня

Превратить базовый скрипт в production-ready код, используя:
- Анатомию идеального промпта
- Few-shot примеры
- Chain of Thought
- Превентивный дебаггинг

---

## Часть 1: Вспоминаем базовый скрипт

### Текущий код (из Недели 1)

```python
from art import tprint

def main():
    print("=== ASCII Арт Генератор ===")
    print()
    
    while True:
        name = input("Введите ваше имя: ").strip()
        
        if name:
            break
        print("Имя не может быть пустым! Попробуйте снова.")
    
    print()
    print("Ваше имя в ASCII-арте:")
    print()
    
    tprint(name, font="block")

if __name__ == "__main__":
    main()
```

### Проблемы:

- ❌ Нет обработки ошибок
- ❌ Нет выбора стиля
- ❌ Нет сохранения в файл
- ❌ Нет документации
- ❌ Нет type hints
- ❌ Нет тестов

---

## Часть 2: Шаг 1 — Few-shot для стиля

### Задача: Добавить консистентный стиль кода

**Промпт:**

```
Вот примеры функций из моего проекта:

Пример 1:
def get_user_input(prompt: str) -> str:
    """Получает ввод пользователя с валидацией."""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Ввод не может быть пустым!")

Пример 2:
def save_to_file(content: str, filepath: str) -> bool:
    """Сохраняет контент в файл."""
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"Ошибка: {e}")
        return False

Перепиши ASCII-арт генератор в этом стиле:
- Type hints для всех аргументов
- Docstrings в формате Google
- Обработка KeyboardInterrupt
- Валидация входных данных
```

---

## Часть 3: Шаг 2 — Chain of Thought для улучшений

**Промпт:**

```
Улучши ASCII-арт генератор, рассуждая step-by-step:

1. Какие проблемы есть в текущем коде?
2. Какие функции нужно добавить?
3. Какие ошибки нужно обработать?
4. Как улучшить UX?
5. Напиши финальный код с комментариями

Текущий код:
[вставь код]
```

---

## Часть 4: Финальная версия

После применения всех техник:

```python
from art import tprint, FONT_NAMES
from typing import Optional
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_input(prompt: str, validator=None) -> str:
    """Получает ввод пользователя с валидацией."""
    while True:
        try:
            user_input = input(prompt).strip()
            if validator is None or validator(user_input):
                return user_input
            print("Некорректный ввод!")
        except KeyboardInterrupt:
            print("\nОтмена.")
            sys.exit(0)

def validate_name(name: str) -> bool:
    """Валидирует имя: не пустое, разумная длина."""
    return 1 <= len(name) <= 50

def select_style() -> str:
    """Предлагает выбор стиля ASCII-арта."""
    styles = ["block", "standard", "slant", "banner"]
    
    print("\nВыберите стиль:")
    for i, style in enumerate(styles, 1):
        print(f"{i}. {style}")
    
    choice = get_user_input("Номер стиля (1-4): ")
    return styles[int(choice) - 1] if choice in "1234" else "block"

def save_result(ascii_art: str) -> None:
    """Сохраняет результат в файл."""
    save = get_user_input("Сохранить в файл? (да/нет): ")
    if save.lower() in ["да", "yes", "y"]:
        try:
            with open("ascii_result.txt", "w") as f:
                f.write(ascii_art)
            print("Сохранено в ascii_result.txt")
        except IOError as e:
            logger.error(f"Ошибка сохранения: {e}")

def main() -> None:
    """Главная функция."""
    print("=" * 40)
    print("     ASCII Арт Генератор v2.0")
    print("=" * 40)
    
    name = get_user_input("Введите имя: ", validate_name)
    style = select_style()
    
    print(f"\nГенерирую '{name}' в стиле '{style}'...\n")
    
    try:
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = result = StringIO()
        tprint(name, font=style)
        sys.stdout = old_stdout
        
        ascii_art = result.getvalue()
        print(ascii_art)
        
        save_result(ascii_art)
        
    except Exception as e:
        logger.error(f"Ошибка генерации: {e}")
        sys.exit(1)
    
    print("\nСпасибо за использование!")

if __name__ == "__main__":
    main()
```

---

## Часть 5: Unit-тесты

**Промпт:**

```
Напиши unit-тесты для ASCII-арт генератора с использованием pytest.
Покрой тестами:
- Валидацию имени
- Выбор стиля
- Сохранение в файл
- Обработку ошибок
```

**Результат:**

```python
import pytest
from io import StringIO
from unittest.mock import patch, mock_open
from ascii_art import validate_name, select_style, save_result

def test_validate_name():
    assert validate_name("Max") == True
    assert validate_name("") == False
    assert validate_name("A" * 51) == False

def test_select_style():
    with patch('builtins.input', return_value='1'):
        assert select_style() == "block"
    
    with patch('builtins.input', return_value='5'):
        assert select_style() == "block"

def test_save_result():
    with patch('builtins.input', return_value='да'):
        with patch('builtins.open', mock_open()) as mock_file:
            save_result("test art")
            mock_file.assert_called_once()
```

---

## Итоги недели 2 🎉

### Что ты узнал:

- ✅ Анатомию идеального промпта (Роль, Задача, Контекст, Ограничения)
- ✅ Разницу Zero-shot и Few-shot
- ✅ Chain of Thought для сложных задач
- ✅ Дебаггинг через промпты

### Твои навыки:

| Навык | Уровень |
|-------|---------|
| Составление промптов | ⭐⭐⭐⭐ |
| Few-shot | ⭐⭐⭐ |
| Chain of Thought | ⭐⭐⭐ |
| Дебаггинг | ⭐⭐⭐ |

---

## Checklist дня ✅

- [ ] Улучшил ASCII-арт генератор
- [ ] Применил Few-shot
- [ ] Использовал Chain of Thought
- [ ] Добавил обработку ошибок
- [ ] Написал тесты

---

**На следующей неделе:** Context Engineering — как давать ИИ правильные файлы и данные для работы.

---

📚 [На предыдущий день ←](./Day_4.md)
