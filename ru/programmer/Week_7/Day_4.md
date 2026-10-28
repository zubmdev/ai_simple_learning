# День 4: Test-Driven AI Development ✅

**Трек:** 👨‍💻 Программист | **Время:** 45 минут

---

## 🎯 Цель дня

Освоить TDD (Test-Driven Development) через AI-промпты для создания надежного кода.

---

## TDD Cycle

### Red-Green-Refactor:

```
1. RED: Write failing test
2. GREEN: Write minimal code to pass test
3. REFACTOR: Improve code while keeping tests green
4. Repeat
```

---

## AI-TDD Workflow

### Phase 1: Write Test First

#### Промпт:

```
Implement TDD for feature: [название фичи]

## Requirements
- [требования к функционалу]
- [edge cases]

## Task
1. Write failing test FIRST
2. Test should describe expected behavior
3. Include edge cases
4. DO NOT write implementation yet

Create: [feature].test.js
```

#### Пример:

```javascript
// payment.test.js (RED - тест падает)

describe('PaymentService', () => {
    let paymentService;
    
    beforeEach(() => {
        paymentService = new PaymentService();
    });
    
    describe('processPayment', () => {
        test('should successfully process valid payment', async () => {
            const payment = {
                amount: 100,
                currency: 'USD',
                cardNumber: '4242424242424242',
                cvv: '123',
                expiryMonth: '12',
                expiryYear: '2025'
            };
            
            const result = await paymentService.processPayment(payment);
            
            expect(result.success).toBe(true);
            expect(result.transactionId).toBeDefined();
            expect(result.amount).toBe(100);
        });
        
        test('should reject invalid card number', async () => {
            const payment = {
                amount: 100,
                currency: 'USD',
                cardNumber: '123', // Invalid
                cvv: '123',
                expiryMonth: '12',
                expiryYear: '2025'
            };
            
            await expect(
                paymentService.processPayment(payment)
            ).rejects.toThrow('Invalid card number');
        });
        
        test('should reject negative amount', async () => {
            const payment = {
                amount: -100,
                currency: 'USD',
                cardNumber: '4242424242424242',
                cvv: '123',
                expiryMonth: '12',
                expiryYear: '2025'
            };
            
            await expect(
                paymentService.processPayment(payment)
            ).rejects.toThrow('Amount must be positive');
        });
        
        test('should handle payment gateway timeout', async () => {
            // Mock gateway timeout
            paymentService.gateway.setTimeout(true);
            
            const payment = { /* valid payment */ };
            
            await expect(
                paymentService.processPayment(payment)
            ).rejects.toThrow('Payment gateway timeout');
        });
    });
});
```

---

### Phase 2: Implement Code

#### Промпт:

```
Now implement the code to make tests pass:

@Files: payment.test.js

Requirements:
1. Write MINIMAL code to pass tests
2. Don't over-engineer
3. Make tests GREEN
4. Handle all test cases

Create: payment.service.js
```

#### Пример:

```javascript
// payment.service.js (GREEN - тесты проходят)

export class PaymentService {
    constructor() {
        this.gateway = new PaymentGateway();
    }
    
    async processPayment(payment) {
        // Validate
        this.validatePayment(payment);
        
        // Process
        const result = await this.gateway.charge(payment);
        
        if (!result.success) {
            throw new Error(result.error);
        }
        
        return {
            success: true,
            transactionId: result.id,
            amount: payment.amount
        };
    }
    
    validatePayment(payment) {
        if (!this.isValidCardNumber(payment.cardNumber)) {
            throw new Error('Invalid card number');
        }
        
        if (payment.amount <= 0) {
            throw new Error('Amount must be positive');
        }
        
        if (!payment.cvv || payment.cvv.length !== 3) {
            throw new Error('Invalid CVV');
        }
        
        // More validations...
    }
    
    isValidCardNumber(number) {
        // Luhn algorithm
        const digits = number.replace(/\D/g, '');
        if (digits.length < 13 || digits.length > 19) {
            return false;
        }
        
        let sum = 0;
        let isEven = false;
        
        for (let i = digits.length - 1; i >= 0; i--) {
            let digit = parseInt(digits[i], 10);
            
            if (isEven) {
                digit *= 2;
                if (digit > 9) {
                    digit -= 9;
                }
            }
            
            sum += digit;
            isEven = !isEven;
        }
        
        return sum % 10 === 0;
    }
}
```

