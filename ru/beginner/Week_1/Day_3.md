# День 3: Выбор "мозга" под твоё железо 🖥️

Сегодня мы подключим ИИ-модель к Continue.dev. У тебя три пути в зависимости от твоего железа. Выбери свой и следуй инструкциям.

---

## 📊 Определи свой путь

### Как узнать, какой путь тебе подходит?

#### Шаг 1: Узнай, есть ли у тебя видеокарта (GPU)

**Windows:**

1. Нажми `Win + R`
2. Введи `dxdiag`
3. Нажми Enter
4. Перейди на вкладку **"Display"**
5. Смотри строку **"Name"** в разделе **"Device"**

![ссылка на изображение: ](https://share.google/VoKxlZ1v2EfNjx18p)

**Или через Task Manager:**
1. Нажми `Ctrl + Shift + Esc`
2. Перейди на вкладку **"Performance"**
3. Слева найди **"GPU 0"**

![ссылка на изображение: ](https://share.google/ibYjJdUoilSv88OSe)

**macOS:**

1. Нажми на яблоко в левом верхнем углу
2. Выбери **"About This Mac"**
3. Смотри строки **"Chip"** или **"Graphics"**

**Linux:**

Открой Terminal и введи:

```bash
# Для NVIDIA GPU
nvidia-smi

# Для всех GPU
lspci | grep -i vga
```

#### Шаг 2: Определи объём видеопамяти (VRAM)

**Windows (NVIDIA):**
```powershell
# Открой PowerShell и введи:
nvidia-smi --query-gpu=memory.total --format=csv
```

**Или через NVIDIA Control Panel:**
1. Правый клик на рабочем столе → **NVIDIA Control Panel**
2. Слева: **System Information**
3. Смотри **"Dedicated Video Memory"**

**macOS:**
- Apple Silicon (M1/M2/M3/M4): Видеопамять — это Unified Memory
  - 8GB RAM = ~4-5GB доступно для GPU
  - 16GB RAM = ~10-12GB доступно для GPU
  - 32GB RAM = ~20-24GB доступно для GPU

---

## 🎯 Выбери свой путь

| Твой случай | Путь | Преимущества |
|------------|------|--------------|
| Нет видеокарты / старый ноутбук | 🟢 **Путь 1: CPU + Free APIs** | Бесплатно, быстро, не грузит систему |
| Видеокарта 4-6GB VRAM | 🟡 **Путь 2: Ollama + Qwen 1.5B/3B** | Локально, приватно, оффлайн |
| Видеокарта 8GB+ VRAM / Mac M1/M2 16GB+ | 🔴 **Путь 3: Ollama + Llama 3.1** | Мощно, качественно, локально |

---

# 🟢 ПУТЬ 1: CPU Only (Бесплатные API)

**Для кого:** Нет видеокарты, старый ноутбук, или просто хочешь попробовать без установки.

**Время настройки:** 10-15 минут
**Стоимость:** Бесплатно (с лимитами)
**Требования:** Стабильный интернет

---

## Вариант 1A: Groq API (Рекомендуется)

### Что такое Groq?

**Groq** — это платформа для супер-быстрого запуска ИИ-моделей. Их особеность — невероятная скорость генерации текста.

**Почему Groq?**
- 🆓 Бесплатный tier с щедрыми лимитами
- ⚡ Очень быстрый (до 500 токенов/сек)
- 🔧 Поддержка популярных моделей (Llama 3.1, Mixtral)
- 🌐 API совместим с OpenAI форматом

**Ограничения бесплатного tier:**
- ~14,400 запросов в день
- ~7 миллионов токенов в минуту (очень много!)
- Требуется интернет

### Шаг 1: Регистрация на Groq

1. Открой браузер и перейди на: **https://console.groq.com**

![Groq console landing page(изображение):](https://share.google/clpHEVXZhee7NQdjT)

2. Нажми **"Sign Up"** или **"Start for Free"**

3. Выбери способ регистрации:
   - **Continue with GitHub** (рекомендуется, если есть аккаунт)
   - **Continue with Google**
   - **Email/Password**

![Groq signup options(изображение):](https://share.google/sikPVlY1DVkP0Lr8P)

4. Если выбрал GitHub:
   - Авторизуйся на GitHub
   - Подтверди доступ к基本信息

5. Подтверди email (если регистрировался через email)

### Шаг 2: Создание API ключа

1. После входа ты попадёшь в **Groq Console**

![Groq console dashboard(изображение):](./images/grok-dashboard.png)

2. Нажми на **"API Keys"** в левом меню

3. Нажми кнопку **"Create API Key"**

![Groq create API key button(изображение):](./images/grok-key.png)

4. Введи имя ключа: `continue-dev` (или любое другое)

5. Нажми **"Submit"** ![Create API Key(изображение):](./images/submit-key.png)

6. **ВАЖНО!** Скопируй ключ прямо сейчас!

![Groq API key copy(изображение):](./images/grok-key-copy.png)

```
⚠️ Ключ показывается только один раз! 
   Скопируй его и сохрани в надёжном месте.
   
   Не делится ключом с другими!
   Не коммить ключ в GitHub!
```

**Где сохранить ключ:**
- Менеджер паролей (1Password, Bitwarden, LastPass)
- Заметки (зашифрованные)
- Файл `.env` в проекте (добавь в `.gitignore`)

### Шаг 3: Подключение Groq к Continue.dev

#### Способ 1: Через настройки Continue

1. Открой VS Code
2. Открой Continue: `Ctrl + L` (или `Cmd + L` на Mac)
3. Нажми на шестерёнку ⚙️ (Settings) в правом верхнем углу панели Continue

![Continue settings gear icon(изображение):](./images/gear-continue.png)

4. Выбери **"Open config.yaml"**

![Continue open config.yaml(изображение):](./images/config-yaml.png)

5. Откроется файл `config.yaml`. Найди раздел `"models"`:

```yaml
models:
  - name: llama
    provider: groq
    model: llama-3.3-70b-versatile
    apiKey: ТВОЙ_API_КЛЮЧ_ЗДЕСЬ
    roles:
      - chat
      - edit
      - autocomplete

```
![config.yaml(изображение):](./images/config-yaml1.png)

6. Замени `ТВОЙ_API_КЛЮЧ_ЗДЕСЬ` на твой скопированный ключ

7. Сохрани файл: `Ctrl + S`

<!-- #### Способ 2: Через переменную окружения (безопаснее)

**Windows (PowerShell):**

```yaml
models:
  - name: llama
    provider: groq
    model: llama-3.3-70b-versatile
    apiKey: ${GROQ_API_KEY}
    roles:
      - chat
      - edit
      - autocomplete

```

```powershell
# Установи переменную окружения (текущая сессия)
$env:GROQ_API_KEY = "твой_ключ_здесь"

# Или постоянно (для всех сессий)
[System.Environment]::SetEnvironmentVariable('GROQ_API_KEY', 'твой_ключ_здесь', 'User')
```

**macOS/Linux (bash/zsh):**

```bash
# Добавь в ~/.bashrc или ~/.zshrc
export GROQ_API_KEY="твой_ключ_здесь"

# Примени изменения
source ~/.bashrc  # или source ~/.zshrc
``` -->


### Шаг 4: Проверка работы

1. Перезапусти VS Code (если использовал переменную окружения)
2. Открой Continue: `Ctrl + L`![Выбери установленную llama: ](./images/choosing-llama.png)
3. В поле ввода напиши: `Привет! Напиши "Hello World" на Python`
4. Нажми Enter или кнопку отправки

**✅ Если ИИ ответил — всё работает!**

### Рекомендуемые модели Groq

| Модель | Размер | Скорость | Качество | Для чего |
|--------|--------|----------|----------|----------|
| `llama-3.3-70b-versatile` | 70B | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Сложные задачи, код |
| `llama-3.1-8b-instant` | 8B | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Быстрые ответы |

**Рекомендация для кодинга:** `llama-3.3-70b-versatile`

[список доступных моделей в grok: ](https://console.groq.com/docs/models)

---

## Вариант 1B: Google Gemini API (Альтернатива)

### Что такое Gemini?

**Gemini** — это ИИ-модель от Google. Доступна бесплатно через Google AI Studio.

**Почему Gemini?**
- 🆓 Бесплатный tier
- 🧠 Современная модель
- 📝 Большое контекстное окно (1M токенов)
- 🌐 Интеграция с Google сервисами

### Шаг 1: Регистрация

1. Перейди на: **https://aistudio.google.com**

![Google AI Studio landing(изображение):](./images/google-studio.png)

2. Нажми **"Get API key in Google AI Studio"**

3. Войди в Google аккаунт

4. Нажми **"Create API Key"**

![Gemini create API key(изображение):](./images/create-key-google.png)

5. Выбери проект или создай новый

6. Скопируй API ключ

### Шаг 2: Подключение к Continue

#### Используйте VPN!!!

В `config.yaml`:

```yaml
models:
  - name: Gemini 3.1 Flash
    provider: gemini
    model: gemini-3.1-flash-lite-preview
    apiKey: ТВОЙ_GEMINI_API_КЛЮЧ
    roles:
      - chat
      - edit
      - autocomplete

```

### Рекомендуемые модели Gemini

`gemini-3.1-flash-lite-preview`(Text, Image, Video, Audio, and PDF)

---

## Вариант 1C: Hugging Face Inference API (Ещё альтернатива)

### Что такое Hugging Face?

**Hugging Face** — это платформа для ML моделей. Бесплатный inference API для многих моделей.

1. Зарегистрируйся: **https://huggingface.co/join**
2. Получи токен: Settings → Access Tokens → New token
3. Выбери модель: **https://huggingface.co/models**
4. В Continue:

```yaml
models:
  - name: Qwen
    provider: huggingface-inference
    model: Qwen/Qwen2.5-Coder-32B-Instruct
    apiKey: ТВОЙ_HUGGINGFACE_ТОКЕН
    roles:
      - chat
      - edit
```

---

# 🟡 ПУТЬ 2: 4GB VRAM (Ollama + Qwen)

**Для кого:** Есть видеокарта с 4-6GB видеопамяти (GTX 1650, GTX 1060, RTX 3050 и т.д.)

**Время настройки:** 15-20 минут
**Стоимость:** Бесплатно навсегда
**Требования:** Видеокарта 4GB+ VRAM, 8GB+ RAM

---

## Что такое Ollama?

**Ollama** — это инструмент для запуска LLM моделей локально на твоём компьютере.

**Преимущества:**
- 🔒 Полная приватность (данные не покидают твой компьютер)
- 🆓 Бесплатно навсегда
- 📴 Работает оффлайн
- ⚙️ Простое управление моделями
- 🚀 Автоматическое использование GPU

**Модели для 4GB VRAM:**

| Модель | Размер | VRAM | Качество | Скорость |
|--------|--------|------|----------|----------|
| `qwen2.5-coder:1.5b` | ~1GB | 2GB | ⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| `qwen2.5-coder:3b` | ~2GB | 3-4GB | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ |
| `phi-3.5` | ~2GB | 3-4GB | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ |

---

## Шаг 1: Установка Ollama

### 🪟 Windows

#### Вариант 1: Через установщик (рекомендуется)

1. Перейди на: **https://ollama.ai/download**

2. Нажми **"Download for Windows"**

![Ollama download page Windows(изображение)](./images/ollama-download.png)

3. Скачается файл `OllamaSetup.exe`

4. Запусти установщик

5. Нажми **"Install"**

![Ollama installer video](https://www.youtube.com/watch?v=VBFndrvxpCI)
![Ollama installer(видео)](https://www.google.com/search?sca_esv=590dbdbf570e834f&sxsrf=ANbL-n7-fF4XVxwXUtaT352TvDTk8s4U3A:1772953509676&q=ollama+install+windows&source=lnms&fbs=ADc_l-aN0CWEZBOHjofHoaMMDiKpmAsnXCN5UBx17opt8eaTX-kA7ovRmAIYWC70eULDzbpKhLTwdBViyqaMPX_061dAYXlr3rIeAfk94tw-2qzqwjHcmvYwkKfGFcofPbhvFXE2LYKBuHCohIkxHayppeOqf6OOmfNJ8QItY9F2Au6ZB2FtAJIv9x65DQawaYQCnq3vq9p11ppXEOzaM1zTksibC3lHcA&sa=X&ved=2ahUKEwjq6JbB3o-TAxX0HxAIHW4bM2MQ0pQJegQIChAB&biw=1920&bih=919&dpr=1#fpstate=ive&vld=cid:ad4e286a,vid:VBFndrvxpCI,st:8)


6. Дождись установки (1-2 минуты)

7. Нажми **"Finish"**

**Ollama запустится автоматически и появится в трее (рядом с часами).**

#### Вариант 2: Через PowerShell

Открой PowerShell от имени администратора и введи:

```powershell
# Скачай и установи через winget (Windows 11/10)
winget install Ollama.Ollama
```

#### Проверка установки

Открой Command Prompt или PowerShell:

```cmd
ollama --version
```

**Должно вывести что-то вроде:**
```
ollama version is 0.1.xx
```

### 🍎 macOS

#### Вариант 1: Через установщик

1. Перейди на: **https://ollama.ai/download**

2. Нажми **"Download for Mac"** (выберется правильная версия автоматически)

![Ollama download page Mac](https://ollama.ai/download/mac)

3. Скачается файл `Ollama-darwin.zip`

4. Распакуй архив (двойной клик)

5. Перетащи **Ollama** в папку **Applications**

6. Открой Ollama из Applications

7. Если появится предупреждение о безопасности:
   - Открой **System Settings** → **Privacy & Security**
   - Найди сообщение об Ollama
   - Нажми **"Open Anyway"**

#### Вариант 2: Через Homebrew

Если у тебя установлен Homebrew:

```bash
brew install ollama
```

#### Проверка установки

Открой Terminal:

```bash
ollama --version
```

### 🐧 Linux

Открой Terminal и введи:

```bash
# Скачай и запусти установочный скрипт
curl -fsSL https://ollama.ai/install.sh | sh
```

**Или пошагово для Ubuntu/Debian:**

```bash
# 1. Добавь ключ Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Запусти сервис
sudo systemctl start ollama

# 3. Включи автозапуск
sudo systemctl enable ollama
```

**Для Arch Linux (AUR):**

```bash
yay -S ollama
```

#### Проверка установки

```bash
ollama --version
```

---

## Шаг 2: Настройка GPU (Важно!)

### Проверка обнаружения GPU

Открой Terminal/Command Prompt и введи:

```bash
ollama run llama3.2:1b --verbose
```

**Если GPU работает, ты увидишь:**
```
loaded meta data with 22 key-value pairs and 322 tensors
...
GPU BLAS = 1
...
```

**Если GPU НЕ работает, ты увидишь:**
```
GPU BLAS = 0
```

### Установка CUDA драйверов (NVIDIA, Windows/Linux)

Если GPU не обнаружен:

1. Проверь, установлены ли драйверы NVIDIA:
   
   **Windows:**
   ```cmd
   nvidia-smi
   ```
   
   **Linux:**
   ```bash
   nvidia-smi
   ```

2. Если команда не найдена, установи драйверы:
   
   **Windows:** Скачай с **https://www.nvidia.com/Download/index.aspx**
   
   **Linux (Ubuntu):**
   ```bash
   sudo apt install nvidia-driver-535  # или актуальную версию
   sudo reboot
   ```

### Для macOS (Apple Silicon)

Ollama автоматически использует Metal (GPU ускорение Apple Silicon).

**Проверь:**
```bash
# Запусти ollama и посмотри логи
OLLAMA_DEBUG=1 ollama run qwen2.5-coder:1.5b
```

Должно быть `metal = 1` в логах.

---

## Шаг 3: Скачивание модели

### Выбор модели

Для 4GB VRAM рекомендуем:

`llama3.2:3b`

| Если нужно | Модель |
|-----------|--------|
| Максимальная скорость | `qwen2.5-coder:1.5b` |
| Баланс скорости и качества | `qwen2.5-coder:3b`, `llama3.2:3b`|
| Альтернатива (Microsoft) | `phi3.5` |

### Скачивание модели

Открой Terminal/Command Prompt:

```bash
# Рекомендуемая модель для кодинга (3B)
ollama pull qwen2.5-coder:3b
```

**Что происходит:**
1. Ollama скачивает модель (~2GB)
2. Автоматически оптимизирует под твоё железо
3. Сохраняет в кэш для быстрого запуска

**Время скачивания:** 5-15 минут (зависит от интернета)

### Альтернативные модели

```bash
# Самая лёгкая (для старых GPU)
ollama pull qwen2.5-coder:1.5b

# Альтернатива от Microsoft
ollama pull phi3.5

# Для общего использования (не только код)
ollama pull llama3.2:3b
```

### Список установленных моделей

```bash
ollama list
```

**Пример вывода:**
```
NAME                    ID              SIZE    MODIFIED
qwen2.5-coder:3b        abc123def456    2.0 GB  2 hours ago
llama3.2:3b             def789ghi012    2.0 GB  1 day ago
```

---

## Шаг 4: Подключение Ollama к Continue.dev

### Способ 1: Автоматическое обнаружение

1. Открой VS Code
2. Открой Continue: `Ctrl + L`
3. Нажми на выпадающий список моделей вверху
4. Если Ollama запущен, модели появятся автоматически
5. Выбери модель `qwen2.5-coder:3b`

### Способ 2: Ручная настройка

Открой `config.yaml` в Continue:

```yaml
models:
  - name: Qwen 3.5 4B
    provider: ollama
    model: qwen3.5:4b
    roles:
      - chat
      - edit
```

### Проверка работы

1. Открой Continue: `Ctrl + L`
2. Напиши: `Привет! Напиши функцию сложения на Python`
3. Нажми Enter

**✅ Если ИИ ответил — всё работает!**

---

## Шаг 5: Запуск Ollama при старте системы

### Windows

Ollama автоматически добавляется в автозапуск при установке.

**Проверь:**
1. Открой Task Manager: `Ctrl + Shift + Esc`
2. Перейди на вкладку **"Startup"**
3. Найди **"Ollama"** — статус должен быть **"Enabled"**

### macOS

```bash
# Создай LaunchAgent
ln -s /Applications/Ollama.app/Contents/Resources/ollama ~/Library/LaunchAgents/com.ollama.ollama.plist
```

Или просто добавь Ollama в **System Settings** → **General** → **Login Items**

### Linux

```bash
# Включи автозапуск сервиса
sudo systemctl enable ollama
```

---

# 🔴 ПУТЬ 3: 16GB+ VRAM (Ollama + Llama 3.1)

**Для кого:** Мощная видеокарта (RTX 3060 12GB, RTX 4070, RTX 3090, RTX 4090) или Mac M1/M2/M3 с 16GB+ RAM

**Время настройки:** 20-30 минут
**Стоимость:** Бесплатно навсегда
**Требования:** 16GB+ VRAM или Apple Silicon 16GB+ RAM

---

## Установка Ollama

Следуй инструкциям из Пути 2 выше.

---

## Выбор модели

Для мощного железа рекомендуются:

| Модель | Размер | VRAM | Качество | Для чего |
|--------|--------|------|----------|----------|
| `llama3.1:8b` | 4.7GB | 8GB+ | ⭐⭐⭐⭐ | Универсальная |
| `deepseek-coder-v2:latest` | 9GB | 16GB+ | ⭐⭐⭐⭐⭐ | Специально для кода |
| `qwen2.5-coder:7b` | 4.7GB | 8GB+ | ⭐⭐⭐⭐⭐ | Код (рекомендуется) |
| `codellama:7b` | 3.8GB | 6GB+ | ⭐⭐⭐⭐ | Legacy, но стабильная |
| `llama3.2:latest` | 4GB | 6GB+ | ⭐⭐⭐⭐ | Новый, быстрый |

**Рекомендация:** Начни с `qwen2.5-coder:7b` — лучшее соотношение качество/размер для кодинга.

---

## Скачивание моделей

```bash
# Рекомендуемая для кода
ollama pull qwen2.5-coder:7b

# Или универсальная от Meta
ollama pull llama3.1:8b

# Или специализированная DeepSeek (для мощных GPU)
ollama pull deepseek-coder-v2:latest
```

**Время скачивания:**
- `qwen2.5-coder:7b`: 5-10 минут
- `deepseek-coder-v2:latest`: 10-20 минут

---

## Подключение к Continue

```yaml
models:
  - name: Qwen 3.5 9B
    provider: ollama
    model: qwen3.5:9b
    roles:
      - chat
      - edit
```

---

## Тестирование скорости

Создай файл `test_speed.py` и попроси ИИ оптимизировать:

```python
# Попроси ИИ оптимизировать этот код
def slow_function(n):
    result = []
    for i in range(n):
        for j in range(n):
            if i * j % 2 == 0:
                result.append(i * j)
    return result
```

**Сравни скорость генерации разных моделей:**
- Qwen 2.5 Coder 7B: обычно быстрее для кода
- DeepSeek Coder V2: иногда медленнее, но качество выше
- Llama 3.1 8B: универсальный баланс

---

# 📊 Сравнение всех путей

| Критерий | Groq API | Ollama Qwen 1.5B | Ollama Llama 3.1 |
|----------|----------|------------------|------------------|
| **Цена** | 🆓 Бесплатно (с лимитами) | 🆓 Бесплатно | 🆓 Бесплатно |
| **Приватность** | ⚠️ Данные в облаке | 🔒 Полная | 🔒 Полная |
| **Оффлайн** | ❌ Нет | ✅ Да | ✅ Да |
| **Скорость** | ⚡⚡⚡⚡⚡ Очень быстро | ⚡⚡⚡⚡ Быстро | ⚡⚡⚡ Средне |
| **Качество кода** | ⭐⭐⭐⭐⭐ Отличное | ⭐⭐⭐ Хорошее | ⭐⭐⭐⭐⭐ Отличное |
| **Требования** | Интернет | 4GB GPU | 16GB GPU |
| **Настройка** | Простой | Средний | Средний |

---

## Checklist дня ✅

### Путь 1 (Groq):
- [ ] Зарегистрировался на Groq Console
- [ ] Создал API ключ
- [ ] Сохранил ключ в надёжном месте
- [ ] Подключил к Continue.dev
- [ ] Проверил работу (ИИ отвечает)

### Путь 2 (Ollama + Qwen):
- [ ] Установил Ollama
- [ ] Проверил работу GPU
- [ ] Скачал модель `qwen2.5-coder:3b`
- [ ] Подключил к Continue.dev
- [ ] Проверил работу (ИИ отвечает)

### Путь 3 (Ollama + Llama):
- [ ] Установил Ollama
- [ ] Проверил работу GPU
- [ ] Скачал модель `qwen2.5-coder:7b` или `llama3.1:8b`
- [ ] Подключил к Continue.dev
- [ ] Проверил работу (ИИ отвечает)

---

## Частые проблемы

### ❌ "Groq API key invalid"

- Проверь, что ключ скопирован полностью (без пробелов)
- Создай новый ключ, если старый не работает
- Проверь, что ключ не просрочен

### ❌ "Ollama not found"

- Проверь, что Ollama запущен:
  - Windows: посмотри в трее
  - macOS: посмотри в Menu Bar
  - Linux: `systemctl status ollama`

### ❌ "Out of memory" при запуске модели

- Попробуй модель меньшего размера:
  - Вместо `qwen2.5-coder:7b` → `qwen2.5-coder:3b`
  - Вместо `llama3.1:8b` → `llama3.2:3b`
- Закрой другие приложения, использующие GPU

### ❌ Медленная генерация на GPU

- Проверь, что GPU используется:
  ```bash
  # При генерации должно быть видно использование GPU
  nvidia-smi  # в другом терминале
  ```
- Если GPU не используется, переустанови драйверы NVIDIA

---

## Что дальше?

**Завтра (День 4):** Мы напишем первую программу через диалог с ИИ! Ты увидишь, как Vibe Coding работает на практике.

**Домашнее задание:**
- Поэкспериментируй с ИИ — задай разные вопросы
- Попробуй попросить объяснить что-то простое
- Запиши, какие вопросы работают хорошо, а какие — нет

---

📚 [На предыдущий день ←](./Day_2.md) | [На следующий день →](./Day_4.md)
