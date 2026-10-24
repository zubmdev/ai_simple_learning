# День 4: Искусство дебаггинга через промпты 🐛

Ошибки в коде — это нормально. Даже Senior-разработчики тратят 80% времени на дебаггинг. Сегодня ты научишься работать с ошибками через ИИ, не паникуя и систематически находя решения.

---

## 🎯 Цель дня

Научиться эффективно дебажить код, используя промпт-инжиниринг.

**Ты научишься:**
- Правильно описывать ошибки для ИИ
- Использовать CoT для дебаггинга
- Просить ИИ найти проблемы до запуска
- Создавать чеклисты для проверки кода

---

## Часть 1: Правильный настрой

### Главное правило

> **Ошибки — это не провал. Это часть процесса.**

**Традиционный подход:**
1. Увидел ошибку
2. Испугался
3. Начал случайно менять код
4. Потратил 3 часа
5. Сдался

**Vibe Coding подход:**
1. Увидел ошибку
2. Скопировал в ИИ
3. ИИ объяснил и помог
4. Исправил за 5 минут
5. Продолжил работу

---

## Часть 2: Как НЕ надо просить о помощи

### ❌ Плохие промпты

**Плохой промпт 1:**
```
Не работает. Помоги.
```

**Проблема:** ИИ не знает:
- Что не работает?
- Какая ошибка?
- Что ты делал?
- Что ожидал?

**Плохой промпт 2:**
```
У меня ошибка, исправь.
```

**Проблема:** Нет информации об ошибке.

**Плохой промпт 3:**
```
Код падает, не знаю почему.
```

**Проблема:** Нет traceback, нет кода, нет контекста.

---

## Часть 3: Как НАДО просить о помощи

### Чеклист для промпта-дебаггинга

Включи ВСЕ эти элементы:

| Элемент | Пример |
|---------|--------|
| ✅ Что делает код | "Парсю JSON из API" |
| ✅ Что ожидаешь | "Получить словарь с данными" |
| ✅ Что получается | "JSONDecodeError" |
| ✅ Полный traceback | Скопируй всё сообщение об ошибке |
| ✅ Код (релевантная часть) | Не весь файл, а проблемное место |
| ✅ Версии | Python 3.11, библиотека X версии Y |
| ✅ Окружение | Windows 11, VS Code |

### Шаблон промпта для дебаггинга

```
Дебаггинг Python кода.

Что делает код:
[описание функционала]

Что ожидаю:
[ожидаемое поведение]

Что происходит:
[фактическое поведение/ошибка]

Текст ошибки:
```
[полный traceback здесь]
```

Код:
```python
[код здесь]
```

Окружение:
- Python: [версия]
- Библиотека: [название и версия]
- ОС: [система]

Проанализируй пошагово:
1. В чём причина ошибки?
2. Как её исправить?
3. Как предотвратить в будущем?
```

---

## Часть 4: Примеры дебаггинга

### Пример 1: Ошибка с JSON

#### Получил ошибку:

```
Traceback (most recent call last):
  File "app.py", line 15, in <module>
    data = json.loads(response.text)
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

#### Плохой промпт:

```
JSONDecodeError, помоги.
```

#### Хороший промпт:

```
Дебаггинг Python кода.

Что делает код:
Скачиваю данные из API и парсю JSON.

Что ожидаю:
Получить словарь с данными пользователей.

Что происходит:
Получаю JSONDecodeError при попытке распарсить ответ.

Текст ошибки:
```
Traceback (most recent call last):
  File "app.py", line 15, in <module>
    data = json.loads(response.text)
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

Код:
```python
import requests
import json

response = requests.get('https://api.example.com/users')
data = json.loads(response.text)

for user in data['users']:
    print(user['name'])
```

Окружение:
- Python: 3.11
- requests: 2.31.0
- ОС: Windows 11

Проанализируй пошагово:
1. В чём причина ошибки?
2. Как её исправить?
3. Как предотвратить в будущем?
```

#### Ответ ИИ:

