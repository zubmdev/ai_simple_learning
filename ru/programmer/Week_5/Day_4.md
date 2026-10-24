# День 4: Tool Calling через MCP 🛠️

**Трек:** 👨‍💻 Программист | **Время:** 35 минут

---

## 🎯 Цель дня

Освоить паттерны tool calling и понять, как LLM взаимодействует с MCP-инструментами.

---

## Tool Calling Flow

### Sequence:

```
User Prompt
    ↓
LLM Analysis → Decides tool needed?
    ↓ Yes
Tool Selection → Which tool?
    ↓
Parameter Extraction → What arguments?
    ↓
Tool Execution → MCP Server
    ↓
Result Processing → Format response
    ↓
LLM Synthesis → Final answer
```

### Example Trace:

```
User: "Show top 5 users by order amount"

LLM:
1. Recognizes need for database query
2. Selects: sqlite:query
3. Extracts: { query: "SELECT u.name, SUM(o.amount)..." }
4. Executes tool
5. Receives: [{name: "Alice", total: 249.98}, ...]
6. Formats: "Top 5 users by order amount:\n1. Alice - $249.98..."
```

---

## Effective Prompting for Tool Use

### Pattern 1: Direct Task

```
✅ "Query the database to find all users who made orders over $100"

LLM automatically:
- Selects sqlite:query
- Generates appropriate SQL
- Executes and formats
```

### Pattern 2: Multi-step Task

```
✅ "Analyze the users table and create a Python script 
    that exports inactive users to CSV"

LLM sequence:
1. sqlite:query → SELECT * FROM users WHERE...
2. filesystem:write_file → Create export_users.py
```

### Pattern 3: Exploration

```
✅ "What data is available? Show me table structures 
    and suggest some analyses"

LLM:
1. sqlite:list_tables
2. sqlite:describe_table (for each)
3. Suggests analyses based on schema
```

---

## Prompting Anti-patterns

### ❌ Over-specifying implementation:

```
Bad: "Use the sqlite:query tool with parameter 
      'SELECT * FROM users' and then parse the JSON response"

Good: "Show me all users in the database"
```

### ❌ Mixing concerns:

```
Bad: "Query the database and also write a blog post 
      about your findings and send an email"

Good: Break into separate prompts:
1. "Query the database and summarize findings"
2. "Write a blog post based on these findings: [paste]"
```

### ❌ Assuming tool availability:

```
Bad: "Delete all test users from the database"
(Assumes DELETE is allowed - might not be!)

Good: "Can you remove test users from the database?"
(LLM will check capabilities first)
```

---

## Advanced Patterns

### Pattern: Chained Tools

```
User: "Find the most active user and generate a report about them"

LLM:
1. Tool: sqlite:query
   → SELECT user_id, COUNT(*) as orders FROM orders GROUP BY user_id
   
2. Tool: sqlite:query  
   → SELECT * FROM users WHERE id = ?
   
3. Tool: filesystem:write_file
   → Create user_report.md
```

### Pattern: Conditional Logic

```
User: "If there are any users without orders, create a re-engagement list"

LLM:
1. Tool: sqlite:query
   → SELECT u.* FROM users u LEFT JOIN orders o ON u.id = o.user_id WHERE o.id IS NULL
   
2. Conditional: If results exist:
   Tool: filesystem:write_file
   → Create reengagement_list.csv
```

### Pattern: Validation

```
User: "Analyze the database schema and validate it follows best practices"

LLM:
1. Tool: sqlite:list_tables
2. Tool: sqlite:describe_table (each table)
3. Analysis: Check normalization, indexes, constraints
4. Output: Report with recommendations
```

---

## Tool Response Handling

### MCP Tool Response Format:

```typescript
interface ToolResult {
  content: Array<{
    type: "text" | "image" | "resource";
    text?: string;
    data?: string;  // base64 for images
    resource?: Resource;
  }>;
  isError?: boolean;
}
```

### Handling in prompts:

```
User: "Query orders and visualize the results"

LLM:
1. Tool: sqlite:query → Returns JSON
2. Processing: Parse JSON
3. Tool: filesystem:write_file → Create Python script
4. Content: Script uses matplotlib to visualize
```

---

## Debugging Tool Calls

### When tools don't work:

```
1. Check if tool is listed:
   "What MCP tools do you have access to?"

2. Verify parameters:
   "What parameters does the query tool accept?"

3. Test with simple call:
   "Call the list_tables tool and show results"

4. Check errors:
   "Show me the last error from tool calls"
```

### Common failures:

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Tool not called | Model doesn't recognize need | More explicit prompt |
| Wrong parameters | Schema mismatch | Check tool schema |
| Timeout | Slow execution | Increase timeout in config |
| Permission denied | Security restriction | Check allowed paths |

---

## Practical Exercise

### Setup:

```bash
# Create orders database
sqlite3 shop.db <<EOF
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, category TEXT);
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, quantity INTEGER, order_date DATE);

INSERT INTO products VALUES (1, 'Laptop', 999.99, 'Electronics');
INSERT INTO products VALUES (2, 'Mouse', 29.99, 'Electronics');
INSERT INTO products VALUES (3, 'Desk', 349.99, 'Furniture');

INSERT INTO customers VALUES (1, 'Alice', 'alice@mail.com', 'Moscow');
INSERT INTO customers VALUES (2, 'Bob', 'bob@mail.com', 'SPb');
INSERT INTO customers VALUES (3, 'Carol', 'carol@mail.com', 'Moscow');

INSERT INTO orders VALUES (1, 1, 1, 1, '2024-01-15');
INSERT INTO orders VALUES (2, 1, 2, 2, '2024-01-16');
INSERT INTO orders VALUES (3, 2, 3, 1, '2024-01-17');
INSERT INTO orders VALUES (4, 3, 1, 1, '2024-01-18');
INSERT INTO orders VALUES (5, 3, 2, 1, '2024-01-19');
EOF
```

### Tasks:

```
1. "Show total sales by city"
2. "Find the best-selling product"
3. "Create a Python script that generates a sales report"
4. "Export customers who bought laptops to a CSV file"
```

---

## Checklist дня ✅

- [ ] Понял flow tool calling
- [ ] Освоил эффективные паттерны промптинга
- [ ] Избегаю anti-patterns
- [ ] Умею debug tool calls
- [ ] Выполнил практические задания

---

📚 [На следующий день →](./Day_5.md)
