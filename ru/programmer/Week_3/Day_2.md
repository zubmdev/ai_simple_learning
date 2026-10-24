# День 2: @Files, @Folder, @Terminal 🎛️

**Трек:** 👨‍💻 Программист | **Время:** 25 минут

---

## 📋 Context Providers в Continue

### Overview

| Provider | Синтаксис | Use Case |
|----------|-----------|----------|
| Files | `@Files: file1.py, file2.py` | Конкретные файлы |
| Folder | `@Folder: src/api` | Модуль целиком |
| Terminal | `@Terminal` | Вывод терминала |

---

## 📂 @Files

### Синтаксис

```
@Files: file1.py, file2.py, file3.py

[Твой промпт]
```

### UI

```
📎 (иконка скрепки) → Files → Выбрать файлы
```

### Примеры

```
@Files: models/user.py, api/users.py

Добавь endpoint PATCH /users/{id} для частичного обновления.
Используй Pydantic model для partial update.
```

---

## 📁 @Folder

### Синтаксис

```
@Folder: path/to/folder

[Твой промпт]
```

### Когда использовать

```
✅ Понять структуру модуля
✅ Найти паттерны в коде
✅ Не знаешь, какие файлы нужны

❌ Большие папки (50+ файлов)
❌ Нужны конкретные файлы
```

### Примеры

```
@Folder: src/services

Объясни архитектуру сервисного слоя.
Какие паттерны используются?
Как улучшить?
```

---

## 💻 @Terminal

### Синтаксис

```
@Terminal

[Твой промпт]
```

### Workflow

```
1. Запусти код → Ошибка
2. Не закрывай терминал
3. @Terminal в Continue
4. ИИ увидит traceback
```

### Примеры

```
@Terminal

Root cause analysis:
1. Где ошибка?
2. Почему возникает?
3. Как исправить?

Покажи исправленный код.
```

---

## 🔗 Комбинации

### @Files + @Terminal

```
@Files: main.py, database.py
@Terminal

Проанализируй ошибку и предложи решение.
```

### @Folder + @Files

```
@Folder: src/models
@Files: config.py

Создай новую модель Product, следуя стилю.
Используй конфиг из config.py.
```

---

## 📊 Сравнение

| Provider | Скорость | Точность | Use Case |
|----------|----------|----------|----------|
| @Files | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Конкретные файлы |
| @Folder | ⚡⚡ | ⭐⭐⭐⭐ | Модули |
| @Terminal | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Debugging |
| @Codebase | ⚡ | ⭐⭐⭐ | Автопоиск |

---

## 💡 Best Practices

### 1. Minimize context

```
❌ @Files: file1.py, file2.py, ..., file10.py
✅ @Files: main.py, models.py
```

### 2. Check what you added

```
После добавления:
1. Кликни "Контекст"
2. Проверь список файлов
3. Удали лишнее (✕)
```

### 3. Local models are slower

```
Ollama (4GB/16GB GPU):
- Больше файлов → дольше обработка
- Для больших проектов → API быстрее
```

---

## 🛠️ Практика

### Упражнение 1: @Files

```
1. Создай файл test.py:

def greet(name: str) -> str:
    return f"Hello, {name}!"

2. В Continue:
@Files: test.py
Добавь функцию calculate(a, b) → int (умножение)

3. Проверь, что ИИ следует стилю
```

### Упражнение 2: @Terminal

```
1. Запусти:
python -c "print(1/0)"

2. В Continue:
@Terminal
Объясни ошибку и как избежать.

3. Сравни с ручным копированием
```

---

## Checklist ✅

- [ ] Освоил @Files
- [ ] Освоил @Folder
- [ ] Освоил @Terminal
- [ ] Попробовал комбинации
- [ ] Понял best practices

---

📚 [На предыдущий день ←](./Day_1.md) | [На следующий день →](./Day_3.md)
