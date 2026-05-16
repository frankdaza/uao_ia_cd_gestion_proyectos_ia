---
id: TASK-5
title: >-
  Configurar entorno reproducible con UV (Python 3.12) y dependencias del
  laboratorio
status: Done
assignee:
  - Juan Velasquez
created_date: '2026-05-09 18:40'
updated_date: '2026-05-16 03:59'
labels: []
dependencies: []
references:
  - docs/tdsp-alineacion.md
  - consignas/Lab1.pdf
  - AGENTS.md
documentation:
  - pyproject.toml
  - uv.lock
  - README.md
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Materializar el requisito **P1** de docs/tdsp-alineacion.md y resolver la discrepancia documentada en §5 (consigna Lab1 sugiere `venv` + `pip`; este repositorio usa **UV** como estándar). Inicializar `pyproject.toml` y `uv.lock` con Python 3.12 fijo y todas las dependencias necesarias para correr el laboratorio (runtime) y el aseguramiento de calidad (dev), garantizando reproducibilidad para el equipo y para CI (TASK-19).

## Alcance

1. Pin de intérprete: `uv python pin 3.12`.
2. Inicializar `pyproject.toml` (proyecto: `laboratorio-drybean-ml`) con metadata mínima (nombre, versión, descripción, autores, requires-python `>=3.12,<3.13`).
3. Dependencias **runtime** (`uv add`): `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `ucimlrepo`, `joblib`, `openpyxl`, `jupyter`, `ipykernel`.
4. Dependencias **dev** (`uv add --dev`): `pytest`, `pytest-cov`, `ruff`, `black`, `pre-commit`, `nbstripout`.
5. Versionar `pyproject.toml` y `uv.lock`.
6. Documentar en README.md sección "Cómo correr" con `uv sync`, `uv run jupyter lab`, `uv run pytest`.

## Fuera de alcance

- Configuración de hooks de pre-commit (TASK-7).
- Implementación de notebooks o módulos (TASK-8 en adelante).
- Generación de `requirements.txt` para entrega (TASK-18).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 pyproject.toml declara requires-python '>=3.12,<3.13' y nombre del proyecto coherente.
- [ ] #2 uv.lock está versionado y uv sync reproduce el entorno desde cero sin errores.
- [ ] #3 uv run python -c 'import pandas, numpy, sklearn, ucimlrepo, joblib, matplotlib, openpyxl' termina con código 0.
- [ ] #4 uv run python -m pytest --version y uv run ruff --version responden correctamente (dev deps instalados).
- [ ] #5 README.md documenta los comandos canónicos uv sync, uv run jupyter lab y uv run pytest en una sección 'Cómo correr'.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Verificar versión de UV instalada (uv --version) y disponibilidad de Python 3.12.
2. Ejecutar uv init --package=false (o equivalente) para generar pyproject.toml mínimo, ajustando metadata manualmente.
3. uv python pin 3.12.
4. Agregar dependencias runtime con uv add ... y dev con uv add --dev ...
5. uv sync para generar uv.lock; verificar que el entorno se reproduce.
6. Smoke test de imports y de comandos pytest/ruff.
7. Actualizar README.md con sección 'Cómo correr' usando exclusivamente comandos UV.
8. Confirmar que .gitignore ya excluye .venv/ (o agregarlo si falta).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Versión objetivo: Python 3.12 (no proponer 3.10 sin acuerdo). No usar pip ni python -m venv como flujo predeterminado. Las versiones específicas deben fijarse desde uv.lock; en pyproject.toml usar restricciones laxas (>=) salvo motivo documentado.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 pyproject.toml y uv.lock revisados en PR; sin dependencias huérfanas ni duplicadas.
- [ ] #2 Si esta tarea cambia políticas de stack, sincronizar AGENTS.md, CLAUDE.md, .github/copilot-instructions.md y .cursor/rules/ según AGENTS.md.
<!-- DOD:END -->
