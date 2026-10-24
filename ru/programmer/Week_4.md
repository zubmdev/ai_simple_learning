# Неделя 4: RAG и Rules ⚙️

**Трек:** 👨‍💻 Программист | **Время:** ~1.5 часа

---

## 📋 План недели

| День | Тема | Время | Статус |
|------|------|-------|--------|
| [День 1](./Week_4/Day_1.md) | RAG — AI Librarian | 15 мин | ⬜ |
| [День 2](./Week_4/Day_2.md) | @Codebase Deep Dive | 20 мин | ⬜ |
| [День 3](./Week_4/Day_3.md) | Rules & System Prompts | 20 мин | ⬜ |
| [День 4](./Week_4/Day_4.md) | Custom Rules for Project | 25 мин | ⬜ |
| [День 5](./Week_4/Day_5.md) | Практика: Rules + @Codebase | 30 мин | ⬜ |

---

## 🎯 Цели недели

- ✅ Понять RAG на техническом уровне
- ✅ Освоить @Codebase для больших проектов
- ✅ Создать персонализированные Rules
- ✅ Автоматизировать стиль кода через Rules
- ✅ Комбинировать RAG + Rules для эффективности

---

## ⚡ TL;DR

### RAG

```
RAG = Retrieval-Augmented Generation

1. Index: Embed all code
2. Retrieve: Find relevant chunks
3. Augment: Add to context
4. Generate: AI response
```

### @Codebase

```
@Codebase → Автоматический поиск по проекту
- Не знаешь, где код? @Codebase
- Понять архитектуру? @Codebase
- Найти все использования? @Codebase
```

### Rules

```json
{
  "rules": [
    {
      "name": "Style",
      "rule": "Type hints, async/await, Google docstrings"
    }
  ]
}
```

---

## ⚠️ Performance Notes

```
Локальные модели (Ollama):
- RAG работает, но медленнее
- Индексация на CPU/GPU
- Большие проекты → API быстрее

API (Groq/Gemini):
- RAG быстрее
- Данные уходят в облако
- Не подходит для приватных проектов
```

---

## 🚀 Начало работы

👉 [День 1: RAG — AI Librarian](./Week_4/Day_1.md)
