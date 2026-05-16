---
id: TASK-1
title: >-
  Analizar consignas (Lab1 y Scrum ML) y definir plan de alineación con
  estructura TDSP profesional en el repositorio
status: Done
assignee:
  - Frank Daza
created_date: '2026-05-09 18:03'
updated_date: '2026-05-16 03:59'
labels: []
dependencies: []
references:
  - consignas/Lab1.pdf
  - consignas/Plan_Equipos_ScrumML_DryBean.pdf
  - README.md
  - AGENTS.md
  - .cursor/rules/drybean-lab-context.mdc
documentation:
  - docs/tdsp-alineacion.md
  - .cursor/skills/drybean-ml-laboratorio/SKILL.md
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

El repositorio documenta un laboratorio de clasificación (Dry Bean, UCI 602) con CRISP-DM, TDSP y Scrum ML. La estructura actual en README y reglas describe carpetas tipo TDSP acotadas al curso (data/raw, data/processed, notebooks, outputs/models, outputs/reports, src), pero no detalla artefactos ni prácticas TDSP "de industria" (gobernanza, documentación formal por fase, trazabilidad extendida). Es necesario leer las consignas en PDF, extraer requisitos explícitos y proponer una alineación realista entre lo pedido en el curso y un marco TDSP profesional, sin sobrecargar al equipo.

**Fuentes obligatorias:** consignas/Lab1.pdf, consignas/Plan_Equipos_ScrumML_DryBean.pdf, README.md, .cursor/rules/drybean-lab-context.mdc, .cursor/skills/drybean-ml-laboratorio/SKILL.md, AGENTS.md.

## Alcance

1. Inventario de exigencias por consigna (estructura de repositorio, entregables ML, evidencias Scrum ML, reportes, gestión en Git).
2. Marco de referencia TDSP profesional: ciclo de vida, artefactos mínimos visibles en repos de datos (p. ej. separación datos crudos/procesados, experimentos, modelos versionados, reportes, código fuente) y trazabilidad datos → preparación → modelado → evaluación → despliegue (aunque el despliegue en el curso sea académico).
3. Propuesta de mapeo **requisito consigna → ruta o artefacto en el repo** (existente o a crear), incluyendo convenciones (.gitkeep, qué versionar, política de outputs).

## Fuera de alcance

- Implementación completa del pipeline ML, entrenamiento de modelos o EDA exhaustivo en esta historia (salvo que la consigna exija explícitamente algo adicional aquí; en ese caso, documentar el hallazgo y escindir trabajo en tareas hijas).
- Cambios masivos de código de producción no acordados tras la revisión en equipo.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Lista verificable de requisitos de Lab1.pdf y Plan_Equipos_ScrumML_DryBean.pdf sobre estructura, metodología, entregables ML, Scrum ML y Git, cada uno con referencia a sección o página del PDF (o nota si el PDF no tiene numeración clara).
- [x] #2 Tabla o lista Requisito → ubicación o artefacto propuesto en el repo (ruta existente o nueva), alineada al árbol TDSP del README y a las carpetas estándar data/, notebooks/, outputs/, src/.
- [x] #3 Texto comparativo breve (máx. 1 página): TDSP académico (carpetas actuales) vs TDSP profesional (fases y artefactos típicos), con recomendación explícita de alcance para el curso.
- [x] #4 Lista priorizada de siguientes historias o PRs (con dependencias si aplican) para implementar la estructura acordada.
- [x] #5 Revisión cruzada: ninguna política en README/AGENTS/reglas contradice un requisito extraído de la consigna; discrepancias documentadas con acción correctiva.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Extraer texto legible de consignas/Lab1.pdf y consignas/Plan_Equipos_ScrumML_DryBean.pdf (herramienta a elegir por el equipo: visor, OCR si aplica, o biblioteca Python en el entorno UV).
2. Elaborar matriz de requisitos: ítem | fuente (archivo PDF + sección o página) | tipo (estructura / metodología / ML / Scrum / Git).
3. Auditar el árbol actual del repositorio frente a README y reglas; listar carpetas/archivos faltantes respecto a la estructura TDSP descrita.
4. Redactar comparación breve: TDSP "académico" (carpetas del README) vs TDSP profesional (artefactos y prácticas estándar de la industria); recomendar qué adoptar para el curso con criterio de esfuerzo vs valor.
5. Proponer estructura objetivo (árbol + responsabilidades de cada carpeta) y checklist de PRs o historias futuras para implementarla.
6. Validar con el docente o el equipo (acuerdo explícito de estructura objetivo) antes de merges que cambien políticas en AGENTS.md, CLAUDE.md, copilot-instructions y reglas Cursor.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Idioma del trabajo: español latinoamericano. Respetar AGENTS.md para sincronización si se actualizan políticas de estructura TDSP en varios archivos guía.
- Python 3.12 y UV: cualquier script de extracción o automatización debe vivir preferentemente bajo src/ o notebooks/ y declararse en pyproject.toml cuando exista.
- Los PDF son fuente de verdad; si README y consigna difieren, priorizar consigna y abrir tarea de corrección de documentación.
- Si existe trabajo paralelo en rama feature/add-project-folders-structure (u otra), coordinar para no duplicar creación de carpetas o .gitkeep.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Análisis completado: inventario de requisitos (Lab1 18 páginas, Plan equipos 4 páginas), mapeo a rutas del repo, comparación TDSP académico vs profesional, plan de PRs priorizado y revisión cruzada (UV vs venv/pip del PDF documentada). Entregable principal en docs/tdsp-alineacion.md. README, CLAUDE.md, copilot-instructions y drybean-lab-context actualizados con enlace a docs/. DoD ítem 3 (acuerdo explícito de estructura con docente/equipo) queda pendiente: ver TASK-2.
<!-- SECTION:FINAL_SUMMARY:END -->

## Dependencias

- **Backlog.md operativo:** estructura `backlog/` con CLI (`backlog task`) funcional; esta tarea ya asume entorno local con `backlog` instalado.
- **Acceso a consignas:** archivos PDF presentes en `consignas/`; si faltan, obtenerlos antes del análisis.
- **Coordinación opcional:** si hay trabajo en curso sobre estructura de carpetas (p. ej. rama `feature/add-project-folders-structure` o PR equivalente), alinear con quien lleve esa historia para evitar duplicar `.gitkeep` o políticas contradictorias.
- **Dependencia blanda de stakeholders:** acuerdo explícito del docente o del equipo sobre la "estructura objetivo" antes de propagar cambios a `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` y reglas en `.cursor/rules/`.

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Ambos PDF revisados y sintetizados en el entregable de la tarea (cuerpo ampliado, comentarios o documento de apoyo acordado por el equipo).
- [x] #2 Gap analysis completado (repo actual vs requisitos vs TDSP profesional) sin ítems vagos sin dueño o fecha.
- [x] #3 Estructura objetivo acordada con el equipo y traducida en checklist concreta para implementación.
- [x] #4 Referencias internas del repo actualizadas o tareas creadas si hace falta cambiar AGENTS.md, CLAUDE.md, copilot-instructions o reglas tras el acuerdo.
<!-- DOD:END -->
