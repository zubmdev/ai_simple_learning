# День 3: Итеративная разработка — Пишем первую фичу 🚀

**Трек:** 🌱 Начинающий | **Время:** 50 минут

---

## 🎯 Цель дня

Реализовать первую функцию приложения через промпты. Правило: одна фича — один промпт.

---

## Часть 1: Правило Vibe Coding

### Золотое правило:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ОДНА ФИЧА = ОДИН ПРОМПТ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Плохо:
"Напиши весь код для всего приложения сразу"

✅ Хорошо:
"Добавь в index.html форму для ввода задачи"
(потом отдельно)
"Напиши CSS стили для формы"
(потом отдельно)
"Реализуй JavaScript функцию addTask"
```

### Почему так?

```
✅ Меньше ошибок
✅ Проще проверять
✅ Можно откатить
✅ Понятнее процесс
```

---

## Часть 2: Фича 1 — HTML контент

### Задача:

Добавить в index.html:
- Заголовок приложения
- Форму для добавления задачи
- Контейнер для списка задач

### Промпт:

```
Открой файл index.html в проекте todo-app.

Добавь в body:
1. Заголовок <h1> с текстом "Мои задачи"
2. Форму с:
   - Полем ввода (input type="text")
   - Кнопкой "Добавить"
3. Пустой контейнер <ul id="task-list"> для задач

Используй семантичную разметку HTML5.
Добавь необходимые id и классы для CSS и JS.
```

### Результат ИИ:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To-Do App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <!-- Заголовок -->
        <h1>Мои задачи</h1>
        
        <!-- Форма для добавления -->
        <form id="task-form">
            <input 
                type="text" 
                id="task-input" 
                placeholder="Введите новую задачу..."
                required
            >
            <button type="submit">Добавить</button>
        </form>
        
        <!-- Список задач -->
        <ul id="task-list">
            <!-- Задачи будут добавляться сюда через JS -->
        </ul>
    </div>
    
    <script src="app.js"></script>
</body>
</html>
```

### Проверка:

```
Открой index.html в браузере. Что видишь?
```

**Ожидаемый результат:** Страница с заголовком, полем ввода и кнопкой (пока некрасивая).

---

## Часть 3: Фича 2 — CSS стили

### Задача:

Сделать приложение красивым.

### Промпт:

```
Открой styles.css в проекте todo-app.

Добавь стили:
1. Контейнер по центру экрана
2. Красивый заголовок
3. Форма: input и button в ряд
4. Input занимает большую часть ширины
5. Button красивая, синяя, с hover эффектом
6. Список задач: каждый элемент как карточка
7. Адаптивность для мобильных

Используй современные CSS (flexbox, box-shadow, border-radius).
Цвета: синий акцент, светлый фон.
```

### Результат ИИ:

```css
/* === Базовые стили === */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 40px 20px;
}

/* === Контейнер === */
.container {
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    padding: 40px;
    width: 100%;
    max-width: 500px;
}

/* === Заголовок === */
h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
    font-size: 2rem;
}

/* === Форма === */
#task-form {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
}

#task-input {
    flex: 1;
    padding: 12px 20px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

#task-input:focus {
    outline: none;
    border-color: #667eea;
}

button[type="submit"] {
    padding: 12px 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

button[type="submit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* === Список задач === */
#task-list {
    list-style: none;
}

.task-item {
    background: #f8f9fa;
    padding: 15px 20px;
    border-radius: 10px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 15px;
    transition: transform 0.2s;
}

.task-item:hover {
    transform: translateX(5px);
}

.task-text {
    flex: 1;
    font-size: 1rem;
    color: #333;
}

.task-item.completed .task-text {
    text-decoration: line-through;
    color: #999;
}

.delete-btn {
    background: #ff6b6b;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;
    font-size: 0.9rem;
}

.delete-btn:hover {
    background: #ee5a5a;
}

/* === Адаптивность === */
@media (max-width: 600px) {
    body {
        padding: 20px 10px;
    }
    
    .container {
        padding: 20px;
    }
    
    #task-form {
        flex-direction: column;
    }
    
    button[type="submit"] {
        width: 100%;
    }
}
```

### Проверка:

```
Обнови страницу в браузере. Как выглядит?
```

**Ожидаемый результат:** Красивая страница с формой, но задачи пока не добавляются.

---

## Часть 4: Фича 3 — JavaScript логика (часть 1)

### Задача:

Реализовать добавление задачи.

### Промпт:

```
Открой app.js в проекте todo-app.

Реализуй функционал:
1. При отправке формы (submit) → вызывать addTask
2. addTask:
   - Получить текст из input
   - Создать объект задачи: { id, text, completed }
   - Добавить в массив tasks
   - Вызвать renderTasks()
   - Очистить input
3. renderTasks:
   - Очистить список в HTML
   - Пройти по tasks и создать <li> для каждой
   - Добавить текст задачи, чекбокс, кнопку удаления

Пока БЕЗ сохранения в localStorage (это следующая фича).
```

### Результат ИИ:

