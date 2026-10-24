# День 1: Debugging Patterns — Breaking AI Loops 🔄

**Трек:** 👨‍💻 Программист | **Время:** 30 минут

---

## 🎯 Цель дня

Освоить продвинутые паттерны отладки при работе с AI-ассистентами.

---

## The AI Loop Problem

### Симптомы:

```
1. ИИ предлагает одно и то же решение
2. Исправление ломает то, что работало
3. Error recursions (баг порождает баг)
4. Context dilution (ИИ "забывает" ограничения)
```

---

## Pattern 1: Context Reset

### Проблема:

```
Previous context → ИИ пытается учесть все прошлые изменения
→ Противоречивые решения
```

### Решение:

```markdown
Промпт:

"RESET CONTEXT.

Current state:
@Files: [только текущие файлы]

Problem: [конкретная проблема]

Constraints:
- Do NOT touch: [что не трогать]
- Must preserve: [что должно работать]

Goal: [одна конкретная цель]

Ignore all previous attempts. Start fresh."
```

---

## Pattern 2: Binary Search Debugging

### Техника:

```
1. Раздели проблему пополам
2. Определи, в какой половине баг
3. Повтори

Пример:
- Баг в файле на 100 строк?
→ Проверь строки 1-50
→ Если баг там → проверь 1-25
→ Если баг там → проверь 1-12
...
```

### Промпт:

```
@Files: largeFile.js

Bug: Function processData fails.

Binary search approach:
1. Check first half (lines 1-50)
2. If bug there → narrow to 1-25
3. If not → check 51-100

Perform binary search. Tell me:
- Where is the bug?
- What's the root cause?"
```

---

## Pattern 3: Minimal Reproduction

### Создай минимальный пример:

```
@Files: complexFile.js

Extract the bug into minimal reproduction:

1. Create isolated test case
2. Remove all unrelated code
3. Keep only what triggers the bug

Generate: minimalBug.js with just the bug."
```

### Пример результата:

```javascript
// Original: 500 lines
// Minimal reproduction: 10 lines

function buggyFunction(input) {
    const result = input.filter(x => x.value > 0);
    // Bug: input is undefined when called with null
    return result.map(x => x.id);
}

// Test case
buggyFunction(null); // Crashes
buggyFunction([{value: 1, id: 1}]); // Works
```

---

## Pattern 4: State Isolation

### Проблема:

```
Global state → побочные эффекты
→ трудно понять, что изменило данные
```

### Решение:

```
@Files: app.js

Add state logging:

1. Before each mutation, log state
2. After each mutation, log state
3. Show what changed

Create stateDiff logger."
```

### Код:

```javascript
// stateLogger.js
let previousState = {};

export function logStateChange(action, newState) {
    const diff = deepDiff(previousState, newState);
    
    console.log(`
Action: ${action}
Changed: ${JSON.stringify(diff, null, 2)}
Before: ${JSON.stringify(previousState, null, 2)}
After: ${JSON.stringify(newState, null, 2)}
    `);
    
    previousState = JSON.parse(JSON.stringify(newState));
}

function deepDiff(oldObj, newObj) {
    const diff = {};
    for (const key in newObj) {
        if (JSON.stringify(oldObj[key]) !== JSON.stringify(newObj[key])) {
            diff[key] = {
                from: oldObj[key],
                to: newObj[key]
            };
        }
    }
    return diff;
}
```

---

## Pattern 5: Error Context Stack

### Структура:

```markdown
## Error Context

### Immediate Error
```
[Ошибка из логов/консоли]
```

### Stack Trace
```
[Полный stack trace]
```

### Relevant Code
```javascript
// Код из файла, где ошибка
```

### Data State
```json
{
  "variable": "value at time of error"
}
```

### Expected vs Actual
- Expected: [что ожидалось]
- Actual: [что случилось]

### Recent Changes
- [Что менялось перед ошибкой]
```

### Промпт:

```
Analyze error context:

## Immediate Error
TypeError: Cannot read property 'id' of undefined

## Stack Trace
at getUserById (user.service.js:45)
at UserController.get (user.controller.js:23)

## Code
[вставь user.service.js]

## Data State
userId: "abc123" (from request)
users: [] (empty array!)

## Expected vs Actual
Expected: Return user object
Actual: TypeError

## Recent Changes
Added caching layer yesterday

Root cause? Solution?"
```

---

## Pattern 6: Rubber Duck + AI

### Техника:

```
1. Объясни проблему "резиновой уточке" (вслух или текстом)
2. Пока объясняешь — часто находишь решение сам
3. Если нет — отправь объяснение ИИ
```

### Пример промпта:

```
Let me explain the problem step by step:

1. I have a function that fetches users
2. It should return an array of users
3. But sometimes it returns undefined
4. I think it happens when the database is empty
5. The function is called from 3 places
6. Only one place handles the empty case

Here's my thinking:
- Should I add a default return []?
- Or should callers handle undefined?
- What's the best practice?

[Attach code]

Am I on the right track?"
```

---

## Pattern 7: Hypothesis Testing

### Подход:

```
1. Сформулируй гипотезу
2. Напиши тест для проверки
3. Запусти тест
4. Подтверди или опровергни гипотезу
```

### Промпт:

```
Hypothesis: The bug occurs when user.email is null.

Write a test to verify:
1. Create user with null email
2. Call processUser()
3. Expect: error OR graceful handling

If test fails → hypothesis wrong
If test passes → confirm fix needed"
```

### Тест:

```javascript
describe('processUser with null email', () => {
    test('should handle null email gracefully', () => {
        const user = { id: 1, email: null };
        
        // Hypothesis: this will throw or return error
        const result = processUser(user);
        
        expect(result).toBeDefined();
        // OR
        expect(() => processUser(user)).toThrow();
    });
});
```

---

## Debugging Checklist

```
□ Can I reproduce the bug consistently?
□ Have I checked logs/console for errors?
□ Have I isolated the problematic code?
□ Have I created a minimal reproduction?
□ Have I checked recent changes (git diff)?
□ Have I cleared caches and restarted?
□ Have I searched for similar issues online?
□ Have I tried the binary search approach?
□ Have I written a test for the bug?
□ Have I documented the fix?
```

---

## Practice

### Задание:

```
Возьми баг из текущего проекта.

Примени 3 паттерна:
1. Context Reset
2. Minimal Reproduction
3. Hypothesis Testing

Документируй процесс.
```

---

## Checklist дня ✅

- [ ] Понял AI Loop Problem
- [ ] Освоил 7 паттернов отладки
- [ ] Научился Context Reset
- [ ] Попрактиковался в Binary Search
- [ ] Создал Minimal Reproduction
- [ ] Написал Hypothesis Test

---

📚 [На следующий день →](./Day_2.md)
