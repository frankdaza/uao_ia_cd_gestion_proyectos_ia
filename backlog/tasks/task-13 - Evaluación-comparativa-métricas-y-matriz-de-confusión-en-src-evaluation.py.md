---
id: TASK-13
title: 'Evaluación comparativa, métricas y matriz de confusión en src/evaluation.py'
status: To Do
assignee:
  - Jenifer Ramos
created_date: '2026-05-09 18:43'
labels: []
dependencies:
  - TASK-11
  - TASK-12
references:
  - consignas/Lab1.pdf
  - docs/tdsp-alineacion.md
documentation:
  - src/evaluation.py
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Cerrar la fase de **Evaluación** de CRISP-DM (PB-05, L12) con un módulo único que compare baseline (TASK-11) y Random Forest (TASK-12) usando **accuracy** y **F1 macro**, genere la **matriz de confusión** del modelo principal y emita un `classification_report` por clase. Este módulo produce los artefactos que el reporte breve (TASK-16) y el notebook integrador (TASK-15) consumen.

## Alcance

1. Implementar `src/evaluation.py` con:
   - `compare_models(models: dict[str, Pipeline], X_test, y_test) -> pd.DataFrame` con columnas `model`, `accuracy`, `f1_macro`.
   - `select_best(comparison: pd.DataFrame, metric: str = "f1_macro") -> str`.
   - `plot_confusion_matrix(model, X_test, y_test, labels: list[str], output_path: Path) -> Path` que guarda PNG.
   - `save_classification_report(model, X_test, y_test, output_path: Path) -> Path` que guarda `.txt`.
2. Crear bloque `if __name__ == "__main__":` que entrena ambos modelos, los compara, exporta:
   - `outputs/reports/comparison.csv` (tabla),
   - `outputs/reports/confusion_matrix.png` (modelo seleccionado),
   - `outputs/reports/classification_report.txt`.
3. Tests en `tests/test_evaluation.py` con dos modelos sintéticos y datos pequeños.

## Fuera de alcance

- Persistencia del modelo final con joblib (TASK-14).
- Reporte narrativo (TASK-16).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 src/evaluation.py expone compare_models, select_best, plot_confusion_matrix y save_classification_report con type hints y docstrings en español.
- [ ] #2 uv run python -m src.evaluation genera outputs/reports/comparison.csv, outputs/reports/confusion_matrix.png y outputs/reports/classification_report.txt.
- [ ] #3 comparison.csv contiene una fila por modelo con accuracy y f1_macro numéricos.
- [ ] #4 La matriz de confusión PNG está etiquetada con los nombres de clase del Dry Bean (no índices numéricos).
- [ ] #5 Tests en tests/test_evaluation.py pasan con uv run pytest.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear src/evaluation.py.
2. compare_models: predict + accuracy + f1_macro por modelo, retorna DataFrame.
3. select_best: idxmax sobre la métrica elegida.
4. plot_confusion_matrix: ConfusionMatrixDisplay.from_estimator con labels, savefig.
5. save_classification_report: classification_report(..., target_names=labels) escrito a .txt.
6. main: instancia ambos modelos (importa build_baseline_pipeline y build_rf_pipeline), entrena, compara, exporta.
7. Tests con datos sintéticos.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Importar las funciones build_*_pipeline desde src/models/ pero NO ejecutar sus mains (evita doble entrenamiento). Usar matplotlib backend 'Agg' para CI headless. La selección 'best' se documenta también en TASK-16 (reporte).
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 El modelo seleccionado por select_best queda registrado en comparison.csv (columna 'is_selected' o nota textual) o en un JSON anexo outputs/reports/selected_model.json.
- [ ] #2 Las figuras PNG no se versionan si superan 1MB (alineado con .gitignore y política TDSP).
<!-- DOD:END -->
