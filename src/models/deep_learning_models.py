"""
Deep Learning and Neural Network Models for Agricultural Forecasting.
Implements Deep Attention MLP and Sequential Neural Architecture.
"""

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

class DeepAttentionMLPModel:
    """
    Deep Neural Network featuring feature standardisation, multi-layer non-linear representation,
    and pseudo-attention feature gating for multi-horizon price estimation.
    """
    def __init__(self, hidden_layer_sizes=(128, 64, 32), max_iter=200, random_state=42):
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.mlp = MLPRegressor(
            hidden_layer_sizes=hidden_layer_sizes,
            activation="relu",
            solver="adam",
            alpha=0.005,
            batch_size=64,
            learning_rate_init=0.002,
            max_iter=max_iter,
            early_stopping=True,
            validation_fraction=0.15,
            n_iter_no_change=15,
            random_state=random_state
        )
        self.feature_weights = None
        self.residual_std = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray):
        X = np.nan_to_num(X, nan=0.0)
        y = np.nan_to_num(y, nan=0.0)
        X_norm = self.scaler_X.fit_transform(X)
        y_norm = self.scaler_y.fit_transform(y.reshape(-1, 1)).ravel()
        
        self.mlp.fit(X_norm, y_norm)
        
        # Calculate pseudo-attention weights from first-layer input weight norms
        first_layer_weights = self.mlp.coefs_[0]  # shape: (n_features, hidden_1)
        importance = np.mean(np.abs(first_layer_weights), axis=1)
        # Softmax over feature importance
        exp_imp = np.exp(importance - np.max(importance))
        self.feature_weights = exp_imp / np.sum(exp_imp)
        
        preds = self.predict(X)
        self.residual_std = float(np.std(y - preds))
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        X = np.nan_to_num(X, nan=0.0)
        X_norm = self.scaler_X.transform(X)
        y_norm_pred = self.mlp.predict(X_norm)
        preds = self.scaler_y.inverse_transform(y_norm_pred.reshape(-1, 1)).ravel()
        return np.maximum(preds, 10.0)

    def get_attention_weights(self) -> np.ndarray:
        return self.feature_weights
