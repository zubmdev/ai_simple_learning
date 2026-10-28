# День 5: Daily Mission — Debug & Test Challenge 🎯

**Трек:** 👨‍💻 Программист | **Время:** 50 минут

---

## 🎯 Цель дня

Применить все навыки недели: найти баги, исправить их, написать тесты, отрефакторить.

---

## 🎯 Миссия: Production-Ready Code

### Задание:

```
1. Возьми проект из недели 6
2. Найди 5 потенциальных багов
3. Напиши тесты для их обнаружения
4. Исправь баги (RED → GREEN)
5. Отрефактори код
6. Достигни 90%+ coverage
```

**Готово, когда:** у каждого из пяти багов есть тест, который падал до фикса, все тесты зелёные, coverage выше 90%, а итоговый коммит запушен в ветку `fix/bug-hunt-challenge`.

---

## Часть 1: Bug Hunting

### Step 1: Static Analysis

```bash
# Установи инструменты
npm install -D eslint @typescript-eslint/parser

# Запусти анализ
npx eslint src/**/*.js
```

### Step 2: Security Scan

```bash
npm audit
npm audit fix
```

### Step 3: Code Review Checklist

```markdown
Промпт:

@Files: [все файлы проекта]

Perform code review and find:

1. Potential bugs
   - Unhandled promises
   - Null/undefined checks missing
   - Race conditions
   - Memory leaks

2. Security issues
   - SQL injection
   - XSS vulnerabilities
   - Hardcoded secrets
   - Insufficient input validation

3. Performance issues
   - N+1 queries
   - Missing indexes
   - Unnecessary computations
   - Large bundle size

4. Code smells
   - Long functions
   - Code duplication
   - Magic numbers
   - Deep nesting

Create detailed report with:
- Issue location
- Severity (Critical/High/Medium/Low)
- Recommended fix
```

---

## Часть 2: Write Bug-Revealing Tests

### Пример для каждого найденного бага:

```javascript
// Bug 1: Missing null check
describe('Bug #1: Null user handling', () => {
    test('should handle null user gracefully', async () => {
        const result = await service.processUser(null);
        
        expect(result).toBeDefined();
        // Should not throw
    });
});

// Bug 2: Race condition
describe('Bug #2: Concurrent order updates', () => {
    test('should handle concurrent updates', async () => {
        const order = await createOrder();
        
        // Simulate concurrent updates
        const updates = Promise.all([
            service.updateOrder(order.id, { status: 'shipped' }),
            service.updateOrder(order.id, { status: 'cancelled' })
        ]);
        
        // Should not corrupt data
        const final = await service.getOrder(order.id);
        expect(final.status).toMatch(/shipped|cancelled/);
    });
});

// Bug 3: Memory leak
describe('Bug #3: Event listener cleanup', () => {
    test('should remove event listeners on destroy', () => {
        const instance = new Service();
        const initialListeners = process.listenerCount('data');
        
        instance.start();
        instance.destroy();
        
        const finalListeners = process.listenerCount('data');
        expect(finalListeners).toBe(initialListeners);
    });
});

// Bug 4: SQL injection
describe('Bug #4: SQL injection vulnerability', () => {
    test('should sanitize user input', async () => {
        const maliciousInput = "'; DROP TABLE users; --";
        
        await expect(
            service.searchUsers(maliciousInput)
        ).not.toThrow();
        
        // Verify table still exists
        const users = await db.query('SELECT * FROM users');
        expect(users).toBeDefined();
    });
});

// Bug 5: Unhandled promise
describe('Bug #5: Unhandled promise rejection', () => {
    test('should catch all promise rejections', async () => {
        const rejectionHandler = jest.fn();
        process.on('unhandledRejection', rejectionHandler);
        
        await service.riskyOperation();
        
        expect(rejectionHandler).not.toHaveBeenCalled();
        
        process.off('unhandledRejection', rejectionHandler);
    });
});
```

---

## Часть 3: Fix Bugs

### Промпт для каждого бага:

```
Bug #[N]: [название]

## Current Code
[код с багом]

## Test (RED)
[тест, который падает]

## Requirements
1. Make test GREEN
2. Don't break other tests
3. Follow best practices

Fix and explain the solution.
```

### Пример фикса:

```javascript
// Bug #1 Fix: Add null check

// Before
async function processUser(user) {
    const orders = await getOrders(user.id);
    return orders;
}

// After
async function processUser(user) {
    if (!user) {
        throw new ValidationError('User is required');
    }
    
    if (!user.id) {
        throw new ValidationError('User ID is required');
    }
    
    const orders = await getOrders(user.id);
    return orders;
}
```

---

## Часть 4: Refactoring

### Промпт:

