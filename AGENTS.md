# Guía para agentes de código (Cursor, Claude Code, Copilot/Codex)

Este repositorio es el laboratorio **Machine Learning — Dry Bean** (UCI id **602**): **CRISP-DM**, **TDSP** y **Scrum ML**. Las consignas completas están en `consignas/`.

## Políticas obligatorias

| Tema | Requisito |
|------|-----------|
| Idioma | **Español latinoamericano** en comentarios, docstrings, commits, PRs y documentación. |
| Python | **3.12** |
| Paquetes y entorno | **UV** (`pyproject.toml`, `uv.lock`, `uv sync`, `uv add`, `uv run`) |
| Calidad de código | **Ruff**, **Black**, **nbstripout** y **pre-commit** (`pyproject.toml`, `.pre-commit-config.yaml`). Tras clonar: `uv run pre-commit install`; validación local: `uv run pre-commit run --all-files`. |

## Dónde está cada cosa

| Herramienta | Archivos |
|-------------|----------|
| **Cursor** | [`.cursor/rules/stack-python-es.mdc`](.cursor/rules/stack-python-es.mdc) (siempre), [`.cursor/rules/drybean-lab-context.mdc`](.cursor/rules/drybean-lab-context.mdc) (Python/notebook/proyecto); skill [`.cursor/skills/drybean-ml-laboratorio/SKILL.md`](.cursor/skills/drybean-ml-laboratorio/SKILL.md); tareas Backlog: [`.cursor/rules/backlog-md-tareas.mdc`](.cursor/rules/backlog-md-tareas.mdc) y skill [`.cursor/skills/backlog-md-tareas/SKILL.md`](.cursor/skills/backlog-md-tareas/SKILL.md) |
| **Claude Code** | [`CLAUDE.md`](CLAUDE.md) (incluye puntero al skill de tareas Backlog) |
| **GitHub Copilot / Codex** | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) (incluye puntero al skill de tareas Backlog) |

## Sincronización (obligatoria al cambiar reglas o skills)

Si se **agrega, elimina o modifica** una política que deba aplicar a todos los asistentes (idioma, versión de Python, UV, estándares de calidad con ruff/black/pre-commit, flujo del laboratorio, Definition of Done, estructura TDSP, etc.), **actualizar en la misma tarea commit** todos estos sitios para que permanezcan alineados:

1. [`.cursor/rules/stack-python-es.mdc`](.cursor/rules/stack-python-es.mdc) y, si aplica el contexto del lab, [`.cursor/rules/drybean-lab-context.mdc`](.cursor/rules/drybean-lab-context.mdc). Si cambian estándares de redacción o flujo de **tareas Backlog.md**, [`.cursor/rules/backlog-md-tareas.mdc`](.cursor/rules/backlog-md-tareas.mdc).
2. [`.cursor/skills/drybean-ml-laboratorio/SKILL.md`](.cursor/skills/drybean-ml-laboratorio/SKILL.md) y, si aplica, [`.cursor/skills/backlog-md-tareas/SKILL.md`](.cursor/skills/backlog-md-tareas/SKILL.md)
3. [`CLAUDE.md`](CLAUDE.md)
4. [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
5. Esta sección en [`AGENTS.md`](AGENTS.md) solo si cambia el **procedimiento** de sincronización o la tabla de ubicaciones.

El contenido no tiene que ser idéntico palabra por palabra entre archivos, pero **las políticas y el flujo técnico no deben contradecirse**.

<!-- BACKLOG.MD MCP GUIDELINES START -->

<CRITICAL_INSTRUCTION>

## BACKLOG WORKFLOW INSTRUCTIONS

This project uses Backlog.md MCP for all task and project management activities.

**CRITICAL GUIDANCE**

- If your client supports MCP resources, read `backlog://workflow/overview` to understand when and how to use Backlog for this project.
- If your client only supports tools or the above request fails, call `backlog.get_backlog_instructions()` to load the tool-oriented overview. Use the `instruction` selector when you need `task-creation`, `task-execution`, or `task-finalization`.

- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

These guides cover:
- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Links to detailed guides for task creation, execution, and finalization
- MCP tools reference

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD MCP GUIDELINES END -->
