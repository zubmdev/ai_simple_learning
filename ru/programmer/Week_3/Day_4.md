# День 4: AI Debugging Workflow 🐛

**Трек:** 👨‍💻 Программист | **Время:** 25 минут

---

## 🎯 Цель

Автоматизировать debugging через @Terminal и продвинутые промпты.

---

## 📋 Workflow

```
1. Запусти код → Ошибка
2. @Terminal в Continue
3. ИИ анализирует
4. Предлагает решение
5. Итерация если нужно
```

---

## 🔬 Структура debugging промпта

### Минимальный

```
@Terminal

Объясни ошибку и как исправить.
```

### Продвинутый

```
@Files: main.py, utils.py
@Terminal

Root cause analysis:
1. Где ошибка? (файл, строка)
2. Почему возникает? (логическая причина)
3. Как исправить? (конкретное решение)

Предложи исправленный код с обработкой edge cases.
```

---

## 🛠️ Практика

### Кейс 1: ZeroDivisionError

```python
# error1.py
def divide(a, b):
    return a / b

result = divide(10, 0)
```

**Промпт:**

```
@Terminal

Найди root cause.
Предложи defensive programming решение.
```

---

### Кейс 2: ImportError

```python
# error2.py
from nonexistent_module import some_function
some_function()
```

**Промпт:**

```
@Terminal

1. Какая библиотека нужна?
2. Как установить?
3. Есть ли альтернативы?
```

---

### Кейс 3: TypeError

```python
# error3.py
def process(data: dict):
    return data["key"]

process(None)
```

**Промпт:**

```
@Files: error3.py
@Terminal

Добавь:
1. Type checking
2. None handling
3. Error messages

Покажи defensive код.
```

---

## 🧠 Продвинутые техники

### Техника 1: Step-by-step debugging

```
@Files: main.py
@Terminal

Пошаговый анализ:
1. Что происходит на строке X?
2. Какое значение переменной Y?
3. Где логика нарушена?
4. Почему?

Добавь debug prints и покажи.
```

### Техника 2: Prevent debugging

```
@Files: main.py

Проверь код на:
- Potential None values
- Division by zero
- Index out of range
- Type mismatches

Где нужны проверки? Покажи код.
```

### Техника 3: Test-driven debugging

```
@Files: main.py
@Terminal

Напиши pytest тест, который:
1. Воспроизводит ошибку
2. Проверяет edge cases
3. Проверяет исправление

Используй fixtures и parametrize.
```

---

## 📊 Сравнение подходов

| Подход | Время | Качество |
|--------|-------|----------|
| Ручной поиск | 30-60 мин | Зависит от опыта |
| Google/StackOverflow | 10-30 мин | Может не подойти |
| AI Debugging | 1-5 мин | Высокое |

---

## 💡 Best Practices

### 1. Всегда добавляй @Files

```
❌ @Terminal → ИИ не видит код
✅ @Files: main.py + @Terminal → ИИ видит контекст
```

### 2. Ask for explanation

```
@Terminal

Не только исправь, но и объясни:
- Почему возникла ошибка?
- Как предотвратить в будущем?
```

### 3. Request tests

```
@Files: main.py
@Terminal

Исправь ошибку.
Напиши тест, который её поймал бы.
```

---

## 🔧 Пример полного workflow

### Ситуация

```python
# app.py
from flask import Flask, request
app = Flask(__name__)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user = {
        'name': data['name'],
        'email': data['email']
    }
    # Save to database...
    return user

if __name__ == '__main__':
    app.run()
```

**Ошибка:** `TypeError: 'NoneType' object is not subscriptable`

### Промпт

```
@Files: app.py
@Terminal

1. Почему data может быть None?
2. Как обработать?
3. Какие ещё edge cases?
4. Добавь валидацию через Pydantic

Покажи production-ready код.
```

---

## Checklist ✅

- [ ] Освоил базовый debugging промпт
- [ ] Попробовал root cause analysis
- [ ] Научился preventive debugging
- [ ] Использую test-driven debugging
- [ ] Понял best practices

---

📚 [На предыдущий день ←](./Day_3.md) | [На следующий день →](./Day_5.md)
