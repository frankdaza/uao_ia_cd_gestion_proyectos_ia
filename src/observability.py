"""Inicialización centralizada de MLflow tracing.

Importar este módulo en cualquier script o servicio que use
`@mlflow.trace` garantiza que el tracking URI y el experimento estén
configurados antes de que se ejecute cualquier traza.

Uso típico:

    import mlflow
    from src import observability  # noqa: F401  side-effect: init tracing

    @mlflow.trace
    def mi_funcion(x):
        ...

Si el servidor remoto no responde, hace fallback silencioso a
`file:./mlruns` para que la traza igual se persista localmente y la
demo no se rompa.
"""

from __future__ import annotations

import mlflow

from src.config import EXPERIMENT_NAME, MLFLOW_TRACKING_URI

_INITIALIZED = False


def init_tracing(experiment: str = EXPERIMENT_NAME) -> str:
    """Configura el tracking URI y el experimento activo. Idempotente."""
    global _INITIALIZED
    if _INITIALIZED:
        return mlflow.get_tracking_uri()

    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(experiment)
        active_uri = MLFLOW_TRACKING_URI
    except Exception as exc:
        print(f"[observability] No se pudo conectar a {MLFLOW_TRACKING_URI}: {exc}")
        print("[observability] Fallback a tracking local en ./mlruns")
        mlflow.set_tracking_uri("file:./mlruns")
        mlflow.set_experiment(experiment)
        active_uri = "file:./mlruns"

    _INITIALIZED = True
    return active_uri


# Side-effect al importar: dejar MLflow listo para tracing.
init_tracing()
