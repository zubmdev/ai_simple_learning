# День 5: Daily Mission — Production MCP Setup 🚀

**Трек:** 👨‍💻 Программист | **Время:** 50 минут

---

## 🎯 Цель дня

Настроить production-ready MCP environment для реального проекта.

---

## Миссия: Полный MCP Stack

### Задача:
Создать окружение для проекта с:
- Database access (PostgreSQL или SQLite)
- File system operations
- Git integration
- Web search (опционально)

---

## Step 1: Установка MCP Servers

### Core servers:

```bash
#!/bin/bash
# setup-mcp.sh

MCP_DIR=~/mcp-servers

# Clone repo
git clone https://github.com/modelcontextprotocol/servers.git $MCP_DIR

# SQLite
cd $MCP_DIR/src/sqlite
npm install && npm run build

# File System
cd $MCP_DIR/src/filesystem
npm install && npm run build

# Git
cd $MCP_DIR/src/git
npm install && npm run build

# GitHub (optional - requires token)
cd $MCP_DIR/src/github
npm install && npm run build

# Brave Search (optional - requires API key)
cd $MCP_DIR/src/brave-search
npm install && npm run build

echo "MCP servers installed successfully!"
```

Run:

```bash
chmod +x setup-mcp.sh
./setup-mcp.sh
```

---

## Step 2: Production Config

### Create `~/.continue/config.production.json`:

```json
{
  "models": [
    {
      "title": "Primary (Ollama GPT-OSS)",
      "provider": "ollama",
      "model": "gpt-oss:20b"
    },
    {
      "title": "Fallback (Groq)",
      "provider": "groq",
      "model": "openai/gpt-oss-20b",
      "apiKey": "${GROQ_API_KEY}"
    }
  ],
  "mcpServers": {
    "sqlite": {
      "command": "node",
      "args": ["${HOME}/mcp-servers/src/sqlite/build/index.js"],
      "disabled": false
    },
    "filesystem": {
      "command": "node",
      "args": [
        "${HOME}/mcp-servers/src/filesystem/build/index.js",
        "${HOME}/projects"
      ],
      "disabled": false
    },
    "git": {
      "command": "node",
      "args": ["${HOME}/mcp-servers/src/git/build/index.js"],
      "disabled": false
    }
  },
  "contextProviders": [
    {
      "name": "codebase",
      "params": {}
    },
    {
      "name": "docs",
      "params": {}
    }
  ]
}
```

---

## Step 3: Environment Setup

### Create `~/.mcp-env`:

```bash
# API Keys (export these)
export GROQ_API_KEY="gsk_xxx"
export BRAVE_API_KEY="xxx"
export GITHUB_TOKEN="ghp_xxx"

# MCP Configuration
export MCP_HOME="${HOME}/mcp-servers"
export MCP_LOG_LEVEL="info"
```

### Add to shell config:

```bash
# ~/.bashrc or ~/.zshrc
[ -f ~/.mcp-env ] && source ~/.mcp-env
```

---

## Step 4: MCP Server Manager Script

### Create `~/bin/mcp-manager`:

```bash
#!/bin/bash

MCP_DIR="${MCP_HOME:-$HOME/mcp-servers}"

case "$1" in
  status)
    echo "MCP Servers Status:"
    for dir in "$MCP_DIR/src"/*; do
      if [ -d "$dir" ]; then
        name=$(basename "$dir")
        if [ -f "$dir/build/index.js" ]; then
          echo "✅ $name: installed"
        else
          echo "❌ $name: not built"
        fi
      fi
    done
    ;;
  
  build)
    echo "Building all MCP servers..."
    for dir in "$MCP_DIR/src"/*; do
      if [ -d "$dir" ] && [ -f "$dir/package.json" ]; then
        name=$(basename "$dir")
        echo "Building $name..."
        cd "$dir"
        npm run build 2>/dev/null
      fi
    done
    ;;
  
  update)
    echo "Updating MCP servers..."
    cd "$MCP_DIR"
    git pull
    $0 build
    ;;
  
  *)
    echo "Usage: mcp-manager {status|build|update}"
    ;;
esac
```

