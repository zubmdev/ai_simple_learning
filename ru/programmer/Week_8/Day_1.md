# День 1: Project Ideation & Scope Definition 💡

**Трек:** 👨‍💻 Программист | **Время:** 30 минут

---

## 🎯 Цель дня

Определить финальный проект с чётким scope и realist timeline.

---

## Project Selection Framework

### Критерии:

```
1. Technical Challenge (умеренная сложность)
2. Practical Utility (реальная польза)
3. Showcase Potential (демонстрация навыков)
4. Completion Feasibility (завершимость за неделю)
5. Learning Opportunity (новые технологии/паттерны)
```

---

## Project Ideas

### Tier 1: CLI Tools

```
1. Task Automation CLI
   - File organization
   - API scaffolding
   - Git workflow automation

2. Data Processing Pipeline
   - CSV/JSON transformation
   - API data aggregation
   - Report generation

3. Development Utilities
   - Environment setup
   - Dependency analyzer
   - Code metrics
```

### Tier 2: API/Backend Services

```
1. REST API with Auth
   - User management
   - CRUD operations
   - JWT authentication
   - Rate limiting

2. GraphQL API
   - Schema design
   - Resolvers
   - Subscriptions
   - DataLoader optimization

3. Microservice
   - Service mesh
   - Event-driven
   - Circuit breaker
   - Health monitoring
```

### Tier 3: Full-Stack Applications

```
1. Dashboard/Analytics
   - Data visualization
   - Real-time updates
   - Export functionality

2. Automation Platform
   - Webhooks
   - Scheduled jobs
   - Integrations

3. Developer Tool
   - Code playground
   - Documentation generator
   - API tester
```

---

## Scope Definition

### MVP Framework:

```markdown
## Project Vision
One sentence: [что делает приложение]

## Core Value Proposition
[какую проблему решает]

## MVP Features (3-5)
1. [Must-have feature 1]
2. [Must-have feature 2]
3. [Must-have feature 3]

## Non-Goals (explicitly NOT doing)
- [Feature to exclude]
- [Feature to exclude]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Timeline
- Day 1: Setup & Architecture
- Day 2: Core features
- Day 3: Integration & Polish
- Day 4: Testing & Documentation
- Day 5: Deployment & Portfolio
```

---

## Technical Stack Selection

### Decision Matrix:

| Component | Option A | Option B | Choice |
|-----------|----------|----------|--------|
| Language | TypeScript | Python | |
| Runtime | Node.js | Deno | |
| Framework | Express | Fastify | |
| Database | PostgreSQL | MongoDB | |
| Auth | JWT | OAuth | |
| Testing | Jest | Vitest | |
| Deployment | Docker | Serverless | |

### Промпт:

```
I'm building [project description].

Recommend optimal stack:

Requirements:
- [requirement 1]
- [requirement 2]

Constraints:
- [constraint 1]
- [constraint 2]

Provide:
1. Technology recommendations
2. Justification for each choice
3. Trade-offs
4. Alternative options
```

---

## Architecture Planning

### High-Level Architecture:

```
Промпт:

Design architecture for [project]:

Requirements:
- Scalability: [requirements]
- Performance: [requirements]
- Security: [requirements]

Create:
1. Component diagram
2. Data flow diagram
3. API contract
4. Database schema
5. Deployment architecture

Use: C4 Model or similar
```

---

## Risk Assessment

### Identify Risks:

```markdown
## Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 2] | | | |

## Timeline Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | High | High | Strict MVP definition |
| Integration issues | Med | Med | Early integration testing |

## Resource Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API limitations | Med | Med | Fallback/alternatives |
| Performance issues | Low | High | Profiling early |
```

---

## Definition of Done

```markdown
## Feature Complete
- [ ] All MVP features implemented
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated

## Quality Gates
- [ ] Test coverage > 80%
- [ ] No critical security vulnerabilities
- [ ] Performance benchmarks met
- [ ] Accessibility requirements met

## Deployment
- [ ] CI/CD pipeline configured
- [ ] Production environment ready
- [ ] Monitoring/alerting configured
- [ ] Rollback strategy defined

## Documentation
- [ ] README complete
- [ ] API documentation
- [ ] Architecture diagrams
- [ ] Deployment guide
```

---

## Practice

### Задание:

```
1. Выбери проект (из Tier 1-3)
2. Определи MVP scope (3-5 features)
3. Выбери technical stack
4. Спроектируй architecture
5. Оцени risks
6. Создай Definition of Done

Сохранить в: PROJECT_CHARTER.md
```

---

## Checklist дня ✅

- [ ] Выбрал проект
- [ ] Определил MVP scope
- [ ] Выбрал stack
- [ ] Спроектировал architecture
- [ ] Оценил risks
- [ ] Создал DoD

---

## 🎯 Миссия

Выбери финальный проект и напиши `PROJECT_CHARTER.md` по шаблону из урока: одно предложение о проекте, 3–5 MVP-фич, явные non-goals и измеримые критерии успеха.

**Готово, когда:** файл лежит в корне репозитория проекта, в non-goals минимум два пункта, каждый критерий успеха проверяется командой или числом, а стек-матрица заполнена с обоснованием выбора.

---

📚 [На следующий день →](./Day_2.md)