---

### Phase 3: Refactor

#### Промпт:

```
Tests are GREEN. Now refactor:

@Files: payment.service.js, payment.test.js

Improve:
1. Extract validation to separate class
2. Add better error messages
3. Improve code organization
4. Add logging

CONSTRAINT: Keep tests GREEN
Run tests after each change.
```

#### Пример:

```javascript
// payment.validator.js
export class PaymentValidator {
    validate(payment) {
        this.validateCardNumber(payment.cardNumber);
        this.validateAmount(payment.amount);
        this.validateCVV(payment.cvv);
        this.validateExpiry(payment.expiryMonth, payment.expiryYear);
    }
    
    validateCardNumber(number) {
        if (!this.luhnCheck(number)) {
            throw new PaymentValidationError(
                `Invalid card number: ${this.maskCard(number)}`
            );
        }
    }
    
    validateAmount(amount) {
        if (amount <= 0) {
            throw new PaymentValidationError(
                `Amount must be positive, got: ${amount}`
            );
        }
    }
    
    // ... more validations
    
    luhnCheck(number) {
        // Luhn algorithm implementation
    }
    
    maskCard(number) {
        return number.slice(-4).padStart(number.length, '*');
    }
}

// payment.service.js (refactored)
export class PaymentService {
    constructor(validator = new PaymentValidator()) {
        this.validator = validator;
        this.gateway = new PaymentGateway();
        this.logger = new Logger();
    }
    
    async processPayment(payment) {
        this.logger.info('Processing payment', { amount: payment.amount });
        
        this.validator.validate(payment);
        
        try {
            const result = await this.gateway.charge(payment);
            
            this.logger.info('Payment successful', { 
                transactionId: result.id 
            });
            
            return this.buildSuccessResponse(payment, result);
        } catch (error) {
            this.logger.error('Payment failed', { error: error.message });
            throw error;
        }
    }
    
    buildSuccessResponse(payment, result) {
        return {
            success: true,
            transactionId: result.id,
            amount: payment.amount
        };
    }
}
```

---

## Test Types

### Unit Tests:

```
Промпт:

"Write unit tests for [function/module]:

1. Test normal cases
2. Test edge cases
3. Test error cases
4. Mock dependencies

Focus on isolated testing.
Each test should be independent."
```

### Integration Tests:

```
Промпт:

"Write integration tests for [feature]:

1. Test components working together
2. Use real dependencies (or realistic mocks)
3. Test data flow
4. Test error handling across boundaries

Use test database/fixtures."
```

### E2E Tests:

```
Промпт:

"Write E2E tests for [user flow]:

1. Test complete user journey
2. Use real browser (Playwright/Cypress)
3. Test UI interactions
4. Verify final state

Example: User registers → confirms email → logs in"
```

---

## Test Coverage

### Промпт:

```
Analyze test coverage for @Files: [files]

Provide:
1. Coverage percentage per file
2. Uncovered lines/branches
3. Missing test cases
4. Recommendations for improvement

Target: 80%+ coverage
```

### Jest Configuration:

```javascript
// jest.config.js
module.exports = {
    coverageThreshold: {
        global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80
        }
    },
    collectCoverageFrom: [
        'src/**/*.js',
        '!src/**/*.test.js',
        '!src/mocks/**'
    ]
};
```

---

## Practice

### Задание:

```
Implement TDD for a feature:

1. Write 5+ tests FIRST (RED)
2. Implement code (GREEN)
3. Refactor while keeping tests green
4. Achieve 80%+ coverage

Suggested features:
- User authentication
- Order processing
- Data validation
```

---

## Checklist дня ✅

- [ ] Понял TDD cycle (Red-Green-Refactor)
- [ ] Научился писать тесты FIRST
- [ ] Реализовал код для прохождения тестов
- [ ] Отрефакторил с зелёными тестами
- [ ] Достиг 80%+ coverage

---

## 🎯 Миссия

Пройди полный цикл Red-Green-Refactor на маленькой функции: валидатор пароля, конвертер дат или парсер строки. Сначала тест — потом код.

**Готово, когда:** тест был написан и упал до появления кода, минимальная реализация делает его зелёным, рефакторинг цвет не теряет, а `npm test -- --coverage` показывает 100% по этой функции.

---

📚 [На следующий день →](./Day_5.md)
