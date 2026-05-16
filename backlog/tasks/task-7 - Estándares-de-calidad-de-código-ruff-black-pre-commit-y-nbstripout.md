---
id: TASK-7
title: 'Estándares de calidad de código: ruff, black, pre-commit y nbstripout'
status: Done
assignee:
  - Frank Daza
created_date: '2026-05-09 18:41'
updated_date: '2026-05-16 03:59'
labels: []
dependencies:
  - TASK-5
references:
  - docs/tdsp-alineacion.md
  - AGENTS.md
documentation:
  - pyproject.toml
  - .pre-commit-config.yaml
ordinal: 500
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Adoptar estándares mínimos de calidad de código de la industria sobre el repositorio para que el laboratorio sea revisable, reproducible y compatible con CI (TASK-19). Esta tarea establece **lint** (ruff), **format** (black + ruff format en compatibilidad), **higiene de notebooks** (nbstripout) y **automatización local** (pre-commit) usando exclusivamente UV como ejecutor.

## Alcance

1. Configurar `[tool.ruff]` y `[tool.ruff.lint]` en `pyproject.toml` con regla mínima razonable (E, F, I, B, UP) y `line-length = 100` para alinear con black.
2. Configurar `[tool.black]` en `pyproject.toml` (`line-length = 100`, `target-version = ['py312']`).
3. Crear `.pre-commit-config.yaml` con hooks: `ruff` (lint + autofix), `ruff-format` o `black`, `nbstripout`, `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-added-large-files` (limit 5MB).
4. Documentar instalación y uso: `uv run pre-commit install` y `uv run pre-commit run --all-files`.
5. Asegurar que el repositorio actual pasa `pre-commit run --all-files` (corregir hallazgos triviales).

## Fuera de alcance

- Configuración del workflow de GitHub Actions (TASK-19).
- Modificación de comportamiento funcional del código (solo formato/lint).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pyproject.toml contiene secciones [tool.ruff], [tool.ruff.lint] y [tool.black] coherentes (line-length 100, target py312).
- [x] #2 .pre-commit-config.yaml existe en la raíz e incluye hooks ruff, ruff-format o black, nbstripout y los hooks estándar de higiene de archivos.
- [x] #3 uv run pre-commit run --all-files termina con código 0 sobre el repositorio en su estado actual.
- [x] #4 README.md (o docs/calidad-codigo.md) documenta cómo instalar (uv run pre-commit install) y cómo correr los hooks.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Instalar deps dev (ya cubiertas por TASK-5): ruff, black, pre-commit, nbstripout.
2. Definir reglas en pyproject.toml: [tool.ruff] line-length 100, target-version py312; [tool.ruff.lint] select = ['E','F','I','B','UP']; [tool.black] line-length 100, target-version py312.
3. Crear .pre-commit-config.yaml con repos versionados (ruff, black o ruff-format, nbstripout, pre-commit-hooks).
4. uv run pre-commit install --install-hooks.
5. uv run pre-commit run --all-files; revisar y aceptar cambios automáticos.
6. Documentar comandos en README.md o docs/calidad-codigo.md.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Si el equipo prefiere ruff-format como único formateador, eliminar black para evitar conflicto. Mantener una sola fuente de verdad de formato. nbstripout evita versionar outputs y metadata pesada de notebooks (alineado con flujo de notebooks/).
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Ningún archivo ignorado por error por las reglas (verificar con git diff tras pre-commit).
- [x] #2 Si esta tarea altera políticas de calidad globales, sincronizar AGENTS.md, CLAUDE.md, .github/copilot-instructions.md y reglas .cursor/rules/ según AGENTS.md.
<!-- DOD:END -->
