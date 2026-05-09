---
name: backlog-md-tareas
description: >-
  Crea y edita tareas de Backlog.md (CLI o MCP) con calidad profesional: español latinoamericano,
  criterios verificables, Definition of Done, plan, dependencias y alineación con backlog/config.yml.
  Usar cuando el usuario pida crear una tarea, historias, ítems del backlog, PBIs o gestión en
  backlog/tasks; o al editar archivos bajo backlog/tasks/.
disable-model-invocation: true
---

# Backlog.md — Calidad profesional en tareas

## Políticas del repositorio

- Redacción en **español latinoamericano**, tono profesional y neutro (títulos, descripción, criterios, notas).
- Respetar [`backlog/config.yml`](../../../backlog/config.yml): **estados** (`To Do`, `In Progress`, `Done`), **assignees** autorizados y convenciones del proyecto. No inventar personas ni estados fuera de la lista.

## Antes de crear una tarea

1. Si el cliente expone MCP de Backlog, leer el recurso o instrucciones de flujo (`backlog://workflow/overview` o equivalente) antes de crear trabajo duplicado.
2. Ejecutar **búsqueda primero**: `backlog search` o revisar `backlog/tasks/` para no duplicar historias.
3. Definir **título** con verbo de acción + objeto + contexto mínimo (una línea, sin ambigüedad).

## Plantilla obligatoria de contenido

Cada tarea nueva debe poder completarse sin interpretación vaga. Incluir estas secciones (en descripción o en campos nativos de la CLI):

| Sección | Contenido esperado |
|--------|---------------------|
| **Contexto y objetivo** | Por qué existe la tarea, problema o oportunidad, vínculo con consignas o producto. |
| **Alcance** | Lista numerada de lo que sí cubre la tarea. |
| **Fuera de alcance** | Explícito: qué no hará esta historia (evita creep). |
| **Acceptance criteria** | Ítems **verificables** y, cuando aplique, **SMART** (específicos, medibles). Usar `backlog task create --ac` o checklist en el archivo. |
| **Definition of Done** | Condiciones de cierre más allá del código: revisión, pruebas, documentación, alineación con políticas (`AGENTS.md`, reglas, skills). |
| **Plan de implementación** | Pasos ordenados que un par pueda seguir ( `--plan` o sección equivalente). |
| **Notas de implementación** | UV, Python 3.12, rutas de repo, riesgos técnicos, convenciones Git. |
| **Dependencias** | Técnicas (otras tareas, ramas, PRs) y blandas (acuerdo de equipo, acceso a datos). |
| **Referencias** | `--ref` / `--doc`: PDFs, `README`, rutas de código. |

## Criterios de calidad (checklist rápido)

- [ ] Cada criterio de aceptación responde "¿cómo sé que está hecho?" sin subjetividad.
- [ ] Hay **un** responsable claro (`assignee` del `config.yml`).
- [ ] Dependencias reales declaradas (o lista vacía y justificada).
- [ ] Sin jerga opaca: términos de dominio definidos la primera vez que aparecen.
- [ ] Si la tarea cambia políticas globales del laboratorio, el ejecutor debe planificar la **sincronización** descrita en [`AGENTS.md`](../../../AGENTS.md).

## Comandos CLI de referencia

```bash
cd <raíz-del-repo>
backlog task create "Título claro" -d "Descripción..." -a "Nombre Apellido" -s "To Do" \
  --ac "Criterio verificable 1" --plan "1. Paso..." --notes "..." \
  --ref "ruta/o/url"
backlog task list
backlog task view TASK-1
```

Ajustar flags según `backlog task create --help`.

## Relación con otras guías

- Laboratorio ML (Dry Bean): [drybean-ml-laboratorio](../drybean-ml-laboratorio/SKILL.md).
- Sincronización multi-asistente: [`AGENTS.md`](../../../AGENTS.md).
