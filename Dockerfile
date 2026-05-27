# syntax=docker/dockerfile:1.7

# ---------- Etapa 1: construir el entorno con uv ----------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

WORKDIR /app

# Copiar manifiestos primero para aprovechar cache de Docker
COPY pyproject.toml uv.lock .python-version ./

# Crear venv aislado del proyecto y resolver dependencias
RUN uv sync --frozen --no-install-project

# Copiar el código y volver a sincronizar (instala el paquete del proyecto)
COPY src ./src
COPY api ./api
COPY app ./app
RUN uv sync --frozen


# ---------- Etapa 2: runtime mínimo ----------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

WORKDIR /app

# Copiar el venv y el código desde el builder
COPY --from=builder /app /app

# Crear directorios escribibles para artefactos de runtime
RUN mkdir -p /app/models /app/mlruns /app/reports/metrics /app/data/processed

EXPOSE 8000 8501 5000

# Comando por defecto — sobreescrito por docker-compose para cada servicio
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
