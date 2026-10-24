# День 2: MCP Servers Catalog — готовые решения 📦

**Трек:** 👨‍💻 Программист | **Время:** 30 минут

---

## 🎯 Цель дня

Изучить каталог MCP-серверов и понять их capabilities.

---

## Официальный каталог

```
https://github.com/modelcontextprotocol/servers
```

### Категории:

```
servers/
├── src/
│   ├── databases/        # SQLite, PostgreSQL, MySQL
│   ├── filesystem/       # File system access
│   ├── git/              # Git operations
│   ├── github/           # GitHub API
│   ├── google/           # Google Maps, Drive, etc
│   ├── brave-search/     # Web search
│   └── ...               # 20+ servers
```

---

## Database MCP Servers

### SQLite

```json
{
  "capabilities": {
    "resources": {
      "list": "List tables",
      "read": "Read table schema"
    },
    "tools": {
      "query": "Execute SQL queries",
      "list_tables": "Get all tables",
      "describe_table": "Get table schema"
    }
  }
}
```

**Use cases:**
- Local development
- Testing
- Prototyping

### PostgreSQL

```json
{
  "capabilities": {
    "resources": {
      "tables": "Database tables",
      "schemas": "Database schemas"
    },
    "tools": {
      "query": "Execute SQL",
      "migrate": "Run migrations"
    }
  },
  "config": {
    "connectionString": "postgresql://...",
    "ssl": true
  }
}
```

**Use cases:**
- Production databases
- Cloud databases (Supabase, Neon, etc.)

---

## File System MCP Server

### Capabilities:

```json
{
  "resources": {
    "files": "Read file contents",
    "directories": "List directory contents"
  },
  "tools": {
    "read_file": "Read file",
    "write_file": "Create/update file",
    "list_directory": "List files",
    "search_files": "Glob search",
    "get_file_info": "File metadata"
  }
}
```

### Configuration:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": [
        "/path/to/filesystem-server/index.js",
        "/allowed/path/1",
        "/allowed/path/2"
      ]
    }
  }
}
```

**Security:** ИИ имеет доступ ТОЛЬКО к указанным путям.

---

## Git & GitHub MCP

### Git Server:

```json
{
  "tools": {
    "git_status": "Show working tree status",
    "git_log": "Show commit history",
    "git_diff": "Show changes",
    "git_show": "Show commit details"
  }
}
```

### GitHub Server:

```json
{
  "resources": {
    "repositories": "Access repo files",
    "issues": "Read issues",
    "pull_requests": "Read PRs"
  },
  "tools": {
    "create_issue": "Create new issue",
    "create_pr": "Create pull request",
    "search_code": "Search in repo",
    "get_file_contents": "Read file from repo"
  }
}
```

**Auth:** Requires GitHub Personal Access Token.

---

## Web Services MCP

### Brave Search:

```json
{
  "tools": {
    "search": "Web search",
    "local_search": "Local business search"
  },
  "config": {
    "env": {
      "BRAVE_API_KEY": "your-key"
    }
  }
}
```

### Google Maps:

```json
{
  "tools": {
    "geocode": "Convert address to coordinates",
    "reverse_geocode": "Coordinates to address",
    "search_places": "Find nearby places",
    "get_directions": "Route planning"
  }
}
```

---

## Choosing the Right MCP Server

### Decision Matrix:

| Need | Recommended MCP | Why |
|------|----------------|-----|
| Local DB analysis | SQLite | No setup, instant |
| Production DB | PostgreSQL | Connection pooling, SSL |
| File operations | File System | Direct access |
| Code from repos | GitHub | API-based, no clone |
| Current git status | Git | Local operations |
| Web research | Brave Search | Real-time data |

---

## Custom MCP Server Development

### When to create your own:

```
✅ Internal APIs without public MCP
✅ Proprietary databases
✅ Custom business logic
✅ Integration with internal tools
```

### Quick Start (TypeScript):

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new Server({
  name: 'custom-mcp',
  version: '1.0.0'
}, {
  capabilities: { tools: {} }
});

// Define tool
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'my_custom_tool',
    description: 'Does something custom',
    inputSchema: z.object({
      param1: z.string()
    }).toJSONSchema()
  }]
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'my_custom_tool') {
    const { param1 } = request.params.arguments;
    // Your logic here
    return {
      content: [{
        type: 'text',
        text: `Result: ${param1}`
      }]
    };
  }
});

// Start
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## MCP Server Quality Checklist

### Before using an MCP server, check:

```
✅ Documentation: Is there a clear README?
✅ Examples: Are there usage examples?
✅ Tests: Does it have tests?
✅ Maintenance: Recent commits?
✅ Issues: Open issues count?
✅ Stars: Community adoption?
```

---

## Checklist дня ✅

- [ ] Изучил официальный каталог
- [ ] Понял capabilities разных серверов
- [ ] Научился выбирать подходящий MCP
- [ ] Увидел пример создания своего сервера
- [ ] Понял критерии качества

---

📚 [На следующий день →](./Day_3.md)
