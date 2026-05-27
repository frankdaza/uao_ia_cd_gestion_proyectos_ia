# Guion Demo Day — Forescast_Project

**Fecha:** 30 de mayo de 2026 · **Duración:** 10 min · **Equipo:** UAO Maestría en IA y Ciencia de Datos.

> Este guion está pensado para ser leído tal cual durante el pitch. Cada bloque
> tiene **qué decir**, **qué mostrar** y **comandos exactos**. Si algo falla en
> vivo, ver §**Plan B** al final.

---

## Pre-flight (10 min antes del pitch)

Tener listo, **en este orden**:

```powershell
# 1. Carpeta del proyecto y entorno activo
cd "C:\Users\PROYECTOS\Desktop\MAESTRIA EN IA Y CD\DEMODAY_GESTIO_PY_IA"
.\.venv\Scripts\Activate.ps1

# 2. Sincronizar develop
git checkout develop
git pull

# 3. Verificar que existe el modelo entrenado (debe pesar ~230 KB)
dir models\sales_forecaster.joblib
```

**Tres PowerShell abiertas y listas, una por servicio:**

```powershell
# Terminal A — MLflow
mlflow ui --backend-store-uri ./mlruns --host 127.0.0.1 --port 5000

# Terminal B — API
uvicorn api.main:app --port 8000

# Terminal C — Streamlit
streamlit run app/streamlit_app.py
```

**Browser con cuatro pestañas pre-abiertas:**

1. GitHub: https://github.com/jennramos87/Forescast_Project
2. MLflow: http://127.0.0.1:5000
3. API Swagger: http://127.0.0.1:8000/docs
4. Streamlit: http://localhost:8501

---

## 0:00 – 1:30 · Problema (90 s)

**Qué decir:**

> "Trabajamos con una cadena de supermercados en Cali. Hoy planifican compras
> con hojas de cálculo, reportes manuales y decisiones por intuición. Eso
> genera tres dolores: quiebres en productos de alta rotación, mermas en
> perecederos por sobrestock, y retrasos entre el cierre del día y la
> información disponible. No hay trazabilidad de cómo se toman las decisiones."

**Qué mostrar:** `docs/BMC_Pronostico_Ventas.pdf` y `docs/DIB_Pronostico_Ventas.pdf`
abiertos a tamaño visible — un pantallazo rápido a cada uno.

**Cierre del bloque:** "Nuestro objetivo: convertir esto en un pipeline MLOps
demostrable que reduzca trabajo manual y dé trazabilidad."

---

## 1:30 – 3:00 · Solución (90 s)

**Qué decir:**

> "Construimos un pipeline end-to-end con Python, MLflow, FastAPI, Streamlit,
> Prometheus y Docker. Seis pasos: ingesta y limpieza, feature engineering en
> formato Nixtla, entrenamiento de siete modelos baseline con StatsForecast,
> tracking en MLflow, servicio FastAPI con métricas Prometheus y app Streamlit
> para consumirlo."

**Qué mostrar:** README.md §3 (diagrama de arquitectura) en GitHub.

**Frase clave:** "Todo corre con un comando: `docker compose up`."

---

## 3:00 – 8:30 · Demo (5:30 min)

### 3:00 – 3:30 · Estructura del repo

**Qué mostrar:** GitHub README §5 (estructura) y §6 (estado de implementación).

**Qué decir:**

> "El repo está separado por capas: src/ tiene el pipeline, api/ el servicio,
> app/ la UI, docker/ la orquestación, docs/ la documentación de negocio.
> Todos los componentes están funcionales menos los tests automatizados, que
> es nuestro próximo paso."

### 3:30 – 4:15 · Ingesta y feature engineering

**Comando (Terminal A):**

```powershell
python -m src.featuring
```

**Qué decir mientras corre:**

> "El CSV crudo pesa 17 GB. `src/data.py` lee en chunks de 2 millones de filas,
> agrega por día sobre la marcha, y el pico de RAM se queda en 50 MB — corre
> cómodo en cualquier laptop. Después `src/featuring.py` convierte al formato
> Nixtla `unique_id, ds, y`, agrega variables de calendario y detecta
> outliers con IQR y Z-score."

**Qué mostrar al terminar:** `reports/figures/series_tiempo.png` y
`reports/figures/outliers_iqr_valor_neto.png`.

### 4:15 – 5:30 · Entrenamiento y MLflow

**No correr `python -m src.train` en vivo** — tarda varios minutos. Mostrar
los resultados ya entrenados:

**Qué mostrar:**

