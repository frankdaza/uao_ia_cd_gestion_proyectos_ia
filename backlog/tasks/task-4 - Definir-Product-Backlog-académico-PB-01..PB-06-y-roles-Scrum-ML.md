---
id: TASK-4
title: Definir Product Backlog académico PB-01..PB-06 y roles Scrum ML
status: To Do
assignee:
  - Frank Daza
created_date: '2026-05-09 18:39'
labels: []
dependencies: []
references:
  - consignas/Plan_Equipos_ScrumML_DryBean.pdf
  - consignas/Lab1.pdf
  - docs/tdsp-alineacion.md
documentation:
  - docs/product-backlog.md
  - docs/scrum/roles.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Formalizar el **Product Backlog académico** del laboratorio Dry Bean (UCI 602) según el plan de equipos (P3) y dejar registrados los roles Scrum ML del equipo (P1). Esta tarea da trazabilidad entre las historias PB-01..PB-06 del plan y las tareas técnicas internas del repositorio (TASK-*), y habilita las evidencias Scrum exigidas en la entrega (L15).

**Fuentes:** consignas/Plan_Equipos_ScrumML_DryBean.pdf, consignas/Lab1.pdf, docs/tdsp-alineacion.md (§4 plan priorizado).

## Alcance

1. Crear `docs/product-backlog.md` con tabla PB-01..PB-06 (título, descripción, criterios de aceptación, mapeo a TASK-* internas, sprint estimado).
2. Crear `docs/scrum/roles.md` con asignación nominal: Product Owner, Scrum Master, Data Engineer/Analyst, ML Engineer, según assignees válidos en `backlog/config.yml`.
3. Crear `docs/scrum/plantilla-retrospectiva.md` con estructura de 3 puntos (qué funcionó, qué no, qué mejorar) y campos para fecha, sprint, asistentes.
4. Crear `docs/scrum/tablero.md` con instrucciones para mantener columnas **Por hacer / En progreso / Hecho** mediante `backlog board` o exportación.

## Fuera de alcance

- Implementación de las historias PB-01..PB-06 (cubiertas por TASK-8 a TASK-16).
- Configuración del entorno UV (TASK-5) o de la estructura de carpetas (ya en TASK-3).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 docs/product-backlog.md existe y lista PB-01..PB-06 con título, descripción, criterios de aceptación y mapeo explícito a TASK-* internas.
- [ ] #2 docs/scrum/roles.md asigna nominalmente PO, SM, Data Eng y ML Eng usando solo nombres definidos en backlog/config.yml.
- [ ] #3 docs/scrum/plantilla-retrospectiva.md contiene estructura de 3 puntos y campos para sprint, fecha y asistentes.
- [ ] #4 docs/scrum/tablero.md describe el flujo Por hacer / En progreso / Hecho y el comando o procedimiento para exportar el tablero.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Leer Plan_Equipos_ScrumML_DryBean.pdf (§ Product Backlog y § Roles) y extraer PB-01..PB-06 textuales.
2. Mapear cada PB a una o varias TASK-* del repo (TASK-8..TASK-17) en una tabla.
3. Redactar docs/product-backlog.md, docs/scrum/roles.md, docs/scrum/plantilla-retrospectiva.md y docs/scrum/tablero.md.
4. Enlazar los nuevos documentos desde README.md (sección Scrum) y desde docs/.
5. Validar nombres de assignees contra backlog/config.yml.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Idioma: español latinoamericano. Respetar nombres exactos de assignees del config (Jenifer Ramos, Juan Velasquez, Yan Cuaran, Frank Daza). Si el equipo decide rotación de roles por sprint, documentar la regla en roles.md.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Documentos enlazados desde README.md o docs/README.md para descubrimiento.
- [ ] #2 Mapeo PB → TASK-* validado contra backlog/tasks/ vigente al cierre de la tarea.
<!-- DOD:END -->
