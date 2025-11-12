# SolarDataDiscovery

Solar Data Discovery

## for test purpose

## Usage

### Notebook: Cross-Country Comparison
- Open `notebook/compare_countries.ipynb`.
- Ensure local CSVs exist:
  - `data/benin_clean.csv`
  - `data/sierra_leone_clean.csv`
  - `data/togo_clean.csv`
- Run all cells to generate:
  - Boxplots of GHI, DNI, DHI by country
  - Summary table (mean/median/std)
  - ANOVA and Kruskal–Wallis p-values
  - Bar chart of average GHI
  - Key observations

### Streamlit Dashboard
- Install requirements: `pip install -r requirements.txt`
- Run app from repo root: `streamlit run app/main.py`
- Features:
  - Country and metric selectors
  - Boxplot of selected metric by country
  - Bar chart of average GHI
  - Top regions table (if a region column exists)

Notes:
- `data/` is gitignored. Place CSVs locally before running.
