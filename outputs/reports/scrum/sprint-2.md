# Sprint 2 — Preparación de datos, modelado y evaluación

**Ventana estimada:** 2026-05-12 a 2026-05-14
**Objetivo:** partición estratificada, baseline logístico, Random Forest, métricas de rúbrica y persistencia para despliegue mínimo.

## Tareas planificadas (TASK-*)

| Tarea | Responsable | Estado al cierre |
|-------|-------------|------------------|
| TASK-10 | Juan Velasquez | Completada |
| TASK-11 | Juan Velasquez | Completada |
| TASK-12 | Jenifer Ramos | Completada |
| TASK-13 | Jenifer Ramos | Completada |
| TASK-14 | Jenifer Ramos | Completada |

## Observaciones

- Los modelos se encapsularon en **`Pipeline`** para evitar fuga de datos; la evaluación (**TASK-13**) consolidó **accuracy**, **F1 macro**, matriz de confusión e informe por clase.
- **TASK-14** cerró el ciclo PB-04 con serialización `joblib` y API mínima de predicción en `src/inference.py`.
- Se mantuvo trazabilidad con PB-03, PB-04 y PB-05 del [`docs/product-backlog.md`](../../../docs/product-backlog.md).
