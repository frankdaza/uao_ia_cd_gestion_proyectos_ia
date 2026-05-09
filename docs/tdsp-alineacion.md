# Alineación consignas — TDSP académico vs TDSP profesional

**Proyecto:** laboratorio Dry Bean (UCI 602)  
**Fuentes:** `consignas/Lab1.pdf`, `consignas/Plan_Equipos_ScrumML_DryBean.pdf`, `README.md`, reglas y skills del repositorio.  
**Extracción de PDF:** texto extraído con `uv run --with pypdf` (páginas indicadas según el lector PDF; el documento Lab1 tiene **18** páginas, el plan de equipos **4**).

---

## 1. Inventario verificable de requisitos

| ID | Requisito (síntesis) | Fuente (archivo · página) | Tipo |
|----|----------------------|---------------------------|------|
| L1 | Objetivos: aplicar CRISP-DM, TDSP, Scrum ML; cargar datos reales; explorar, limpiar, modelar; evaluar; documentar como proyecto profesional | Lab1.pdf · p.1 | Metodología |
| L2 | Dataset Dry Bean UCI 602; variable objetivo `Class`; contexto de negocio simulado | Lab1.pdf · p.2 | Datos / negocio |
| L3 | CRISP-DM en 6 fases (negocio, datos, preparación, modelado, evaluación, despliegue) | Lab1.pdf · p.2 | Metodología |
| L4 | TDSP: estructura de repo, trazabilidad de experimentos, versionado datos/código/modelos, documentación, reproducibilidad | Lab1.pdf · p.2–3 | TDSP / estructura |
| L5 | Scrum ML: roles (PO, SM, equipo), backlog, sprints, Definition of Done | Lab1.pdf · p.3 | Scrum |
| L6 | **Estructura de carpetas obligatoria:** `data/raw`, `data/processed`, `notebooks`, `outputs/models`, `outputs/reports`, `src`, `README.md` (raíz ejemplo `laboratorio_drybean_ml/`) | Lab1.pdf · p.3 | Estructura |
| L7 | Backlog sugerido: historias (carga datos, calidad, baseline LR, RF, matriz/reporte, joblib) con criterios de aceptación | Lab1.pdf · p.3–4 | Scrum / ML |
| L8 | Sprints 1–2 con entregables explícitos (EDA, train/test, pipeline; baseline, RF, métricas, modelo guardado) | Lab1.pdf · p.4 | Scrum / ML |
| L9 | Entorno: consigna muestra `venv` + `pip install pandas numpy matplotlib scikit-learn ucimlrepo joblib openpyxl` | Lab1.pdf · p.4 | Entorno |
| L10 | Artefactos de trabajo: `notebooks/01_laboratorio_drybean.ipynb` o `src/laboratorio_drybean.py` | Lab1.pdf · p.4 | Estructura |
| L11 | Carga con `fetch_ucirepo(id=602)`; EDA; nulos y duplicados; `drop_duplicates` si aplica; análisis de `Class` | Lab1.pdf · p.5–8 | ML |
| L12 | Partición train/test; `Pipeline` + `StandardScaler` + `LogisticRegression`; `RandomForestClassifier`; accuracy y **F1 macro**; matriz de confusión | Lab1.pdf · p.8+ (pasos intermedios) | ML |
| L13 | Persistencia: `joblib` bajo `outputs/models/` (ej. `random_forest_drybean.joblib`); carga y predicción de prueba | Lab1.pdf · p.14–15 | TDSP / ML |
| L14 | Mini despliegue: función reutilizable de predicción (vínculo fase despliegue CRISP-DM) | Lab1.pdf · p.14–15 | ML / despliegue |
| L15 | **Entregables:** notebook ejecutado (carga, EDA, limpieza, modelos, evaluación, conclusiones); reporte breve en **7 secciones**; evidencias Scrum (backlog, tablero Por hacer / En progreso / Hecho, tareas por sprint, retrospectiva 3 puntos) | Lab1.pdf · p.15–16 | Entrega / Scrum |
| L16 | **Definition of Done** del laboratorio (9 ítems: notebook sin errores, dataset, nulos/duplicados, baseline+alternativo, accuracy+F1 macro, matriz, modelo guardado, interpretación, vínculo CRISP-DM/TDSP/Scrum ML) | Lab1.pdf · p.16 | DoD |
| L17 | Rúbrica: CRISP-DM 20, TDSP 15, Scrum ML 15, código 20, evaluación 15, interpretación 15 | Lab1.pdf · p.16 | Evaluación |
| L18 | Git colaborativo implícito en trabajo en equipo (no detallado en Lab1 como en el plan de equipos) | Lab1.pdf · implícito | Git |
| P1 | Equipo ~4 personas; roles PO, SM, Data Engineer/Analyst, ML Engineer con entregables | Plan_Equipos · p.1 | Scrum / organización |
| P2 | Misma **estructura TDSP** que Lab1 + `requirements.txt` + `.gitignore` | Plan_Equipos · p.1 | Estructura |
| P3 | Product backlog PB-01…PB-06 (dataset, calidad, LR, RF, métricas, README) | Plan_Equipos · p.2 | Scrum |
| P4 | Sprints 1–3 (comprensión, modelado, despliegue/doc) con tareas y entregables | Plan_Equipos · p.2–3 | Scrum |
| P5 | Flujo GitHub: repo, `git init`, estructura TDSP, `push`, colaboradores, `feature/*`, PR, revisión antes de merge | Plan_Equipos · p.3 | Git |
| P6 | DoD: notebook sin errores, dataset OK, baseline y alternativo, accuracy y F1 macro, matriz de confusión, documentación reproducible | Plan_Equipos · p.4 | DoD |

