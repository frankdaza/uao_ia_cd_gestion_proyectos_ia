"""Entrenamiento de baselines de pronóstico con StatsForecast + MLflow.

Carga `data/processed/nixtla_format.csv` (generado por `src/featuring.py`),
entrena varios modelos de series de tiempo sobre las series `valor_neto` y
`valor_costo`, evalúa con backtest temporal (cross_validation) y registra todo
en MLflow. Guarda el mejor modelo localmente y un resumen de métricas en JSON.

Ejecutar como módulo:
    python -m src.train

Requisitos:
    - Haber corrido antes `python -m src.data` y `python -m src.featuring`.
    - Tener un MLflow tracking server escuchando en `MLFLOW_TRACKING_URI`
      (o aceptar el fallback a `mlruns/` local si no responde).
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import joblib
import mlflow
import numpy as np
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import (
    AutoARIMA,
    AutoETS,
    AutoTheta,
    HistoricAverage,
    MSTL,
    Naive,
    SeasonalNaive,
)

from src.config import (
    DF_NIXTLA_PATH,
    EXPERIMENT_NAME,
    METRICS_DIR,
    MLFLOW_TRACKING_URI,
    MODELS_DIR,
)

warnings.filterwarnings("ignore", category=FutureWarning)

# ---------- Parámetros del experimento ----------
FREQ = "D"                  # frecuencia diaria
HORIZON = 30                # pronóstico a 30 días vista
SEASON_WEEK = 7             # estacionalidad semanal
SEASON_MONTH = 30           # estacionalidad mensual (STL exige entero)
N_WINDOWS = 3               # ventanas de backtest
STEP_SIZE = HORIZON         # avance entre ventanas


def get_models() -> list:
    """Lista de modelos baseline + clásicos a comparar."""
    return [
        Naive(),
        HistoricAverage(),
        SeasonalNaive(season_length=SEASON_WEEK),
        AutoETS(season_length=SEASON_WEEK),
        AutoARIMA(season_length=SEASON_WEEK),
        AutoTheta(season_length=SEASON_WEEK),
        MSTL(season_length=[SEASON_WEEK, SEASON_MONTH]),
    ]


def load_nixtla_data() -> pd.DataFrame:
    """Carga el dataframe en formato Nixtla generado por featuring.py."""
    if not DF_NIXTLA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró {DF_NIXTLA_PATH}. "
            "Ejecuta primero `python -m src.data` y luego `python -m src.featuring`."
        )
    df = pd.read_csv(DF_NIXTLA_PATH, parse_dates=["ds"])
    return df[["unique_id", "ds", "y"]]


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """MAE, RMSE, MAPE y R² robustos a divisiones por cero."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

    mask = y_true != 0
    mape = (
        float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)
        if mask.any()
        else float("nan")
    )

    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return {"MAE": mae, "RMSE": rmse, "MAPE": mape, "R2": r2}


