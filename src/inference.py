"""Persistencia y predicción reutilizable para el laboratorio Dry Bean (UCI 602).

Cubre la fase de Despliegue de CRISP-DM: serializa el modelo seleccionado
con joblib y expone funciones de inferencia sobre nuevos registros.

Ejemplo de uso::

    from src.inference import load_model, predict, predict_one

    # Cargar modelo ya serializado
    model = load_model("outputs/models/random_forest_drybean.joblib")

    # Predecir sobre un DataFrame
    predicciones = predict(model, X_test)

    # Predecir un único registro como diccionario
    clase = predict_one(model, {
        "Area": 54386, "Perimeter": 887.35, "MajorAxisLength": 332.58,
        "MinorAxisLength": 208.45, "AspectRatio": 1.595, "Eccentricity": 0.778,
        "ConvexArea": 55132, "EquivDiameter": 263.2, "Extent": 0.761,
        "Solidity": 0.987, "Roundness": 0.868, "Compactness": 0.793,
        "ShapeFactor1": 0.00611, "ShapeFactor2": 0.00172,
        "ShapeFactor3": 0.629, "ShapeFactor4": 0.996,
    })
    print(clase)  # ej. 'SIRA'
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

# Tipo flexible: acepta pipeline en memoria o ruta al archivo .joblib
ModelOrPath = Pipeline | Path | str


def save_model(model: Pipeline, path: Path) -> Path:
    """Serializa el pipeline en disco usando joblib.

    Parámetros
    ----------
    model : Pipeline
        Pipeline ajustado a guardar.
    path : Path
        Ruta destino del archivo ``.joblib``.

    Retorna
    -------
    Path
        Ruta al archivo guardado.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return path


def load_model(path: Path) -> Pipeline:
    """Carga un pipeline previamente serializado con joblib.

    Parámetros
    ----------
    path : Path
        Ruta al archivo ``.joblib``.

    Retorna
    -------
    Pipeline
        Pipeline listo para predecir.
    """
    return joblib.load(Path(path))


def predict(model_or_path: ModelOrPath, X: pd.DataFrame) -> np.ndarray:
    """Genera predicciones sobre un DataFrame de features.

    Parámetros
    ----------
    model_or_path : Pipeline | Path | str
        Pipeline ajustado o ruta a un archivo ``.joblib``.
    X : pd.DataFrame
        Features con las mismas columnas usadas en el entrenamiento.

    Retorna
    -------
    np.ndarray
        Array con las clases predichas para cada fila.
    """
    model = load_model(model_or_path) if not isinstance(model_or_path, Pipeline) else model_or_path
    return model.predict(X)


def predict_one(model_or_path: ModelOrPath, sample: dict) -> str:
    """Predice la clase de un único registro representado como diccionario.

    El diccionario debe contener exactamente las 16 features numéricas del
    Dry Bean Dataset en cualquier orden; internamente se construye un
    DataFrame de una fila antes de llamar al modelo.

    Parámetros
    ----------
    model_or_path : Pipeline | Path | str
        Pipeline ajustado o ruta a un archivo ``.joblib``.
    sample : dict
        Diccionario con los nombres de las features como claves y sus
        valores numéricos como valores.

    Retorna
    -------
    str
        Nombre de la clase predicha (ej. ``"SIRA"``).
    """
    X = pd.DataFrame([sample])
    result = predict(model_or_path, X)
    return str(result[0])


if __name__ == "__main__":
    from src.data_loading import fetch_drybean
    from src.models.random_forest import train_rf
    from src.preprocessing import clean, split

    print("Cargando y preparando datos...")
    _, _, df = fetch_drybean()
    df = clean(df)
    X_train, X_test, y_train, y_test = split(df, random_state=42)

    print("Entrenando modelo final (RandomForestClassifier)...")
    model = train_rf(X_train, y_train, random_state=42)

    model_path = Path("outputs/models/random_forest_drybean.joblib")
    save_model(model, model_path)
    print(f"Modelo guardado en {model_path}")

    # Verificación round-trip: cargar y predecir la primera fila del test
    model_cargado = load_model(model_path)
    primera_fila = X_test.iloc[[0]]
    clase_predicha = predict(model_cargado, primera_fila)[0]
    clase_real = y_test.iloc[0]

    print("\nPredicción de prueba:")
    print(f"  Clase real:     {clase_real}")
    print(f"  Clase predicha: {clase_predicha}")
    print(f"  Correcto: {clase_real == clase_predicha}")
