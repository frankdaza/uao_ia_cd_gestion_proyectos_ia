"""Métricas Prometheus para la app Streamlit (puerto 8502)."""

from __future__ import annotations

from prometheus_client import Counter, start_http_server

STREAMLIT_FORECAST_REQUESTS = Counter(
    "forescast_streamlit_forecast_requests_total",
    "Pronósticos generados desde Streamlit",
    ["source"],
)
STREAMLIT_ERRORS = Counter(
    "forescast_streamlit_errors_total",
    "Errores en la app Streamlit",
    ["error_type"],
)

_METRICS_STARTED = False
METRICS_PORT = 8502


def start_metrics_server() -> None:
    """Expone /metrics en un hilo daemon (idempotente)."""
    global _METRICS_STARTED
    if _METRICS_STARTED:
        return
    start_http_server(METRICS_PORT)
    _METRICS_STARTED = True
