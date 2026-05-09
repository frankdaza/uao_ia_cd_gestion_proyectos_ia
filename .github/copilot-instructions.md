# Instrucciones del repositorio — GitHub Copilot / Codex

## Idioma

Comentarios en código, docstrings, mensajes de commit, textos de PR y documentación (`README`, reportes): **español latinoamericano**, profesional y neutro.

## Python y entorno

- **Python 3.12**.
- Dependencias y entorno con **UV**: `pyproject.toml` + `uv.lock`; `uv python pin 3.12`, `uv sync`, `uv add`, `uv run`. Evitar `pip` y `venv` como predeterminados.

## Proyecto — Laboratorio Dry Bean

Clasificación multiclase del **Dry Bean Dataset** (UCI id **602**), objetivo **`Class`**, con **CRISP-DM**, **TDSP** y **Scrum ML**. Estructura: `data/raw`, `data/processed`, `notebooks`, `outputs/models`, `outputs/reports`, `src`. Modelos: baseline `Pipeline` (`StandardScaler` + `LogisticRegression`); alternativo `RandomForestClassifier`. Métricas: accuracy, **F1 macro**, matriz de confusión. Guardar modelo con **`joblib`**. Git: ramas `feature/*`, pull requests.

Consignas: `consignas/Lab1.pdf`, `consignas/Plan_Equipos_ScrumML_DryBean.pdf`.

## Otras guías del mismo repo

- Cursor: `.cursor/rules/`, skill `.cursor/skills/drybean-ml-laboratorio/SKILL.md`
- Claude Code: `CLAUDE.md`
- Tabla de sincronización: `AGENTS.md`

Al cambiar políticas globales del proyecto, actualizar **este archivo**, `CLAUDE.md`, `.cursor/rules/`, el skill y `AGENTS.md`.
