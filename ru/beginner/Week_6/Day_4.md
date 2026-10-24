# День 4: Связывание компонентов — Контекст в действии 🔗

**Трек:** 🌱 Начинающий | **Время:** 45 минут

---

## 🎯 Цель дня

Понять, как файлы проекта работают вместе, и добавить улучшения через контекст.

---

## Часть 1: Как связаны файлы?

### Диаграмма связей:

```
┌─────────────────────────────────────────────┐
│              index.html                      │
│  ┌───────────────┐    ┌──────────────────┐ │
│  │   <link>      │    │    <script>      │ │
│  │  styles.css   │    │     app.js       │ │
│  └───────┬───────┘    └────────┬─────────┘ │
└──────────┼──────────────────────┼──────────┘
           │                      │
           ▼                      ▼
    ┌─────────────┐        ┌──────────────┐
    │ styles.css  │        │   app.js     │
    │             │        │              │
    │ .container  │←───────│ querySelector│
    │ #task-form  │←───────│ getElementById│
    │ .task-item  │←───────│ createElement│
    └─────────────┘        └──────────────┘
                                   │
                                   ▼
                           ┌──────────────┐
                           │ localStorage │
                           │              │
                           │ 'todo_tasks' │
                           └──────────────┘
```

### Проверка понимания:

```
Ответь на вопросы:
1. Где описан класс .container?
2. Где используется getElementById('task-form')?
3. Что происходит при нажатии "Добавить"?
4. Где сохраняются задачи?
```

---

## Часть 2: Использование контекста для улучшений

### Задача: Добавить уведомления

#### Промпт с контекстом:

```
@Files: index.html, app.js

Добавь уведомление при:
- Добавлении задачи: "Задача добавлена!"
- Удалении задачи: "Задача удалена"
- Отметке выполненной: "Отлично!"

Уведомление должно:
- Появляться на 2 секунды
- Быть красивым (зелёный цвет)
- Показываться вверху экрана
```

### Что делает ИИ:

1. **Читает index.html** → видит, куда добавить уведомление
2. **Читает app.js** → понимает, где вызвать
3. **Добавляет**:
   - HTML: `<div id="notification"></div>`
   - CSS: стили для notification (через app.js динамически)
   - JS: функцию `showNotification(message)`

### Результат:

```javascript
// Добавить в app.js

/**
 * Показать уведомление
 */
function showNotification(message) {
    // Создать элемент уведомления
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Удалить через 2 секунды
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Обновить функции
function addTask(text) {
    // ... existing code ...
    showNotification('Задача добавлена!');
}

function deleteTask(id) {
    // ... existing code ...
    showNotification('Задача удалена');
}

function toggleTask(id) {
    // ... existing code ...
    if (task.completed) {
        showNotification('Отлично!');
    }
}
```

---

## Часть 3: Добавление улучшений

### Улучшение 1: Счётчик задач

```
@Files: index.html, app.js

Добавь счётчик задач:
- Показывать: "Всего задач: X"
- Показывать: "Выполнено: Y"
- Обновлять при каждом изменении
```

### Результат:

```html
<!-- Добавить в index.html после заголовка -->
<div class="stats">
    <span id="total-count">Всего: 0</span>
    <span id="completed-count">Выполнено: 0</span>
</div>
```

```javascript
// Добавить в app.js

function updateStats() {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    
    document.getElementById('total-count').textContent = `Всего: ${total}`;
    document.getElementById('completed-count').textContent = `Выполнено: ${completed}`;
}

// Вызывать в renderTasks()
function renderTasks() {
    // ... existing code ...
    updateStats();
}
```

---

### Улучшение 2: Подтверждение удаления

```
@Files: app.js

При удалении задачи:
- Спросить подтверждение: "Удалить задачу?"
- Если "Да" → удалить
- Если "Нет" → отменить
```

### Результат:

```javascript
function deleteTask(id) {
    const task = tasks.find(t => t.id === id);
    
    if (confirm(`Удалить задачу "${task.text}"?`)) {
        tasks = tasks.filter(t => t.id !== id);
        saveTasks();
        renderTasks();
        showNotification('Задача удалена');
    }
}
```

---

### Улучшение 3: Пустой список

```
@Files: index.html, app.js, styles.css

Когда задач нет:
- Показывать: "Нет задач. Добавьте первую!"
- Красивое сообщение по центру
```

### Результат:

```javascript
function renderTasks() {
    taskList.innerHTML = '';
    
    if (tasks.length === 0) {
        const emptyMessage = document.createElement('li');
        emptyMessage.className = 'empty-message';
        emptyMessage.textContent = 'Нет задач. Добавьте первую!';
        taskList.appendChild(emptyMessage);
        return;
    }
    
    // ... existing code ...
}
```

```css
/* Добавить в styles.css */
.empty-message {
    text-align: center;
    color: #999;
    padding: 40px;
    font-size: 1.2rem;
    font-style: italic;
}
```

---

## Часть 4: Работа с ошибками

### Сценарий: ИИ допустил ошибку

#### Пример ошибки:

