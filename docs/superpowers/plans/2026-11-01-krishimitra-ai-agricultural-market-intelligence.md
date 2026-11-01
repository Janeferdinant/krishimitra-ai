# KrishiMitra AI: Agricultural Market Intelligence & Crop Price Forecasting System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, scientifically evaluate, and deploy a production-grade, peer-reviewed-standard Agricultural Market Intelligence & Crop Price Forecasting platform (KrishiMitra AI) for Kerala Young Innovators Programme (YIP 9.0) complete with reproducible datasets, ML/hybrid models, explainable AI, decision support, IEEE paper, and 20-slide presentation.

**Architecture:** A modular Python 3.14 backend architecture separating data acquisition/preprocessing, time-series feature engineering, multi-paradigm model evaluation (statistical baseline, ARIMA/SARIMA, XGBoost, LightGBM, neural net, and hybrid ARIMA+XGBoost), SHAP explainability, and agro-economic decision support engines (crop planning, best market recommendation, price alerts). Exposed through a high-performance FastAPI REST API layer and delivered via an interactive, responsive, farmer-accessible glassmorphic web dashboard with Plotly visualisations and bilingual Kerala context.

**Tech Stack:** Python 3.14, FastAPI, Uvicorn, Pydantic v2, Pandas, NumPy, Scipy, Statsmodels, Scikit-learn, XGBoost, LightGBM, SHAP, Matplotlib, Seaborn, Plotly, Python-pptx, Pytest, HTML5/CSS3/Vanilla ES6 modern responsive frontend with Tailwind utility styling.

**Spec:** Prompt requirements for YIP 9.0 Agricultural Market Intelligence & Crop Price Forecasting System covering 17 execution instructions, 10 scientific experiments, 7 deliverables, and authentic Kerala & National agricultural datasets.

## Global Constraints

- Authentic data only: No fabricated historical price, arrival, or weather observations. Use AGMARKNET, Open Data India, IMD/NASA POWER meteorological parameters, and verified Kerala commodity market records (Arecanut, Garbled Black Pepper, Coconut/Copra, Banana/Nendran, Rubber, Cardamom).
- Zero data leakage: Chronological time-series splitting (train/val/test) and rolling-window walk-forward validation; never use future information or random shuffling.
- Model diversity: Evaluate baseline naive, seasonal naive, ARIMA/SARIMA, Random Forest, XGBoost, LightGBM, Neural Multilayer/Sequence architecture, and Hybrid (ARIMA + XGBoost residual modeling).
- Actionable decision support: Crop planning and market recommendation must consider price trends, transport costs, arrival volume elasticity, and seasonality without promising speculative guaranteed returns.
- Full deliverable completeness: All 7 deliverables (source code, clean dataset repository, EDA report, model evaluation report, IEEE format research paper, 20-slide PowerPoint & HTML presentation, and interactive live demonstration app) must be fully authored and validated.

## Review Focus

1. Zero or negative price inputs and missing mandi arrival days: Must be handled via seasonal and calendar-aware forward imputation without future-window lookahead.
2. Market extreme volatility and festival/monsoon spikes: Must be preserved as real structural signals rather than blindly trimmed by statistical outlier detectors (IQR/Z-score).
3. Sparse mandi trading records across secondary Kerala markets: Fallback gracefully to district or state-level modal price aggregates with clear data quality confidence indicators.
4. Multicollinear lag and rolling statistics features: Regularized feature selection (Mutual Information, RF feature importance, permutation testing) to prevent overfitting.
5. Inaccessible external network APIs: Resilient local caching and reproducible offline dataset fixtures ensuring 100% test pass rate and offline reproducibility.

---

### Task 1: Literature Review Matrix & Problem Canvas Formulation

**Files:**
- Create: `docs/literature_review/literature_review_matrix.md`
- Create: `docs/literature_review/research_gap_analysis.md`
- Test: `tests/test_literature_review.py`

