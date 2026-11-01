"""
Feature Engineering and Feature Selection Pipeline for KrishiMitra AI.
Constructs leak-free time-series lags, multi-window rolling statistics, calendar harmonics,
agro-climatic weather features, and runs feature selection algorithms.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

HARVEST_MONTHS = {
    "Arecanut": [11, 12, 1, 2, 3],
    "Black Pepper": [12, 1, 2, 3],
    "Copra": [3, 4, 5, 6],
    "Banana": [7, 8, 9, 10],
    "Rubber": [10, 11, 12, 1],
    "Cardamom": [8, 9, 10, 11, 12]
}

def generate_features(df: pd.DataFrame, output_path: str = "data/processed/analytical_features_dataset.csv") -> pd.DataFrame:
    """
    Constructs leak-free time-series features grouped by commodity and market.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["commodity", "market", "date"]).reset_index(drop=True)
    
    # 1. Calendar Features
    doy = df["date"].dt.dayofyear
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.dayofweek
    df["quarter"] = df["date"].dt.quarter
    df["year_trend"] = (df["date"].dt.year - 2020) + (doy / 365.25)
    
    # Cyclical harmonics
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12.0)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12.0)
    df["doy_sin"] = np.sin(2 * np.pi * doy / 365.25)
    df["doy_cos"] = np.cos(2 * np.pi * doy / 365.25)
    
    # Festival flags
    df["is_onam"] = ((doy >= 230) & (doy <= 265)).astype(int)
    df["is_vishu"] = ((doy >= 100) & (doy <= 110)).astype(int)
    
    # Harvest flag
    df["is_harvest"] = 0
    for comm, months in HARVEST_MONTHS.items():
        mask = (df["commodity"] == comm) & (df["month"].isin(months))
        df.loc[mask, "is_harvest"] = 1
        
    # 2. Lag Features & Rolling Statistics (STRICTLY SHIFTED BY 1 TO PREVENT DATA LEAKAGE)
    grouped = df.groupby(["commodity", "market"])
    
    # Lagged prices
    for lag in [1, 7, 14, 30, 60]:
        df[f"price_lag_{lag}"] = grouped["modal_price"].shift(lag)
        
    # Lagged arrivals
    for lag in [1, 7, 14]:
        df[f"arrivals_lag_{lag}"] = grouped["arrivals_tonnes"].shift(lag)
        
    # Rolling statistics over t-1 observations
    # We shift first, then apply rolling window
    shifted_price = grouped["modal_price"].shift(1)
    shifted_arrivals = grouped["arrivals_tonnes"].shift(1)
    
    # Group again on the shifted series to preserve market boundaries
    df["price_rolling_mean_7"] = grouped.apply(lambda g: g["modal_price"].shift(1).rolling(7, min_periods=1).mean()).reset_index(level=[0,1], drop=True)
    df["price_rolling_std_7"] = grouped.apply(lambda g: g["modal_price"].shift(1).rolling(7, min_periods=1).std().fillna(0)).reset_index(level=[0,1], drop=True)
    df["price_rolling_mean_14"] = grouped.apply(lambda g: g["modal_price"].shift(1).rolling(14, min_periods=1).mean()).reset_index(level=[0,1], drop=True)
    df["price_rolling_mean_30"] = grouped.apply(lambda g: g["modal_price"].shift(1).rolling(30, min_periods=1).mean()).reset_index(level=[0,1], drop=True)
    df["price_rolling_min_30"] = grouped.apply(lambda g: g["modal_price"].shift(1).rolling(30, min_periods=1).min()).reset_index(level=[0,1], drop=True)
    df["price_rolling_max_30"] = grouped.apply(lambda g: g["modal_price"].shift(1).rolling(30, min_periods=1).max()).reset_index(level=[0,1], drop=True)
    
    # Exponential moving averages
    df["price_ema_7"] = grouped.apply(lambda g: g["modal_price"].shift(1).ewm(span=7, adjust=False).mean()).reset_index(level=[0,1], drop=True)
    df["price_ema_14"] = grouped.apply(lambda g: g["modal_price"].shift(1).ewm(span=14, adjust=False).mean()).reset_index(level=[0,1], drop=True)
    df["price_ema_30"] = grouped.apply(lambda g: g["modal_price"].shift(1).ewm(span=30, adjust=False).mean()).reset_index(level=[0,1], drop=True)
    
    # Arrival rolling and momentum
    arr_mean_7 = grouped.apply(lambda g: g["arrivals_tonnes"].shift(1).rolling(7, min_periods=1).mean()).reset_index(level=[0,1], drop=True)
    df["arrivals_rolling_mean_7"] = arr_mean_7
    df["arrival_momentum_7"] = (df["arrivals_lag_1"] / (arr_mean_7 + 1e-5)).round(3)
    
    # 3. Weather Features (Rolling precipitation, temp anomaly)
    df["rainfall_7d_sum"] = grouped.apply(lambda g: g["rainfall_mm"].shift(1).rolling(7, min_periods=1).sum()).reset_index(level=[0,1], drop=True)
    df["rainfall_14d_sum"] = grouped.apply(lambda g: g["rainfall_mm"].shift(1).rolling(14, min_periods=1).sum()).reset_index(level=[0,1], drop=True)
    temp_mean_30 = grouped.apply(lambda g: g["temp_mean"].shift(1).rolling(30, min_periods=1).mean()).reset_index(level=[0,1], drop=True)
    df["temp_anomaly_30"] = (df["temp_mean"] - temp_mean_30).round(2)
    df["rel_humidity_7d_mean"] = grouped.apply(lambda g: g["rel_humidity_pct"].shift(1).rolling(7, min_periods=1).mean()).reset_index(level=[0,1], drop=True)
    
    # 4. Fill initial boundary lag nulls with first available backfilled value
    lag_cols = [c for c in df.columns if "lag" in c or "rolling" in c or "ema" in c or "sum" in c]
    df[lag_cols] = df.groupby(["commodity", "market"])[lag_cols].bfill()
    
    # Save analytical features dataset
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        export_df = df.copy()
        export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")
        export_df.to_csv(output_path, index=False)
        
    return df

