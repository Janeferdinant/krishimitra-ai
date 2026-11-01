# KrishiMitra AI: 20-Slide Research Presentation Deck
## Kerala Young Innovators Programme (YIP 9.0)

---

### Slide 1: Title & Team Introduction
- **Title:** KrishiMitra AI: Agricultural Market Intelligence & Crop Price Forecasting System
- **Subtitle:** An Explainable Multi-Paradigm Machine Learning Platform for Kerala Farmers (YIP 9.0)
- **Research Team:** Multidisciplinary AI, Agro-Economic & Data Science Group
- **Core Domain:** Agricultural Economics, Time-Series Machine Learning, Spatial Arbitrage, Explainable AI

---

### Slide 2: Background and Motivation
- Over 45% of India's workforce depends on agriculture, dominated by smallholders (<1 hectare).
- Kerala's agrarian economy relies heavily on high-value cash crops: Arecanut, Black Pepper, Rubber, Copra, Cardamom, and Nendran Banana.
- Extreme price volatility: Post-harvest gluts routinely trigger 30–50% farm-gate price collapse.
- Severe information asymmetry forces smallholders into distress sales with local village intermediaries.

---

### Slide 3: Problem Statement
- **The Core Dilemma:** Farmers cultivate crops without reliable forecasting of future harvest prices and market demand.
- **Microeconomic Consequences:** Overproduction, unfavorable selling windows, financial indebtedness, and inability to capture value.
- **Logistical Market Friction:** Farmers cannot evaluate whether trucking produce to higher-priced terminal markets yields a net gain after freight costs.
- **Urgent Need:** A scientifically validated, reproducible forecasting tool with actionable decision support.

---

### Slide 4: Challenges Faced by Farmers
- Complete absence of localized, forward-looking market intelligence at the taluk/district level.
- High perishability of horticultural crops (e.g. Nendran banana) demanding precise harvest selling windows.
- Monsoon transit disruptions: Heavy rainfall interrupts sun-drying and delays mandi trade dispatches.
- Point forecasts without uncertainty bounds fail to communicate market risk to risk-averse smallholders.
- Complex data science tools remain inaccessible due to linguistic and technical barriers.

---

### Slide 5: Stakeholder Impact
- **Smallholder Farmers:** +7% to +15% enhanced net price realization, elimination of distress selling, informed crop selection.
- **Farmer Producer Organizations (FPOs):** Synchronized harvesting, collective freight dispatch, and optimal storage management.
- **Agricultural Economists:** Transparent modeling of price-arrival elasticity and cross-mandi spatial transmission.
- **Government Planners:** Automated early warning triggers for market intervention and minimum support price (MSP) execution.

---

### Slide 6: Existing Solutions and Limitations
- **AGMARKNET / e-NAM:** Historical transaction repositories only; zero forward-looking predictive models or uncertainty bounds.
- **TNAU DEMIC (Canvas 2):** Econometric SMS bulletins were valuable, but lacked dynamic ML pipelines and real-time APIs.
- **UAS Bangalore (Canvas 1):** Integrated trader opinion surveys with econometrics, but relied heavily on manual consensus without automated feature engineering.
- **Academic Machine Learning (Canvas 3 & 4):** Univariate models (Sabu & Manoj Kumar 2020; Ananthi et al. 2020) omitted weather and arrival volume dynamics.

---

### Slide 7: Literature Review
- Evaluated 32 verified Q1/Q2 peer-reviewed studies across IEEE, Elsevier, Springer, and ICAR repositories.
- Sabu & Manoj Kumar (2020, Procedia CS): LSTM outperformed Holt-Winters for Kerala Arecanuts (Canvas Source 3).
- Ananthi et al. (2020, JSRR): SVR and Random Forest captured weekly volatility of Wayanad Black Pepper (Canvas Source 4).
- Hybrid Architectures (Liu et al. 2022; Wang et al. 2022): Decoupling secular trend from non-linear residuals yields lowest composite RMSE.
- Exogenous Fusion (Kumar et al. 2023; Xiong et al. 2021): Weather anomalies and arrival volumes provide critical turning-point predictive power.

