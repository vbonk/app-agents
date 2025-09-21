#!/bin/bash

# session-start.sh
# Repository health check and session initialization

echo "🚀 Starting AI Agent Session..."
echo "================================"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Display current repository info
echo "📍 Repository: $(basename $(git rev-parse --show-toplevel))"
echo "🌿 Current branch: $(git branch --show-current)"
echo "📊 Current commit: $(git rev-parse --short HEAD)"
echo ""

# Fetch latest changes
echo "📥 Fetching latest changes..."
git fetch origin

# Check repository status
echo "🔍 Repository Status Check:"
echo "================================"

# Check if we're behind
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
if [ "$BEHIND" -gt 0 ]; then
    echo "⚠️  Repository is $BEHIND commits behind origin/main"
    echo "Recent commits on remote:"
    git log --oneline HEAD..origin/main | head -5
    echo ""
    echo "💡 Recommendation: Run 'git rebase origin/main' before starting work"
    echo ""
fi

# Check if we're ahead
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
if [ "$AHEAD" -gt 0 ]; then
    echo "📤 Repository is $AHEAD commits ahead of origin/main"
    echo "Unpushed commits:"
    git log --oneline origin/main..HEAD
    echo ""
    echo "💡 Recommendation: Push changes using './scripts/sync-and-push.sh'"
    echo ""
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Uncommitted changes detected:"
    git status --porcelain
    echo ""
    echo "💡 Recommendation: Commit or stash changes before starting new work"
    echo ""
fi

# Check for untracked files
UNTRACKED=$(git ls-files --others --exclude-standard | wc -l)
if [ "$UNTRACKED" -gt 0 ]; then
    echo "📄 $UNTRACKED untracked files found"
    echo "💡 Consider adding important files to git"
    echo ""
fi

# Display recent activity
echo "📈 Recent Activity (last 5 commits):"
echo "================================"
git log --oneline -5

echo ""
echo "🎯 Session Ready!"
echo "Available scripts:"
echo "  ./scripts/sync-and-push.sh  - Safe push with conflict prevention"
echo "  ./scripts/session-end.sh    - Session cleanup and documentation"
echo ""

# Check for active session documentation
if [ -f "manus/ACTIVE_SESSIONS.md" ]; then
    echo "📋 Active session info found in manus/ACTIVE_SESSIONS.md"
else
    echo "💡 Consider creating manus/ACTIVE_SESSIONS.md to track concurrent work"
fi

echo "================================"
echo "✅ Session initialization complete!"
