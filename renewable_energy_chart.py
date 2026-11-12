"""Create a preliminary renewable-energy comparison from live OWID data.

Install the only external dependency: python -m pip install matplotlib
Run in VS Code's terminal: python renewable_energy_chart.py

Metric definitions: https://github.com/owid/energy-data/blob/master/owid-energy-codebook.csv
renewables_share_energy measures the renewable share of PRIMARY energy
consumption (substitution method). renewables_share_elec covers electricity
generation only, so it is not used for this broader energy comparison.
"""

import csv
import hashlib
import io
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.request import urlopen

import matplotlib

matplotlib.use("Agg")  # Save reliably in VS Code, terminals, and headless sessions.
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


DATA_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
METRIC = "renewables_share_energy"
COUNTRIES = (
    "Germany", "Denmark", "Norway", "France", "China", "United States",
    "India", "Brazil", "Japan", "South Africa",
)
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_PNG = PROJECT_DIR / "renewable_energy_share_by_country.png"


def load_latest_values():
    """Read source rows directly; validate before selecting the latest per country.

    Keep full source precision for validation, sorting, and bar heights.
    Display percentages rounded to one decimal place.
    Missing values are skipped; values are never filled, estimated, or interpolated.
    """
    with urlopen(DATA_URL, timeout=120) as response:
        raw_csv = response.read()
    reader = csv.DictReader(io.StringIO(raw_csv.decode("utf-8-sig")))
    required = {"country", "year", METRIC}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError(f"OWID CSV is missing required columns: {required}")

    latest = {}
    seen = set()
    for row in reader:
        country = row["country"]
        if country not in COUNTRIES:
            continue
        try:
            year = int(row["year"])
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Invalid source year for {country}: {row['year']}") from exc
        if (country, year) in seen:
            raise ValueError(f"Duplicate source row: {country}, {year}")
        seen.add((country, year))

        source_value = row[METRIC].strip()
        if not source_value:
            continue
        try:
            value = Decimal(source_value)
        except InvalidOperation as exc:
            raise ValueError(f"Invalid percentage for {country}, {year}") from exc
        if not value.is_finite() or not 0 <= value <= 100:
            raise ValueError(f"Percentage outside 0-100: {country}, {year}: {value}")
        # Retain the original country, year, and share from the downloaded row.
        if country not in latest or year > latest[country]["year"]:
            latest[country] = {
                "country": country, "year": year,
                "share": value, "source_value": source_value,
            }

    missing = set(COUNTRIES) - set(latest)
    if missing:
        raise ValueError(f"No renewable-energy observations for: {sorted(missing)}")
    records = sorted(latest.values(), key=lambda item: (-item["share"], item["country"]))
    print(f"Downloaded directly from: {DATA_URL}")
    print(f"Retrieved (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print(f"Source CSV SHA-256: {hashlib.sha256(raw_csv).hexdigest()}")
    print(f"Verified {len(records)} source observations; latest non-missing year per country.")
    return records


def print_table(records):
    print("\nMetric: renewables_share_energy (primary energy, substitution method).")
    print("renewables_share_elec measures electricity only and is not used.\n")
    print(f"{'country':<15} | {'year':<4} | renewable energy share")
    print("-" * 51)
    for item in records:
        print(f"{item['country']:<15} | {item['year']:<4} | {item['share']:.1f}%")


def plot_chart(records):
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12,
        "text.color": "#172B36", "axes.labelcolor": "#334B56",
        "xtick.color": "#334B56", "ytick.color": "#536873",
    })
    fig, ax = plt.subplots(figsize=(14, 8), facecolor="white")
    fig.subplots_adjust(left=0.085, right=0.98, bottom=0.23, top=0.76)
    positions = list(range(len(records)))
    bars = ax.bar(positions, [float(item["share"]) for item in records],
                  width=0.66, color="#16857D", zorder=3)
    ax.bar_label(bars, labels=[f"{item['share']:.1f}%" for item in records],
                 padding=8, fontsize=11, fontweight="bold", color="#172B36")
    # Years remain visible even if countries have different latest observations.
    names = {"United States": "United\nStates", "South Africa": "South\nAfrica"}
    ax.set_xticks(positions, [f"{names.get(item['country'], item['country'])}\n{item['year']}"
                              for item in records], fontsize=11)
    ax.set_ylabel("Renewable energy share (%)", labelpad=14)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#E5EBED", linewidth=0.8)
    ax.tick_params(axis="both", length=0, pad=10)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.text(0.085, 0.925, "Renewable Energy Share by Country",
             fontsize=25, fontweight="bold", ha="left")
    fig.text(0.085, 0.874, "Preliminary project visual",
             fontsize=14, color="#536873", ha="left")
    fig.text(0.085, 0.817,
             "Primary energy consumption | Latest available year per country",
             fontsize=11, color="#536873", ha="left")
    fig.text(0.085, 0.087, "Source: Our World in Data Energy Dataset",
             fontsize=10, color="#536873")
    fig.text(0.085, 0.052,
             "Primary energy: substitution method | Percentages rounded to 1 decimal place",
             fontsize=9, color="#536873")
    fig.savefig(OUTPUT_PNG, dpi=300, facecolor="white")
    plt.close(fig)
    print(f"\nSaved chart: {OUTPUT_PNG} (4200 x 2400 pixels, 300 dpi)")


def main():
    records = load_latest_values()  # All checks finish before plotting.
    print_table(records)
    plot_chart(records)


if __name__ == "__main__":
    main()