```
## Анализ ошибки

### 1. Причина ошибки

`JSONDecodeError: Expecting value: line 1 column 1 (char 0)` означает:
- **Попытка распарсить пустую строку** как JSON
- `response.text` пустой или не содержит JSON

### 2. Возможные причины

1. **API вернул пустой ответ** (status 204 No Content)
2. **API вернул ошибку** (status 4xx/5xx, HTML вместо JSON)
3. **API требует авторизацию** (401 Unauthorized)
4. **Проблема с сетью** (таймаут, блокировка)

### 3. Как исправить

Добавь проверки перед парсингом:

```python
import requests
import json

url = 'https://api.example.com/users'
response = requests.get(url)

# Проверка 1: Статус ответа
print(f"Status code: {response.status_code}")
print(f"Response text: {response.text[:200]}")  # Первые 200 символов

# Проверка 2: Успешный ли запрос
if response.status_code != 200:
    raise Exception(f"API error: {response.status_code}")

# Проверка 3: Не пустой ли ответ
if not response.text:
    raise Exception("Empty response from API")

# Проверка 4: Валидный ли JSON
try:
    data = response.json()  # Лучше чем json.loads(response.text)
except json.JSONDecodeError as e:
    raise Exception(f"Invalid JSON: {e}")

# Теперь работаем с данными
for user in data.get('users', []):
    print(user.get('name', 'Unknown'))
```

### 4. Как предотвратить

1. **Всегда проверяй status_code**
2. **Используй response.json() вместо json.loads(response.text)**
3. **Добавь обработку ошибок**
4. **Логируй ответ для отладки**

### 5. Улучшенный код с обработкой ошибок

```python
import requests
import logging
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_api_data(url: str) -> Optional[dict]:
    """
    Получает данные из API с обработкой ошибок.
    
    Args:
        url: URL API endpoint
        
    Returns:
        Словарь с данными или None при ошибке
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверка на 4xx/5xx
        
        data = response.json()
        logger.info(f"Successfully fetched data from {url}")
        return data
        
    except requests.Timeout:
        logger.error(f"Timeout fetching {url}")
        return None
    except requests.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

# Использование
data = fetch_api_data('https://api.example.com/users')
if data:
    for user in data.get('users', []):
        print(user.get('name', 'Unknown'))
```
```

---

### Пример 2: Логическая ошибка

#### Проблема: Код работает, но результат неправильный

```python
def calculate_discount(price, discount_percent):
    """Вычисляет цену со скидкой."""
    return price - (price * discount_percent)
```

**Тест:**
```python
>>> calculate_discount(100, 20)  # 20% скидка
-1900  # Ожидали 80, получили -1900!
```

#### Промпт для дебаггинга:

```
Дебаггинг логической ошибки.

Что делает код:
Вычисляет цену товара со скидкой.

Что ожидаю:
При цене 100 и скидке 20% должен вернуть 80.

Что получается:
Возвращает -1900.

Код:
```python
def calculate_discount(price, discount_percent):
    """Вычисляет цену со скидкой."""
    return price - (price * discount_percent)

print(calculate_discount(100, 20))  # -1900
```

Проанализируй:
1. В чём логическая ошибка?
2. Как исправить?
3. Добавь валидацию входных данных.
```

#### Ответ ИИ:

```
## Анализ логической ошибки

### 1. В чём ошибка?

**Проблема:** `discount_percent` передаётся как 20 (число), а не как 0.20 (доля).

**Что происходит:**
```python
price - (price * discount_percent)
100 - (100 * 20)
100 - 2000
-1900
```

**Должно быть:**
- `discount_percent` в процентах (20) → нужно разделить на 100
- `discount_percent` в долях (0.20) → использовать как есть

### 2. Как исправить?

**Вариант 1: Ожидаем проценты (рекомендуется)**

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Вычисляет цену со скидкой.
    
    Args:
        price: Исходная цена
        discount_percent: Процент скидки (например, 20 для 20%)
        
    Returns:
        Цена со скидкой
        
    Raises:
        ValueError: Если скидка не в диапазоне 0-100
        
    Examples:
        >>> calculate_discount(100, 20)
        80.0
        >>> calculate_discount(200, 50)
        100.0
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    
    if price < 0:
        raise ValueError("price cannot be negative")
    
    discount_factor = discount_percent / 100
    return price * (1 - discount_factor)

print(calculate_discount(100, 20))  # 80.0
```

**Вариант 2: Явная документация**

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Вычисляет цену со скидкой.
    
    Args:
        price: Исходная цена
        discount_percent: Процент скидки (0-100)
        
    Returns:
        Цена со скидкой
        
    Note:
        discount_percent указывается в процентах, не в долях!
        20% = discount_percent=20, а не discount_percent=0.20
    """
    return price * (1 - discount_percent / 100)