---

## 2. Requisito → ubicación o artefacto en el repositorio (propuesta)

| Ref. | Requisito | Artefacto / ruta propuesta |
|------|-----------|----------------------------|
| L6, P2 | Árbol TDSP | Crear en la raíz del repo (el nombre puede no ser `laboratorio_drybean_ml/`; importa la **forma** del árbol): `data/raw/`, `data/processed/`, `notebooks/`, `outputs/models/`, `outputs/reports/`, `src/`. Opcional: `docs/` para informes de alineación y metodología (`docs/tdsp-alineacion.md`). |
| L6 | README en raíz | Ya existe `README.md`; mantenerlo como **punto de entrada** y reflejar estructura real cuando existan carpetas. |
| P2 | `requirements.txt` | **Conflicto con política del repo (UV).** Ver sección 5. Recomendación: `pyproject.toml` + `uv.lock` como fuente de verdad; si el docente exige `requirements.txt`, generarlo con `uv export` o equivalente en CI/script. |
| P2 | `.gitignore` | Ya existe; revisar exclusiones para `data/raw/*` y modelos grandes según política del equipo. |
| L10 | Notebook o script | `notebooks/01_laboratorio_drybean.ipynb` y/o `src/laboratorio_drybean.py` (crear al implementar Lab1). |
| L13 | Modelo joblib | `outputs/models/*.joblib` (p. ej. `random_forest_drybean.joblib`). |
| L15 | Reporte 7 secciones | `outputs/reports/informe_laboratorio.md` o PDF exportado desde notebook; o sección en README enlazada. |
| L15 | Evidencias Scrum | `docs/scrum/` o `outputs/reports/scrum/` con capturas/export del tablero (Backlog.md, GitHub Projects, etc.) + actas de retrospectiva. |
| L7, P3 | Backlog de producto | **Backlog.md** en `backlog/tasks/` (ya en uso) + opcional tabla PB-01… en `docs/product-backlog.md` para entrega académica. |
| P5 | Ramas y PR | Flujo ya descrito en `README.md` / `AGENTS.md`: `feature/*`, PR, revisión. |

---

## 3. TDSP académico (repo actual) vs TDSP profesional (industria)

**TDSP académico (consignas + README actual):**  
Carpetas fijas para datos crudos/procesados, experimentación en notebooks, salidas de modelos y reportes, código reutilizable en `src/`. Énfasis en **reproducibilidad básica** (joblib, rutas claras) y documentación en README + reporte breve.

**TDSP profesional (Microsoft / equipos de datos maduros):**  
Además del árbol: **ciclo de vida explícito** (charter o problema de negocio versionado, especificación de datos, informes de seguridad/privacidad cuando aplique), **control de versiones de datos** (DVC, lakehouse o al menos hashes/README de versiones), **experiment tracking** (MLflow, Weights & Biases o tabla en `outputs/reports/experiments.md`), **revisión por pares** formalizada, **CI** (tests de smoke del notebook o script), **contrato de inferencia** y **checklist de despliegue** aunque el “despliegue” sea solo una demo.

**Recomendación para el curso (esfuerzo vs valor):**  
Mantener el **árbol TDSP de las consignas** como núcleo (cumple L6 y rúbrica TDSP). Añadir solo prácticas “profesionales livianas”: (1) `docs/` con este análisis y actas Scrum; (2) convención de nombres de experimentos y rutas en `outputs/reports/`; (3) ramas `feature/*` + PR ya alineadas con P5; (4) si el curso lo permite, un `README` de sección “Trazabilidad” con tabla fecha–commit–cambio relevante. **No** imponer DVC/MLflow salvo extensión opcional del curso.

