# День 3: Модели — Cloud vs Local 🖥️

**Трек:** 👨‍💻 Программист | **Время:** 20 минут

---

## 🎯 Быстрый выбор

| Твой случай | Рекомендация | Команда |
|-------------|--------------|---------|
| Нет GPU / нужен максимум скорости | **Groq API** | Зарегистрируйся на console.groq.com |
| 4GB GPU | **Ollama Qwen 1.5B/3B** | `ollama pull qwen2.5-coder:3b` |
| 8GB+ GPU / Mac M1/M2 16GB+ | **Ollama Llama 3.1 / Qwen 7B** | `ollama pull qwen2.5-coder:7b` |

---

## 🟢 Вариант 1: Groq API (Cloud)

### Почему Groq?

- 🆓 Бесплатный tier: ~14,400 запросов/день
- ⚡ До 500 токенов/сек
- 🔧 OpenAI-совместимый API

### Настройка

```bash
# 1. Получи API key: https://console.groq.com/keys
# 2. Добавь в config.json:
```

```json
{
  "models": [
    {
      "title": "Groq Llama 3.1 70B",
      "provider": "groq",
      "model": "llama-3.1-70b-versatile",
      "apiKey": "${GROQ_API_KEY}"
    }
  ]
}
```

### Рекомендуемые модели Groq

| Модель | Для чего | VRAM |
|--------|----------|------|
| `llama-3.1-70b-versatile` | Сложные задачи, код | Cloud |
| `llama-3.1-8b-instant` | Быстрые ответы | Cloud |
| `llama-3.2-90b-vision-preview` | Multimodal | Cloud |

---

## 🟡 Вариант 2: Ollama (Local)

### Установка Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: скачай с https://ollama.ai/download
# Или через winget
winget install Ollama.Ollama
```

### Модели по VRAM

| VRAM | Модель | Размер | Качество |
|------|--------|--------|----------|
| 2GB | `qwen2.5-coder:1.5b` | 1GB | ⭐⭐⭐ |
| 4GB | `qwen2.5-coder:3b` | 2GB | ⭐⭐⭐⭐ |
| 8GB | `llama3.1:8b` | 4.7GB | ⭐⭐⭐⭐ |
| 8GB | `qwen2.5-coder:7b` | 4.7GB | ⭐⭐⭐⭐⭐ |
| 16GB | `deepseek-coder-v2` | 9GB | ⭐⭐⭐⭐⭐ |

### Проверка GPU

```bash
# Проверь, что GPU используется
ollama run qwen2.5-coder:3b --verbose

# Должно быть: GPU BLAS = 1
```

### Настройка Continue

```json
{
  "models": [
    {
      "title": "Qwen 2.5 Coder 7B",
      "provider": "ollama",
      "model": "qwen2.5-coder:7b"
    }
  ]
}
```

---

## 📊 Сравнение

| Критерий | Groq | Ollama Small | Ollama Large |
|----------|------|--------------|--------------|
| Цена | 🆓 Freemium | 🆓 Бесплатно | 🆓 Бесплатно |
| Приватность | ⚠️ Cloud | 🔒 Локально | 🔒 Локально |
| Оффлайн | ❌ Нет | ✅ Да | ✅ Да |
| Скорость | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡ | ⚡⚡⚡ |
| Качество кода | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔧 Проверка

```bash
# Для Groq
curl -H "Authorization: Bearer $GROQ_API_KEY" \
  https://api.groq.com/openai/v1/models

# Для Ollama
ollama list
```

---

## ✅ Checklist

- [ ] Выбрал путь (Groq / Ollama)
- [ ] Установил (Ollama) или зарегистрировался (Groq)
- [ ] Получил API key (Groq) или скачал модель (Ollama)
- [ ] Добавил в config.json
- [ ] Проверил: AI отвечает на промпты

---

## Что дальше?

**Завтра (День 4):** AI Workflow — как эффективно работать с промптами.

📚 [На предыдущий день ←](./Day_2.md) | [На следующий день →](./Day_4.md)
