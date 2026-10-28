# День 3: Refactoring Strategies 🏗️

**Трек:** 👨‍💻 Программист | **Время:** 40 минут

---

## 🎯 Цель дня

Освоить стратегии рефакторинга через AI-промпты с гарантией сохранения функционала.

---

## Refactoring Principles

### SOLID Principles:

```
S - Single Responsibility (единственная ответственность)
O - Open/Closed (открыт для расширения, закрыт для изменения)
L - Liskov Substitution (подстановка Барбары Лисков)
I - Interface Segregation (разделение интерфейсов)
D - Dependency Inversion (инверсия зависимостей)
```

### Refactoring Patterns:

```
1. Extract Method
2. Extract Variable
3. Rename Variable/Method
4. Replace Magic Numbers with Constants
5. Decompose Conditional
6. Consolidate Duplicate Conditional Fragments
7. Replace Nested Conditional with Guard Clauses
```

---

## AI-Driven Refactoring

### Pattern 1: Extract Method

#### Промпт:

```
@Files: largeFunction.js

Refactor: Extract methods from this large function.

Requirements:
1. Each method should do ONE thing
2. Name methods descriptively
3. Keep same functionality
4. Add JSDoc comments

Before refactoring:
- Show current structure
- Identify code smells

After refactoring:
- Show new structure
- Explain each extracted method
```

#### Пример:

```javascript
// Before (50 lines)
function processOrder(order) {
    // Validate order (10 lines)
    if (!order.items || order.items.length === 0) {
        throw new Error('Empty order');
    }
    for (const item of order.items) {
        if (!item.productId || item.quantity <= 0) {
            throw new Error('Invalid item');
        }
    }
    
    // Calculate total (15 lines)
    let total = 0;
    for (const item of order.items) {
        const product = getProduct(item.productId);
        const itemTotal = product.price * item.quantity;
        total += itemTotal;
    }
    order.total = total;
    
    // Apply discount (10 lines)
    if (order.couponCode) {
        const coupon = validateCoupon(order.couponCode);
        if (coupon && coupon.isValid) {
            total = total * (1 - coupon.discountPercent / 100);
        }
    }
    order.finalTotal = total;
    
    // Save order (15 lines)
    order.status = 'created';
    order.createdAt = new Date();
    saveToDatabase(order);
    sendConfirmationEmail(order);
}

// After (multiple small methods)
function processOrder(order) {
    validateOrder(order);
    calculateOrderTotal(order);
    applyDiscount(order);
    saveOrder(order);
}

function validateOrder(order) {
    if (!order.items?.length) {
        throw new Error('Empty order');
    }
    validateOrderItems(order.items);
}

function validateOrderItems(items) {
    for (const item of items) {
        if (!item.productId || item.quantity <= 0) {
            throw new Error('Invalid item');
        }
    }
}

function calculateOrderTotal(order) {
    order.total = order.items.reduce((sum, item) => {
        const product = getProduct(item.productId);
        return sum + (product.price * item.quantity);
    }, 0);
}

function applyDiscount(order) {
    if (!order.couponCode) return;
    
    const coupon = validateCoupon(order.couponCode);
    if (coupon?.isValid) {
        order.finalTotal = order.total * (1 - coupon.discountPercent / 100);
    } else {
        order.finalTotal = order.total;
    }
}

function saveOrder(order) {
    order.status = 'created';
    order.createdAt = new Date();
    saveToDatabase(order);
    sendConfirmationEmail(order);
}
```

---

### Pattern 2: Replace Magic Numbers

#### Промпт:

```
@Files: config.js

Replace all magic numbers with named constants.

Rules:
1. Extract to separate constants file
2. Use descriptive names
3. Add comments for non-obvious values
4. Keep functionality unchanged
```

#### Пример:

