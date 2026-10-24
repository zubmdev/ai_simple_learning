# День 3: Интеграция MCP с Continue.dev 🔌

**Трек:** 👨‍💻 Программист | **Время:** 40 минут

---

## 🎯 Цель дня

Настроить MCP-серверы в Continue.dev и протестировать интеграцию.

---

## Практическая настройка

### Задача: Подключить SQLite и File System MCP

### Step 1: Install MCP Servers

```bash
# Clone official repo
git clone https://github.com/modelcontextprotocol/servers.git ~/mcp-servers

# Install & build SQLite
cd ~/mcp-servers/src/sqlite
npm install && npm run build

# Install & build File System
cd ~/mcp-servers/src/filesystem
npm install && npm run build
```

### Step 2: Configure Continue.dev

```json
// ~/.continue/config.json
{
  "models": [
    {
      "title": "Local Llama3",
      "provider": "ollama",
      "model": "llama3"
    }
  ],
  "mcpServers": {
    "sqlite": {
      "command": "node",
      "args": ["/home/user/mcp-servers/src/sqlite/build/index.js"],
      "env": {}
    },
    "filesystem": {
      "command": "node",
      "args": [
        "/home/user/mcp-servers/src/filesystem/build/index.js",
        "/home/user/projects"
      ],
      "env": {}
    }
  }
}
```

### Step 3: Test Integration

В Continue.dev:

```
Какие MCP-инструменты доступны?
```

Expected response:

```
Available MCP tools:
1. sqlite:list_tables - List all tables
2. sqlite:query - Execute SQL query
3. filesystem:read_file - Read file
4. filesystem:write_file - Write file
5. filesystem:list_directory - List directory
```

---

## MCP Server Configuration Options

### Full configuration schema:

```typescript
interface MCPServerConfig {
  command: string;           // Executable (node, python, etc)
  args: string[];            // Command-line arguments
  env?: Record<string, string>;  // Environment variables
  disabled?: boolean;        // Disable without removing
  timeout?: number;          // Request timeout (ms)
}
```

### Examples:

#### Python MCP Server:

```json
{
  "mcpServers": {
    "my-python-server": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

#### With API Key:

```json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["/path/to/github-server/build/index.js"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

#### Multiple allowed paths:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": [
        "/path/to/filesystem-server/index.js",
        "/home/user/projects",
        "/home/user/data",
        "/tmp/sandbox"
      ]
    }
  }
}
```

---

## Debugging MCP Connections

### Check server is running:

```bash
# Manual test
node ~/mcp-servers/src/sqlite/build/index.js

# Send test message (in another terminal)
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | node ~/mcp-servers/src/sqlite/build/index.js
```

### Common issues:

| Issue | Solution |
|-------|----------|
| "Cannot find module" | Run `npm install` in server dir |
| "Permission denied" | Check file permissions |
| "Server not found" | Verify absolute path in config |
| Tools not appearing | Restart VS Code after config change |

---

## Advanced: Using with Different Models

### Local models (Ollama):

```json
{
  "models": [{
    "title": "Ollama Qwen2",
    "provider": "ollama",
    "model": "qwen2:7b"
  }],
  "mcpServers": {...}
}
```

**Note:** Smaller models (< 7B) may struggle with tool calling.

### Free APIs (Groq):

```json
{
  "models": [{
    "title": "Groq Llama3",
    "provider": "groq",
    "model": "llama3-70b-8192",
    "apiKey": "gsk_xxx"
  }],
  "mcpServers": {...}
}
```

**Note:** Groq has excellent tool calling support.

### Paid APIs (Anthropic):

```json
{
  "models": [{
    "title": "Claude Sonnet",
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    "apiKey": "sk-ant-xxx"
  }],
  "mcpServers": {...}
}
```

**Note:** Best tool calling capabilities.

---

## Security Considerations

### File System MCP:

```json
// ❌ DON'T: Root access
{
  "args": ["/server/index.js", "/"]
}

// ✅ DO: Specific project folder
{
  "args": ["/server/index.js", "/home/user/projects/myapp"]
}

// ✅ DO: Multiple specific paths
{
  "args": ["/server/index.js", "/home/user/projects", "/home/user/data"]
}
```

### Database MCP:

```json
// ❌ DON'T: Production DB with write access
{
  "connectionString": "postgresql://prod-db:5432/main"
}

// ✅ DO: Read-only replica or dev DB
{
  "connectionString": "postgresql://readonly@replica:5432/main",
  "readOnly": true
}
```

### API Keys:

```bash
# Use environment variables
export BRAVE_API_KEY="xxx"

# In config.json:
{
  "env": {
    "BRAVE_API_KEY": "${BRAVE_API_KEY}"
  }
}
```

---

## Practical Exercise

### Create test database:

```bash
# Create test DB
sqlite3 test.db <<EOF
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL);

INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO users VALUES (2, 'Bob', 'bob@example.com');
INSERT INTO orders VALUES (1, 1, 99.99);
INSERT INTO orders VALUES (2, 1, 149.99);
INSERT INTO orders VALUES (3, 2, 49.99);
EOF
```

### Test queries:

```
1. List all tables
2. Show table schema
3. Query top user by orders
4. Generate Python script from schema
```

---

## Checklist дня ✅

- [ ] Установил MCP-серверы
- [ ] Настроил config.json
- [ ] Протестировал интеграцию
- [ ] Понял security best practices
- [ ] Создал тестовую БД

---

📚 [На следующий день →](./Day_4.md)
