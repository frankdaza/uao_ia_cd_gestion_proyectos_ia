import pandas as pd
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


# Agrega features de calendario: día de semana, mes, día del mes, quincena y fin de semana
def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["dia_semana"] = df["fecha"].dt.dayofweek
    df["mes"] = df["fecha"].dt.month
    df["dia_mes"] = df["fecha"].dt.day
    df["quincena"] = (df["fecha"].dt.day > 15).astype(int) + 1
    df["es_fin_semana"] = (df["dia_semana"] >= 5).astype(int)
    return df


# Agrega ventas de 7, 14 y 30 días atrás para que el modelo aprenda del comportamiento pasado
def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["lag_7"] = df["valor_neto"].shift(7)
    df["lag_14"] = df["valor_neto"].shift(14)
    df["lag_30"] = df["valor_neto"].shift(30)
    return df


# Calcula el promedio móvil de 7 y 30 días para capturar la tendencia reciente
def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rolling_7"] = df["valor_neto"].shift(1).rolling(7).mean()
    df["rolling_30"] = df["valor_neto"].shift(1).rolling(30).mean()
    return df


# Orquesta todo el pipeline de features y guarda el resultado en data/processed/features.csv
def build_features() -> pd.DataFrame:
    df = load_processed_data()
    df = aggregate_daily(df)
    df = add_calendar_features(df)
    df = add_lag_features(df)
    df = add_rolling_features(df)

    df = df.dropna().reset_index(drop=True)

    FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_PATH, index=False)

    print(f"Features guardadas en: {FEATURES_PATH}")
    print(f"Filas: {len(df)} | Columnas: {list(df.columns)}")
    return df


if __name__ == "__main__":
    build_features()
