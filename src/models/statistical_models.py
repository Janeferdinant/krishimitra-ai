"""
Econometric and Statistical Forecasting Models.
Implements SARIMA (Seasonal Autoregressive Integrated Moving Average) and Holt-Winters Exponential Smoothing.
"""

import numpy as np
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class SarimaForecastingModel:
    """
    SARIMA(p, d, q) x (P, D, Q)_s econometric model with support for exogenous regressors.
    """
    def __init__(self, order=(1, 1, 1), seasonal_order=(1, 0, 1, 7)):
        self.order = order
        self.seasonal_order = seasonal_order
        self.model_res = None
        self.last_y = None
        
    def fit(self, y: np.ndarray, exog: np.ndarray = None):
        self.last_y = y[-1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Subsample recent 500 points for computational efficiency during training
            train_y = y[-500:] if len(y) > 500 else y
            train_exog = exog[-500:] if exog is not None and len(exog) > 500 else exog
            
            model = SARIMAX(
                train_y,
                exog=train_exog,
                order=self.order,
                seasonal_order=self.seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            self.model_res = model.fit(disp=False, maxiter=50)
        return self
        
    def predict(self, horizon: int, exog: np.ndarray = None) -> np.ndarray:
        if self.model_res is None:
            raise ValueError("Model must be fitted before predict.")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            forecast = self.model_res.forecast(steps=horizon, exog=exog)
            # Clip negative predictions to positive floor
            forecast = np.maximum(np.array(forecast), 10.0)
            return forecast

class HoltWintersModel:
    """
    Holt-Winters Triple Exponential Smoothing (Level, Trend, Seasonal).
    """
    def __init__(self, seasonal_periods: int = 7, trend: str = "add", seasonal: str = "add"):
        self.seasonal_periods = seasonal_periods
        self.trend = trend
        self.seasonal = seasonal
        self.model_res = None
        
    def fit(self, y: np.ndarray):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            train_y = y[-400:] if len(y) > 400 else y
            hw = ExponentialSmoothing(
                train_y,
                seasonal_periods=self.seasonal_periods,
                trend=self.trend,
                seasonal=self.seasonal,
                initialization_method="estimated"
            )
            self.model_res = hw.fit()
        return self
        
    def predict(self, horizon: int) -> np.ndarray:
        if self.model_res is None:
            raise ValueError("Model must be fitted before predict.")
        forecast = self.model_res.forecast(horizon)
        return np.maximum(np.array(forecast), 10.0)
