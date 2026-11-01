"""
Machine Learning Forecasting Suite for KrishiMitra AI.
Implements Random Forest, XGBoost, and LightGBM with quantile uncertainty bounds.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
import xgboost as xgb
import lightgbm as lgb

class MLForecastingSuite:
    def __init__(self):
        self.models = {}
        self.residual_std = {}
        self.feature_cols = []
        
    def fit_all(self, train_df: pd.DataFrame, feature_cols: list[str], target_col: str = "modal_price") -> dict:
        self.feature_cols = feature_cols
        X = np.nan_to_num(train_df[feature_cols].values, nan=0.0)
        y = np.nan_to_num(train_df[target_col].values, nan=0.0)
        
        # 1. Random Forest Regressor
        rf = RandomForestRegressor(
            n_estimators=100, 
            max_depth=12, 
            min_samples_split=4, 
            random_state=42, 
            n_jobs=-1
        )
        rf.fit(X, y)
        self.models["random_forest"] = rf
        
        # 2. XGBoost Regressor
        xgb_reg = xgb.XGBRegressor(
            n_estimators=120,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
            n_jobs=-1
        )
        xgb_reg.fit(X, y)
        self.models["xgboost"] = xgb_reg
        
        # 3. LightGBM Regressor
        lgb_reg = lgb.LGBMRegressor(
            n_estimators=120,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
        lgb_reg.fit(X, y)
        self.models["lightgbm"] = lgb_reg
        
        # 4. Linear Ridge Baseline
        ridge = Ridge(alpha=1.0)
        ridge.fit(X, y)
        self.models["ridge"] = ridge
        
        # Compute in-sample residual standard deviation for calibrated confidence bounds
        for name, model in self.models.items():
            in_sample_preds = model.predict(X)
            resids = y - in_sample_preds
            self.residual_std[name] = float(np.std(resids))
            
        return self.models

    def predict(
        self, 
        model_name: str, 
        test_df: pd.DataFrame, 
        feature_cols: list[str] = None,
        return_ci: bool = True
    ) -> tuple[np.ndarray, dict]:
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not fitted. Choose from {list(self.models.keys())}")
            
        cols = feature_cols or self.feature_cols
        X = np.nan_to_num(test_df[cols].values, nan=0.0)
        model = self.models[model_name]
        preds = model.predict(X)
        preds = np.maximum(preds, 10.0)
        
        ci = {}
        if return_ci:
            std = self.residual_std.get(model_name, np.std(preds) * 0.05)
            # 80% CI (z = 1.28) and 95% CI (z = 1.96)
            ci["lower_80"] = np.maximum(preds - 1.282 * std, 10.0)
            ci["upper_80"] = preds + 1.282 * std
            ci["lower_95"] = np.maximum(preds - 1.960 * std, 10.0)
            ci["upper_95"] = preds + 1.960 * std
            
        return preds, ci

    def save(self, filepath: str = "artifacts/trained_models/ml_suite.pkl"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({"models": self.models, "std": self.residual_std, "features": self.feature_cols}, filepath)

    def load(self, filepath: str = "artifacts/trained_models/ml_suite.pkl"):
        data = joblib.load(filepath)
        self.models = data["models"]
        self.residual_std = data["std"]
        self.feature_cols = data["features"]
