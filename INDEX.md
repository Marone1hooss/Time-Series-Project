# Project index — Day-ahead forecasting of French electricity demand

_Machine- and Copilot-readable catalog of this workspace. Generated 2026-10-21. Search this file to locate any notebook, dataset, figure, or presentation asset._

**How to use (for Copilot / search):** every figure is a PNG (not text-searchable by content), so it is cataloged below **with a text description** — search the description to find the right image, then open the `path`. A machine-readable copy is in [`figures_index.json`](figures_index.json).

## Notebooks (pipeline, run in order)

- [`notebooks/00_data_cleaning_regional.ipynb`](notebooks/00_data_cleaning_regional.ipynb) — Load+clean national & 12-region hourly data, impute DST gaps, reconcile regions->national, save processed CSVs.
- [`notebooks/01_exploration_cleaning.ipynb`](notebooks/01_exploration_cleaning.ipynb) — EDA + statistics: seasonality, ADF/KPSS, ACF/PACF, temperature link, RTE benchmark audit, naive baselines, split.
- [`notebooks/02_models_benchmarking.ipynb`](notebooks/02_models_benchmarking.ipynb) — Classical ARIMA day-ahead: normal+anomaly, recursive ARIMA(1,0,0) & lag-window ARIMA(3,0,2), vs RTE.
- [`notebooks/03_ml_forecasting.ipynb`](notebooks/03_ml_forecasting.ipynb) — Tree ML, global regional bottom-up: DT/RF/XGB/LightGBM; feature importance; local vs global; LightGBM beats RTE ~23%.
- [`notebooks/04_deep_learning_uncertainty.ipynb`](notebooks/04_deep_learning_uncertainty.ipynb) — Global PyTorch MLP + forecasts-with-uncertainty (quantile vs split-conformal intervals, coverage by hour).

## Data (processed, CSV)

- `data/processed/france_clean_hourly.csv` — national hourly load + RTE forecast + temperature + split.
- `data/processed/france_regional_clean_hourly.csv` — 12 regions, long format, 2023-2026.
- `data/processed/regional_overlap_summary.csv` — region vs national reconciliation summary.

## Presentation

- [`reports/presentation/PRESENTATION_PLAN.md`](reports/presentation/PRESENTATION_PLAN.md) — slide-by-slide plan (~28 slides), equations, feature lists, result tables, with every figure embedded.
- [`reports/presentation/images/`](reports/presentation/images/) — 28 slide-ordered figures (`s04`…`s25`).

## Key results (national day-ahead MAE)

| Approach | Model | MAE (GW) | vs RTE |
|---|---|---|---|
| Baseline | Naive-daily (D-1) | 2.61 | 2.2x worse |
| Benchmark | RTE | 1.14-1.47* | 1.0 |
| ARIMA | Recursive (1,0,0) | 2.51 | 1.8x worse |
| ARIMA | Lag-window (3,0,2) | 2.64 | 1.9x worse |
| ML | LightGBM local | 1.24 | -16% |
| **ML** | **LightGBM global** | **1.13** | **-23%** |
| DL | Deep MLP global | 1.43 | ~tie |

*_RTE's MAE depends on the test window; compare each model to RTE on its own window._

## Figure catalog — `reports/figures/` (source figures)