def select_features(
    df: pd.DataFrame, 
    feature_cols: list[str], 
    target_col: str = "modal_price",
    top_k: int = 15
) -> pd.DataFrame:
    """
    Ranks features using Mutual Information and Random Forest Gini Importance.
    """
    clean_sub = df.dropna(subset=feature_cols + [target_col])
    X = clean_sub[feature_cols].select_dtypes(include=[np.number])
    y = clean_sub[target_col]
    
    # Random Forest Importance
    rf = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    rf_scores = rf.feature_importances_
    
    # Mutual Information (subsampled for speed)
    sample_size = min(len(X), 2500)
    indices = np.random.choice(len(X), sample_size, replace=False)
    mi_scores = mutual_info_regression(X.iloc[indices], y.iloc[indices], random_state=42)
    
    # Normalized composite score
    rf_norm = rf_scores / (np.max(rf_scores) + 1e-8)
    mi_norm = mi_scores / (np.max(mi_scores) + 1e-8)
    composite = 0.6 * rf_norm + 0.4 * mi_norm
    
    importance_df = pd.DataFrame({
        "feature": X.columns,
        "rf_importance": np.round(rf_scores, 4),
        "mi_score": np.round(mi_scores, 4),
        "importance_score": np.round(composite, 4)
    }).sort_values(by="importance_score", ascending=False).reset_index(drop=True)
    
    return importance_df.head(top_k)

if __name__ == "__main__":
    cleaned = pd.read_csv("data/processed/cleaned_agricultural_market_dataset.csv")
    feat_df = generate_features(cleaned)
    print("Features generated. Shape:", feat_df.shape)
    
    feat_cols = [c for c in feat_df.columns if c not in ["date", "state", "district", "market", "commodity", "variety", "modal_price", "min_price", "max_price"]]
    top_feats = select_features(feat_df[feat_df["commodity"] == "Arecanut"], feat_cols)
    print("Top Features:\n", top_feats)

