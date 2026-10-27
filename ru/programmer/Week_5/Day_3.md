# День 3: Подключение MCP к OpenCode 🔌

**Трек:** 👨‍💻 Программист | **Время:** 40 минут

---

## 🎯 Цель дня

Подключить два MCP-сервера (filesystem и sqlite) к OpenCode, настроить approvals и провести первые одобренные tool calls. К концу дня у тебя рабочий конфиг без секретов, закоммиченный в репозиторий.

💡 **Миграция со старого курса:** раньше неделя MCP строилась вокруг `~/.continue/config.json` — Continue.dev больше не развивается. Теперь конфиг живёт в `opencode.json` рядом с проектом. Если пользуешься Cline — там эквивалентный файл `cline_mcp_settings.json` с тем же блоком `mcpServers` (см. в конце урока).

---

## 📊 Модель по тирам

| Уровень | Железо | Модель | Примечание |
|---------|--------|--------|------------|
| Tier 1 | CPU + бесплатный API | Groq `openai/gpt-oss-20b` | бесплатный tier, лимиты ~30 RPM |
| Tier 2 | 4GB GPU + Ollama | `qwen3.5:2b` | fallback: `qwen3:4b` |
| Tier 3 | 16GB GPU + Ollama | `gpt-oss:20b` | лучший локальный tool calling |

**Проверено: 2026-10-24**

💡 Для tool calling через MCP нужна модель с поддержкой tools. Все три уровня справляются; на Tier 2 держи таски простыми.

---

## 🛠️ Шаг 1: Лабораторный проект

```bash
mkdir -p ~/projects/mcp-lab && cd ~/projects/mcp-lab
git init

# Демо-база
sqlite3 data.db <<'EOF'
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO users VALUES (2, 'Bob', 'bob@example.com');
INSERT INTO orders VALUES (1, 1, 99.99);
INSERT INTO orders VALUES (2, 1, 149.99);
INSERT INTO orders VALUES (3, 2, 49.99);
EOF

echo "Заметка для агента" > notes.md
```

Проверка: `ls` показывает `data.db` и `notes.md`.

---

## 🛠️ Шаг 2: Установка инструментов

OpenCode ставится одной командой (если ещё не стоит):

```bash
curl -fsSL https://opencode.ai/install | bash
```

MCP-серверы — обычные npm/PyPI-пакеты, клонировать репозитории не нужно. Для sqlite-сервера нужен `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Версию filesystem-сервера пинуй по уроку Дня 2:

```bash
npm view @modelcontextprotocol/server-filesystem version
```

---

## 🛠️ Шаг 3: Конфиг `opencode.json`

Создай `opencode.json` в корне `~/projects/mcp-lab/`. Замени пути и версию пакета на свои.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "groq/openai/gpt-oss-20b",
  "provider": {
    "groq": {
      "options": {
        "apiKey": "{env:GROQ_API_KEY}"
      }
    }
  },
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@modelcontextprotocol/server-filesystem@0.6.2",
        "/home/max/projects/mcp-lab"
      ],
      "enabled": true
    },
    "sqlite": {
      "type": "local",
      "command": [
        "uvx",
        "mcp-server-sqlite",
        "--db-path",
        "/home/max/projects/mcp-lab/data.db"
      ],
      "enabled": true
    }
  },
  "permission": {
    "edit": "ask",
    "bash": {
      "git status": "allow",
      "git diff": "allow",
      "git push*": "deny",
      "rm*": "deny",
      "*": "ask"
    },
    "webfetch": "ask"
  }
}
```

Разбор по-безопасному:

- `$schema` — автодополнение и валидация в редакторе: опечатки в ключах видны сразу
- `{env:GROQ_API_KEY}` — ключ читается из окружения, **не из файла в git**
- `command` для stdio — массив; последний аргумент filesystem — единственный разрешённый путь
- `permission` — политика: чтение разрешено, запись и bash — через вопрос, `push` и `rm` — запрещены (`*` в паттерне — префиксная маска)

Вариант для Tier 2/3 (Ollama вместо Groq):

```json
"model": "ollama/gpt-oss:20b",
"provider": {
  "ollama": {
    "npm": "@ai-sdk/openai-compatible",
    "options": {
      "baseURL": "http://localhost:11434/v1"
    }
  }
}
```

