#!/bin/bash

# session-end.sh
# Session cleanup and documentation update

echo "🏁 Ending AI Agent Session..."
echo "================================"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo "Files with changes:"
    git status --porcelain
    echo ""
    read -p "Do you want to commit these changes? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📝 Please provide a commit message:"
        read -p "Commit message: " commit_message
        git add .
        git commit -m "$commit_message"
        echo "✅ Changes committed"
    else
        echo "⚠️  Changes left uncommitted"
    fi
fi

# Check if we have unpushed commits
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
if [ "$AHEAD" -gt 0 ]; then
    echo "📤 You have $AHEAD unpushed commits"
    echo "Unpushed commits:"
    git log --oneline origin/main..HEAD
    echo ""
    read -p "Do you want to push these commits? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Using safe push script..."
        ./scripts/sync-and-push.sh
    else
        echo "⚠️  Commits left unpushed"
        echo "💡 Remember to push later using: ./scripts/sync-and-push.sh"
    fi
fi

# Update session documentation
echo ""
echo "📋 Updating session documentation..."

# Create session summary
SESSION_DATE=$(date +"%Y-%m-%d %H:%M:%S")
SESSION_ID="session-$(date +"%Y%m%d-%H%M%S")"

# Update or create active sessions file
mkdir -p manus
cat > manus/LAST_SESSION.md << EOF
# Last Session Summary

**Session ID**: $SESSION_ID
**End Time**: $SESSION_DATE
**Branch**: $(git branch --show-current)
**Last Commit**: $(git log --oneline -1)

## Session Statistics
- **Commits Made**: $(git rev-list --count HEAD --since="1 hour ago")
- **Files Modified**: $(git diff --name-only HEAD~1 2>/dev/null | wc -l)
- **Repository Status**: $(if [ "$AHEAD" -eq 0 ]; then echo "Synced"; else echo "$AHEAD commits ahead"; fi)

## Files Changed This Session
$(git diff --name-only HEAD~3 2>/dev/null | head -10)

## Next Session Recommendations
- Check manus/Agents.md for session context
- Run ./scripts/session-start.sh for repository health check
- Review recent commits for context

## Repository State
- **Clean Working Directory**: $(if git diff-index --quiet HEAD --; then echo "Yes"; else echo "No"; fi)
- **Synced with Remote**: $(if [ "$AHEAD" -eq 0 ]; then echo "Yes"; else echo "No"; fi)
- **Latest Remote Commit**: $(git log --oneline origin/main -1 2>/dev/null || echo "Unknown")
EOF

echo "✅ Session documentation updated in manus/LAST_SESSION.md"

# Display session summary
echo ""
echo "📊 Session Summary:"
echo "================================"
echo "🆔 Session ID: $SESSION_ID"
echo "⏰ Duration: Session ended at $SESSION_DATE"
echo "🌿 Branch: $(git branch --show-current)"
echo "📝 Last commit: $(git log --oneline -1)"
echo "📊 Repository status: $(if [ "$AHEAD" -eq 0 ]; then echo "✅ Synced with remote"; else echo "⚠️  $AHEAD commits ahead of remote"; fi)"
echo "🧹 Working directory: $(if git diff-index --quiet HEAD --; then echo "✅ Clean"; else echo "⚠️  Has uncommitted changes"; fi)"

echo ""
echo "🎯 Next Session Setup:"
echo "================================"
echo "1. Run: ./scripts/session-start.sh"
echo "2. Review: manus/Agents.md for context"
echo "3. Check: manus/LAST_SESSION.md for previous work"
echo ""

echo "✅ Session cleanup complete!"
echo "👋 Thank you for using the AI Agent Development Platform!"
