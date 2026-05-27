#Extracción + Transformación de datos

import pandas as pd
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, RAW_DATA_PATH, PROCESSED_DATA_PATH



def load_raw_data() -> pd.DataFrame:
    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo {RAW_DATA_DIR}. "
            "por favor carga el documento dentro de data/raw/"
        )

    # Cargar sólo las 3 columnas que se usan, con dtypes compactos.
    # Reduce drásticamente la memoria para datasets grandes (decenas de GB).
    return pd.read_csv(
        RAW_DATA_PATH,
        usecols=["fecha", "valor_neto", "valor_costo"],
        dtype={"fecha": "string", "valor_neto": "float32", "valor_costo": "float32"},
    )


# funcion para filtrar las comlumnas de interés dejando solo fecha, valor neto y calor costo.
def filter_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[["fecha", "valor_neto", "valor_costo"]]
    return df


# funcion para cambiar el tipo de dato de la columan fecha a datatime
def change_type(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y%m%d")
    df["valor_neto"] = df["valor_neto"].astype("float32")
    df["valor_costo"] = df["valor_costo"].astype("float32")
    return df


# funcion para eliminar filas con valores de ventas menores a 0
def delete_negative_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[df["valor_neto"] > 0]
    return df


# función que cuenta los valores nulos por columna, 
# imputa por el promedio del mes y 
# luego imprime el total de nullos imputados por columna

def impute_nulls_by_month(df: pd.DataFrame, date_column: str = "fecha") -> pd.DataFrame:
    df = df.copy()
    
    # 1. Contar valores nulos antes de la imputación
    nulls_before = df.isnull().sum()
     
    # Asegurar que la columna de fecha esté en formato datetime para agrupar
    df[date_column] = pd.to_datetime(df[date_column])
    df['year_month'] = df[date_column].dt.to_period('M')
    
    # 2. Imputar columnas numéricas por el promedio del mes
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    for col in numeric_cols:
        if nulls_before[col] > 0:
            # Promedio del mes para cada registro
            monthly_mean = df.groupby('year_month')[col].transform('mean')
            df[col] = df[col].fillna(monthly_mean)

                
    # Eliminar columna auxiliar de año-mes
    df = df.drop(columns=['year_month'])
    
    # 3. Contar nulos después y calcular el total de imputados
    nulls_after = df.isnull().sum()
    imputed_counts = nulls_before - nulls_after
    
    print("Resumen de imputación de valores nulos:")
    for col, count in imputed_counts.items():
        if nulls_before[col] > 0:
            print(f"- {col}: {count} nulos imputados (Quedan: {nulls_after[col]} nulos)")
            
    return df



def preprocess_data(chunk_size: int = 2_000_000) -> pd.DataFrame:
    """Procesa el CSV crudo por chunks y guarda ventas agregadas por día.

    El dataset crudo puede pesar decenas de GB. Cargarlo entero a memoria
    revienta la RAM. En lugar de eso:

      1. Se lee en chunks de `chunk_size` filas (~24 MB cada uno con 3 cols
         float32 + string).
      2. En cada chunk: parsear fecha, descartar inválidas, filtrar
         valor_neto > 0, agregar por día.
      3. Concatenar y re-agregar todos los chunks (resultado: 1 fila por día).
      4. Imputar nulos por mes en el resultado agregado (rápido y barato).

    Output: `ventas_procesadas.csv` con columnas `fecha`, `valor_neto`,
    `valor_costo` ya agregadas a nivel diario. featuring.py vuelve a
    aplicar `aggregate_daily` sobre esto, que es idempotente sobre datos
    ya agregados.

    Pico de RAM esperado: ~50 MB independientemente del tamaño del CSV.
    """
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró {RAW_DATA_PATH}. "
            "Coloca el dataset en data/raw/data_consolidada.csv."
        )

    print(f"Procesando {RAW_DATA_PATH.name} en chunks de {chunk_size:,} filas...")

    reader = pd.read_csv(
        RAW_DATA_PATH,
        usecols=["fecha", "valor_neto", "valor_costo"],
        dtype={"fecha": "string", "valor_neto": "float32", "valor_costo": "float32"},
        chunksize=chunk_size,
    )

    daily_chunks: list[pd.DataFrame] = []
    total_rows = 0
    total_kept = 0

    for i, chunk in enumerate(reader, start=1):
        original_size = len(chunk)
        chunk["fecha"] = pd.to_datetime(chunk["fecha"], format="%Y%m%d", errors="coerce")
        chunk = chunk.dropna(subset=["fecha"])
        chunk = chunk[chunk["valor_neto"] > 0]

        agg = chunk.groupby("fecha", as_index=False).agg(
            valor_neto=("valor_neto", "sum"),
            valor_costo=("valor_costo", "sum"),
        )
        daily_chunks.append(agg)
        total_rows += original_size
        total_kept += len(chunk)
        print(f"  Chunk {i}: {original_size:>10,} filas → {len(chunk):>10,} válidas "
              f"({agg['fecha'].nunique()} días distintos)")
        del chunk, agg

    print(f"\nTotal procesado: {total_rows:,} filas | mantenidas: {total_kept:,} "
          f"({100 * total_kept / max(total_rows, 1):.1f} %)")

    combined = pd.concat(daily_chunks, ignore_index=True)
    daily = (
        combined.groupby("fecha", as_index=False)
        .agg(valor_neto=("valor_neto", "sum"), valor_costo=("valor_costo", "sum"))
        .sort_values("fecha")
        .reset_index(drop=True)
    )

    daily = impute_nulls_by_month(daily)

    print(f"\nDimensiones finales (agregado diario): {daily.shape}")
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    daily.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Guardado en: {PROCESSED_DATA_PATH}")
    return daily



if __name__ == "__main__":
    processed = preprocess_data()
    print(processed.head())
    print(processed.info())