### Make executable:

```bash
chmod +x ~/bin/mcp-manager
```

### Usage:

```bash
mcp-manager status   # Check installed servers
mcp-manager build    # Build all servers
mcp-manager update   # Update from git
```

---

## Step 5: Testing Production Setup

### Create test project:

```bash
mkdir -p ~/projects/mcp-test
cd ~/projects/mcp-test

# Initialize git
git init

# Create sample files
cat > app.py <<'EOF'
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect('data.db')

@app.route('/api/users')
def users():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return jsonify(users)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
EOF

cat > README.md <<'EOF'
# MCP Test Project

Sample project for testing MCP integration.

## Setup

pip install flask

## Run

python app.py
EOF

# Create database
sqlite3 data.db <<'EOF'
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO users VALUES (1, 'Test User', 'test@example.com');
EOF

git add .
git commit -m "Initial commit"
```

### Test prompts in Continue.dev:

```
1. "Analyze this project structure and suggest improvements"

2. "What tables are in data.db? Show me the schema"

3. "Show me the git log and suggest a commit message for the current changes"

4. "Generate API documentation from app.py"
```

---

## Step 6: MCP Best Practices Checklist

### Configuration:

```
✅ Use environment variables for secrets
✅ Specify absolute paths
✅ Limit file system access to project directories
✅ Use read-only DB connections for production
✅ Set appropriate timeouts
```

### Security:

```
✅ Never commit API keys to config
✅ Restrict file system paths
✅ Use separate DB users for MCP (limited permissions)
✅ Regularly rotate API keys
✅ Audit tool usage logs
```

### Performance:

```
✅ Use local models for speed (Ollama)
✅ Cache frequent queries
✅ Batch operations when possible
✅ Set reasonable timeouts
```

---

## Optional: Custom MCP Server

### Create simple custom server:

```typescript
// ~/mcp-servers/src/custom/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new Server({
  name: 'custom-utility',
  version: '1.0.0'
}, {
  capabilities: { tools: {} }
});

// Tool: Calculate statistics
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'calculate_stats',
    description: 'Calculate basic statistics from numbers',
    inputSchema: z.object({
      numbers: z.array(z.number()).describe('Array of numbers')
    }).toJSONSchema()
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'calculate_stats') {
    const { numbers } = request.params.arguments as { numbers: number[] };
    
    const sum = numbers.reduce((a, b) => a + b, 0);
    const avg = sum / numbers.length;
    const min = Math.min(...numbers);
    const max = Math.max(...numbers);
    
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ sum, avg, min, max, count: numbers.length }, null, 2)
      }]
    };
  }
  throw new Error('Unknown tool');
});

const transport = new StdioServerTransport();
server.connect(transport);
```

### Build and add to config:

```bash
cd ~/mcp-servers/src/custom
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init

# Add to config.json:
{
  "custom": {
    "command": "node",
    "args": ["${HOME}/mcp-servers/src/custom/build/index.js"]
  }
}
```

---

## Checklist недели ✅

- [ ] Понял MCP архитектуру
- [ ] Изучил каталог серверов
- [ ] Настроил интеграцию с Continue.dev
- [ ] Освоил tool calling паттерны
- [ ] Создал production-ready setup
- [ ] Написал custom MCP server (optional)

---

## 🎉 Итоги недели

Ты освоил MCP — стандарт для подключения внешних инструментов к ИИ-ассистентам.

**Ключевые навыки:**
- Настройка MCP-серверов
- Безопасное управление доступом
- Эффективные промпты для tool calling
- Production deployment

**Следующая неделя:** Vibe Coding реального проекта!

---

📚 [На следующую неделю →](../Week_6.md)