---

## 4. Lista priorizada de historias / PRs (implementación)

| Prioridad | Historia / PR | Dependencias | Notas |
|-----------|---------------|----------------|-------|
| P0 | PR “Estructura TDSP física”: carpetas + `.gitkeep` donde haga falta + alinear `.gitignore` con datos/modelos | Ninguna | **Hecho (2026-05-09):** carpetas TDSP + `.gitkeep`; `.gitignore` activo para `data/*` y `outputs/models/*` con excepción `.gitkeep`. Ver tarea **TASK-3**. |
| P1 | PR “Entorno reproducible UV”: `pyproject.toml` + `uv.lock` con dependencias del Lab1; documentar comando único `uv sync` | P0 opcional | Resuelve discrepancia L9 vs política repo; ofrecer export a `requirements.txt` si se exige entrega literal. |
| P2 | PR “Notebook o script mínimo ejecutable”: carga UCI 602, EDA breve, train/test | P1 | Cierra PB-01, PB-02 parcialmente. |
| P3 | PR “Modelado”: baseline + RF + métricas + matriz + joblib | P2 | PB-03, PB-04, PB-05. |
| P4 | PR “Documentación y Scrum”: reporte 7 secciones + carpeta evidencias Scrum | P3 | PB-06 + entregables L15. |
| P5 | Tarea Backlog: “Validación docente de `docs/tdsp-alineacion.md` y congelación de estructura objetivo” | Este documento | Cierra el hueco de “acuerdo explícito” del plan de trabajo TASK-1. |

---

## 5. Revisión cruzada (README / AGENTS / reglas vs consignas)

| Hallazgo | Severidad | Acción correctiva |
|----------|-----------|-------------------|
| Lab1 **p.4** prescribe `python -m venv` y **pip**; el repo exige **UV** (`AGENTS.md`, `README.md`, reglas). | Media | Mantener **UV** como estándar del repositorio. En README o `docs/`, añadir nota: *“La consigna muestra venv/pip como referencia pedagógica; en este repo se usa UV para reproducibilidad del equipo.”* Opcional: script `uv export -o requirements.txt` para quien deba entregar `requirements.txt` (Plan_Equipos P2). |
| Plan de equipos lista **`requirements.txt`**; el proyecto usa **`pyproject.toml` + `uv.lock`**. | Baja | Igual que arriba: declarar equivalencia o generar `requirements.txt` desde UV en entrega. |
| Nombre raíz `laboratorio_drybean_ml/` en PDF vs nombre real del repo Git. | Baja | Ningún cambio obligatorio; documentar equivalencia de estructura. |
| README ya incluye **`consignas/`** (no está en el árbol mínimo del PDF); es coherente con el curso. | Ninguna | Mantener. |
| Políticas de ML (baseline, RF, F1 macro, joblib) en reglas/skill **coinciden** con Lab1. | Ninguna | Mantener sincronización según `AGENTS.md`. |

---

## 6. Gap analysis (estado del repo al cierre de este análisis)

| Elemento | Estado | Comentario |
|----------|--------|------------|
| `README.md` con árbol TDSP | Documentado + congelado v1.0 | Enlaza a `tdsp-estructura-congelada.md` (TASK-2). |
| `data/raw`, `data/processed`, `notebooks`, `outputs/models`, `outputs/reports`, `src` | **Resuelto (2026-05-09)** | Carpetas creadas con `.gitkeep`; `.gitignore` alineado (TASK-3 / P0). |
| `pyproject.toml` / `uv.lock` | Ausente al momento del análisis | Abordar PR P1. |
| Notebook / script Lab1 | Pendiente | PB-01 en adelante. |
| Evidencias Scrum en repo | Parcial (Backlog.md operativo) | Añadir artefactos para entrega L15. |

---

## 7. Cierre TASK-1 y validación TASK-2

- **Entregable principal (TASK-1):** [tdsp-alineacion.md](tdsp-alineacion.md).  
- **Congelación y validación (TASK-2):** [tdsp-estructura-congelada.md](tdsp-estructura-congelada.md) (v1.0) y [tdsp-validacion-acuerdo.md](tdsp-validacion-acuerdo.md) (acuerdo del equipo; bloque docente opcional).  
- **Fecha de análisis (TASK-1):** 2026-05-09.  
- **Fecha de congelación (TASK-2):** 2026-05-09.
