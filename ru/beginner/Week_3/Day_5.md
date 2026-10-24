# День 5: Daily Mission — Modifying Open Source 🚀

**Трек:** 🌱 Начинающий | **Время:** 60 минут

---

## 🎯 Миссия дня

Скачать open-source проект и изменить его с помощью ИИ — без ручного поиска кода.

---

## Часть 1: Подготовка

### Что будем делать

```
1. Скачаем простой open-source проект
2. Попросим ИИ найти нужный код
3. Изменим дизайн без ручного поиска
4. Запустим и проверим
```

### Выбор проекта

Для практики выберем простой проект:
- **todo-cli** — консольный todo список
- **weather-app** — погодное приложение
- **calculator** — калькулятор

---

## Часть 2: Скачиваем проект

### Шаг 1: Создай папку для практики

```bash
mkdir -p ~/vibe-coding-practice
cd ~/vibe-coding-practice
```

### Шаг 2: Скачай простой проект

**Вариант А: Todo CLI (рекомендуется)**

```bash
# Создадим простой todo проект с нуля
mkdir todo-cli
cd todo-cli
```

Создай файл `todo.py`:

```python
import json
import os

TODO_FILE = "todos.json"

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def add_todo(text):
    todos = load_todos()
    todos.append({"text": text, "done": False})
    save_todos(todos)
    print(f"✅ Added: {text}")

def list_todos():
    todos = load_todos()
    if not todos:
        print("No todos yet!")
        return
    for i, todo in enumerate(todos, 1):
        status = "✓" if todo["done"] else " "
        print(f"{i}. [{status}] {todo['text']}")

def complete_todo(index):
    todos = load_todos()
    if 0 < index <= len(todos):
        todos[index - 1]["done"] = True
        save_todos(todos)
        print(f"✅ Completed: {todos[index - 1]['text']}")
    else:
        print("❌ Invalid index")

def main():
    print("📝 Todo CLI")
    print("Commands: add <text>, list, complete <num>, exit")
    
    while True:
        command = input("\n> ").strip().split(maxsplit=1)
        
        if not command:
            continue
        
        if command[0] == "exit":
            print("Goodbye!")
            break
        elif command[0] == "add" and len(command) > 1:
            add_todo(command[1])
        elif command[0] == "list":
            list_todos()
        elif command[0] == "complete" and len(command) > 1:
            complete_todo(int(command[1]))
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
```

### Шаг 3: Открой в VS Code

```bash
code .
```

---

## Часть 3: Задание 1 — Добавляем цвета

### Проблема

Сейчас вывод скучный:

```
📝 Todo CLI
Commands: add <text>, list, complete <num>, exit

> add Buy milk
✅ Added: Buy milk

> list
1. [ ] Buy milk
```

### Цель

Сделать цветным:

```
📝 Todo CLI (зелёный)
Commands: add <text>, list, complete <num>, exit (жёлтый)

> add Buy milk
✅ Added: Buy milk (зелёный)

> list
1. [ ] Buy milk (белый)
```

### Решение через ИИ

В Continue напиши:

```
@Files: todo.py

Добавь цветной вывод с помощью библиотеки colorama:
- Заголовок 📝 Todo CLI — зелёный
- Подсказка Commands — жёлтый
- ✅ сообщения — зелёный
- ❌ сообщения — красный
- Невыполненные задачи — белые
- Выполненные задачи — серые (dim)

Добавь в начало инициализацию colorama.
Перепиши весь код с цветами.
```

### Проверь результат

```bash
pip install colorama
python todo.py
```

---

## Часть 4: Задание 2 — Добавляем категории

### Проблема

Все задачи в одном списке. Нет категорий.

### Цель

Добавить категории: work, personal, shopping

```
> add work:Finish report
✅ Added [work]: Finish report

> add personal:Buy groceries
✅ Added [personal]: Buy groceries

> list
[work] 1. [ ] Finish report
[personal] 2. [ ] Buy groceries

> list work
[work] 1. [ ] Finish report
```

### Решение через ИИ

В Continue напиши:

