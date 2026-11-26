# Renewable Energy Transition Across Countries

**Team:** Aya Abdine, Meriam El Askri, Mcolisi Austine, Ghofran Mahmoud

**Course:** Visual Communication and Data Storytelling

We compare renewable-energy adoption, electricity-source mixes, and changes over time for Germany, Denmark, Norway, France, China, the United States, India, Brazil, Japan, and South Africa. The project is for general readers interested in sustainability and global development.

## Research questions

1. How does renewable-energy adoption differ across the 10 selected countries?
2. How do countries differ in the renewable sources they rely on, especially solar, wind, and hydropower?
3. What patterns appear when we compare renewable-energy adoption with economic context and change over time?

**Main finding.** There is no single path to renewable energy. Norway led the group in renewable primary-energy share in 2024, while Denmark made the largest percentage-point gain since 2000. Hydropower stands out in Norway and Brazil, and wind stands out in Denmark. Countries at different income levels can have similar renewable shares, and countries with similar incomes can have very different shares.

## Data and limitations

The project uses a checksum-verified snapshot of the [legacy Our World in Data Energy Dataset](https://github.com/owid/energy-data) and [Natural Earth country boundaries](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/). The 260-row panel covers 2000–2025. Electricity series extend through 2025. Primary-energy shares end in 2024, the common reference year for the energy figures. GDP ends in 2022 for all ten countries, making 2022 the latest common year for income comparisons.

Primary-energy share uses OWID’s legacy substitution method. Renewable electricity share divides generation from all renewable sources by total electricity generation. The source-mix charts and map show hydro, wind, and solar as shares of all electricity generation. Renewable electricity volume is estimated as total generation in TWh multiplied by the reported renewable electricity share divided by 100.

Blank observations are preserved. The countries were selected for contrast, and the analysis describes patterns within that group. GDP per capita is in purchasing-power-adjusted 2011 international dollars per person. See [the data notes](ENERGY_DATA_NOTES.md) for units, coverage, and OWID’s methodology change.

## Reproduce the analysis

From the repository root, use a Python 3.13 environment and install the pinned dependencies.

```powershell
python -m pip install -r requirements.txt
```

Open the notebooks in Jupyter and use **Restart Kernel and Run All** on each notebook in order. To run the same sequence from the command line, use the following commands. Jupyter writes executed copies with the `.nbconvert.ipynb` suffix.

```powershell
jupyter nbconvert --to notebook --execute notebooks/01_data_preparation.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_main_insights.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_visual_drafts.ipynb
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=240 notebooks/04_3d_visualization.ipynb
```

Notebook 01 rebuilds the two analysis CSVs offline using the saved OWID files. Notebook 03 rebuilds Visuals 1–4. Notebook 04 assembles the visual story and refreshes the other figures. It uses the checked-in map PNG during normal runs. To regenerate the map PNG, install Chrome or Chromium for Kaleido and set `ENERGY_EXPORT_MAP_PNG=1` before running Notebook 04. Kaleido also exports the PNG when the file is absent. If using a custom Chromium executable, set `BROWSER_PATH` to its full path.

Open either interactive HTML file directly in a desktop browser. Both bundle Plotly and the chart data and work offline. The 3D map requires browser WebGL support. A wide window works best for the map’s labels and controls, and the PNG provides a static fallback.

## Visuals

| Visual | Measure and period |
| --- | --- |
| [1 · Renewable adoption](visuals/01_renewable_adoption_2024.png) | Renewable primary-energy share, 2024 |
| [2 · Electricity pathways](visuals/02_renewable_electricity_pathways_2024.png) | Solar, wind, and hydro shares of electricity generation, 2024 |
| [3 · Income context](visuals/03_gdp_vs_renewables.png) | GDP per capita and renewable primary-energy share, 2022 |
| [4 · Renewable-energy gains](visuals/04_transition_over_time.png) | Primary-energy shares and percentage-point change, 2000–2024 |
| [5 · Animated 3D map](visuals/05_3d_renewable_energy_map.html) · [2024 PNG](visuals/05_3d_renewable_energy_map.png) | Hydro, wind, and solar shares of electricity generation, every year from 2000 to 2024 |
| [6 · Electricity and primary energy](visuals/06_electricity_vs_total_energy.png) | Two renewable shares and their percentage-point gap, latest common year 2024 |
| [7 · Electricity source mix over time](visuals/07_source_mix_over_time.png) | Hydro, wind, and solar shares of electricity generation, 2000–2024 |
| [8 · Animated income comparison](visuals/08_income_vs_renewables_over_time.html) · [2022 PNG](visuals/08_income_vs_renewables_over_time.png) | GDP per capita and renewable primary-energy share in 2000, 2005, 2010, 2015, 2020, and 2022 |
| [9 · Electricity share and volume](visuals/09_share_vs_volume.png) | Renewable electricity share and estimated generation in TWh, 2024 |

## Repository guide

- `notebooks/` contains the four notebooks, from data preparation through the integrated visual story.
- `data/` contains the raw snapshot and codebook in `energy_source/`, the working panel, its coverage summary, and the map geometry.
- `visuals/` contains the nine visualizations and the two interactive figures’ stills.
- `prepare_energy_data.py` builds the working panel.
- `index.qmd` and `presentation.qmd` contain the overview and Milestone 4 storyboard. With Quarto installed, run `quarto render` to build them into `_site/`. The storyboard’s conceptual diagram records the project at that milestone.
- The root-level early chart and course template files are retained for reference.
