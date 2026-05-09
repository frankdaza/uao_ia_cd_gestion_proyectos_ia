# Guía para agentes de código (Cursor, Claude Code, Copilot/Codex)

Este repositorio es el laboratorio **Machine Learning — Dry Bean** (UCI id **602**): **CRISP-DM**, **TDSP** y **Scrum ML**. Las consignas completas están en `consignas/`.

## Políticas obligatorias

| Tema | Requisito |
|------|-----------|
| Idioma | **Español latinoamericano** en comentarios, docstrings, commits, PRs y documentación. |
| Python | **3.12** |
| Paquetes y entorno | **UV** (`pyproject.toml`, `uv.lock`, `uv sync`, `uv add`, `uv run`) |

## Dónde está cada cosa

| Herramienta | Archivos |
|-------------|----------|
| **Cursor** | [`.cursor/rules/stack-python-es.mdc`](.cursor/rules/stack-python-es.mdc) (siempre), [`.cursor/rules/drybean-lab-context.mdc`](.cursor/rules/drybean-lab-context.mdc) (Python/notebook/proyecto); skill [`.cursor/skills/drybean-ml-laboratorio/SKILL.md`](.cursor/skills/drybean-ml-laboratorio/SKILL.md) |
| **Claude Code** | [`CLAUDE.md`](CLAUDE.md) |
| **GitHub Copilot / Codex** | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) |

## Sincronización (obligatoria al cambiar reglas o skills)

Si se **agrega, elimina o modifica** una política que deba aplicar a todos los asistentes (idioma, versión de Python, UV, flujo del laboratorio, Definition of Done, estructura TDSP, etc.), **actualizar en la misma tarea commit** todos estos sitios para que permanezcan alineados:

1. [`.cursor/rules/stack-python-es.mdc`](.cursor/rules/stack-python-es.mdc) y, si aplica el contexto del lab, [`.cursor/rules/drybean-lab-context.mdc`](.cursor/rules/drybean-lab-context.mdc)
2. [`.cursor/skills/drybean-ml-laboratorio/SKILL.md`](.cursor/skills/drybean-ml-laboratorio/SKILL.md)
3. [`CLAUDE.md`](CLAUDE.md)
4. [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
5. Esta sección en [`AGENTS.md`](AGENTS.md) solo si cambia el **procedimiento** de sincronización o la tabla de ubicaciones.

El contenido no tiene que ser idéntico palabra por palabra entre archivos, pero **las políticas y el flujo técnico no deben contradecirse**.
