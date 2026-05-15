# Datos procesados — Dry Bean Dataset

Este directorio almacena los datos derivados del procesamiento aplicado sobre los datos crudos
(`data/raw/`). No se versionan archivos de datos en este repositorio. Ver política de versionado más abajo.

## Definición de datos procesados

En este laboratorio se consideran datos procesados los archivos generados tras aplicar:

- **Limpieza** (`clean()` en `src/preprocessing.py`): eliminación de duplicados y verificación de nulos.
- **Partición estratificada** (`split()` en `src/preprocessing.py`): división train/test
  manteniendo la proporción de clases de la variable objetivo `Class`.

Referencia estructural: [docs/tdsp-estructura-congelada.md](../../docs/tdsp-estructura-congelada.md)

## Convención de nombres de archivos

| Archivo                    | Descripción                                      |
|----------------------------|--------------------------------------------------|
| `drybean_train.parquet`    | Conjunto de entrenamiento (features + Class)     |
| `drybean_test.parquet`     | Conjunto de prueba (features + Class)            |
| `drybean_clean.parquet`    | Dataset completo post-limpieza, antes del split  |

El formato `.parquet` es preferido por eficiencia. Si se requiere `.csv` para compatibilidad,
usar el mismo nombre base con extensión `.csv`.

## Política de versionado

- Solo se versiona el archivo `.gitkeep` (marcador de carpeta vacía).
- **No** se versionan archivos `.parquet`, `.csv` ni ningún binario de datos procesados.
- Los datos procesados son **reproducibles** ejecutando `src/preprocessing.py` sobre los datos crudos.
- El `.gitignore` del repositorio excluye binarios en `data/processed/`.

## Reproducibilidad

Para regenerar los datos procesados desde cero:

```bash
uv run python -m src.preprocessing
```

Esto requiere que los datos crudos estén disponibles en `data/raw/` o que `fetch_drybean()`
pueda descargarlos desde UCI (requiere conexión a internet).

## Plantilla de procedencia

| Campo              | Valor |
|--------------------|-------|
| Dataset base       | Dry Bean Dataset (UCI 602) |
| Script de origen   | src/preprocessing.py |
| Fecha de generación | AAAA-MM-DD |
| Responsable        | (nombre del integrante) |
| Parámetros         | (ej. test_size=0.2, random_state=42) |
| Notas              | (observaciones o cambios respecto a la versión anterior) |
