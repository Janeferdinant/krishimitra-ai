import os
import pandas as pd
import numpy as np
import pytest

def test_feature_engineering_pipeline():
    from src.data_pipeline.feature_engineering import generate_features, select_features
    
    cleaned_path = os.path.join("data", "processed", "cleaned_agricultural_market_dataset.csv")
    assert os.path.exists(cleaned_path), "Preprocessed data required"
    
    df = pd.read_csv(cleaned_path)
    
    # 1. Feature generation
    features_df = generate_features(df)
    assert isinstance(features_df, pd.DataFrame)
    
    # Check time-based features
    assert "month" in features_df.columns
    assert "day_of_week" in features_df.columns
    assert "is_onam" in features_df.columns
    assert "is_harvest" in features_df.columns
    
    # Check lag features
    for lag in [1, 7, 14, 30, 60]:
        col_name = f"price_lag_{lag}"
        assert col_name in features_df.columns, f"Lag feature missing: {col_name}"
        
    # Check rolling statistics
    assert "price_rolling_mean_7" in features_df.columns
    assert "price_rolling_std_7" in features_df.columns
    assert "price_rolling_mean_30" in features_df.columns
    assert "price_ema_14" in features_df.columns
    
    # Check exogenous features
    assert "rainfall_7d_sum" in features_df.columns
    assert "arrival_momentum_7" in features_df.columns
    
    # Verify zero-leakage: lag_1 must strictly equal previous day's modal_price for each series
    sample_series = features_df[(features_df["commodity"] == "Arecanut") & (features_df["market"] == "Vatakara APMC")].sort_values("date")
    assert sample_series["price_lag_1"].iloc[5] == sample_series["modal_price"].iloc[4], "Leakage check: price_lag_1 must equal t-1 modal_price"
    
    # Verify feature selection
    feature_cols = [c for c in features_df.columns if c not in ["date", "state", "district", "market", "commodity", "variety", "modal_price", "min_price", "max_price"]]
    importance_df = select_features(features_df[features_df["commodity"] == "Arecanut"], feature_cols=feature_cols, target_col="modal_price")
    
    assert isinstance(importance_df, pd.DataFrame)
    assert "feature" in importance_df.columns
    assert "importance_score" in importance_df.columns
    assert len(importance_df) > 10
    
    # Verify exported analytical features file exists
    features_path = os.path.join("data", "processed", "analytical_features_dataset.csv")
    assert os.path.exists(features_path), f"Features dataset missing at {features_path}"

