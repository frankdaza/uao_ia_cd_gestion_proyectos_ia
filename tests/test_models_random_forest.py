"""Pruebas unitarias para src.models.random_forest."""

from __future__ import annotations

import pandas as pd

from src.models.random_forest import (
    build_rf_pipeline,
    evaluate_rf,
    train_rf,
)

# ---------------------------------------------------------------------------
# Datos sintéticos
# ---------------------------------------------------------------------------

_CLASSES = ["SEKER", "BARBUNYA", "BOMBAY", "CALI"]


def _make_train_test() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
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


class TestBuildRfPipeline:
    """Verifica la construcción del pipeline."""

    def test_retorna_pipeline(self) -> None:
        """build_rf_pipeline retorna un Pipeline de scikit-learn."""
        from sklearn.pipeline import Pipeline

        pipe = build_rf_pipeline()
        assert isinstance(pipe, Pipeline)

    def test_tiene_random_forest(self) -> None:
        """El pipeline contiene un RandomForestClassifier."""
        from sklearn.ensemble import RandomForestClassifier

        pipe = build_rf_pipeline()
        nombres = [nombre for nombre, _ in pipe.steps]
        assert "rf" in nombres
        assert isinstance(pipe.named_steps["rf"], RandomForestClassifier)

    def test_hiperparametros_por_defecto(self) -> None:
        """Los hiperparámetros por defecto son los esperados."""
        pipe = build_rf_pipeline()
        rf = pipe.named_steps["rf"]
        assert rf.n_estimators == 300
        assert rf.max_depth is None
        assert rf.random_state == 42
        assert rf.n_jobs == -1


class TestTrainRf:
    """Verifica el entrenamiento del modelo."""

    def test_pipeline_ajustado(self) -> None:
        """train_rf retorna un pipeline que puede predecir."""
        X_train, X_test, y_train, _ = _make_train_test()
        model = train_rf(X_train, y_train)
        preds = model.predict(X_test)
        assert len(preds) == len(X_test)


class TestEvaluateRf:
    """Verifica la evaluación del modelo."""

    def test_metricas_presentes(self) -> None:
        """evaluate_rf retorna accuracy y f1_macro."""
        X_train, X_test, y_train, y_test = _make_train_test()
        model = train_rf(X_train, y_train)
        metrics = evaluate_rf(model, X_test, y_test)
        assert "accuracy" in metrics
        assert "f1_macro" in metrics

    def test_metricas_en_rango(self) -> None:
        """Las métricas están entre 0 y 1."""
        X_train, X_test, y_train, y_test = _make_train_test()
        model = train_rf(X_train, y_train)
        metrics = evaluate_rf(model, X_test, y_test)
        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert 0.0 <= metrics["f1_macro"] <= 1.0

    def test_metricas_son_float(self) -> None:
        """Los valores de las métricas son float (serializables a JSON)."""
        X_train, X_test, y_train, y_test = _make_train_test()
        model = train_rf(X_train, y_train)
        metrics = evaluate_rf(model, X_test, y_test)
        assert isinstance(metrics["accuracy"], float)
        assert isinstance(metrics["f1_macro"], float)