Для Tier 2 подставь `ollama/qwen3.5:2b`.

---

## 🛠️ Шаг 4: Секреты — вне репозитория

Ключ Groq храним в `~/.mcp.env` (вне проекта), файл закрыт от чужих глаз:

```bash
echo 'export GROQ_API_KEY="твой_ключ_сюда"' > ~/.mcp.env
chmod 600 ~/.mcp.env
```

Подключи к оболочке (один раз):

```bash
echo '[ -f ~/.mcp.env ] && source ~/.mcp.env' >> ~/.bashrc
source ~/.mcp.env
```

Альтернатива для OpenCode: `opencode auth login` — ключ сохраняется в локальном хранилище агента, конфиг остаётся чистым.

🚨 Проверка гигиены: `git status` в проекте не должен показывать никаких файлов с ключами. В конфиге ключ никогда не пишется литералом.

---

## 🛠️ Шаг 5: Запуск и проверка

```bash
cd ~/projects/mcp-lab
opencode
```

Первый промпт — проверка подключения:

```text
Какие MCP-инструменты тебе доступны? Перечисли списком.
```

Ожидаемый ответ содержит группы `filesystem` (`read_file`, `write_file`, `list_directory`...) и `sqlite` (работа с таблицами). Если агент говорит «инструментов нет» — см. таблицу отладки ниже.

Второй промпт — первый одобренный вызов:

```text
Прочитай notes.md и скажи, что в нём написано.
```

OpenCode покажет диалог одобрения tool call: имя инструмента и аргументы. Нажми «разрешить один раз». Агент вернёт содержимое файла.

Третий промпт — проверка отказа:

```text
Удали data.db.
```

Ожидание: вызов не выполняется — либо агент отказывается, либо ты видишь запрос и **отказываешь**. Файл на месте: `ls data.db`. Это и есть рабочая схема безопасности: агент предложил — ты решил.

---

## 🔧 Отладка

| Симптом | Причина | Лечение |
|---------|---------|---------|
| «Cannot find module» | пакет не скачался/опечатка в имени | проверь имя и версию пакета, запусти команду из `command` руками |
| Сервер не подключился | ошибка в `opencode.json` | проверь конфиг по `$schema`: запятые, кавычки, массив `command` |
| Tools не появились | конфиг поправили при запущенном агенте | перезапусти OpenCode |
| Permission denied на файл | путь вне scope filesystem-сервера | добавь конкретный путь в аргументы, не «весь дом» |
| `uvx: command not found` | нет uv | установи uv (Шаг 2), перезапусти терминал |

---

## 💡 Эквивалент для Cline

Cline хранит MCP-конфиг в `cline_mcp_settings.json` (иконка MCP Servers в Cline → Configure). Формат тот же блок `mcpServers` с `command`/`args`/`env`. Разница в безопасности: у Cline **каждый** tool call по умолчанию требует одобрения, а автосогласование включается списком `autoApprove` — держи его пустым или только для читающих инструментов. Путь к файлу — в глобальном хранилище VS Code, в git он не попадает, но и его не публикуй в скриншотах.

---

## Checklist дня ✅

- [ ] Создал лабораторный проект с data.db
- [ ] Записал модель своего тира и вариант провайдера
- [ ] Пинская версия filesystem-сервера в конфиге
- [ ] `opencode.json` с `mcp` и `permission` закоммичен, ключ — в `~/.mcp.env`
- [ ] Видел диалог одобрения и выполнил первый tool call
- [ ] Отклонил деструктивный запрос, файл уцелел

---

## 🎯 Миссия

Добей лабораторию до артефакта:

1. `opencode.json` — рабочий, без секретов, закоммичен: `git add opencode.json && git commit -m "mcp: filesystem + sqlite with approvals"`
2. `.env.example` — файл с именами переменных **без значений** (`GROQ_API_KEY=`), тоже в git
3. `notes.md` — допиши туда лог: один одобренный вызов (инструмент + аргументы) и один отклонённый

**Готово, когда:**

```bash
git log --oneline        # есть коммит с конфигом
git grep -E "gsk_|sk-"   # пусто — секретов в репозитории нет
ls data.db               # база уцелела после попытки удаления
```

---

⏭️ Что дальше: завтра — как агент выбирает инструменты и как читать его tool calls как diff.

📚 [На следующий день →](./Day_4.md)
