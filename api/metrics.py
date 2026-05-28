"""Métricas Prometheus y middleware HTTP para la API Forescast."""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from typing import TYPE_CHECKING

from prometheus_client import Counter, Gauge, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.config import MLFLOW_TRACKING_URI

if TYPE_CHECKING:
    from fastapi import FastAPI

# ---------- Predicción (/predict) ----------
PREDICTIONS_TOTAL = Counter(
    "forescast_predictions_total",
    "Total de predicciones servidas",
    ["series", "model"],
)
PREDICTION_ERRORS_TOTAL = Counter(
    "forescast_prediction_errors_total",
    "Total de errores en /predict",
    ["error_type"],
)
PREDICTION_LATENCY = Histogram(
    "forescast_prediction_latency_seconds",
    "Latencia de /predict en segundos",
)

# ---------- HTTP (middleware) ----------
HTTP_REQUESTS_TOTAL = Counter(
    "forescast_http_requests_total",
    "Total de requests HTTP",
    ["method", "endpoint", "status"],
)
HTTP_REQUEST_DURATION = Histogram(
    "forescast_http_request_duration_seconds",
    "Duración de requests HTTP en segundos",
    ["method", "endpoint"],
)

# ---------- Estado del sistema ----------
MODEL_LOADED = Gauge(
    "forescast_model_loaded",
    "1 si el joblib del modelo existe en disco, 0 si no",
)
MLFLOW_REACHABLE = Gauge(
    "forescast_mlflow_reachable",
    "1 si MLflow responde en /health, 0 si no",
)
MODEL_INFO_ERRORS_TOTAL = Counter(
    "forescast_model_info_errors_total",
    "Total de errores en /model-info",
    ["error_type"],
)

_MLFLOW_PROBE_TIMEOUT_S = 2.0


def _normalize_endpoint(path: str) -> str:
    """Reduce cardinalidad: rutas fijas de la API."""
    if path in ("/", "/health", "/model-info", "/metrics", "/predict", "/docs", "/openapi.json"):
        return path
    if path.startswith("/docs"):
        return "/docs"
    return "other"


def probe_mlflow_health() -> bool:
    """Comprueba MLFLOW_TRACKING_URI/health con timeout corto."""
    base = MLFLOW_TRACKING_URI.rstrip("/")
    url = f"{base}/health"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=_MLFLOW_PROBE_TIMEOUT_S) as resp:
            return resp.status == 200
    except (urllib.error.URLError, OSError, TimeoutError, ValueError):
        return False


def refresh_mlflow_reachable() -> None:
    MLFLOW_REACHABLE.set(1.0 if probe_mlflow_health() else 0.0)


def set_model_loaded(loaded: bool) -> None:
    MODEL_LOADED.set(1.0 if loaded else 0.0)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        if path == "/metrics":
            return await call_next(request)

        method = request.method
        endpoint = _normalize_endpoint(path)
        start = time.perf_counter()
        status = "500"

        try:
            response = await call_next(request)
            status = str(response.status_code)
            return response
        except Exception:
            status = "500"
            raise
        finally:
            elapsed = time.perf_counter() - start
            HTTP_REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(elapsed)
            HTTP_REQUESTS_TOTAL.labels(
                method=method,
                endpoint=endpoint,
                status=status,
            ).inc()


def register_metrics(app: FastAPI, *, model_path_exists: bool) -> None:
    """Registra middleware y actualiza gauges de arranque."""
    set_model_loaded(model_path_exists)
    refresh_mlflow_reachable()
    app.add_middleware(PrometheusMiddleware)
