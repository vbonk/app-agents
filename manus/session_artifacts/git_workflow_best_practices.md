# Git Workflow Best Practices for AI Agent Sessions

## Problem Analysis: What Went Wrong

The recent push attempt resulted in complex merge conflicts and a lengthy resolution process due to:

1. **Divergent Repository State**: Remote had new commits we didn't have locally
2. **Concurrent Development**: Multiple sessions working on the same repository
3. **Large File Conflicts**: README.md had substantial changes on both sides
4. **Editor Issues**: Nano editor got stuck during rebase, requiring manual intervention
5. **No Sync Strategy**: No established protocol for handling repository synchronization

## Prevention Strategies

### 1. **Always Fetch Before Starting Work**

```bash
# At the beginning of every session
cd /path/to/repository
git fetch origin
git status
git log --oneline origin/main -5  # Check what's new on remote
```

**Implementation**: Add this as a standard session startup checklist.

### 2. **Use Feature Branches for Major Work**

Instead of working directly on `main`:

```bash
# Create feature branch for Constitution Service
git checkout -b feature/constitution-service
# Do all work on this branch
git add .
git commit -m "feat: implement Constitution Service"
# Push feature branch
git push origin feature/constitution-service
# Create PR for review and merge
```

**Benefits**:
- Isolates work from main branch changes
- Allows for clean PR-based merges
- Easier to handle conflicts in controlled environment

### 3. **Implement Sync-Before-Push Protocol**

```bash
# Before any push, always:
git fetch origin
git rebase origin/main  # or git merge origin/main
# Resolve any conflicts
git push origin main
```

**Automation**: Create a script for this:

```bash
#!/bin/bash
# sync-and-push.sh
echo "Fetching latest changes..."
git fetch origin
echo "Rebasing on origin/main..."
git rebase origin/main
if [ $? -eq 0 ]; then
    echo "Pushing to origin..."
    git push origin main
else
    echo "Conflicts detected. Please resolve manually."
    exit 1
fi
```

### 4. **Configure Git for Better Conflict Resolution**

```bash
# Set up better merge tools
git config --global merge.tool vimdiff
# Or use a GUI tool
git config --global merge.tool meld

# Configure editor to avoid nano issues
git config --global core.editor "code --wait"  # VS Code
# or
git config --global core.editor "vim"

# Enable rerere (reuse recorded resolution)
git config --global rerere.enabled true
```

### 5. **Use Atomic Commits and Smaller Changes**

Instead of large commits with many files:

```bash
# Commit service implementation separately from documentation
git add services/constitution-service/
git commit -m "feat: implement Constitution Service core functionality"

git add README.md
git commit -m "docs: update README with Constitution Service"

git add manus/
git commit -m "docs: add session migration artifacts"
```

### 6. **Implement Pre-Push Hooks**

Create `.git/hooks/pre-push`:

```bash
#!/bin/bash
# Check if we're ahead of remote
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u} 2>/dev/null)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "Warning: Local branch is not in sync with remote"
    echo "Run 'git fetch && git rebase origin/main' first"
    exit 1
fi
```

### 7. **Session Coordination Strategy**

For multi-session projects:

```bash
# At session start:
1. Check for session handoff notes in manus/
2. Fetch latest changes
3. Review recent commits
4. Create feature branch if major work planned

# At session end:
1. Commit all work
2. Update session handoff documentation
3. Push to feature branch or sync with main
4. Document any pending conflicts or issues
```

### 8. **Repository State Monitoring**

Add to session startup checklist:

```bash
# Check repository health
git status
git log --oneline -10
git remote -v
git branch -a
git fetch origin
git log --oneline origin/main -5
```

### 9. **Conflict Prevention Through Communication**

Create `manus/ACTIVE_SESSIONS.md`:

```markdown
# Active Sessions

## Current Session
- **Session ID**: constitution-service-implementation
- **Start Time**: 2025-09-21 05:00 EDT
- **Working On**: Constitution Service implementation
- **Files Modified**: services/, README.md, manus/
- **Expected End**: 2025-09-21 06:00 EDT

## Recent Sessions
- **Previous**: agent-enhancement-session (completed)
- **Files Modified**: agents/, docs/, shared/
```

### 10. **Automated Conflict Detection**

Create a pre-session script:

```bash
#!/bin/bash
# check-repo-status.sh

echo "=== Repository Status Check ==="
git fetch origin

# Check if we're behind
BEHIND=$(git rev-list --count HEAD..origin/main)
if [ $BEHIND -gt 0 ]; then
    echo "⚠️  Repository is $BEHIND commits behind origin/main"
    echo "Recent commits on remote:"
    git log --oneline HEAD..origin/main
    echo ""
    echo "Recommendation: Run 'git rebase origin/main' before starting work"
fi

# Check if we're ahead
AHEAD=$(git rev-list --count origin/main..HEAD)
if [ $AHEAD -gt 0 ]; then
    echo "⚠️  Repository is $AHEAD commits ahead of origin/main"
    echo "Unpushed commits:"
    git log --oneline origin/main..HEAD
    echo ""
    echo "Recommendation: Push changes before starting new work"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Uncommitted changes detected"
    git status --porcelain
fi

echo "=== End Status Check ==="
```

## Implementation Plan

### Immediate Actions

1. **Create Git Configuration Script**:
```bash
# setup-git-config.sh
git config --global core.editor "vim"
git config --global merge.tool vimdiff
git config --global rerere.enabled true
git config --global pull.rebase true
```

2. **Add Repository Scripts**:
- `scripts/sync-and-push.sh`
- `scripts/check-repo-status.sh`
- `scripts/session-start.sh`
- `scripts/session-end.sh`

3. **Update Session Protocols**:
- Add repository sync to session startup checklist
- Require feature branches for major implementations
- Implement session coordination documentation

### Long-term Improvements

1. **CI/CD Integration**: Set up GitHub Actions for automated conflict detection
2. **Branch Protection**: Require PR reviews for main branch changes
3. **Automated Testing**: Run tests before allowing merges
4. **Documentation Automation**: Auto-update documentation on merges

## Emergency Procedures

If conflicts occur despite prevention:

```bash
# Option 1: Abort and restart cleanly
git rebase --abort
git reset --hard origin/main
# Re-apply changes manually

# Option 2: Use merge instead of rebase
git merge origin/main
# Resolve conflicts in merge commit

# Option 3: Create new branch and PR
git checkout -b fix/merge-conflicts
git push origin fix/merge-conflicts
# Create PR for manual review
```

## Success Metrics

- **Zero conflict sessions**: Aim for sessions with no merge conflicts
- **Faster pushes**: Reduce time from commit to successful push
- **Clean history**: Maintain linear, readable git history
- **Session efficiency**: Reduce time spent on git operations vs. actual work

## Tools and Resources

### Recommended Git Tools
- **GUI**: GitKraken, SourceTree, or GitHub Desktop
- **CLI Enhancements**: `git-extras`, `hub`, `gh`
- **Diff Tools**: `meld`, `kdiff3`, or VS Code built-in

### Monitoring Commands
```bash
# Quick status check
alias gst="git status && git log --oneline -5"

# Sync check
alias gsync="git fetch origin && git log --oneline HEAD..origin/main"

# Safe push
alias gpush="git fetch origin && git rebase origin/main && git push origin main"
```

This comprehensive approach should eliminate the complex merge conflict scenarios we experienced and make git operations smooth and predictable.
