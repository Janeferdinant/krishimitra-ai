import os
import json
import numpy as np
import pandas as pd
import pytest

def test_models_suite_and_evaluation():
    from src.models.baselines import NaiveForecastModel, SeasonalNaiveModel
    from src.models.ml_models import MLForecastingSuite
    from src.models.hybrid_models import HybridSarimaXGBoostModel
    from src.models.validation import evaluate_all_models, compute_metrics
    from src.models.explainability import AgriculturalShapExplainer
    
    # 1. Test metric computations
    y_true = np.array([100.0, 105.0, 110.0, 95.0, 100.0])
    y_pred = np.array([102.0, 104.0, 108.0, 97.0, 101.0])
    metrics = compute_metrics(y_true, y_pred)
    
    assert "mae" in metrics
    assert "rmse" in metrics
    assert "mape" in metrics
    assert "smape" in metrics
    assert "wape" in metrics
    assert "r2" in metrics
    assert metrics["mae"] > 0
    assert metrics["mape"] < 10.0  # Percentage error should be low for this toy sample
    
    # 2. Test baseline models
    naive = NaiveForecastModel()
    train_series = np.array([100, 102, 105, 107, 110])
    naive.fit(train_series)
    preds = naive.predict(horizon=5)
    assert len(preds) == 5
    assert (preds == 110).all()
    
    # 3. Test ML Models & Hybrid Model on sample commodity series
    features_path = os.path.join("data", "processed", "analytical_features_dataset.csv")
    assert os.path.exists(features_path)
    df = pd.read_csv(features_path)
    sub_df = df[(df["commodity"] == "Banana") & (df["market"] == "Palakkad APMC")].sort_values("date").reset_index(drop=True)
    
    # ML Suite
    ml_suite = MLForecastingSuite()
    train_size = int(len(sub_df) * 0.8)
    train_df = sub_df.iloc[:train_size]
    test_df = sub_df.iloc[train_size:]
    
    feature_cols = [c for c in sub_df.columns if "lag" in c or "rolling" in c or "ema" in c or "sin" in c or "cos" in c]
    trained_models = ml_suite.fit_all(train_df, feature_cols=feature_cols, target_col="modal_price")
    assert "xgboost" in trained_models
    assert "lightgbm" in trained_models
    assert "random_forest" in trained_models
    
    xgb_preds, xgb_ci = ml_suite.predict("xgboost", test_df, feature_cols=feature_cols, return_ci=True)
    assert len(xgb_preds) == len(test_df)
    assert "lower_80" in xgb_ci
    assert "upper_80" in xgb_ci
    assert (xgb_ci["lower_80"] <= xgb_preds).all()
    assert (xgb_preds <= xgb_ci["upper_80"]).all()
    
    # Hybrid Model
    hybrid = HybridSarimaXGBoostModel()
    hybrid.fit(train_df["modal_price"].values, train_df[feature_cols].values)
    hybrid_preds = hybrid.predict(horizon=len(test_df), X_exog=test_df[feature_cols].values)
    assert len(hybrid_preds) == len(test_df)
    
    # SHAP Explainer
    explainer = AgriculturalShapExplainer(trained_models["xgboost"], feature_cols)
    explanation = explainer.explain_instance(test_df.iloc[0])
    assert "feature_contributions" in explanation
    assert "natural_language_advisory" in explanation
    assert len(explanation["feature_contributions"]) > 0
    assert len(explanation["natural_language_advisory"]) > 20

