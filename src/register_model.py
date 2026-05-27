"""Registro del mejor modelo en MLflow Model Registry.

Envuelve el bundle joblib generado por `src.train` en un `mlflow.pyfunc`
custom, lo loguea como artefacto y lo registra como `sales-forecaster`.
Asigna el alias `production` a la última versión.

Si el MLflow tracking server no responde, hace fallback a tracking local
(`mlruns/`) y NO rompe la demo — el modelo local `models/sales_forecaster.joblib`
sigue siendo válido para la API.

Ejecutar:
    python -m src.register_model
"""

from __future__ import annotations

import json
import sys

import joblib
import mlflow
import mlflow.pyfunc
import pandas as pd
from mlflow.exceptions import MlflowException
from mlflow.tracking import MlflowClient

from src.config import (
    EXPERIMENT_NAME,
    METRICS_DIR,
    MLFLOW_TRACKING_URI,
    MODELS_DIR,
    REGISTERED_MODEL_NAME,
)

MODEL_PATH = MODELS_DIR / "sales_forecaster.joblib"
METRICS_JSON_PATH = METRICS_DIR / "train_metrics.json"
PRODUCTION_ALIAS = "production"


class ForescastModel(mlflow.pyfunc.PythonModel):
    """Wrapper PyFunc del bundle StatsForecast guardado por src.train.

    Espera un DataFrame de entrada con columnas:
        - days: int (horizonte a pronosticar)
        - unique_id: str (serie: "valor_neto" o "valor_costo")
    """

    def load_context(self, context):
        bundle = joblib.load(context.artifacts["bundle"])
        self._forecaster = bundle["forecaster"]
        self._best_model = bundle["best_model"]

    def predict(self, context, model_input: pd.DataFrame) -> pd.DataFrame:
        if model_input.empty:
            raise ValueError("model_input vacío.")
        days = int(model_input["days"].iloc[0])
        unique_id = str(model_input["unique_id"].iloc[0])

        forecast_df = self._forecaster.predict(h=days)
        if "unique_id" not in forecast_df.columns:
            forecast_df = forecast_df.reset_index()

        series_df = forecast_df[forecast_df["unique_id"] == unique_id].copy()
        out = series_df[["ds", self._best_model]].rename(
            columns={self._best_model: "y_hat"}
        )
        out["model"] = self._best_model
        return out.reset_index(drop=True)


def setup_mlflow() -> str:
    """Conecta a tracking server o cae a local. Devuelve el URI activo."""
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(EXPERIMENT_NAME)
        client = MlflowClient()
        client.search_experiments(max_results=1)
        return MLFLOW_TRACKING_URI
    except Exception as exc:
        print(f"[WARN] No se pudo conectar a {MLFLOW_TRACKING_URI}: {exc}")
        print("[WARN] Fallback a tracking local (file:./mlruns).")
        mlflow.set_tracking_uri("file:./mlruns")
        mlflow.set_experiment(EXPERIMENT_NAME)
        return "file:./mlruns"


def load_train_summary() -> dict:
    if not METRICS_JSON_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró {METRICS_JSON_PATH}. "
            "Ejecuta primero `python -m src.train`."
        )
    with METRICS_JSON_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def register_and_alias() -> dict:
    """Loguea el modelo PyFunc, lo registra y le pone el alias 'production'."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró {MODEL_PATH}. "
            "Ejecuta primero `python -m src.train`."
        )

    summary = load_train_summary()
    best_model = summary["best_model"]
    mape = summary["mape_by_model"].get(best_model)

    sample_input = pd.DataFrame(
        [{"days": 7, "unique_id": "valor_neto"}]
    )

    with mlflow.start_run(run_name=f"register_{best_model}") as run:
        mlflow.set_tag("source", "register_model.py")
        mlflow.set_tag("best_model", best_model)
        if mape is not None:
            mlflow.log_metric("MAPE_avg", float(mape))

        mlflow.pyfunc.log_model(
            name="sales_forecaster",
            python_model=ForescastModel(),
            artifacts={"bundle": str(MODEL_PATH)},
            input_example=sample_input,
            registered_model_name=REGISTERED_MODEL_NAME,
        )
        run_id = run.info.run_id

    client = MlflowClient()
    versions = client.search_model_versions(f"name='{REGISTERED_MODEL_NAME}'")
    if not versions:
        raise RuntimeError(
            f"El modelo se logueó pero no aparece en el registry {REGISTERED_MODEL_NAME!r}."
        )
    latest = max(versions, key=lambda v: int(v.version))

    try:
        client.set_registered_model_alias(
            REGISTERED_MODEL_NAME, PRODUCTION_ALIAS, latest.version
        )
        alias_set = True
    except MlflowException as exc:
        print(f"[WARN] No se pudo asignar alias 'production': {exc}")
        alias_set = False

    return {
        "run_id": run_id,
        "registered_model_name": REGISTERED_MODEL_NAME,
        "version": latest.version,
        "alias": PRODUCTION_ALIAS if alias_set else None,
        "best_model": best_model,
        "mape": mape,
    }


def main() -> int:
    print("=" * 60)
    print("Registro de modelo en MLflow Model Registry")
    print("=" * 60)

    try:
        tracking_uri = setup_mlflow()
        info = register_and_alias()
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return 2
    except MlflowException as exc:
        print(f"[ERROR] MLflow: {exc}")
        print(
            f"[INFO] La demo sigue funcionando con el modelo local "
            f"{MODEL_PATH} vía src.predict / api.main."
        )
        return 1

    print(f"\nTracking URI:    {tracking_uri}")
    print(f"Run ID:          {info['run_id']}")
    print(f"Modelo:          {info['registered_model_name']}")
    print(f"Versión:         {info['version']}")
    print(f"Alias:           {info['alias'] or '(no asignado)'}")
    print(f"Best baseline:   {info['best_model']}")
    if info["mape"] is not None:
        print(f"MAPE backtest:   {info['mape']:.2f} %")
    print("\nLista en la UI:  Experiments → Models → "
          f"{REGISTERED_MODEL_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
