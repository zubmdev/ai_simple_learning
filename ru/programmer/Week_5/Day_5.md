# День 5: Миссия — Production MCP Setup 🚀

**Трек:** 👨‍💻 Программист | **Время:** 50 минут

---

## 🎯 Цель дня

Собрать production-настройку MCP для реального проекта: минимальные права у каждого сервера, секреты вне git, политика approvals, аудит. К концу дня у тебя проверяемый набор: конфиг, который можно показать команде, и скрипт, который ловит утечки.

---

## 📊 Модель по тирам

| Уровень | Железо | Модель | Примечание |
|---------|--------|--------|------------|
| Tier 1 | CPU + бесплатный API | Groq `openai/gpt-oss-20b` | бесплатный tier, лимиты ~30 RPM |
| Tier 2 | 4GB GPU + Ollama | `qwen3.5:2b` | fallback: `qwen3:4b` |
| Tier 3 | 16GB GPU + Ollama | `gpt-oss:20b` | лучший локальный tool calling |

**Проверено: 2026-10-24**

---

## 🛠️ Шаг 1: Секреты — одно место хранения, ноль попаданий в git

Правило production: ключ существует в двух местах — менеджер секретов/`.env` и ротация. Нигде больше: не в промптах, не в конфигах, не в логах и скриншотах.

```bash
cd ~/projects/mcp-lab   # или твой реальный проект

cat > .gitignore <<'EOF'
.env
*.db
EOF

cat > .env <<'EOF'
GROQ_API_KEY=gsk_...
# BRAVE_API_KEY=...
# GITHUB_TOKEN=...
EOF

chmod 600 .env
```

- `.env` — источник; в `opencode.json` только ссылки `{env:GROQ_API_KEY}` (или `opencode auth login`)
- `.env.example` с именами без значений — в git, чтобы команда знала, что нужно завести
- Ротация ключей — раз в квартал и сразу после любого «случайно закоммитил»

---

## 🛠️ Шаг 2: База данных — минимальные права

**SQLite (учебный/локальный проект):** агент работает с копией, не с живым файлом.

```bash
cp data.db data-readonly.db
```

И путь `data-readonly.db` — в конфиг MCP. Сломают копию — оригинал цел.

**PostgreSQL (продакшн):** отдельный read-only пользователь, никакого суперпользователя.

```sql
-- выполняется админом БД; пароль сгенерируй: openssl rand -hex 16
CREATE ROLE mcp_readonly LOGIN PASSWORD 'пароль_из_.env';
GRANT CONNECT ON DATABASE appdb TO mcp_readonly;
\c appdb
GRANT USAGE ON SCHEMA public TO mcp_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO mcp_readonly;
```

Строку подключения держи в `.env` (`DATABASE_URL=postgresql://mcp_readonly:...@host:5432/appdb`), в конфиг MCP — через `{env:DATABASE_URL}`.

🚨 Даже read-only пользователь видит **все данные** схемы — включая персональные. Для чувствительных таблиц сделай отдельную схему с выверенным списком таблиц.

---

## 🛠️ Шаг 3: Production `opencode.json`

Файл лежит в корне проекта и **коммитится** — он без секретов, и команда получает одинаковую настройку:

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
        "/home/max/projects/mcp-lab/data-readonly.db"
      ],
      "enabled": true
    },
    "github": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@modelcontextprotocol/server-github@0.6.1"
      ],
      "environment": {
        "GITHUB_TOKEN": "{env:GITHUB_TOKEN}"
      },
      "enabled": false
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

Принципы:

- версии запинены (подставь актуальные с `npm view`); обновление — осознанный коммит, а не `git pull` всего мира
- `github` по умолчанию `"enabled": false` — включается на задачу, выключается после; неиспользуемый сервер с токеном — лишняя поверхность атаки
- deny-список короче и надёжнее любых обещаний агента

---

## 🛠️ Шаг 4: Аудит — скрипт `check-secrets.sh`

Проверяемый артефакт вместо «я вроде не коммитил»:

