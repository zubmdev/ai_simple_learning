# День 5: Практика — Улучшение проекта 🚀

**Трек:** 👨‍💻 Программист | **Время:** 40 минут

---

## 🎯 Миссия

Улучши ASCII генератор из Недели 1, используя техники промптинга.

---

## 📋 Задачи

### 1. Code Review через AI

```
Проверь код на:
- Security issues
- Performance bottlenecks
- Error handling gaps
- Code quality

[вставь код]
```

### 2. Добавление тестов (Few-shot)

```python
Вот стиль тестов в проекте:

import pytest
from my_module import get_user_by_id

def test_get_user_by_id_exists():
    user = get_user_by_id(1)
    assert user is not None
    assert user.id == 1

def test_get_user_by_id_not_exists():
    user = get_user_by_id(999)
    assert user is None

Напиши тесты для функции validate_name(name: str) -> bool
```

### 3. Оптимизация (CoT)

```
Код работает, но можно улучшить.

Проанализируй:
1. Какие части можно оптимизировать?
2. Какие паттерны лучше применить?
3. Как улучшить читаемость?
4. Как добавить type safety?

Напиши улучшенную версию.
```

---

## 🛠️ Пример улучшенного кода

```python
from art import tprint, FONT_NAMES
from colorama import init, Fore
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import sys
from typing import Optional

init()

@dataclass
class AsciiArt:
    name: str
    style: str
    timestamp: str
    
    @classmethod
    def create(cls, name: str, style: str) -> 'AsciiArt':
        return cls(
            name=name,
            style=style,
            timestamp=datetime.now().isoformat()
        )

class AsciiGenerator:
    HISTORY_FILE = Path("ascii_history.json")
    MAX_HISTORY = 10
    
    def __init__(self):
        self.history = self._load_history()
    
    def generate(self, name: str, style: str = "block") -> str:
        if not self._validate_name(name):
            raise ValueError("Invalid name")
        
        tprint(name, font=style)
        self._save_to_history(name, style)
        return f"{name} generated in {style} style"
    
    def _validate_name(self, name: str) -> bool:
        return bool(name and name.isalnum())
    
    def _load_history(self) -> list[dict]:
        try:
            return json.loads(self.HISTORY_FILE.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_to_history(self, name: str, style: str) -> None:
        entry = AsciiArt.create(name, style)
        self.history.append(entry.__dict__)
        self.HISTORY_FILE.write_text(
            json.dumps(self.history[-self.MAX_HISTORY:], indent=2)
        )

def main() -> None:
    generator = AsciiGenerator()
    
    try:
        name = input(Fore.CYAN + "Name: " + Fore.RESET).strip()
        style = input("Style (block/standard/slant): ").strip() or "block"
        
        generator.generate(name, style)
        print(Fore.GREEN + "✅ Done!" + Fore.RESET)
    
    except ValueError as e:
        print(Fore.RED + f"Error: {e}" + Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nCancelled." + Fore.RESET)
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## 📊 Метрики улучшения

| Метрика | Было | Стало |
|---------|------|-------|
| Количество функций | 1 | 5+ |
| Type hints | ❌ | ✅ |
| Error handling | Basic | Full |
| Testability | ❌ | ✅ |
| Код-стайл | Script | Production-ready |

---

## ✅ Checklist недели 2

- [ ] Освоил P.T.C.F. модель промптов
- [ ] Понял Zero-shot vs Few-shot
- [ ] Научился применять CoT
- [ ] Освоил AI debugging
- [ ] Улучшил проект с помощью техник

---

## 🧠 Итоги

| Навык | Применение |
|-------|------------|
| Точные промпты | Меньше итераций, лучше результат |
| Few-shot | Консистентность кода в проекте |
| CoT | Сложные задачи, дебаггинг |
| AI debugging | Быстрое решение проблем |

---

📚 [На предыдущий день ←](./Day_4.md)
