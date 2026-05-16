---
id: TASK-15
title: >-
  Notebook integrador notebooks/01_laboratorio_drybean.ipynb (CRISP-DM
  end-to-end)
status: Done
assignee:
  - Frank Daza
created_date: '2026-05-09 18:44'
updated_date: '2026-05-16 03:59'
labels: []
dependencies:
  - TASK-14
references:
  - consignas/Lab1.pdf
  - .cursor/skills/drybean-ml-laboratorio/SKILL.md
  - docs/tdsp-alineacion.md
documentation:
  - notebooks/01_laboratorio_drybean.ipynb
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Producir el **entregable principal del laboratorio** (L10, L15): un notebook único que orquesta CRISP-DM de inicio a fin reutilizando los módulos `src/`. Este notebook es el artefacto que el docente ejecuta y revisa, y la fuente desde la cual se exporta el reporte (TASK-16).

## Alcance

1. Crear `notebooks/01_laboratorio_drybean.ipynb` con secciones numeradas alineadas a CRISP-DM:
   - **1. Comprensión del negocio** — problema, objetivo, métrica primaria (F1 macro).
   - **2. Comprensión de datos** — `fetch_drybean`, EDA resumido (shape, balance de Class, hallazgos).
   - **3. Preparación de datos** — `clean` y `split` desde `src/preprocessing.py`.
   - **4. Modelado** — entrenar baseline (TASK-11) y Random Forest (TASK-12) reusando `build_*_pipeline`.
   - **5. Evaluación** — `compare_models`, `plot_confusion_matrix`, `save_classification_report`.
   - **6. Despliegue** — `save_model`, `load_model` y predicción de prueba (TASK-14).
   - **7. Scrum ML** — backlog usado, tablero, retrospectiva resumen, vínculo a evidencias (TASK-17).
2. Incluir Markdown narrativo entre celdas explicando decisiones (split estratificado, métrica elegida, etc.).
3. Validar que el notebook ejecuta de inicio a fin con `uv run jupyter nbconvert --to notebook --execute`.

## Fuera de alcance

- Reporte separado en Markdown (TASK-16).
- Evidencias Scrum exportadas (TASK-17).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 notebooks/01_laboratorio_drybean.ipynb existe con las 7 secciones nombradas según CRISP-DM + Scrum ML.
- [ ] #2 uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01_laboratorio_drybean.ipynb termina con código 0.
- [ ] #3 El notebook reutiliza funciones de src/data_loading, src/preprocessing, src/models, src/evaluation y src/inference (no duplica lógica).
- [ ] #4 Reporta accuracy y F1 macro de ambos modelos y muestra la matriz de confusión del modelo seleccionado.
- [ ] #5 Incluye una predicción de prueba cargando el modelo desde outputs/models/random_forest_drybean.joblib.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear notebooks/01_laboratorio_drybean.ipynb basado en plantilla del SKILL drybean.
2. Importar funciones desde src/ en la primera celda de código.
3. Llenar cada sección reutilizando los módulos.
4. Insertar Markdown explicativo entre secciones (decisiones de modelado, lectura de la matriz de confusión, etc.).
5. Validar ejecución end-to-end con jupyter nbconvert --execute.
6. Confirmar que nbstripout deja el .ipynb limpio antes de commit.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Este notebook es la fuente de evidencia principal para el docente. Mantenerlo legible: celdas cortas, Markdown narrativo, salidas relevantes. Si surge tensión entre 01_eda_drybean.ipynb (TASK-9) y este integrador, mantener ambos: el primero es exploratorio, el segundo es la entrega oficial.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Las salidas binarias pesadas quedan stripeadas por nbstripout (TASK-7) salvo figuras pequeñas embebidas.
- [ ] #2 El notebook está listo para ser ejecutado por el docente en una instalación limpia tras uv sync.
<!-- DOD:END -->
