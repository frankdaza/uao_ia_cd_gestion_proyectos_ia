# Instrucciones del proyecto — Claude Code

## Idioma

Todo comentario en código, docstrings, mensajes de commit, descripciones de PR, `README.md` y documentación del repositorio debe redactarse en **español latinoamericano**, con tono profesional y neutro.

## Python y herramientas

- **Python 3.12** como versión objetivo del proyecto.
- **UV** (Astral) es el gestor de paquetes y entornos: mantener `pyproject.toml` y `uv.lock`; usar `uv python pin 3.12`, `uv sync`, `uv add` y `uv run`. No usar `pip` ni `python -m venv` como flujo predeterminado.

## Contexto académico — Dry Bean ML

Laboratorio de **clasificación** con el **Dry Bean Dataset** (UCI, id **602**), aplicando **CRISP-DM**, **TDSP** y **Scrum ML**. Variable objetivo: **`Class`**. Estructura tipo TDSP con `data/raw`, `data/processed`, `notebooks`, `outputs/models`, `outputs/reports`, `src`.

Flujo esperado: EDA; partición train/test estratificada; baseline con `Pipeline` (`StandardScaler` + `LogisticRegression`); alternativa con `RandomForestClassifier`; **accuracy** y **F1 macro**; matriz de confusión; persistencia con **`joblib`**. Trabajo colaborativo con ramas `feature/*` y pull requests.

Consignas en [consignas/Lab1.pdf](consignas/Lab1.pdf) y [consignas/Plan_Equipos_ScrumML_DryBean.pdf](consignas/Plan_Equipos_ScrumML_DryBean.pdf).

## Cursor

- Reglas: [.cursor/rules/](.cursor/rules/)
- Skill detallado: [.cursor/skills/drybean-ml-laboratorio/SKILL.md](.cursor/skills/drybean-ml-laboratorio/SKILL.md)

## Tareas Backlog.md

Al crear o editar ítems de gestión en el repositorio, seguir el skill [.cursor/skills/backlog-md-tareas/SKILL.md](.cursor/skills/backlog-md-tareas/SKILL.md) y la configuración [backlog/config.yml](backlog/config.yml).

## Sincronización entre herramientas de IA

Al agregar, quitar o cambiar políticas (idioma, Python, UV, metodología del laboratorio, estándares de tareas Backlog), actualizar **Cursor** (`.cursor/rules/` y los skills afectados), **esta guía** (`CLAUDE.md`) y **[.github/copilot-instructions.md](.github/copilot-instructions.md)**. La lista canónica y el procedimiento están en [AGENTS.md](AGENTS.md).