**Interfaces:**
- Consumes: Verified papers from IEEE, Elsevier (Procedia CS), Springer, Scopus Q1/Q2 agricultural journals, and canvas sources (UAS Bangalore, TNAU RKVY, Procedia CS Sabu & Manoj Kumar 2020, JSRR Pepper 3404).
- Produces: Structured 32-paper literature matrix with DOI, methodology, performance metrics, and identified research gaps.

- [ ] **Step 1: Write the test to verify literature review completeness and authentic DOI indexing**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Compile comprehensive 32-paper literature review matrix and research gap synthesis in `docs/literature_review/`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit literature review assets**

---

### Task 2: Data Acquisition & Preprocessing Pipeline

**Files:**
- Create: `src/data_pipeline/acquisition.py`
- Create: `src/data_pipeline/preprocessing.py`
- Create: `data/raw/sources_register.json`
- Create: `data/processed/data_dictionary.json`
- Test: `tests/test_data_pipeline.py`

**Interfaces:**
- Consumes: AGMARKNET historical mandi price feeds, IMD/NASA POWER meteorological parameters for major Kerala agro-climatic zones (Palakkad, Wayanad, Idukki, Kozhikode, Thrissur, Kottayam).
- Produces: `CleanedAgriculturalDataset` pandas DataFrame with schema `[date, state, district, market, commodity, variety, arrivals_tonnes, min_price, max_price, modal_price, temp_mean, temp_max, temp_min, rainfall_mm, rel_humidity_pct]`.

- [ ] **Step 1: Write test for data validation, missing value imputation, and outlier detection**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement `acquisition.py` and `preprocessing.py` with seasonal imputation, IQR vs genuine spike classification, and unit normalization**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Generate cleaned analytical dataset in `data/processed/cleaned_agricultural_market_dataset.csv`**
- [ ] **Step 6: Commit preprocessing pipeline**

---

### Task 3: Exploratory Data Analysis & Statistical Diagnostics

**Files:**
- Create: `src/data_pipeline/eda_engine.py`
- Create: `docs/reports/eda_report.md`
- Test: `tests/test_eda.py`

**Interfaces:**
- Consumes: Cleaned agricultural and meteorological dataset.
- Produces: ADF stationarity test statistics, ACF/PACF autocorrelation diagnostics, seasonal-trend decomposition (STL), price-arrival price elasticity metrics, and figure artifacts in `artifacts/figures/`.

- [ ] **Step 1: Write test verifying ADF stationarity tests, seasonal decomposition, and distribution statistics**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement `eda_engine.py` generating statistical metrics and Matplotlib/Plotly figures**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Compile comprehensive `docs/reports/eda_report.md` with research interpretations**
- [ ] **Step 6: Commit EDA deliverables**

---

### Task 4: Time-Series Feature Engineering & Feature Selection

**Files:**
- Create: `src/data_pipeline/feature_engineering.py`
- Create: `data/processed/analytical_features_dataset.csv`
- Test: `tests/test_feature_engineering.py`

**Interfaces:**
- Consumes: Cleaned daily/weekly price and weather time-series.
- Produces: Feature matrix with calendar features (month, season, harvest season, festival flag), lag prices (t-1, t-7, t-14, t-30, t-60), rolling window statistics (mean, std, min, max, EMA 7/14/30), arrival momentum, weather anomalies, and feature importance rankings (Mutual Info, RF, XGBoost).

- [ ] **Step 1: Write test verifying lag generation, rolling statistics, zero-leakage alignment, and feature selection scoring**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement `feature_engineering.py` with leak-free chronological shift and feature selection selectors**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Export analytical features dataset and feature importance ranking**
- [ ] **Step 6: Commit feature engineering module**

---

### Task 5: Model Development (Statistical, Machine Learning, Deep Learning & Hybrid)

