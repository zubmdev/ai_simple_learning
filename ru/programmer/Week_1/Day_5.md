# День 5: Практика — ASCII Генератор 🎯

**Трек:** 👨‍💻 Программист | **Время:** 30 минут

---

## 🎯 Миссия

Создать ASCII-арт генератор через итеративные промпты.

---

## ⚡ Быстрый старт

### Итерация 1: Базовая версия

```
Создай Python CLI для генерации ASCII-арта:
- Ввод имени пользователя
- Вывод ASCII-арта имени
- Используй библиотеку art или pyfiglet
```

```python
from art import tprint

name = input("Введите имя: ")
tprint(name)
```

### Итерация 2: Валидация и стили

```
Добавь:
- Валидацию имени (не пустое, только буквы/цифры)
- Выбор стиля (block, standard, slant, banner)
- Обработку Ctrl+C
```

### Итерация 3: Сохранение и история

```
Добавь:
- Сохранение в файл
- Историю генераций
- Цветной вывод (colorama)
```

---

## 🔧 Полный пример

```python
from art import tprint, FONT_NAMES
from colorama import init, Fore
import json
from datetime import datetime
import sys

init()

HISTORY_FILE = "ascii_history.json"

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history[-10:], f, indent=2)  # Храним последние 10

def get_style():
    print("Доступные стили:")
    for i, font in enumerate(FONT_NAMES[:10], 1):
        print(f"{i}. {font}")
    
    choice = input("Выбери стиль (1-10): ").strip()
    return FONT_NAMES[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= 10 else "block"

def main():
    print(Fore.CYAN + "=== ASCII Art Generator ===" + Fore.RESET)
    
    # История
    history = load_history()
    if history:
        print(f"\nПоследние генерации: {len(history)}")
    
    # Ввод
    try:
        name = input("Введите имя: ").strip()
        if not name:
            print(Fore.RED + "Имя не может быть пустым!" + Fore.RESET)
            return
        
        style = get_style()
        
        print(Fore.GREEN + f"\nГенерирую '{name}' в стиле '{style}'..." + Fore.RESET)
        tprint(name, font=style)
        
        # Сохранение
        save_to_file = input("\nСохранить в файл? (y/n): ").strip().lower()
        if save_to_file == 'y':
            with open(f"{name}_ascii.txt", 'w') as f:
                f.write(str(tprint(name, font=style, return_string=True)))
            print(Fore.GREEN + f"Сохранено в {name}_ascii.txt" + Fore.RESET)
        
        # История
        save_history({
            "name": name,
            "style": style,
            "timestamp": datetime.now().isoformat()
        })
        
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nПрервано пользователем." + Fore.RESET)
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## 🚀 Установка зависимостей

```bash
pip install art colorama
```

---

## 📋 Задание на самостоятельную работу

Выбери 1-2 улучшения и реализуй:

1. **Web UI** — Flask/FastAPI интерфейс
2. **Telegram бот** — отправка ASCII в Telegram
3. **API** — REST API для генерации
4. **Распознавание изображений** — ASCII из картинок
5. **GUI** — Tkinter/PyQt интерфейс

---

## ✅ Checklist недели 1

- [ ] Понял философию Vibe Coding
- [ ] Установил Continue.dev
- [ ] Выбрал и настроил модель
- [ ] Освоил AI workflow
- [ ] Создал практический проект

---

## 🧠 Ключевые выводы

| Принцип | Применение |
|---------|------------|
| Контекст важнее синтаксиса | Давай AI полную картину задачи |
| Итеративный подход | Проверяй каждый шаг |
| Code review обязателен | AI может ошибаться |
| Промпты — это навык | Практикуйся, улучшай формулировки |

---

## 📚 Что дальше?

**Неделя 2:** Промпт-инжиниринг — углублённые техники.

---

📚 [На предыдущий день ←](./Day_4.md) | [На следующую неделю →](../Week_2.md)
