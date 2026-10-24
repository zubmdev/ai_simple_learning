# День 3: Системные промпты и Rules 📋

**Трек:** 🌱 Начинающий | **Время:** 35 минут

---

## 🎯 Цель дня

Понять, что такое системные промпты и Rules, и зачем они нужны.

---

## Часть 1: Проблема повторений

### Ситуация

Каждый раз ты пишешь одно и то же:

```
Промпт 1:
"Напиши код на Python с type hints, docstrings в Google формате,
используя async/await. Не пиши очевидных комментариев."

Промпт 2:
"Напиши код на Python с type hints, docstrings в Google формате,
используя async/await. Не пиши очевидных комментариев."

Промпт 3:
"Напиши код на Python с type hints, docstrings в Google формате..."
```

### Решение: Rules

```
Создай файл с правилами ОДИН РАЗ:
→ ИИ будет следовать им ВСЕГДА
```

---

## Часть 2: Что такое Rules?

### Определение

**Rules** (правила) — это инструкции, которые ИИ получает ПЕРЕД каждым ответом.

### Аналогия

```
Rules = Инструкция для нового сотрудника

Когда нанимаешь разработчика:
1. Даёшь ему "гайдлайн" (правила проекта)
2. Он читает ОДИН РАЗ
3. И следует им ВСЕГДА

Rules работают так же для ИИ!
```

### Как это работает

```
1. Ты создаёшь файл правил (.continuerules или в config.json)
2. При каждом запросе Continue добавляет правила в контекст
3. ИИ следует правилам автоматически
4. Тебе не нужно напоминать каждый раз
```

---

## Часть 3: Где хранить Rules в Continue.dev

### Способ 1: config.json

Открой настройки Continue:

1. `Ctrl+L` → Открой Continue
2. Нажми ⚙️ (шестерёнка)
3. Выбери "Open config.json"

Добавь раздел `"rules"`:

```json
{
  "models": [...],
  "rules": [
    {
      "name": "Python Style",
      "rule": "Always use type hints, Google-style docstrings, and async/await in Python code."
    },
    {
      "name": "No Obvious Comments",
      "rule": "Don't write comments for obvious code like 'increment counter' or 'return result'."
    },
    {
      "name": "Short Responses",
      "rule": "Keep responses concise. Don't explain things that are self-explanatory."
    }
  ]
}
```

### Способ 2: .continuerules файл

Создай файл `.continuerules` в корне проекта:

```
# Python Style
Always use type hints for all function parameters and return types.
Use Google-style docstrings.
Prefer async/await over sync code.

# Code Quality
Don't write obvious comments.
Use meaningful variable names.
Keep functions under 30 lines.

# Response Style
Be concise.
Show code first, then brief explanation.
Use bullet points for lists.
```

---

## Часть 4: Примеры Rules

### Rule 1: Стиль кода

```json
{
  "name": "Code Style",
  "rule": "Use Python 3.10+ syntax (match/case, type union with |). Always add type hints. Use Google docstring format. Prefer list/dict comprehensions over loops when readable."
}
```

**До Rules:**
```
Ты: "Напиши функцию"
ИИ: *пишет без type hints*
```

**После Rules:**
```
Ты: "Напиши функцию"
ИИ: *пишет с type hints автоматически*
```

---

### Rule 2: Фреймворк

```json
{
  "name": "Framework",
  "rule": "Always use FastAPI for API endpoints. Use SQLAlchemy for database. Use Pydantic for schemas. Follow the project structure: api/, models/, schemas/, services/."
}
```

**Результат:**
```
Ты: "Создай endpoint для пользователей"
ИИ: *автоматически использует FastAPI + Pydantic*
```

---

### Rule 3: Формат ответа

```json
{
  "name": "Response Format",
  "rule": "Always show code first, then brief explanation. Use bullet points for lists. Maximum 3 sentences for explanations. Don't explain obvious things."
}
```

**До Rules:**
```
ИИ: "Конечно! Я с радостью помогу тебе создать функцию.
     Эта функция будет выполнять следующие действия...
     [длинное объяснение]
     Вот код:"
```

**После Rules:**
```
ИИ: "Вот код:
     ```python
     def example():
         pass
     ```
     Функция делает X."
```

---

### Rule 4: Безопасность

```json
{
  "name": "Security",
  "rule": "Never hardcode secrets, passwords, or API keys. Use environment variables. Validate all user inputs. Use parameterized queries for SQL. Never use eval() or exec()."
}
```

---

### Rule 5: Тестирование

```json
{
  "name": "Testing",
  "rule": "Always write unit tests for new functions using pytest. Include edge cases tests. Aim for 80%+ coverage. Use fixtures for setup."
}
```

---

## Часть 5: Практика — создаём первые Rules

### Задание

Создай Rules для своего проекта.

**Шаг 1:** Открой config.json

```
Ctrl+L → ⚙️ → Open config.json
```

**Шаг 2:** Добавь базовые Rules

```json
{
  "rules": [
    {
      "name": "Language",
      "rule": "Always respond in Russian."
    },
    {
      "name": "Code Style",
      "rule": "Use type hints for Python code. Add docstrings for functions. Keep functions short (under 30 lines)."
    },
    {
      "name": "Concise",
      "rule": "Be concise. Don't explain obvious things. Show code first, then brief explanation."
    }
  ]
}
```

**Шаг 3:** Сохрани файл (`Ctrl+S`)

**Шаг 4:** Протестируй

```
Напиши функцию для расчёта факториала.
```

ИИ должен:
- Ответить на русском
- Добавить type hints
- Добавить docstring
- Быть кратким

---

## Часть 6: Rules vs Промпты

| Аспект | Rules | Промпт в чате |
|--------|-------|---------------|
| Применение | Всегда | Один раз |
| Место | config.json или файл | Поле ввода |
| Перезапуск | Не нужно | Нужно каждый раз |
| Контекст | Автоматически | Вручную |

### Когда использовать Rules

```
✅ Правила проекта (стиль, фреймворк)
✅ Формат ответа (краткость, язык)
✅ Повторяющиеся требования
✅ Настройки безопасности
```

### Когда использовать промпты

```
✅ Конкретная задача (один раз)
✅ Специфический контекст
✅ Временные требования
```

---

## Checklist дня ✅

- [ ] Понял, что такое Rules
- [ ] Узнал, где хранить Rules
- [ ] Посмотрел примеры Rules
- [ ] Создал базовые Rules для проекта
- [ ] Протестировал, как Rules влияют на ответы ИИ

---

## Что дальше?

**Завтра (День 4):** Научимся создавать продвинутые Rules для конкретного проекта — фреймворки, паттерны, автоматизация.

**Домашнее задание:**
- Создай 3-5 Rules для своего проекта
- Протестируй с разными промптами
- Запиши, что изменилось в ответах ИИ

---

📚 [На предыдущий день ←](./Day_2.md) | [На следующий день →](./Day_4.md)
