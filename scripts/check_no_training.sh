#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m compileall -q src tests
python -m ruff check src tests
python -m pytest -q
nox download
nox audit --output reports/data_audit.json
nox dry-run
