"""Build the Time-Series presentation.
Place this script in reports/presentation/ (next to the images/ folder) and run:
    pip install python-pptx pillow
    python build_presentation.py
Output: Time_Series_Presentation.pptx
Missing images are replaced by a grey placeholder showing the file name.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
OUT = os.path.join(HERE, "Time_Series_Presentation.pptx")

DARK = RGBColor(0x22, 0x22, 0x22)
GREY = RGBColor(0x66, 0x66, 0x66)
FONT = "Calibri"

SLIDES = [
    dict(title="The problem", bullets=[
        "Every day D, before the 12:00 market auction, we must state the demand for all 24 hours of day D+1",
        "Electricity is bought in advance: every MWh wrong is settled later at imbalance (penalty) prices",
        "Errors hurt most on cold winter evenings, when demand and prices peak",
        "Task: forecast tomorrow's 24 hourly demands using only what is known by noon today"]),
    dict(title="Objective & the 3 questions", bullets=[
        "Objective: an honest day-ahead forecaster, benchmarked against RTE's public forecast",
        "Q1 – Can we beat RTE, honestly measured?",
        "Q2 – How uncertain is the forecast, and when does it fail?",
        "Q3 – What should we deploy, and what are the risks?",
        "Rule: no data from after the noon cutoff is ever used (no leakage)"]),
    dict(title="The data", bullets=[
        "National: 65,712 hourly rows, 2019-01 → 2026-06 (UTC)",
        "Columns: load_mw (target), rte_forecast_d1_mw (benchmark), temperature_c, calendar",
        "Regional: 12 regions, hourly, 2023–2026 (367,752 rows), used for bottom-up models"],
        images=["s04_demand_overview.png"]),
    dict(title="Data preparation", bullets=[
        "National: only 7 missing values (0.011%), all at the autumn DST change, interpolated",
        "Regional: 36 gaps imputed",
        "Regions reconcile to the national total within ~16 MW (0.03%)"],
        images=["s05_regional_reconciliation.png"]),
    dict(title="Demand has strong, learnable structure", bullets=[
        "Three nested cycles: daily (24 h), weekly (168 h), yearly",
        "Peaks: winter evenings ~19:00; troughs: summer nights",
        "Weekends several GW below weekdays"],
        images=["s06_seasonality_heatmap.png"]),
    dict(title="Statistical backing", bullets=[
        "Ljung-Box p ≈ 0 at lags 1, 24, 168: strong hourly/daily/weekly memory",
        "Raw series non-stationary (KPSS rejects)",
        "Stationary after seasonal (lag-24) differencing → justifies (S)ARIMA"],
        images=["s07_acf.png"]),
    dict(title="Temperature: the dominant driver", bullets=[
        "Non-linear 'hockey stick': heating below ~15 °C, light cooling above ~20 °C",
        "Raw r = −0.60; heating-degree-day transform → r = +0.72",
        "France is heating-dominated (cooling r ≈ −0.12)"],
        images=["s08_load_vs_temperature.png"]),
    dict(title="Regions differ", bullets=[
        "Same rhythm, but some regions have steeper evening peaks / deeper night troughs",
        "A per-region bottom-up model can exploit this (used in ML/DL)"],
        images=["s09_regional_variation.png"]),
    dict(title="The benchmark to beat: RTE", bullets=[
        "MAE ≈ 1.14 GW · RMSE ≈ 1.49 GW · MAPE ≈ 2.25%",
        "Under-forecast bias +0.67 GW (t-test p ≈ 0); residuals autocorrelated at 24/168 h",
        "Fails most on evening peaks and temperature extremes"],
        images=["s10_rte_error_breakdown.png"]),
    dict(title="The floor: naive baselines",
        table=[["Forecast", "MAE (GW)", "MAPE", "× vs RTE"],
               ["RTE", "1.19", "2.4%", "1.0"],
               ["Naive-daily (lag 24)", "2.61", "5.2%", "2.2× worse"],
               ["Naive-weekly (lag 168)", "3.52", "6.5%", "3.0× worse"],
               ["Seasonal-cascade (1y→1w→1d)", "4.13", "7.8%", "3.5× worse"]],
        bullets=["RTE is 2–3.5× better than any naive rule"],
        images=["s11_naive_baselines.png"]),
    dict(title="Evaluation protocol", bullets=[
        "Chronological split: train 2019–2023 · validation 2024 · test 2025 – 2026-06",
        "Decision at 12:00 on day D, forecast all of D+1 with pre-cutoff information only"],
        images=["s12_train_val_test_split.png"]),
    dict(title="ARIMA: normal + anomaly", bullets=[
        "Seasonal ARIMA on 65k points is intractable",
        "Load = seasonal normal (season × weekday × hour) + anomaly",
        "ARIMA on the anomaly, then load = normal + forecast anomaly"],
        images=["s13_normal_anomaly.png"]),
    dict(title="Two ARIMA forecasts & order selection", bullets=[
        "Recursive: rolls its own predictions across the day",
        "Lag-window: one ARIMA per hour, lag 24 (00–11 h) / lag 48 (12–23 h)",
        "(p,q) grid on validation MAE: recursive ARIMA(1,0,0), lag-window ARIMA(3,0,2)"],
        images=["s14_anomaly_acf_pacf.png", "s14b_arima_pq_tuning.png"]),
    dict(title="ARIMA results vs RTE (56-day test)",
        table=[["Model", "MAE (GW)", "RMSE (GW)", "MAPE"],
               ["Recursive ARIMA(1,0,0)", "2.51", "3.58", "4.0%"],
               ["Lag-window ARIMA(3,0,2)", "2.64", "3.77", "4.2%"],
               ["Raw-lag hybrid (no fit)", "3.63", "4.74", "5.7%"],
               ["RTE", "1.37", "1.71", "2.1%"]],
        bullets=["ARIMAs tie (p = 0.64), beat raw lag (p = 1e-4), still trail RTE: no weather"],
        images=["s15_arima_mae_by_hour.png", "s15b_arima_example_days.png"]),
    dict(title="Feature engineering (34 features)", bullets=[
        "Demand history (≥ 48 h): lag_48 … lag_336, 7-day level roll7, recent (hybrid 24/48)",
        "Weather: noised temperature forecast, HDD = max(16−T,0), CDD = max(T−20,0), temp_lag48",
        "Calendar: hour, weekday, month, weekend, holiday, season",
        "Identity: 12 region one-hots",
        "All features knowable at the noon cutoff"]),
    dict(title="Design: global regional, bottom-up", bullets=[
        "One model trained on all 12 regions stacked (region as a feature)",
        "Predict each region, then sum the 12 → national forecast",
        "Four tree models (Decision Tree, Random Forest, XGBoost, LightGBM) vs RTE on 2025–2026"]),
    dict(title="ML results: first model to beat RTE",
        table=[["Model", "MAE (GW)", "MAPE", "vs RTE"],
               ["LightGBM", "1.13", "2.1%", "−23%"],
               ["XGBoost", "1.15", "2.2%", "−22%"],
               ["RTE", "1.47", "2.9%", "—"],
               ["Random Forest", "1.59", "3.0%", "+8%"],
               ["Decision Tree", "1.67", "3.2%", "+14%"]],
        bullets=["LightGBM −23% vs RTE (Wilcoxon p ≈ 6e-26)",
                 "Caveat: relies on an idealised noised-weather input"],
        images=["s18_ml_national_benchmark.png", "s18b_ml_national_forecast.png"]),
    dict(title="Feature influence", bullets=[
        "By gain: recent 76% + lag_168 18% → demand history ≈ 97%",
        "Essentially a smart persistence model; weather, calendar and region fine-tune it"],
        images=["s19_ml_feature_importance.png"]),
    dict(title="Local vs global models", bullets=[
        "Global wins in all 12 regions",
        "National MAE 1.13 vs 1.24 GW (p = 3e-9); both beat RTE",
        "Pooling gives ~12× more data than 2 years per region"],
        images=["s20_local_vs_global.png", "s20b_feature_influence_local_global.png"]),
    dict(title="Per-region forecasts & errors", bullets=[
        "MAE tracks region size (Île-de-France largest)",
        "MAPE: best PACA / Hauts-de-France (~2.7%), worst Centre-Val de Loire (4.9%)"],
        images=["s21_region_forecasts.png", "s21b_region_error_comparison.png"]),
    dict(title="Global deep forecaster (PyTorch MLP)",
        table=[["Model", "MAE (GW)", "MAPE"],
               ["LightGBM", "1.12", "2.1%"],
               ["Deep MLP", "1.43", "2.8%"],
               ["RTE", "1.47", "2.9%"]],
        bullets=["12 regions, 76 features, bottom-up",
                 "Ties RTE, does not beat the trees"],
        images=["s22_deep_benchmark.png"]),
    dict(title="Forecasts with uncertainty (80% interval)",
        table=[["Method", "Coverage", "Width", "Winkler"],
               ["Quantile (LightGBM)", "69%", "3.31 GW", "5,953"],
               ["Split conformal", "78%", "3.98 GW", "6,645"]],
        bullets=["Quantile: sharper but over-confident",
                 "Conformal: well-calibrated"],
        images=["s23_uncertainty_interval.png"]),
    dict(title="When does it fail?", bullets=[
        "Coverage dips in the afternoon/evening peak",
        "For reserve sizing, calibration beats sharpness → conformal interval"],
        images=["s24_coverage_by_hour.png"]),
    dict(title="Where the 80% interval fails: season & temperature", bullets=[
        "80% interval = actual demand lands inside it ~80% of the time (a coverage promise, not point confidence)",
        "Overall 78%, but a fixed ±1.99 GW band cannot adapt to conditions",
        "FAILS in winter (62%) and below 8 °C (57–61%): over-confident on cold peaks",
        "Over-covers in summer (94%); fix = conditional per-season radius"],
        images=["s24b_coverage_season_temperature.png"]),
    dict(title="Every approach vs RTE", bullets=[
        "MAE ÷ RTE MAE on each model's own test window (< 1 beats RTE)",
        "Naive ~2.2× → ARIMA ~1.8–1.9× → Deep MLP ~0.98× → LightGBM 0.77×"],
        images=["s25_overall_comparison.png"]),
    dict(title="Where can we trust the model vs RTE?", bullets=[
        "Best model (LightGBM) MAE vs RTE, split by season and temperature",
        "Beats RTE in every season (+28–40%), and in cool / mild / warm conditions",
        "RTE still WINS on cold days: −8% at 2–8 °C, −26% below 2 °C (freezing)",
        "Deploy rule: trust our model by default, fall back to RTE below ~8 °C"],
        images=["s25b_trust_vs_rte_season_temperature.png"]),
    dict(title="Answers to the three questions", bullets=[
        "Q1 – Beat RTE? Yes: LightGBM bottom-up, −23% MAE (p ≈ 6e-26), under the noised-weather assumption",
        "Q2 – Uncertainty? Conformal 80% interval, 78% coverage; reliability dips on evening peaks",
        "Q3 – Deploy? LightGBM point forecast + conformal interval, frequent retraining, RTE as fallback"]),
    dict(title="Risks", bullets=[
        "The ~23% edge partly rests on an idealised independent noised-weather input",
        "Realistic correlated weather errors would shrink it, mostly on extremes",
        "Single chronological holdout (no walk-forward yet)",
        "Regional training limited to 2023–2024"]),
    dict(title="Conclusion & next steps",
        table=[["Model (national day-ahead)", "MAE (GW)", "vs RTE"],
               ["LightGBM — bottom-up (deploy)", "1.13", "−23% ✓"],
               ["Deep MLP (global)", "1.43", "~tie"],
               ["RTE benchmark", "1.47", "—"],
               ["ARIMA (recursive)", "2.51", "~1.8× worse"],
               ["Naive-daily (D-1)", "2.61", "~2.2× worse"]],
        bullets=[
        "Only the ML/DL models reach or beat RTE; LightGBM wins by −23% (p ≈ 6e-26)",
        "Delivered: clean data → statistics → ARIMA → ML (beats RTE) → DL + calibrated uncertainty",
        "Next: walk-forward validation, weather stress-test, SARIMAX, hierarchical reconciliation"]),
]

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height
M = Inches(0.5)


def text(slide, x, y, w, h, lines, size, bold=False, color=DARK, bullet=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ("•  " + line) if bullet else line
        p.space_after = Pt(10)
        for r in p.runs:
            r.font.size, r.font.bold, r.font.name = Pt(size), bold, FONT
            r.font.color.rgb = color
    return tb


def image(slide, name, x, y, w, h):
    path = os.path.join(IMG, name)
    if os.path.exists(path):
        from PIL import Image
        iw, ih = Image.open(path).size
        s = min(w / iw, h / ih)
        pw, ph = int(iw * s), int(ih * s)
        slide.shapes.add_picture(path, x + (w - pw) // 2, y + (h - ph) // 2, pw, ph)
    else:
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0xEE, 0xEE, 0xEE)
        box.line.color.rgb = RGBColor(0xBB, 0xBB, 0xBB)
        box.text_frame.text = "images/" + name
        r = box.text_frame.paragraphs[0].runs[0]
        r.font.size, r.font.color.rgb, r.font.name = Pt(14), GREY, FONT


def table(slide, rows, x, y, w):
    rh = Inches(0.42)
    t = slide.shapes.add_table(len(rows), len(rows[0]), x, y, w, rh * len(rows)).table
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j)
            c.text = v
            r = c.text_frame.paragraphs[0].runs[0]
            r.font.size, r.font.name, r.font.bold = Pt(12), FONT, i == 0
    return rh * len(rows)


# Title slide
s = prs.slides.add_slide(BLANK)
text(s, M, Inches(0.7), W - 2 * M, Inches(1.4),
     ["Day-ahead forecasting of French electricity demand"], 36, bold=True)
text(s, M, Inches(1.8), W - 2 * M, Inches(0.6),
     ["Can we beat the national grid's own forecast?"], 22, color=GREY)
text(s, M, Inches(2.5), W - 2 * M, Inches(0.5),
     ["Marouane Housni · Mastère Data & AI for Finance · Time Series"], 16, color=GREY)
image(s, "s04_demand_overview.png", M, Inches(3.2), W - 2 * M, Inches(3.9))

for d in SLIDES:
    s = prs.slides.add_slide(BLANK)
    text(s, M, Inches(0.35), W - 2 * M, Inches(0.8), [d["title"]], 30, bold=True)
    top = Inches(1.3)
    imgs = d.get("images", [])
    if not imgs:
        y = top
        if "table" in d:
            y += table(s, d["table"], M, y, Inches(8)) + Inches(0.3)
        text(s, M, y, W - 2 * M, H - y - M, d["bullets"], 20, bullet=True)
        continue
    # left column: table + bullets ; right column: image(s)
    lw = Inches(6.3) if "table" in d else Inches(5.2)
    y = top
    if "table" in d:
        y += table(s, d["table"], M, y, lw) + Inches(0.3)
    text(s, M, y, lw, H - y - M, d["bullets"], 16, bullet=True)
    rx, rw = M + lw + Inches(0.4), W - M - (M + lw + Inches(0.4))
    avail = H - top - M
    n = len(imgs)
    gap = Inches(0.2)
    ih = (avail - gap * (n - 1)) / n
    for k, name in enumerate(imgs):
        image(s, name, rx, int(top + k * (ih + gap)), rw, int(ih))

prs.save(OUT)
print("Saved", OUT)
