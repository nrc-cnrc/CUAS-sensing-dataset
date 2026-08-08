"""Example: load and plot radar tracks from the UAV vs. Bird Radar Tracks Dataset.

Requires: pandas, openpyxl, matplotlib
    pip install pandas openpyxl matplotlib

Run from the repository root:
    python examples/load_tracks.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import openpyxl
import pandas as pd

REPO = Path(__file__).resolve().parents[1]


def _sheet_to_df(worksheet):
    rows = worksheet.iter_rows(values_only=True)
    header = next(rows)
    return pd.DataFrame(rows, columns=header)


def load_annotated_session(xlsx_path):
    """Load an annotated .xlsx session -> (tracks_df, labels_df).

    tracks_df has one row per track update; labels_df maps SystemTrackID to
    the expert ground-truth Classification.
    """
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    tracks = _sheet_to_df(wb.worksheets[0])
    labels = _sheet_to_df(wb.worksheets[1])
    wb.close()
    labels.columns = ["SystemTrackID", "Classification"]
    return tracks, labels


def load_raw_log(csv_path):
    """Load a raw Echodyne log (.csv or .csv.gz, comma- or semicolon-delimited)."""
    with pd.io.common.get_handle(csv_path, "r", compression="infer") as h:
        first_line = h.handle.readline()
    sep = ";" if first_line.count(";") > first_line.count(",") else ","
    df = pd.read_csv(csv_path, sep=sep, low_memory=False)
    return df.loc[:, ~df.columns.str.startswith("Unnamed")]


def main():
    # --- 1. An annotated session: plot every labeled track, colored by class ---
    session = REPO / "data" / "Demo-2" / "Echodyne_Log_20201119_151809.xlsx"
    tracks, labels = load_annotated_session(session)
    merged = tracks.merge(labels, on="SystemTrackID", how="inner")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    colors = {"UAV": "tab:red", "BIRD": "tab:blue", "BURD": "tab:blue"}
    for (tid, cls), g in merged.groupby(["SystemTrackID", "Classification"]):
        key = str(cls).strip().upper()
        ax1.plot(g["posX"], g["posY"],
                 color=colors.get(key, "tab:gray"), alpha=0.7, lw=1)
    ax1.set_xlabel("posX [m]")
    ax1.set_ylabel("posY [m]")
    ax1.set_title(f"{session.name}\n(red = UAV, blue = Bird)")
    ax1.set_aspect("equal", adjustable="datalim")

    # --- 2. A curated raw-log UAV extract: range over time ---
    extract = REPO / "data" / "Demo-7" / "Echodyne_Log_20210318_102509_UAV_1.csv"
    raw = load_raw_log(extract)
    t = pd.to_datetime(raw["timeStamp"], format="%Y%m%dT%H%M%S.%fZ")
    ax2.plot(t, raw["range"], lw=1)
    ax2.set_xlabel("time (UTC)")
    ax2.set_ylabel("range [m]")
    ax2.set_title(extract.name)
    fig.autofmt_xdate()

    fig.tight_layout()
    out = REPO / "examples" / "example_tracks.png"
    fig.savefig(out, dpi=150)
    print(f"Saved {out}")

    # --- 3. Dataset-wide label index ---
    all_labels = pd.read_csv(REPO / "metadata" / "track_labels.csv")
    print("\nLabeled tracks per class:")
    print(all_labels["label"].value_counts().to_string())


if __name__ == "__main__":
    main()
