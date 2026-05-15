"""Pruebas unitarias para src.models.baseline."""

from __future__ import annotations

import pandas as pd

from src.models.baseline import (
    build_baseline_pipeline,
    evaluate_baseline,
    train_baseline,
)

# ---------------------------------------------------------------------------
# Datos sintéticos
# ---------------------------------------------------------------------------

_CLASSES = ["SEKER", "BARBUNYA", "BOMBAY", "CALI"]


def _make_train_test() -> (
    tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
):
    """Genera conjuntos de entrenamiento y prueba sintéticos."""
    n_train, n_test = 40, 12  # múltiplos de len(_CLASSES)=4
    X_train = pd.DataFrame(
        {"f1": range(n_train), "f2": range(n_train, 2 * n_train)},
        dtype=float,
    )
    y_train = pd.Series((_CLASSES * (n_train // len(_CLASSES)))[:n_train], name="Class")

    X_test = pd.DataFrame(
        {"f1": range(n_test), "f2": range(n_test, 2 * n_test)},
        dtype=float,
    )
    y_test = pd.Series((_CLASSES * (n_test // len(_CLASSES)))[:n_test], name="Class")

    return X_train, X_test, y_train, y_test


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestBuildBaselinePipeline:
    """Verifica la construcción del pipeline."""

    def test_retorna_pipeline(self) -> None:
        """build_baseline_pipeline retorna un Pipeline de scikit-learn."""
        from sklearn.pipeline import Pipeline

        pipe = build_baseline_pipeline()
        assert isinstance(pipe, Pipeline)

    def test_tiene_scaler_y_lr(self) -> None:
        """El pipeline contiene StandardScaler y LogisticRegression."""
        pipe = build_baseline_pipeline()
        nombres = [nombre for nombre, _ in pipe.steps]
        assert "scaler" in nombres
        assert "lr" in nombres


class TestTrainBaseline:
    """Verifica el entrenamiento del baseline."""

    def test_pipeline_ajustado(self) -> None:
        """train_baseline retorna un pipeline que puede predecir."""
        X_train, X_test, y_train, _ = _make_train_test()
        model = train_baseline(X_train, y_train)
        preds = model.predict(X_test)
        assert len(preds) == len(X_test)


class TestEvaluateBaseline:
    """Verifica la evaluación del modelo."""

    def test_metricas_presentes(self) -> None:
        """evaluate_baseline retorna accuracy y f1_macro."""
        X_train, X_test, y_train, y_test = _make_train_test()
        model = train_baseline(X_train, y_train)
        metrics = evaluate_baseline(model, X_test, y_test)
        assert "accuracy" in metrics
        assert "f1_macro" in metrics

    def test_metricas_en_rango(self) -> None:
        """Las métricas están entre 0 y 1."""
        X_train, X_test, y_train, y_test = _make_train_test()
        model = train_baseline(X_train, y_train)
        metrics = evaluate_baseline(model, X_test, y_test)
        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert 0.0 <= metrics["f1_macro"] <= 1.0

    def test_metricas_son_float(self) -> None:
        """Los valores de las métricas son float (serializables a JSON)."""
        X_train, X_test, y_train, y_test = _make_train_test()
        model = train_baseline(X_train, y_train)
        metrics = evaluate_baseline(model, X_test, y_test)
        assert isinstance(metrics["accuracy"], float)
        assert isinstance(metrics["f1_macro"], float)
