---
id: TASK-18
title: >-
  README final: sección de reproducibilidad y export de requirements.txt desde
  UV
status: To Do
assignee:
  - Yan Cuaran
created_date: '2026-05-09 18:46'
labels: []
dependencies:
  - TASK-14
references:
  - consignas/Plan_Equipos_ScrumML_DryBean.pdf
  - docs/tdsp-alineacion.md
  - AGENTS.md
documentation:
  - README.md
  - scripts/export_requirements.sh
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Cerrar el requisito **PB-06** y **P2** (Plan de Equipos exige `requirements.txt`) sin renunciar a UV como fuente de verdad del entorno (política del repositorio, ver `docs/tdsp-alineacion.md` §5). Esta tarea actualiza el `README.md` con instrucciones claras de reproducibilidad y entrega un mecanismo automatizado para generar `requirements.txt` cuando el docente lo exija.

## Alcance

1. Actualizar `README.md` con sección **"Cómo correr el laboratorio"** que cubra:
   - Requisitos previos (Python 3.12, UV instalado).
   - `uv sync` (instala desde `uv.lock`).
   - `uv run pre-commit install` (TASK-7).
   - `uv run pytest` (suite de tests).
   - `uv run jupyter lab notebooks/01_laboratorio_drybean.ipynb`.
   - `uv run python -m src.inference` (predicción de prueba).
2. Crear `scripts/export_requirements.sh` (o tarea equivalente en `pyproject.toml`/`Makefile`) que ejecute `uv export --no-hashes --format requirements-txt -o requirements.txt`.
3. Documentar en README que `requirements.txt` se genera bajo demanda y la **fuente de verdad es `pyproject.toml` + `uv.lock`**.
4. Verificar que el script se ejecuta sin error y produce un `requirements.txt` válido (`pip install -r requirements.txt --dry-run` pasa).

## Fuera de alcance

- Configuración de CI (TASK-19).
- Versionado de `requirements.txt` en cada commit (se genera bajo demanda).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 README.md contiene sección 'Cómo correr el laboratorio' con los comandos UV listados (uv sync, uv run pytest, uv run jupyter lab, uv run python -m src.inference).
- [ ] #2 scripts/export_requirements.sh existe, es ejecutable y corre uv export con los flags correctos.
- [ ] #3 Ejecutar bash scripts/export_requirements.sh produce requirements.txt sin error.
- [ ] #4 README declara explícitamente que pyproject.toml + uv.lock son la fuente de verdad y que requirements.txt es derivado.
- [ ] #5 requirements.txt está en .gitignore (o se versiona deliberadamente con justificación documentada).
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Editar README.md: añadir sección 'Cómo correr el laboratorio' con los comandos UV.
2. Crear scripts/export_requirements.sh con uv export --no-hashes --format requirements-txt -o requirements.txt.
3. chmod +x scripts/export_requirements.sh.
4. Probar el script en local; verificar requirements.txt válido.
5. Actualizar .gitignore para excluir requirements.txt si se decide no versionarlo.
6. Confirmar que la nota 'fuente de verdad: pyproject.toml + uv.lock' está visible en README.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
El plan de equipos lista requirements.txt como artefacto esperado, pero la política del repo es UV. Esta tarea ofrece la equivalencia: generar requirements.txt desde uv export bajo demanda. Mantener la doble vía evita romper la entrega académica sin abandonar la reproducibilidad de UV.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Si esta tarea cambia políticas globales del stack, sincronizar AGENTS.md, CLAUDE.md, .github/copilot-instructions.md y .cursor/rules/ según AGENTS.md.
- [ ] #2 Sección README pasa revisión cruzada de un par antes de merge.
<!-- DOD:END -->
