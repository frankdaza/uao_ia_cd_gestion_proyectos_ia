# Datos crudos — Dry Bean Dataset

Este directorio almacena los datos originales descargados directamente desde UCI Machine Learning Repository.
No se versionan archivos de datos en este repositorio. Ver política de versionado más abajo.

## Identificación del dataset

| Campo           | Valor                                      |
|-----------------|--------------------------------------------|
| Nombre          | Dry Bean Dataset                           |
| Fuente          | UCI Machine Learning Repository            |
| ID UCI          | 602                                        |
| Variable objetivo | `Class`                                  |
| Instancias      | 13,611                                     |
| Features        | 16 (numéricas)                             |
| Clases          | 7 (BARBUNYA, BOMBAY, CALI, DERMASON, HOROZ, SEKER, SIRA) |

Referencia estructural: [docs/tdsp-estructura-congelada.md](../../docs/tdsp-estructura-congelada.md)

## Procedimiento canónico de descarga

Usar el módulo `ucimlrepo` desde el entorno UV del proyecto:

```python
from ucimlrepo import fetch_ucirepo

dataset = fetch_ucirepo(id=602)
X = dataset.data.features   # DataFrame con las 16 features
y = dataset.data.targets    # DataFrame con la columna Class
```

La función `fetch_drybean()` de `src/data_loading.py` encapsula este procedimiento
y soporta cacheo local opcional en este directorio.

## Política de versionado

- Solo se versiona el archivo `.gitkeep` (marcador de carpeta vacía).
- **No** se versionan archivos `.csv`, `.xlsx`, `.parquet` ni ningún binario de datos.
- Los datos se descargan bajo demanda ejecutando `src/data_loading.py`.
- El `.gitignore` del repositorio excluye binarios en `data/raw/`.

## Plantilla de procedencia

Completar cada vez que se descarguen los datos en una nueva máquina o entorno:

| Campo              | Valor |
|--------------------|-------|
| Dataset            | Dry Bean Dataset (UCI 602) |
| Fuente             | https://archive.ics.uci.edu/dataset/602/dry+bean+dataset |
| Fecha de descarga  | AAAA-MM-DD |
| Responsable        | (nombre del integrante) |
| Hash SHA-256       | (opcional) |
| Versión ucimlrepo  | (ej. 0.0.7) |
| Notas              | (observaciones o incidencias) |
