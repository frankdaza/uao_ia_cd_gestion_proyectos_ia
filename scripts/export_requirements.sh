#!/usr/bin/env bash
# Genera requirements.txt desde el lock de UV (artefacto derivado; fuente de verdad: pyproject.toml + uv.lock).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

exec uv export --no-hashes --format requirements-txt -o requirements.txt