```
@Files: todo.py

Добавь категории задач:
1. Формат добавления: "add <category>:<text>"
   Категории: work, personal, shopping, other
2. Если категория не указана — "other"
3. Добавь команду "list <category>" для фильтрации
4. В list_todos показывай категорию в скобках: [work]
5. Цвета для категорий:
   - work: синий
   - personal: зелёный
   - shopping: жёлтый
   - other: белый

Обнови структуру данных и все функции.
Перепиши код полностью.
```

---

## Часть 5: Задание 3 — Добавляем приоритеты

### Цель

```
> add work:High:Finish report
✅ Added [work] (HIGH): Finish report

> list
Priority sorting:
[HIGH] [work] 1. [ ] Finish report
[NORMAL] [personal] 2. [ ] Buy groceries
[LOW] [shopping] 3. [ ] Get coffee
```

### Решение через ИИ

В Continue напиши:

```
@Files: todo.py

Добавь приоритеты задач:
1. Формат: "add <category>:<priority>:<text>"
   Приоритеты: high, normal, low (по умолчанию normal)
2. В list сортируй по приоритету (high → normal → low)
3. Показывай приоритет: [HIGH], [NORMAL], [LOW]
4. Цвета:
   - high: красный
   - normal: белый
   - low: серый (dim)

Обнови структуру, функции и вывод.
```

---

## Часть 6: Задание 4 — Сохранение в отдельные файлы

### Цель

Каждая категория в своём файле:

```
todos/
├── work.json
├── personal.json
├── shopping.json
└── other.json
```

### Решение через ИИ

```
@Files: todo.py

Измени хранение:
1. Создай папку todos/ при первом запуске
2. Каждая категория — отдельный JSON файл
3. При add сохраняй в нужный файл
4. При list показывай все или конкретную категорию
5. Добавь команду "stats" — показать статистику по категориям

Обеспечь backwards compatibility с существующим todos.json.
```

---

## Часть 7: Финальный челлендж

### Задание

Объедини все изменения в один финальный промпт:

```
@Files: todo.py

Перепиши todo-cli с улучшениями:

1. Цветной вывод (colorama):
   - Заголовки: зелёный
   - Подсказки: жёлтый
   - Успех: зелёный
   - Ошибки: красный

2. Категории (work, personal, shopping, other):
   - Формат: add <category>:<text>
   - Цвета для каждой категории

3. Приоритеты (high, normal, low):
   - Формат: add <category>:<priority>:<text>
   - Сортировка по приоритету
   - Цвета: high=красный, normal=белый, low=серый

4. Раздельное хранение:
   - Папка todos/
   - Отдельные файлы для категорий

5. Команды:
   - add <category>:<priority>:<text>
   - list [category]
   - complete <num>
   - stats (статистика)
   - exit

6. Красивый UI:
   - ASCII art заголовок
   - Таблица в list
   - Подсветка текущего дня/времени

Напиши полный код с комментариями.
```

---

## Checklist дня ✅

- [ ] Создал todo-cli проект
- [ ] Добавил цвета через ИИ
- [ ] Добавил категории через ИИ
- [ ] Добавил приоритеты через ИИ
- [ ] Научился давать сложные промпты
- [ ] Запустил улучшенный проект

---

## 🎉 Итоги недели 3

### Что ты узнал:

| День | Навык |
|------|-------|
| 1 | Context is King — важность правильного контекста |
| 2 | Управление контекстом (@Files, @Folder, @Terminal) |
| 3 | Чтение чужого кода через ИИ |
| 4 | Дебаггинг через @Terminal |
| 5 | Практика: изменение open-source проекта |

### Ключевые принципы:

```
✅ Контекст — это 80% успеха
✅ Не перегружай ИИ файлами (Context Bloat)
✅ Используй @Files для конкретных файлов
✅ Используй @Folder для понимания структуры
✅ Используй @Terminal для дебаггинга
✅ Комбинируй @ инструменты для сложных задач
```

---

## Что дальше?

**Неделя 4:** Продвинутый контекст — RAG и Rules. Ты научишься:
- Настраивать автоматический поиск файлов (@Codebase)
- Создавать правила для ИИ (аналог .cursorrules)
- Делать ИИ "умнее" для твоего проекта

---

📚 [На предыдущий день ←](./Day_4.md) | [На следующую неделю →](../Week_4.md)
