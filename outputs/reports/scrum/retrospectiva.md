# Retrospectiva — cierre del laboratorio Dry Bean ML

- **Sprint:** Cierre del laboratorio (Sprint 3 — entrega académica)
- **Fecha:** 2026-05-15
- **Asistentes:** Jenifer Ramos, Juan Velasquez, Yan Cuaran, Frank Daza

---

## Qué funcionó

- La estructura **TDSP** desde el inicio permitió ubicar datos, notebooks, modelos e informes sin ambigüedad.
- El uso de **`Pipeline`** de scikit-learn redujo riesgo de fuga de datos y simplificó persistencia con **joblib**.
- **UV** como gestor de entorno unificó dependencias y versiones de Python (**3.12**) entre integrantes.

## Qué no funcionó

- Parte de la **documentación de proceso** (estándares y evidencias Scrum) compitió con el desarrollo técnico en ventanas cortas de sprint.
- La coordinación entre **ramas feature** generó fricción en merges que podría haberse mitigado con integraciones más frecuentes.

## Qué mejorar

- Incluir **evidencias Scrum** y revisión del tablero como criterio explícito de fin de sprint, no solo como tarea de cierre.
- Adoptar **CI** desde etapas tempranas (TASK-19) para detectar regresiones en lint y pruebas de forma automática.
- Realizar **retrospectivas breves** al cierre de cada sprint, además de la retrospectiva de cierre del laboratorio.
