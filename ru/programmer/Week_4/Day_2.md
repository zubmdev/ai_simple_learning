# День 2: @Codebase Deep Dive 🔍

**Трек:** 👨‍💻 Программист | **Время:** 20 минут

---

## 🎯 Цель

Освоить продвинутые техники @Codebase.

---

## 🔬 Как работает @Codebase в Continue

### Process

```
1. User types @Codebase + question
2. Continue embeds question
3. Vector search in indexed code
4. Retrieve top-K chunks (default: 10)
5. Add chunks to context
6. LLM generates response
```

### Configuration

```json
{
  "contextProviders": [
    {
      "name": "codebase",
      "params": {
        "nRetrieve": 20,  // Сколько чанков искать
        "nFinal": 10      // Сколько передать в LLM
      }
    }
  ]
}
```

---

## 🛠️ Продвинутые техники

### 1. Архитектурный анализ

```
@Codebase

Построй dependency graph:
1. Какие модули зависят от каких?
2. Есть ли circular dependencies?
3. Самые связанные модули?
4. Точка входа?

Покажи диаграмму.
```

### 2. Поиск паттернов

```
@Codebase

Найди использование паттернов:
- Repository pattern
- Factory pattern
- Singleton
- Observer

Где применяются? Корректно ли?
```

### 3. Security audit

```
@Codebase

Найди security issues:
- Hardcoded secrets
- SQL injection risks
- XSS vulnerabilities
- Missing authentication
- Insecure dependencies

Prioritize by severity.
```

### 4. Performance analysis

```
@Codebase

Найди performance bottlenecks:
- N+1 queries
- Missing indexes
- Synchronous operations (should be async)
- Large data transfers
- Unnecessary loops

Покажи файлы и строки.
```

---

## 📊 Комбинации

### @Codebase + @Terminal

```
@Codebase
@Terminal

Ошибка при запуске.
Найди:
1. Какой endpoint?
2. Какая функция?
3. Root cause?
4. Fix?
```

### @Codebase + @Files

```
@Codebase
@Files: config.py

Найди все использования config из config.py.
Проверь consistency.
```

---

## 🧠 Best Practices

### 1. Specific questions

```
❌ @Codebase "Что делать?"
✅ @Codebase "Где функция process_payment и какие edge cases обрабатывает?"
```

### 2. Combine with context

```
@Codebase
@Files: main.py

В main.py используется get_user.
Найди все места, где get_user вызывается.
Проверь, везде ли обработан None.
```

### 3. Incremental refinement

```
1. @Codebase "Где авторизация?" → Общий ответ
2. @Codebase "Функция login в auth.py — покажи все вызовы" → Конкретный
```

---

## ⚡ Performance Tips

### Large projects (500+ files)

```
1. Фильтруй:
   @Codebase в папке src/api (используй @Folder)

2. Уменьши nRetrieve:
   "nRetrieve": 10 → быстрее, но меньше контекста

3. Используй API:
   Groq быстрее для больших проектов
```

### Local models (Ollama)

```
4GB GPU:
- Проекты до 50 файлов — OK
- 50-200 файлов — медленно
- 200+ файлов — используй API

16GB GPU:
- До 200 файлов — OK
- 200-500 — медленно
- 500+ — API
```

---

## 🛠️ Практика

### Задание: Refactoring через @Codebase

**1. Открой любой проект**

**2. Запусти:**

```
@Codebase

Найди все функции, которые:
- Длиннее 30 строк
- Принимают больше 3 аргументов
- Не имеют docstring

Создай список для рефакторинга.
```

**3. Рефактори:**

```
@Codebase
@Files: [найденные файлы]

Рефакторинг:
1. Разбей большие функции
2. Уменьши количество аргументов
3. Добавь docstrings

Покажи изменения.
```

---

## Checklist ✅

- [ ] Понял как работает @Codebase
- [ ] Освоил продвинутые техники
- [ ] Попробовал комбинации
- [ ] Усвоил best practices
- [ ] Понял performance implications

---

📚 [На предыдущий день ←](./Day_1.md) | [На следующий день →](./Day_3.md)
