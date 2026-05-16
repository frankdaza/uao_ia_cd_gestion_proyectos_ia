#!/usr/bin/env python3
"""Comprueba coherencia entre artefactos de evaluación y el informe (§5).

Ejecutar desde la raíz del repositorio:

    uv run python scripts/verify_informe_artifacts.py

Valida: ``comparison.csv`` frente a ``metrics_baseline.json`` y ``metrics_rf.json``;
contenido clave de ``classification_report.txt``; existencia de figuras referenciadas
en el informe (matriz de confusión, importancia de variables, comparación de modelos).
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "outputs" / "reports"


def _round4(x: str | float) -> float:
    return round(float(x), 4)


def main() -> int:
    errors: list[str] = []

    metrics_bl = json.loads((REPORTS / "metrics_baseline.json").read_text(encoding="utf-8"))
    metrics_rf = json.loads((REPORTS / "metrics_rf.json").read_text(encoding="utf-8"))

    with (REPORTS / "comparison.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    by_model = {r["model"]: r for r in rows}
    for name, expected in (
        ("baseline", metrics_bl),
        ("random_forest", metrics_rf),
    ):
        if name not in by_model:
            errors.append(f"Falta fila '{name}' en comparison.csv")
            continue
        row = by_model[name]
        if _round4(row["accuracy"]) != _round4(expected["accuracy"]):
            ra, rb = _round4(row["accuracy"]), _round4(expected["accuracy"])
            errors.append(f"{name} accuracy: CSV {ra} != metrics {rb}")
        if _round4(row["f1_macro"]) != _round4(expected["f1_macro"]):
            rf, mf = _round4(row["f1_macro"]), _round4(expected["f1_macro"])
            errors.append(f"{name} f1_macro: CSV {rf} != metrics {mf}")

    # Cifras publicadas en informe_laboratorio.md §5.1 (redondeo a 4 decimales)
    informe = (REPORTS / "informe_laboratorio.md").read_text(encoding="utf-8")
    for needle in (
        "| **Baseline (LR)** | **0.9195** | **0.9306** |",
        "| Random Forest     | 0.9181   | 0.9295   |",
    ):
        if needle not in informe:
            errors.append(f"Informe §5.1: falta línea esperada: {needle!r}")

    report = (REPORTS / "classification_report.txt").read_text(encoding="utf-8")
    for line in (
        "    BARBUNYA       0.93      0.89      0.91       265",
        "        SIRA       0.86      0.89      0.87       527",
        "    accuracy                           0.92      2709",
    ):
        if line not in report:
            errors.append(f"classification_report.txt: falta línea: {line!r}")

    for png in ("confusion_matrix.png", "feature_importance.png", "comparison_chart.png"):
        p = REPORTS / png
        if not p.is_file() or p.stat().st_size == 0:
            errors.append(f"Figura ausente o vacía: {png}")

    if errors:
        print("Errores de verificación:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("OK: comparison.csv alineado con metrics_*.json; informe §5.1; reporte por clase; PNGs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
