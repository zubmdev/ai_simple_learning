# День 2: Zero-shot vs Few-shot в кодинге 🎯

Вчера мы разобрали анатомию промпта. Сегодня углубимся в технику **Few-shot** — как давать ИИ примеры, чтобы он писал код именно так, как тебе нужно.

---

## 🎯 Цель дня

Научиться использовать примеры для направления стиля и качества кода ИИ.

**Ты научишься:**
- Понимать разницу Zero-shot и Few-shot
- Выбирать подход для разных задач
- Давать эффективные примеры

---

## Часть 1: Что такое Zero-shot?

### Определение

**Zero-shot** — это когда ты просишь ИИ выполнить задачу **без примеров**.

ИИ использует только свои знания из обучения.

### Пример Zero-shot

```
Напиши функцию, которая преобразует JSON в XML.
```

**Результат:** ИИ напишет код, основываясь на общих знаниях о JSON и XML.

### Когда использовать Zero-shot?

| Ситуация | Подходит? |
|----------|-----------|
| Стандартная задача | ✅ Да |
| Не важен стиль кода | ✅ Да |
| Нет специфических требований | ✅ Да |
| Нужно быстро получить результат | ✅ Да |
| Нужен специфический стиль | ❌ Нет |
| Проект со сложившимся стилем | ❌ Нет |
| Нестандартные требования | ❌ Нет |

### Плюсы Zero-shot

- ✅ Быстро (короткий промпт)
- ✅ Подходит для простых задач
- ✅ ИИ свободен в выборе решения

### Минусы Zero-shot

- ❌ Результат может не соответствовать ожиданиям
- ❌ Стиль кода может отличаться от твоего проекта
- ❌ ИИ может выбрать не тот подход

---

## Часть 2: Что такое Few-shot?

### Определение

**Few-shot** — это когда ты даёшь ИИ **1-3 примера** перед задачей.

ИИ "учится" на примерах и повторяет стиль.

### Пример Few-shot

```
Напиши функцию для конвертации CSV в JSON, следуя этому стилю:

Пример 1:
def yaml_to_dict(yaml_str: str) -> dict:
    """Конвертирует YAML строку в словарь.
    
    Args:
        yaml_str: YAML строка
        
    Returns:
        Словарь с данными
        
    Raises:
        ValueError: Если YAML невалидный
    """
    import yaml
    try:
        return yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")

Пример 2:
def xml_to_dict(xml_str: str) -> dict:
    """Конвертирует XML строку в словарь.
    
    Args:
        xml_str: XML строка
        
    Returns:
        Словарь с данными
        
    Raises:
        ValueError: Если XML невалидный
    """
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(xml_str)
        return {child.tag: child.text for child in root}
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}")

Теперь напиши функцию csv_to_json в том же стиле.
```

### Что даёт Few-shot?

ИИ "видит" паттерны в примерах:
- 📝 Формат docstring (Google style)
- ⚠️ Обработка ошибок (try/except + raise ValueError)
- 📦 Импорты внутри функции
- 🏷️ Type hints
- 📖 Подробное описание в docstring

### Когда использовать Few-shot?

| Ситуация | Подходит? |
|----------|-----------|
| Нужен специфический стиль | ✅ Да |
| Проект со сложившимся стилем | ✅ Да |
| Нестандартные требования | ✅ Да |
| Консистентность в проекте | ✅ Да |
| Простая стандартная задача | ❌ Нет (избыточно) |
| Ограниченное контекстное окно | ❌ Нет (примеры занимают место) |

### Плюсы Few-shot

- ✅ Точный контроль стиля
- ✅ Консистентность в проекте
- ✅ Лучшее понимание требований

### Минусы Few-shot

- ❌ Длинный промпт
- ❌ Требует времени на подготовку примеров
- ❌ Занимает контекстное окно модели

---

## Часть 3: Сколько примеров нужно?

### Правило

| Количество примеров | Когда использовать |
|---------------------|-------------------|
| **1 пример** | Простой паттерн, нужно показать стиль |
| **2-3 примера** | Сложный паттерн, нужно показать вариации |
| **4+ примеров** | Редко нужно, лучше разбить на подзадачи |

