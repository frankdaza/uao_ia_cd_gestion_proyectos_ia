# Tablero Scrum ML — evidencia de cierre

**Fecha:** 2026-05-15
**Proyecto:** laboratorio drybean ml (Backlog.md)

Convención de columnas (según [`docs/scrum/tablero.md`](../../../docs/scrum/tablero.md)):

Los valores de estado provienen de [`backlog/config.yml`](../../../backlog/config.yml) y se agrupan en tres columnas: **Por hacer**, **En progreso** y **Hecho** (detalle en [`docs/scrum/tablero.md`](../../../docs/scrum/tablero.md)).

Estado **tras completar TASK-17**: no quedan tareas en *En progreso*; las tareas abiertas son únicamente cierre de documentación (TASK-18) y CI (TASK-19).

---

## Por hacer

- **TASK-18** — README final: sección de reproducibilidad y export de `requirements.txt` desde UV — *Yan Cuaran*
- **TASK-19** — CI smoke test con GitHub Actions: lint, tests y ejecución del notebook — *Frank Daza*

## En progreso

*(Sin tareas: al registrar esta evidencia no hay trabajo en curso sin cerrar.)*

## Hecho

- **TASK-1** — Analizar consignas (Lab1 y Scrum ML) y plan TDSP — *Frank Daza*
- **TASK-2** — Validar `docs/tdsp-alineacion.md` y congelar estructura TDSP — *Frank Daza*
- **TASK-3** — Estructura TDSP física — *Frank Daza*
- **TASK-4** — Product Backlog PB-01..PB-06 y roles Scrum ML — *Frank Daza*
- **TASK-5** — Entorno UV y Python 3.12 — *Juan Velasquez*
- **TASK-6** — Política de datos en `data/raw` y `data/processed` — *Yan Cuaran*
- **TASK-7** — Ruff, Black, pre-commit y nbstripout — *Frank Daza*
- **TASK-8** — `src/data_loading.py` y pruebas — *Juan Velasquez*
- **TASK-9** — Notebook EDA — *Yan Cuaran*
- **TASK-10** — `src/preprocessing.py` — *Juan Velasquez*
- **TASK-11** — Baseline regresión logística — *Juan Velasquez*
- **TASK-12** — Random Forest — *Jenifer Ramos*
- **TASK-13** — Evaluación comparativa — *Jenifer Ramos*
- **TASK-14** — Persistencia e inferencia — *Jenifer Ramos*
- **TASK-15** — Notebook integrador CRISP-DM — *Frank Daza*
- **TASK-16** — Informe de 7 secciones — *Juan Velasquez*
- **TASK-17** — Evidencias Scrum en `outputs/reports/scrum/` — *Frank Daza*

---

*Nota:* Para regenerar una vista tipo Kanban desde la CLI del proyecto, ver `backlog board view` y `backlog board export` en la guía del repositorio.
