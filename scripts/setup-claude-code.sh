#!/usr/bin/env bash
# Wire Claude Code to FreeLLMAPI (verified upstream command).
# Usage:  FREELLMAPI_API_KEY=<unified-key-from-dashboard> bash scripts/setup-claude-code.sh
# The script backs up your existing Claude Code config instead of
# clobbering it (upstream generator behaviour).
set -euo pipefail

if [ -z "${FREELLMAPI_API_KEY:-}" ]; then
  echo "Set FREELLMAPI_API_KEY first — the unified key from http://localhost:3001 (Keys page header)."
  echo "Never paste a provider key here; only the unified freellmapi-... key."
  exit 1
fi

curl -fsS http://127.0.0.1:3001/api/ping >/dev/null \
  || { echo "FreeLLMAPI is not running on localhost:3001. Start it first: docker compose up -d freellmapi"; exit 1; }

npx freellmapi setup-claude --url http://localhost:3001 --api-key "$FREELLMAPI_API_KEY"

echo
echo "Claude Code -> FreeLLMAPI done."
echo "OmniRoute alternative (no script needed, set in Claude Code settings):"
echo "  Base URL: http://localhost:20128/v1"
echo "  API Key:  copy from http://localhost:20128 -> Endpoints"
echo "  Model:    auto"
