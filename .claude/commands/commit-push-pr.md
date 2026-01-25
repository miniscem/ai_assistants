# Commit, Push, and Create PR

Perform a complete git workflow: stage changes, commit, push, and create a pull request.

## Flags

Parse the arguments for these flags FIRST before executing:

| Flag | Effect |
|------|--------|
| `--local` | Commit only, skip push and PR |
| `--no-pr` | Commit and push, skip PR creation |
| (default) | Full workflow: commit, push, and create PR |

Any text that is not a flag should be used as context for the commit message.

Examples:
- `/commit-push-pr --local` - commit only
- `/commit-push-pr --local fix auth bug` - commit only, use "fix auth bug" for message
- `/commit-push-pr --no-pr` - commit and push, no PR
- `/commit-push-pr` - full workflow

## Instructions

1. **Analyze Changes**: Run these commands in parallel to understand the current state:
   - `git status` to see all modified and untracked files
   - `git diff` to see unstaged changes
   - `git diff --staged` to see already staged changes
   - `git log --oneline -5` to see recent commit message style
   - `git branch --show-current` to get current branch name

2. **Verify Branch**:
   - If on `main` or `master`, ask the user if they want to create a new branch first
   - Check if the branch exists on remote with `git ls-remote --heads origin <branch>`

3. **Stage Changes**:
   - Review all changes and stage appropriate files with `git add`
   - Warn about and skip any files that might contain secrets (.env, credentials, keys)
   - If the user provided specific files as arguments, only stage those

4. **Create Commit**:
   - Draft a concise commit message that describes the "why" not just the "what"
   - Follow the repository's existing commit message style
   - Use this format for the commit:
   ```bash
   git commit -m "$(cat <<'EOF'
   <commit message here>

   Co-Authored-By: Claude
   EOF
   )"
   ```

5. **Push to Remote** (skip if `--local` flag):
   - Push with upstream tracking: `git push -u origin <branch>`
   - If push fails, diagnose the issue and suggest solutions

6. **Create Pull Request** (skip if `--local` or `--no-pr` flag):
   - Use `gh pr create` with a well-structured body:
   ```bash
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   ## Summary
   <2-3 bullet points describing the changes>

   ## Changes
   <list of key files/components modified>

   ## Test Plan
   - [ ] <testing checklist items>

   🤖 Generated with [Claude Code](https://claude.ai/code)
   EOF
   )"
   ```

7. **Report Results**:
   - Summarize what was done based on flags used:
     - `--local`: "Committed locally. Run `/commit-push-pr` to push and create PR."
     - `--no-pr`: "Committed and pushed. Run `gh pr create` to create PR."
     - default: Display the PR URL

## Safety

- Never force push unless explicitly requested
- Never commit files matching: `.env*`, `*credentials*`, `*secret*`, `*.pem`, `*.key`
- Always verify with the user before committing if there are many untracked files
