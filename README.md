# Forescast_Project — Sistema inteligente de pronóstico de ventas

Proyecto MLOps de la **Maestría en IA y Ciencia de Datos (UAO)** para una cadena de
supermercados en Cali. Combina ingeniería de datos, modelos de series de tiempo
y prácticas MLOps para producir pronósticos accionables y trazables.

> **Estado:** En desarrollo activo. Pipeline de datos y featuring funcionales;
> modelado, API y despliegue en construcción rumbo al Demo Day del **30 de mayo
> de 2026** y entrega final del **3 de junio de 2026**.

---

## 1. Problema

La cadena planifica compras e inventario con procesos manuales en hojas de
cálculo, reportes fragmentados desde un ERP en transición y decisiones basadas
en intuición. Esto produce:

- **Quiebres frecuentes** en productos de alta rotación.
- **Mermas y vencimientos** en perecederos por sobrestock.
- **Retraso** entre el cierre del día y la información disponible.
- **Falta de trazabilidad** en cómo se toman las decisiones de compra.

Contexto completo del problema: ver [`docs/BMC_Pronostico_Ventas.pdf`](docs/BMC_Pronostico_Ventas.pdf)
(Business Model Canvas) y [`docs/DIB_Pronostico_Ventas.pdf`](docs/DIB_Pronostico_Ventas.pdf)
(Data Innovation Board).

## 2. Solución

Pipeline MLOps end-to-end, simple y demostrable:

1. **Ingesta y limpieza** del histórico de ventas desde CSV consolidado.
2. **Featuring** con formato Nixtla (`unique_id`, `ds`, `y`), agregación diaria,
   variables de calendario y detección de outliers (IQR + Z-score).
