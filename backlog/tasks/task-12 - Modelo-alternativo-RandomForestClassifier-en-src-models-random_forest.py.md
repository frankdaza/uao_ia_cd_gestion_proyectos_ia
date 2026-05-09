---
id: TASK-12
title: Modelo alternativo RandomForestClassifier en src/models/random_forest.py
status: To Do
assignee:
  - Jenifer Ramos
created_date: '2026-05-09 18:43'
labels: []
dependencies:
  - TASK-10
references:
  - consignas/Lab1.pdf
  - docs/tdsp-alineacion.md
documentation:
  - src/models/random_forest.py
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Implementar el **modelo alternativo** del laboratorio (PB-04 y L12): `RandomForestClassifier` con hiperparámetros explícitos y reproducibles. Junto al baseline (TASK-11), permite contrastar un modelo lineal vs. un ensamble de árboles para clasificación multiclase del Dry Bean Dataset.

## Alcance

1. Implementar `src/models/random_forest.py` con la **misma interfaz** que `baseline.py` para que sean intercambiables:
   - `build_rf_pipeline(n_estimators: int = 300, max_depth: int | None = None, random_state: int = 42, n_jobs: int = -1) -> Pipeline`.
   - `train_rf(X_train, y_train, **kwargs) -> Pipeline`.
   - `evaluate_rf(model, X_test, y_test) -> dict[str, float]` con `accuracy` y `f1_macro`.
   - Bloque `if __name__ == "__main__":` que orquesta carga → split → entrena → evalúa → guarda métricas en `outputs/reports/metrics_rf.json`.
2. Tests en `tests/test_models_random_forest.py` análogos a los del baseline.
3. Documentar hiperparámetros elegidos y razón en el docstring del módulo.

## Fuera de alcance

- Búsqueda de hiperparámetros con GridSearch / Optuna (extensión opcional, no exigida por la consigna).
- Comparación entre modelos (TASK-13).
- Persistencia joblib del modelo final (TASK-14).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 src/models/random_forest.py expone build_rf_pipeline, train_rf y evaluate_rf con type hints y docstrings en español.
- [ ] #2 uv run python -m src.models.random_forest produce outputs/reports/metrics_rf.json con claves accuracy y f1_macro.
- [ ] #3 Tests en tests/test_models_random_forest.py pasan con uv run pytest y validan retorno de las dos métricas.
- [ ] #4 Hiperparámetros (n_estimators, max_depth, random_state, n_jobs) son explícitos y reproducibles.
- [ ] #5 La interfaz pública es paralela a la del baseline (mismas firmas y nombres equivalentes).
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear src/models/random_forest.py.
2. build_rf_pipeline(): Pipeline([('rf', RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1))]). Random Forest no requiere StandardScaler, pero se mantiene Pipeline por consistencia y trazabilidad.
3. train_rf y evaluate_rf análogos al baseline.
4. main idéntico al baseline pero con outputs/reports/metrics_rf.json.
5. Test con datos sintéticos.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Random Forest no requiere escalado, por eso el Pipeline tiene un único paso. Mantener Pipeline (en lugar de el clasificador directo) facilita la persistencia con joblib (TASK-14) y la futura adición de transformadores. Documentar n_estimators=300 como compromiso entre tiempo de entrenamiento y desempeño.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Sin importes mutuos entre baseline.py y random_forest.py (ambos siguen un contrato común sin acoplarse).
- [ ] #2 Métricas serializadas en JSON UTF-8.
<!-- DOD:END -->
