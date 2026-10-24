# День 2: Project Scaffolding Automation ⚡

**Трек:** 👨‍💻 Программист | **Время:** 35 минут

---

## 🎯 Цель дня

Автоматизировать создание структуры проекта через AI-генерацию.

---

## Smart Scaffolding

### Промпт для генерации структуры:

```
@Files: (пусто, новый проект)

Создай структуру проекта [название] согласно архитектуре:

Требования:
- TypeScript strict mode
- ESLint + Prettier
- Jest для тестов
- Docker + docker-compose
- Makefile для команд
- GitHub Actions CI/CD

Создай:
1. Все файлы с базовым содержимым
2. package.json с нужными зависимостями
3. Конфигурации (tsconfig, eslint, jest)
4. Dockerfile и docker-compose.yml
5. README.md с инструкциями
6. .gitignore
7. Makefile

Для каждого файла объясни назначение.
```

---

## Практический пример

### Создание Node.js API проекта:

```
Создай структуру для Node.js REST API:

Стек: Express + TypeScript + PostgreSQL + Prisma

Сгенерируй:
1. src/index.ts (entry point)
2. src/app.ts (Express app)
3. src/config/ (env variables)
4. prisma/schema.prisma (DB schema)
5. tests/setup.ts (Jest config)
6. .env.example
7. Docker setup

Используй best practices для каждого файла.
```

### Пример сгенерированных файлов:

**package.json:**

```json
{
  "name": "api-project",
  "version": "1.0.0",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint src/**/*.ts",
    "format": "prettier --write src/**/*.ts",
    "db:migrate": "prisma migrate dev",
    "db:generate": "prisma generate"
  },
  "dependencies": {
    "express": "^4.18.2",
    "@prisma/client": "^5.0.0",
    "dotenv": "^16.3.1",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.17",
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "tsx": "^3.12.0",
    "prisma": "^5.0.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0",
    "ts-jest": "^29.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

**tsconfig.json:**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Dockerfile:**

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --production

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

---

## Автоматизация через Makefile

### Генерация Makefile:

```
Создай Makefile с командами:
- make install (установить зависимости)
- make dev (запуск в dev режиме)
- make build (сборка)
- make test (тесты)
- make lint (линтинг)
- make docker-build (сборка docker)
- make docker-up (запуск docker)
- make clean (очистка)
```

Пример:

```makefile
.PHONY: install dev build test lint docker-build docker-up clean

install:
	npm install

dev:
	npm run dev

build:
	npm run build

test:
	npm test

lint:
	npm run lint

docker-build:
	docker build -t api-project .

docker-up:
	docker-compose up -d

clean:
	rm -rf dist node_modules
```

---

## CI/CD Pipeline

### Генерация GitHub Actions:

```
Создай .github/workflows/ci.yml:
- Run on push to main
- Node.js 20
- Install, lint, test, build
- Docker build test
```

Пример:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
      
      - name: Build
        run: npm run build
      
      - name: Build Docker image
        run: docker build -t api-project .
```

---

## Template Reuse

### Создай свой шаблон:

```bash
# После создания идеального проекта
mkdir ~/.project-templates/node-api
cp -r ./template-files ~/.project-templates/node-api/
```

### Скрипт для инициализации:

```bash
#!/bin/bash
# init-project.sh

PROJECT_NAME=$1
TEMPLATE_DIR=~/.project-templates/node-api

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: ./init-project.sh <project-name>"
  exit 1
fi

mkdir $PROJECT_NAME
cp -r $TEMPLATE_DIR/* $PROJECT_NAME/
cd $PROJECT_NAME

# Replace placeholder
find . -type f -exec sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" {} +

echo "Project $PROJECT_NAME created!"
```

---

## Практика

### Задание:

```
1. Выбери тип проекта
2. Сгенерируй scaffolding через AI
3. Настрой все конфигурации
4. Протестируй: make install && make dev
5. Зафиксируй как template
```

---

## Checklist дня ✅

- [ ] Сгенерировал полную структуру проекта
- [ ] Создал все конфигурационные файлы
- [ ] Настроил Docker
- [ ] Создал Makefile
- [ ] Настроил CI/CD
- [ ] Протестировал сборку

---

📚 [На следующий день →](./Day_3.md)