```bash
#!/bin/bash
# check-secrets.sh — ищем случайно закоммиченные ключи
set -u
PATTERNS='gsk_|sk-ant-|sk-proj-|ghp_|github_pat_|AKIA|xox[bap]-|://[^ /:]+:[^ @]+@'

if git grep -nIE "$PATTERNS" -- . 2>/dev/null; then
  echo "❌ Строки выше похожи на ключи: убери их и ротируй ключи"
  exit 1
fi

if git check-ignore -q .env; then
  echo "✅ .env в .gitignore"
else
  echo "❌ Добавь .env в .gitignore"
  exit 1
fi

echo "✅ Ключей в репозитории не найдено"
```

```bash
chmod +x check-secrets.sh
./check-secrets.sh
```

💡 Скрипт даёт ложные срабатывания на строки вида `user:pass@host` — это нормально: проверь глазами и подкорректируй паттерн под проект. Запускай его перед каждым push (или повесь на pre-commit hook).

---

## 🛠️ Шаг 5: Проверка production-конфига

```bash
opencode
```

Прогоны:

1. `Какие MCP-инструменты доступны?` — есть filesystem и sqlite, github молчит (disabled)
2. `Покажи схему базы данных` — читает из `data-readonly.db`
3. `Добавь пользователя Test в базу` — попытка записи: увидишь отказ/ошибку или approval, который ты отклоняешь; проверь: `sqlite3 data.db "SELECT COUNT(*) FROM users;"` — без изменений
4. `Сделай коммит изменений` — bash-запрос через approval; убедиcь, что `git push` остаётся под deny

---

## ✅ Чек-лист production MCP

**Конфигурация:**

```text
✅ Версии серверов запинены, пути абсолютные
✅ filesystem — только папка проекта
✅ БД — read-only пользователь или копия файла
✅ Неиспользуемые серверы disabled
✅ permission: allow — только чтение, deny — push/rm
```

**Секреты:**

```text
✅ Ключи только в .env / opencode auth login
✅ .env в .gitignore, права 600
✅ В конфиге и промптах — только ссылки {env:...}
✅ Скриншоты и логи без ключей
✅ Ротация раз в квартал и после каждой утечки
```

**Supply chain:**

```text
✅ Перед установкой: repository.url, сопровождающие, дата коммитов
✅ Обновление версии = осознанный коммит с чтением changelog
✅ Минимум capabilities у каждого сервера
```

---

## Checklist недели ✅

- [ ] Понял архитектуру MCP и транспорты
- [ ] Проверяю серверы перед установкой, пиную версии
- [ ] Подключил MCP к OpenCode (`opencode.json` + `permission`)
- [ ] Освоил tool calling с approvals и читал аргументы до нажатия «разрешить»
- [ ] Собрал production-setup: секреты в `.env`, read-only БД, аудит-скрипт зелёный

---

## 🎯 Миссия

Финальный артефакт недели — аудируемый production-setup в твоём проекте:

1. `opencode.json` production-уровня закоммичен (пины, `permission`, лишние серверы disabled)
2. `.env` существует, в `.gitignore`, права 600; `.env.example` закоммичен
3. `check-secrets.sh` зелёный: `./check-secrets.sh` заканчивается кодом 0
4. Попытка записи в БД заблокирована, данные не изменились
5. Короткий итог `mcp-setup-audit.md`: какие серверы, с какими правами, какие секреты где лежат, кто и когда обновляет версии

**Готово, когда:** скрипт аудита прошёл, попытка записи провалилась (проверено COUNT-ом), и новый член команды может поднять окружение по твоему `opencode.json` + `.env.example`, не спросив у тебя ни одного ключа.

---

## 🎉 Итоги недели

Ты умеешь давать агенту инструменты так, чтобы это не превращалось в дыру в безопасности: проверять серверы до установки, ограничивать права, держать секреты в `.env` и читать tool calls до одобрения.

**Ключевые навыки:**

- Архитектура MCP: клиент — сервер — транспорт, Resources/Tools/Prompts
- Supply chain: пины версий, проверка источника, минимум capabilities
- OpenCode: `opencode.json`, `permission`, approvals; Cline как альтернатива
- Production-дисциплина: read-only доступ, аудит, ротация

**Следующая неделя:** агентная сборка реального проекта!

---

📚 [На следующую неделю →](../Week_6.md)
