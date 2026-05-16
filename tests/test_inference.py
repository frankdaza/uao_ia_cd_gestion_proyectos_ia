"""Pruebas unitarias para src.inference."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.inference import load_model, predict, predict_one, save_model

# ---------------------------------------------------------------------------
# Datos sintéticos y modelo entrenado
# ---------------------------------------------------------------------------

_CLASSES = ["SEKER", "BARBUNYA", "BOMBAY", "CALI"]


@pytest.fixture(scope="module")
def modelo_entrenado():
    """Entrena un pipeline reutilizable para todos los tests del módulo."""
    from src.models.random_forest import train_rf

    n = 40
    X = pd.DataFrame({"f1": range(n), "f2": range(n, 2 * n)}, dtype=float)
    y = pd.Series((_CLASSES * (n // len(_CLASSES)))[:n], name="Class")
    return train_rf(X, y)


@pytest.fixture(scope="module")
def datos_prueba():
    """Genera un conjunto de prueba sintético."""
    n = 12
    X = pd.DataFrame({"f1": range(n), "f2": range(n, 2 * n)}, dtype=float)
    y = pd.Series((_CLASSES * (n // len(_CLASSES)))[:n], name="Class")
    return X, y


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestSaveLoadModel:
    """Verifica la persistencia del modelo."""

    def test_save_crea_archivo(self, modelo_entrenado, tmp_path) -> None:
        """save_model crea el archivo .joblib en la ruta indicada."""
        path = tmp_path / "modelo.joblib"
        resultado = save_model(modelo_entrenado, path)
        assert resultado.exists()

    def test_load_retorna_pipeline(self, modelo_entrenado, tmp_path) -> None:
        """load_model retorna un Pipeline de scikit-learn."""
        from sklearn.pipeline import Pipeline

        path = tmp_path / "modelo.joblib"
        save_model(modelo_entrenado, path)
        modelo_cargado = load_model(path)
        assert isinstance(modelo_cargado, Pipeline)

    def test_round_trip_mantiene_predicciones(
        self, modelo_entrenado, datos_prueba, tmp_path
    ) -> None:
        """El modelo cargado produce las mismas predicciones que el original."""
        X_test, _ = datos_prueba
        path = tmp_path / "modelo.joblib"
        save_model(modelo_entrenado, path)
        modelo_cargado = load_model(path)

        pred_original = modelo_entrenado.predict(X_test)
        pred_cargado = modelo_cargado.predict(X_test)
        np.testing.assert_array_equal(pred_original, pred_cargado)


class TestPredict:
    """Verifica la función predict."""

    def test_retorna_array(self, modelo_entrenado, datos_prueba) -> None:
        """predict retorna un array numpy."""
        X_test, _ = datos_prueba
        resultado = predict(modelo_entrenado, X_test)
        assert isinstance(resultado, np.ndarray)

    def test_longitud_correcta(self, modelo_entrenado, datos_prueba) -> None:
        """predict retorna una predicción por fila."""
        X_test, _ = datos_prueba
        resultado = predict(modelo_entrenado, X_test)
        assert len(resultado) == len(X_test)

    def test_acepta_ruta_joblib(self, modelo_entrenado, datos_prueba, tmp_path) -> None:
        """predict acepta una ruta a .joblib además de un pipeline."""
        X_test, _ = datos_prueba
        path = tmp_path / "modelo.joblib"
        save_model(modelo_entrenado, path)
        resultado = predict(path, X_test)
        assert len(resultado) == len(X_test)


class TestPredictOne:
    """Verifica la predicción de un único registro."""

    def test_retorna_string(self, modelo_entrenado) -> None:
        """predict_one retorna un string con el nombre de la clase."""
        sample = {"f1": 5.0, "f2": 15.0}
        resultado = predict_one(modelo_entrenado, sample)
        assert isinstance(resultado, str)

    def test_clase_valida(self, modelo_entrenado) -> None:
        """La clase predicha pertenece al conjunto de clases conocidas."""
        sample = {"f1": 5.0, "f2": 15.0}
        resultado = predict_one(modelo_entrenado, sample)
        assert resultado in _CLASSES


class TestPredictOneColumnasUci:
    """Regresión: el ejemplo del docstring usa los nombres UCI 602 reales.

    El UCI Dry Bean Dataset entregado por ``fetch_ucirepo(id=602)`` publica
    los features con ``AspectRatio`` y ``Roundness`` (capitalizados, sin
    typos). Este test entrena un pipeline con esos nombres exactos y
    confirma que ``predict_one`` no rompe por mismatch de columnas si el
    usuario copia el ejemplo del docstring.
    """

    _UCI_COLUMNS = [
        "Area",
        "Perimeter",
        "MajorAxisLength",
        "MinorAxisLength",
        "AspectRatio",
        "Eccentricity",
        "ConvexArea",
        "EquivDiameter",
        "Extent",
        "Solidity",
        "Roundness",
        "Compactness",
        "ShapeFactor1",
        "ShapeFactor2",
        "ShapeFactor3",
        "ShapeFactor4",
    ]

    @pytest.fixture(scope="class")
    def modelo_uci(self):
        """Entrena un RF sobre datos sintéticos con las 16 columnas UCI reales."""
        from src.models.random_forest import train_rf

        n = 28
        rng = np.random.default_rng(42)
        X = pd.DataFrame(
            {col: rng.uniform(0.1, 100.0, n) for col in self._UCI_COLUMNS},
            dtype=float,
        )
        y = pd.Series((_CLASSES * (n // len(_CLASSES) + 1))[:n], name="Class")
        return train_rf(X, y)

    def test_predict_one_con_nombres_uci(self, modelo_uci) -> None:
        """Llamar ``predict_one`` con las claves UCI exactas no rompe."""
        sample = {col: 1.0 for col in self._UCI_COLUMNS}
        resultado = predict_one(modelo_uci, sample)
        assert resultado in _CLASSES