1. MLflow UI (http://127.0.0.1:5000) → **Experiments** → `sales-forecasting`
   → ver los 7 runs con sus métricas.
2. Tab **Models** → `sales-forecaster` versión con alias `@production`.
3. Tab **Traces** → la cascada `train_pipeline → load_nixtla_data → evaluate_with_cv → compute_metrics × 14`.

**Qué decir:**

> "Comparamos siete modelos: Naive, HistoricAverage, SeasonalNaive, AutoETS,
> AutoARIMA, AutoTheta y MSTL. Validamos con backtest temporal de 3 ventanas,
> no con split aleatorio porque son series de tiempo. MLflow trackea
> parámetros, métricas y el modelo serializado. El ganador fue **AutoARIMA
> con MAPE 20.96 %**. Está registrado en el Registry con alias `production`
> — un cambio de modelo es un solo click."

**Si te preguntan por el MAPE de 21% vs el KPI del DIB de 10%:**

> "Es un baseline honesto sin variables exógenas. Para cerrar la brecha:
> festivos de Cali, promociones, IPC, clima, y trabajar por categoría o sede
> en lugar de a nivel agregado. Está documentado como próximos pasos en el
> README §6.1."

### 5:30 – 6:30 · API FastAPI

**Qué mostrar:** http://127.0.0.1:8000/docs (Swagger).

**Qué decir:**

> "La API expone cuatro endpoints: health, model-info, predict y metrics.
> Validación con Pydantic, errores tipados con HTTPException, métricas
> Prometheus de cantidad de predicciones, latencia y errores."

**Demo en vivo:** desde Swagger, hacer **POST /predict** con:

```json
{"days": 30, "series": "valor_neto"}
```

Mostrar el response (30 puntos, total, promedio, modelo usado: AutoARIMA).

### 6:30 – 7:30 · Streamlit

**Qué mostrar:** http://localhost:8501.

**Qué hacer:**

1. Seleccionar serie "Ventas (valor neto)" en la sidebar.
2. Slider a 30 días.
3. Click **Generar pronóstico**.

**Qué decir:**

> "Esta app de Streamlit consume la API. Si el servicio está activo, la fuente
> es 'API'; si la API se cae, automáticamente cae a llamada local — la demo
> no se rompe en vivo. Mostramos KPIs: total esperado, promedio diario, día
> pico, y gráfico de histórico vs pronóstico. Para un planificador de
> compras esto reemplaza las hojas de cálculo manuales."

### 7:30 – 8:30 · Monitoreo y Docker

**Qué mostrar (rápido):**

1. http://127.0.0.1:8000/metrics — métricas Prometheus en raw.
2. (Opcional, si está corriendo) http://localhost:9090 — Prometheus UI.

**Qué decir:**

> "Cada pronóstico incrementa contadores Prometheus. Esto es la base del
> monitoreo en producción: latencia, errores y throughput. Y todo el stack
> se levanta con `docker compose up` — un comando, cuatro servicios."

---

## 8:30 – 10:00 · Cierre (90 s)

**Qué decir:**

> "Logramos un ciclo MLOps completo y reproducible: datos crudos a 17 GB
> procesados eficientemente, siete modelos comparados con trazabilidad, modelo
> registrado y servido por API, app demo, métricas para monitoreo y
> orquestación Docker.
>
> Para negocio, esto representa: pronósticos consistentes en lugar de
> intuición, trazabilidad completa de qué modelo decidió qué, una API que
> el ERP puede consumir, y una UI para el equipo de planeación.
>
> Próximos pasos: tests automatizados, variables exógenas para bajar el MAPE
> al 10 % objetivo, granularidad por categoría/sede, y despliegue cloud con
> monitoreo de drift y retraining automático.
>
> Gracias."

---

## Plan B — qué hacer si algo falla en vivo

| Falla | Acción inmediata |
|---|---|
| MLflow UI no carga | Mostrar capturas en `docs/screenshots/mlflow_*.png` (TODO si hay tiempo). Continuar con narrativa. |
| API tarda en responder en `/predict` | Decir "está corriendo el primer warm-up" — esperar 5 s. Si no responde en 10 s, mostrar Streamlit y dejar que el fallback local cubra. |
| Streamlit muestra "fuente: local" | **No es un bug, es la feature.** Decir: "Acá se ve el fallback que mencioné — la API se cayó y la app sigue funcionando." |
| `mlflow ui` no levanta | Usar tracking local: la app sigue funcionando, sólo no se muestran las traces. Mostrar `reports/metrics/train_metrics.json` en su lugar. |
| Docker se cuelga | No usar Docker en vivo. Tenerlo pre-levantado o saltar al modo local. |
| Quiebra de internet | El pitch es 100 % local. No se necesita red. |

---

## Atajos de teclado útiles durante el pitch

- `Alt + Tab` entre PowerShell terminals.
- `Ctrl + Tab` entre pestañas del navegador.
- `Ctrl + L` o `clear` para limpiar la terminal antes de un comando importante.

---

## Métricas que te van a preguntar

| Pregunta | Respuesta |
|---|---|
| ¿Cuántos modelos compararon? | 7 baselines (Naive, HistoricAverage, SeasonalNaive, AutoETS, AutoARIMA, AutoTheta, MSTL). |
| ¿Mejor modelo? | AutoARIMA, MAPE 20.96 %. |
| ¿KPI del DIB? | MAPE ≤ 10 %. Brecha cierra con exógenas. |
| ¿Tamaño del dataset? | ~17 GB crudo, agregado a 365 filas diarias en `data/processed/`. |
| ¿Cuánto RAM consume? | ~50 MB pico gracias a chunked read + float32. |
| ¿Cómo decidieron el modelo? | Backtest temporal (3 ventanas, h=30) con MAPE promedio entre las 2 series. |
| ¿Cómo lo despliegan? | Docker Compose con 4 servicios: MLflow, FastAPI, Streamlit, Prometheus. |
| ¿Cómo lo monitorean? | Prometheus scrape de `/metrics` cada 15 s. Grafana es paso siguiente. |
| ¿Pueden cambiar de modelo sin redeploy? | Sí — promover otra versión al alias `@production` en MLflow Registry. |

---

## Repartición del equipo (sugerencia)

- **Frank Daza** — abre el pitch (problema y solución).
- **Jenn Ramos** — demo de datos, featuring, MLflow.
- **Yancarlos Cuarán** — demo de API y Streamlit.
- **Juan Velásquez** — cierre, valor de negocio y próximos pasos.

Ajustable según preferencia del equipo.
