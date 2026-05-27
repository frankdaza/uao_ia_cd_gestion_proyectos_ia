"""Tests de la API FastAPI con TestClient.

Si no hay modelo entrenado en `models/sales_forecaster.joblib`, los tests
que dependen del modelo se saltan automáticamente (no fallan).
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import MODEL_PATH, app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def model_exists() -> bool:
    return MODEL_PATH.exists()


def test_root_returns_index(client: TestClient) -> None:
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert "service" in body
    assert "docs" in body


def test_health_endpoint_returns_ok(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert isinstance(body["model_loaded"], bool)


def test_metrics_endpoint_exposes_prometheus_format(client: TestClient) -> None:
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "text/plain" in r.headers["content-type"]
    assert "forescast_predictions_total" in r.text


def test_predict_rejects_zero_days(client: TestClient) -> None:
    r = client.post("/predict", json={"days": 0, "series": "valor_neto"})
    assert r.status_code == 422  # Pydantic validation (ge=1)


def test_predict_rejects_unknown_series(client: TestClient) -> None:
    r = client.post("/predict", json={"days": 7, "series": "precio"})
    assert r.status_code == 422  # Literal validation


def test_predict_rejects_days_above_limit(client: TestClient) -> None:
    r = client.post("/predict", json={"days": 999, "series": "valor_neto"})
    assert r.status_code == 422  # Pydantic validation (le=180)


def test_model_info_503_when_no_model(client: TestClient, model_exists: bool) -> None:
    if model_exists:
        pytest.skip("Hay modelo entrenado; el caso 503 no aplica.")
    r = client.get("/model-info")
    assert r.status_code == 503


def test_model_info_ok_when_model_exists(client: TestClient, model_exists: bool) -> None:
    if not model_exists:
        pytest.skip("No hay modelo entrenado; correr `python -m src.train`.")
    r = client.get("/model-info")
    assert r.status_code == 200
    body = r.json()
    assert "best_model" in body
    assert body["available_series"] == ["valor_neto", "valor_costo"]


def test_predict_happy_path_when_model_exists(client: TestClient, model_exists: bool) -> None:
    if not model_exists:
        pytest.skip("No hay modelo entrenado; correr `python -m src.train`.")
    r = client.post("/predict", json={"days": 7, "series": "valor_neto"})
    assert r.status_code == 200
    body = r.json()
    assert body["series"] == "valor_neto"
    assert body["horizon"] == 7
    assert len(body["predictions"]) == 7
    assert all("ds" in p and "y_hat" in p for p in body["predictions"])
    assert body["total"] > 0
    assert body["average"] > 0
