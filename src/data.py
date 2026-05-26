#Extracción + Transformación de datos

import pandas as pd
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, RAW_DATA_PATH, PROCESSED_DATA_PATH

import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os



def load_raw_data() -> pd.DataFrame:
    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo {RAW_DATA_DIR}. "
            "por favor carga el documento dentro de data/raw/"
        )

    return pd.read_csv(RAW_DATA_PATH)


# funcion para filtrar las comlumnas de interés dejando solo fecha, valor neto y calor costo.
def filter_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[["fecha", "valor_neto", "valor_costo"]]
    return df


# funcion para cambiar el tipo de dato de la columan fecha a datatime
def change_type(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["valor_neto"] = df["valor_neto"].astype(float)
    df["valor_costo"] = df["valor_costo"].astype(float)
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



def preprocess_data() -> pd.DataFrame:
    df = load_raw_data()
    df = filter_columns(df)
    df = impute_nulls_by_month(df)
    df = change_type(df)
    df = delete_negative_sales(df)
    
    print("Dimensiones finales:", df.shape)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    return df



if __name__ == "__main__":
    processed = preprocess_data()
    print(processed.head())
    print(processed.info())