---
id: TASK-3
title: 'PR: Estructura TDSP física (carpetas, .gitkeep, .gitignore datos/modelos)'
status: Done
assignee:
  - Frank Daza
created_date: '2026-05-09 18:16'
updated_date: '2026-05-16 03:59'
labels: []
dependencies:
  - TASK-1
references:
  - docs/tdsp-alineacion.md
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Ejecuta el requisito **P0** de docs/tdsp-alineacion.md: materializar en disco el árbol TDSP de las consignas (Lab1 / Plan equipos) para desbloquear PB y el laboratorio.

## Alcance

1. Crear carpetas `data/raw`, `data/processed`, `notebooks`, `outputs/models`, `outputs/reports`, `src` con `.gitkeep` donde corresponda.
2. Ajustar `.gitignore` para ignorar datos y modelos generados sin eliminar las carpetas del repositorio.

## Fuera de alcance

- Contenido del notebook o script de laboratorio (P2).
- pyproject.toml / uv.lock (P1).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Existen en el repo las rutas data/raw, data/processed, notebooks, outputs/models, outputs/reports y src, cada una con .gitkeep salvo que ya hubiera otro archivo versionado en esa ruta.
- [x] #2 El .gitignore ignora el contenido de data/raw y data/processed y de outputs/models, permitiendo explícitamente los .gitkeep correspondientes.
- [x] #3 docs/tdsp-alineacion.md refleja que el gap de carpetas físicas quedó resuelto (o se añade nota con fecha).
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Crear árbol de directorios y archivos .gitkeep.
2. Reemplazar bloque opcional comentado en .gitignore por reglas activas con excepción .gitkeep.
3. Verificar con git status que solo se añaden rutas esperadas.
4. Actualizar docs/tdsp-alineacion.md (gap P0) si aplica.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Referencias: docs/tdsp-alineacion.md sección 4 (P0). Política: no versionar datasets ni .joblib/.pkl en modelos; el equipo obtiene datos con ucimlrepo o copia local documentada.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implementación aplicada en el repo: carpetas TDSP con .gitkeep; .gitignore activo para data/raw, data/processed y outputs/models con excepciones .gitkeep; docs/tdsp-alineacion.md (P0 y gap §6) actualizado.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Cambios revisados localmente (git status limpio de archivos accidentales).
- [x] #2 La tarea enlaza a docs/tdsp-alineacion.md y queda lista para PR/merge según flujo del equipo.
<!-- DOD:END -->
