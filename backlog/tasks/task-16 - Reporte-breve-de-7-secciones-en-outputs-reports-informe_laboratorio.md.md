---
id: TASK-16
title: Reporte breve de 7 secciones en outputs/reports/informe_laboratorio.md
status: Done
assignee:
  - Juan Velasquez
created_date: '2026-05-09 18:45'
updated_date: '2026-05-16 03:59'
labels: []
dependencies:
  - TASK-15
references:
  - consignas/Lab1.pdf
  - .cursor/skills/drybean-ml-laboratorio/SKILL.md
documentation:
  - outputs/reports/informe_laboratorio.md
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Producir el **reporte narrativo** exigido en L15 y en el SKILL del laboratorio: un documento Markdown corto, profesional, con las 7 secciones canónicas del SKILL `drybean-ml-laboratorio`. Sirve como complemento al notebook integrador (TASK-15) y como insumo para la entrega final del laboratorio.

## Alcance

1. Crear `outputs/reports/informe_laboratorio.md` con las 7 secciones en español latinoamericano:
   - **1. Comprensión del negocio** — problema y objetivo.
   - **2. Comprensión de datos** — tamaño, variables, clases, calidad.
   - **3. Preparación** — transformaciones y partición train/test (incluye semilla y proporción).
   - **4. Modelado** — modelos entrenados e hiperparámetros relevantes.
   - **5. Evaluación** — accuracy, F1 macro, comparación, matriz de confusión (referencia a `outputs/reports/confusion_matrix.png`).
   - **6. Despliegue** — ruta del `.joblib` y cómo cargar y probar predicción.
   - **7. Scrum ML** — backlog, avance por sprint, retrospectiva (3 puntos).
2. Enlazar al notebook integrador y a los artefactos `outputs/reports/comparison.csv`, `confusion_matrix.png`, `classification_report.txt`.
3. Mantener el reporte breve (≤ 4-6 páginas Markdown).

## Fuera de alcance

- Evidencias Scrum exportadas en `outputs/reports/scrum/` (TASK-17).
- Generación PDF (extensión opcional).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 outputs/reports/informe_laboratorio.md existe con las 7 secciones nombradas.
- [ ] #2 Cada sección contiene contenido sustantivo (no marcadores vacíos): mínimo 1 párrafo explicativo + datos/cifras.
- [ ] #3 El reporte enlaza al notebook integrador (TASK-15) y a los artefactos de TASK-13 (comparison.csv, confusion_matrix.png, classification_report.txt).
- [ ] #4 Las cifras de accuracy y F1 macro reportadas coinciden con outputs/reports/comparison.csv (consistencia entre artefactos).
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Tomar como base la plantilla del SKILL drybean-ml-laboratorio (sección 'Plantilla mínima — reporte breve').
2. Para cada sección: redactar 1-3 párrafos en español latinoamericano y citar números reales del experimento.
3. Insertar enlaces relativos a notebook y artefactos en outputs/reports/.
4. Verificar consistencia con comparison.csv y métricas JSON.
5. Solicitar revisión cruzada en PR.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Si en el futuro se exporta a PDF, considerar pandoc; por ahora el Markdown es suficiente. Mantener el archivo bajo outputs/reports/ (alineado con TASK-3 / estructura congelada).
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Reporte revisado por al menos un miembro del equipo distinto del autor antes del cierre.
- [ ] #2 Sin contenido en inglés salvo nombres propios o comandos.
<!-- DOD:END -->
