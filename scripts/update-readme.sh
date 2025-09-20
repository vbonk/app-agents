#!/bin/bash

# Manual README Update Script
# This script can be run locally to update the README.md with current agent information

set -e

echo "🔄 Updating README.md with current agent information..."

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: README.md not found. Please run this script from the repository root."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Install required dependencies if needed
echo "📦 Installing required Python packages..."
pip3 install -q pyyaml pandas openpyxl 2>/dev/null || {
    echo "⚠️ Warning: Could not install some packages. Continuing anyway..."
}

# Run the update script
echo "🚀 Running README update script..."
python3 .github/scripts/update_readme.py

# Check if changes were made
if git diff --quiet README.md; then
    echo "ℹ️ No changes needed - README.md is already up to date"
else
    echo "✅ README.md has been updated!"
    echo ""
    echo "📝 Changes made:"
    git diff --stat README.md
    echo ""
    echo "💡 To commit these changes, run:"
    echo "   git add README.md"
    echo "   git commit -m 'docs: update README with latest agent information'"
    echo "   git push"
fi

echo ""
echo "✨ README update complete!"
