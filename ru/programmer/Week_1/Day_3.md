# День 3: Модели — Cloud vs Local 🖥️

**Трек:** 👨‍💻 Программист | **Время:** 20 минут

---

## 🎯 Быстрый выбор

| Твой случай | Рекомендация | Команда |
|-------------|--------------|---------|
| Нет GPU / нужен максимум скорости | **Groq API** | Зарегистрируйся на console.groq.com |
| 4GB GPU | **Ollama Qwen3.5 2B** | `ollama pull qwen3.5:2b` |
| 8GB+ GPU / Mac M1/M2 16GB+ | **Ollama GPT-OSS 20B** | `ollama pull gpt-oss:20b` |

---

## 🟢 Вариант 1: Groq API (Cloud)

### Почему Groq?

- 🆓 Бесплатный tier: ~1000 запросов/день на модель
- ⚡ До 1000 токенов/сек (gpt-oss-20b)
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
      "title": "Groq GPT-OSS 20B",
      "provider": "groq",
      "model": "openai/gpt-oss-20b",
      "apiKey": "${GROQ_API_KEY}"
    }
  ]
}
```

### Рекомендуемые модели Groq

| Модель | Для чего | VRAM |
|--------|----------|------|
| `openai/gpt-oss-20b` | Основная: код, агентные задачи | Cloud |
| `openai/gpt-oss-120b` | Сложные задачи, сильные рассуждения | Cloud |
| `qwen/qwen3.8-27b` | Свежий Qwen (preview — может исчезнуть) | Cloud |

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
| 2GB | `qwen3.5:0.8b` | 1.2GB | ⭐⭐⭐ |
| 4GB | `qwen3.5:2b` | 3GB | ⭐⭐⭐⭐ |
| 8GB | `qwen3:8b` | 5.2GB | ⭐⭐⭐⭐ |
| 12GB | `gemma4:12b` | 8GB | ⭐⭐⭐⭐⭐ |
| 16GB | `gpt-oss:20b` | 14GB | ⭐⭐⭐⭐⭐ |

### Проверка GPU

```bash
# Проверь, что GPU используется
ollama run qwen3.5:2b --verbose

# Должно быть: GPU BLAS = 1
```

### Настройка Continue

```json
{
  "models": [
    {
      "title": "GPT-OSS 20B",
      "provider": "ollama",
      "model": "gpt-oss:20b"
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