---

### Slide 8: Research Gap
- **Gap 1:** Omission of multi-source meteorological and physical arrival volume feature fusion.
- **Gap 2:** Fragility of pure deep learning on sparse regional mandi time series with non-trading days.
- **Gap 3:** Complete absence of calibrated 80% and 95% multi-horizon confidence intervals.
- **Gap 4:** Disconnect between price prediction and farm-gate decision support (spatial arbitrage and crop planning).
- **Gap 5:** Black-box models without farmer-accessible natural language explainability.

---

### Slide 9: Objectives and Contributions
- Curate a 6-year, 19,728-record empirical dataset fusing AGMARKNET wholesale records with NASA POWER / IMD meteorology.
- Develop and evaluate a two-stage Hybrid SARIMA + XGBoost residual learning model.
- Implement multi-horizon calibrated confidence intervals (7, 15, 30, and 60 days).
- Translate TreeSHAP game-theoretic feature attributions into natural-language farmer advisories.
- Build spatial arbitrage and intelligent crop planning decision support engines.
- Deploy a production-ready, mobile-responsive full-stack platform.

---

### Slide 10: Proposed Solution: KrishiMitra AI
- Holistic system architecture connecting data acquisition, feature engineering, multi-paradigm modeling, explainability, and decision support.
- Bilingual accessibility: English and Malayalam terminology tailored to Kerala agro-climatic zones.
- Farmer-centric modules: Dashboard, Multi-Horizon Forecast, Market Intelligence, Crop Planner, Arbitrage Finder, and Smart Alerts.
- Strict non-speculative philosophy: Transparent risk ratings without making speculative guaranteed profit claims.

---

### Slide 11: System Architecture
- **Data Pipeline:** Automated ingestion, zero-lookahead chronological imputation, and outlier classification.
- **Feature Store:** 32 engineered features (lags, multi-window rolling stats, arrival momentum, calendar harmonics).
- **Model Tier:** Ensemble of statistical baselines, SARIMA, Random Forest, XGBoost, LightGBM, and Hybrid Residual Booster.
- **Service Tier:** FastAPI asynchronous REST microservices with OpenAPI specifications.
- **Presentation Tier:** Responsive glassmorphic frontend utilizing Plotly.js interactive vector graphics.

---

### Slide 12: Data Collection & Dataset Description
- Coverage: 2020-01-01 through 2025-12-31 (19,728 verified daily observations).
- Target Commodities: Arecanut (Chali), Black Pepper (Garbled), Copra (Milling), Banana (Nendran), Rubber (RSS-4), Cardamom (7-8mm).
- Representative Kerala Mandis: Vatakara, Kochi Terminal, Sulthan Bathery, Palakkad, Nedumkandam, Kottayam, Kasaragod.
- Meteorological Parameters: Daily mean/max/min temperature, precipitation accumulation (mm), and surface relative humidity from NASA POWER / IMD.
- Data Source Register: Fully documented in data/raw/sources_register.json.

---

### Slide 13: Data Preprocessing & EDA Findings
- Augmented Dickey-Fuller (ADF) Test: Level prices are non-stationary (p > 0.40); first differences achieve strong stationarity (p < 0.0001, d=1).
- Arrival-Price Elasticity: Empirical elasticity coefficients are negative (ε = -0.18 to -0.28). Higher arrivals create 1.8–2.8% downward price pressure.
- Price Volatility Index: Banana (CV 22.4%) and Cardamom (CV 24.8%) exhibit high volatility; Copra (CV 10.2%) is highly stable.
- Zero-Leakage Imputation: Chronological forward fill (ffill) ensures no future information contaminates training observations.

---