```
Ты: "Добавь кнопку 'Очистить всё'"

ИИ: (добавляет кнопку, но она не работает)
```

#### Как исправить:

```
Кнопка "Очистить всё" не работает.

@Files: app.js

Вот код кнопки (показываю из HTML):
<button id="clear-all">Очистить всё</button>

Почему не работает? Исправь.
```

#### ИИ анализирует:

```
Проблема: Кнопка добавлена в HTML, но нет обработчика в JS.

Решение:
```

```javascript
// Добавить в app.js

const clearAllBtn = document.getElementById('clear-all');

if (clearAllBtn) {
    clearAllBtn.addEventListener('click', () => {
        if (tasks.length > 0 && confirm('Удалить все задачи?')) {
            tasks = [];
            saveTasks();
            renderTasks();
            showNotification('Все задачи удалены');
        }
    });
}
```

---

## Часть 5: Рефакторинг через контекст

### Задача: Улучшить код

```
@Files: app.js

Проанализируй код и предложи улучшения:
- Читаемость
- Производительность
- Безопасность

Не меняй функционал, только улучши код.
```

### Пример ответа ИИ:

```
📊 Анализ кода:

✅ Хорошо:
- Функции разбиты логично
- Используются const/let
- Есть комментарии

⚠️ Можно улучшить:
1. Вынести селекторы в константы
2. Добавить валидацию input
3. Использовать делегирование событий
4. Добавить обработку ошибок

Хочешь применить эти улучшения?
```

### После согласования:

```javascript
// === Константы селекторов ===
const SELECTORS = {
    form: '#task-form',
    input: '#task-input',
    list: '#task-list',
    totalCount: '#total-count',
    completedCount: '#completed-count',
    clearAll: '#clear-all'
};

// === Валидация ===
function validateTaskText(text) {
    if (!text || typeof text !== 'string') {
        throw new Error('Текст задачи обязателен');
    }
    if (text.length > 200) {
        throw new Error('Максимум 200 символов');
    }
    return text.trim();
}

// === Делегирование событий ===
taskList.addEventListener('click', (e) => {
    const taskItem = e.target.closest('.task-item');
    if (!taskItem) return;
    
    const taskId = parseInt(taskItem.dataset.id);
    
    if (e.target.matches('input[type="checkbox"]')) {
        toggleTask(taskId);
    } else if (e.target.matches('.delete-btn')) {
        deleteTask(taskId);
    }
});
```

---

## Часть 6: Финальное тестирование

### Чеклист тестирования:

```
Проверь:
[ ] Добавление задачи работает
[ ] Задача появляется в списке
[ ] Можно отметить выполненной
[ ] Текст зачёркнут
[ ] Можно удалить
[ ] Подтверждение удаления есть
[ ] Задачи сохраняются после перезагрузки
[ ] Счётчик обновляется
[ ] Уведомления появляются
[ ] Пустой список показывает сообщение
[ ] Кнопка "Очистить всё" работает
[ ] На мобильном выглядит хорошо
```

### Промпт для ИИ:

```
Протестируй приложение и скажи:
1. Что работает хорошо?
2. Что нужно исправить?
3. Что можно улучшить?
```

---

## Часть 7: Сохранение финальной версии

### Создай CHANGELOG.md:

```
Создай файл CHANGELOG.md с историей изменений:
- Что было сделано
- Когда
- Какие улучшения добавлены
```

Пример:

```markdown
# Changelog

## [1.0.0] - 2024-01-15

### Added
- Базовая структура проекта
- Форма для добавления задач
- Список задач с отображением
- Отметка выполненных задач
- Удаление задач
- Сохранение в localStorage
- Уведомления при действиях
- Счётчик задач
- Подтверждение удаления
- Сообщение при пустом списке
- Кнопка "Очистить всё"
- Адаптивный дизайн

### Technical
- Семантичная HTML5 разметка
- Современные CSS стили
- ES6+ JavaScript
- LocalStorage API
```

---

## 🧠 Ключевые принципы

| Принцип | Объяснение |
|---------|------------|
| **Контекст — связь** | @Files показывает ИИ связи между файлами |
| **Итеративные улучшения** | Добавляй по одному улучшению |
| **Тестируй часто** | После каждого изменения |
| **Документируй изменения** | CHANGELOG.md помогает понять историю |
| **Не бойся рефакторить** | Улучшай код без изменения функционала |

---

## Checklist дня ✅

- [ ] Понял связи между файлами проекта
- [ ] Добавил уведомления
- [ ] Добавил счётчик задач
- [ ] Добавил подтверждение удаления
- [ ] Добавил сообщение для пустого списка
- [ ] Исправил ошибки (если были)
- [ ] Провёл рефакторинг кода
- [ ] Протестировал все функции
- [ ] Создал CHANGELOG.md

---

## Что дальше?

**Завтра (День 5):** Daily Mission — завершим MVP и подготовим к деплою.

**Домашнее задание:**
- Потестируй приложение ещё раз
- Подумай, что ещё можно улучшить
- Запиши идеи для версии 2.0
- Подготовь вопросы по деплою

---

📚 [На следующий день →](./Day_5.md)
