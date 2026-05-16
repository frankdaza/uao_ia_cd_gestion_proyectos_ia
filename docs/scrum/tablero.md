# Tablero Scrum ML — flujo y exportación

Este documento describe cómo el equipo mantiene el tablero **Por hacer / En progreso / Hecho** para el laboratorio Dry Bean. Es una **guía de proceso** en `docs/scrum/`. La **evidencia de cierre** para la consigna (export o captura al momento de la entrega) se documenta en `outputs/reports/scrum/` (**TASK-17**).

## Columnas del tablero

| Columna | Significado |
|---------|-------------|
| **Por hacer** | Tareas TASK-* aún no iniciadas o sin responsable activo. |
| **En progreso** | Tarea en curso; idealmente una por persona para reducir multitarea. |
| **Hecho** | Criterios de aceptación cumplidos y cambios integrados en el repositorio cuando aplique. |

Los estados canónicos en archivos de tarea son `To Do`, `In Progress` y `Done` (ver [`backlog/config.yml`](../../backlog/config.yml)). Convención sugerida:

- `To Do` → columna **Por hacer**
- `In Progress` → columna **En progreso**
- `Done` → columna **Hecho**

## Cómo actualizar el estado

1. Editar el frontmatter de la tarea correspondiente en [`backlog/tasks/`](../../backlog/tasks/) (`status:`).
2. Opcional: usar la CLI **Backlog.md** desde la raíz del repositorio para visualizar el tablero Kanban.

### Ver el tablero en terminal

```bash
cd /ruta/al/repositorio
backlog board view
```

Layout vertical:

```bash
backlog board view --vertical
```

### Exportar el tablero a Markdown

Genera un archivo (por ejemplo para adjuntar o mover a evidencias de entrega):

```bash
cd /ruta/al/repositorio
backlog board export outputs/reports/scrum/tablero.md --force
```

Si aún no existe la carpeta `outputs/reports/scrum/`, crearla antes o usar otra ruta temporal y luego mover el archivo. La opción `--force` sobrescribe el destino sin confirmación interactiva.

### Alternativa sin CLI (plan B)

Copiar una tabla Markdown con tres columnas (**Por hacer**, **En progreso**, **Hecho**) y listar los IDs **TASK-*** según el estado real del frontmatter en `backlog/tasks/`. Este método es válido para la rúbrica si el export automatizado no está disponible (**TASK-17**).

## Referencias

- Skill del laboratorio: [`.cursor/skills/drybean-ml-laboratorio/SKILL.md`](../../.cursor/skills/drybean-ml-laboratorio/SKILL.md)
- Product Backlog PB-01..PB-06: [`docs/product-backlog.md`](../product-backlog.md)