### Пример с 1 примером

**Ситуация:** Все функции в проекте логируют действия.

```
Вот пример функции из моего проекта:

def read_file(path: str) -> str:
    """Читает файл и возвращает содержимое."""
    import logging
    logging.info(f"Reading file: {path}")
    with open(path, 'r') as f:
        content = f.read()
    logging.info(f"Successfully read {len(content)} chars")
    return content

Напиши функцию write_file в том же стиле.
```

**Результат:** ИИ добавит логирование в новую функцию.

### Пример с 2-3 примерами

**Ситуация:** Нужно показать вариации.

```
Примеры функций из моего проекта:

def get_user(user_id: int) -> dict | None:
    """Получает пользователя по ID."""
    import logging
    logging.info(f"Getting user: {user_id}")
    # ... implementation

def get_all_users() -> list[dict]:
    """Получает всех пользователей."""
    import logging
    logging.info("Getting all users")
    # ... implementation

def create_user(name: str, email: str) -> dict:
    """Создаёт нового пользователя."""
    import logging
    logging.info(f"Creating user: {name}, {email}")
    # ... implementation

Напиши функцию update_user в том же стиле.
```

**Результат:** ИИ поймёт паттерн: все CRUD функции логируют действия.

---

## Часть 4: Практика — Zero-shot vs Few-shot

### Задача: Функция для работы с API

### Вариант A: Zero-shot

**Промпт:**

```
Напиши функцию для получения данных из API.
URL: https://api.example.com/users
Верни список пользователей.
```

**Результат (примерный):**

```python
import requests

def get_users():
    response = requests.get('https://api.example.com/users')
    return response.json()
```

**Проблемы:**
- ❌ Нет обработки ошибок
- ❌ Нет type hints
- ❌ Нет docstring
- ❌ Нет timeout
- ❌ URL захардкожен

### Вариант B: Few-shot

**Промпт:**

```
Напиши функцию get_users в стиле моего проекта:

Пример 1:
def get_posts() -> list[dict]:
    """Получает все посты из API.
    
    Returns:
        Список словарей с постами
        
    Raises:
        requests.RequestException: Если запрос не удался
    """
    import requests
    from typing import Any
    
    url = "https://api.example.com/posts"
    timeout = 10
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch posts: {e}")

Пример 2:
def get_comments(post_id: int) -> list[dict]:
    """Получает комментарии к посту.
    
    Args:
        post_id: ID поста
        
    Returns:
        Список комментариев
        
    Raises:
        ValueError: Если post_id < 1
        requests.RequestException: Если запрос не удался
    """
    import requests
    
    if post_id < 1:
        raise ValueError("post_id must be >= 1")
    
    url = f"https://api.example.com/posts/{post_id}/comments"
    timeout = 10
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch comments: {e}")

Теперь напиши get_users в том же стиле.
```

**Результат:**

```python
def get_users() -> list[dict]:
    """Получает всех пользователей из API.
    
    Returns:
        Список словарей с пользователями
        
    Raises:
        requests.RequestException: Если запрос не удался
    """
    import requests
    
    url = "https://api.example.com/users"
    timeout = 10
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch users: {e}")
```

**Отличия:**
- ✅ Есть обработка ошибок
- ✅ Есть type hints
- ✅ Есть docstring
- ✅ Есть timeout
- ✅ Консистентный стиль с проектом

---

## Часть 5: Как создавать хорошие примеры для Few-shot?

### Правило 1: Примеры должны быть реальными

❌ **Плохо:** Выдуманные примеры

```python
# Пример 1
def foo():
    pass

# Пример 2
def bar():
    pass
```

✅ **Хорошо:** Реальные функции из проекта