| Figure | Notebook | Description |
|---|---|---|
| [`00_reconciliation.png`](reports/figures/00_reconciliation.png) | 00_data_cleaning_regional | Sum of the 12 regional loads vs the national total — validates reconciliation to ~0.03%. |
| [`00_region_climate.png`](reports/figures/00_region_climate.png) | 00_data_cleaning_regional | Regions grouped/coloured by climate (temperature regime). |
| [`00_region_daily_shape.png`](reports/figures/00_region_daily_shape.png) | 00_data_cleaning_regional | Each region's average daily load shape (normalised) — compares profile shapes. |
| [`00_region_monthly_shape.png`](reports/figures/00_region_monthly_shape.png) | 00_data_cleaning_regional | Each region's monthly/seasonal load shape. |
| [`00_region_peakiness.png`](reports/figures/00_region_peakiness.png) | 00_data_cleaning_regional | Regional peakiness (peak-to-mean) comparison. |
| [`00_region_size.png`](reports/figures/00_region_size.png) | 00_data_cleaning_regional | Average load size per region (which regions are biggest). |
| [`02_overview.png`](reports/figures/02_overview.png) | 01_exploration_cleaning | National demand 2019-2026 as a daily mean — the series at a glance. |
| [`03_distribution.png`](reports/figures/03_distribution.png) | 01_exploration_cleaning | Distribution of hourly load — right-skewed with a cold-evening-peak upper tail. |
| [`04_daily_profile.png`](reports/figures/04_daily_profile.png) | 01_exploration_cleaning | Average daily load profile — morning ramp and ~19h winter evening peak. |
| [`05_weekday_weekend.png`](reports/figures/05_weekday_weekend.png) | 01_exploration_cleaning | Weekday vs weekend daily load profiles (weekends several GW lower). |
| [`06_hour_month_heatmap.png`](reports/figures/06_hour_month_heatmap.png) | 01_exploration_cleaning | Mean load by hour-of-day x month — winter-evening peak, summer-night trough. |
| [`07_stl.png`](reports/figures/07_stl.png) | 01_exploration_cleaning | STL decomposition of load into trend / seasonal / remainder. |
| [`08_acf.png`](reports/figures/08_acf.png) | 01_exploration_cleaning | ACF of the seasonal (lag-24) difference — spikes at 24/48/168 h. |
| [`08_pacf.png`](reports/figures/08_pacf.png) | 01_exploration_cleaning | PACF of the seasonal difference — cuts off after low-order/seasonal lags. |
| [`09_load_vs_temp.png`](reports/figures/09_load_vs_temp.png) | 01_exploration_cleaning | Load vs temperature V-shape (hockey stick) and the degree-day transform. |
| [`10_rte_error_breakdown.png`](reports/figures/10_rte_error_breakdown.png) | 01_exploration_cleaning | RTE forecast error by hour and temperature — worst on evening peaks / cold snaps. |
| [`11_split_timeline.png`](reports/figures/11_split_timeline.png) | 01_exploration_cleaning | Chronological train (2019-23) / validation (2024) / test (2025-26) timeline. |
| [`12_baselines.png`](reports/figures/12_baselines.png) | 01_exploration_cleaning | Naive seasonal baselines (daily/weekly/cascade) vs RTE — MAE bars. |
| [`13_forecast_vs_actual_weeks.png`](reports/figures/13_forecast_vs_actual_weeks.png) | 01_exploration_cleaning | RTE and naive-daily tracking actual load over a winter and a summer week. |
| [`14_forecast_vs_actual_scatter.png`](reports/figures/14_forecast_vs_actual_scatter.png) | 01_exploration_cleaning | Predicted vs actual scatter (RTE tight to diagonal, naive wider). |
| [`15_daily_temperature.png`](reports/figures/15_daily_temperature.png) | 01_exploration_cleaning | Daily mean temperature annual cycle with 30-day average. |
| [`16_regional_variation.png`](reports/figures/16_regional_variation.png) | 01_exploration_cleaning | Each region's daily profile indexed to its own mean — spread around the national shape. |
| [`20_normal_anomaly.png`](reports/figures/20_normal_anomaly.png) | 02_models_benchmarking | Seasonal normal profile (season x weekday x hour) and the resulting anomaly series. |
| [`21_anomaly_acf_pacf.png`](reports/figures/21_anomaly_acf_pacf.png) | 02_models_benchmarking | ACF/PACF of the anomaly used to identify ARIMA (p,q) orders. |
| [`22_grid_search.png`](reports/figures/22_grid_search.png) | 02_models_benchmarking | LEGACY single ARIMA (p,q) validation-MAE grid; superseded by 22_model_tuning_comparison.png. |
| [`22_model_tuning_comparison.png`](reports/figures/22_model_tuning_comparison.png) | 02_models_benchmarking | (p,q) validation-MAE grids for both the recursive ARIMA and the lag-window ARIMA. |
| [`23_per_horizon.png`](reports/figures/23_per_horizon.png) | 02_models_benchmarking | Test MAE by target hour: recursive ARIMA, lag-window ARIMA, raw hybrid, RTE. |
| [`24_example_days.png`](reports/figures/24_example_days.png) | 02_models_benchmarking | Day-ahead ARIMA forecasts vs actual load on example days. |
| [`25_residuals.png`](reports/figures/25_residuals.png) | 02_models_benchmarking | Chosen ARIMA residual diagnostics (residual ACF + histogram). |
| [`30_ml_benchmark.png`](reports/figures/30_ml_benchmark.png) | 03_ml_forecasting | National day-ahead MAE: bottom-up ML models (DT/RF/XGB/LightGBM) vs RTE. |
| [`31_importance.png`](reports/figures/31_importance.png) | 03_ml_forecasting | LightGBM top-15 feature importances (split count). |
| [`32_national_forecast.png`](reports/figures/32_national_forecast.png) | 03_ml_forecasting | Bottom-up LightGBM national forecast vs actual vs RTE, winter and summer weeks. |
| [`33_local_vs_global.png`](reports/figures/33_local_vs_global.png) | 03_ml_forecasting | Per-region MAE (local vs global) and the national bottom-up MAE vs RTE. |
| [`34_feature_influence_local_global.png`](reports/figures/34_feature_influence_local_global.png) | 03_ml_forecasting | Global vs mean-local gain importance, plus a region x feature local-gain heatmap. |
| [`35_region_forecasts.png`](reports/figures/35_region_forecasts.png) | 03_ml_forecasting | Per-region day-ahead forecasts (actual/global/local), winter week — 12 small multiples. |
| [`36_region_error_comparison.png`](reports/figures/36_region_error_comparison.png) | 03_ml_forecasting | Per-region error: absolute MAE (MW) and size-adjusted MAPE (%), global vs local. |
| [`37_overall_comparison.png`](reports/figures/37_overall_comparison.png) | 03_ml_forecasting | SUMMARY: every approach's national MAE relative to RTE (each on its own test window). |
| [`40_deep_benchmark.png`](reports/figures/40_deep_benchmark.png) | 04_deep_learning_uncertainty | Global PyTorch MLP vs LightGBM vs RTE — national MAE. |
| [`41_quantile_interval.png`](reports/figures/41_quantile_interval.png) | 04_deep_learning_uncertainty | 80% day-ahead prediction interval (quantile / conformal) over an example period. |
| [`42_coverage_by_hour.png`](reports/figures/42_coverage_by_hour.png) | 04_deep_learning_uncertainty | Interval coverage by hour of day — dips in the afternoon/evening peak. |
| [`43_coverage_season_temperature.png`](reports/figures/43_coverage_season_temperature.png) | ? | 80% conformal interval coverage by season and by temperature band vs the 80% target / 75% fail line — fails in winter and below 8C, over-covers in summer. |
| [`44_trust_vs_rte_season_temperature.png`](reports/figures/44_trust_vs_rte_season_temperature.png) | ? | Best model (LightGBM) vs RTE point MAE by season and temperature — we beat RTE in every season and in cool/mild/warm, but RTE wins on cold days (<8C); shows where to trust the model vs fall back to RTE. |

