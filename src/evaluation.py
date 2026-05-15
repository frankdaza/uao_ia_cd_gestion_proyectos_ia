"""Evaluación comparativa de modelos para el laboratorio Dry Bean (UCI 602).

Módulo de la fase de Evaluación de CRISP-DM (PB-05). Compara el baseline
(LogisticRegression) y el modelo alternativo (RandomForest), genera la
matriz de confusión del mejor modelo y emite un reporte por clase.

Ejemplo de uso::

    from src.evaluation import compare_models, select_best, plot_confusion_matrix

    comparison = compare_models({"baseline": pipe_lr, "rf": pipe_rf}, X_test, y_test)
    mejor = select_best(comparison)
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # backend sin pantalla, necesario para CI headless
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    f1_score,
)
from sklearn.pipeline import Pipeline


def compare_models(
    models: dict[str, Pipeline],
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> pd.DataFrame:
    """Compara varios modelos calculando accuracy y F1 macro sobre el conjunto de prueba.

    Parámetros
    ----------
    models : dict[str, Pipeline]
        Diccionario con nombre del modelo como clave y pipeline ajustado como valor.
    X_test : pd.DataFrame
        Features de prueba.
    y_test : pd.Series
        Variable objetivo de prueba.

    Retorna
    -------
    pd.DataFrame
        DataFrame con columnas ``model``, ``accuracy`` y ``f1_macro``,
        una fila por modelo.
    """
    filas = []
    for nombre, modelo in models.items():
        y_pred = modelo.predict(X_test)
        filas.append({
            "model": nombre,
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
        })
    return pd.DataFrame(filas)


def select_best(
    comparison: pd.DataFrame,
    metric: str = "f1_macro",
) -> str:
    """Selecciona el nombre del modelo con el mejor valor en la métrica indicada.

    Parámetros
    ----------
    comparison : pd.DataFrame
        DataFrame retornado por ``compare_models``.
    metric : str
        Columna por la que se ordena (por defecto ``"f1_macro"``).

    Retorna
    -------
    str
        Nombre del modelo con el mejor desempeño.
    """
    idx = comparison[metric].idxmax()
    return str(comparison.loc[idx, "model"])


def plot_confusion_matrix(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    labels: list[str],
    output_path: Path,
) -> Path:
    """Genera y guarda la matriz de confusión del modelo como imagen PNG.

    Parámetros
    ----------
    model : Pipeline
        Modelo ajustado.
    X_test : pd.DataFrame
        Features de prueba.
    y_test : pd.Series
        Variable objetivo de prueba.
    labels : list[str]
        Nombres de las clases en el orden deseado para los ejes.
    output_path : Path
        Ruta donde se guarda el archivo PNG.

    Retorna
    -------
    Path
        Ruta al archivo guardado.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 7))
    ConfusionMatrixDisplay.from_estimator(
        model,
        X_test,
        y_test,
        display_labels=labels,
        cmap="Blues",
        ax=ax,
        colorbar=False,
    )
    ax.set_title("Matriz de confusión — modelo seleccionado", fontsize=13)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return output_path


def save_classification_report(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    output_path: Path,
) -> Path:
    """Genera y guarda el reporte de clasificación por clase en formato texto.

    Parámetros
    ----------
    model : Pipeline
        Modelo ajustado.
    X_test : pd.DataFrame
        Features de prueba.
    y_test : pd.Series
        Variable objetivo de prueba.
    output_path : Path
        Ruta donde se guarda el archivo .txt.

    Retorna
    -------
    Path
        Ruta al archivo guardado.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    y_pred = model.predict(X_test)
    labels = sorted(y_test.unique())
    report = classification_report(y_test, y_pred, target_names=labels)
    output_path.write_text(report, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    from src.data_loading import fetch_drybean
    from src.models.baseline import train_baseline
    from src.models.random_forest import train_rf
    from src.preprocessing import clean, split

    print("Cargando y preparando datos...")
    _, _, df = fetch_drybean()
    df = clean(df)
    X_train, X_test, y_train, y_test = split(df, random_state=42)

    print("Entrenando modelos...")
    modelo_baseline = train_baseline(X_train, y_train)
    modelo_rf = train_rf(X_train, y_train)

    print("Comparando modelos...")
    comparison = compare_models(
        {"baseline": modelo_baseline, "random_forest": modelo_rf},
        X_test,
        y_test,
    )
    print(comparison.to_string(index=False))

    mejor = select_best(comparison)
    print(f"\nMejor modelo: {mejor}")

    # Guardamos tabla comparativa
    comparison_path = Path("outputs/reports/comparison.csv")
    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    comparison["is_best"] = comparison["model"] == mejor
    comparison.to_csv(comparison_path, index=False)
    print(f"Comparación guardada en {comparison_path}")

    # Registramos el modelo seleccionado en JSON
    selected_path = Path("outputs/reports/selected_model.json")
    selected_path.write_text(
        json.dumps({"selected_model": mejor}, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    # Matriz de confusión del mejor modelo
    modelo_seleccionado = modelo_baseline if mejor == "baseline" else modelo_rf
    labels = sorted(y_test.unique())
    cm_path = plot_confusion_matrix(
        modelo_seleccionado, X_test, y_test, labels,
        Path("outputs/reports/confusion_matrix.png"),
    )
    print(f"Matriz de confusión guardada en {cm_path}")

    # Reporte por clase
    report_path = save_classification_report(
        modelo_seleccionado, X_test, y_test,
        Path("outputs/reports/classification_report.txt"),
    )
    print(f"Reporte de clasificación guardado en {report_path}")
