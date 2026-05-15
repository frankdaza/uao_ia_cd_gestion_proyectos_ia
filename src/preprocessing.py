"""Preparación de datos para el laboratorio Dry Bean (CRISP-DM).

Funciones puras para limpieza y partición del dataset.
No incluye transformaciones que dependan del modelo (escalado, encoding),
ya que eso vive dentro del ``Pipeline`` de scikit-learn.

Ejemplo de uso::

    from src.data_loading import fetch_drybean
    from src.preprocessing import clean, split

    _, _, df = fetch_drybean()
    df_limpio = clean(df)
    X_train, X_test, y_train, y_test = split(df_limpio)
"""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia el dataframe eliminando duplicados y filas con nulos en features.

    Parámetros
    ----------
    df : pd.DataFrame
        Dataframe con features numéricas y columna ``Class``.

    Retorna
    -------
    pd.DataFrame
        Copia del dataframe sin duplicados ni filas con valores nulos.

    Excepciones
    -----------
    ValueError
        Si la columna ``Class`` contiene valores nulos después de la limpieza.
    """
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()
    df_clean = df_clean.dropna()

    if df_clean["Class"].isna().any():
        raise ValueError("La columna 'Class' contiene valores nulos tras la limpieza.")

    return df_clean.reset_index(drop=True)


def split(
    df: pd.DataFrame,
    target: str = "Class",
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Particiona el dataframe en conjuntos de entrenamiento y prueba con estratificación.

    Parámetros
    ----------
    df : pd.DataFrame
        Dataframe limpio con features y columna objetivo.
    target : str
        Nombre de la columna objetivo (por defecto ``"Class"``).
    test_size : float
        Proporción del conjunto de prueba (por defecto ``0.2``).
    random_state : int
        Semilla para reproducibilidad (por defecto ``42``).

    Retorna
    -------
    tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
        ``(X_train, X_test, y_train, y_test)`` con partición estratificada
        respecto a la variable objetivo.
    """
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test
