"""
Statistical Baseline Models for Agricultural Price Forecasting.
Establishes benchmark references: Naive, Seasonal Naive, and Rolling Moving Average.
"""

import numpy as np

class NaiveForecastModel:
    """
    Standard Naive model: Predicts future horizons equal to the last observed historical price.
    y_{t+h} = y_t
    """
    def __init__(self):
        self.last_observation = None
        
    def fit(self, y: np.ndarray):
        self.last_observation = float(y[-1])
        return self
        
    def predict(self, horizon: int) -> np.ndarray:
        if self.last_observation is None:
            raise ValueError("Model must be fitted before predict.")
        return np.full(horizon, self.last_observation)

class SeasonalNaiveModel:
    """
    Seasonal Naive model: Predicts future price equal to the price observed one full seasonal cycle prior.
    y_{t+h} = y_{t+h - season_length}
    """
    def __init__(self, season_length: int = 365):
        self.season_length = season_length
        self.history = None
        
    def fit(self, y: np.ndarray):
        self.history = np.array(y)
        return self
        
    def predict(self, horizon: int) -> np.ndarray:
        if self.history is None or len(self.history) < self.season_length:
            # Fallback to mean of last available season if history is short
            return np.full(horizon, np.mean(self.history))
        preds = []
        for h in range(1, horizon + 1):
            idx = -self.season_length + ((h - 1) % self.season_length)
            preds.append(self.history[idx])
        return np.array(preds)

class MovingAverageBaseline:
    """
    Simple Moving Average baseline: Predicts the arithmetic mean of the last k periods.
    """
    def __init__(self, window: int = 30):
        self.window = window
        self.mean_val = None
        
    def fit(self, y: np.ndarray):
        k = min(len(y), self.window)
        self.mean_val = float(np.mean(y[-k:]))
        return self
        
    def predict(self, horizon: int) -> np.ndarray:
        return np.full(horizon, self.mean_val)

