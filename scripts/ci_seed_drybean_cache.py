#!/usr/bin/env python3
"""Genera un Parquet mínimo en ``data/raw/drybean.parquet`` para CI sin red.

``notebooks/01_laboratorio_drybean.ipynb`` usa ``fetch_drybean(cache_dir=...)``.
Si ese archivo ya existe, no se llama a ``ucimlrepo.fetch_ucirepo``. En GitHub
Actions se invoca este script antes de ``nbconvert --execute`` para evitar
dependencia de la red y del UCI.

Las columnas coinciden con el contrato de tests en ``tests/test_data_loading.py``.
Se generan varias filas por clase para que ``train_test_split(..., stratify=y)``
del notebook sea válido.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

_FEATURE_COLS = [
    "Area",
    "Perimeter",
    "MajorAxisLength",
    "MinorAxisLength",
    "AspectRatio",
    "Eccentricity",
    "ConvexArea",
    "EquivDiameter",
    "Extent",
    "Solidity",
    "Roundness",
    "Compactness",
    "ShapeFactor1",
    "ShapeFactor2",
    "ShapeFactor3",
    "ShapeFactor4",
]

_CLASSES = ["SEKER", "BARBUNYA", "BOMBAY", "CALI", "HOROZ", "SIRA", "DERMASON"]

# Varias muestras por clase para estratificación 80/20 estable en el notebook.
_FILAS_POR_CLASE = 12


def main() -> None:
    rng = np.random.default_rng(42)
    filas: list[dict[str, float | str]] = []
    for clase in _CLASSES:
        for _ in range(_FILAS_POR_CLASE):
            fila = {}
            for c in _FEATURE_COLS:
                hi = 50000.0 if c in ("Area", "ConvexArea") else 1.0
                fila[c] = float(rng.uniform(0.1, hi))
            fila["Class"] = clase
            # BOMBAY suele ser morfológicamente distinta: un poco más de área.
            if clase == "BOMBAY":
                fila["Area"] = float(rng.uniform(35000.0, 55000.0))
            filas.append(fila)

    df = pd.DataFrame(filas)
    destino = Path("data/raw/drybean.parquet")
    destino.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(destino, index=False)
    print(f"Escrito {destino} ({len(df)} filas, {len(df.columns)} columnas).")


if __name__ == "__main__":
    main()
