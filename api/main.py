"""FastAPI para servir pronósticos de ventas.

Endpoints:
- GET  /health       — liveness probe (200 si la app respira).
- GET  /model-info   — metadatos del modelo activo y métricas del último train.
- POST /predict      — pronostica los próximos N días para una serie.
- GET  /metrics      — métricas Prometheus (cantidad, latencia, errores).

Levantar local:
    uvicorn api.main:app --reload --port 8000

Docs interactivas: http://127.0.0.1:8000/docs
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from typing import Literal

import mlflow
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel, Field, field_validator

from api.metrics import (
    MODEL_INFO_ERRORS_TOTAL,
    PREDICTION_ERRORS_TOTAL,
    PREDICTION_LATENCY,
    PREDICTIONS_TOTAL,
    refresh_mlflow_reachable,
    register_metrics,
    set_model_loaded,
)
from src import observability  # noqa: F401  side-effect: init MLflow tracing
from src.config import METRICS_DIR, MODELS_DIR
from src.predict import VALID_SERIES, load_model, predict_next_days

MODEL_PATH = MODELS_DIR / "sales_forecaster.joblib"
METRICS_JSON_PATH = METRICS_DIR / "train_metrics.json"

# ---------- App ----------
app = FastAPI(
    title="Forescast API",
    description="Servicio de pronóstico de ventas — Forescast_Project (UAO).",
    version="0.1.0",
)

register_metrics(app, model_path_exists=MODEL_PATH.exists())


# ---------- Schemas ----------
class PredictRequest(BaseModel):
    days: int = Field(default=30, ge=1, le=180, description="Días a pronosticar.")
    series: Literal["valor_neto", "valor_costo"] = Field(
        default="valor_neto", description="Serie a pronosticar."
    )

    @field_validator("series")
    @classmethod
    def _check_series(cls, v: str) -> str:
        if v not in VALID_SERIES:
            raise ValueError(f"`series` debe ser uno de {VALID_SERIES}.")
        return v


class PredictionPoint(BaseModel):
    ds: str = Field(..., description="Fecha del pronóstico (YYYY-MM-DD).")
    y_hat: float = Field(..., description="Valor pronosticado.")


class PredictResponse(BaseModel):
    series: str
    model: str
    horizon: int
    predictions: list[PredictionPoint]
    total: float
    average: float


class ModelInfoResponse(BaseModel):
    best_model: str
    available_series: list[str]
    model_path: str
    model_exists: bool
    last_modified: str | None = None
    mape_by_model: dict[str, float] | None = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


# ---------- Endpoints ----------
@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    loaded = MODEL_PATH.exists()
    set_model_loaded(loaded)
    refresh_mlflow_reachable()
    return HealthResponse(status="ok", model_loaded=loaded)


@app.get("/model-info", response_model=ModelInfoResponse, tags=["model"])
@mlflow.trace(name="api.model_info", attributes={"stage": "api"})
def model_info() -> ModelInfoResponse:
    if not MODEL_PATH.exists():
        MODEL_INFO_ERRORS_TOTAL.labels(error_type="model_not_found").inc()
        set_model_loaded(False)
        raise HTTPException(
            status_code=503,
            detail="Modelo no entrenado. Correr `python -m src.train` primero.",
        )

    set_model_loaded(True)

    try:
        bundle = load_model()
    except Exception as exc:
        MODEL_INFO_ERRORS_TOTAL.labels(error_type="internal").inc()
        raise HTTPException(status_code=500, detail=f"Error al cargar modelo: {exc}") from exc

    last_mod = datetime.fromtimestamp(MODEL_PATH.stat().st_mtime).isoformat()

    mape_by_model: dict[str, float] | None = None
    if METRICS_JSON_PATH.exists():
        try:
            with METRICS_JSON_PATH.open(encoding="utf-8") as f:
                mape_by_model = json.load(f).get("mape_by_model")
        except (OSError, json.JSONDecodeError):
            mape_by_model = None

    return ModelInfoResponse(
        best_model=bundle["best_model"],
        available_series=list(VALID_SERIES),
        model_path=str(MODEL_PATH),
        model_exists=True,
        last_modified=last_mod,
        mape_by_model=mape_by_model,
    )


@app.post("/predict", response_model=PredictResponse, tags=["forecast"])
@mlflow.trace(name="api.predict", attributes={"stage": "api", "type": "inference"})
def predict(req: PredictRequest) -> PredictResponse:
    start = time.perf_counter()
    try:
        df = predict_next_days(days=req.days, unique_id=req.series)
    except FileNotFoundError as exc:
        PREDICTION_ERRORS_TOTAL.labels(error_type="model_not_found").inc()
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        PREDICTION_ERRORS_TOTAL.labels(error_type="validation").inc()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        PREDICTION_ERRORS_TOTAL.labels(error_type="internal").inc()
        raise HTTPException(status_code=500, detail=f"Error interno: {exc}") from exc
    finally:
        PREDICTION_LATENCY.observe(time.perf_counter() - start)

    model_used = str(df["model"].iloc[0])
    PREDICTIONS_TOTAL.labels(series=req.series, model=model_used).inc(len(df))

    points = [
        PredictionPoint(
            ds=row["ds"].strftime("%Y-%m-%d") if hasattr(row["ds"], "strftime") else str(row["ds"]),
            y_hat=float(row["y_hat"]),
        )
        for _, row in df.iterrows()
    ]

    return PredictResponse(
        series=req.series,
        model=model_used,
        horizon=len(points),
        predictions=points,
        total=float(df["y_hat"].sum()),
        average=float(df["y_hat"].mean()),
    )


@app.get("/metrics", tags=["system"])
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {
        "service": "Forescast API",
        "docs": "/docs",
        "health": "/health",
        "predict": "POST /predict",
    }
