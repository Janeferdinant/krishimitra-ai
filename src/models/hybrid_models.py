"""
Hybrid Econometric + Machine Learning Model for Agricultural Forecasting.
Combines linear and seasonal modeling (SARIMA) with non-linear residual boosting (XGBoost).
"""

import numpy as np
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
import xgboost as xgb

class HybridSarimaXGBoostModel:
    """
    Two-stage Hybrid Architecture:
    Stage 1: SARIMA models secular trend and annual/weekly seasonality: y_t = L_t + e_t
    Stage 2: XGBoost models residual non-linear interactions e_t = f(X_t)
    Final: y^_t = L^_t + f(X_t)
    """
    def __init__(self, sarima_order=(1, 1, 1), seasonal_order=(1, 0, 1, 7)):
        self.sarima_order = sarima_order
        self.seasonal_order = seasonal_order
        self.sarima_res = None
        self.xgb_residual_model = None
        self.residual_std = 0.0
        self.last_y = None

    def fit(self, y: np.ndarray, X_exog: np.ndarray):
        self.last_y = y[-1]
        n_samples = len(y)
        train_window = min(n_samples, 600)
        
        # Subsample if long for fast convergence
        y_sub = np.nan_to_num(y[-train_window:], nan=0.0)
        X_sub = np.nan_to_num(X_exog[-train_window:], nan=0.0)
        
        # Stage 1: Fit SARIMA
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sarima = SARIMAX(
                y_sub,
                order=self.sarima_order,
                seasonal_order=self.seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            self.sarima_res = sarima.fit(disp=False, maxiter=40)
            linear_pred = self.sarima_res.fittedvalues
            residuals = y_sub - linear_pred
            
        # Stage 2: Fit XGBoost on residuals
        self.xgb_residual_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.04,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=42,
            n_jobs=-1
        )
        self.xgb_residual_model.fit(X_sub, residuals)
        
        # Calculate final hybrid residuals
        hybrid_in_sample = linear_pred + self.xgb_residual_model.predict(X_sub)
        self.residual_std = float(np.std(y_sub - hybrid_in_sample))
        return self

    def predict(self, horizon: int, X_exog: np.ndarray) -> np.ndarray:
        if self.sarima_res is None or self.xgb_residual_model is None:
            raise ValueError("Hybrid model must be fitted prior to prediction.")
            
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            linear_forecast = self.sarima_res.forecast(steps=horizon)
            
        # Ensure X_exog matches horizon
        X_exog = np.nan_to_num(X_exog, nan=0.0)
        X_eval = X_exog[:horizon] if len(X_exog) >= horizon else np.tile(X_exog[-1], (horizon, 1))
        nonlinear_residuals = self.xgb_residual_model.predict(X_eval)
        
        final_forecast = np.array(linear_forecast) + nonlinear_residuals
        return np.maximum(final_forecast, 10.0)

    def get_confidence_intervals(self, preds: np.ndarray) -> dict:
        z80 = 1.282
        z95 = 1.960
        return {
            "lower_80": np.maximum(preds - z80 * self.residual_std, 10.0),
            "upper_80": preds + z80 * self.residual_std,
            "lower_95": np.maximum(preds - z95 * self.residual_std, 10.0),
            "upper_95": preds + z95 * self.residual_std
        }
