# Estructura TDSP congelada — laboratorio Dry Bean

**Versión:** 1.0
**Fecha de congelación:** 2026-05-09
**Base normativa:** `consignas/Lab1.pdf`, `consignas/Plan_Equipos_ScrumML_DryBean.pdf`, [tdsp-alineacion.md](tdsp-alineacion.md).
**Estado:** vigente para este repositorio hasta que se publique una versión 1.x o 2.0 en este mismo directorio.

---

## 1. Árbol obligatorio (paths relativos a la raíz del repo)

```text
consignas/              # PDFs de consignas (no sustituir por enlaces externos sin acuerdo)
docs/                   # Análisis, acuerdos y estructura congelada (este documento)
data/
├── raw/                # Datos sin procesar (no versionar binarios; solo .gitkeep o README explicativo)
└── processed/          # Datos limpios o transformados (misma política de no versionar pesados)
notebooks/              # Jupyter de exploración y laboratorio
outputs/
├── models/             # Artefactos .joblib / serializados (ignorados por Git salvo .gitkeep)
└── reports/            # Figuras, CSV de predicciones, tablas exportadas
src/                    # Código Python importable o scripts
README.md               # Punto de entrada del proyecto
```

**Extensiones del curso ya alineadas en el repo (no obligatorias en el PDF mínimo, pero presentes):**

- `backlog/` — gestión de tareas con Backlog.md.
- `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/` — guías para asistentes y políticas del equipo.

---

## 2. Archivos mínimos por carpeta de datos y salidas

| Ruta | Qué versionar en Git |
|------|----------------------|
| `data/raw/` | `.gitkeep` (y opcionalmente `README.md` local con instrucciones de descarga). |
| `data/processed/` | `.gitkeep` (misma convención). |
| `outputs/models/` | `.gitkeep` únicamente; los modelos se generan en el entorno local o CI. |
| `outputs/reports/` | `.gitkeep` y archivos livianos que el equipo decida versionar (p. ej. figuras pequeñas). |

La política de exclusión en `.gitignore` está descrita en [tdsp-alineacion.md](tdsp-alineacion.md) y aplicada en el repositorio (P0 / TASK-3).

---

## 3. Política de entorno (congelada para este repo)

- **Gestor de dependencias:** UV (`pyproject.toml` + `uv.lock` cuando existan).
- **No** usar como flujo predeterminado `pip` ni `python -m venv` en la documentación interna del repositorio.
- La consigna del Lab1 muestra `venv`/`pip` como referencia pedagógica; la **interpretación oficial del equipo** es mantener UV y documentar la equivalencia (ver [tdsp-alineacion.md §5](tdsp-alineacion.md)).
- Si el docente exige entregar `requirements.txt`, generarlo desde UV (`uv export`) sin sustituir `pyproject.toml` como fuente de verdad.

---

## 4. Artefactos de trabajo obligatorios (curso)

| Artefacto | Ubicación acordada |
|-----------|-------------------|
| Notebook principal sugerido por consigna | `notebooks/01_laboratorio_drybean.ipynb` (nombre puede ajustarse si el docente lo indica; mantener bajo `notebooks/`). |
| Script alternativo | `src/laboratorio_drybean.py` (opcional si el equipo usa solo notebook). |
| Modelo serializado ejemplo | `outputs/models/*.joblib` (p. ej. `random_forest_drybean.joblib`). |

---

## 5. Historial de versiones

| Versión | Fecha | Cambio |
|---------|-------|--------|
| 1.0 | 2026-05-09 | Primera congelación tras TASK-2; incorpora estructura física P0 (TASK-3) y análisis TASK-1. |