def evaluate_with_cv(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Backtest temporal con cross_validation de StatsForecast.

    Retorna:
        cv_df: predicciones por (unique_id, ds, cutoff, modelo).
        metrics_by_model_series: {modelo: {serie: {MAE, RMSE, MAPE, R2}}}.
    """
    sf = StatsForecast(models=get_models(), freq=FREQ, n_jobs=1)
    cv_df = sf.cross_validation(
        df=df,
        h=HORIZON,
        n_windows=N_WINDOWS,
        step_size=STEP_SIZE,
    )

    model_columns = [c for c in cv_df.columns if c not in ("unique_id", "ds", "cutoff", "y")]
    metrics_by_model_series: dict[str, dict[str, dict[str, float]]] = {}

    for model_name in model_columns:
        metrics_by_model_series[model_name] = {}
        for uid, group in cv_df.groupby("unique_id"):
            metrics_by_model_series[model_name][str(uid)] = compute_metrics(
                group["y"].values, group[model_name].values
            )

    return cv_df, metrics_by_model_series


def average_mape_per_model(metrics: dict) -> dict[str, float]:
    """Promedio de MAPE entre series para cada modelo (métrica de selección)."""
    result = {}
    for model, by_series in metrics.items():
        mapes = [
            m["MAPE"] for m in by_series.values()
            if m["MAPE"] is not None and not np.isnan(m["MAPE"])
        ]
        result[model] = float(np.mean(mapes)) if mapes else float("inf")
    return result


def setup_mlflow() -> bool:
    """Intenta conectar a MLflow remoto; si falla, usa tracking local en mlruns/."""
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(EXPERIMENT_NAME)
        return True
    except Exception as exc:
        print(f"[WARN] No se pudo conectar a MLflow en {MLFLOW_TRACKING_URI}: {exc}")
        print("[WARN] Fallback a tracking local en ./mlruns")
        mlflow.set_tracking_uri("file:./mlruns")
        mlflow.set_experiment(EXPERIMENT_NAME)
        return False


def log_run(
    model_name: str,
    metrics_by_series: dict[str, dict[str, float]],
    params: dict,
    artifact_path: Path | None = None,
) -> None:
    """Registra un run en MLflow con parámetros, métricas por serie y artefactos."""
    with mlflow.start_run(run_name=model_name):
        mlflow.log_params(params)
        mlflow.set_tag("model_family", model_name)
        for uid, m in metrics_by_series.items():
            for metric_name, value in m.items():
                if value is None or (isinstance(value, float) and np.isnan(value)):
                    continue
                mlflow.log_metric(f"{metric_name}_{uid}", value)
        if artifact_path is not None and artifact_path.exists():
            mlflow.log_artifact(str(artifact_path))


def train() -> dict:
    """Pipeline principal: carga datos, evalúa modelos, registra en MLflow, guarda mejor."""
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Entrenamiento de baselines de pronóstico con StatsForecast")
    print("=" * 60)

    df = load_nixtla_data()
    print(f"Datos: {len(df)} filas, {df['unique_id'].nunique()} series "
          f"({df['ds'].min().date()} → {df['ds'].max().date()})")

    setup_mlflow()
    cv_df, metrics = evaluate_with_cv(df)

    mape_by_model = average_mape_per_model(metrics)
    best_model = min(mape_by_model, key=mape_by_model.get)
    print(f"\nMAPE promedio por modelo (sobre todas las series):")
    for m, v in sorted(mape_by_model.items(), key=lambda x: x[1]):
        marker = "★" if m == best_model else " "
        print(f"  {marker} {m:<20s} MAPE = {v:6.2f}%")

    params_base = {
        "freq": FREQ,
        "horizon": HORIZON,
        "season_week": SEASON_WEEK,
        "season_month": SEASON_MONTH,
        "n_windows": N_WINDOWS,
        "step_size": STEP_SIZE,
    }

    cv_path = METRICS_DIR / "cv_predictions.csv"
    cv_df.to_csv(cv_path, index=False)

    for model_name, metrics_by_series in metrics.items():
        log_run(
            model_name=model_name,
            metrics_by_series=metrics_by_series,
            params={**params_base, "model": model_name},
            artifact_path=cv_path,
        )

    sf_final = StatsForecast(models=get_models(), freq=FREQ, n_jobs=1)
    sf_final.fit(df)
    model_path = MODELS_DIR / "sales_forecaster.joblib"
    joblib.dump({"forecaster": sf_final, "best_model": best_model}, model_path)
    print(f"\nMejor modelo: {best_model}")
    print(f"Modelo guardado en: {model_path}")

    summary = {
        "best_model": best_model,
        "mape_by_model": mape_by_model,
        "metrics_per_model_per_series": metrics,
        "params": params_base,
    }
    summary_path = METRICS_DIR / "train_metrics.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Métricas guardadas en: {summary_path}")

    return summary


if __name__ == "__main__":
    train()
