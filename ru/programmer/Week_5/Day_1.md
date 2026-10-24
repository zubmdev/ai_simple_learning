# День 1: MCP Architecture — как это работает 🏗️

**Трек:** 👨‍💻 Программист | **Время:** 25 минут

---

## 🎯 Цель дня

Понять архитектуру MCP и модель Client-Server-Transport.

---

## Архитектура MCP

### Компоненты:

```
┌─────────────────────────────────────────┐
│           MCP Client (Continue.dev)     │
│  - Управляет соединениями                │
│  - Диспатчит tool calls                  │
│  - Интегрируется с LLM                   │
└─────────────┬───────────────────────────┘
              │ JSON-RPC 2.0 over Transport
              ▼
┌─────────────────────────────────────────┐
│           MCP Server                     │
│  - Resources (доступ к данным)           │
│  - Tools (выполнение действий)           │
│  - Prompts (шаблоны)                     │
└─────────────┬───────────────────────────┘
              │
              ▼
        ┌──────────┐
        │ External │
        │ System   │
        └──────────┘
```

### Transport Types:

```
1. Stdio Transport
   - Server как дочерний процесс
   - Коммуникация через stdin/stdout
   - Идеально для локальных серверов

2. HTTP/SSE Transport
   - Server как HTTP сервис
   - Server-Sent Events для streaming
   - Для удалённых серверов

3. WebSocket Transport
   - Двунаправленная коммуникация
   - Для real-time interactions
```

---

## MCP Protocol Specification

### Основные методы JSON-RPC:

```json
// List available resources
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list"
}

// Read a resource
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "resources/read",
  "params": {
    "uri": "file:///path/to/file.txt"
  }
}

// List tools
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/list"
}

// Call a tool
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "query_database",
    "arguments": {
      "sql": "SELECT * FROM users"
    }
  }
}
```

---

## MCP Server Capabilities

### Resources:

```typescript
// Resource definition
interface Resource {
  uri: string;          // Уникальный идентификатор
  name: string;         // Человекочитаемое имя
  description?: string;
  mimeType?: string;
}

// Example
{
  uri: "sqlite:///db/users",
  name: "users table",
  mimeType: "application/json"
}
```

### Tools:

```typescript
// Tool definition
interface Tool {
  name: string;
  description: string;
  inputSchema: JSONSchema;  // Валидация аргументов
}

// Example
{
  name: "execute_sql",
  description: "Execute SQL query",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string" },
      params: { type: "array" }
    },
    required: ["query"]
  }
}
```

### Prompts:

```typescript
// Prompt template
interface Prompt {
  name: string;
  description: string;
  arguments: PromptArgument[];
}

// Example
{
  name: "analyze_table",
  description: "Analyze table structure and data",
  arguments: [
    {
      name: "table_name",
      description: "Name of the table to analyze",
      required: true
    }
  ]
}
```

---

## Интеграция с Continue.dev

### Config structure:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "env": {
        "API_KEY": "xxx"
      },
      "disabled": false
    }
  }
}
```

### Как Continue.dev работает с MCP:

```
1. При старте VS Code:
   - Читает config.json
   - Запускает каждый MCP server
   - Инициализирует соединение

2. При обработке промпта:
   - LLM решает, нужен ли tool call
   - Если да → вызывает MCP tool
   - Возвращает результат в контекст LLM

3. При закрытии VS Code:
   - Gracefully shutdown servers
   - Закрывает transport connections
```

---

## MCP vs LangChain Tools

| Aspect | MCP | LangChain Tools |
|--------|-----|-----------------|
| Standard | Open protocol | Framework-specific |
| Interoperability | Any MCP client | LangChain only |
| Server distribution | Independent servers | Bundled with app |
| Configuration | JSON config | Code-based |
| Discovery | Runtime | Static definition |

---

## SDK и библиотеки

### TypeScript SDK:

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'my-mcp-server',
  version: '1.0.0'
}, {
  capabilities: {
    resources: {},
    tools: {}
  }
});

// Register tool
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'my_tool',
    description: 'My tool description',
    inputSchema: { type: 'object', properties: {} }
  }]
}));

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python SDK:

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-mcp-server")

@server.list_tools()
async def list_tools():
    return [{
        "name": "my_tool",
        "description": "My tool",
        "inputSchema": {"type": "object", "properties": {}}
    }]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)
```

---

## Checklist дня ✅

- [ ] Понял Client-Server-Transport модель
- [ ] Изучил JSON-RPC 2.0 методы
- [ ] Разобрался в Resources, Tools, Prompts
- [ ] Понял интеграцию с Continue.dev
- [ ] Увидел различия с LangChain Tools

---

📚 [На следующий день →](./Day_2.md)
