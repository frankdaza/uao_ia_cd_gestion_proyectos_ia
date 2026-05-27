import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import stats
from src.config import PROCESSED_DATA_PATH, PROCESSED_DATA_DIR, DF_DAY_PATH, DF_NIXTLA_PATH, FEATURES_PATH


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
def plot_series(df: pd.DataFrame) -> go.Figure:
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
    return fig


# ── Outliers Método 1: IQR (Rango Intercuartílico) ────────────────────────────────
def detect_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detecta outliers en la columna 'y' del DataFrame usando el método IQR.
    """
    Q1, Q3 = df.y.quantile(0.25), df.y.quantile(0.75)
    IQR    = Q3 - Q1
    limite_inf_iqr = Q1 - 1.5 * IQR
    limite_sup_iqr = Q3 + 1.5 * IQR
    outliers_iqr = df[(df.y < limite_inf_iqr) | (df.y > limite_sup_iqr)]

    print("IQR — Detección de Outliers")
    print(f"  Q1={Q1:.0f}  Q3={Q3:.0f}  IQR={IQR:.0f}")
    print(f"  Límite inferior: {limite_inf_iqr:.0f}")
    print(f"  Límite superior: {limite_sup_iqr:.0f}")
    print(f"  Outliers detectados: {len(outliers_iqr)}")
    print(outliers_iqr[['ds','y']])
    return outliers_iqr


# ── Método 2: Z-score ─────────────────────────────────────────────────────
def detect_outliers_zscore(df: pd.DataFrame, num_desvest: int = 3) -> pd.DataFrame:
    """
    Detecta outliers en la columna 'y' del DataFrame usando el método Z-score.
    """
    z_scores = np.abs(stats.zscore(df.y))
    outliers_z = df[z_scores > num_desvest]

    # Calculate Z-score limits
    mean_y = df.y.mean()
    std_y = df.y.std()
    limite_inf_z = mean_y - num_desvest * std_y
    limite_sup_z = mean_y + num_desvest * std_y

    print(f"\nZ-score (|z| > {num_desvest}) — Outliers detectados: {len(outliers_z)}")
    if len(outliers_z): 
        print(outliers_z[['ds','y']])
    return outliers_z



# ── Visualización comparativa ─────────────────────────────────────────────
def plot_outliers_comparativa(df: pd.DataFrame, outliers_iqr: pd.DataFrame, outliers_z: pd.DataFrame, num_desvest: int = 3) -> tuple[go.Figure, go.Figure]:
    """
    Genera y muestra gráficos comparativos para la detección de outliers (IQR y Z-score).
    
    :return: Tupla (fig_iqr, fig_z) con los objetos de figura de Plotly.
    """
    # Metodo IQR
    Q1, Q3 = df.y.quantile(0.25), df.y.quantile(0.75)
    IQR    = Q3 - Q1
    limite_inf_iqr = Q1 - 1.5 * IQR
    limite_sup_iqr = Q3 + 1.5 * IQR

    fig_iqr = go.Figure()
    fig_iqr.add_trace(go.Scatter(x=df.ds, y=df.y, mode='lines',
                              name='Serie', line=dict(color='#2196F3', width=1.5)))
    fig_iqr.add_hline(y=limite_sup_iqr, line_dash='dash', line_color='orange',
                  annotation_text='Límite IQR superior')
    fig_iqr.add_hline(y=limite_inf_iqr, line_dash='dash', line_color='orange',
                  annotation_text='Límite IQR inferior')
    if len(outliers_iqr):
        fig_iqr.add_trace(go.Scatter(x=outliers_iqr.ds, y=outliers_iqr.y,
                                  mode='markers', name='Outlier (IQR)',
                                  marker=dict(color='red', size=10, symbol='circle-open', line_width=2)))
    fig_iqr.update_layout(title='Detección de Outliers — Método IQR',
                      height=380, template='plotly_white',
                      xaxis_title='Fecha', yaxis_title='Ventas')
    fig_iqr.show()

    # Metodo Z-score
    mean_y = df.y.mean()
    std_y = df.y.std()
    limite_inf_z = mean_y - num_desvest * std_y
    limite_sup_z = mean_y + num_desvest * std_y

    fig_z = go.Figure()
    fig_z.add_trace(go.Scatter(x=df.ds, y=df.y, mode='lines',
                              name='Serie', line=dict(color='#2196F3', width=1.5)))
    fig_z.add_hline(y=limite_sup_z, line_dash='dash', line_color='orange',
                  annotation_text='Límite Z-score superior')
    fig_z.add_hline(y=limite_inf_z, line_dash='dash', line_color='orange',
                  annotation_text='Límite Z-score inferior')
    if len(outliers_z):
        fig_z.add_trace(go.Scatter(x=outliers_z.ds, y=outliers_z.y,
                                  mode='markers', name='Outlier Z-score',
                                  marker=dict(color='red', size=10, symbol='circle-open', line_width=2)))
    fig_z.update_layout(title='Detección de Outliers — Método Z-Score',
                      height=380, template='plotly_white',
                      xaxis_title='Fecha', yaxis_title='Ventas')
    fig_z.show()
    
    return fig_iqr, fig_z



def save_image(fig: go.Figure, nombre_archivo: str, ruta_guardado: str, 
                width: int = 1200, height: int = 600, scale: int = 2):
    """
    Guarda la figura de Plotly como imagen con resolución mejorada para evitar borrosidad.
    Crea la ruta especificada si esta no existe.
    
    :param fig: Figura de Plotly a guardar.
    :param nombre_archivo: Nombre del archivo con su extensión (ej. 'grafico.png').
    :param ruta_guardado: Directorio donde se guardará la imagen.
    :param width: Ancho de la imagen en píxeles.
    :param height: Alto de la imagen en píxeles.
    :param scale: Multiplicador de escala (resolución/DPI). Por ejemplo, 2 duplica la resolución.
    """
    # 1. Crear directorios si no existen
    directorio = Path(ruta_guardado)
    directorio.mkdir(parents=True, exist_ok=True)
    
    ruta_completa = directorio / nombre_archivo
    
    # 2. Guardar la figura de Plotly con resolución configurada
    fig.write_image(str(ruta_completa), width=width, height=height, scale=scale)
    print(f"Imagen guardada correctamente en: {ruta_completa} (Resolución: {width*scale}x{height*scale} px)")


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
    fig = plot_series(df_nixtla)
    save_image(fig, "series_tiempo.png", "reports/figures")
    
    # Outliers por serie
    for serie, group in df_nixtla.groupby('unique_id'): 
        print(f"\n{'='*15} Serie: {serie} {'='*15}")
        outliers_iqr = detect_outliers_iqr(group)
        outliers_z = detect_outliers_zscore(group)

        # Generar visualización comparativa para cada serie
        fig_iqr, fig_z = plot_outliers_comparativa(group, outliers_iqr, outliers_z)
        
        # Guardar figuras
        save_image(fig_iqr, f"outliers_iqr_{serie}.png", "reports/figures")
        save_image(fig_z, f"outliers_zscore_{serie}.png", "reports/figures")

    # datos con informacion de calendario
    df_calendar = add_calendar_features(df_nixtla)


    # Guardar datos diarios, en formato nixtla, calendarizados
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        
    df_day.to_csv(DF_DAY_PATH, index=False)
    print(f"Daily aggregate guardado en: {DF_DAY_PATH}")
    
    df_nixtla.to_csv(DF_NIXTLA_PATH, index=False)
    print(f"Nixtla format guardado en: {DF_NIXTLA_PATH}")
    
    df_calendar.to_csv(FEATURES_PATH, index=False)
    print(f"Features (calendar) guardadas en: {FEATURES_PATH}")
    
    print(f"Filas df_day: {len(df_day)} | Filas df_nixtla: {len(df_nixtla)} | Filas df_calendar: {len(df_calendar)}")
    return df_calendar


if __name__ == "__main__":
    build_features()
