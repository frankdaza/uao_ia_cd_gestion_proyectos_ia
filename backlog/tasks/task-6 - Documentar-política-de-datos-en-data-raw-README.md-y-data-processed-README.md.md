---
id: TASK-6
title: Documentar política de datos en data/raw/README.md y data/processed/README.md
status: To Do
assignee:
  - Yan Cuaran
created_date: '2026-05-09 18:40'
labels: []
dependencies: []
references:
  - consignas/Lab1.pdf
  - docs/tdsp-estructura-congelada.md
  - docs/tdsp-alineacion.md
documentation:
  - data/raw/README.md
  - data/processed/README.md
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

La estructura física TDSP ya existe (TASK-3), pero las carpetas de datos no documentan **cómo obtener** el Dry Bean Dataset (UCI 602), qué se versiona y qué no, ni cómo registrar la procedencia y la fecha de descarga. Sin esta documentación, el equipo no puede reproducir el laboratorio en otra máquina y el flujo CRISP-DM (Comprensión de datos) queda incompleto.

## Alcance

1. Crear `data/raw/README.md` con:
   - Identificación del dataset: Dry Bean Dataset, UCI id **602**, variable objetivo `Class`.
   - Procedimiento canónico: `from ucimlrepo import fetch_drybean` (vía `fetch_ucirepo(id=602)`).
   - Política de versionado: solo se versiona `.gitkeep`; no se versionan archivos `.csv`, `.xlsx` ni binarios.
   - Plantilla para registrar fecha de descarga, hash SHA-256 (opcional) y notas.
2. Crear `data/processed/README.md` con:
   - Definición de "datos procesados" en este laboratorio (post `clean()` y/o post `split()`).
   - Convención de nombres (p. ej. `drybean_train.parquet`, `drybean_test.parquet`).
   - Política de versionado (no versionar binarios; reproducibles desde `src/preprocessing.py`).

## Fuera de alcance

- Implementación de la función `fetch_drybean` (TASK-8) o `clean/split` (TASK-10).
- Cambios a `.gitignore` (ya cubiertos por TASK-3).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 data/raw/README.md existe, identifica UCI 602, describe el comando ucimlrepo y la política de no versionado de datos crudos.
- [ ] #2 data/processed/README.md existe, define convención de nombres y política de no versionado de datos procesados.
- [ ] #3 Ambos README enlazan a docs/tdsp-estructura-congelada.md (sección de archivos mínimos por carpeta).
- [ ] #4 Ambos README incluyen plantilla con campos: dataset, fuente, fecha de descarga, responsable, notas.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Revisar docs/tdsp-estructura-congelada.md §2 para alinear la convención de archivos mínimos.
2. Redactar data/raw/README.md con la plantilla de procedencia y el comando ucimlrepo.
3. Redactar data/processed/README.md con la convención de nombres y la regla de reproducibilidad.
4. Enlazar ambos desde README.md raíz.
5. Verificar git status para confirmar que solo se añaden archivos Markdown (no binarios).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Idioma: español latinoamericano. Si el equipo opta por un dataset alternativo (poco probable), documentar cambio en docs/tdsp-alineacion.md y abrir tarea de actualización aquí.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Sin binarios versionados accidentalmente en data/raw o data/processed (verificar con git status).
- [ ] #2 Documentos enlazados desde README.md raíz (sección Datos).
<!-- DOD:END -->