```

### 3. Добавь unit-тесты

```python
import pytest

def test_calculate_discount():
    # Обычные случаи
    assert calculate_discount(100, 20) == 80.0
    assert calculate_discount(200, 50) == 100.0
    assert calculate_discount(100, 0) == 100.0
    assert calculate_discount(100, 100) == 0.0
    
    # Edge cases
    assert calculate_discount(0, 20) == 0.0
    
    # Ошибки
    with pytest.raises(ValueError):
        calculate_discount(100, -10)  # Отрицательная скидка
    
    with pytest.raises(ValueError):
        calculate_discount(100, 150)  # Скидка > 100%
```
```

---

## Часть 5: Превентивный дебаггинг

### ИИ как ревьюер

Попроси ИИ найти проблемы **до** запуска:

```
Просмотри этот код и найди потенциальные проблемы:

1. Логические ошибки
2. Edge cases
3. Возможные исключения
4. Проблемы производительности
5. Небезопасный код

Код:
```python
def process_user_data(users):
    result = []
    for user in users:
        name = user['name']
        age = int(user['age'])
        if age > 18:
            result.append({'name': name, 'adult': True})
    return result
```

Для каждой проблемы:
- Опиши, что может пойти не так
- Приведи пример входных данных
- Предложи исправление
```

---

## Часть 6: Частые ошибки и их решения

### Ошибка 1: TypeError

**Пример:**
```
TypeError: 'NoneType' object is not subscriptable
```

**Причина:** Попытка обратиться к элементу None.

**Промпт:**
```
Получил ошибку TypeError: 'NoneType' object is not subscriptable
на строке: name = user['name']

Код:
```python
def get_user_name(user_id):
    user = get_user_from_db(user_id)  # Может вернуть None
    return user['name']  # Ошибка здесь
```

Как исправить?
```

### Ошибка 2: KeyError

**Пример:**
```
KeyError: 'email'
```

**Причина:** Ключ отсутствует в словаре.

**Решение:** Используй `.get()`:

```python
# Плохо
email = user['email']

# Хорошо
email = user.get('email', 'unknown@example.com')
```

### Ошибка 3: IndexError

**Пример:**
```
IndexError: list index out of range
```

**Причина:** Обращение к несуществующему индексу.

**Решение:** Проверяй длину:

```python
# Плохо
item = items[5]

# Хорошо
if len(items) > 5:
    item = items[5]
else:
    item = None
```

---

## Практические задания

### Задание 1: Исправь ошибку

Дан код с ошибкой. Опиши промпт для ИИ:

```python
def find_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print(find_average([]))  # Ошибка!
```

### Задание 2: Найди все проблемы

Проанализируй код и найди 5 потенциальных проблем:

```python
def save_user(user_data):
    import json
    with open('users.json', 'w') as f:
        json.dump(user_data, f)
    return True
```

### Задание 3: Создай чеклист

Создай чеклист для проверки функции, которая:
- Принимает URL
- Скачивает файл
- Сохраняет на диск

---

## Checklist дня ✅

- [ ] Понял структуру промпта для дебаггинга
- [ ] Научился описывать ошибки для ИИ
- [ ] Попрактиковался в дебаггинге через промпты
- [ ] Создал чеклист для превентивного дебаггинга

---

## Что дальше?

**Завтра (День 5):** Daily Mission! Ты улучшишь скрипт из Недели 1, используя все техники промптинга.

**Домашнее задание:**
- Найди 3 своих старых ошибки
- Примени техники дебаггинга через промпты
- Запиши, сколько времени сэкономил

---

📚 [На предыдущий день ←](./Day_3.md) | [На следующий день →](./Day_5.md)
