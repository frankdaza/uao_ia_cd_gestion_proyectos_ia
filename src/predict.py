"""Inferencia con el mejor modelo entrenado en src.train.

Carga el bundle `models/sales_forecaster.joblib` generado por `src.train` y
expone funciones reutilizables para pronosticar las próximas N observaciones
de las series `valor_neto` y `valor_costo`.

Uso CLI:
    python -m src.predict --days 30 --series valor_neto
    python -m src.predict --days 14 --series valor_costo --json

Uso como librería:
    from src.predict import load_model, predict_next_days
    df = predict_next_days(days=30, unique_id="valor_neto")
"""

from __future__ import annotations

import argparse
import json
from typing import Any

import joblib
import pandas as pd

from src.config import MODELS_DIR

MODEL_PATH = MODELS_DIR / "sales_forecaster.joblib"
VALID_SERIES = ("valor_neto", "valor_costo")


def load_model() -> dict[str, Any]:
    """Carga el bundle {forecaster, best_model} guardado por src.train.

    Returns:
        dict con claves "forecaster" (StatsForecast entrenado) y "best_model"
        (str con el nombre del modelo ganador en el backtest).

    Raises:
        FileNotFoundError: si no se ha entrenado todavía.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró {MODEL_PATH}. Ejecuta primero `python -m src.train`."
        )
    bundle = joblib.load(MODEL_PATH)
    if "forecaster" not in bundle or "best_model" not in bundle:
        raise ValueError(
            "El bundle de modelo es inválido: faltan claves 'forecaster' o 'best_model'."
        )
    return bundle


def predict_next_days(days: int, unique_id: str = "valor_neto") -> pd.DataFrame:
    """Pronostica los próximos `days` días para una serie.

    Args:
        days: número de días a pronosticar (> 0).
        unique_id: serie a pronosticar — "valor_neto" o "valor_costo".

    Returns:
        DataFrame con columnas:
            - ds: fecha del pronóstico
            - y_hat: valor pronosticado por el mejor modelo
            - model: nombre del modelo usado

    Raises:
        ValueError: si `days <= 0` o `unique_id` no es válido.
    """
    if not isinstance(days, int) or days <= 0:
        raise ValueError(f"`days` debe ser un entero positivo, recibí {days!r}.")
    if unique_id not in VALID_SERIES:
        raise ValueError(
            f"`unique_id` debe ser uno de {VALID_SERIES}, recibí {unique_id!r}."
        )

    bundle = load_model()
    forecaster = bundle["forecaster"]
    best_model = bundle["best_model"]

    forecast_df = forecaster.forecast(h=days)
    forecast_df = forecast_df.reset_index() if "unique_id" not in forecast_df.columns else forecast_df

    series_df = forecast_df[forecast_df["unique_id"] == unique_id].copy()
    if series_df.empty:
        raise ValueError(
            f"El forecaster no produjo predicciones para `{unique_id}`. "
            f"Series disponibles: {sorted(forecast_df['unique_id'].unique())}."
        )

    out = series_df[["ds", best_model]].rename(columns={best_model: "y_hat"})
    out["model"] = best_model
    out = out.reset_index(drop=True)
    return out


def _format_money(value: float) -> str:
    return f"{value:>20,.0f}"


def _print_human(df: pd.DataFrame, unique_id: str) -> None:
    print(f"\nPronóstico de `{unique_id}` con modelo `{df['model'].iloc[0]}`:")
    print("-" * 50)
    print(f"{'Fecha':<12}{'Pronóstico':>20}")
    print("-" * 50)
    for _, row in df.iterrows():
        fecha = pd.to_datetime(row["ds"]).strftime("%Y-%m-%d")
        print(f"{fecha:<12}{_format_money(row['y_hat'])}")
    print("-" * 50)
    print(f"Total {len(df):>2} días: {_format_money(df['y_hat'].sum())}")
    print(f"Promedio diario:    {_format_money(df['y_hat'].mean())}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pronóstico de ventas con el mejor modelo entrenado.")
    parser.add_argument("--days", type=int, default=30, help="Días a pronosticar (default: 30).")
    parser.add_argument(
        "--series",
        type=str,
        default="valor_neto",
        choices=list(VALID_SERIES),
        help="Serie a pronosticar (default: valor_neto).",
    )
    parser.add_argument("--json", action="store_true", help="Salida en JSON en vez de tabla.")
    args = parser.parse_args()

    df = predict_next_days(days=args.days, unique_id=args.series)

    if args.json:
        payload = {
            "series": args.series,
            "model": df["model"].iloc[0],
            "horizon": int(len(df)),
            "predictions": [
                {"ds": pd.to_datetime(r["ds"]).strftime("%Y-%m-%d"), "y_hat": float(r["y_hat"])}
                for _, r in df.iterrows()
            ],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        _print_human(df, args.series)


if __name__ == "__main__":
    main()
