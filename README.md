# Laboratorio de Machine Learning — Dry Bean

Proyecto académico de **clasificación multiclase** sobre el **Dry Bean Dataset** del UCI Machine Learning Repository (id **602**). La variable objetivo es la columna **`Class`**. El trabajo integra prácticas de **CRISP-DM**, **Team Data Science Process (TDSP)** y **Scrum ML**, en línea con la gestión colaborativa de proyectos de ciencia de datos e inteligencia artificial.

## Metodología y flujo técnico

- Exploración de datos (EDA): forma del conjunto, valores nulos, duplicados y distribución de clases.
- Partición **train/test** estratificada respecto a la variable objetivo (p. ej. `test_size=0.2`, `random_state=42`, salvo otra justificación documentada).
- **Modelo baseline**: `Pipeline` con `StandardScaler` y `LogisticRegression` (p. ej. `max_iter=1000`, `random_state=42`).
- **Modelo alternativo**: `RandomForestClassifier` con hiperparámetros razonables y documentados.
- **Evaluación**: accuracy, **F1 macro** (`average="macro"`), informe de clasificación y **matriz de confusión**.
- **Persistencia**: guardar el modelo final con **`joblib`** bajo `outputs/models/` (p. ej. extensión `.joblib`).

Para un checklist de entrega (Definition of Done), evidencias de Scrum ML y plantillas breves, consultá el skill del repositorio en `.cursor/skills/drybean-ml-laboratorio/SKILL.md` y las consignas en PDF enlazadas más abajo.

## Estructura del proyecto (TDSP)

La organización sigue las consignas (Lab1 y plan de equipos). La **versión congelada** de referencia (obligatorios, política de Git y entorno) está en [docs/tdsp-estructura-congelada.md](docs/tdsp-estructura-congelada.md). El registro de validación del equipo y el espacio para el docente están en [docs/tdsp-validacion-acuerdo.md](docs/tdsp-validacion-acuerdo.md).

```text
├── consignas/            # Consignas y plan de equipos (PDF)
├── docs/                 # Análisis y documentación de apoyo (p. ej. alineación TDSP)
├── data/
│   ├── raw/              # Datos sin procesar
│   └── processed/        # Datos limpios o transformados
├── notebooks/            # Exploración y experimentos en Jupyter
├── scripts/              # Utilidades (p. ej. export de requirements.txt)
├── outputs/
│   ├── models/           # Modelos persistidos (joblib)
│   └── reports/          # Figuras, tablas o reportes exportados
├── src/                  # Código Python reutilizable
├── AGENTS.md             # Guía para asistentes de código y sincronización de políticas
├── CLAUDE.md             # Instrucciones para Claude Code
├── pyproject.toml        # Metadatos del proyecto y dependencias (UV)
└── uv.lock               # Versiones resueltas (reproducibilidad con uv sync)
```

## Requisitos y entorno

- **Python 3.12**
- **UV** (Astral) instalado y disponible en el PATH para dependencias y entorno virtual

## Cómo correr el laboratorio

Desde la **raíz del repositorio**, con los requisitos anteriores:

```bash
uv sync
uv run pre-commit install
uv run pytest
uv run jupyter lab notebooks/01_laboratorio_drybean.ipynb
uv run python -m src.inference
```

- `uv sync` crea o actualiza `.venv` y alinea el entorno con `uv.lock`.
- `src.inference` entrena un modelo de ejemplo, lo guarda bajo `outputs/models/` y muestra una predicción de verificación (los datos deben poder obtenerse según la política en `data/raw` y `src/data_loading.py`).

> **Nota:** no usar `pip install` ni `python -m venv` como flujo predeterminado del equipo.

### Reproducibilidad y `requirements.txt`

La **fuente de verdad** de las dependencias es **`pyproject.toml`** y el archivo de lock **`uv.lock`** (reproducibilidad con `uv sync`).

El archivo **`requirements.txt`** no se versiona: es un **artefacto derivado** para quien deba entregarlo explícitamente (p. ej. consigna académica). Generalo bajo demanda:

```bash
bash scripts/export_requirements.sh
```

Equivale a `uv export --no-hashes --format requirements-txt -o requirements.txt` en la raíz del repo. Si necesitás solo dependencias de **runtime** (sin herramientas de desarrollo del grupo `dev`), podés ejecutar manualmente el mismo comando añadiendo `--no-dev`.

## Calidad de código

El repositorio usa **Ruff** (lint), **Black** (formato), **nbstripout** (evita versionar salidas pesadas en `.ipynb`) y **pre-commit** (hooks de Git). La configuración vive en `pyproject.toml` y `.pre-commit-config.yaml`.

La instalación inicial de hooks está en la sección **Cómo correr el laboratorio**. Para correr todos los hooks sobre el árbol completo (útil antes de abrir un PR):

```bash
uv run pre-commit run --all-files
```

Sin instalar hooks, podés usar `uv run ruff check .` o `uv run black --check .` de forma puntual.

## Consignas y plan de equipo

- [consignas/Lab1.pdf](consignas/Lab1.pdf)
- [consignas/Plan_Equipos_ScrumML_DryBean.pdf](consignas/Plan_Equipos_ScrumML_DryBean.pdf)
- [docs/tdsp-alineacion.md](docs/tdsp-alineacion.md) — inventario de requisitos de las consignas, mapeo al repositorio y comparación TDSP académico vs profesional (entregable TASK-1).
- [docs/tdsp-estructura-congelada.md](docs/tdsp-estructura-congelada.md) — estructura TDSP **v1.0 congelada** (TASK-2).
- [docs/tdsp-validacion-acuerdo.md](docs/tdsp-validacion-acuerdo.md) — acuerdo del equipo y plantilla para el docente (TASK-2).

### Scrum ML y backlog de producto

- [docs/product-backlog.md](docs/product-backlog.md) — historias **PB-01..PB-06** y mapeo a tareas **TASK-***
- [docs/scrum/roles.md](docs/scrum/roles.md) — roles del equipo (PO, SM, Data Engineer/Analyst, ML Engineer)
- [docs/scrum/plantilla-retrospectiva.md](docs/scrum/plantilla-retrospectiva.md) — plantilla de retrospectiva (tres bloques)
- [docs/scrum/tablero.md](docs/scrum/tablero.md) — columnas Por hacer / En progreso / Hecho y exportación del tablero

## Colaboración en Git

Uso de ramas `feature/<nombre>`, integración mediante **pull requests** y revisión antes de fusionar a la rama principal.

## Referencias

- Dataset Dry Bean (UCI, id 602): [https://archive.ics.uci.edu/dataset/602/dry+bean+dataset](https://archive.ics.uci.edu/dataset/602/dry+bean+dataset)
- Políticas del repositorio para asistentes de código: [AGENTS.md](AGENTS.md)
