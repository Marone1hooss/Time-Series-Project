# Day-Ahead Forecasting of French Electricity Demand

A day-ahead forecasting system for **hourly French national electricity demand**, built, evaluated honestly,
and turned into a recommendation a head of trading can act on.

**Business setting.** Our utility buys energy on the day-ahead market. Every day **D**, before the auction closes
at **12:00 CET**, the trading desk must forecast the demand of every hour of day **D+1**. Each MWh of error is
settled later at imbalance prices, and the **evening peaks of cold days** are where errors cost the most.

### The three questions this project answers
1. **Can we beat RTE's public day-ahead forecast, and by how much — honestly measured?**
2. **How uncertain is the forecast, and when does it fail?**
3. **What should we deploy, and what are the risks?**

## Data
`data/france_electricity_hourly.csv` — hourly, UTC, **2019-01 → 2026-06** (65,712 rows):

| column | meaning |
|---|---|
| `datetime_utc` | hour timestamp (UTC — no DST ambiguity) |
| `load_mw` | actual French national consumption — **the target** |
| `rte_forecast_d1_mw` | RTE public day-ahead forecast — **the benchmark to beat** |
| `temperature_c` | population-weighted temperature — main weather driver |

`data/france_regional_electricity_hourly.csv.gz` — same data split by region (bonus: hierarchical modelling).

## Repository structure
```
├── data/
│   ├── france_electricity_hourly.csv
│   ├── france_regional_electricity_hourly.csv.gz
│   └── processed/                      # cleaned Parquet, written by notebook 01
├── notebooks/
│   ├── 01_exploration_cleaning.ipynb   # EDA, cleaning, statistical validation   ✅ done
│   ├── 02_models_benchmarking.ipynb    # feature engineering + model ladder vs RTE  (next)
│   └── 03_forecasting_validation.ipynb # walk-forward, uncertainty, deployment      (next)
├── reports/figures/                    # exported charts for the slides
├── requirements.txt
└── README.md
```

## How to run
```bash
pip install -r requirements.txt
python -m nbconvert --to notebook --execute --inplace notebooks/01_exploration_cleaning.ipynb
# or open it in Jupyter / VS Code and run all cells
```

## Notebook 01 — key findings
- **Data quality is excellent**: continuous hourly grid, no duplicates; only **7 missing values (0.011%)**, all on
  the autumn DST change — imputed by time interpolation.
- **Rich, learnable structure**: strong daily (24h) + weekly (168h) seasonality and a winter annual peak
  (Ljung-Box p ≈ 0 at all three); ADF + KPSS justify **seasonal differencing** → SARIMA.
- **Temperature is the dominant driver** through a non-linear V-shape: raw Pearson r = −0.60, but a
  **heating-degree transform lifts it to +0.72** (France is heating-dominated).
- **The benchmark is strong but beatable where it counts**: RTE scores **MAE ≈ 1.14 GW, RMSE ≈ 1.49 GW,
  MAPE ≈ 2.25%**, with a small but **statistically significant under-forecast bias (+0.67 GW, t-test p ≈ 0)** and
  **autocorrelated residuals** — errors concentrate in cold conditions and evening peaks.
- A fixed chronological split (**train 2019–2023 / val 2024 / test 2025–2026**) is saved for honest evaluation.

## Honesty principle
Every feature must be knowable at **12:00 CET on day D**. The split and RTE audit are designed around this so the
modelling notebooks inherit a fair benchmark comparison.
