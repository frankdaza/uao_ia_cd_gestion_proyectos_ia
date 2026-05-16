---
id: TASK-19
title: 'CI smoke test con GitHub Actions: lint, tests y ejecución del notebook'
status: Done
assignee:
  - Frank Daza
created_date: '2026-05-09 18:46'
updated_date: '2026-05-15'
labels: []
dependencies:
  - TASK-15
references:
  - docs/tdsp-alineacion.md
  - AGENTS.md
  - .github/copilot-instructions.md
documentation:
  - .github/workflows/ci.yml
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Implementar el **TDSP profesional ligero** sugerido en `docs/tdsp-alineacion.md` §3: un workflow de GitHub Actions que verifica en cada push/PR que el laboratorio sigue siendo reproducible (lint, tests y ejecución del notebook integrador). Cierra el bloque de aseguramiento sin imponer DVC/MLflow (extensión opcional fuera del alcance del curso).

## Alcance

1. Crear `.github/workflows/ci.yml` con un job `quality-and-smoke` que:
   - Corre en `ubuntu-latest`.
   - Instala UV (`astral-sh/setup-uv@v3` o equivalente vigente).
   - Pin de Python 3.12.
   - Cachea `uv.lock`.
   - `uv sync --all-extras --dev`.
   - `uv run pre-commit run --all-files` (TASK-7).
   - `uv run pytest -q --maxfail=1`.
   - `uv run jupyter nbconvert --to notebook --execute --output /tmp/integrador-ci.ipynb notebooks/01_laboratorio_drybean.ipynb`.
2. Añadir badges al README (build status).
3. Configurar disparadores: `push` a `main` y `pull_request` hacia `main`.
4. Reportar duración objetivo del job (< 10 min como referencia, no bloqueante).

## Fuera de alcance

- Despliegue a registry / model registry (extensión opcional).
- Cobertura mínima bloqueante (referencia, no enforced en este sprint).
- DVC, MLflow u otros frameworks de seguimiento de experimentos.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .github/workflows/ci.yml existe y se dispara en push a main y pull_request a main.
- [x] #2 El workflow ejecuta uv sync, uv run pre-commit run --all-files, uv run pytest y uv run jupyter nbconvert --execute sobre notebooks/01_laboratorio_drybean.ipynb.
- [ ] #3 Un PR de prueba con un cambio trivial completa el job en verde (confirmar en GitHub tras el primer push del workflow).
- [ ] #4 Un PR con violación de ruff/black o test fallido bloquea el merge (configurar branch protection y el check **CI** como requerido; ver README).
- [x] #5 README.md muestra el badge de estado del workflow.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear .github/workflows/ci.yml con jobs y steps detallados.
2. Usar astral-sh/setup-uv@v3 con enable-cache: true.
3. Pin de Python 3.12 (uv python install 3.12).
4. uv sync --dev.
5. Pasos de pre-commit, pytest y nbconvert --execute.
6. Probar con un PR de prueba en una rama feature/.
7. Añadir badge a README.md.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
**Datos en CI:** antes de `nbconvert --execute`, el workflow ejecuta `scripts/ci_seed_drybean_cache.py`, que escribe `data/raw/drybean.parquet` (ignorado por Git). Así `fetch_drybean(cache_dir=...)` no llama a la red.

**Verificación local (2026-05-15):** mismos pasos que el workflow (`pre-commit run --all-files`, `pytest`, semilla, `nbconvert`) ejecutados con éxito en el entorno del desarrollador.

**Pendiente en GitHub:** AC #3 (PR de prueba en Actions) y AC #4 (branch protection) requieren acciones en el remoto; instrucciones en `README.md` sección *Integración continua*.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Tiempo de ejecución del job documentado en notas (referencia, sin SLA estricto).
- [x] #2 No aplica sincronización extra de AGENTS.md / reglas: el CI se documenta en README y el check requerido en `main` queda a cargo del administrador del repo en GitHub.
<!-- DOD:END -->
