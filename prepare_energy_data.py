"""Prepare the project's OWID country-year CSVs without modifying template files.

Run from the repository root: python prepare_energy_data.py
Requires Python 3.10+ and pandas (python -m pip install pandas).
Use --offline to reproduce the saved source snapshot without network access.
Default runs download the specified legacy OWID dataset, which is no longer
updated. See ENERGY_DATA_NOTES.md before migrating to OWID's new dataset.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SNAPSHOT = DATA / "energy_source"
BASE_URL = "https://raw.githubusercontent.com/owid/energy-data/master/"
SOURCE_FILES = ("owid-energy-data.csv", "owid-energy-codebook.csv")
COUNTRIES = (
    "Germany", "Denmark", "Norway", "France", "China", "United States",
    "India", "Brazil", "Japan", "South Africa",
)
START_YEAR = 2000
# Shares give comparable country mixes; generation gives electricity-system size.
# Preserve OWID names and units. Do not mix primary-energy and electricity shares.
COLUMNS = (
    "country", "year", "population", "gdp", "renewables_share_energy",
    "renewables_share_elec", "solar_share_elec", "wind_share_elec",
    "hydro_share_elec", "electricity_generation",
)


def get_sources(offline: bool) -> tuple[dict[str, bytes], dict]:
    """Download in memory, or read and checksum-verify the saved snapshot."""
    if offline:
        manifest = json.loads((SNAPSHOT / "manifest.json").read_text(encoding="utf-8"))
        payloads = {name: (SNAPSHOT / name).read_bytes() for name in SOURCE_FILES}
        for name, content in payloads.items():
            if hashlib.sha256(content).hexdigest() != manifest["files"][name]["sha256"]:
                raise ValueError(f"Snapshot checksum mismatch: {name}")
        return payloads, manifest

    payloads = {}
    for name in SOURCE_FILES:
        request = Request(BASE_URL + name, headers={"User-Agent": "DataStory-Energy/1.0"})
        with urlopen(request, timeout=120) as response:
            payloads[name] = response.read()
    manifest = {
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_status": "Legacy OWID Energy dataset; no longer updated",
        "documentation_url": "https://github.com/owid/energy-data",
        "files": {
            name: {"url": BASE_URL + name, "sha256": hashlib.sha256(content).hexdigest()}
            for name, content in payloads.items()
        },
    }
    return payloads, manifest


def quality_summary(clean: pd.DataFrame) -> pd.DataFrame:
    """Coverage describes non-missing values within the filtered project sample."""
    rows = []
    for column in COLUMNS:
        present = clean[column].notna()
        years = clean.loc[present, "year"]
        rows.append({
            "variable": column,
            "non_missing_observations": int(present.sum()),
            "missing_observations": int((~present).sum()),
            "percentage_missing": round(float((~present).mean() * 100), 2),
            "earliest_available_year": int(years.min()) if len(years) else None,
            "latest_available_year": int(years.max()) if len(years) else None,
        })
    summary = pd.DataFrame(rows)
    for column in ("earliest_available_year", "latest_available_year"):
        summary[column] = summary[column].astype("Int64")
    return summary


def prepare(offline: bool = False) -> None:
    payloads, manifest = get_sources(offline)
    source = pd.read_csv(io.BytesIO(payloads[SOURCE_FILES[0]]), low_memory=False)
    codebook = pd.read_csv(io.BytesIO(payloads[SOURCE_FILES[1]]))
    print(f"Source: {BASE_URL + SOURCE_FILES[0]}")
    print(f"Snapshot retrieved: {manifest['retrieved_at_utc']}")
    print("WARNING: OWID labels this source as legacy and no longer updated.")
    print(f"Source dimensions: {len(source):,} rows x {len(source.columns)} columns")
    print(f"Source year coverage: {source['year'].min()}-{source['year'].max()}")
    print("\nAvailable source columns:\n" + ", ".join(source.columns))

    absent = set(COLUMNS) - set(source.columns)
    if absent:
        raise ValueError(f"Required columns absent from OWID source: {sorted(absent)}")
    missing_countries = set(COUNTRIES) - set(source["country"].dropna())
    if missing_countries:
        raise ValueError(f"Requested countries absent: {sorted(missing_countries)}")
    # Inspect actual alternatives rather than guessing names from earlier releases.
    candidates = [c for c in source.columns if c.startswith(("renewables_", "solar_", "wind_", "hydro_"))
                  and ("share" in c or c.endswith(("consumption", "electricity")))]
    print("\nAvailable renewable measure alternatives:\n" + ", ".join(candidates))
    if not set(COLUMNS).issubset(set(codebook["column"])):
        raise ValueError("Codebook does not describe every selected column")
    definitions = codebook.set_index("column").loc[list(COLUMNS)]
    print("\nSelected definitions and units:")
    print(definitions[["title", "unit", "description"]].to_string())

    clean = source.loc[
        source["country"].isin(COUNTRIES) & source["year"].ge(START_YEAR),
        list(COLUMNS),
    ].copy()
    if clean.empty or set(clean["country"]) != set(COUNTRIES):
        raise ValueError("Not all selected countries have observations from 2000 onward")
    if clean[["country", "year"]].isna().any().any():
        raise ValueError("Missing country-year key")
    if clean.duplicated(["country", "year"]).any():
        raise ValueError("Duplicate country-year observations; refusing to aggregate silently")
    for column in COLUMNS[1:]:
        clean[column] = pd.to_numeric(clean[column], errors="raise")
        if not clean[column].dropna().map(math.isfinite).all():
            raise ValueError(f"Non-finite values in {column}")
    if not clean["year"].eq(clean["year"].astype(int)).all():
        raise ValueError("Non-integer years")
    clean["year"] = clean["year"].astype(int)
    clean = clean.sort_values(["country", "year"]).reset_index(drop=True)
    for column in COLUMNS[2:]:
        values = clean[column].dropna()
        if values.lt(0).any() or ("_share_" in column and values.gt(100).any()):
            raise ValueError(f"Out-of-range observations in {column}; inspect source")

    latest = int(clean["year"].max())
    expected = pd.MultiIndex.from_product([sorted(COUNTRIES), range(START_YEAR, latest + 1)],
                                          names=["country", "year"])
    absent_keys = expected.difference(pd.MultiIndex.from_frame(clean[["country", "year"]]))
    print(f"\nMissing country-year keys in 2000-{latest}: {len(absent_keys)}")
    if len(absent_keys):
        print(absent_keys.tolist())
        print("Absent source rows are reported, not fabricated.")
    summary = quality_summary(clean)
    print(f"\nClean dimensions: {len(clean)} rows x {len(clean.columns)} columns")
    print(f"Clean year coverage: {clean['year'].min()}-{latest}")
    print("Countries: " + ", ".join(sorted(clean["country"].unique())))
    print("Selected columns: " + ", ".join(COLUMNS))
    print("\nCountry-year coverage:")
    print(clean.groupby("country")["year"].agg(["min", "max", "count"]).to_string())
    print("\nMissing values and variable coverage (project sample):")
    print(summary.to_string(index=False))
    print("\nMissing counts by country:")
    print(clean.groupby("country")[list(COLUMNS[2:])].agg(lambda s: s.isna().sum()).to_string())
    print("\nLatest non-missing year by country and variable:")
    latest_by_country = pd.DataFrame({
        column: clean.loc[clean[column].notna()].groupby("country")["year"].max()
        for column in COLUMNS[2:]
    }).reindex(sorted(COUNTRIES))
    print(latest_by_country.to_string())
    rates = summary.set_index("variable")["percentage_missing"]
    print(f"\nGDP missing: {rates['gdp']:.2f}%; energy-variable missing range: "
          f"{rates[list(COLUMNS[4:])].min():.2f}%-{rates[list(COLUMNS[4:])].max():.2f}%")
    print("GDP is suitable only for years where observed. Consider another compatible "
          "source for recent-year economic comparisons; do not fill or splice silently.")
    print("Missing values remain blank; zeros remain zero. No imputation or row dropping.")

    # Only these project-owned files are written. All template files remain untouched.
    DATA.mkdir(exist_ok=True)
    if not offline:
        SNAPSHOT.mkdir(exist_ok=True)
        for name, content in payloads.items():
            (SNAPSHOT / name).write_bytes(content)
        (SNAPSHOT / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    clean_path = DATA / "energy_10countries_clean.csv"
    summary_path = DATA / "energy_data_quality_summary.csv"
    clean.to_csv(clean_path, index=False, na_rep="", lineterminator="\n")
    summary.to_csv(summary_path, index=False, na_rep="", lineterminator="\n")
    # Verify persisted outputs preserve all values, including missingness.
    pd.testing.assert_frame_equal(clean, pd.read_csv(clean_path), check_dtype=False)
    pd.testing.assert_frame_equal(summary, pd.read_csv(summary_path), check_dtype=False)
    print(f"\nSaved and verified: {clean_path.relative_to(ROOT)}")
    print(f"Saved and verified: {summary_path.relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true",
                        help="Rebuild using saved, checksum-verified source files")
    prepare(offline=parser.parse_args().offline)
