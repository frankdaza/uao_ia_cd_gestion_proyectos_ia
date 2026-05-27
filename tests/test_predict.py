"""Tests de src.predict.

Estos tests no requieren que exista un modelo entrenado: cubren las
validaciones de entrada y el manejo de errores. El happy path con un
modelo real está cubierto por la prueba manual del Demo Day.
"""

from __future__ import annotations

import pytest

from src.predict import VALID_SERIES, predict_next_days


def test_predict_next_days_rejects_zero_days() -> None:
    with pytest.raises(ValueError, match="entero positivo"):
        predict_next_days(days=0, unique_id="valor_neto")


def test_predict_next_days_rejects_negative_days() -> None:
    with pytest.raises(ValueError, match="entero positivo"):
        predict_next_days(days=-5, unique_id="valor_neto")


def test_predict_next_days_rejects_non_integer_days() -> None:
    with pytest.raises(ValueError, match="entero positivo"):
        predict_next_days(days=3.5, unique_id="valor_neto")  # type: ignore[arg-type]


def test_predict_next_days_rejects_unknown_series() -> None:
    with pytest.raises(ValueError, match="unique_id"):
        predict_next_days(days=7, unique_id="precio")


def test_valid_series_constant_matches_expected() -> None:
    assert "valor_neto" in VALID_SERIES
    assert "valor_costo" in VALID_SERIES
    assert len(VALID_SERIES) == 2
