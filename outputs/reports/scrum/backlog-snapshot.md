# Snapshot del backlog — laboratorio Dry Bean ML

**Fecha del snapshot:** 2026-05-15
**Procedencia:** generado a partir del frontmatter de [`backlog/tasks/`](../../../backlog/tasks/) y del Product Backlog en [`docs/product-backlog.md`](../../../docs/product-backlog.md). Los estados canónicos y asignaciones válidas están definidos en [`backlog/config.yml`](../../../backlog/config.yml).

Este archivo cumple la evidencia académica de backlog al cierre descrita en **TASK-17**.

---

## Product Backlog (PB-01..PB-06)

| ID | Título | Mapeo a TASK-* | Sprint estimado (referencia) |
|----|--------|----------------|-----------------------------|
| PB-01 | Datos Dry Bean disponibles y trazables | TASK-8, TASK-6 | 1 |
| PB-02 | Comprensión de datos y preparación | TASK-9, TASK-10 | 1–2 |
| PB-03 | Modelo baseline (regresión logística) | TASK-11 | 2 |
| PB-04 | Modelo alternativo (Random Forest) y despliegue mínimo | TASK-12, TASK-14 | 2 |
| PB-05 | Evaluación comparativa | TASK-13 | 2 |
| PB-06 | Documentación y reproducibilidad de entrega | TASK-15, TASK-16, TASK-18; TASK-17, TASK-19 | 3 |

---

## Backlog técnico (TASK-1..TASK-19)

Estado y responsable según archivos de tarea **al cierre del laboratorio** (todas las TASK en estado *Done*/*Hecho* en Backlog.md, alineadas con `backlog/tasks/` y [`backlog/config.yml`](../../../backlog/config.yml)).

| ID | Título | Estado (Backlog.md) | Asignado/a |
|----|--------|---------------------|-------------|
| TASK-1 | Analizar consignas (Lab1 y Scrum ML) y definir plan de alineación con estructura TDSP profesional en el repositorio | Hecho | Frank Daza |
| TASK-2 | Validar docs/tdsp-alineacion.md con docente y congelar estructura TDSP objetivo | Hecho | Frank Daza |
| TASK-3 | PR: Estructura TDSP física (carpetas, .gitkeep, .gitignore datos/modelos) | Hecho | Frank Daza |
| TASK-4 | Definir Product Backlog académico PB-01..PB-06 y roles Scrum ML | Hecho | Frank Daza |
| TASK-5 | Configurar entorno reproducible con UV (Python 3.12) y dependencias del laboratorio | Hecho | Juan Velasquez |
| TASK-6 | Documentar política de datos en data/raw/README.md y data/processed/README.md | Hecho | Yan Cuaran |
| TASK-7 | Estándares de calidad de código: ruff, black, pre-commit y nbstripout | Hecho | Frank Daza |
| TASK-8 | Implementar módulo src/data_loading.py con fetch_drybean() y pruebas unitarias | Hecho | Juan Velasquez |
| TASK-9 | Notebook de EDA notebooks/01_eda_drybean.ipynb (Dry Bean UCI 602) | Hecho | Yan Cuaran |
| TASK-10 | Implementar src/preprocessing.py: limpieza y partición train/test estratificada | Hecho | Juan Velasquez |
| TASK-11 | Modelo baseline: Pipeline(StandardScaler + LogisticRegression) en src/models/baseline.py | Hecho | Juan Velasquez |
| TASK-12 | Modelo alternativo RandomForestClassifier en src/models/random_forest.py | Hecho | Jenifer Ramos |
| TASK-13 | Evaluación comparativa, métricas y matriz de confusión en src/evaluation.py | Hecho | Jenifer Ramos |
| TASK-14 | Persistencia con joblib y función reutilizable de predicción en src/inference.py | Hecho | Jenifer Ramos |
| TASK-15 | Notebook integrador notebooks/01_laboratorio_drybean.ipynb (CRISP-DM end-to-end) | Hecho | Frank Daza |
| TASK-16 | Reporte breve de 7 secciones en outputs/reports/informe_laboratorio.md | Hecho | Juan Velasquez |
| TASK-17 | Evidencias Scrum ML en outputs/reports/scrum/ (tablero, sprints, retrospectiva) | Hecho | Frank Daza |
| TASK-18 | README final: sección de reproducibilidad y export de requirements.txt desde UV | Hecho | Yan Cuaran |
| TASK-19 | CI smoke test con GitHub Actions: lint, tests y ejecución del notebook | Hecho | Frank Daza |

**Resumen:** 19 tareas en **Hecho**, 0 en **Por hacer**: el laboratorio queda cerrado con núcleo ML, evidencias Scrum, README reproducible y pipeline de CI integrados.
