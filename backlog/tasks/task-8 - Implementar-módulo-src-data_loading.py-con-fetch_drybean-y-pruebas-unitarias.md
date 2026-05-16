---
id: TASK-8
title: Implementar módulo src/data_loading.py con fetch_drybean() y pruebas unitarias
status: Done
assignee:
  - Juan Velasquez
created_date: '2026-05-09 18:41'
updated_date: '2026-05-16 03:59'
labels: []
dependencies:
  - TASK-5
  - TASK-7
references:
  - consignas/Lab1.pdf
  - docs/tdsp-alineacion.md
documentation:
  - src/data_loading.py
  - tests/test_data_loading.py
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Encapsular en `src/` la carga del Dry Bean Dataset (UCI 602) para poder reutilizarla desde notebooks (EDA, integrador) y desde scripts de modelado. Cubre los requisitos **L11** (carga real con `fetch_ucirepo(id=602)`) y **PB-01** (datos disponibles y trazables).

## Alcance

1. Crear paquete `src/` con `__init__.py` y módulo `src/data_loading.py`.
2. Implementar `fetch_drybean(cache_dir: Path | None = None) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]` que:
   - Use `ucimlrepo.fetch_ucirepo(id=602)`.
   - Retorne `(X, y, df)` donde `df` es la unión con columna `Class`.
   - Soporte cacheo opcional en `cache_dir` (parquet) para evitar descargas repetidas en CI/dev.
3. Implementar `load_drybean(path: Path) -> pd.DataFrame` para leer un parquet/CSV local cuando ya se descargó.
4. Crear `tests/__init__.py` (vacío) y `tests/test_data_loading.py` con:
   - Test de contrato sobre `fetch_drybean` usando `monkeypatch` o `unittest.mock` para no depender de red.
   - Test de tipos y columnas mínimas (incluye `Class`).
5. Docstrings en español latinoamericano y type hints en todas las funciones públicas.

## Fuera de alcance

- EDA o limpieza (TASK-9, TASK-10).
- Persistencia de modelos (TASK-14).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 src/__init__.py y src/data_loading.py existen; from src.data_loading import fetch_drybean, load_drybean es importable bajo uv run.
- [ ] #2 fetch_drybean retorna (X, y, df) con tipos pandas correctos; df contiene la columna Class y todas las features numéricas del dataset UCI 602.
- [ ] #3 tests/test_data_loading.py pasa con uv run pytest y cubre al menos: contrato de retorno, presencia de columna Class, manejo de cache_dir.
- [ ] #4 Las funciones públicas tienen docstrings en español y type hints completos.
- [ ] #5 uv run ruff check src tests termina con código 0.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear src/__init__.py y src/data_loading.py.
2. Implementar fetch_drybean con type hints; usar Path para cache_dir y to_parquet/read_parquet.
3. Implementar load_drybean(path).
4. Escribir tests con monkeypatch sobre ucimlrepo.fetch_ucirepo retornando un objeto stub con .data.features y .data.targets.
5. Verificar con uv run pytest -q y uv run ruff check.
6. Documentar uso mínimo en docstring del módulo.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
El paquete ucimlrepo expone fetch_ucirepo(id=602) que retorna un objeto con atributos .data.features (DataFrame) y .data.targets (DataFrame con columna Class). Usar pandas >= 2.0 (definido en TASK-5). El cache_dir es opcional y debe respetar la política de no versionar binarios (data/raw o data/processed quedan ignorados por .gitignore).
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Cobertura mínima del módulo data_loading reportada con uv run pytest --cov=src/data_loading (referencia, no umbral bloqueante en este sprint).
- [ ] #2 El test no falla si no hay red (uso de mock para fetch_ucirepo).
<!-- DOD:END -->
