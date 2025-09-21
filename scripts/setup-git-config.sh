#!/bin/bash

# setup-git-config.sh
# Configure Git for optimal AI agent session workflow

echo "⚙️  Configuring Git for AI Agent Development..."
echo "================================"

# Set better editor (avoid nano issues)
echo "📝 Setting up editor configuration..."
if command -v code &> /dev/null; then
    git config --global core.editor "code --wait"
    echo "✅ Set VS Code as default editor"
elif command -v vim &> /dev/null; then
    git config --global core.editor "vim"
    echo "✅ Set Vim as default editor"
else
    git config --global core.editor "nano"
    echo "⚠️  Using nano as fallback editor"
fi

# Configure merge tool
echo "🔧 Setting up merge tool..."
if command -v code &> /dev/null; then
    git config --global merge.tool vscode
    git config --global mergetool.vscode.cmd 'code --wait $MERGED'
    echo "✅ Set VS Code as merge tool"
elif command -v vimdiff &> /dev/null; then
    git config --global merge.tool vimdiff
    echo "✅ Set vimdiff as merge tool"
else
    echo "⚠️  No suitable merge tool found"
fi

# Enable rerere (reuse recorded resolution)
echo "🔄 Enabling conflict resolution reuse..."
git config --global rerere.enabled true
echo "✅ Enabled rerere for conflict resolution"

# Set pull strategy to rebase
echo "📥 Configuring pull strategy..."
git config --global pull.rebase true
echo "✅ Set pull to use rebase by default"

# Configure push behavior
echo "📤 Configuring push behavior..."
git config --global push.default simple
echo "✅ Set push to simple mode"

# Enable auto-setup of remote tracking
echo "🌿 Configuring branch tracking..."
git config --global branch.autosetupmerge always
git config --global branch.autosetuprebase always
echo "✅ Enabled automatic branch tracking and rebase"

# Configure diff and merge settings
echo "📊 Configuring diff and merge settings..."
git config --global diff.algorithm patience
git config --global merge.conflictstyle diff3
echo "✅ Improved diff algorithm and conflict style"

# Set up useful aliases
echo "🔗 Setting up useful aliases..."
git config --global alias.st "status"
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.ci "commit"
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
git config --global alias.visual "!gitk"
git config --global alias.sync "!git fetch origin && git rebase origin/main"
git config --global alias.safepush "!bash scripts/sync-and-push.sh"
echo "✅ Added helpful Git aliases"

# Configure line ending handling
echo "📄 Configuring line endings..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    git config --global core.autocrlf true
else
    git config --global core.autocrlf input
fi
echo "✅ Configured line ending handling"

# Set up better logging
echo "📋 Configuring log format..."
git config --global log.oneline true
git config --global format.pretty "format:%C(yellow)%h%C(reset) %C(blue)%an%C(reset) %C(green)%ar%C(reset) %s"
echo "✅ Improved log formatting"

# Display current configuration
echo ""
echo "📋 Current Git Configuration:"
echo "================================"
echo "Editor: $(git config --global core.editor)"
echo "Merge tool: $(git config --global merge.tool)"
echo "Pull strategy: $(git config --global pull.rebase)"
echo "Push default: $(git config --global push.default)"
echo "Rerere enabled: $(git config --global rerere.enabled)"

echo ""
echo "🎯 Available Aliases:"
echo "================================"
echo "git st        - git status"
echo "git co        - git checkout"
echo "git br        - git branch"
echo "git ci        - git commit"
echo "git unstage   - git reset HEAD --"
echo "git last      - git log -1 HEAD"
echo "git sync      - git fetch origin && git rebase origin/main"
echo "git safepush  - Use safe push script"

echo ""
echo "✅ Git configuration complete!"
echo "💡 Use 'git safepush' instead of 'git push' to prevent conflicts"
