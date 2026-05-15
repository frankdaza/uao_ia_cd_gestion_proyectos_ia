"""Pruebas unitarias para src.preprocessing (clean y split)."""

from __future__ import annotations

import pandas as pd

from src.preprocessing import clean, split

# ---------------------------------------------------------------------------
# Datos sintéticos de prueba
# ---------------------------------------------------------------------------

_CLASSES = ["SEKER", "BARBUNYA", "BOMBAY", "CALI", "HOROZ", "SIRA", "DERMASON"]


def _make_df(n_per_class: int = 10, with_duplicates: bool = False) -> pd.DataFrame:
    """Genera un DataFrame sintético similar al Dry Bean Dataset."""
    rows = []
    for cls in _CLASSES:
        for i in range(n_per_class):
            rows.append({"Area": float(i), "Perimeter": float(i * 2), "Class": cls})
    df = pd.DataFrame(rows)
    if with_duplicates:
        df = pd.concat([df, df.head(5)], ignore_index=True)
    return df


# ---------------------------------------------------------------------------
# Tests de clean
# ---------------------------------------------------------------------------


class TestClean:
    """Verifica que clean() elimina duplicados y maneja nulos correctamente."""

    def test_elimina_duplicados(self) -> None:
        """Las filas duplicadas se eliminan."""
        df = _make_df(with_duplicates=True)
        n_original_sin_dup = len(_make_df())
        df_limpio = clean(df)
        assert len(df_limpio) == n_original_sin_dup

    def test_columna_class_presente(self) -> None:
        """El dataframe limpio conserva la columna Class."""
        df_limpio = clean(_make_df())
        assert "Class" in df_limpio.columns

    def test_no_muta_entrada(self) -> None:
        """La función no modifica el DataFrame de entrada."""
        df = _make_df(with_duplicates=True)
        n_filas_original = len(df)
        _ = clean(df)
        assert len(df) == n_filas_original

    def test_elimina_filas_con_nulos(self) -> None:
        """Las filas con nulos en features se eliminan."""
        df = _make_df()
        df.loc[0, "Area"] = None
        df_limpio = clean(df)
        assert not df_limpio.isna().any().any()
        assert len(df_limpio) == len(_make_df()) - 1

    def test_index_reseteado(self) -> None:
        """El índice queda continuo tras la limpieza."""
        df = _make_df(with_duplicates=True)
        df_limpio = clean(df)
        assert list(df_limpio.index) == list(range(len(df_limpio)))


# ---------------------------------------------------------------------------
# Tests de split
# ---------------------------------------------------------------------------


class TestSplit:
    """Verifica partición train/test estratificada."""

    def test_proporciones(self) -> None:
        """El split respeta la proporción 80/20 aproximada."""
        df = clean(_make_df(n_per_class=20))
        X_train, X_test, y_train, y_test = split(df, test_size=0.2)
        total = len(X_train) + len(X_test)
        assert abs(len(X_test) / total - 0.2) < 0.05

    def test_determinismo(self) -> None:
        """Dos llamadas con el mismo random_state producen el mismo resultado."""
        df = clean(_make_df(n_per_class=20))
        X1, _, y1, _ = split(df, random_state=42)
        X2, _, y2, _ = split(df, random_state=42)
        pd.testing.assert_frame_equal(X1.reset_index(drop=True), X2.reset_index(drop=True))
        pd.testing.assert_series_equal(y1.reset_index(drop=True), y2.reset_index(drop=True))

    def test_estratificacion(self) -> None:
        """La proporción de cada clase se mantiene en train y test."""
        df = clean(_make_df(n_per_class=50))
        _, _, y_train, y_test = split(df, test_size=0.2)

        prop_train = y_train.value_counts(normalize=True).sort_index()
        prop_test = y_test.value_counts(normalize=True).sort_index()

        for cls in _CLASSES:
            assert abs(prop_train[cls] - prop_test[cls]) < 0.05

    def test_no_muta_entrada(self) -> None:
        """La función no modifica el DataFrame de entrada."""
        df = clean(_make_df(n_per_class=20))
        n_filas = len(df)
        cols = list(df.columns)
        _ = split(df)
        assert len(df) == n_filas
        assert list(df.columns) == cols

    def test_class_no_en_features(self) -> None:
        """X_train y X_test no contienen la columna Class."""
        df = clean(_make_df(n_per_class=20))
        X_train, X_test, _, _ = split(df)
        assert "Class" not in X_train.columns
        assert "Class" not in X_test.columns
