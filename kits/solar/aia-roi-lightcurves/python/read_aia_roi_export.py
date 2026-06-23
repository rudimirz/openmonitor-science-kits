"""Read an OpenMonitor AIA ROI export.

This helper is intentionally small: it is meant for scientists who downloaded
an AIA ROI FITS/CSV/ECSV file from Solar Lab and want to inspect the columns,
metadata, and optionally make a quick local plot.

Examples:

    python kits/solar/aia-roi-lightcurves/python/read_aia_roi_export.py lightcurves.fits
    python kits/solar/aia-roi-lightcurves/python/read_aia_roi_export.py lightcurves.csv --plot
    python kits/solar/aia-roi-lightcurves/python/read_aia_roi_export.py lightcurves.fits --metadata metadata.json --plot curve.png
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def read_table(path: Path) -> tuple[list[str], list[dict[str, Any]], dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix in {".fits", ".fit", ".ecsv"}:
        try:
            from astropy.table import Table
        except ImportError as exc:  # pragma: no cover - depends on local env
            raise SystemExit(
                "Astropy is required for FITS/ECSV. Install it or use the CSV export."
            ) from exc
        table = Table.read(path)
        rows = [{name: row[name].item() if hasattr(row[name], "item") else row[name] for name in table.colnames} for row in table]
        return list(table.colnames), rows, dict(table.meta)

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return list(reader.fieldnames or []), rows, {}


def load_metadata(path: Path | None) -> dict[str, Any]:
    if not path:
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def roi_columns(columns: list[str]) -> list[str]:
    ignored = {"UTC", "utc", "time", "Time"}
    return [
        name for name in columns
        if name not in ignored
        and not name.endswith("_sat_frac")
        and not name.endswith("_saturated")
    ]


def as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def print_summary(path: Path, columns: list[str], rows: list[dict[str, Any]], metadata: dict[str, Any]) -> None:
    print(f"File: {path}")
    print(f"Rows: {len(rows)}")
    print("Columns:")
    for name in columns:
        print(f"  - {name}")
    if rows and "UTC" in rows[0]:
        print(f"UTC span: {rows[0]['UTC']} -> {rows[-1]['UTC']}")
    curves = roi_columns(columns)
    if curves:
        print("ROI light-curve columns:")
        for name in curves:
            values = [as_float(row.get(name)) for row in rows]
            numeric = [value for value in values if value is not None]
            if numeric:
                print(f"  - {name}: min={min(numeric):.6g}, max={max(numeric):.6g}")
            else:
                print(f"  - {name}")
    if metadata:
        print("Metadata keys:")
        for key in sorted(metadata):
            print(f"  - {key}")


def plot_table(path: Path, columns: list[str], rows: list[dict[str, Any]], output: Path | None) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:  # pragma: no cover - depends on local env
        raise SystemExit("matplotlib is required for --plot") from exc

    curves = roi_columns(columns)
    if not curves:
        raise SystemExit("No ROI light-curve columns found to plot.")
    x = list(range(len(rows)))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for name in curves:
        y = [as_float(row.get(name)) for row in rows]
        ax.plot(x, y, label=name, linewidth=1.8)
    ax.set_xlabel("Frame index")
    ax.set_ylabel("ROI mean intensity")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    if output is None:
        output = path.with_suffix(".quicklook.png")
    fig.savefig(output, dpi=160)
    print(f"Plot written: {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read an OpenMonitor AIA ROI export.")
    parser.add_argument("table", type=Path, help="Downloaded lightcurves.csv, lightcurves.ecsv, or lightcurves.fits")
    parser.add_argument("--metadata", type=Path, help="Optional downloaded metadata.json")
    parser.add_argument(
        "--plot",
        nargs="?",
        const="",
        default=None,
        help="Write a quick PNG plot. Optionally pass an output filename.",
    )
    args = parser.parse_args()

    columns, rows, table_metadata = read_table(args.table)
    sidecar = load_metadata(args.metadata)
    metadata = {**table_metadata, **sidecar}
    print_summary(args.table, columns, rows, metadata)
    if args.plot is not None:
        output = Path(args.plot) if args.plot else None
        plot_table(args.table, columns, rows, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
