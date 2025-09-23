#!/usr/bin/env bash
set -euo pipefail

SAAS_ARCH_PATH=${1:-${SAAS_ARCH_PATH:-../saas-ecosystem-architecture}}

if [ ! -d "$SAAS_ARCH_PATH" ]; then
  echo "❌ SaaSArch repository not found at $SAAS_ARCH_PATH" >&2
  exit 1
fi

SOURCE_DIR="$(dirname "$0")/../shared/templates/agent_templates"
TARGET_DIR="$SAAS_ARCH_PATH/standards/templates/agent"
REGISTRY_SRC="$(dirname "$0")/../agents/registry.json"
REGISTRY_DEST="$TARGET_DIR/registry.json"

mkdir -p "$TARGET_DIR"
cp "$SOURCE_DIR"/* "$TARGET_DIR"/

if [ -f "$REGISTRY_SRC" ]; then
  cp "$REGISTRY_SRC" "$REGISTRY_DEST"
  echo "🗂️ Copied agents/registry.json to $REGISTRY_DEST"
else
  echo "⚠️ Warning: agents/registry.json not found; registry not synced"
fi

echo "✅ Synced agent templates to $TARGET_DIR"
