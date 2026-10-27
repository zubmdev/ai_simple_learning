# День 5: Практика — Улучшение проекта 🚀

**Трек:** 👨‍💻 Программист | **Время:** 40 минут

---

## 🎯 Миссия

Улучши ASCII генератор из Недели 1 через полный цикл: спеки с критериями приёмки → делегирование → diff review → тесты.

**Формат артефакта:** обновлённый проект + файл тестов + отчёт агента (JSON) по ревью + вывод `pytest` (зелёный).

---

## 📋 Задачи (каждая — отдельная итерация)

### 1. Ревью текущего кода (структурированный отчёт)

```markdown
Проанализируй ascii_gen.py и верни ответ строго в JSON:

{"issues": [{"line": 0, "severity": "high|medium|low",
             "problem": "...", "fix": "..."}],
 "summary": "..."}

Категории: security, обработка ошибок, тестируемость, дублирование.
Без правок кода — только отчёт.
```

Из отчёта выбери 2-3 пункта с severity high/medium — это будут следующие спеки.

### 2. Рефакторинг по спеке (CoT + diff review)

```markdown
Отрефактори ascii_gen.py: функции валидации, генерации и истории — раздельно,
без изменения поведения.

Сначала план: какие функции, порядок шагов, как убедиться, что поведение не изменилось.
После подтверждения — дифф.

Готово, когда: скрипт работает как раньше (прогони 3 сценария из Недели 1),
глобального состояния стало меньше.
```

### 3. Тесты через Few-shot

```python
Вот стиль тестов в проекте:

import pytest

from ascii_gen import validate_name

def test_validate_name_accepts_alnum():
    assert validate_name("Ada42") is True

def test_validate_name_rejects_empty():
    assert validate_name("") is False

Напиши тесты для generate() и save_history():
- нормальное имя, пустое имя, имя из символов
- история: пустая, 10+ записей (хранить только последние 10)

Готово, когда: pytest проходит, покрытие основной логики есть.
```

### 4. Улучшение (по отчёту из задачи 1)

Возьми один high-пункт отчёта и оформи спекой: задача, требования, «готово, когда», формат (дифф + тесты).

---

## 🛠️ Ориентир: как может выглядеть итог

Не копируй вручную — добейся похожей структуры через агента, ревьюя каждый дифф.

```python
from art import tprint, FONT_NAMES
from colorama import init, Fore
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import sys

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

## ✅ Верификация

```bash
pytest -v          # все тесты зелёные
python ascii_gen.py # три сценария из Недели 1: имя, пустая строка, Ctrl+C
```

| Метрика | Было | Стало |
|---------|------|-------|
| Type hints | ❌ | ✅ |
| Тесты | ❌ | ✅ pytest |
| Глобальное состояние | Script | Класс с изоляцией |
| Структурированный отчёт о проблемах | ❌ | ✅ JSON |

---

## ✅ Checklist недели 2

- [ ] Освоил P.T.C.F. как спецификацию с критериями приёмки
- [ ] Понял Zero-shot vs Few-shot, получил структурированный JSON-отчёт
- [ ] Научился применять CoT: план до кода
- [ ] Освоил debug-цикл с воспроизводящим тестом
- [ ] Улучшил проект через спеки, diff review и тесты

---

## 🧠 Итоги

| Навык | Применение |
|-------|------------|
| Спека с критериями приёмки | «Готово» — это тест, а не мнение |
| Структурированный вывод | Отчёты агента скармливаются чек-листам и скриптам |
| CoT: план до кода | Ошибка в плане дешевле ошибки в диффе |
| Diff review + тесты | Агент производит диффы, не истину — проверяй каждый |

---

📚 [На предыдущий день ←](./Day_4.md)
