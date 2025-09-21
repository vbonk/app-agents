#!/bin/bash

# sync-and-push.sh
# Safe git push script that prevents merge conflicts

set -e  # Exit on any error

echo "🔄 Starting safe push process..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo "Please commit or stash your changes first:"
    git status --porcelain
    exit 1
fi

# Fetch latest changes from remote
echo "📥 Fetching latest changes from remote..."
git fetch origin

# Check if we're behind remote
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
if [ "$BEHIND" -gt 0 ]; then
    echo "📊 Repository is $BEHIND commits behind origin/main"
    echo "Recent commits on remote:"
    git log --oneline HEAD..origin/main
    echo ""
    
    # Attempt to rebase
    echo "🔄 Rebasing on origin/main..."
    if git rebase origin/main; then
        echo "✅ Rebase successful"
    else
        echo "❌ Rebase failed due to conflicts"
        echo "Please resolve conflicts manually and run:"
        echo "  git rebase --continue"
        echo "  git push origin main"
        exit 1
    fi
fi

# Check if we have commits to push
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
if [ "$AHEAD" -eq 0 ]; then
    echo "ℹ️  No new commits to push"
    exit 0
fi

echo "📤 Pushing $AHEAD commits to origin/main..."
if git push origin main; then
    echo "✅ Successfully pushed to remote repository"
    echo "🎉 All done!"
else
    echo "❌ Push failed"
    exit 1
fi