**Files:**
- Create: `src/models/baselines.py`
- Create: `src/models/statistical_models.py`
- Create: `src/models/ml_models.py`
- Create: `src/models/deep_learning_models.py`
- Create: `src/models/hybrid_models.py`
- Create: `src/models/validation.py`
- Create: `src/models/explainability.py`
- Test: `tests/test_models.py`

**Interfaces:**
- Consumes: Analytical feature matrix.
- Produces: Trained model estimators, walk-forward validation results (MAE, RMSE, MAPE, sMAPE, WAPE, R² across 7, 15, 30, and 60-day horizons), SHAP explainer values, and serialized model artifacts in `artifacts/trained_models/`.

- [ ] **Step 1: Write test verifying walk-forward chronological evaluation, forecasting interfaces, and evaluation metrics calculations**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement baseline models (Naive, Seasonal Naive, Moving Average)**
- [ ] **Step 4: Implement ARIMA / SARIMA in `statistical_models.py`**
- [ ] **Step 5: Implement Random Forest, XGBoost, and LightGBM in `ml_models.py`**
- [ ] **Step 6: Implement Neural Sequence / MLP forecasting architecture in `deep_learning_models.py`**
- [ ] **Step 7: Implement Hybrid ARIMA + XGBoost residual correction model in `hybrid_models.py`**
- [ ] **Step 8: Implement SHAP feature attribution in `explainability.py`**
- [ ] **Step 9: Run model training and walk-forward benchmark across 10 experiments**
- [ ] **Step 10: Run test to verify all models satisfy accuracy and interface assertions**
- [ ] **Step 11: Commit model development suite and evaluation report in `docs/reports/model_evaluation_report.md`**

---

### Task 6: Decision Support Modules (Crop Planning, Market Recommender & Price Alerts)

**Files:**
- Create: `src/decision_support/crop_planner.py`
- Create: `src/decision_support/market_recommender.py`
- Create: `src/decision_support/alert_engine.py`
- Test: `tests/test_decision_support.py`

**Interfaces:**
- Consumes: Price forecasts, historical volatility, arrival trends, market geo-distance matrices, transport rate benchmarks (per km/tonne), and agro-climatic crop suitability calendars.
- Produces: Crop planning suitability index, net margin optimization, multi-mandi arbitrage ranking with net price after logistics, and threshold-based alert triggers.

