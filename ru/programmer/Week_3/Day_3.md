# День 3: Чтение чужого кода через AI 📖

**Трек:** 👨‍💻 Программист | **Время:** 25 минут

---

## 🎯 Цель

Быстро понимать любой код (legacy, open source, коллег) через AI.

---

## 🔬 Магические промпты

### Промпт 1: ELI5 (Explain Like I'm 5)

```
@Files: [файлы]

Объясни этот код так, будто я 10-летний.
Не используй жаргон.
```

### Промпт 2: Architecture

```
@Folder: src

Объясни архитектуру:
1. Какие слои?
2. Какие зависимости?
3. Точка входа?
4. Flow данных?
```

### Промпт 3: Find functionality

```
@Codebase

Где происходит:
- Авторизация?
- Подключение к БД?
- Обработка ошибок?
- Логирование?

Покажи файлы и строки.
```

---

## 🛠️ Практика

### Задание: Разобрать legacy код

**Шаг 1:** Создай "запутанный" файл

```python
# legacy.py
import json
from pathlib import Path
from typing import Any, Optional

class P:
    def __init__(self, s: str):
        self.s = Path(s)
        self._c: dict[str, Any] = {}
    
    def l(self) -> dict:
        if self.s.name in self._c:
            return self._c[self.s.name]
        with open(self.s, 'r') as f:
            d = json.load(f)
        self._c[self.s.name] = d
        return d
    
    def t(self, d: dict, k: list[str]) -> list[dict]:
        r = []
        for x in k:
            if x in d:
                r.append({x: d[x]})
        return r
    
    def s(self, d: list[dict], o: str) -> None:
        with open(o, 'w') as f:
            json.dump(d, f, indent=2)

if __name__ == '__main__':
    p = P('data.json')
    d = p.l()
    t = p.t(d, ['name', 'email'])
    p.s(t, 'out.json')
```

**Шаг 2:** Попроси AI объяснить

```
@Files: legacy.py

Объясни:
1. Что делает класс P?
2. Что означают методы l, t, s?
3. Какие проблемы в коде?
4. Как рефакторить?

Предложи читаемые названия.
```

**Шаг 3:** Рефакторинг

```
@Files: legacy.py

Рефакторинг:
1. Переименуй класс и методы
2. Добавь docstrings
3. Улучши type hints
4. Убери сокращения

Покажи полный рефакторенный код.
```

---

## 📊 Продвинутые техники

### Техника 1: Code Review

```
@Files: [код]

Найди:
- Security vulnerabilities
- Performance issues
- Code smells
- Best practices violations

Prioritize by severity.
```

### Техника 2: Dependency Analysis

```
@Folder: src

Построй dependency graph:
1. Какие модули зависят от каких?
2. Есть ли circular dependencies?
3. Какие модули самые связанные?
4. Как уменьшить coupling?
```

### Техника 3: Test Coverage

```
@Files: main.py

Напиши unit tests для всех функций.
Покрой:
- Happy path
- Edge cases
- Error cases
```

---

## 💡 Pro Tips

### Tip 1: Incremental understanding

```
1. Начни с @Codebase → общая архитектура
2. Потом @Folder: module → детали модуля
3. Потом @Files: file.py → конкретный код
```

### Tip 2: Ask specific questions

```
❌ "Объясни код"
✅ "Что делает функция X? Какие edge cases обрабатывает?"
```

### Tip 3: Request documentation

```
@Files: legacy.py

Напиши документацию:
1. README.md для проекта
2. Docstrings для всех функций
3. Type hints для всех параметров
```

---

## Checklist ✅

- [ ] Использовал ELI5 промпт
- [ ] Разобрал legacy код
- [ ] Сделал рефакторинг через AI
- [ ] Освоил code review через AI
- [ ] Попробовал dependency analysis

---

📚 [На предыдущий день ←](./Day_2.md) | [На следующий день →](./Day_4.md)
