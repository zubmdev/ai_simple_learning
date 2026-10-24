# День 3: Установка первого MCP-сервера ⚙️

**Трек:** 🌱 Начинающий | **Время:** 50 минут

---

## 🎯 Цель дня

Установить SQLite MCP-сервер и подключить его к Continue.dev.

---

## ⚠️ Важно перед началом

### Требования:

```
✅ Node.js установлен (проверь: node --version)
✅ Continue.dev установлен в VS Code
✅ Тестовая база test.db создана (из Дня 2)
```

### Если Node.js нет:

```bash
# Ubuntu/Debian
sudo apt-get install nodejs npm

# macOS
brew install node

# Windows
# Скачай с https://nodejs.org/
```

---

## Часть 1: Что мы будем делать?

### План:

```
1. Установить SQLite MCP через npm
2. Настроить Continue.dev для работы с MCP
3. Протестировать подключение
4. Убедиться, что ИИ "видит" базу данных
```

### Схема:

```
┌──────────────┐
│  Continue.dev │
│  (VS Code)    │
└───────┬──────┘
        │ MCP Protocol
        ▼
┌──────────────┐         ┌────────────┐
│  SQLite MCP   │ ←─────→│ test.db    │
│  Server       │         │ (твоя БД)  │
└──────────────┘         └────────────┘
```

---

## Часть 2: Установка SQLite MCP

### Шаг 1: Создай папку для MCP-серверов

```bash
mkdir -p ~/mcp-servers
cd ~/mcp-servers
```

### Шаг 2: Клонируй репозиторий MCP-серверов

```bash
git clone https://github.com/modelcontextprotocol/servers.git
```

Если git не установлен:

```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git
```

### Шаг 3: Перейди в папку SQLite MCP

```bash
cd servers/src/sqlite
```

### Шаг 4: Установи зависимости

```bash
npm install
```

Это может занять 1-2 минуты.

### Шаг 5: Собери проект

```bash
npm run build
```

Если成功了 (success), увидишь сообщение о сборке.

---

## Часть 3: Настройка Continue.dev

### Где конфигурация?

```
Файл: ~/.continue/config.json

Или в VS Code:
1. Cmd/Ctrl + Shift + P
2. Напиши "Continue: Open Settings"
3. Выбери "Open Config File"
```

### Структура config.json:

```json
{
  "models": [...],
  "tabAutocompleteModel": {...},
  "mcpServers": {
    "sqlite": {
      "command": "node",
      "args": ["/path/to/sqlite-server/build/index.js"],
      "env": {}
    }
  }
}
```

### Шаг 1: Найди полный путь к SQLite MCP

```bash
pwd
```

Это покажет текущий путь. Он должен заканчиваться на `servers/src/sqlite`.

Пример:
```
/home/username/mcp-servers/servers/src/sqlite
```

### Шаг 2: Открой config.json Continue.dev

```bash
# Linux/macOS
nano ~/.continue/config.json

# Или открой через VS Code
code ~/.continue/config.json
```

### Шаг 3: Добавь секцию mcpServers

Если файл пустой или минимальный, добавь:

```json
{
  "models": [
    {
      "title": "Local Model",
      "provider": "ollama",
      "model": "llama3"
    }
  ],
  "mcpServers": {
    "sqlite": {
      "command": "node",
      "args": ["/home/username/mcp-servers/servers/src/sqlite/build/index.js"]
    }
  }
}
```

**Важно:** Замени `/home/username/...` на ТВОЙ реальный путь!

### Для разных конфигураций железа:

#### CPU Only (Free API):

```json
{
  "models": [
    {
      "title": "Groq Llama",
      "provider": "groq",
      "model": "llama3-70b-8192",
      "apiKey": "твой-groq-api-key"
    }
  ],
  "mcpServers": {
    "sqlite": {
      "command": "node",
      "args": ["/полный/путь/к/sqlite/build/index.js"]
    }
  }
}
```

#### 4GB GPU (Ollama):

```json
{
  "models": [
    {
      "title": "Ollama Qwen",
      "provider": "ollama",
      "model": "qwen2:1.5b"
    }
  ],
  "mcpServers": {
    "sqlite": {
      "command": "node",
      "args": ["/полный/путь/к/sqlite/build/index.js"]
    }
  }
}
```

#### 16GB GPU (Ollama):

```json
{
  "models": [
    {
      "title": "Ollama Llama3",
      "provider": "ollama",
      "model": "llama3"
    }
  ],
  "mcpServers": {
    "sqlite": {
      "command": "node",
      "args": ["/полный/путь/к/sqlite/build/index.js"]
    }
  }
}
```

---

## Часть 4: Проверка установки

### Шаг 1: Перезапусти VS Code

```
Cmd/Ctrl + Shift + P → "Reload Window"
```

Или просто закрой и открой VS Code.

### Шаг 2: Открой Continue.dev

```
Cmd/Ctrl + L → откроется боковая панель Continue
```

### Шаг 3: Проверь, что MCP загружен

В чате Continue.dev напиши:

