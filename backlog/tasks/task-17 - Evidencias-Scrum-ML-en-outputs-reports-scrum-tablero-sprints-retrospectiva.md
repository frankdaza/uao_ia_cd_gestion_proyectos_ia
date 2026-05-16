---
id: TASK-17
title: >-
  Evidencias Scrum ML en outputs/reports/scrum/ (tablero, sprints,
  retrospectiva)
status: Done
assignee:
  - Frank Daza
created_date: '2026-05-09 18:45'
updated_date: '2026-05-16 04:10'
labels: []
dependencies:
  - TASK-4
  - TASK-15
references:
  - consignas/Plan_Equipos_ScrumML_DryBean.pdf
  - consignas/Lab1.pdf
  - docs/scrum/plantilla-retrospectiva.md
documentation:
  - outputs/reports/scrum/
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Generar las **evidencias Scrum ML** exigidas en L15 (entregable de Scrum) y P4 (sprints 1-3 con tareas y entregables) del Plan de Equipos. Esta tarea consolida en `outputs/reports/scrum/` los artefactos que demuestran que el equipo aplicó Scrum sobre el laboratorio: backlog, tablero, distribución por sprint y retrospectiva.

## Alcance

1. Crear `outputs/reports/scrum/` con los archivos:
   - `backlog-snapshot.md` — listado del Product Backlog (PB-01..PB-06) y del backlog técnico (TASK-1..TASK-19) al cierre.
   - `tablero.md` — captura textual o export del tablero **Por hacer / En progreso / Hecho** (puede generarse con `backlog board export` o equivalente).
   - `sprint-1.md`, `sprint-2.md`, `sprint-3.md` — tareas asignadas, completadas y observaciones por sprint.
   - `retrospectiva.md` — retrospectiva final con 3 puntos (qué funcionó, qué no, qué mejorar) usando la plantilla de TASK-4.
2. Enlazar el directorio desde el reporte (TASK-16, sección 7).
3. Validar nombres de assignees y estados contra `backlog/config.yml`.

## Fuera de alcance

- Re-creación de tareas Backlog (ya existen).
- Métricas avanzadas tipo burn-down (extensión opcional).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 outputs/reports/scrum/ contiene backlog-snapshot.md, tablero.md, sprint-1.md, sprint-2.md, sprint-3.md y retrospectiva.md.
- [x] #2 backlog-snapshot.md lista PB-01..PB-06 y TASK-1..TASK-19 con estado al cierre del laboratorio.
- [x] #3 Cada archivo sprint-N.md indica fechas estimadas, tareas TASK-* asignadas y completadas, y notas relevantes.
- [x] #4 retrospectiva.md sigue la plantilla de 3 puntos definida en TASK-4 y registra fecha y asistentes.
- [x] #5 El reporte (TASK-16, sección 7 Scrum ML) enlaza explícitamente a outputs/reports/scrum/.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Ejecutar backlog task list y backlog board export (si está disponible) para capturar el estado real al momento del cierre.
2. Distribuir TASK-* en los tres sprints según consigna (Sprint 1: bases + EDA; Sprint 2: modelado; Sprint 3: entrega).
3. Redactar retrospectiva con el equipo (3 puntos).
4. Enlazar desde informe_laboratorio.md sección 7.
5. Validar nombres y estados contra backlog/config.yml.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Si backlog board export no está disponible o produce un formato no Markdown, usar copia textual de la tabla de tareas. Esta evidencia es crítica para la rúbrica Scrum ML (15 puntos según L17).
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Sin información en inglés salvo nombres propios y comandos.
- [x] #2 Tablero exportado o transcrito sin tareas atascadas in-progress sin justificación.
<!-- DOD:END -->
