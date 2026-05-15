"""Modelo baseline: Pipeline(StandardScaler + LogisticRegression).

Implementa la fase de Modelado de CRISP-DM con un clasificador lineal
como referencia inferior para el laboratorio Dry Bean (UCI 602).

Ejemplo de uso::

    from src.models.baseline import build_baseline_pipeline, train_baseline, evaluate_baseline

    pipeline = train_baseline(X_train, y_train)
    metrics = evaluate_baseline(pipeline, X_test, y_test)
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_baseline_pipeline(
    random_state: int = 42,
    max_iter: int = 1000,
) -> Pipeline:
    """Construye el pipeline baseline (escalado + regresión logística).

    Parámetros
    ----------
    random_state : int
        Semilla para reproducibilidad del modelo.
    max_iter : int
        Iteraciones máximas para la convergencia del solver.

    Retorna
    -------
    Pipeline
        Pipeline de scikit-learn listo para ajustar.
    """
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("lr", LogisticRegression(max_iter=max_iter, random_state=random_state)),
        ]
    )


def train_baseline(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = 42,
    max_iter: int = 1000,
) -> Pipeline:
    """Entrena el pipeline baseline con los datos de entrenamiento.

    Parámetros
    ----------
    X_train : pd.DataFrame
        Features de entrenamiento.
    y_train : pd.Series
        Variable objetivo de entrenamiento.
    random_state : int
        Semilla para reproducibilidad.
    max_iter : int
        Iteraciones máximas para convergencia.

    Retorna
    -------
    Pipeline
        Pipeline ajustado.
    """
    pipeline = build_baseline_pipeline(random_state=random_state, max_iter=max_iter)
    pipeline.fit(X_train, y_train)
    return pipeline


def evaluate_baseline(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float]:
    """Evalúa el modelo con accuracy y F1 macro.

    Parámetros
    ----------
    model : Pipeline
        Modelo ajustado.
    X_test : pd.DataFrame
        Features de prueba.
    y_test : pd.Series
        Variable objetivo de prueba.

    Retorna
    -------
    dict[str, float]
        Diccionario con claves ``"accuracy"`` y ``"f1_macro"``.
    """
    y_pred = model.predict(X_test)
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
    }


if __name__ == "__main__":
    from src.data_loading import fetch_drybean
    from src.preprocessing import clean, split

    # Carga y preparación
    print("Cargando Dry Bean Dataset (UCI 602)...")
    _, _, df = fetch_drybean()
    df = clean(df)
    X_train, X_test, y_train, y_test = split(df, random_state=42)

    # Entrenamiento
    print("Entrenando modelo baseline (StandardScaler + LogisticRegression)...")
    model = train_baseline(X_train, y_train, random_state=42)

    # Evaluación
    metrics = evaluate_baseline(model, X_test, y_test)
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1 macro: {metrics['f1_macro']:.4f}")

    # Persistencia de métricas
    output_path = Path("outputs/reports/metrics_baseline.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=True))
    print(f"Métricas guardadas en {output_path}")
