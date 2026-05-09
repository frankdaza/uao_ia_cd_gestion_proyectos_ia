---
name: drybean-ml-laboratorio
description: >-
  Guía el laboratorio de clasificación con Dry Bean (UCI id 602) usando CRISP-DM,
  TDSP y Scrum ML con scikit-learn. Incluye Definition of Done, entregables,
  evidencias ágiles y reproducibilidad con UV y Python 3.12. Usar cuando se trabaje
  en notebooks, `src/`, datos, modelos, reportes, el README del laboratorio o cuando
  el usuario mencione frijol seco, Dry Bean, UCI 602, Sprint o TDSP.
disable-model-invocation: true
---

# Laboratorio Dry Bean — Guía operativa

## Políticas del repositorio

- Documentación visible, comentarios y commits: **español latinoamericano**.
- **Python 3.12** y **UV**: dependencias en `pyproject.toml` + `uv.lock`; `uv sync`, `uv add`, `uv run`.

## Referencias

- Consigna detallada: [consignas/Lab1.pdf](../../../consignas/Lab1.pdf)
- Plan de equipo y Scrum: [consignas/Plan_Equipos_ScrumML_DryBean.pdf](../../../consignas/Plan_Equipos_ScrumML_DryBean.pdf)

## Comandos UV (referencia rápida)

```bash
uv python pin 3.12
uv sync
uv add pandas numpy matplotlib scikit-learn ucimlrepo joblib openpyxl jupyter
uv run python src/laboratorio_drybean.py
# o notebook:
uv run jupyter lab
```

Ajustar la lista de paquetes según el `pyproject.toml` del repo.

## Checklist — Definition of Done (laboratorio)

- [ ] El flujo (notebook o script) corre de inicio a fin sin errores.
- [ ] El dataset se obtiene o carga correctamente (UCI 602 o equivalente documentado).
- [ ] Se reportan nulos y duplicados; se documenta limpieza (p. ej. `drop_duplicates`).
- [ ] Hay al menos **un baseline** (`LogisticRegression` en `Pipeline` con `StandardScaler`) y **un modelo alternativo** (`RandomForestClassifier`).
- [ ] Se comparan modelos con **accuracy** y **F1 macro** (`average="macro"`).
- [ ] Se incluye **matriz de confusión** para el modelo principal o el escogido.
- [ ] El modelo final se guarda con **`joblib`** bajo `outputs/models/`.
- [ ] Se explican resultados en lenguaje comprensible.
- [ ] Se documenta la relación con **CRISP-DM**, **TDSP** y **Scrum ML**.

## Plantilla mínima — reporte breve (7 secciones)

1. Comprensión del negocio: problema y objetivo.
2. Comprensión de datos: tamaño, variables, clases, calidad.
3. Preparación: transformaciones y partición train/test.
4. Modelado: modelos entrenados e hiperparámetros relevantes.
5. Evaluación: métricas, comparación y matriz de confusión.
6. Despliegue: ruta del `.joblib` y cómo cargar o probar predicción.
7. Scrum ML: backlog, avance por sprint, retrospectiva (qué funcionó / qué no / qué mejorar).

## Evidencias Scrum ML para entregar

- Backlog inicial (historias o items PB-01… y tareas técnicas).
- Tablero simple: columnas **Por hacer**, **En progreso**, **Hecho**.
- Tareas completadas por sprint y retrospectiva (puntos acordados en la consigna).

## Flujo Git sugerido

Ramas `feature/<nombre>`, `git push`, **pull request** y aprobación antes de merge a la rama principal.

## Sincronización entre herramientas de IA

Si cambian políticas del laboratorio o del stack (idioma, Python, UV, DoD), actualizar también [CLAUDE.md](../../../CLAUDE.md), [.github/copilot-instructions.md](../../../.github/copilot-instructions.md) y las reglas en [.cursor/rules/](../../rules/). Ver [AGENTS.md](../../../AGENTS.md).