### Slide 14: Feature Engineering & Selection
- Autoregressive Lags: t-1, t-7, t-14, t-30, t-60 strictly shifted to prevent lookahead leakage.
- Rolling Statistics: 7-day, 14-day, and 30-day means, standard deviations, and exponential moving averages (EMA-7, EMA-14, EMA-30).
- Supply Momentum: Ratio of previous-day arrival to the 7-day rolling arrival baseline.
- Calendar Harmonics: Sin/cos cyclic transformations of month and day of year; explicit Onam and Vishu festival flags.
- Feature Selection: Mutual Information + Random Forest Gini score identified Top-15 features, cutting latency by 58%.

---

### Slide 15: Machine Learning & Deep Learning Models
- Statistical Baselines: Naive (last value), Seasonal Naive (t-365), and 30-day Moving Average.
- Econometric Models: SARIMA(1,1,1)x(1,0,1)7 and Holt-Winters Triple Exponential Smoothing.
- Supervised ML: Linear Ridge, Random Forest Regressor, XGBoost, and LightGBM.
- Deep Learning: Deep Attention Multi-Layer Perceptron (128-64-32) with soft feature gating.
- Two-Stage Hybrid Architecture: SARIMA linear baseline + XGBoost residual error boosting.

---

### Slide 16: Experimental Methodology
- Chronological Splitting: 80% train (Jan 2020 – Sep 2024), 20% future test (Oct 2024 – Dec 2025). Zero random shuffling.
- Walk-Forward Validation: Multi-step ahead rollouts across 7, 15, 30, and 60-day horizons.
- Standard Evaluation Metrics: MAE, RMSE, MAPE, sMAPE, WAPE, and R² Score.
- Ablation Studies: Evaluating independent contributions of weather features, arrival volumes, and feature selection methods.
- 10 Structured Scientific Experiments: Documented in docs/reports/experimental_analysis_report.md.

---

### Slide 17: Model Comparison and Actual Results
- Naive Baseline: RMSE ₹2,163.16/Qtl | MAPE 3.05% | R² -0.464
- SARIMA(1,1,1): RMSE ₹1,784.75/Qtl | MAPE 2.56% | R² 0.003
- Random Forest: RMSE ₹1,433.36/Qtl | MAPE 2.05% | R² 0.357
- XGBoost Regressor: RMSE ₹1,255.46/Qtl | MAPE 1.78% | R² 0.507
- LightGBM Regressor: RMSE ₹1,209.59/Qtl | MAPE 1.68% | R² 0.542
- Deep Attention MLP: RMSE ₹1,069.93/Qtl | MAPE 1.37% | R² 0.642
- Hybrid SARIMA+XGBoost (7-Day): RMSE ₹602.28/Qtl | MAPE 1.45% | R² 0.884 (Top Overall)

---

### Slide 18: Application Demonstration
- Farmer Dashboard: Real-time spot price cards, meteorological alerts, and volatility gauges.
- Crop Forecasting: Interactive Plotly chart with 80% and 95% calibrated confidence intervals.
- Market Arbitrage Engine: Compares nearby mandis, deducts road freight, and identifies maximum net return.
- Intelligent Crop Planner: Calculates projected yield, cultivation costs, net margins, and risk ratings.
- Explainable AI: Translates SHAP values into plain-language agricultural drivers.

---

### Slide 19: Future Scope and Scalability
- Multilingual Voice AI: Speech-to-text advisory in Malayalam dialects for marginal farmers.
- Satellite Remote Sensing: Sentinel-2 NDVI vegetative indices for real-time yield forecasts.
- Spatio-Temporal Graph Neural Networks (ST-GCN): Modeling cross-mandi physical trade flows.
- Integration with Kerala Agriculture Department (KAU / Haritha Keralam / VFPCK) digital initiatives.

---

### Slide 20: Conclusion and References
- Summary: Successfully built, scientifically evaluated, and deployed an end-to-end agricultural forecasting platform.
- Empirical Evidence: Hybrid SARIMA + XGBoost reduces error by 66% over classical statistical baselines.
- Key Citations: Sabu & Manoj Kumar (2020), Ananthi et al. (2020), TNAU RKVY (2018), UAS Bangalore (2021), Liu et al. (2022).
- Project Repository: Fully reproducible code, datasets, reports, IEEE paper, and test suite.
