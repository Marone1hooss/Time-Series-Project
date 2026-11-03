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
│   └── processed/                      # cleaned CSVs, written by notebook 00
├── notebooks/
│   ├── 00_data_cleaning_regional.ipynb # load + clean national & regional, reconcile, save  ✅ done
│   ├── 01_exploration_cleaning.ipynb   # EDA + statistical validation + RTE audit          ✅ done
│   ├── 02_models_benchmarking.ipynb    # AR/MA/ARIMA day-ahead, (p,q) grid, recursive vs real-data  ✅ done
│   ├── 03_ml_forecasting.ipynb         # DT/RF/XGB/LGBM, global regional bottom-up vs RTE           ✅ done
│   └── 04_deep_learning_uncertainty.ipynb # PyTorch deep net + quantile/conformal intervals (TP05)  ✅ done
├── reports/figures/                    # exported charts for the slides
├── requirements.txt
└── README.md
```

## How to run
```bash
pip install -r requirements.txt
# run in order — notebook 00 writes the cleaned data that 01 consumes
python -m nbconvert --to notebook --execute --inplace notebooks/00_data_cleaning_regional.ipynb
python -m nbconvert --to notebook --execute --inplace notebooks/01_exploration_cleaning.ipynb
# or open them in Jupyter / VS Code and run all cells
```

## Notebook 00 — data layer (key findings)
- **Data quality is excellent** in both files: continuous hourly grids, no duplicates; **7** missing values
  (national) + **36** (regional) — all at the autumn DST change — imputed by interpolation.
- The **12 regions reconcile to the national total** to within **~16 MW (0.03%)** → bottom-up forecasting is valid.
- **National mean recomputed on the common 2023–2026 window** = ~50.5 GW (vs ~51.5 GW over full 2019–2026).
- Clear north-cold / south-warm climate gradient; Île-de-France is notably peakier than France.
- Saves `france_clean_hourly.csv`, `france_regional_clean_hourly.csv`, `regional_overlap_summary.csv`.

## Notebook 04 — Deep learning + uncertainty (TP05)
- **Global deep forecaster** (PyTorch MLP over the 12 regions, bottom-up): national MAE ~1.46 GW — **ties RTE** but
  does **not** beat LightGBM (1.13 GW) on tabular day-ahead features (trees win here).
- **Uncertainty (Q2):** 80% day-ahead intervals two ways — **quantile** (LightGBM pinball) **under-covers (68%)**,
  **split conformal** is **well-calibrated (78%≈80%)**; compared by coverage/width/**Winkler**.
- **Coverage by hour** dips in the **afternoon/evening peak** → *when the forecast is least reliable*.
- **Deploy recommendation (Q3):** LightGBM point forecast + **conformal** interval for reserve sizing; retrain
  regularly; keep RTE as fallback; alert when live error leaves the band.

## Notebook 03 — ML forecasting (key findings)  ⭐ beats RTE
- **Global regional model** (12 regions stacked, region as a feature) predicting each region's demand, summed
  **bottom-up** to a national forecast. Honest day-ahead features: safe lags (≥48h) + hybrid-24/48, 7-day level,
  **noised** tomorrow-temperature + degree-days, calendar incl. **holiday** and **season**.
- Benchmark on 2025–2026 (national MAE): **LightGBM 1.13 GW** ≈ XGBoost 1.15 < **RTE 1.47** < Random Forest 1.59
  < Decision Tree 1.67. **LightGBM beats RTE by ~23%** (Wilcoxon p≈6e-26) — first affirmative answer to Q1.
- Top features: 7-day demand level, recent/safe lags, calendar, weather (temp + degree-days).
- **Honesty caveat:** the edge partly rests on an idealised i.i.d. noised weather input; a realistic correlated
  forecast error would shrink it (stress-tested in NB4).

## Notebook 02 — AR/MA/ARIMA day-ahead (key findings)
- **Day-ahead protocol:** decision at noon on D, forecast all 24h of D+1; verified the **hybrid 24/48 lag** (first
  12h → lag-24, last 12h → lag-48) uses only observed data at the cutoff.
- **Deseasonalize** to a *normal* (weekday×hour) + *anomaly*; fit ARIMA on the stationary anomaly (tractable).
- **(p,q) grid by validation MAE → ARIMA(1,0,0).** Pure-MA (p=0) is catastrophic (~21 GW, reverts to the mean) —
  a clean demonstration that MA alone is useless day-ahead; one AR term fixes it.
- **Recursive ARIMA beats the real-data 24/48-lag** (MAE 2.44 vs 3.63 GW, Wilcoxon p<0.001); both trail RTE (1.37 GW).
- Residual Ljung-Box still significant at 24/168h → a **seasonal (SARIMA)** term and **weather** are the next gains.

## Notebook 01 — analysis (key findings)
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
