# Product Backlog académico (PB-01..PB-06)

Historias de producto del laboratorio **Dry Bean** (UCI id **602**), alineadas con el plan de equipos ([`consignas/Plan_Equipos_ScrumML_DryBean.pdf`](../consignas/Plan_Equipos_ScrumML_DryBean.pdf), requisito **P3**) y con el inventario de consignas en [`docs/tdsp-alineacion.md`](tdsp-alineacion.md) (fila **P3**: dataset, calidad, LR, RF, métricas, README).

El desglose operativo en tareas técnicas está en [`backlog/tasks/`](../backlog/tasks/) (**TASK-1** a **TASK-19**), gestionadas con Backlog.md y [`backlog/config.yml`](../backlog/config.yml).

## Historias de producto

| ID | Título | Descripción | Criterios de aceptación (verificables) | Mapeo a TASK-* | Sprint estimado |
|----|--------|-------------|----------------------------------------|----------------|-----------------|
| PB-01 | Datos Dry Bean disponibles y trazables | El conjunto UCI 602 se obtiene de forma reproducible y queda documentada la procedencia en el repositorio. | Carga con `fetch_ucirepo(id=602)` (o flujo equivalente documentado); políticas de `data/raw` y `data/processed` aclaran qué se versiona; código reutilizable en `src/` con pruebas donde aplique. | TASK-8, TASK-6 | 1 |
| PB-02 | Comprensión de datos y preparación | EDA sobre forma del dataset, nulos, duplicados y `Class`; partición train/test estratificada y limpieza acorde a la consigna. | Notebook o flujo de EDA ejecutable; reporte de nulos y duplicados; `train_test_split` con `stratify` respecto a `Class` documentado. | TASK-9, TASK-10 | 1–2 |
| PB-03 | Modelo baseline (regresión logística) | Pipeline con escalado y regresión logística como referencia inferior reproducible. | `Pipeline` con `StandardScaler` + `LogisticRegression`; hiperparámetros fijos y reproducibles (`random_state`, etc.); código en `src/`. | TASK-11 | 2 |
| PB-04 | Modelo alternativo (Random Forest) y despliegue mínimo | Modelo de árboles contrastado con el baseline; persistencia e inferencia reproducible. | `RandomForestClassifier` entrenado y documentado; modelo serializado con `joblib` bajo `outputs/models/`; función o API mínima de predicción en `src/`. | TASK-12, TASK-14 | 2 |
| PB-05 | Evaluación comparativa | Comparación cuantitativa entre baseline y alternativo acorde a la rúbrica. | **Accuracy** y **F1 macro**; matriz de confusión e informe por clase; artefactos exportados bajo `outputs/reports/` cuando aplique. | TASK-13 | 2 |
| PB-06 | Documentación y reproducibilidad de entrega | Cierre narrativo del laboratorio: reporte, README, notebook integrador y apoyo a evidencias Scrum / CI. | Reporte breve en 7 secciones (CRISP-DM + Scrum); README con flujo UV; notebook integrador enlazado; mecanismo para `requirements.txt` si se exige entrega literal; evidencias Scrum y CI según TASK-17 y TASK-19. | TASK-15, TASK-16, TASK-18; TASK-17, TASK-19 | 3 |

## Notas de trazabilidad

- Las historias **PB-01..PB-06** no sustituyen las tareas **TASK-***: las TASK incluyen también trabajo de infraestructura (estructura TDSP, alineación consignas, estándares de código, etc.) que soporta el producto pero no mapea 1:1 a una sola historia PB.
- Roles Scrum ML: [`docs/scrum/roles.md`](scrum/roles.md).
