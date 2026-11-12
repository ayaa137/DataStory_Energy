# Renewable Energy Transition Across Countries: data preparation

## Run and reproduce

From the repository root, with Python 3.10+ and pandas installed:

```powershell
python prepare_energy_data.py
```

The script downloads the explicitly requested OWID CSV and its codebook, inspects
all column names and renewable-measure alternatives, validates the selected data,
and prints sample-wide and country-specific missingness and coverage. It writes:

- `data/energy_10countries_clean.csv`: the working dataset.
- `data/energy_data_quality_summary.csv`: coverage for every selected column.
- `data/energy_source/owid-energy-data.csv`: unmodified full source snapshot.
- `data/energy_source/owid-energy-codebook.csv`: source definitions and units.
- `data/energy_source/manifest.json`: retrieval time, source URLs, SHA-256 checksums.

To reproduce the saved snapshot without downloading a potentially revised source:

```powershell
python prepare_energy_data.py --offline
```

Offline mode verifies source checksums. A normal run refreshes the project-owned
source snapshot and generated CSVs. It never writes to existing course templates.
CSV outputs are UTF-8, comma-separated, with blank cells for missing values.

## Source and important migration warning

Requested source:
https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv

Definitions:
https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-codebook.csv

OWID repository documentation: https://github.com/owid/energy-data

Inspected on 12 November 2026. The source has 23,377 rows, 130 columns, and years
1900–2025. The manifest records the precise download time and content checksums.

OWID now labels this GitHub dataset as **legacy and no longer updated**. Its README
links a replacement dataset with a changed primary-energy methodology, codebook,
and column mapping. This project deliberately uses the URL requested for this step.
“Latest available” below means latest in that file, not necessarily latest in the
replacement. Before future updates, decide explicitly whether to migrate and
rebuild the entire historical series. Do not append new-methodology observations
to this legacy primary-energy series.

## Selected columns and reasons

| Exact OWID column | Unit | Role and selection reason |
| --- | --- | --- |
| `country` | country name | Country-year identifier. |
| `year` | calendar year | Time identifier for adoption and transition speed. |
| `population` | people | Demographic context and potential denominator for later per-person measures. |
| `gdp` | international dollars in 2011 prices | Total output, adjusted for inflation and differences in living costs; economic context. Not GDP per capita or current US dollars. |
| `renewables_share_energy` | percent of primary energy consumption | Broad renewable adoption, using OWID's legacy substitution method. This extends beyond electricity. |
| `renewables_share_elec` | percent of electricity generated | Renewable adoption within electricity; supplies the same denominator as the three source shares. |
| `solar_share_elec` | percent of electricity generated | Solar's contribution to each country's electricity mix, comparable across differently sized systems. |
| `wind_share_elec` | percent of electricity generated | Wind's contribution on the same basis. |
| `hydro_share_elec` | percent of electricity generated | Hydropower's contribution on the same basis. |
| `electricity_generation` | terawatt-hours (TWh) | Total electricity produced; gives the scale behind percentage comparisons. |

Shares use a 0–100 scale, not a 0–1 fraction. Source-specific shares were preferred
to absolute consumption or generation because the project compares countries of
very different sizes. The codebook also offers `solar_electricity`,
`wind_electricity`, `hydro_electricity`, source-specific primary-energy consumption,
and primary-energy shares. Those are valid measures for other questions but are
unnecessary in this focused working dataset. Total generation retains system size
without letting country size dominate comparisons of renewable adoption.

Do not stack electricity shares with `renewables_share_energy`: their denominators
differ. Solar, wind, and hydro are not all renewable sources; bioenergy and other
renewables also contribute. Do not label their sum as total renewables. Renewables
are also distinct from low-carbon energy, which includes nuclear. In particular,
renewable shares alone do not describe France's full low-carbon electricity mix.
Generation describes domestic production, not electricity consumption or imports.
The primary-energy indicator should not be relabeled as renewable final-energy
consumption or an SDG indicator.

## Observed data quality

The clean dataset contains **260 rows and 10 columns**, one unique row per country
and year, covering **2000–2025 inclusive** for Germany, Denmark, Norway, France,
China, United States, India, Brazil, Japan, and South Africa. Each country has all
26 year keys; no duplicates or missing country-year keys were found.

| Variables | Non-missing | Missing | Percent missing | Observed years |
| --- | ---: | ---: | ---: | --- |
| `gdp` | 230 | 30 | 11.54% | 2000–2022 |
| `renewables_share_energy` | 250 | 10 | 3.85% | 2000–2024 |
| Every other selected column, individually | 260 | 0 | 0% | 2000–2025 |

The pattern is identical across all 10 countries: GDP is missing in 2023–2025,
and primary-energy renewable share is missing in 2025. There are no earlier gaps
in these selected series. The machine-readable quality summary measures coverage
within the filtered project sample, not the full historical source.

GDP has materially more missing data than the energy measures. OWID's GDP is
sufficient for historical economic context through 2022. If later analysis needs
GDP relationships in 2023–2025, obtain another consistent economic series and
check its price base, purchasing-power adjustment, and source methodology. Prefer
a consistent replacement over the full comparison period rather than silently
splicing incompatible dollar series. No economic data were added in this step.
For economic comparisons between countries, GDP per person can later be computed
from observed GDP and population; total GDP mainly reflects economic size.

All observations are preserved. No interpolation, extrapolation, forward filling,
zero replacement, aggregation, or dropping rows for missing values was performed.
Reported zeros remain zero. Numeric parsing, finiteness, nonnegative measures,
0–100 share bounds, unique keys, country availability, and CSV round trips are
validated by the script. These checks establish structural quality and observed
coverage, not independent verification of each source estimate.

## Suitability for the planned story

2000 onward is a sensible multi-decade window for comparing renewable adoption,
electricity-source mixes, and transition speed. Use **2000–2025 for electricity**,
**2000–2024 for primary-energy renewable shares**, and **2000–2022 when GDP is
required**. Preserve the full dataset and choose the common observed period for
each future chart or analysis. Do not imply that all variables describe 2025.

All 10 countries are suitable on the observed coverage and offer varied renewable
mixes. This is a deliberately selected comparison group, not a representative
sample of the world. Population and GDP provide context; the dataset alone cannot
establish that economic or demographic differences cause adoption differences.
No project charts or 3D visualizations were created in this step.
