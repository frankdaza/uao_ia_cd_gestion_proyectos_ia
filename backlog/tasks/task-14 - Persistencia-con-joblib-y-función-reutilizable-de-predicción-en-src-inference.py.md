---
id: TASK-14
title: >-
  Persistencia con joblib y función reutilizable de predicción en
  src/inference.py
status: Done
assignee:
  - Jenifer Ramos
created_date: '2026-05-09 18:44'
labels: []
dependencies:
  - TASK-13
references:
  - consignas/Lab1.pdf
  - docs/tdsp-alineacion.md
documentation:
  - src/inference.py
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Cubrir el cierre de PB-04, **L13** (persistencia con joblib bajo `outputs/models/`) y **L14** (función reutilizable de predicción y mini despliegue como vínculo con la fase Despliegue de CRISP-DM). Esta tarea materializa el modelo final seleccionado por TASK-13 como artefacto serializado y entrega una API mínima de inferencia.

## Alcance

1. Implementar `src/inference.py` con:
   - `save_model(model, path: Path) -> Path`.
   - `load_model(path: Path) -> Pipeline`.
   - `predict(model_or_path, X: pd.DataFrame) -> np.ndarray`.
   - `predict_one(model_or_path, sample: dict) -> str` (predicción de prueba sobre un único registro).
2. Script `if __name__ == "__main__":` que:
   - Entrena el modelo seleccionado (típicamente Random Forest).
   - Lo guarda en `outputs/models/random_forest_drybean.joblib`.
   - Carga el modelo y hace una predicción de prueba con la primera fila del test set.
   - Imprime resumen y código de retorno 0.
3. Tests en `tests/test_inference.py`: round-trip save → load → predict mantiene la salida.
4. Documentar en docstring un ejemplo de uso (cargar y predecir).

## Fuera de alcance

- API HTTP / FastAPI (no exigida en la consigna).
- Dockerización (extensión opcional).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 src/inference.py expone save_model, load_model, predict y predict_one con type hints y docstrings en español.
- [ ] #2 uv run python -m src.inference genera outputs/models/random_forest_drybean.joblib y muestra una predicción de prueba.
- [ ] #3 tests/test_inference.py valida round-trip save/load/predict con datos sintéticos.
- [ ] #4 Las funciones aceptan tanto un objeto Pipeline ya cargado como una ruta a archivo .joblib (firma flexible).
- [ ] #5 El archivo .joblib NO queda versionado (excluido por .gitignore vigente desde TASK-3).
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear src/inference.py con save_model/load_model/predict/predict_one.
2. main: entrenar RF (build_rf_pipeline + train_rf), save_model a outputs/models/random_forest_drybean.joblib, load_model y predecir la primera fila del test.
3. Tests con monkeypatch o tmp_path para validar round-trip sin tocar el sistema de archivos real.
4. Validar que git status no incluye el .joblib.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
joblib >= 1.3 incluido en TASK-5. predict_one debe convertir el dict a DataFrame de una fila preservando el orden de columnas del entrenamiento; documentar este contrato. Nombre del modelo serializado: random_forest_drybean.joblib (alineado con la consigna L13).
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Docstring del módulo incluye ejemplo de carga y predicción copiable y verificado.
- [ ] #2 Si la firma de predict cambia respecto a la convención sklearn (predict/predict_proba), justificarlo en el docstring.
<!-- DOD:END -->
