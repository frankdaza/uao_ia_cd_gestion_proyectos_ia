"""Tests de las transformaciones de src.data."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.data import (
    change_type,
    delete_negative_sales,
    filter_columns,
    impute_nulls_by_month,
)


def test_filter_columns_keeps_only_three(sample_raw_df: pd.DataFrame) -> None:
    extra = sample_raw_df.copy()
    extra["columna_extra"] = "x"
    result = filter_columns(extra)
    assert list(result.columns) == ["fecha", "valor_neto", "valor_costo"]


def test_change_type_converts_fecha_to_datetime(sample_raw_df: pd.DataFrame) -> None:
    df = change_type(sample_raw_df.copy())
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])
    assert df["valor_neto"].dtype == np.float32
    assert df["valor_costo"].dtype == np.float32


def test_delete_negative_sales_drops_negative_and_keeps_positive() -> None:
    df = pd.DataFrame(
        {
            "fecha": pd.date_range("2023-01-01", periods=4, freq="D"),
            "valor_neto": [100.0, -10.0, 50.0, 0.0],
            "valor_costo": [60.0, 5.0, 30.0, 10.0],
        }
    )
    result = delete_negative_sales(df)
    assert (result["valor_neto"] > 0).all()
    assert len(result) == 2


def test_impute_nulls_by_month_fills_with_monthly_mean() -> None:
    df = pd.DataFrame(
        {
            "fecha": pd.to_datetime(
                ["2023-01-01", "2023-01-15", "2023-01-30", "2023-02-01"]
            ),
            "valor_neto": [100.0, np.nan, 300.0, 50.0],
            "valor_costo": [60.0, 80.0, np.nan, 30.0],
        }
    )
    result = impute_nulls_by_month(df.copy())
    assert result["valor_neto"].isna().sum() == 0
    assert result["valor_costo"].isna().sum() == 0
    # Promedio de enero para valor_neto fue (100+300)/2 = 200
    assert result.loc[1, "valor_neto"] == pytest.approx(200.0)
