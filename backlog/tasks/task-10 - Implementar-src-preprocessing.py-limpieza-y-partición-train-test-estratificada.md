---
id: TASK-10
title: >-
  Implementar src/preprocessing.py: limpieza y partición train/test
  estratificada
status: Done
assignee:
  - Juan Velasquez
created_date: '2026-05-09 18:42'
updated_date: '2026-05-16 03:59'
labels: []
dependencies:
  - TASK-8
references:
  - consignas/Lab1.pdf
  - docs/tdsp-alineacion.md
documentation:
  - src/preprocessing.py
  - tests/test_preprocessing.py
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Encapsular la fase de **Preparación de datos** de CRISP-DM en funciones puras, testeables y reutilizables desde notebooks y scripts de modelado. Cubre los requisitos **L11** (drop_duplicates, manejo de nulos) y **L12** (partición train/test). Este módulo es prerequisito de los modelos baseline (TASK-11) y alternativo (TASK-12).

## Alcance

1. Implementar `src/preprocessing.py` con funciones puras:
   - `clean(df: pd.DataFrame) -> pd.DataFrame`: aplica `drop_duplicates`, valida ausencia de nulos en `Class`, opcionalmente imputa o elimina filas con nulos en features.
   - `split(df: pd.DataFrame, target: str = "Class", test_size: float = 0.2, random_state: int = 42) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]`: usa `sklearn.model_selection.train_test_split` con `stratify=df[target]`.
2. Type hints completos y docstrings en español.
3. Tests en `tests/test_preprocessing.py`:
   - `clean` elimina duplicados y mantiene la columna `Class`.
   - `split` retorna proporciones esperadas y mantiene la estratificación (KS o equivalente).
   - `random_state` produce resultados deterministas.

## Fuera de alcance

- Cualquier transformación que dependa del modelo (escalado, encoding) — eso vive en el `Pipeline` de TASK-11 / TASK-12.
- Persistencia de splits a disco (opcional, no obligatorio).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 src/preprocessing.py expone clean y split con type hints y docstrings en español.
- [ ] #2 tests/test_preprocessing.py pasa con uv run pytest y valida: eliminación de duplicados, presencia de Class, proporciones del split, determinismo con random_state, estratificación por Class.
- [ ] #3 Las funciones no mutan el DataFrame de entrada (idempotentes y puras).
- [ ] #4 uv run ruff check src tests termina con código 0 sobre el módulo modificado.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear src/preprocessing.py con clean() y split().
2. clean(): df.copy() -> drop_duplicates -> validar Class no nulo -> retornar.
3. split(): train_test_split con stratify y random_state.
4. Escribir tests con un DataFrame sintético pequeño y representativo.
5. Verificar uv run pytest -q y uv run ruff check.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
test_size por defecto 0.2 y random_state 42, alineado con la convención del laboratorio. Si el equipo decide otro split (p. ej. 0.3), documentar la justificación en la docstring y en el reporte (TASK-16).
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Cobertura del módulo preprocessing reportable con uv run pytest --cov=src/preprocessing.
- [ ] #2 Documentación de uso mínimo en el docstring del módulo o en docs/ si aplica.
<!-- DOD:END -->
