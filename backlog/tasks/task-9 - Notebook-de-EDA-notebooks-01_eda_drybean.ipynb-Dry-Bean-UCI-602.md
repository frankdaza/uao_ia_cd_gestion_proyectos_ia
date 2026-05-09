---
id: TASK-9
title: Notebook de EDA notebooks/01_eda_drybean.ipynb (Dry Bean UCI 602)
status: To Do
assignee:
  - Yan Cuaran
created_date: '2026-05-09 18:42'
labels: []
dependencies:
  - TASK-6
  - TASK-8
references:
  - consignas/Lab1.pdf
  - docs/tdsp-alineacion.md
documentation:
  - notebooks/01_eda_drybean.ipynb
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contexto y objetivo

Realizar el **Análisis Exploratorio de Datos (EDA)** del Dry Bean Dataset cubriendo CRISP-DM fase 2 (Comprensión de datos) y los requisitos **L11** y **PB-02** del plan de equipos. El notebook usa el módulo `src/data_loading.py` (TASK-8) y queda como evidencia versionada del entendimiento de los datos antes del modelado.

## Alcance

1. Crear `notebooks/01_eda_drybean.ipynb` con celdas Markdown introductorias y secciones numeradas.
2. Cargar datos vía `from src.data_loading import fetch_drybean`.
3. Análisis estructural: `shape`, `dtypes`, `info`, `describe`.
4. Calidad: nulos por columna, conteo de duplicados, valores únicos por feature.
5. Distribución de la variable objetivo `Class` (conteo, porcentaje, gráfica de barras).
6. Análisis univariado: histogramas o KDE de las 16 features numéricas.
7. Análisis bivariado: matriz de correlación (Pearson) con heatmap; boxplots de 2-3 features clave por `Class`.
8. Conclusiones del EDA en celda Markdown final (5-8 hallazgos accionables para preparación y modelado).

## Fuera de alcance

- Limpieza definitiva o partición train/test (TASK-10).
- Entrenamiento de modelos (TASK-11, TASK-12).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 notebooks/01_eda_drybean.ipynb existe y se ejecuta de inicio a fin con uv run jupyter nbconvert --execute sin errores.
- [ ] #2 El notebook reporta explícitamente: shape, conteo de nulos por columna, conteo de duplicados y distribución de Class.
- [ ] #3 Incluye al menos 1 figura por sección (distribución de Class, histogramas de features, matriz de correlación, boxplots).
- [ ] #4 La sección final 'Conclusiones del EDA' lista 5 a 8 hallazgos en lenguaje claro y en español.
- [ ] #5 Las salidas pesadas del notebook quedan stripeadas por nbstripout (no se versionan outputs binarios grandes).
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. uv run jupyter lab y crear notebooks/01_eda_drybean.ipynb.
2. Sección 1: contexto del dataset (UCI 602, variable objetivo Class).
3. Sección 2: carga con fetch_drybean (cache_dir opcional a data/raw).
4. Sección 3: estructura y calidad (shape, dtypes, nulos, duplicados).
5. Sección 4: análisis de Class (conteo + barplot).
6. Sección 5: distribución de features (hist o KDE).
7. Sección 6: correlación (heatmap) y boxplots por Class.
8. Sección 7: conclusiones accionables (qué limpieza aplicar, qué features parecen separar mejor las clases).
9. Validar ejecución completa con uv run jupyter nbconvert --to notebook --execute.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Usar matplotlib y/o seaborn (instalable como dep adicional si no está). Asegurar reproducibilidad fijando random_state donde aplique. Mantener celdas cortas y narrativa en Markdown entre secciones (estándar de notebook profesional).
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 El notebook importa funciones desde src/ en lugar de duplicar lógica de carga.
- [ ] #2 Cualquier figura exportada se guarda en outputs/reports/eda/ (no versionada si pesa, alineado con TASK-3).
<!-- DOD:END -->
