"""Streamlit demo del pipeline de pronóstico.

Consume la API FastAPI (`/predict`, `/model-info`) si está disponible y hace
fallback al módulo `src.predict` para que la demo no se rompa si el servicio
no está levantado.

Ejecutar:
    streamlit run app/streamlit_app.py

Asume que ya se ejecutó `python -m src.data`, `python -m src.featuring` y
`python -m src.train`.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

from src.config import DF_NIXTLA_PATH, METRICS_DIR
from src.predict import VALID_SERIES, predict_next_days

API_URL = "http://127.0.0.1:8000"
TRAIN_METRICS_PATH = METRICS_DIR / "train_metrics.json"


# ---------- Helpers ----------
def fmt_money(value: float) -> str:
    return f"$ {value:,.0f}"


def get_predictions(days: int, series: str) -> tuple[pd.DataFrame, str, str]:
    """Intenta llamar a la API; si falla, usa src.predict como fallback."""
    try:
        r = requests.post(
            f"{API_URL}/predict",
            json={"days": days, "series": series},
            timeout=20,
        )
        r.raise_for_status()
        payload = r.json()
        df = pd.DataFrame(payload["predictions"])
        df["ds"] = pd.to_datetime(df["ds"])
        return df, payload["model"], "API"
    except (requests.RequestException, ValueError):
        df = predict_next_days(days=days, unique_id=series)
        df["ds"] = pd.to_datetime(df["ds"])
        return df, str(df["model"].iloc[0]), "local"


@st.cache_data
def load_history() -> pd.DataFrame:
    if not DF_NIXTLA_PATH.exists():
        return pd.DataFrame(columns=["unique_id", "ds", "y"])
    df = pd.read_csv(DF_NIXTLA_PATH, parse_dates=["ds"])
    return df


@st.cache_data
def load_train_metrics() -> dict | None:
    if not TRAIN_METRICS_PATH.exists():
        return None
    import json
    with TRAIN_METRICS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


# ---------- UI ----------
st.set_page_config(
    page_title="Forescast — Pronóstico de ventas",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Forescast — Pronóstico de ventas")
st.caption(
    "MLOps para una cadena de supermercados en Cali. "
    "Maestría en IA y Ciencia de Datos · UAO."
)

with st.sidebar:
    st.header("Parámetros")
    series = st.selectbox(
        "Serie a pronosticar",
        list(VALID_SERIES),
        format_func=lambda s: "Ventas (valor neto)" if s == "valor_neto" else "Costo (valor costo)",
    )
    days = st.slider("Días a pronosticar", min_value=7, max_value=90, value=30, step=1)
    run = st.button("Generar pronóstico", type="primary", use_container_width=True)

    st.divider()
    st.subheader("Modelo activo")
    train_summary = load_train_metrics()
    if train_summary:
        st.metric("Best model", train_summary.get("best_model", "—"))
        mape = train_summary.get("mape_by_model", {}).get(train_summary.get("best_model"))
        if mape is not None:
            st.metric("MAPE backtest", f"{mape:.2f} %")
    else:
        st.warning("No hay métricas de entrenamiento aún. Correr `python -m src.train`.")

if not run:
    st.info("Ajusta los parámetros y haz clic en **Generar pronóstico**.")
    st.stop()

with st.spinner("Generando pronóstico..."):
    forecast_df, model_used, source = get_predictions(days, series)

# ---------- KPIs ----------
total = float(forecast_df["y_hat"].sum())
avg = float(forecast_df["y_hat"].mean())
peak_idx = forecast_df["y_hat"].idxmax()
peak_date = pd.to_datetime(forecast_df.loc[peak_idx, "ds"]).strftime("%Y-%m-%d")
peak_value = float(forecast_df.loc[peak_idx, "y_hat"])

c1, c2, c3, c4 = st.columns(4)
c1.metric(f"Total esperado ({days} días)", fmt_money(total))
c2.metric("Promedio diario", fmt_money(avg))
c3.metric("Día con mayor pronóstico", peak_date, fmt_money(peak_value))
c4.metric("Fuente", source.upper(), help="API si el servicio está activo, local si hay fallback.")

st.caption(f"Modelo usado: **{model_used}**")

# ---------- Gráfico histórico + pronóstico ----------
history = load_history()
hist_series = history[history["unique_id"] == series] if not history.empty else pd.DataFrame()

fig = go.Figure()
if not hist_series.empty:
    fig.add_trace(
        go.Scatter(
            x=hist_series["ds"],
            y=hist_series["y"],
            mode="lines",
            name="Histórico",
            line=dict(color="#2196F3", width=1.5),
        )
    )
fig.add_trace(
    go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["y_hat"],
        mode="lines+markers",
        name=f"Pronóstico ({model_used})",
        line=dict(color="#FF6D00", width=2),
        marker=dict(size=5),
    )
)
fig.update_layout(
    title=f"{'Ventas' if series == 'valor_neto' else 'Costo'} — histórico vs pronóstico",
    xaxis_title="Fecha",
    yaxis_title="Valor",
    height=420,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Tabla ----------
with st.expander("📋 Detalle del pronóstico"):
    display_df = forecast_df.copy()
    display_df["ds"] = display_df["ds"].dt.strftime("%Y-%m-%d")
    display_df["y_hat"] = display_df["y_hat"].map(lambda x: f"{x:,.0f}")
    display_df.columns = ["Fecha", "Pronóstico", "Modelo"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ---------- Cómo funciona ----------
with st.expander("ℹ️ Cómo funciona el MLOps"):
    st.markdown(
        """
        **Pipeline:**

        1. **Ingesta + limpieza** (`src/data.py`) — filtra columnas relevantes,
           imputa nulos por mes, elimina ventas negativas.
        2. **Feature engineering** (`src/featuring.py`) — agregación diaria,
           formato Nixtla (`unique_id`, `ds`, `y`), variables de calendario,
           detección de outliers IQR + Z-score.
        3. **Entrenamiento** (`src/train.py`) — 7 modelos baseline de
           StatsForecast (Naive, HistoricAverage, SeasonalNaive, AutoETS,
           AutoARIMA, AutoTheta, MSTL) evaluados con backtest temporal.
           Trackeo completo en MLflow.
        4. **Inferencia** (`src/predict.py`) — carga el mejor modelo y
           pronostica el horizonte solicitado.
        5. **Servicio** (`api/main.py`) — FastAPI expone `/predict` con
           validación Pydantic y métricas Prometheus.
        6. **Visualización** (esta app) — consume la API o cae a llamada
           local si el servicio no está disponible.

        **KPI objetivo (DIB):** MAPE ≤ 10 %. Baseline actual: ~21 %. La brecha
        se cierra incorporando variables exógenas (festivos Cali, promociones,
        IPC, clima) y mayor granularidad (por categoría / sede).
        """
    )

st.caption(
    "Datos: cadena de supermercados — Cali · 2023 · "
    f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
)
