---
id: TASK-11
title: >-
  Modelo baseline: Pipeline(StandardScaler + LogisticRegression) en
  src/models/baseline.py
status: Done
assignee:
  - Juan Velasquez
created_date: '2026-05-09 18:42'
updated_date: '2026-05-16 03:59'
labels: []
dependencies:
  - TASK-10
references:
  - consignas/Lab1.pdf
  - docs/tdsp-alineacion.md
documentation:
  - src/models/baseline.py
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Implementar el **modelo baseline** del laboratorio (PB-03 y L12): un `sklearn.pipeline.Pipeline` que encadena `StandardScaler` y `LogisticRegression`. Sirve como referencia inferior contra la cual se compara el modelo alternativo (TASK-12) y permite cerrar la fase de Modelado de CRISP-DM con un artefacto reproducible y trazable.

## Alcance

1. Crear paquete `src/models/` con `__init__.py`.
2. Implementar `src/models/baseline.py` con:
   - Función `build_baseline_pipeline(random_state: int = 42, max_iter: int = 1000) -> Pipeline`.
   - Función `train_baseline(X_train, y_train, **kwargs) -> Pipeline`.
   - Función `evaluate_baseline(model, X_test, y_test) -> dict[str, float]` que retorna `{"accuracy": ..., "f1_macro": ...}`.
   - Bloque `if __name__ == "__main__":` que orquesta carga (TASK-8) → split (TASK-10) → entrena → evalúa → guarda métricas en `outputs/reports/metrics_baseline.json`.
3. Tests en `tests/test_models_baseline.py` con un DataFrame sintético: el pipeline ajusta sin error y `evaluate_baseline` retorna las dos métricas con valores en [0, 1].

## Fuera de alcance

- Modelo alternativo Random Forest (TASK-12).
- Comparación entre modelos y matriz de confusión (TASK-13).
- Persistencia con joblib del modelo final (TASK-14).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 src/models/baseline.py expone build_baseline_pipeline, train_baseline y evaluate_baseline con type hints y docstrings en español.
- [ ] #2 uv run python -m src.models.baseline ejecuta el flujo end-to-end y produce outputs/reports/metrics_baseline.json con claves accuracy y f1_macro.
- [ ] #3 tests/test_models_baseline.py pasa con uv run pytest.
- [ ] #4 Las métricas se calculan con sklearn.metrics.accuracy_score y f1_score(average='macro').
- [ ] #5 Random_state está fijo (42) tanto en el split como en el modelo para reproducibilidad.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear src/models/__init__.py y src/models/baseline.py.
2. build_baseline_pipeline(): Pipeline([('scaler', StandardScaler()), ('lr', LogisticRegression(max_iter=1000, random_state=42))]).
3. train_baseline(X_train, y_train): fit y retorno.
4. evaluate_baseline(model, X_test, y_test): predict + accuracy_score + f1_score(average='macro').
5. main: fetch_drybean -> clean -> split -> train -> evaluate -> dump JSON.
6. Test con datos sintéticos.
7. uv run python -m src.models.baseline para validar.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Usar LogisticRegression con max_iter=1000 (evita warnings de convergencia con datos escalados). Si el dataset tarda en converger, considerar solver='lbfgs' (default) o 'saga'. Estandarizar SIEMPRE dentro del Pipeline para evitar fuga de información del test al train.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Sin acoplamiento al modelo alternativo: este módulo no importa Random Forest.
- [ ] #2 Métricas serializadas en JSON ASCII-safe (sin caracteres no UTF-8).
<!-- DOD:END -->