```
All tests GREEN. Now refactor:

@Files: [все файлы]

Apply:
1. Extract methods (keep < 30 lines)
2. Remove duplication (< 5% duplication)
3. Simplify conditionals
4. Add guard clauses
5. Improve naming

CONSTRAINTS:
- Keep all tests GREEN
- No functionality changes
- Add/update tests for refactored code
- Document changes
```

---

## Часть 5: Coverage Analysis

### Jest Coverage Report:

```bash
npm test -- --coverage
```

### Анализ uncovered lines:

```javascript
// Промпт:

"Analyze coverage report:

Coverage: 87%
Uncovered lines: 23, 45-47, 102

@Files: [files with uncovered lines]

For each uncovered line:
1. Why is it not covered?
2. What test case is missing?
3. Write test to cover it

Target: 90%+ coverage"
```

### Добавление тестов:

```javascript
// Cover line 23: Error handling branch
test('should handle database connection error', async () => {
    mockDatabase.simulateConnectionError();
    
    await expect(
        service.getData()
    ).rejects.toThrow(DatabaseError);
});

// Cover lines 45-47: Edge case
test('should handle empty result set', async () => {
    mockDatabase.setResults([]);
    
    const result = await service.getData();
    
    expect(result).toEqual([]);
});

// Cover line 102: Timeout scenario
test('should timeout after 30 seconds', async () => {
    mockApi.setDelay(35000);
    
    await expect(
        service.fetchData()
    ).rejects.toThrow(TimeoutError);
}, 40000);
```

---

## Часть 6: Documentation

### Обнови документацию:

```markdown
## Testing

### Run Tests
\`\`\`bash
npm test                 # Unit tests
npm run test:integration # Integration tests
npm run test:e2e         # E2E tests
npm run test:coverage    # Coverage report
\`\`\`

### Coverage
- Lines: 92%
- Functions: 94%
- Branches: 88%
- Statements: 93%

### Test Structure
\`\`\`
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/            # End-to-end tests
└── fixtures/       # Test data
\`\`\`

### Bug Fixes
1. ✅ Null user handling (added validation)
2. ✅ Concurrent updates (added mutex lock)
3. ✅ Memory leak (added cleanup in destroy)
4. ✅ SQL injection (added input sanitization)
5. ✅ Unhandled promise (added try-catch)
```

---

## Часть 7: Performance Verification

### Load Testing:

```bash
# Установи k6 или artillery
npm install -D artillery

# Запусти load test
artillery quick --count 100 --num 10 http://localhost:3000/api/health
```

### Performance Profiling:

```javascript
// Промпт:

"Profile this function for performance:

@Files: [file]

Identify:
1. Bottlenecks
2. Unnecessary computations
3. Memory usage
4. Async issues

Optimize while keeping tests green."
```

---

## Часть 8: Final Verification

### Checklist:

```
✅ All bugs found and fixed
✅ All tests passing (GREEN)
✅ Coverage > 90%
✅ No security vulnerabilities
✅ Performance acceptable
✅ Documentation updated
✅ Code reviewed and approved
```

### Git Workflow:

```bash
git checkout -b fix/bug-hunt-challenge
git add .
git commit -m "fix: resolve 5 critical bugs, add tests, refactor

Bugs fixed:
1. Null user handling - added validation
2. Concurrent updates - added mutex lock
3. Memory leak - added event cleanup
4. SQL injection - added input sanitization
5. Unhandled promise - added error handling

Tests:
- Added 25 new tests
- Coverage: 92%
- All tests passing

Refactoring:
- Extracted 8 methods
- Reduced duplication from 12% to 3%
- Improved code quality score"

git push origin fix/bug-hunt-challenge
```

---

## 🎖️ Mission Complete!

### Достигнуто:

```
✅ 5 багов найдено и исправлено
✅ 25+ тестов написано
✅ 92% coverage
✅ Код отрефакторен
✅ Security audit пройден
✅ Performance оптимизирован
```

### Навыки недели:

```
✨ Debugging patterns
✨ Log analysis
✨ Refactoring strategies
✨ Test-driven development
✨ Production-ready code
```

---

## Checklist недели ✅

- [ ] Освоил AI debugging patterns
- [ ] Научился анализировать логи
- [ ] Применил refactoring strategies
- [ ] Написал comprehensive tests
- [ ] Достиг 90%+ coverage
- [ ] Исправил критические баги
- [ ] Подготовил production-ready код

---

## 🎉 Поздравляем!

Ты завершил неделю AI Debugging & Refactoring!

**Ты умеешь:**
- Находить и исправлять баги систематически
- Анализировать логи и предоставлять контекст ИИ
- Рефакторить код без потери функционала
- Писать comprehensive test suites
- Достигать высокого code coverage

**Следующая неделя:** Финальный проект и вклад в Open Source!

---

📚 [На следующую неделю →](../Week_8.md)