```javascript
// === Данные ===
let tasks = [];
let taskIdCounter = 1;

// === DOM элементы ===
const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const taskList = document.getElementById('task-list');

// === Функции ===

/**
 * Добавить новую задачу
 */
function addTask(text) {
    const task = {
        id: taskIdCounter++,
        text: text,
        completed: false
    };
    
    tasks.push(task);
    renderTasks();
}

/**
 * Отобразить все задачи
 */
function renderTasks() {
    taskList.innerHTML = '';
    
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.className = 'task-item';
        li.dataset.id = task.id;
        
        if (task.completed) {
            li.classList.add('completed');
        }
        
        // Чекбокс
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = task.completed;
        checkbox.addEventListener('change', () => toggleTask(task.id));
        
        // Текст задачи
        const span = document.createElement('span');
        span.className = 'task-text';
        span.textContent = task.text;
        
        // Кнопка удаления
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = 'Удалить';
        deleteBtn.addEventListener('click', () => deleteTask(task.id));
        
        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(deleteBtn);
        
        taskList.appendChild(li);
    });
}

/**
 * Отметить задачу как выполненную
 */
function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        renderTasks();
    }
}

/**
 * Удалить задачу
 */
function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    renderTasks();
}

// === Обработчики событий ===

taskForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const text = taskInput.value.trim();
    
    if (text) {
        addTask(text);
        taskInput.value = '';
    }
});
```

### Проверка:

```
Обнови страницу и попробуй добавить задачу.
Работает?
```

**Ожидаемый результат:** Можно добавлять задачи, отмечать, удалять. Но при перезагрузке пропадают.

---

## Часть 5: Фича 4 — Сохранение в localStorage

### Задача:

Сохранять задачи между сессиями.

### Промпт:

```
Добавь в app.js:
1. При загрузке страницы → loadTasks() из localStorage
2. После каждого изменения → saveTasks() в localStorage
3. saveTasks: сохранить массив tasks как JSON
4. loadTasks: загрузить из localStorage, если есть

Используй ключ 'todo_tasks' для localStorage.
```

### Результат ИИ (добавить в app.js):

```javascript
// === Работа с localStorage ===

/**
 * Сохранить задачи в localStorage
 */
function saveTasks() {
    localStorage.setItem('todo_tasks', JSON.stringify(tasks));
}

/**
 * Загрузить задачи из localStorage
 */
function loadTasks() {
    const saved = localStorage.getItem('todo_tasks');
    if (saved) {
        tasks = JSON.parse(saved);
        // Найти максимальный ID для корректного taskIdCounter
        if (tasks.length > 0) {
            taskIdCounter = Math.max(...tasks.map(t => t.id)) + 1;
        }
        renderTasks();
    }
}

// === Обновлённые функции ===

function addTask(text) {
    const task = {
        id: taskIdCounter++,
        text: text,
        completed: false
    };
    
    tasks.push(task);
    saveTasks();  // ← Добавлено
    renderTasks();
}

function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        saveTasks();  // ← Добавлено
        renderTasks();
    }
}

function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    saveTasks();  // ← Добавлено
    renderTasks();
}

// === Инициализация ===
loadTasks();  // ← Загрузить при старте
```

### Проверка:

```
1. Добавь несколько задач
2. Перезагрузи страницу
3. Задачи должны сохраниться!
```

**Ожидаемый результат:** Задачи сохраняются и загружаются автоматически.

---

## Часть 6: Обновление PLAN.md

### Промпт:

```
Обнови PLAN.md:
- Отметь выполненные шаги
- Добавь что осталось сделать
```

### Результат:

```markdown
# План разработки To-Do App

## Текущий статус
✅ MVP ЗАВЕРШЁН!

## Шаги разработки
- [x] 1. Планирование
- [x] 2. Scaffolding
- [x] 3. HTML - добавлен контент
- [x] 4. CSS - добавлены стили
- [x] 5. JavaScript - реализована логика
- [x] 6. localStorage - сохранение работает

## Что можно улучшить (опционально)
- [ ] Добавить категории задач
- [ ] Добавить фильтры
- [ ] Добавить редактирование задач
- [ ] Добавить дату создания
- [ ] Деплой на GitHub Pages
```

---

## 🧠 Ключевые принципы

| Принцип | Объяснение |
|---------|------------|
| **Одна фича — один промпт** | Не проси всё сразу |
| **Проверяй после каждого шага** | Убедись, что работает |
| **Итеративный подход** | Добавляй по чуть-чуть |
| **Сохраняй прогресс** | Обновляй PLAN.md |
| **Не бойся просить исправить** | Если не работает — скажи ИИ |

---

## Checklist дня ✅

- [ ] Добавил HTML контент (форма, список)
- [ ] Добавил CSS стили
- [ ] Реализовал JavaScript логику
- [ ] Добавил сохранение в localStorage
- [ ] Протестировал добавление/удаление задач
- [ ] Проверил сохранение после перезагрузки
- [ ] Обновил PLAN.md

---

## Что дальше?

**Завтра (День 4):** Свяжем компоненты и улучшим приложение.

**Домашнее задание:**
- Потестируй приложение тщательно
- Найди баги или неудобства
- Запиши идеи для улучшений
- Подумай, что ещё можно добавить

---

📚 [На следующий день →](./Day_4.md)
