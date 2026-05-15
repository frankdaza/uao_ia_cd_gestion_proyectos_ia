"""Pruebas unitarias para src.evaluation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.evaluation import (
    compare_models,
    plot_confusion_matrix,
    save_classification_report,
    select_best,
)

# ---------------------------------------------------------------------------
# Datos sintéticos y modelos entrenados
# ---------------------------------------------------------------------------

_CLASSES = ["SEKER", "BARBUNYA", "BOMBAY", "CALI"]


def _make_train_test() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Genera conjuntos de entrenamiento y prueba sintéticos."""
    n_train, n_test = 40, 12
    X_train = pd.DataFrame(
        {"f1": range(n_train), "f2": range(n_train, 2 * n_train)}, dtype=float
    )
    y_train = pd.Series((_CLASSES * (n_train // len(_CLASSES)))[:n_train], name="Class")
    X_test = pd.DataFrame(
        {"f1": range(n_test), "f2": range(n_test, 2 * n_test)}, dtype=float
    )
    y_test = pd.Series((_CLASSES * (n_test // len(_CLASSES)))[:n_test], name="Class")
    return X_train, X_test, y_train, y_test


@pytest.fixture(scope="module")
def modelos_y_datos():
    """Entrena dos modelos sintéticos reutilizables en los tests."""
    from src.models.baseline import train_baseline
    from src.models.random_forest import train_rf

    X_train, X_test, y_train, y_test = _make_train_test()
    modelo_lr = train_baseline(X_train, y_train)
    modelo_rf = train_rf(X_train, y_train)
    return {"baseline": modelo_lr, "random_forest": modelo_rf}, X_test, y_test


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCompareModels:
    """Verifica la comparación de modelos."""

    def test_retorna_dataframe(self, modelos_y_datos) -> None:
        """compare_models retorna un DataFrame."""
        models, X_test, y_test = modelos_y_datos
        resultado = compare_models(models, X_test, y_test)
        assert isinstance(resultado, pd.DataFrame)

    def test_columnas_correctas(self, modelos_y_datos) -> None:
        """El DataFrame tiene las columnas model, accuracy y f1_macro."""
        models, X_test, y_test = modelos_y_datos
        resultado = compare_models(models, X_test, y_test)
        assert "model" in resultado.columns
        assert "accuracy" in resultado.columns
        assert "f1_macro" in resultado.columns

    def test_una_fila_por_modelo(self, modelos_y_datos) -> None:
        """Hay una fila por cada modelo comparado."""
        models, X_test, y_test = modelos_y_datos
        resultado = compare_models(models, X_test, y_test)
        assert len(resultado) == len(models)


class TestSelectBest:
    """Verifica la selección del mejor modelo."""

    def test_retorna_nombre_valido(self, modelos_y_datos) -> None:
        """select_best retorna uno de los nombres del DataFrame."""
        models, X_test, y_test = modelos_y_datos
        comparison = compare_models(models, X_test, y_test)
        mejor = select_best(comparison)
        assert mejor in comparison["model"].values

    def test_selecciona_por_f1_macro(self, modelos_y_datos) -> None:
        """El modelo seleccionado tiene el f1_macro más alto."""
        models, X_test, y_test = modelos_y_datos
        comparison = compare_models(models, X_test, y_test)
        mejor = select_best(comparison, metric="f1_macro")
        idx = comparison[comparison["model"] == mejor].index[0]
        assert comparison.loc[idx, "f1_macro"] == comparison["f1_macro"].max()


class TestPlotConfusionMatrix:
    """Verifica la generación de la matriz de confusión."""

    def test_genera_archivo_png(self, modelos_y_datos, tmp_path) -> None:
        """plot_confusion_matrix guarda un archivo PNG en la ruta indicada."""
        models, X_test, y_test = modelos_y_datos
        output = tmp_path / "confusion_matrix.png"
        result = plot_confusion_matrix(
            models["baseline"], X_test, y_test, _CLASSES, output
        )
        assert result.exists()
        assert result.suffix == ".png"


class TestSaveClassificationReport:
    """Verifica el reporte de clasificación por clase."""

    def test_genera_archivo_txt(self, modelos_y_datos, tmp_path) -> None:
        """save_classification_report guarda un archivo .txt."""
        models, X_test, y_test = modelos_y_datos
        output = tmp_path / "report.txt"
        result = save_classification_report(
            models["baseline"], X_test, y_test, output
        )
        assert result.exists()
        assert result.suffix == ".txt"

    def test_contiene_nombres_de_clases(self, modelos_y_datos, tmp_path) -> None:
        """El reporte contiene los nombres de las clases."""
        models, X_test, y_test = modelos_y_datos
        output = tmp_path / "report.txt"
        save_classification_report(models["baseline"], X_test, y_test, output)
        contenido = output.read_text(encoding="utf-8")
        for clase in _CLASSES:
            assert clase in contenido