```python
# Пример 1 (реальная функция из utils.py)
def calculate_discount(price: float, discount_percent: float) -> float:
    """Вычисляет цену со скидкой."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

### Правило 2: Примеры должны быть разнообразными

❌ **Плохо:** Все примеры одинаковые

```python
def get_user_1(): ...
def get_user_2(): ...
def get_user_3(): ...
```

✅ **Хорошо:** Разные вариации

```python
def get_user(user_id: int): ...      # GET один
def get_all_users(): ...              # GET все
def create_user(data: dict): ...      # POST создать
def update_user(user_id: int, data: dict): ...  # PUT обновить
```

### Правило 3: Показывай полный паттерн

❌ **Плохо:** Только начало функции

```python
def process_data(data):
    # что-то делает
```

✅ **Хорошо:** Полная функция

```python
def process_data(data: list[dict]) -> list[dict]:
    """Обрабатывает данные.
    
    Args:
        data: Список словарей для обработки
        
    Returns:
        Обработанный список
        
    Raises:
        ValueError: Если data пустой
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    result = []
    for item in data:
        processed = {
            'id': item.get('id'),
            'name': item.get('name', '').upper()
        }
        result.append(processed)
    
    return result
```

---

## Часть 6: Когда Zero-shot достаточно?

### Ситуация 1: Простые функции

```
Напиши функцию сложения двух чисел на Python.
```

Zero-shot достаточно — задача тривиальная.

### Ситуация 2: Эксперименты

```
Напиши прототип функции для [задача].
```

Zero-shot подходит — ты ещё не знаешь, какой стиль нужен.

### Ситуация 3: Стандартные библиотеки

```
Напиши пример использования pandas для чтения CSV.
```

Zero-shot достаточно — есть стандартные подходы.

---

## Часть 7: Практические задания

### Задание 1: Определи подход

Для каждой задачи выбери: Zero-shot или Few-shot?

1. Написать функцию `sum(a, b)` — сложение двух чисел
2. Написать функцию в стиле существующего проекта с 50 функциями
3. Написать REST API endpoint для блога
4. Написать функцию с нестандартной обработкой ошибок (логирование в файл + отправка в Slack)
5. Написать "Hello World" на Python

### Задание 2: Создай Few-shot промпт

**Задача:** Написать функцию для работы с файлами конфигурации.

**Даны примеры из проекта:**

```python
# config_loader.py

def load_json_config(path: str) -> dict:
    """Загружает JSON конфигурацию.
    
    Args:
        path: Путь к файлу
        
    Returns:
        Словарь с конфигурацией
        
    Raises:
        FileNotFoundError: Если файл не найден
        json.JSONDecodeError: Если JSON невалидный
    """
    import json
    import logging
    
    logging.info(f"Loading config from {path}")
    
    with open(path, 'r') as f:
        config = json.load(f)
    
    logging.info(f"Loaded {len(config)} config items")
    return config

def load_yaml_config(path: str) -> dict:
    """Загружает YAML конфигурацию.
    
    Args:
        path: Путь к файлу
        
    Returns:
        Словарь с конфигурацией
        
    Raises:
        FileNotFoundError: Если файл не найден
        yaml.YAMLError: Если YAML невалидный
    """
    import yaml
    import logging
    
    logging.info(f"Loading config from {path}")
    
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    logging.info(f"Loaded {len(config)} config items")
    return config
```

**Твоя задача:** Напиши Few-shot промпт для функции `load_toml_config`.

### Задание 3: Сравни результаты

1. Напиши функцию `save_config` через Zero-shot
2. Напиши функцию `save_config` через Few-shot (используя примеры выше)
3. Сравни результаты — в чём разница?

---

## Checklist дня ✅

- [ ] Понял разницу Zero-shot и Few-shot
- [ ] Знаю, когда использовать каждый подход
- [ ] Попрактиковался в создании Few-shot промптов
- [ ] Создал функции через оба подхода и сравнил

---

## Что дальше?

**Завтра (День 3):** Chain of Thought — как заставить ИИ "думать" перед написанием кода. Это критически важно для сложных задач!

**Домашнее задание:**
- Возьми 3 функции из своего проекта (или придумай)
- Создай Few-shot промпт для новой функции
- Сравни результат с Zero-shot версией

---

📚 [На предыдущий день ←](./Day_1.md) | [На следующий день →](./Day_3.md)
