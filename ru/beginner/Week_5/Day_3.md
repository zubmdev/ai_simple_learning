# День 3: MCP для данных — подключаем SQLite 🗄️

**Трек:** 🌱 Начинающий | **Время:** 50 минут

---

## 🎯 Цель дня

Создать тестовую базу данных, подключить к ней SQLite MCP-сервер вручную и выполнить первые запросы через карточки одобрения — читая SQL до того, как он выполнится.

---

## 🛠️ Часть 1: Что понадобится

| Уровень | Железо | Модель в Cline |
|---------|--------|----------------|
| CPU + бесплатный API | любой компьютер | Groq `openai/gpt-oss-20b` |
| 4GB GPU (Ollama) | видеокарта от 4GB VRAM | `qwen3.5:2b` (запасная: `qwen3:4b`) |
| 16GB GPU (Ollama) | видеокарта от 16GB VRAM | `gpt-oss:20b` |

**Проверено: 2026-10-24.** Официальный SQLite MCP-сервер — это Python-пакет, который запускается через `uvx`. Ставим один раз:

```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

После установки открой **новый** терминал и проверь: `uvx --version`.

---

## 🗄️ Часть 2: Готовим тестовую базу

Создадим лабораторную папку — она останется с нами до конца недели.

```bash
mkdir -p ~/projects/mcp-lab
cd ~/projects/mcp-lab
```

Создай файл `create_test_db.sql`:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product TEXT NOT NULL,
    amount REAL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (name, email) VALUES
    ('Анна', 'anna@example.com'),
    ('Борис', 'boris@example.com'),
    ('Виктор', 'victor@example.com'),
    ('Галина', 'galina@example.com'),
    ('Дмитрий', 'dmitry@example.com');

INSERT INTO orders (user_id, product, amount) VALUES
    (1, 'Laptop', 999.99),
    (1, 'Mouse', 25.50),
    (2, 'Keyboard', 75.00),
    (3, 'Monitor', 299.99),
    (3, 'Webcam', 45.00),
    (4, 'Headphones', 120.00),
    (5, 'Laptop', 999.99),
    (1, 'USB Hub', 35.00),
    (2, 'Mouse Pad', 15.00),
    (3, 'Speaker', 85.00);
```

Собери базу и проверь:

```bash
sqlite3 test.db < create_test_db.sql
sqlite3 test.db "SELECT name, email FROM users LIMIT 3;"
```

Ожидаемый вывод:

```text
Анна|anna@example.com
Борис|boris@example.com
Виктор|victor@example.com
```

Если `sqlite3` не установлен: Ubuntu/Debian — `sudo apt-get install sqlite3`, macOS — `brew install sqlite`, Windows — инсталлятор с sqlite.org.

---

## ⚙️ Часть 3: Подключаем SQLite MCP

Открой `cline_mcp_settings.json` (окно MCP → **Configure MCP Servers**) и добавь сервер `sqlite` рядом с `memory`:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/home/username/projects/mcp-lab/test.db"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Важно:**

- Замени путь на **свой абсолютный путь** к `test.db`. Windows: двойные обратные слэши — `"C:\\Users\\name\\projects\\mcp-lab\\test.db"`.
- Сервер подключён к **одному конкретному файлу** базы. Другие базы агент через него не увидит — это уже наименьшие привилегии, оценишь в День 4.
- Сохрани (`Ctrl+S`) и убедись, что `sqlite` зелёный в списке Installed.

Если сервер не стартует: перезапусти VS Code после установки uv (чтобы обновился PATH) и проверь `uvx --version` в терминале.

---

## ✅ Часть 4: Первые запросы через одобрения

### Запрос 1: обзор базы

```text
Подключись к базе test.db и покажи, какие таблицы в ней есть.
```

Карточка: `sqlite (MCP): list_tables` → аргументов нет → **Approve**.

Ожидаемый ответ: две таблицы, `users` (5 записей) и `orders` (10 записей).

### Запрос 2: структура таблицы

```text
Покажи структуру таблицы users.
```

Карточка: `sqlite (MCP): describe_table` → **Approve**. Агент перечислит поля: id, name, email, created_at.

### Запрос 3: настоящий SQL — читай внимательно!

```text
Покажи топ-3 пользователя по сумме заказов.
```

Теперь в карточке будет SQL. Пример того, что ты увидишь:

```sql
SELECT u.name, SUM(o.amount) AS total
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY total DESC
LIMIT 3
```

Прочитай запрос как договор: он только читает (`SELECT`), ничего не меняет → **Approve**.

Ожидаемый результат:

```text
1. Анна   — $1,060.49
2. Виктор — $429.99
3. Борис  — $90.00
```

💡 Ты не писал ни строчки SQL — но обязан понимать, что одобряешь. `SELECT` читает, `INSERT/UPDATE/DELETE` меняет данные. Это различие — твой главный фильтр при чтении карточек.

---

## 🧠 Часть 5: Что произошло под капотом

```text
Ты:      «Покажи топ-3 пользователя по сумме заказов»
Модель:  решает, какой инструмент нужен → read_query
Cline:   показывает карточку и ждёт тебя
Ты:      читаешь SQL → Approve
Сервер:  выполняет SQL над test.db и возвращает строки
Модель:  форматирует ответ
```

История вызовов видна в окне MCP — можно всегда проверить, кто и что спрашивал у базы.

---

## 🔧 Часть 6: Troubleshooting

| Симптом | Что делать |
|---------|------------|
| `uvx` не найден | Установи uv (Часть 1), перезапусти терминал и VS Code |
| Сервер красный в Installed | Проверь абсолютный путь к test.db в `--db-path` |
| «unable to open database file» | Файла нет или путь с опечаткой: проверь `ls ~/projects/mcp-lab` |
| Агент зовёт не тот инструмент | Уточни промпт: «используй MCP-сервер sqlite» |

---

## 🧠 Ключевые принципы

| Принцип | Объяснение |
|---------|------------|
| **Один сервер — одна база** | Доступ выдаётся к конкретному файлу, не ко всем сразу |
| **Читай SQL до одобрения** | SELECT — читать можно, DELETE — стоп |
| **Карточка = договор** | Что в аргументах, то и выполнится |
| **Локальный сервер** | База не покидала твой компьютер |

---

## Checklist дня ✅

- [ ] Создал `~/projects/mcp-lab/test.db` с двумя таблицами
- [ ] Установил uv и подключил SQLite MCP вручную
- [ ] Прошёл три запроса: list_tables, describe_table, read_query
- [ ] Прочитал SQL в карточке перед каждым одобрением
- [ ] Проверил историю вызовов в окне MCP

---

## 🎯 Миссия дня

Задай агенту три собственных аналитических вопроса к базе (например: «Какой товар приносит больше всего денег?», «Есть ли пользователи без заказов?», «Какова средняя сумма заказа?»). Затем:

1. Лучший ответ с цифрами сохрани в файл `~/projects/mcp-lab/report.md`.
2. В `mcp-notes.md` запиши один SQL-запрос, который агент выполнил (скопируй из карточки одобрения).

**Проверка:** `report.md` существует и содержит цифры, совпадающие с ответом агента; SQL в `mcp-notes.md` начинается с `SELECT`.

---

## Что дальше?

**Завтра (День 4):** Подключим файловый сервер и научимся ограничивать доступ одной папкой.

---

📚 [На следующий день →](./Day_4.md)
