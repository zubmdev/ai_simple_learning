# День 4: Open Source Contribution Workflow 🌟

**Трек:** 👨‍💻 Программист | **Время:** 40 минут

---

## 🎯 Цель дня

Сделать meaningful contribution в Open Source проект через GitHub.

---

## Finding the Right Project

### Criteria:

```
✅ Active (commits in last month)
✅ Good documentation (CONTRIBUTING.md)
✅ Welcoming community (good first issue labels)
✅ Tech stack matches your skills
✅ Interesting to you personally

Use:
- github.com/explore
- goodfirstissue.dev
- up-for-grabs.net
```

---

## Contribution Types

### Good for First Contributors:

```
1. Bug Fixes
   - Small, isolated issues
   - Clear reproduction steps
   - Testable

2. Documentation
   - README improvements
   - API documentation
   - Example additions
   - Typo fixes

3. Tests
   - Increase coverage
   - Edge case testing
   - Integration tests

4. Features (small)
   - New configuration option
   - Additional output format
   - Minor enhancement
```

---

## Workflow

### Step 1: Fork & Clone

```bash
# Fork on GitHub UI
# Clone your fork
git clone https://github.com/YOUR_USERNAME/project.git
cd project

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL/project.git
```

### Step 2: Create Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### Step 3: Make Changes

```
Промпт:

Working on issue: [link]

@Codebase

Help me:
1. Understand the codebase structure
2. Identify files to modify
3. Implement the fix/feature
4. Ensure backward compatibility
5. Add/update tests

Constraints:
- Follow project conventions
- Maintain test coverage
- Update documentation
```

### Step 4: Test

```bash
# Run project tests
npm test
# or
yarn test

# Add tests for your changes
# Ensure all tests pass
```

### Step 5: Commit

```bash
git add .
git commit -m "feat: add [feature description]

- Implementation details
- Why this approach
- Testing approach

Fixes #[issue-number]"
```

### Step 6: Push & PR

```bash
git push origin feature/your-feature-name

# Create PR on GitHub
# Fill PR template
```

---

## PR Template

```markdown
## Description
[What does this PR do?]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated

## Screenshots (if applicable)

## Related Issues
Fixes #[issue]
```

---

## Best Practices

### Communication:

```
✅ Comment on issue before starting
✅ Ask clarifying questions
✅ Update on progress
✅ Be responsive to feedback
✅ Thank reviewers
```

### Code Quality:

```
✅ Follow project style guide
✅ Write self-documenting code
✅ Add inline comments for complex logic
✅ Update documentation
✅ Add/update tests
```

### Git Hygiene:

```
✅ Atomic commits (one logical change)
✅ Clear commit messages
✅ Rebase on upstream before PR
✅ Keep PR focused
✅ Resolve conflicts promptly
```

---

## Handling Feedback

### When Changes Requested:

```
1. Don't take it personally
2. Understand the concern
3. Ask for clarification if needed
4. Make requested changes
5. Respond to each comment
6. Push updates
```

### Example Response:

```
@reviewer Thanks for the feedback!

You're right, this approach is better.
I've updated the code as suggested.

Changes:
- [specific change 1]
- [specific change 2]

Let me know if further adjustments needed.
```

---

## Checklist дня ✅

- [ ] Found suitable project
- [ ] Identified issue to work on
- [ ] Forked and cloned repo
- [ ] Made changes
- [ ] Tests pass
- [ ] Created PR
- [ ] Waiting for review

---

📚 [На следующий день →](./Day_5.md)
