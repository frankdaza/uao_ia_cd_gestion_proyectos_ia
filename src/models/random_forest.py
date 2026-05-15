"""Modelo alternativo: Pipeline(RandomForestClassifier).

Implementa la fase de Modelado de CRISP-DM con un ensamble de árboles
como alternativa al baseline lineal para el laboratorio Dry Bean (UCI 602).

Random Forest no requiere escalado previo, por lo que el Pipeline tiene un
único paso. Se mantiene Pipeline por consistencia con baseline.py y para
facilitar la persistencia con joblib (TASK-14).

Hiperparámetros elegidos:
- n_estimators=300: compromiso entre estabilidad del ensamble y tiempo de entrenamiento.
- max_depth=None: los árboles crecen hasta nodos puros; el ensamble controla el sobreajuste.
- random_state=42: reproducibilidad garantizada entre ejecuciones.
- n_jobs=-1: usa todos los núcleos disponibles para acelerar el entrenamiento.

Ejemplo de uso::

    from src.models.random_forest import build_rf_pipeline, train_rf, evaluate_rf

    pipeline = train_rf(X_train, y_train)
    metrics = evaluate_rf(pipeline, X_test, y_test)
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline


def build_rf_pipeline(
    n_estimators: int = 300,
    max_depth: int | None = None,
    random_state: int = 42,
    n_jobs: int = -1,
) -> Pipeline:
    """Construye el pipeline con RandomForestClassifier.

    Parámetros
    ----------
    n_estimators : int
        Número de árboles en el ensamble.
    max_depth : int | None
        Profundidad máxima de cada árbol. ``None`` crece hasta nodos puros.
    random_state : int
        Semilla para reproducibilidad.
    n_jobs : int
        Número de núcleos a usar. ``-1`` usa todos los disponibles.

    Retorna
    -------
    Pipeline
        Pipeline de scikit-learn listo para ajustar.
    """
    return Pipeline(
        [
            (
                "rf",
                RandomForestClassifier(
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    random_state=random_state,
                    n_jobs=n_jobs,
                ),
            )
        ]
    )


def train_rf(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_estimators: int = 300,
    max_depth: int | None = None,
    random_state: int = 42,
    n_jobs: int = -1,
) -> Pipeline:
    """Entrena el pipeline RandomForest con los datos de entrenamiento.

    Parámetros
    ----------
    X_train : pd.DataFrame
        Features de entrenamiento.
    y_train : pd.Series
        Variable objetivo de entrenamiento.
    n_estimators : int
        Número de árboles en el ensamble.
    max_depth : int | None
        Profundidad máxima de cada árbol.
    random_state : int
        Semilla para reproducibilidad.
    n_jobs : int
        Número de núcleos a usar.

    Retorna
    -------
    Pipeline
        Pipeline ajustado.
    """
    pipeline = build_rf_pipeline(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=n_jobs,
    )
    pipeline.fit(X_train, y_train)
    return pipeline


def evaluate_rf(
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

    print("Cargando Dry Bean Dataset (UCI 602)...")
    _, _, df = fetch_drybean()
    df = clean(df)
    X_train, X_test, y_train, y_test = split(df, random_state=42)

    print("Entrenando modelo alternativo (RandomForestClassifier)...")
    model = train_rf(X_train, y_train, random_state=42)

    metrics = evaluate_rf(model, X_test, y_test)
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1 macro: {metrics['f1_macro']:.4f}")

    output_path = Path("outputs/reports/metrics_rf.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=True))
    print(f"Métricas guardadas en {output_path}")
