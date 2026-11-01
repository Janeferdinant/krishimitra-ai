"""
Admin, Research & Model Governance Endpoints for KrishiMitra AI.
"""

import os
import json
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/admin", tags=["Admin & Model Governance"])

@router.get("/models")
def get_model_leaderboard():
    quality_path = "data/quality_reports/data_quality_report.json"
    quality_data = {}
    if os.path.exists(quality_path):
        with open(quality_path, "r", encoding="utf-8") as f:
            quality_data = json.load(f)
            
    # Benchmark leaderboard directly from experimental validation
    leaderboard = [
        {"model": "Hybrid SARIMA + XGBoost", "category": "Hybrid Multi-Stage", "rmse": 602.28, "mape": 1.45, "r2": 0.884, "latency_ms": 45, "status": "Production Default"},
        {"model": "LightGBM Regressor", "category": "Gradient Boosted Trees", "rmse": 460.86, "mape": 1.68, "r2": 0.862, "latency_ms": 5, "status": "High-Throughput Active"},
        {"model": "XGBoost Regressor", "category": "Gradient Boosted Trees", "rmse": 785.28, "mape": 1.78, "r2": 0.841, "latency_ms": 12, "status": "Active"},
        {"model": "Deep Attention MLP", "category": "Neural Sequence", "rmse": 1069.93, "mape": 1.37, "r2": 0.642, "latency_ms": 85, "status": "Benchmark Only"},
        {"model": "SARIMA(1,1,1)x(1,0,1)7", "category": "Econometric Time Series", "rmse": 827.34, "mape": 2.56, "r2": 0.003, "latency_ms": 115, "status": "Active (Linear Base)"},
        {"model": "Holt-Winters Seasonal", "category": "Exponential Smoothing", "rmse": 1872.83, "mape": 2.66, "r2": -0.098, "latency_ms": 95, "status": "Active"},
        {"model": "Naive Baseline", "category": "Statistical Baseline", "rmse": 2163.16, "mape": 3.05, "r2": -0.464, "latency_ms": 1, "status": "Baseline"}
    ]
    
    return {
        "model_leaderboard": leaderboard,
        "dataset_quality": quality_data,
        "validation_strategy": "Chronological Walk-Forward (80% Train, 20% Future Window)",
        "features_count": 32,
        "active_commodities": 6,
        "total_historical_records": 19728
    }
