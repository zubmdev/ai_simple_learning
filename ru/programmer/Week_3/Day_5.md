# День 5: Практика — Open Source Модификация 🚀

**Трек:** 👨‍💻 Программист | **Время:** 35 минут

---

## 🎯 Миссия

Модифицировать open-source проект через AI — без ручного поиска кода.

---

## 📋 Задачи

1. Скачать простой проект
2. Понять архитектуру через AI
3. Найти нужный код через @Codebase
4. Модифицировать через AI
5. Запустить и проверить

---

## 🛠️ Практика

### Шаг 1: Создай проект

```bash
mkdir todo-cli
cd todo-cli
```

Создай `todo.py`:

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
    print(f"Added: {text}")

def list_todos():
    todos = load_todos()
    for i, todo in enumerate(todos, 1):
        status = "✓" if todo["done"] else " "
        print(f"{i}. [{status}] {todo['text']}")

def main():
    print("Todo CLI")
    while True:
        cmd = input("> ").strip().split(maxsplit=1)
        if not cmd:
            continue
        if cmd[0] == "add" and len(cmd) > 1:
            add_todo(cmd[1])
        elif cmd[0] == "list":
            list_todos()
        elif cmd[0] == "exit":
            break

if __name__ == "__main__":
    main()
```

---

### Шаг 2: Понять код

```
@Files: todo.py

Объясни архитектуру:
1. Какие функции?
2. Как хранятся данные?
3. Какие команды поддерживаются?
4. Что можно улучшить?
```

---

### Шаг 3: Задание 1 — Добавить цвета

```
@Files: todo.py

Добавь colorama для:
- "Added: X" → зелёный
- "Todo CLI" → cyan
- Done задачи → зелёный
- Undone задачи → белый

Перепиши весь код.
```

---

### Шаг 4: Задание 2 — Добавить категории

```
@Files: todo.py

Добавь категории:
- Формат: "add work:Task"
- Категории: work, personal, shopping, other
- Цвета: work=синий, personal=зелёный, shopping=жёлтый
- Команда: "list work" → фильтр по категории

Обнови структуру и все функции.
```

---

### Шаг 5: Задание 3 — Добавить приоритеты

```
@Files: todo.py

Добавь приоритеты:
- Формат: "add work:high:Task"
- Приоритеты: high, normal, low (default: normal)
- Сортировка по приоритету
- Цвета: high=красный, normal=белый, low=серый

Обнови всё.
```

---

### Шаг 6: Финальный промпт (всё вместе)

```
@Files: todo.py

Полный рефакторинг:

1. Цвета (colorama):
   - Заголовки: cyan
   - Успех: зелёный
   - Ошибки: красный

2. Категории:
   - work, personal, shopping, other
   - Цвета для каждой

3. Приоритеты:
   - high, normal, low
   - Сортировка
   - Цвета

4. Команды:
   - add <cat>:<priority>:<text>
   - list [category]
   - done <num>
   - delete <num>
   - stats
   - exit

5. Хранение:
   - Папка todos/
   - Файлы по категориям

6. UI:
   - ASCII art заголовок
   - Таблица в list
   - Подсветка

Напиши полный production-ready код.
```

---

## 📊 Checklist

### Before AI

```
❌ Ручной поиск функций: 30 мин
❌ Понимание структуры: 20 мин
❌ Написание кода: 60 мин
❌ Debugging: 30 мин
Total: 140 мин
```

### With AI

```
✅ Понимание: 2 мин (@Files)
✅ Задание 1: 3 мин
✅ Задание 2: 5 мин
✅ Задание 3: 5 мин
✅ Финальный: 10 мин
Total: 25 мин
```

**Экономия: ~2 часа!**

---

## 🎉 Итоги недели 3

### Навыки

| День | Навык |
|------|-------|
| 1 | Context Engineering |
| 2 | Context Providers (@Files, @Folder, @Terminal) |
| 3 | Reading legacy code |
| 4 | AI Debugging |
| 5 | Open source modification |

### Ключевые принципы

```
✅ Context is King
✅ Избегай Context Bloat
✅ Используй нужный provider
✅ AI для understanding + modification
✅ Итеративный подход
```

---

## Checklist ✅

- [ ] Создал проект
- [ ] Понял архитектуру через AI
- [ ] Добавил цвета
- [ ] Добавил категории
- [ ] Добавил приоритеты
- [ ] Запустил и проверил

---

📚 [На предыдущий день ←](./Day_4.md) | [На следующую неделю →](../Week_4.md)
