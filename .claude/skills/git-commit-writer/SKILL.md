---
name: git-commit-writer
description: Writes clear, conventional commit messages following best practices
---

## Commit Message Format

**Structure:**
```
<type>: <subject line (50-72 chars)>

[optional body: explain WHY, not what - the diff shows what changed]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Type prefixes:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code change that neither fixes a bug nor adds a feature
- `test:` Adding or updating tests
- `chore:` Maintenance (dependencies, config, build)

**Guidelines:**
1. **Subject line** - Imperative mood ("Add feature" not "Added feature"), no period, 50-72 chars
2. **Focus on WHY** - Body explains motivation and context, not implementation details
3. **Match repo style** - Review recent commits with `git log --oneline -10` first
4. **Be specific** - "Fix login timeout on slow connections" not "Fix bug"
5. **One logical change** - If you need "and" in the subject, split into multiple commits

**Examples:**
```
feat: Add user session timeout after 30min inactivity

Prevents security risk from unattended sessions. Configurable via
SESSION_TIMEOUT_MINUTES env variable.
```

```
fix: Resolve race condition in async file upload

Upload completion wasn't awaited before rendering success message,
causing intermittent failures on slow networks.
```