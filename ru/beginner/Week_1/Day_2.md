# День 2: Установка базы (VS Code + Continue.dev) 🛠️

Сегодня мы установим все необходимые инструменты. Я проведу тебя через каждый шаг с картинками и командами для твоей операционной системы.

---

## 📋 Что мы установим сегодня

1. **VS Code** — редактор кода (твоя "кухня" для программирования)
2. **Continue.dev** — ИИ-ассистент внутри VS Code

**Общее время установки:** 15-20 минут

---

## Часть 1: Установка VS Code

### Что такое VS Code?

VS Code (Visual Studio Code) — это бесплатный редактор кода от Microsoft. Представь его как Word, но для программ.

**Почему VS Code?**
- ✅ Бесплатный навсегда
- ✅ Работает на Windows, macOS, Linux
- ✅ Огромное количество расширений
- ✅ Активно развивается (обновления каждый месяц)
- ✅ Используется миллионами разработчиков

---

### 🪟 Установка на Windows

[официальная документация(установка для windows):](https://code.visualstudio.com/docs/setup/windows)

[установка с изображениями:](https://neu-se.github.io/CS4530-Spring-2025/tutorials/week1-getting-started#installing-visual-studio-code-vscode)

#### Шаг 1: Скачай установщик

1. Открой браузер (Chrome, Firefox, Edge — любой)
2. Перейди по ссылке: **https://code.visualstudio.com**
3. Нажми кнопку **"Download for Windows"**


**Скриншот: Главная страница VS Code с кнопкой загрузки** : 
[изображение](./images/vscode.png)

#### Шаг 2: Запусти установщик

1. Найди скачанный файл `VSCodeUserSetup-x64-1.xx.x.exe` в папке **Загрузки**
2. Двойной клик для запуска
3. Если появилось окно "User Account Control" — нажми **"Да"**


#### Шаг 3: Пройди установку

**Окно 1 — License Agreement:**
- Прочитай лицензию (или не читай, кто мы такие, чтобы судить 😄)
- Нажми **"I accept the agreement"**
- Нажми **"Next"**

**Окно 2 — Destination Location:**
- Оставь путь по умолчанию: `C:\Users\[твоё_имя]\AppData\Local\Programs\Microsoft VS Code`
- Нажми **"Next"**

**Окно 3 — Select Start Menu Folder:**
- Оставь как есть
- Нажми **"Next"**

**Окно 4 — Select Additional Tasks:**
**ВАЖНО!** Отметь галочками:
- ☑️ **Create a desktop icon** (создать ярлык на рабочем столе)
- ☑️ **Add "Open with Code" action to Windows Explorer file context menu** (добавить в контекстное меню)
- ☑️ **Add "Open with Code" action to Windows Explorer directory context menu** (добавить в контекстное меню папок)
- ☑️ **Register Code as an editor for supported file types** (сделать VS Code редактором по умолчанию)
- ☑️ **Add to PATH** (очень важно для работы из командной строки)


Нажми **"Next"**, затем **"Install"**

#### Шаг 4: Завершение

- Дождись завершения установки (1-2 минуты)
- Отметь **"Launch Visual Studio Code"**
- Нажми **"Finish"**


**✅ VS Code установлен!**

---

### 🍎 Установка на macOS

[официальная документация(установка для macOS):](https://code.visualstudio.com/docs/setup/mac)

[установка с изображениями:](https://neu-se.github.io/CS4530-Spring-2025/tutorials/week1-getting-started#installation-steps-windows--mac)

#### Шаг 1: Скачай приложение

1. Открой браузер (Safari, Chrome — любой)
2. Перейди по ссылке: **https://code.visualstudio.com**
3. Нажми кнопку **"Download for macOS"**

**Выбери правильную версию:**
- **Intel Mac** (процессоры Intel Core) → выбирай "Intel chip"
- **Apple Silicon Mac** (M1, M2, M3, M4) → выбирай "Apple Silicon"

**Как узнать свой процессор?**
1. Нажми на яблоко в левом верхнем углу
2. Выбери **"About This Mac"**
3. Смотри строку **"Chip"**:
   - Если написано "Apple M1/M2/M3/M4" → Apple Silicon
   - Если написано "Intel" → Intel chip


#### Шаг 2: Открой DMG файл

1. Найди скачанный файл `VSCode-darwin-universal.zip` или `.dmg` в папке **Downloads**
2. Двойной клик для открытия
3. Появится окно с иконкой VS Code


#### Шаг 3: Установи приложение

1. Перетащи иконку **Visual Studio Code** в папку **Applications**


2. Дождись копирования (30-60 секунд)

#### Шаг 4: Первый запуск

1. Открой **Launchpad** или найди VS Code в **Applications**
2. Двойной клик на **Visual Studio Code**

**Если появилось предупреждение:**
```
"Visual Studio Code" is an app downloaded from the Internet. Are you sure you want to open it?
```
Нажми **"Open"**


**Если появилось предупреждение о неподписанном разработчике:**
1. Открой **System Settings** → **Privacy & Security**
2. Найди сообщение о VS Code
3. Нажми **"Open Anyway"**

**✅ VS Code установлен!**

#### Дополнительный шаг: Добавить VS Code в PATH (macOS)

Чтобы запускать VS Code из терминала:

1. Открой VS Code
2. Нажми `Cmd + Shift + P` (откроется Command Palette)
3. Введи: `shell command`
4. Нажми **"Shell Command: Install 'code' command in PATH"**
5. Увидишь сообщение "Successfully installed 'code' command in PATH"


---

### 🐧 Установка на Linux

[официальная документация(установка для macOS):](https://code.visualstudio.com/docs/setup/linux)

[установка с cli:](https://neu-se.github.io/CS4530-Spring-2025/tutorials/week1-getting-started#installation-linux)

#### Вариант 1: Ubuntu/Debian (рекомендуется)

**Открой Terminal** (`Ctrl + Alt + T`)

**Введи следующие команды по одной:**

```bash
# 1. Обнови список пакетов
sudo apt update

# 2. Установи необходимые зависимости
sudo apt install -y wget gpg

# 3. Добавь ключ Microsoft GPG
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg

# 4. Добавь репозиторий VS Code
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null

# 5. Обнови список пакетов с новым репозиторием
sudo apt update

# 6. Установи VS Code
sudo apt install -y code
```

**Пояснение команд:**
- `sudo` — запуск от имени администратора (введи свой пароль)
- `apt update` — обновить список доступных программ
- `apt install` — установить программу


**✅ VS Code установлен!**

#### Вариант 2: Fedora/RHEL/CentOS

```bash
# 1. Импортируй ключ Microsoft
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

# 2. Добавь репозиторий
echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

# 3. Установи VS Code
sudo dnf install -y code
```

#### Вариант 3: Arch Linux

```bash
# Установи через AUR (нужен yay или другой AUR helper)
yay -S visual-studio-code-bin
```

#### Вариант 4: Flatpak (универсальный)

```bash
# Установи через Flatpak (работает на всех дистрибутивах)
flatpak install flathub com.visualstudio.code
```

#### Вариант 5: Snap (Ubuntu и другие)

```bash
# Установи через Snap
sudo snap install code --classic
```

---

## Часть 2: Первый запуск VS Code

### Открой VS Code

**Windows:**
- Двойной клик по ярлыку на рабочем столе
- Или: Пуск → Visual Studio Code

**macOS:**
- Launchpad → Visual Studio Code
- Или: Applications → Visual Studio Code

**Linux:**
- Найди "Visual Studio Code" в меню приложений
- Или введи `code` в терминале

### Начальный экран


**Разберём интерфейс:**

1. **Слева — Activity Bar:**
   - 📁 Explorer (проводник файлов)
   - 🔍 Search (поиск по файлам)
   - 🔄 Source Control (Git)
   - 🐛 Run and Debug (отладка)
   - 🧩 Extensions (расширения)

2. **Сверху — Menu Bar:**
   - File, Edit, Selection, View, Go, Run, Terminal, Help

3. **По центру — Editor:**
   - Здесь будет твой код

4. **Снизу — Status Bar:**
   - Информация о текущем файле, ветке Git и т.д.

---

## Часть 3: Установка Continue.dev

### Что такое Continue.dev?

**Continue.dev** — это Open Source расширение для VS Code, которое добавляет ИИ-ассистента прямо в твой редактор.

**Почему Continue.dev?**

| Критерий | Continue.dev | Cursor | GitHub Copilot |
|----------|--------------|--------|----------------|
| **Цена** | 🆓 Бесплатный | 💰 $20/мес | 💰 $10/мес |
| **Open Source** | ✅ Да | ❌ Нет | ❌ Нет |
| **Приватность** | 🔒 Полный контроль | ⚠️ Через их серверы | ⚠️ Через GitHub |
| **Гибкость** | ⚙️ Любые модели | 🔒 Только их модели | 🔒 Только OpenAI |
| **Оффлайн** | ✅ Да (с Ollama) | ❌ Нет | ❌ Нет |

**Continue.dev = Cursor + Copilot, но бесплатно и с приватностью!**

---

### Установка Continue.dev (все ОС)

#### Шаг 1: Открой Extensions

**Способ 1 (горячие клавиши):**
- Windows/Linux: `Ctrl + Shift + X`
- macOS: `Cmd + Shift + X`

**Способ 2 (через меню):**
1. Нажми на иконку квадратов слева (Extensions) - [изображение](./images/extention.png)
2. Или: View → Extensions


#### Шаг 2: Найди Continue

1. В поле поиска введи: `Continue` -- [изображение](./images/find-continue.png)
2. Найди расширение **"Continue — VS Code Extensions"** от **Continue Dev**
3. Автор: **continuedev**


**Как узнать, что это правильное расширение:**
- ✅ Название: "Continue"
- ✅ Автор: "Continue"
- ✅ Количество установок: 2.2M+
- ✅ Рейтинг: 3.5+ звёзд

#### Шаг 3: Установи расширение

1. Нажми кнопку **"Install"** : [изображение](./images/install.png)
2. Дождись установки (10-30 секунд)
3. Кнопка изменится на **"Disable"** или **"Uninstall"** — это значит, что установлено


#### Шаг 4: Открой Continue

**Способ 1:**
- Найди иконку Continue слева в Activity Bar ([изображение](./images/continue-icon.png))

**Способ 2 (горячие клавиши):**
- Windows/Linux: `Ctrl + L`
- macOS: `Cmd + L`

**Способ 3:**
- Нажми `Ctrl + Shift + P` (или `Cmd + Shift + P` на Mac)
- Введи: `Continue: Open` : [изображение](./images/continue-opened.png)
- Нажми Enter


---

## Часть 4: Настройка Continue.dev (базовая)

### Первый запуск

При первом открытии Continue увидишь экран приветствия:

![Continue welcome screen]

**Выбери: "I'll set it up myself"** или **"Manual Setup"**

### Интерфейс Continue


**Панель Continue состоит из:**
1. **Чат** — место для общения с ИИ
2. **Поле ввода** — куда пишешь промпты
3. **Модель** — какой ИИ используется (настроим завтра)
4. **Контекст** — какие файлы "видит" ИИ
5. **Модификация** - режим работы модели

[Панель Continue(изображение)](./images/continue-sections.png)

---

## Проверка установки ✅

### Тест 1: VS Code работает

1. Создай новый файл: `File → New File` или `Ctrl + N`
2. Сохрани: `File → Save` или `Ctrl + S`
3. Назови файл: `test.txt`
4. Напиши что-нибудь: "Hello, VS Code!"
5. Сохрани: `Ctrl + S`

**✅ Если файл сохранился — VS Code работает!**

### Тест 2: Continue установлен

1. Нажми `Ctrl + L` (или `Cmd + L` на Mac)
2. Должна открыться панель Continue справа
3. Попробуй написать: "Привет!"

**⚠️ Важно:** ИИ пока не ответит, потому что мы не подключили модель. Это мы сделаем завтра!

**✅ Если панель открылась — Continue установлен!**

---

## Частые проблемы и решения

### ❌ Проблема 1: "VS Code не открывается"

**Windows:**
- Попробуй запустить от имени администратора (правый клик → "Run as administrator")
- Проверь, не заблокирован ли файл антивирусом

**macOS:**
- Если пишет "app is damaged", открой Terminal и введи:
  ```bash
  xattr -cr /Applications/Visual\ Studio\ Code.app
  ```

**Linux:**
- Попробуй запустить из терминала: `code`
- Смотри ошибки в выводе

### ❌ Проблема 2: "Не могу найти Continue в Extensions"

- Проверь интернет-соединение
- Попробуй перезапустить VS Code
- Попробуй установить напрямую:
  - Открой https://marketplace.visualstudio.com/items?itemName=Continue.continue
  - Нажми "Install"

### ❌ Проблема 3: "Continue не открывается"

- Перезапусти VS Code
- Проверь, что расширение включено: Extensions → Continue → Enable
- Попробуй переустановить расширение

---

## Checklist дня ✅

- [ ] Скачал VS Code
- [ ] Установил VS Code с нужными галочками (Windows)
- [ ] Запустил VS Code
- [ ] Открыл Extensions
- [ ] Нашёл и установил Continue.dev
- [ ] Открыл панель Continue (`Ctrl + L`)
- [ ] Создал тестовый файл

---

## Что дальше?

**Завтра (День 3):** Мы выберем и подключим "мозг" — ИИ-модель. Я покажу три пути:
1. CPU + Groq API (бесплатно, быстро, в облаке)
2. 4GB GPU + Ollama Qwen (локально, приватно)
3. 16GB GPU + Ollama Llama 3.1 (мощно, локально)

**Домашнее задание:**
- Поэкспериментируй с VS Code — открой разные меню, посмотри настройки
- Попробуй создать файл с расширением `.py` (Python) — VS Code предложит установить поддержку Python, согласись

---

📚 [На предыдущий день ←](./Day_1.md) | [На следующий день →](./Day_3.md)