3. **Modelado de series de tiempo** con la librería [Nixtla](https://nixtlaverse.nixtla.io)
   (StatsForecast / NeuralForecast) sobre las series `valor_neto` y `valor_costo`.
4. **Tracking de experimentos** con MLflow (parámetros, métricas, artefactos).
5. **Registry** del mejor modelo como `sales-forecaster`.
6. **Servicio de predicción** vía FastAPI con métricas Prometheus.
7. **Interfaz de demo** en Streamlit con histórico vs pronóstico.
8. **Orquestación** vía Docker Compose.

### KPIs objetivo (definidos en el DIB)

| Métrica | Meta |
|---|---|
| MAPE | ≤ 10 % |
| R² | ≥ 0.80 |
| RMSE / MAE | Mejor que baseline ingenuo |
| Tiempo de generación de dato | Reducción significativa vs proceso manual |

## 3. Arquitectura

```
data/raw/data_consolidada.csv
        │
        ▼  src/data.py  (limpieza, tipos, imputación)
data/processed/ventas_procesadas.csv
        │
        ▼  src/featuring.py  (agregación diaria, formato Nixtla, calendario, outliers)
data/processed/{daily_aggregate.csv, nixtla_format.csv, features.csv}
        │
        ▼  src/train.py  (Nixtla + MLflow tracking)
MLflow Tracking Server  ──►  models/sales_forecaster  (+ reports/metrics/)
        │
        ▼  src/register_model.py
MLflow Model Registry  ──►  sales-forecaster (Staging/Production)
        │
        ▼  src/predict.py
        │
        ▼  api/main.py  (FastAPI: /health /predict /model-info /metrics)
        │
        ▼  app/streamlit_app.py  (UI demo: histórico vs pronóstico, KPIs)
        │
        ▼  Prometheus  ──►  Grafana (opcional)
```

## 4. Stack técnico

| Capa | Herramienta |
|---|---|
| Lenguaje | Python 3.12 |
| Gestor de entorno | [uv](https://docs.astral.sh/uv/) |
| Datos / EDA | pandas, numpy, matplotlib, seaborn, plotly |
| Modelado | Nixtla (StatsForecast / NeuralForecast), scikit-learn (baselines) |
| Tracking & Registry | MLflow |
| API | FastAPI + Uvicorn + Pydantic + Prometheus client |
| App de demo | Streamlit |
| Monitoreo | Prometheus (+ Grafana opcional) |
| Orquestación | Docker Compose |
| Tests | pytest |

## 5. Estructura del repositorio

```text
.
├── api/                       Servicio FastAPI
│   └── main.py
├── app/                       App Streamlit
│   └── streamlit_app.py
├── docker/                    Configs de orquestación
│   └── prometheus.yml
├── docs/                      Documentación de negocio
│   ├── BMC_Pronostico_Ventas.pdf
│   └── DIB_Pronostico_Ventas.pdf
├── notebook/                  EDA y experimentación
│   └── EDA.ipynb
├── reports/
│   ├── figures/               Gráficas generadas por featuring.py
│   └── metrics/               Resumen JSON de métricas de entrenamiento
├── src/                       Pipeline core
│   ├── config.py              Rutas y configuración central
│   ├── data.py                Carga + limpieza
│   ├── featuring.py           Feature engineering + outliers
│   ├── train.py               (pendiente) Entrenamiento + MLflow
│   ├── register_model.py      (pendiente) Registro en MLflow
│   └── predict.py             (pendiente) Inferencia
├── tests/                     (pendiente) Pruebas
├── docker-compose.yml         (pendiente)
├── pyproject.toml             Dependencias y metadata
├── uv.lock                    Lock file de uv
└── README.md
```

## 6. Estado de implementación

| Componente | Estado |
|---|---|
| Pipeline de datos (`src/data.py`) | Funcional |
| Feature engineering (`src/featuring.py`) | Funcional (formato Nixtla, calendario, outliers IQR/Z-score) |
| EDA (`notebook/EDA.ipynb`) | Avanzado |
| Entrenamiento (`src/train.py`) | Funcional (7 baselines StatsForecast, backtest, MLflow) |
| MLflow tracking | Funcional (fallback automático a `mlruns/` local si no hay servidor) |
| Registry (`src/register_model.py`) | Funcional (PyFunc wrapper + alias `production`) |
| Inferencia (`src/predict.py`) | Funcional (CLI + librería, JSON / tabla) |
| API FastAPI (`api/main.py`) | Funcional (`/predict`, `/health`, `/model-info`, `/metrics`) |
| App Streamlit (`app/streamlit_app.py`) | Funcional (KPIs, histórico vs pronóstico, fallback local) |
| Prometheus + monitoreo | Funcional (scrape automático de `api:8000/metrics` cada 15 s) |
| Docker Compose | Funcional (MLflow + API + Streamlit + Prometheus con `docker compose up`) |
| Tests | Pendiente |

## 6.1 Resultados del baseline actual

Ejecutando `python -m src.train` sobre el histórico de 2023 (728 obs, 2 series),
con backtest temporal de 3 ventanas y horizonte de 30 días:

| Modelo | MAPE promedio | R² `valor_neto` | R² `valor_costo` |
|---|---:|---:|---:|
| **MSTL([7, 30])** ★ | **20.98 %** | 0.02 | 0.13 |
| AutoARIMA(7) | 21.44 % | 0.16 | 0.24 |
| HistoricAverage | 23.00 % | −0.01 | −0.02 |
| SeasonalNaive(7) | 31.12 % | −0.93 | −0.80 |
| Naive | 40.45 % | −0.76 | −0.92 |
| AutoTheta(7) | 48.40 % | −1.34 | −1.79 |
| AutoETS(7) | 67.71 % | −2.83 | −5.64 |

**Mejor modelo:** MSTL — captura la doble estacionalidad semanal + mensual (calza
con el patrón quincenal del DIB).

**Lectura honesta del resultado:**

- El KPI del DIB es MAPE ≤ 10 %; el mejor baseline está en ~21 %. La brecha es
  esperable sin variables exógenas (clima, promociones, calendario de festivos
  de Cali) y con sólo 1 año de histórico.
- Sólo MSTL y AutoARIMA logran R² positivo. Los demás pierden contra la media.
- AutoETS falla muy mal — probable sensibilidad a outliers en la serie.

**Próximos pasos para cerrar la brecha (en próximos PRs):**

1. Incorporar features exógenas: días festivos Colombia/Cali, calendario de
   quincenas, promociones si están disponibles.
2. Evaluar `AutoCES`, `AutoTBATS` para múltiples estacionalidades.
3. Probar `NHITS` / `NBEATS` (NeuralForecast) si se dispone de más histórico.
4. Trabajar con datos por categoría o sede (granularidad mayor mejora MAPE).

## 7. Requisitos

- **Python 3.12.11** (versión fijada en `.python-version`).
- **uv** instalado ([guía](https://docs.astral.sh/uv/getting-started/installation/)).
- Sistema operativo: Windows o Linux.
- Dataset crudo `data_consolidada.csv` ubicado en `data/raw/` (no incluido en el
  repo por tamaño y confidencialidad).

## 8. Instalación

```bash
# Clonar el repo
git clone https://github.com/jennramos87/Forescast_Project.git
cd Forescast_Project

# Crear entorno e instalar dependencias con uv
uv sync

# Activar entorno (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activar entorno (Linux/Mac)
source .venv/bin/activate
```

## 9. Ejecución local

### 9.1 Pipeline de datos

```bash
# Genera data/processed/ventas_procesadas.csv
python -m src.data
```

### 9.2 Feature engineering

```bash
# Genera daily_aggregate.csv, nixtla_format.csv, features.csv
# y figuras en reports/figures/
python -m src.featuring
```

### 9.3 Entrenamiento

```bash
# (Opcional) Levantar MLflow tracking server en otra terminal
mlflow ui --backend-store-uri ./mlruns --host 127.0.0.1 --port 5000

# Entrenar los 7 baselines, evaluar backtest y guardar el mejor.
# Si MLflow server no responde, hace fallback automático a ./mlruns local.
python -m src.train
```

Genera `models/sales_forecaster.joblib` + `reports/metrics/train_metrics.json`.

### 9.4 Inferencia desde la CLI

```bash
# Pronóstico de 30 días para valor_neto, formato tabla
python -m src.predict --days 30 --series valor_neto

# Pronóstico de 14 días para valor_costo, JSON
python -m src.predict --days 14 --series valor_costo --json
```

### 9.5 Registry MLflow

```bash
# Registra el mejor modelo como sales-forecaster y asigna alias 'production'
python -m src.register_model
```

Verlo en MLflow UI → tab **Models** → `sales-forecaster` → versión con alias `@production`.

### 9.6 API FastAPI

```bash
uvicorn api.main:app --reload --port 8000
```

Endpoints:
- http://127.0.0.1:8000/docs — Swagger UI.
- `GET /health` · `GET /model-info` · `POST /predict` · `GET /metrics`.

### 9.7 Streamlit demo

```bash
streamlit run app/streamlit_app.py
```

Abre en http://localhost:8501. Consume la API si está activa; si no, cae a llamada local — la demo no se rompe.

## 10. Ejecución con Docker

Levanta toda la plataforma con un solo comando:

```bash
docker compose up --build
```

Servicios y puertos:

| Servicio | URL | Descripción |
|---|---|---|
| MLflow | http://localhost:5000 | Tracking server + Model Registry |
| API FastAPI | http://localhost:8000/docs | Swagger UI |
| Streamlit | http://localhost:8501 | App demo |
| Prometheus | http://localhost:9090 | Métricas (job `forescast-api`) |

**Pre-requisitos para que la demo arranque con datos:** correr una vez
localmente `python -m src.data` → `python -m src.featuring` → `python -m src.train`
para generar `data/processed/` y `models/sales_forecaster.joblib`. El compose monta
estas carpetas como volúmenes.

**Detener todo:**

```bash
docker compose down
```

**Variables de entorno usadas dentro del compose** (sobrescriben los defaults de
`src/config.py` y `app/streamlit_app.py`):

- `MLFLOW_TRACKING_URI=http://mlflow:5000`
- `API_URL=http://api:8000` (sólo en Streamlit)

Grafana queda como mejora futura — Prometheus ya expone los datos listos para
conectarlo.

## 11. Datos

- **Granularidad de modelado:** diaria, sobre ventas agregadas a nivel global.
- **Series predichas:** `valor_neto` y `valor_costo`.
- **Histórico requerido:** ~1 año disponible en `data_consolidada.csv`.
- **Formato Nixtla:** `unique_id`, `ds`, `y` para compatibilidad con
  StatsForecast / NeuralForecast.

> El dataset crudo (~5.5 GB) y los procesados quedan fuera del repo
> (`.gitignore`). Compartir vía canal interno del equipo.

## 12. Flujo de trabajo Git

Convención del equipo:

- `main` — sólo recibe releases revisados desde `develop`.
- `develop` — rama integradora del equipo.
- `feature/<nombre>`, `fix/<nombre>`, `chore/<nombre>` — ramas de trabajo.
- **Todos los PRs van contra `develop`**, nunca contra `main` directamente.

```bash
# Flujo típico
git checkout develop && git pull
git checkout -b feature/<algo>
# ...trabajo, commits...
git push -u origin feature/<algo>
# Abrir PR en GitHub con base = develop
```

## 13. Equipo

- **Frank Edward Daza Gonzalez** — scaffolding inicial, dependencias.
- **Jenn Ramos** ([@jennramos87](https://github.com/jennramos87)) — datos, EDA, featuring, outliers.
- **Yancarlos Cuarán** — EDA, integración del equipo.
- **Juan M. Velásquez T.** — diseño del problema (BMC / DIB), arquitectura MLOps.

Maestría en Inteligencia Artificial y Ciencia de Datos · **Universidad Autónoma
de Occidente (UAO)** · Cali, Colombia.

## 14. Demo Day — guion (10 minutos)

| Tiempo | Bloque | Contenido |
|---|---|---|
| 0:00 – 1:30 | **Problema** | Procesos manuales, quiebres, mermas, falta de trazabilidad. |
| 1:30 – 3:00 | **Solución** | Pipeline MLOps con Nixtla + MLflow + FastAPI + Streamlit. |
| 3:00 – 8:30 | **Demo** | `python -m src.data` → `src.featuring` → `src.train` → MLflow UI → FastAPI `/docs` → Streamlit. |
| 8:30 – 10:00 | **Cierre** | KPIs alcanzados, valor de negocio, próximos pasos. |

## 15. Limitaciones conocidas

- Sólo se modelan series agregadas (`valor_neto`, `valor_costo`); el BMC plantea
  granularidad SKU-tienda-día, fuera del alcance del Demo Day.
- No se incluyen variables exógenas (clima, promociones, IPC) en esta versión.
- Histórico limitado a ~1 año.
- Monitoreo con Grafana queda como mejora si el tiempo no alcanza.

## 16. Próximos pasos

1. Cerrar `src/train.py` con Nixtla + MLflow tracking.
2. `src/predict.py` con `predict_next_days()`.
3. FastAPI `/predict` con Pydantic + Prometheus.
4. Streamlit con visualización histórico vs pronóstico.
5. `docker-compose.yml` levantando todos los servicios.
6. Tests mínimos (`test_data.py`, `test_predict.py`, `test_api.py`).
7. Extender a granularidad por categoría o sede.
8. Incorporar variables exógenas (calendario de festivos de Cali, IPC, clima).
9. Validación temporal (walk-forward) y monitoreo de drift.
