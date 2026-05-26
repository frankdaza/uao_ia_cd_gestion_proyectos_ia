import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.config import PROCESSED_DATA_PATH, PROCESSED_DATA_DIR


FEATURES_PATH = PROCESSED_DATA_DIR / "features.csv"


# Lee el CSV procesado por data.py y lo retorna como DataFrame
def load_processed_data() -> pd.DataFrame:
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró {PROCESSED_DATA_PATH}. "
            "Ejecuta primero python -m src.data"
        )
    df = pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["fecha"])
    return df


# Agrupa las transacciones por día sumando valor_neto y valor_costo → 365 filas
def aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:
    df = df.groupby("fecha", as_index=False).agg(
        valor_neto=("valor_neto", "sum"),
        valor_costo=("valor_costo", "sum"),
    )
    df = df.sort_values("fecha").reset_index(drop=True)
    return df


def to_nixtla_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el DataFrame al formato requerido por Nixtla (StatsForecast/NeuralForecast).
    Crea un formato largo donde 'valor_neto' y 'valor_costo' son series individuales
    identificadas por 'unique_id', con la fecha en 'ds' y los valores en 'y'.
    """
    df_neto = df[["fecha", "valor_neto"]].rename(columns={"fecha": "ds", "valor_neto": "y"})
    df_neto["unique_id"] = "valor_neto"
    
    df_costo = df[["fecha", "valor_costo"]].rename(columns={"fecha": "ds", "valor_costo": "y"})
    df_costo["unique_id"] = "valor_costo"
    
    nixtla_df = pd.concat([df_neto, df_costo], ignore_index=True)
    return nixtla_df[["unique_id", "ds", "y"]]



# Agrega features de calendario: día de semana, mes, día del mes, quincena y fin de semana
def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Usamos la columna "ds" en lugar de "fecha" ya que ahora el df está en formato Nixtla
    df["ds"] = pd.to_datetime(df["ds"])
    df["dia_semana"] = df["ds"].dt.dayofweek
    df["mes"] = df["ds"].dt.month
    df["dia_mes"] = df["ds"].dt.day
    df["quincena"] = (df["ds"].dt.day > 15).astype(int) + 1
    df["es_fin_semana"] = (df["dia_semana"] >= 5).astype(int)
    return df


# graficar series de valor_neto y valor_costo

def plot_series(df: pd.DataFrame):
    fig = go.Figure()
    
    for uid in df["unique_id"].unique():
        sub_df = df[df["unique_id"] == uid]
        fig.add_trace(go.Scatter(
            x=sub_df["ds"],
            y=sub_df["y"],
            mode='lines+markers',
            name=uid,
            marker=dict(size=3)
        ))
        
    fig.update_layout(
        title='Ventas y Costos Diarios',
        xaxis_title='Fecha',
        yaxis_title='Valor',
        height=380,
        template='plotly_white'
    )
    fig.show()



# Agrega ventas de 7, 14 y 30 días atrás agrupando por serie (unique_id) para evitar mezcla de datos
# def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     df["lag_7"] = df.groupby("unique_id")["y"].shift(7)
#     df["lag_14"] = df.groupby("unique_id")["y"].shift(14)
#     df["lag_30"] = df.groupby("unique_id")["y"].shift(30)
#     return df


# # Calcula el promedio móvil de 7 y 30 días agrupando por serie (unique_id) para evitar mezcla de datos
# def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     df["rolling_7"] = df.groupby("unique_id")["y"].transform(lambda x: x.shift(1).rolling(7).mean())
#     df["rolling_30"] = df.groupby("unique_id")["y"].transform(lambda x: x.shift(1).rolling(30).mean())
#     return df


# Orquesta todo el pipeline de features y guarda el resultado en data/processed/features.csv
def build_features() -> pd.DataFrame:
    df = load_processed_data()
    df_day = aggregate_daily(df)
    df_nixtla = to_nixtla_format(df_day)
    plot_series(df_nixtla)
    df_calendar = add_calendar_features(df_nixtla)


    FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_PATH, index=False)

    print(f"Features guardadas en: {FEATURES_PATH}")
    print(f"Filas: {len(df)} | Columnas: {list(df.columns)}")
    return df


if __name__ == "__main__":
    build_features()
