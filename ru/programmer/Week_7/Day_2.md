# День 2: Log Analysis & Error Context 📊

**Трек:** 👨‍💻 Программист | **Время:** 35 минут

---

## 🎯 Цель дня

Научиться эффективно анализировать логи и предоставлять ИИ правильный контекст для решения проблем.

---

## Structured Logging

### Уровни логов:

```
ERROR  → Критические ошибки (система не работает)
WARN   → Предупреждения (потенциальные проблемы)
INFO   → Информационные (ключевые события)
DEBUG  → Отладочные (детали для разработки)
TRACE  → Трассировка (максимальная детализация)
```

### Пример структурированных логов:

```javascript
// logger.js
import winston from 'winston';

const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
    ),
    defaultMeta: { service: 'api' },
    transports: [
        new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
        new winston.transports.File({ filename: 'logs/combined.log' }),
    ],
});

export default logger;
```

---

## Log-Driven Debugging

### Шаг 1: Собери логи

```bash
# Просмотр последних ошибок
tail -f logs/error.log

# Поиск по паттерну
grep "TypeError" logs/combined.log

# Фильтр по времени
grep "2024-01-15 10:" logs/combined.log

# Извлечение stack traces
grep -A 10 "Error:" logs/error.log
```

### Шаг 2: Структурируй для ИИ

```markdown
## Log Analysis Report

### Error Summary
```
[Вставь 5-10 строк логов с ошибкой]
```

### Timestamp
When: 2024-01-15 10:23:45

### Frequency
- Occurred 15 times in last hour
- Pattern: every ~4 minutes

### Context
- User action: POST /api/orders
- Request payload: [вставь]
- Response: 500 Internal Server Error

### Stack Trace
```
[Полный stack trace]
```

### Related Code
@Files: order.service.js, order.controller.js

### Suspected Cause
[Твоя гипотеза]

What's the root cause? How to fix?
```

---

## Error Context Template

### Полный контекст для ИИ:

```markdown
# Error Context Report

## 1. Error Details

**Type:** TypeError
**Message:** Cannot read property 'id' of undefined
**Location:** order.service.js:45

## 2. Stack Trace

```
TypeError: Cannot read property 'id' of undefined
    at OrderService.create (order.service.js:45:25)
    at OrderController.create (order.controller.js:23:18)
    at Layer.handle (router/layer.js:95:5)
    ...
```

## 3. Reproduction Steps

1. POST /api/orders with payload: { "userId": "abc", "items": [] }
2. Server returns 500
3. Log shows error

## 4. Code Context

```javascript
// order.service.js:40-50
async create(orderData) {
    const user = await this.userRepo.findById(orderData.userId);
    // Line 45: user is undefined when userId not found
    const orderId = user.id; // ← Error here
    // ...
}
```

## 5. Data State

```json
{
  "orderData": {
    "userId": "nonexistent-user-id",
    "items": []
  },
  "user": null  // ← Problem: no validation
}
```

## 6. Expected Behavior

- If userId doesn't exist → return 404
- Not crash with 500

## 7. Recent Changes

- Added order caching yesterday
- No validation for user existence

## 8. Related Files

@Files: order.service.js, user.repository.js

## Questions

1. Should we validate user existence before creating order?
2. Should we throw custom error or return null?
3. How to add proper error handling?
```

---

## Automated Log Analysis

### Скрипт для анализа:

```javascript
// analyze-logs.js
const fs = require('fs');
const readline = require('readline');

async function analyzeErrorLogs(filePath) {
    const errors = {};
    
    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });
    
    for await (const line of rl) {
        if (line.includes('"level":"error"')) {
            const log = JSON.parse(line);
            const key = log.message || log.stack?.split('\n')[0];
            
            if (!errors[key]) {
                errors[key] = {
                    count: 0,
                    firstSeen: log.timestamp,
                    lastSeen: log.timestamp,
                    examples: []
                };
            }
            
            errors[key].count++;
            errors[key].lastSeen = log.timestamp;
            
            if (errors[key].examples.length < 3) {
                errors[key].examples.push(log);
            }
        }
    }
    
    return Object.entries(errors)
        .sort((a, b) => b[1].count - a[1].count)
        .slice(0, 10);
}

// Usage
analyzeErrorLogs('logs/combined.log').then(errors => {
    console.log('Top 10 Errors:');
    errors.forEach(([message, data]) => {
        console.log(`\n[${data.count}x] ${message}`);
        console.log(`First: ${data.firstSeen}`);
        console.log(`Last: ${data.lastSeen}`);
    });
});
```

---

## Log Aggregation Patterns

### Pattern 1: Correlation ID

```javascript
// Добавь correlation ID для трассировки запросов

import { v4 as uuidv4 } from 'uuid';

app.use((req, res, next) => {
    req.correlationId = uuidv4();
    logger.info('Request started', {
        correlationId: req.correlationId,
        method: req.method,
        url: req.url
    });
    next();
});

// В логах:
{
  "correlationId": "abc-123",
  "message": "Request started",
  "method": "POST",
  "url": "/api/orders"
}
```

### Pattern 2: Request/Response Logging

```javascript
app.use((req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
        logger.info('Request completed', {
            correlationId: req.correlationId,
            method: req.method,
            url: req.url,
            statusCode: res.statusCode,
            duration: Date.now() - start
        });
    });
    
    next();
});
```

---

## AI-Driven Log Analysis

### Промпт для ИИ:

```
Analyze these error logs and provide:

## Logs
```
[Вставь 50-100 строк логов]
```

## Tasks

1. Identify top 3 recurring errors
2. Find patterns (time-based, user-based, action-based)
3. Suggest root causes for each
4. Prioritize fixes by impact
5. Recommend monitoring/alerts

Format as structured report.
```

### Пример ответа ИИ:

```markdown
# Log Analysis Report

## Top 3 Recurring Errors

### 1. Database Connection Timeout (45 occurrences)
**Pattern:** Every 2-3 hours
**Root Cause:** Connection pool exhausted
**Impact:** HIGH - 500 errors
**Fix:** Increase pool size, add connection timeouts

### 2. Validation Error (23 occurrences)
**Pattern:** Peak hours (10am-2pm)
**Root Cause:** Missing input validation
**Impact:** MEDIUM - 400 errors
**Fix:** Add request validation middleware

### 3. Authentication Failed (12 occurrences)
**Pattern:** Random distribution
**Root Cause:** Expired tokens
**Impact:** LOW - 401 errors
**Fix:** Implement token refresh

## Recommended Actions

1. Immediate: Fix database connection pool
2. This week: Add validation middleware
3. Next sprint: Implement token refresh

## Monitoring Setup

Add alerts for:
- Error rate > 5% in 5 minutes
- Database connection count > 80% of pool
- Response time > 2s average
```

---

## Practice

### Задание:

```
1. Собери логи из своего проекта (или создай тестовые)
2. Проанализируй с помощью скрипта выше
3. Подготовь Error Context Report
4. Отправь ИИ для анализа
5. Примени рекомендации
```

---

## Checklist дня ✅

- [ ] Настроил структурированные логи
- [ ] Освоил log-driven debugging
- [ ] Создал Error Context Template
- [ ] Написал скрипт анализа логов
- [ ] Попрактиковался в AI-driven analysis

---

📚 [На следующий день →](./Day_3.md)
