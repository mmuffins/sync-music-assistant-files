#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$HOME/Projects/sync-music-assistant-files"
SOURCE_DIR="$HOME/mySourceDirectory"
TARGET_DIR="/tmp/myTargetDirectory"

if ! command -v devenv >/dev/null 2>&1; then
  echo "devenv is required but was not found in PATH." >&2
  exit 1
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Project directory does not exist: $PROJECT_DIR" >&2
  exit 1
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory does not exist: $SOURCE_DIR" >&2
  exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target directory does not exist: $TARGET_DIR" >&2
  exit 1
fi

cd "$PROJECT_DIR"
exec devenv shell -- uv run main.py --source "$SOURCE_DIR" --target "$TARGET_DIR"
