#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-ci}"

usage() {
  cat <<'USAGE'
Usage: scripts/verify.sh [ci|syntax|json|test]

Targets:
  ci      Run offline syntax, checked-in JSON, and fixture checks.
  syntax  Compile Python files without importing browser/proxy dependencies.
  json    Parse checked-in result JSON files.
  test    Run synthetic page fixtures without browser dependencies.

This verifier does not install browser engines, launch browsers, use proxies, or contact external targets.
USAGE
}

run_repo() {
  (cd "$ROOT_DIR" && "$@")
}

check_syntax() {
  run_repo python3 -m py_compile $(find . -path './.venv' -prune -o -path './node_modules' -prune -o -name '*.py' -print)
}

check_json() {
  run_repo python3 - <<'PY'
import json
from pathlib import Path

for path in Path("results").rglob("*.json"):
    json.loads(path.read_text(encoding="utf-8"))
PY
}

case "$TARGET" in
  ci)
    "$0" syntax
    "$0" json
    "$0" test
    ;;
  syntax)
    check_syntax
    ;;
  json)
    check_json
    ;;
  test)
    run_repo python3 -m unittest discover -s tests -v
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
