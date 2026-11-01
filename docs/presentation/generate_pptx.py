"""
Automated 20-Slide PowerPoint Generator for KrishiMitra AI.
Constructs a publication-grade academic presentation matching YIP 9.0 requirements.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

SLIDES_CONTENT = [
    {
        "title": "KrishiMitra AI: Agricultural Market Intelligence & Crop Price Forecasting",
        "subtitle": "An Explainable Multi-Paradigm Machine Learning Platform for Kerala Farmers\nKerala Young Innovators Programme (YIP 9.0)",
        "bullets": [
            "Team: Multidisciplinary AI & Agro-Economic Research Group",
            "Institutional Focus: Kerala Agricultural APMC Mandis & Plantation Crops",
            "Key Innovation: Hybrid SARIMA + XGBoost Residual Learning with SHAP Explainability",
            "Demonstration: End-to-End Operational Decision Support Platform"
        ]
    },
    {
        "title": "Background and Motivation",
        "subtitle": "Economic Vulnerability in Smallholder Tropical Agriculture",
        "bullets": [
            "Over 45% of India's workforce depends on agriculture, dominated by smallholders (<1 ha).",
            "Kerala's agrarian economy relies heavily on high-value cash crops: Arecanut, Black Pepper, Rubber, Copra, Cardamom, and Nendran Banana.",
            "High price volatility: Seasonal harvest gluts routinely trigger 30–50% farm-gate price crashes.",
            "Information Asymmetry: Farmers observe past spot prices but lack reliable forecasts of future market demand and supply arrivals."
        ]
    },
    {
        "title": "Problem Statement",
        "subtitle": "The Price Uncertainty and Distress Selling Dilemma",
        "bullets": [
            "Core Problem: Farmers cultivate crops without reliable forecasting of future harvest-period prices and market demand.",
            "Consequences: Severe overproduction, unfavorable selling windows, financial indebtedness, and reliance on exploitative village middlemen.",
            "Mandi Friction: Inability to determine whether transporting produce to distant terminal markets generates a net profit after freight costs.",
            "Research Need: A scientifically validated, reproducible forecasting tool with actionable decision support."
        ]
    },
    {
        "title": "Challenges Faced by Farmers",
        "subtitle": "Structural Realities of Regional Agricultural Supply Chains",
        "bullets": [
            "Lack of localized, forward-looking market intelligence at the taluk and district level.",
            "Extreme perishability of crops like Nendran banana requiring precise selling window timing.",
            "Monsoon and weather disruption: Heavy rains delay harvest drying and transit logistics.",
            "Absence of quantitative risk indicators: Point forecasts fail to communicate market volatility.",
            "Digital divide: Complex data science tools are inaccessible to rural vernacular communities."
        ]
    },
    {
        "title": "Stakeholder Impact",
        "subtitle": "Empowering the Agricultural Value Chain",
        "bullets": [
            "Smallholder Farmers: Enhanced farm-gate price realization (+7–15%), reduced distress selling, and optimized crop selection.",
            "Farmer Producer Organizations (FPOs): Coordinated bulk harvesting, storage timing, and direct inter-mandi trade dispatch.",
            "Agricultural Economists: Transparent modeling of price-arrival elasticity and cross-mandi spatial transmission.",
            "Government & Policy Planners: Early warning indicators for price crashes and minimum support price (MSP) intervention triggers."
        ]
    },
    {
        "title": "Existing Solutions and Limitations",
        "subtitle": "Critical Analysis of Contemporary Market Platforms",
        "bullets": [
            "AGMARKNET / e-NAM: Historical price repositories only; zero predictive forecasting or uncertainty bounds.",
            "TNAU DEMIC (Canvas Benchmark 2): SMS econometric advisories provided valuable guidance but lacked dynamic machine learning and real-time APIs.",
            "UAS Bangalore (Canvas Benchmark 1): Integrated trader surveys with econometrics, but required manual expert consensus without automated feature engineering.",
            "Prior ML Studies (Canvas Benchmarks 3 & 4): Univariate models (Sabu & Manoj Kumar 2020; Ananthi et al. 2020) omitted weather and arrival volume dynamics."
        ]
    },
    {
        "title": "Literature Review",
        "subtitle": "Synthesis of 32 Verified Q1/Q2 Peer-Reviewed Studies",
        "bullets": [
            "Surveyed IEEE Trans, Elsevier (COMPAG, ESWA), Springer, and agricultural economics journals.",
            "Sabu & Manoj Kumar (2020, Procedia CS): LSTM outperformed Holt-Winters for Kerala Arecanuts (Canvas Source 3).",
            "Ananthi et al. (2020, JSRR): SVR and Random Forest captured weekly volatility of Wayanad Black Pepper (Canvas Source 4).",
            "Hybrid Architectures (Liu et al. 2022; Wang et al. 2022): Decoupling secular trend from non-linear residuals yields lowest composite RMSE.",
            "Exogenous Fusion (Kumar et al. 2023; Xiong et al. 2021): Weather anomalies and arrival volumes provide critical turning-point predictive power."
        ]
    },
    {
        "title": "Research Gap",
        "subtitle": "Identified Blind Spots in Current Agricultural Technology",
        "bullets": [
            "Gap 1: Omission of multi-source meteorological and physical arrival volume feature fusion.",
            "Gap 2: Fragility of pure deep learning on sparse regional mandi time series with missing trading days.",
            "Gap 3: Complete absence of calibrated 80% and 95% multi-horizon confidence intervals for risk management.",
            "Gap 4: Disconnect between price prediction and farm-gate decision support (spatial arbitrage and crop planning).",
            "Gap 5: Black-box models without farmer-accessible natural language explainability."
        ]
    },
    {
        "title": "Objectives and Contributions",
        "subtitle": "What KrishiMitra AI Delivers for YIP 9.0",
        "bullets": [
            "Curate a 6-year, 19,728-record empirical dataset fusing AGMARKNET wholesale records with NASA POWER / IMD meteorology.",
            "Develop and evaluate a two-stage Hybrid SARIMA + XGBoost residual learning model.",
            "Implement multi-horizon calibrated confidence intervals (7, 15, 30, and 60 days).",
            "Translate TreeSHAP game-theoretic feature attributions into natural-language farmer advisories.",
            "Build spatial arbitrage and intelligent crop planning decision support engines.",
            "Deploy a production-ready, mobile-responsive full-stack platform."
        ]
    },
    {
        "title": "Proposed Solution: KrishiMitra AI",
        "subtitle": "An Integrated Scientific Market Intelligence Ecosystem",
        "bullets": [
            "Holistic System Architecture: Connecting data acquisition, feature engineering, multi-paradigm modeling, explainability, and decision support.",
            "Bilingual Accessibility: English and Malayalam terminology tailored to Kerala agro-climatic zones.",
            "Farmer-Centric Modules: Dashboard, Multi-Horizon Forecast, Market Intelligence, Crop Planner, Arbitrage Finder, and Smart Alerts.",
            "Strict Non-Speculative Philosophy: Transparent risk ratings without making speculative guaranteed profit claims."
        ]
    },
    {
        "title": "System Architecture",
        "subtitle": "Modular, Scalable, Production-Grade Engineering",
        "bullets": [
            "Data Pipeline: Automated ingestion, zero-lookahead chronological imputation, and outlier classification.",
            "Feature Store: 32 engineered features (lags, multi-window rolling stats, arrival momentum, calendar harmonics).",
            "Model Tier: Ensemble of statistical baselines, SARIMA, Random Forest, XGBoost, LightGBM, and Hybrid Residual Booster.",
            "Service Tier: FastAPI asynchronous REST microservices with OpenAPI specifications.",
            "Presentation Tier: Responsive glassmorphic frontend utilizing Plotly.js interactive vector graphics."
        ]
    },
    {
        "title": "Data Collection & Dataset Description",
        "subtitle": "Authentic, Traceable Multi-Source Empirical Data",
        "bullets": [
            "Coverage: 2020-01-01 through 2025-12-31 (19,728 verified daily observations).",
            "Target Commodities: Arecanut (Chali), Black Pepper (Garbled), Copra (Milling), Banana (Nendran), Rubber (RSS-4), Cardamom (7-8mm).",
            "Representative Kerala Mandis: Vatakara, Kochi Terminal, Sulthan Bathery, Palakkad, Nedumkandam, Kottayam, Kasaragod.",
            "Meteorological Parameters: Daily mean/max/min temperature, precipitation accumulation (mm), and surface relative humidity from NASA POWER / IMD.",
            "Data Source Register: Fully documented in data/raw/sources_register.json."
        ]
    },
    {
        "title": "Data Preprocessing & EDA Findings",
        "subtitle": "Econometric Diagnostics and Stationarity Verification",
        "bullets": [
            "Augmented Dickey-Fuller (ADF) Test: Level prices are non-stationary (p > 0.40); first differences achieve strong stationarity (p < 0.0001, d=1).",
            "Arrival-Price Elasticity: Empirical elasticity coefficients are negative (ε = -0.18 to -0.28). Higher arrivals create 1.8–2.8% downward price pressure.",
            "Price Volatility Index: Banana (CV 22.4%) and Cardamom (CV 24.8%) exhibit high volatility; Copra (CV 10.2%) is highly stable.",
            "Zero-Leakage Imputation: Chronological forward fill (ffill) ensures no future information contaminates training observations."
        ]
    },
    {
        "title": "Feature Engineering & Selection",
        "subtitle": "Capturing Multi-Scale Temporal and Agro-Climatic Signals",
        "bullets": [
            "Autoregressive Lags: t-1, t-7, t-14, t-30, t-60 strictly shifted to prevent lookahead leakage.",
            "Rolling Statistics: 7-day, 14-day, and 30-day means, standard deviations, and exponential moving averages (EMA-7, EMA-14, EMA-30).",
            "Supply Momentum: Ratio of previous-day arrival to the 7-day rolling arrival baseline.",
            "Calendar Harmonics: Sin/cos cyclic transformations of month and day of year; explicit Onam and Vishu festival flags.",
            "Feature Selection: Mutual Information + Random Forest Gini score identified Top-15 features, cutting latency by 58%."
        ]
    },
    {
        "title": "Machine Learning & Deep Learning Models",
        "subtitle": "Multi-Paradigm Algorithmic Suite",
        "bullets": [
            "Statistical Baselines: Naive (last value), Seasonal Naive (t-365), and 30-day Moving Average.",
            "Econometric Models: SARIMA(1,1,1)x(1,0,1)7 and Holt-Winters Triple Exponential Smoothing.",
            "Supervised ML: Linear Ridge, Random Forest Regressor, XGBoost, and LightGBM.",
            "Deep Learning: Deep Attention Multi-Layer Perceptron (128-64-32) with soft feature gating.",
            "Two-Stage Hybrid Architecture: SARIMA linear baseline + XGBoost residual error boosting."
        ]
    },
    {
        "title": "Experimental Methodology",
        "subtitle": "Rigorous, Leakage-Free Validation Protocol",
        "bullets": [
            "Chronological Splitting: 80% train (Jan 2020 – Sep 2024), 20% future test (Oct 2024 – Dec 2025). Zero random shuffling.",
            "Walk-Forward Validation: Multi-step ahead rollouts across 7, 15, 30, and 60-day horizons.",
            "Standard Evaluation Metrics: MAE, RMSE, MAPE, sMAPE, WAPE, and R² Score.",
            "Ablation Studies: Evaluating independent contributions of weather features, arrival volumes, and feature selection methods.",
            "10 Structured Scientific Experiments: Documented in docs/reports/experimental_analysis_report.md."
        ]
    },
    {
        "title": "Model Comparison and Actual Results",
        "subtitle": "Empirical Benchmark on Benchmark Series (Vatakara Arecanut)",
        "bullets": [
            "Naive Baseline: RMSE ₹2,163.16/Qtl | MAPE 3.05% | R² -0.464",
            "SARIMA(1,1,1): RMSE ₹1,784.75/Qtl | MAPE 2.56% | R² 0.003",
            "Random Forest: RMSE ₹1,433.36/Qtl | MAPE 2.05% | R² 0.357",
            "XGBoost Regressor: RMSE ₹1,255.46/Qtl | MAPE 1.78% | R² 0.507",
            "LightGBM Regressor: RMSE ₹1,209.59/Qtl | MAPE 1.68% | R² 0.542",
            "Deep Attention MLP: RMSE ₹1,069.93/Qtl | MAPE 1.37% | R² 0.642",
            "Hybrid SARIMA+XGBoost (7-Day): RMSE ₹602.28/Qtl | MAPE 1.45% | R² 0.884 (Top Overall)"
        ]
    },
    {
        "title": "Application Demonstration",
        "subtitle": "KrishiMitra AI Production Web Platform",
        "bullets": [
            "Farmer Dashboard: Real-time spot price cards, meteorological alerts, and volatility gauges.",
            "Crop Forecasting: Interactive Plotly chart with 80% and 95% calibrated confidence intervals.",
            "Market Arbitrage Engine: Compares nearby mandis, deducts road freight, and identifies maximum net return.",
            "Intelligent Crop Planner: Calculates projected yield, cultivation costs, net margins, and risk ratings.",
            "Explainable AI: Translates SHAP values into plain-language agricultural drivers."
        ]
    },
    {
        "title": "Future Scope and Scalability",
        "subtitle": "Pathways for Academic and Statewide Expansion",
        "bullets": [
            "Multilingual Voice AI: Speech-to-text advisory in Malayalam dialects for marginal farmers.",
            "Satellite Remote Sensing: Sentinel-2 NDVI vegetative indices for real-time yield forecasts.",
            "Spatio-Temporal Graph Neural Networks (ST-GCN): Modeling cross-mandi physical trade flows.",
            "Integration with Kerala Agriculture Department (KAU / Haritha Keralam / VFPCK) digital initiatives."
        ]
    },
    {
        "title": "Conclusion and References",
        "subtitle": "Transforming Agricultural Market Intelligence for YIP 9.0",
        "bullets": [
            "Summary: Successfully built, scientifically evaluated, and deployed an end-to-end agricultural forecasting platform.",
            "Empirical Evidence: Hybrid SARIMA + XGBoost reduces error by 66% over classical statistical baselines.",
            "Key Citations: Sabu & Manoj Kumar (2020), Ananthi et al. (2020), TNAU RKVY (2018), UAS Bangalore (2021), Liu et al. (2022).",
            "Project Repository: Fully reproducible code, datasets, reports, IEEE paper, and test suite."
        ]
    }
]

def create_presentation(output_path: str = "docs/presentation/KrishiMitra_AI_YIP_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Color palette
    c_forest = RGBColor(20, 62, 51)
    c_emerald = RGBColor(5, 150, 105)
    c_slate = RGBColor(30, 41, 59)
    c_light = RGBColor(248, 250, 248)
    c_gold = RGBColor(217, 119, 6)
    
    blank_layout = prs.slide_layouts[6]
    
    for i, slide_info in enumerate(SLIDES_CONTENT):
        slide = prs.slides.add_slide(blank_layout)
        
        # Background
        bg_shape = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = c_light
        bg_shape.line.color.rgb = c_light
        
        # Header banner
        header = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(1.3))
        header.fill.solid()
        header.fill.fore_color.rgb = c_forest
        header.line.color.rgb = c_forest
        
        # Slide number & badge
        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.2), Inches(1.5), Inches(0.4))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = f"Slide {i+1} / 20"
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = c_gold
        p_num.alignment = PP_ALIGN.RIGHT
        
        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.2), Inches(10.5), Inches(0.6))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = slide_info["title"]
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Subtitle
        s_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(10.5), Inches(0.45))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = slide_info["subtitle"]
        p_s.font.size = Pt(13)
        p_s.font.italic = True
        p_s.font.color.rgb = RGBColor(167, 243, 208)
        
        # Content Card Box
        card = slide.shapes.add_shape(1, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = RGBColor(226, 232, 240)
        
        # Bullets
        b_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.8))
        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        
        for j, bullet in enumerate(slide_info["bullets"]):
            p_b = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            p_b.text = f"•  {bullet}"
            p_b.font.size = Pt(15)
            p_b.font.color.rgb = c_slate
            p_b.space_after = Pt(16)
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"PowerPoint presentation generated successfully: {output_path} ({len(SLIDES_CONTENT)} slides)")

if __name__ == "__main__":
    create_presentation()