```
Какие MCP-инструменты у тебя есть?
```

ИИ должен ответить что-то вроде:

```
У меня есть доступ к следующим MCP-инструментам:
1. read_query - выполнить SQL запрос на чтение
2. list_tables - показать список таблиц
3. describe_table - показать структуру таблицы
```

**Если ИИ не видит инструменты:**
- Проверь путь в config.json
- Убедись, что npm run build успешно выполнился
- Проверь, что node установлен: `node --version`

---

## Часть 5: Первый запрос к базе через MCP!

### Убедись, что test.db в доступном месте:

```bash
# Создай папку для проекта
mkdir -p ~/projects/mcp-test
cd ~/projects/mcp-test

# Скопируй test.db (если она не здесь)
cp /path/to/test.db .
```

### Запрос 1: Список таблиц

В Continue.dev:

```
@Folder: ~/projects/mcp-test

Подключись к базе test.db и покажи список всех таблиц
```

ИИ (через MCP) должен ответить:

```
В базе test.db найдены таблицы:
- users (5 записей)
- orders (10 записей)
```

### Запрос 2: Структура таблицы

```
Покажи структуру таблицы users
```

ИИ:

```
Таблица users:
- id: INTEGER, PRIMARY KEY
- name: TEXT, NOT NULL
- email: TEXT, UNIQUE
- created_at: DATETIME, DEFAULT CURRENT_TIMESTAMP
```

### Запрос 3: Простой SELECT

```
Покажи первых 3 пользователей из таблицы users
```

ИИ (выполняет SQL через MCP):

```sql
SELECT * FROM users LIMIT 3;
```

Результат:

```
ID | Name   | Email              | Created At
1  | Анна   | anna@example.com   | 2024-01-15 10:30:00
2  | Борис  | boris@example.com  | 2024-01-15 10:30:00
3  | Виктор | victor@example.com | 2024-01-15 10:30:00
```

---

## Часть 6: Что происходит "под капотом"?

### Когда ты пишешь промпт:

```
Ты: "Покажи топ-3 пользователя по заказам"

Continue.dev:
1. Распознаёт, что нужен MCP-инструмент
2. Вызывает SQLite MCP Server
3. MCP выполняет SQL:
   SELECT u.name, COUNT(o.id) as order_count
   FROM users u
   JOIN orders o ON u.id = o.user_id
   GROUP BY u.id
   ORDER BY order_count DESC
   LIMIT 3
4. MCP возвращает результат
5. ИИ форматирует и показывает тебе
```

### Ты НЕ пишешь SQL!

```
❌ Старый способ:
Ты: Пишешь SQL вручную
Ты: Выполняешь в терминале
Ты: Копируешь результат

✅ Vibe Coding с MCP:
Ты: "Покажи топ-3 пользователя по заказам"
ИИ: Всё делает сам через MCP
```

---

## Часть 7: Troubleshooting (Решение проблем)

### Проблема: ИИ не видит MCP-инструменты

**Решение:**
```bash
# 1. Проверь путь
ls ~/mcp-servers/servers/src/sqlite/build/index.js

# 2. Если файла нет, собери заново
cd ~/mcp-servers/servers/src/sqlite
npm run build

# 3. Перезапусти VS Code
```

### Проблема: Ошибка "Cannot find module"

**Решение:**
```bash
cd ~/mcp-servers/servers/src/sqlite
npm install
```

### Проблема: ИИ не может подключиться к базе

**Решение:**
```
Убедись:
1. test.db существует (ls test.db)
2. Путь к базе правильный
3. У тебя есть права на чтение файла
```

### Проблема: MCP сервер падает

**Решение:**
```bash
# Запусти MCP сервер вручную для отладки
node ~/mcp-servers/servers/src/sqlite/build/index.js

# Если есть ошибки, посмотри вывод
```

---

## 🧠 Ключевые принципы

| Принцип | Объяснение |
|---------|------------|
| **config.json** | Файл настройки Continue.dev |
| **mcpServers** | Секция для подключения MCP-серверов |
| **Абсолютный путь** | Всегда указывай полный путь к MCP-серверу |
| **Перезапуск** | После изменения config нужно перезапустить VS Code |
| **npm run build** | Обязательно собери MCP-сервер перед использованием |

---

## Checklist дня ✅

- [ ] Установил SQLite MCP через git clone и npm
- [ ] Собрал проект (npm run build)
- [ ] Нашёл абсолютный путь к серверу
- [ ] Добавил mcpServers в config.json Continue.dev
- [ ] Перезапустил VS Code
- [ ] Проверил, что ИИ видит MCP-инструменты
- [ ] Выполнил первый SQL запрос через MCP

---

## Что дальше?

**Завтра (День 4):** Научимся вести диалог с ИИ через MCP — как правильно формулировать запросы к данным.

**Домашнее задание:**
- Попробуй разные запросы к test.db
- Запиши, какие запросы сработали хорошо, а какие — нет
- Подумай: какие ещё данные было бы интересно проанализировать?

---

📚 [На следующий день →](./Day_4.md)
