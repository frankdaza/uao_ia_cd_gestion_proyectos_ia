"""Tests de las métricas y utilidades de src.train."""

from __future__ import annotations

import numpy as np
import pytest

from src.train import average_mape_per_model, compute_metrics


def test_compute_metrics_perfect_prediction() -> None:
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    metrics = compute_metrics(y, y)
    assert metrics["MAE"] == pytest.approx(0.0)
    assert metrics["RMSE"] == pytest.approx(0.0)
    assert metrics["MAPE"] == pytest.approx(0.0)
    assert metrics["R2"] == pytest.approx(1.0)


def test_compute_metrics_handles_zero_in_y_true() -> None:
    y_true = np.array([0.0, 100.0, 200.0])
    y_pred = np.array([10.0, 110.0, 190.0])
    metrics = compute_metrics(y_true, y_pred)
    # MAPE ignora el 0 en y_true — sólo promedia los 2 válidos
    assert metrics["MAPE"] == pytest.approx(((10 / 100) + (10 / 200)) / 2 * 100)
    assert not np.isnan(metrics["MAE"])


def test_compute_metrics_constant_target_gives_undefined_r2() -> None:
    y_true = np.array([5.0, 5.0, 5.0])
    y_pred = np.array([5.1, 4.9, 5.0])
    metrics = compute_metrics(y_true, y_pred)
    assert np.isnan(metrics["R2"])


def test_average_mape_picks_lowest_as_best() -> None:
    metrics = {
        "A": {"s1": {"MAPE": 30.0}, "s2": {"MAPE": 20.0}},
        "B": {"s1": {"MAPE": 10.0}, "s2": {"MAPE": 12.0}},
        "C": {"s1": {"MAPE": np.nan}, "s2": {"MAPE": np.nan}},
    }
    result = average_mape_per_model(metrics)
    assert result["A"] == pytest.approx(25.0)
    assert result["B"] == pytest.approx(11.0)
    assert result["C"] == float("inf")
    best = min(result, key=result.get)
    assert best == "B"
