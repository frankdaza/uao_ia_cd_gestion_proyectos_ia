"""Módulo de carga del Dry Bean Dataset (UCI 602).

Provee funciones para descargar el dataset desde el repositorio UCI
y para leer una copia local en formato Parquet o CSV.

Ejemplo de uso::

    from src.data_loading import fetch_drybean

    X, y, df = fetch_drybean()
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo


def fetch_drybean(
    cache_dir: Path | None = None,
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """Descarga el Dry Bean Dataset (UCI id 602) y retorna features, objetivo y dataframe completo.

    Parámetros
    ----------
    cache_dir : Path | None
        Directorio opcional para cachear el dataset en formato Parquet.
        Si existe ``cache_dir / "drybean.parquet"``, se lee de disco
        en lugar de descargar.

    Retorna
    -------
    tuple[pd.DataFrame, pd.Series, pd.DataFrame]
        ``(X, y, df)`` donde:
        - *X*: features numéricas (sin la columna ``Class``).
        - *y*: serie con la variable objetivo ``Class``.
        - *df*: dataframe completo (features + ``Class``).
    """
    cache_path = cache_dir / "drybean.parquet" if cache_dir is not None else None

    if cache_path is not None and cache_path.exists():
        df = pd.read_parquet(cache_path)
    else:
        dataset = fetch_ucirepo(id=602)
        features: pd.DataFrame = dataset.data.features
        targets: pd.DataFrame = dataset.data.targets
        df = pd.concat([features, targets], axis=1)

        if cache_path is not None:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(cache_path, index=False)

    y: pd.Series = df["Class"]
    X: pd.DataFrame = df.drop(columns=["Class"])
    return X, y, df


def load_drybean(path: Path) -> pd.DataFrame:
    """Lee un archivo local con el Dry Bean Dataset (Parquet o CSV).

    Parámetros
    ----------
    path : Path
        Ruta al archivo. Se elige el lector según la extensión:
        ``.parquet`` usa ``pd.read_parquet``; cualquier otra extensión
        usa ``pd.read_csv``.

    Retorna
    -------
    pd.DataFrame
        Dataframe completo con features y columna ``Class``.
    """
    path = Path(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)
