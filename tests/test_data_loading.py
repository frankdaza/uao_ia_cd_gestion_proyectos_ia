"""Pruebas unitarias para src.data_loading.

Se usa monkeypatch sobre ``ucimlrepo.fetch_ucirepo`` para evitar
dependencia de red en CI y ejecución local.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from src.data_loading import fetch_drybean, load_drybean

# ---------------------------------------------------------------------------
# Datos de prueba (stub)
# ---------------------------------------------------------------------------

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


def _build_stub_dataset() -> SimpleNamespace:
    """Construye un objeto stub que imita la respuesta de ``fetch_ucirepo``."""
    n = 21  # 3 muestras por clase
    features = pd.DataFrame(
        {col: range(n) for col in _FEATURE_COLS},
        dtype=float,
    )
    targets = pd.DataFrame({"Class": (_CLASSES * 3)[:n]})
    data = SimpleNamespace(features=features, targets=targets)
    return SimpleNamespace(data=data)


# ---------------------------------------------------------------------------
# Tests de fetch_drybean
# ---------------------------------------------------------------------------


class TestFetchDrybean:
    """Verifica contrato de retorno y caché de ``fetch_drybean``."""

    def test_retorna_tupla_correcta(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """fetch_drybean retorna (X, y, df) con tipos esperados."""
        monkeypatch.setattr("src.data_loading.fetch_ucirepo", lambda id: _build_stub_dataset())
        X, y, df = fetch_drybean()

        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert isinstance(df, pd.DataFrame)

    def test_columna_class_presente(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """El dataframe completo contiene la columna ``Class``."""
        monkeypatch.setattr("src.data_loading.fetch_ucirepo", lambda id: _build_stub_dataset())
        _, _, df = fetch_drybean()
        assert "Class" in df.columns

    def test_features_sin_class(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """X no contiene la columna ``Class``."""
        monkeypatch.setattr("src.data_loading.fetch_ucirepo", lambda id: _build_stub_dataset())
        X, _, _ = fetch_drybean()
        assert "Class" not in X.columns
        assert len(X.columns) == len(_FEATURE_COLS)

    def test_cache_dir_escribe_y_lee(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Con cache_dir, la primera llamada escribe Parquet y la segunda lo lee."""
        call_count = 0

        def _mock_fetch(id: int) -> SimpleNamespace:
            nonlocal call_count
            call_count += 1
            return _build_stub_dataset()

        monkeypatch.setattr("src.data_loading.fetch_ucirepo", _mock_fetch)

        # Primera llamada: descarga y cachea
        X1, y1, df1 = fetch_drybean(cache_dir=tmp_path)
        assert (tmp_path / "drybean.parquet").exists()
        assert call_count == 1

        # Segunda llamada: lee del caché, no descarga
        X2, y2, df2 = fetch_drybean(cache_dir=tmp_path)
        assert call_count == 1  # no se llamó de nuevo a fetch_ucirepo


# ---------------------------------------------------------------------------
# Tests de load_drybean
# ---------------------------------------------------------------------------


class TestLoadDrybean:
    """Verifica lectura local desde Parquet y CSV."""

    def test_load_parquet(self, tmp_path: Path) -> None:
        """Carga correctamente un archivo Parquet."""
        df_orig = pd.DataFrame({"Area": [1.0, 2.0], "Class": ["SEKER", "CALI"]})
        path = tmp_path / "test.parquet"
        df_orig.to_parquet(path, index=False)

        df = load_drybean(path)
        assert "Class" in df.columns
        assert len(df) == 2

    def test_load_csv(self, tmp_path: Path) -> None:
        """Carga correctamente un archivo CSV."""
        df_orig = pd.DataFrame({"Area": [1.0, 2.0], "Class": ["SEKER", "CALI"]})
        path = tmp_path / "test.csv"
        df_orig.to_csv(path, index=False)

        df = load_drybean(path)
        assert "Class" in df.columns
        assert len(df) == 2
