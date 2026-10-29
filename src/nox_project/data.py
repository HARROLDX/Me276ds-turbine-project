"""Verified original CSVs; year and row IDs are metadata, never predictors."""

import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

import numpy as np
import pandas as pd

FEATURES = ["AT", "AP", "AH", "AFDP", "GTEP", "TIT", "TAT", "TEY", "CDP"]
TARGET = "NOX"
COLUMNS = FEATURES + ["CO", TARGET]
TRAIN_YEARS = (2011, 2012, 2013, 2014)
HOLDOUT_YEAR = 2015
SPLIT_PROTOCOL = "2011-2014 train; 2015 first floor(N/2) validation; remaining test"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_manifest(root):
    return json.loads((Path(root) / "data/manifest.json").read_text())


def download(root):
    """Restore missing files from a pinned UCI archive, without overwriting data."""
    root = Path(root)
    manifest = read_manifest(root)
    raw = root / "data/raw"
    raw.mkdir(parents=True, exist_ok=True)
    missing = []
    for name, info in manifest["files"].items():
        path = raw / name
        if path.exists():
            if sha256(path) != info["sha256"]:
                raise ValueError(f"Modified data: {path}; refusing to overwrite")
        else:
            missing.append(name)
    if not missing:
        return {"downloaded": [], "status": "all checksums match"}
    with urlopen(manifest["source_url"], timeout=60) as response:
        payload = response.read()
    if hashlib.sha256(payload).hexdigest() != manifest["archive_sha256"]:
        raise ValueError("UCI archive changed; review provenance before updating the manifest")
    with ZipFile(io.BytesIO(payload)) as archive:
        for name in missing:
            content = archive.read(name)
            if hashlib.sha256(content).hexdigest() != manifest["files"][name]["sha256"]:
                raise ValueError(f"Checksum mismatch: {name}")
            with (raw / name).open("xb") as stream:
                stream.write(content)
    return {"downloaded": missing, "status": "verified"}


def validate_frame(frame):
    if list(frame.columns) != COLUMNS:
        raise ValueError(f"Unexpected columns: {list(frame.columns)}")
    if not all(pd.api.types.is_numeric_dtype(frame[c]) for c in COLUMNS):
        raise ValueError("All original columns must be numeric")
    if not np.isfinite(frame.to_numpy(dtype=float)).all():
        raise ValueError("Missing or non-finite values in original data")


def load_years(root, years):
    """Read original rows without reordering or inventing timestamps."""
    manifest = read_manifest(root)
    frames = []
    for year in years:
        name = f"gt_{year}.csv"
        path = Path(root) / "data/raw" / name
        if sha256(path) != manifest["files"][name]["sha256"]:
            raise ValueError(f"Checksum mismatch: {name}")
        frame = pd.read_csv(path)
        validate_frame(frame)
        if len(frame) != manifest["files"][name]["rows"]:
            raise ValueError(f"Unexpected row count: {name}")
        frame["year"] = year
        frame["row_id"] = [f"{year}:{i}" for i in range(len(frame))]
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def audit(root):
    """Structural QA only on test years; descriptive statistics use development only."""
    rows = []
    for year in TRAIN_YEARS + (HOLDOUT_YEAR,):
        frame = load_years(root, [year])
        rows.append(
            {
                "year": year,
                "rows": len(frame),
                "columns": 11,
                "missing": int(frame[COLUMNS].isna().sum().sum()),
                "duplicate_measurement_rows": int(frame[COLUMNS].duplicated().sum()),
            }
        )
    dev = load_years(root, TRAIN_YEARS)
    return {
        "status": "passed",
        "training_performed": False,
        "years": rows,
        "total_rows": sum(r["rows"] for r in rows),
        "features": FEATURES,
        "target": TARGET,
        "excluded": ["CO", "year", "row_id"],
        "training_summary": dev[COLUMNS].describe().to_dict(),
        "note": "No test target distributions or model scores inspected. No rows removed.",
    }


def partition_holdout(frame):
    """Chronological disjoint blocks; raw records have no exact timestamps."""
    midpoint = len(frame) // 2
    if midpoint < 2:
        raise ValueError("Holdout requires at least four rows")
    return frame.iloc[:midpoint].copy(), frame.iloc[midpoint:].copy()


def load_development(root):
    train = load_years(root, TRAIN_YEARS)
    validation, _ = partition_holdout(load_years(root, [HOLDOUT_YEAR]))
    return train, validation


def load_test(root):
    _, test = partition_holdout(load_years(root, [HOLDOUT_YEAR]))
    return test