```javascript
// Before
if (user.age > 18) {
    // ...
}

setTimeout(callback, 5000);

const discount = total * 0.15;

// After
// constants.js
export const LEGAL_AGE = 18;
export const DEBOUNCE_DELAY_MS = 5000;
export const DEFAULT_DISCOUNT_RATE = 0.15; // 15% default discount

// code.js
import { LEGAL_AGE, DEBOUNCE_DELAY_MS, DEFAULT_DISCOUNT_RATE } from './constants';

if (user.age > LEGAL_AGE) {
    // ...
}

setTimeout(callback, DEBOUNCE_DELAY_MS);

const discount = total * DEFAULT_DISCOUNT_RATE;
```

---

### Pattern 3: Guard Clauses

#### Промпт:

```
@Files: nestedCode.js

Replace nested conditionals with guard clauses.

Benefits:
- Reduced nesting
- Early returns
- Clearer logic

Keep same behavior.
```

#### Пример:

```javascript
// Before (deeply nested)
function processUser(user) {
    if (user) {
        if (user.isActive) {
            if (user.hasPermission) {
                if (user.quota > 0) {
                    return performAction(user);
                } else {
                    return 'No quota';
                }
            } else {
                return 'No permission';
            }
        } else {
            return 'User inactive';
        }
    } else {
        return 'No user';
    }
}

// After (guard clauses)
function processUser(user) {
    if (!user) return 'No user';
    if (!user.isActive) return 'User inactive';
    if (!user.hasPermission) return 'No permission';
    if (user.quota <= 0) return 'No quota';
    
    return performAction(user);
}
```

---

## Refactoring Workflow

### Шаг 1: Baseline Tests

```markdown
Промпт:

"Before refactoring, create baseline tests:

@Files: [текущие файлы]

1. Write integration tests for current behavior
2. Cover all edge cases
3. Ensure all tests pass

These tests will verify refactoring doesn't break functionality."
```

### Шаг 2: Small Refactorings

```markdown
Промпт:

"Refactor incrementally:

1. Make ONE small change
2. Run tests
3. If pass → commit
4. If fail → rollback and fix

Do NOT make multiple changes at once.

Order of refactorings:
1. Rename unclear variables
2. Extract methods
3. Remove duplication
4. Simplify conditionals

After each step, ask for confirmation."
```

### Шаг 3: Verify Behavior

```markdown
Промпт:

"After refactoring:

1. Run all tests
2. Perform manual testing
3. Check for performance regression
4. Verify edge cases

Report:
- What changed?
- Any breaking changes?
- Performance impact?
- Improved readability score?"
```

---

## Code Quality Metrics

### Промпт для анализа:

```
Analyze code quality metrics:

@Files: [files]

Metrics to assess:
1. Cyclomatic Complexity (target: < 10 per function)
2. Lines of Code per function (target: < 30)
3. Maintainability Index (target: > 70)
4. Code Duplication (target: < 5%)
5. Coupling between objects (target: low)

Provide:
- Current scores
- Problem areas
- Refactoring recommendations
- Expected improvements
```

---

## Refactoring Checklist

```
Before:
□ Do I have test coverage?
□ Do tests pass?
□ Have I created a backup/branch?
□ Have I identified specific code smells?

During:
□ Am I making ONE change at a time?
□ Are tests still passing?
□ Am I committing frequently?
□ Am I documenting changes?

After:
□ Do all tests pass?
□ Is functionality unchanged?
□ Is code more readable?
□ Are there no new bugs?
□ Have I updated documentation?
```

---

## Practice

### Задание:

```
1. Выбери файл с code smells (длинные функции, дублирование)
2. Напиши baseline тесты
3. Примени 3 refactoring patterns
4. Проверь тестами
5. Документируй изменения
```

---

## Checklist дня ✅

- [ ] Понял refactoring principles
- [ ] Освоил 3+ refactoring patterns
- [ ] Научился писать baseline tests
- [ ] Попрактиковался в incremental refactoring
- [ ] Проверил quality metrics

---

## 🎯 Миссия

Выбери один файл с code smells, напиши baseline-тесты и примени ровно один паттерн из урока (например, guard clauses). Один шаг — один коммит.

**Готово, когда:** тесты зелёные до и после, диф коммита меняет структуру кода, а не поведение, и ты можешь показать в git diff, что именно упростилось.

---

📚 [На следующий день →](./Day_4.md)