## Presentation images — `reports/presentation/images/` (curated, by slide)

| Slide | Image | Source figure | Description |
|---|---|---|---|
| 1,4 | [`s04_demand_overview.png`](reports/presentation/images/s04_demand_overview.png) | 02_overview.png | National demand, 2019-2026 (daily mean). |
| 5 | [`s05_regional_reconciliation.png`](reports/presentation/images/s05_regional_reconciliation.png) | 00_reconciliation.png | Regions reconcile to the national total. |
| 6 | [`s06_seasonality_heatmap.png`](reports/presentation/images/s06_seasonality_heatmap.png) | 06_hour_month_heatmap.png | Demand by hour x month. |
| 6 | [`s06b_daily_profile.png`](reports/presentation/images/s06b_daily_profile.png) | 04_daily_profile.png | Average daily load profile. |
| 7 | [`s07_acf.png`](reports/presentation/images/s07_acf.png) | 08_acf.png | Autocorrelation (ACF) with 24/168 h spikes. |
| 7 | [`s07b_stl_decomposition.png`](reports/presentation/images/s07b_stl_decomposition.png) | 07_stl.png | STL decomposition. |
| 8 | [`s08_load_vs_temperature.png`](reports/presentation/images/s08_load_vs_temperature.png) | 09_load_vs_temp.png | Load vs temperature (hockey stick). |
| 9 | [`s09_regional_variation.png`](reports/presentation/images/s09_regional_variation.png) | 16_regional_variation.png | Regional daily-profile variation. |
| 10 | [`s10_rte_error_breakdown.png`](reports/presentation/images/s10_rte_error_breakdown.png) | 10_rte_error_breakdown.png | Where RTE's error concentrates. |
| 11 | [`s11_naive_baselines.png`](reports/presentation/images/s11_naive_baselines.png) | 12_baselines.png | Naive baselines vs RTE. |
| 11 | [`s11b_forecast_vs_actual_weeks.png`](reports/presentation/images/s11b_forecast_vs_actual_weeks.png) | 13_forecast_vs_actual_weeks.png | RTE vs naive, example weeks. |
| 12 | [`s12_train_val_test_split.png`](reports/presentation/images/s12_train_val_test_split.png) | 11_split_timeline.png | Train / validation / test timeline. |
| 13 | [`s13_normal_anomaly.png`](reports/presentation/images/s13_normal_anomaly.png) | 20_normal_anomaly.png | Seasonal normal + anomaly. |
| 14 | [`s14_anomaly_acf_pacf.png`](reports/presentation/images/s14_anomaly_acf_pacf.png) | 21_anomaly_acf_pacf.png | Anomaly ACF / PACF (order ID). |
| 14 | [`s14b_arima_pq_tuning.png`](reports/presentation/images/s14b_arima_pq_tuning.png) | 22_model_tuning_comparison.png | ARIMA (p,q) validation grids. |
| 15 | [`s15_arima_mae_by_hour.png`](reports/presentation/images/s15_arima_mae_by_hour.png) | 23_per_horizon.png | ARIMA MAE by target hour. |
| 15 | [`s15b_arima_example_days.png`](reports/presentation/images/s15b_arima_example_days.png) | 24_example_days.png | ARIMA forecasts vs actual. |
| 18 | [`s18_ml_national_benchmark.png`](reports/presentation/images/s18_ml_national_benchmark.png) | 30_ml_benchmark.png | National MAE: ML models vs RTE. |
| 18 | [`s18b_ml_national_forecast.png`](reports/presentation/images/s18b_ml_national_forecast.png) | 32_national_forecast.png | LightGBM national forecast, example weeks. |
| 19 | [`s19_ml_feature_importance.png`](reports/presentation/images/s19_ml_feature_importance.png) | 31_importance.png | LightGBM feature importance. |
| 20 | [`s20_local_vs_global.png`](reports/presentation/images/s20_local_vs_global.png) | 33_local_vs_global.png | Local vs global: per-region & national MAE. |
| 20 | [`s20b_feature_influence_local_global.png`](reports/presentation/images/s20b_feature_influence_local_global.png) | 34_feature_influence_local_global.png | Feature influence: global vs local. |
| 21 | [`s21_region_forecasts.png`](reports/presentation/images/s21_region_forecasts.png) | 35_region_forecasts.png | Per-region forecasts, winter week. |
| 21 | [`s21b_region_error_comparison.png`](reports/presentation/images/s21b_region_error_comparison.png) | 36_region_error_comparison.png | Per-region error: MAE vs MAPE. |
| 22 | [`s22_deep_benchmark.png`](reports/presentation/images/s22_deep_benchmark.png) | 40_deep_benchmark.png | Deep MLP vs trees vs RTE. |
| 23 | [`s23_uncertainty_interval.png`](reports/presentation/images/s23_uncertainty_interval.png) | 41_quantile_interval.png | 80% prediction interval. |
| 24 | [`s24_coverage_by_hour.png`](reports/presentation/images/s24_coverage_by_hour.png) | 42_coverage_by_hour.png | Interval coverage by hour. |
| 24 | [`s24b_coverage_season_temperature.png`](reports/presentation/images/s24b_coverage_season_temperature.png) | 43_coverage_season_temperature.png | 80% interval coverage by season & temperature — where it fails. |
| 25 | [`s25_overall_comparison.png`](reports/presentation/images/s25_overall_comparison.png) | 37_overall_comparison.png | Every approach vs RTE. |
| 26 | [`s25b_trust_vs_rte_season_temperature.png`](reports/presentation/images/s25b_trust_vs_rte_season_temperature.png) | 44_trust_vs_rte_season_temperature.png | Where to trust the best model vs RTE — by season & temperature. |
