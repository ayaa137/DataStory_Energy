# Renewable Energy Transition Across Countries

**Team:** Aya Abdine, Meriam El Askri, Mcolisi Austine, Ghofran Mahmoud

**Keyword:** Green Energy

**Course:** Visual Communication and Data Storytelling

**Status:** Milestones 0–4 completed; repository prepared for individual review. The final report and 3D visualization are future work.

We compare renewable adoption, electricity-source mixes, economic context, and changes since 2000 across **Germany, Denmark, Norway, France, China, United States, India, Brazil, Japan, and South Africa**.

The target audience is general, non-expert readers interested in sustainability and global development. Our central insight is that there is no single path to renewable energy: national shares, source mixes, economic contexts, and trajectories differ.

## Data and coverage

Source: [Our World in Data Energy Dataset](https://github.com/owid/energy-data), using the [requested CSV](https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv) and its saved snapshot.

The working dataset has 260 country-year rows for 2000–2025. Primary-energy renewable shares end in 2024; GDP ends in 2022. Missing observations are preserved. The requested GitHub dataset is now a legacy release and is no longer updated. See [ENERGY_DATA_NOTES.md](ENERGY_DATA_NOTES.md) for definitions, coverage, and provenance.

## Repository structure

```text
data/
  energy_10countries_clean.csv
  energy_data_quality_summary.csv
  energy_source/                 # Raw CSV, codebook, checksum manifest
notebooks/
  01_data_preparation.ipynb
  02_main_insights.ipynb
  03_visual_drafts.ipynb          # Four visuals; preserves existing final PNGs
visuals/
  01_renewable_adoption_2024.png
  02_renewable_electricity_pathways_2024.png
  03_gdp_vs_renewables.png
  04_transition_over_time.png
index.qmd                        # Short project overview, not the final report
presentation.qmd                 # Milestone 4 presentation/storyboard
presentation.css
prepare_energy_data.py
requirements.txt
_quarto.yml
```

## Reproduce and review

Use Python 3.11+ and Quarto (validated with Python 3.13 and Quarto 1.9.37). Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the notebooks in order with a Python 3 kernel. The preparation notebook calls the existing preparation script in **offline** mode, verifying the saved snapshot rather than downloading revised data. Alternatively:

```powershell
python prepare_energy_data.py --offline
jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_preparation.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_main_insights.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_visual_drafts.ipynb
quarto render
```

Open `_site/index.html` and `_site/presentation.html`. The active website build renders only the project overview and presentation. Figure cells display their charts but preserve already-existing final PNG files.

If Windows blocks Quarto's default cache location, use a process-local cache inside the repository:

```powershell
$env:LOCALAPPDATA = Join-Path (Get-Location) '.quarto/runtime'
quarto render
```

## Retained material and limitations

Course template R scripts, example QMD pages, bibliography, extension, and unrelated template data are retained. They are not part of the active Python analysis or website build. The earlier root-level chart script and PNG are retained as prior work; the four reviewed visuals are in `visuals/`.

The pitch's global map is not present, so the presentation opens with text. Adding the original map still requires its source asset. The 3D slide is a conceptual diagram only.
