# AI Agent Development Scripts

This directory contains utility scripts to streamline Git workflow and prevent merge conflicts during AI agent development sessions.

## 🚀 Quick Start

```bash
# First time setup
./scripts/setup-git-config.sh

# Start each session with
./scripts/session-start.sh

# End each session with
./scripts/session-end.sh

# Use for safe pushes
./scripts/sync-and-push.sh
```

## 📋 Available Scripts

### `setup-git-config.sh`
**Purpose**: Configure Git with optimal settings for AI agent development

**Features**:
- Sets appropriate editor (VS Code > Vim > nano)
- Configures merge tools for conflict resolution
- Enables rerere for conflict resolution reuse
- Sets pull strategy to rebase
- Adds helpful Git aliases
- Optimizes diff and merge settings

**Usage**: Run once per environment
```bash
./scripts/setup-git-config.sh
```

### `session-start.sh`
**Purpose**: Repository health check and session initialization

**Features**:
- Displays current repository status
- Checks for remote changes
- Identifies uncommitted changes
- Shows recent activity
- Provides recommendations for safe workflow

**Usage**: Run at the beginning of each session
```bash
./scripts/session-start.sh
```

### `session-end.sh`
**Purpose**: Session cleanup and documentation

**Features**:
- Prompts to commit uncommitted changes
- Offers to push unpushed commits
- Updates session documentation
- Creates session summary
- Provides next session setup instructions

**Usage**: Run at the end of each session
```bash
./scripts/session-end.sh
```

### `sync-and-push.sh`
**Purpose**: Safe push with automatic conflict prevention

**Features**:
- Fetches latest remote changes
- Checks for conflicts before pushing
- Automatically rebases on remote changes
- Provides clear error messages
- Prevents force pushes and data loss

**Usage**: Use instead of `git push`
```bash
./scripts/sync-and-push.sh
```

## 🔧 Git Aliases Added

After running `setup-git-config.sh`, these aliases are available:

| Alias | Command | Description |
|-------|---------|-------------|
| `git st` | `git status` | Quick status check |
| `git co` | `git checkout` | Switch branches |
| `git br` | `git branch` | List/manage branches |
| `git ci` | `git commit` | Commit changes |
| `git unstage` | `git reset HEAD --` | Unstage files |
| `git last` | `git log -1 HEAD` | Show last commit |
| `git sync` | `git fetch origin && git rebase origin/main` | Sync with remote |
| `git safepush` | `bash scripts/sync-and-push.sh` | Safe push |

## 🛡️ Conflict Prevention Strategy

### The Problem
AI agent sessions often result in merge conflicts due to:
- Multiple concurrent sessions
- Large documentation updates
- Divergent repository states
- Complex rebase operations

### The Solution
1. **Always sync before starting work** (`session-start.sh`)
2. **Use safe push operations** (`sync-and-push.sh`)
3. **Maintain clean session boundaries** (`session-end.sh`)
4. **Optimize Git configuration** (`setup-git-config.sh`)

### Workflow Example
```bash
# Session start
./scripts/session-start.sh

# Do your work...
git add .
git commit -m "feat: implement new feature"

# Safe push
./scripts/sync-and-push.sh

# Session end
./scripts/session-end.sh
```

## 🚨 Emergency Procedures

If conflicts still occur:

```bash
# Option 1: Abort and restart
git rebase --abort
git reset --hard origin/main
# Re-apply changes manually

# Option 2: Use merge instead of rebase
git merge origin/main
# Resolve conflicts in merge commit

# Option 3: Create feature branch
git checkout -b fix/merge-conflicts
git push origin fix/merge-conflicts
# Create PR for manual review
```

## 📊 Success Metrics

These scripts aim to achieve:
- **Zero conflict sessions**: No merge conflicts during normal workflow
- **Faster operations**: Reduced time spent on Git operations
- **Clean history**: Linear, readable commit history
- **Better documentation**: Automatic session tracking and documentation

## 🔍 Troubleshooting

### Script Permission Issues
```bash
chmod +x scripts/*.sh
```

### Git Configuration Issues
```bash
git config --list | grep -E "(editor|merge|pull|push)"
```

### Repository State Issues
```bash
git status
git log --oneline -5
git remote -v
```

## 📚 Additional Resources

- [Git Best Practices](../manus/session_artifacts/git_workflow_best_practices.md)
- [Session Migration Guide](../manus/Agents.md)
- [Repository Documentation](../README.md)

---

**Remember**: Prevention is better than resolution. Use these scripts consistently to maintain a smooth development workflow.