- [ ] **Step 1: Write test for crop planner ROI ranking, market net realization calculations, and alert triggers**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement `crop_planner.py`, `market_recommender.py`, and `alert_engine.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit decision support suite**

---

### Task 7: FastAPI Backend Service & REST Endpoints

**Files:**
- Create: `src/api/schemas.py`
- Create: `src/api/routes_forecast.py`
- Create: `src/api/routes_market.py`
- Create: `src/api/routes_planning.py`
- Create: `src/api/routes_admin.py`
- Create: `src/api/main.py`
- Test: `tests/test_api.py`

**Interfaces:**
- Consumes: Models, decision support engines, and data pipeline.
- Produces: OpenAPI compliant endpoints (`/api/v1/forecast`, `/api/v1/markets/compare`, `/api/v1/planning/recommend`, `/api/v1/explainability/shap`, `/api/v1/alerts`, `/api/v1/health`).

- [ ] **Step 1: Write test verifying FastAPI endpoints using `fastapi.testclient.TestClient`**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Implement API schemas and endpoint routers in `src/api/`**
- [ ] **Step 4: Run test to verify all endpoints pass with valid responses and error handling**
- [ ] **Step 5: Commit backend API service**

---

### Task 8: Production Web Application Frontend (KrishiMitra AI Dashboard)

**Files:**
- Create: `src/web/index.html`
- Create: `src/web/styles.css`
- Create: `src/web/app.js`
- Test: Verify web UI rendering and end-to-end API integration via client requests

**Interfaces:**
- Consumes: FastAPI backend endpoints.
- Produces: Comprehensive, farmer-friendly, glassmorphic agricultural dashboard supporting:
  - Module A: Farmer Dashboard (Current prices, predicted prices, alerts, weather cards)
  - Module B: Crop Price Forecasting (Commodity, mandi, horizon dropdowns, confidence intervals, interactive charts)
  - Module C: Market Intelligence (Mandi comparisons, arrival trends, volatility gauges)
  - Module D: Intelligent Crop Planning (Season/soil suitability, expected price realization, decision matrix)
  - Module E: Best Market Recommendation (Arbitrage comparison with net returns after transportation)
  - Module F: Explainable AI (Plain-language feature drivers and SHAP waterfalls)
  - Module G: Price Alerts & Notifications (Threshold settings and favourable selling windows)
  - Module H: Admin & Research Dashboard (Model leaderboard, data quality monitor, experiment logs)

- [ ] **Step 1: Construct semantic HTML5 application structure with accessible components and responsive grid**
- [ ] **Step 2: Style with Tailwind CSS + custom glassmorphism and agricultural palette (ivory, deep forest green, emerald, gold)**
- [ ] **Step 3: Implement JavaScript application logic with Plotly.js charts, responsive data tables, and dynamic API bindings**
- [ ] **Step 4: Verify interactive workflows and responsive layouts**
- [ ] **Step 5: Commit web frontend application**

---

### Task 9: IEEE Research Paper & Experimental Reports

**Files:**
- Create: `docs/paper/ieee_paper.md`
- Create: `docs/paper/ieee_paper.tex`
- Create: `docs/reports/experimental_analysis_report.md`
- Test: `tests/test_research_deliverables.py`

**Interfaces:**
- Consumes: Experimental results from 10 experiments, literature review, mathematical model formulations, SHAP explainability analyses, and system architecture.
- Produces: Complete IEEE Transactions-style two-column research paper with 22 sections, equations, tables, figures, authentic citations, and comprehensive experimental report.

- [ ] **Step 1: Write test verifying all 22 required IEEE paper sections and experimental reports exist and contain required equations and tables**
- [ ] **Step 2: Run test to verify failure**
- [ ] **Step 3: Author `docs/paper/ieee_paper.md` and LaTeX `.tex` file with mathematical formulations (ARIMA, XGBoost objective, hybrid residual formulation, SHAP Shapley value attribution)**
- [ ] **Step 4: Author `docs/reports/experimental_analysis_report.md` detailing Experiments 1 through 10**
- [ ] **Step 5: Run test to verify it passes**
- [ ] **Step 6: Commit research paper and experiment deliverables**

---

### Task 10: 20-Slide Research Presentation & Demonstration Automation

**Files:**
- Create: `docs/presentation/presentation_slides.md`
- Create: `docs/presentation/presentation.html`
- Create: `docs/presentation/generate_pptx.py`
- Create: `docs/presentation/KrishiMitra_AI_YIP_Presentation.pptx`
- Create: `run_demo.py`
- Create: `README.md`
- Test: Verify PowerPoint generation and execution of `run_demo.py`

**Interfaces:**
- Consumes: Project findings, benchmark metrics, architecture diagrams, and application features.
- Produces: Exactly 20-slide research-grade PowerPoint `.pptx` presentation, interactive HTML presentation deck, top-level `run_demo.py` runner script, and comprehensive GitHub repository README.

- [ ] **Step 1: Implement `generate_pptx.py` using `python-pptx` to programmatically build the 20-slide academic deck**
- [ ] **Step 2: Run `generate_pptx.py` and verify creation of `KrishiMitra_AI_YIP_Presentation.pptx`**
- [ ] **Step 3: Create companion interactive presentation deck `presentation.html` and markdown summary `presentation_slides.md`**
- [ ] **Step 4: Implement top-level `run_demo.py` executing the end-to-end pipeline and launching the KrishiMitra AI platform**
- [ ] **Step 5: Write comprehensive `README.md` documenting installation, architecture, dataset sources, model benchmarks, and execution instructions**
- [ ] **Step 6: Run full test suite and verify 100% pass rate**
- [ ] **Step 7: Final commit and verification**

