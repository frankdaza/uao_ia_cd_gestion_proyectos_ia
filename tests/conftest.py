"""Fixtures compartidas entre tests."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def sample_raw_df() -> pd.DataFrame:
    """DataFrame pequeño con la forma del CSV crudo (post-filter_columns)."""
    return pd.DataFrame(
        {
            "fecha": ["20230101", "20230102", "20230103", "20230104", "20230105"],
            "valor_neto": [100.0, 150.0, np.nan, -50.0, 200.0],
            "valor_costo": [60.0, 90.0, 80.0, 30.0, 120.0],
        }
    )


@pytest.fixture
def sample_nixtla_df() -> pd.DataFrame:
    """DataFrame en formato Nixtla con 14 puntos por serie (2 semanas)."""
    dates = pd.date_range("2023-01-01", periods=14, freq="D")
    return pd.concat(
        [
            pd.DataFrame(
                {
                    "unique_id": ["valor_neto"] * 14,
                    "ds": dates,
                    "y": np.arange(100, 114, dtype=float),
                }
            ),
            pd.DataFrame(
                {
                    "unique_id": ["valor_costo"] * 14,
                    "ds": dates,
                    "y": np.arange(50, 64, dtype=float),
                }
            ),
        ],
        ignore_index=True,
    )
