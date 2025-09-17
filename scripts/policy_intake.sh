#!/usr/bin/env bash
set -euo pipefail
f="$1"; dest="policies/$(basename "$f")"
cp "$f" "$dest"
PYTHONPATH=. python -m engine.policy_index
echo "[policy] added $(basename "$f") and re-indexed"
