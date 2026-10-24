# День 1: RAG — AI Librarian 📚

**Трек:** 👨‍💻 Программист | **Время:** 15 минут

---

## 💡 Что такое RAG?

**RAG = Retrieval-Augmented Generation**

```
Традиционный LLM:
Question → LLM → Answer

RAG:
Question → Retrieve Context → LLM + Context → Answer
```

---

## 🔬 Техническое объяснение

### Pipeline

```
1. INDEX PHASE (один раз)
   ├─ Scan all files
   ├─ Chunk text (512-1024 tokens)
   ├─ Generate embeddings
   └─ Store in vector DB

2. RETRIEVE PHASE (каждый запрос)
   ├─ Embed question
   ├─ Vector similarity search
   ├─ Return top-K chunks
   └─ Add to context

3. GENERATE PHASE
   ├─ LLM receives: question + chunks
   └─ Generates answer
```

### Аналогия

```
RAG = Библиотекарь + Книга

Библиотекарь (Retrieval):
- Знает, где все книги
- Находит нужные по запросу

Книга (Context):
- Содержит информацию
- Отдаётся для чтения

Читатель (LLM):
- Читает книгу
- Отвечает на вопрос
```

---

## 📊 RAG vs Manual Context

| Аспект | Manual (@Files) | RAG (@Codebase) |
|--------|-----------------|-----------------|
| Знание файлов | Нужно знать | Авто-поиск |
| Время | ~30 сек на выбор | ~5 сек авто |
| Точность | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Масштаб | Малый (до 10 файлов) | Большой (100+ файлов) |

---

## 🛠️ Как использовать @Codebase

### Синтаксис

```
@Codebase

[Твой вопрос]
```

### Use Cases

```
1. Не знаешь, где код:
   @Codebase
   Где отправляется email?

2. Понять архитектуру:
   @Codebase
   Как работает авторизация?

3. Найти использования:
   @Codebase
   Где используется функция get_user?
```

---

## 🔧 Практика

### Задание: Протестировать RAG

**1. Создай проект:**

```bash
mkdir rag-test && cd rag-test
```

```python
# main.py
from auth import login
from database import get_user
from email_service import send_email

def main():
    user = login("admin", "pass")
    if user:
        send_email(user.email, "Welcome!")
```

```python
# auth.py
def login(username, password):
    # Authentication logic
    pass
```

```python
# email_service.py
def send_email(to, subject):
    # Email sending logic
    pass
```

**2. Открой в VS Code:**

```bash
code .
```

**3. Подожди индексации (30-60 сек)**

**4. Протестируй:**

```
@Codebase

Где происходит отправка email?
Какая функция? Где вызывается?
```

---

## ⚡ Performance Tips

### Для локальных моделей

```
Ollama (4GB/16GB GPU):
- Индексация на CPU
- Поиск на CPU
- Генерация на GPU

Оптимизация:
- Маленькие чанки (512 tokens)
- Ограничь top-K (3-5 chunks)
- Фильтруй по расширениям (*.py, *.ts)
```

### Для больших проектов

```
100+ файлов:
- Рассмотри API (Groq) для RAG
- Или раздели на подпапки (@Folder)
```

---

## 📋 Quick Reference

| Вопрос | Инструмент |
|--------|------------|
| Знаю файлы | `@Files: file1.py, file2.py` |
| Знаю папку | `@Folder: src/api` |
| Не знаю где код | `@Codebase` |
| Ошибка в терминале | `@Terminal` |

---

## Checklist ✅

- [ ] Понял RAG концептуально
- [ ] Узнал technical pipeline
- [ ] Попробовал @Codebase
- [ ] Понял performance implications

---

📚 [На следующий день →](./Day_2.md)
