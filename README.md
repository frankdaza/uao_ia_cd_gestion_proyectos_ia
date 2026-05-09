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

La siguiente organización es la esperada a medida que avance el laboratorio; algunas carpetas pueden crearse cuando el equipo empiece a cargar datos, notebooks y código.

```text
├── consignas/            # Consignas y plan de equipos (PDF)
├── docs/                 # Análisis y documentación de apoyo (p. ej. alineación TDSP)
├── data/
│   ├── raw/              # Datos sin procesar
│   └── processed/        # Datos limpios o transformados
├── notebooks/            # Exploración y experimentos en Jupyter
├── outputs/
│   ├── models/           # Modelos persistidos (joblib)
│   └── reports/          # Figuras, tablas o reportes exportados
├── src/                  # Código Python reutilizable
├── AGENTS.md             # Guía para asistentes de código y sincronización de políticas
├── CLAUDE.md             # Instrucciones para Claude Code
└── pyproject.toml        # Dependencias con UV (cuando el proyecto las declare)
```

## Requisitos y entorno

- **Python 3.12**
- **UV** (Astral) para dependencias y entorno virtual

Comandos de referencia:

```bash
uv python pin 3.12
uv sync
uv add <paquete>
uv run python src/<script>.py
uv run jupyter lab
```

La lista concreta de paquetes debe alinearse con `pyproject.toml` y `uv.lock` cuando existan en el repositorio. El proyecto recomienda evitar `pip install` y `python -m venv` como flujo predeterminado.

## Consignas y plan de equipo

- [consignas/Lab1.pdf](consignas/Lab1.pdf)
- [consignas/Plan_Equipos_ScrumML_DryBean.pdf](consignas/Plan_Equipos_ScrumML_DryBean.pdf)
- [docs/tdsp-alineacion.md](docs/tdsp-alineacion.md) — inventario de requisitos de las consignas, mapeo al repositorio y comparación TDSP académico vs profesional (entregable TASK-1).

## Colaboración en Git

Uso de ramas `feature/<nombre>`, integración mediante **pull requests** y revisión antes de fusionar a la rama principal.

## Referencias

- Dataset Dry Bean (UCI, id 602): [https://archive.ics.uci.edu/dataset/602/dry+bean+dataset](https://archive.ics.uci.edu/dataset/602/dry+bean+dataset)
- Políticas del repositorio para asistentes de código: [AGENTS.md](AGENTS.md)
