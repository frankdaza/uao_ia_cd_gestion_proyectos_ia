from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MONITORING_DIR = DATA_DIR / "monitoring"

REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_DIR = REPORTS_DIR / "metrics"
MODELS_DIR = ROOT_DIR / "models"

RAW_DATA_PATH = RAW_DATA_DIR / "data_consolidada.csv"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "ventas_procesadas.csv"
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT_NAME = "sales-forecasting"
REGISTERED_MODEL_NAME = "sales-forecaster"

RANDOM_STATE = 42
TEST_SIZE = 0.2