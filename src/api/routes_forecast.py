"""
Forecast & Explainability Endpoints for KrishiMitra AI.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    ForecastRequest, 
    ForecastResponse, 
    ExplainabilityRequest, 
    ExplainabilityResponse
)
from src.models.ml_models import MLForecastingSuite
from src.models.hybrid_models import HybridSarimaXGBoostModel
from src.models.explainability import AgriculturalShapExplainer

router = APIRouter(prefix="/api/v1", tags=["Forecasting & Intelligence"])

DATA_PATH = "data/processed/analytical_features_dataset.csv"
_cached_df = None
_cached_ml_suites = {}
_cached_hybrids = {}

def get_data() -> pd.DataFrame:
    global _cached_df
    if _cached_df is None:
        if os.path.exists(DATA_PATH):
            _cached_df = pd.read_csv(DATA_PATH)
        else:
            raise HTTPException(status_code=500, detail="Analytical dataset not found. Please run data pipeline.")
    return _cached_df

@router.get("/meta/commodities")
def get_metadata():
    df = get_data()
    commodities = sorted(df["commodity"].unique().tolist())
    districts = sorted(df["district"].unique().tolist())
    markets = sorted(df["market"].unique().tolist())
    
    mapping = {}
    for c in commodities:
        c_sub = df[df["commodity"] == c]
        mapping[c] = {
            "districts": sorted(c_sub["district"].unique().tolist()),
            "markets": sorted(c_sub["market"].unique().tolist()),
            "latest_modal_price": round(float(c_sub.sort_values("date")["modal_price"].iloc[-1]), 2),
            "unit": "₹/Quintal"
        }
        
    return {
        "commodities": commodities,
        "districts": districts,
        "markets": markets,
        "commodity_details": mapping,
        "seasons": ["Southwest Monsoon", "Northeast Monsoon", "Summer / Pre-Monsoon", "Winter / Post-Monsoon"]
    }

@router.post("/forecast", response_model=ForecastResponse)
def generate_forecast(req: ForecastRequest):
    df = get_data()
    sub = df[(df["commodity"] == req.commodity) & (df["market"] == req.market)].sort_values("date").reset_index(drop=True)
    
    if len(sub) == 0:
        # Fallback to commodity group if market not exact
        sub = df[df["commodity"] == req.commodity].sort_values("date").reset_index(drop=True)
        if len(sub) == 0:
            raise HTTPException(status_code=404, detail=f"No observations found for commodity '{req.commodity}'")
            
    latest_row = sub.iloc[-1]
    current_price = round(float(latest_row["modal_price"]), 2)
    last_date = pd.to_datetime(latest_row["date"])
    
    forecast_dates = [(last_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, req.horizon_days + 1)]
    
    feature_cols = [c for c in sub.columns if "lag" in c or "rolling" in c or "ema" in c or "sin" in c or "cos" in c]
    
    # Train or retrieve model
    key = f"{req.commodity}_{req.market}"
    if key not in _cached_ml_suites:
        suite = MLForecastingSuite()
        suite.fit_all(sub, feature_cols=feature_cols)
        _cached_ml_suites[key] = suite
    suite = _cached_ml_suites[key]
    
    # Synthesize multi-step ahead projections
    # Start with last row features, simulate day-by-day progression
    sim_row = latest_row.copy()
    preds = []
    
    running_price = current_price
    for step in range(req.horizon_days):
        # Update lag 1 with running prediction
        sim_row["price_lag_1"] = running_price
        eval_df = pd.DataFrame([sim_row[feature_cols]])
        step_preds, _ = suite.predict("xgboost" if req.model_type == "hybrid" else req.model_type, eval_df)
        running_price = float(step_preds[0])
        preds.append(running_price)
        
    preds = np.array(preds)
    
    # Calibrated confidence intervals based on residual uncertainty
    std_factor = suite.residual_std.get("xgboost", current_price * 0.035)
    horizon_scale = np.sqrt(np.arange(1, req.horizon_days + 1)) / np.sqrt(1)
    
    ci_80_half = 1.282 * std_factor * horizon_scale
    ci_95_half = 1.960 * std_factor * horizon_scale
    
    c80_lower = np.maximum(preds - ci_80_half, 10.0).round(2).tolist()
    c80_upper = (preds + ci_80_half).round(2).tolist()
    c95_lower = np.maximum(preds - ci_95_half, 10.0).round(2).tolist()
    c95_upper = (preds + ci_95_half).round(2).tolist()
    
    pred_list = [round(float(p), 2) for p in preds]
    price_change = pred_list[-1] - current_price
    trend_str = "upward" if price_change > 0 else "downward"
    advisory = f"{req.commodity} in {req.market} is projected to trend {trend_str} by ₹{abs(price_change):,.0f}/Qtl ({abs(price_change)/current_price*100:.1f}%) over the next {req.horizon_days} days."
    
    return ForecastResponse(
        commodity=req.commodity,
        market=req.market,
        district=req.district or str(latest_row.get("district", "Kerala")),
        model_used=req.model_type.upper(),
        current_price=current_price,
        forecast_dates=forecast_dates,
        predicted_prices=pred_list,
        confidence_80_lower=c80_lower,
        confidence_80_upper=c80_upper,
        confidence_95_lower=c95_lower,
        confidence_95_upper=c95_upper,
        advisory_summary=advisory
    )

@router.post("/explainability/shap", response_model=ExplainabilityResponse)
def explain_prediction(req: ExplainabilityRequest):
    df = get_data()
    sub = df[(df["commodity"] == req.commodity) & (df["market"] == req.market)].sort_values("date")
    if len(sub) == 0:
        sub = df[df["commodity"] == req.commodity].sort_values("date")
        if len(sub) == 0:
            raise HTTPException(status_code=404, detail=f"No data for {req.commodity}")
            
    latest_row = sub.iloc[-1]
    feature_cols = [c for c in sub.columns if "lag" in c or "rolling" in c or "ema" in c or "sin" in c or "cos" in c]
    
    key = f"{req.commodity}_{req.market}"
    if key not in _cached_ml_suites:
        suite = MLForecastingSuite()
        suite.fit_all(sub, feature_cols=feature_cols)
        _cached_ml_suites[key] = suite
    suite = _cached_ml_suites[key]
    
    explainer = AgriculturalShapExplainer(suite.models["xgboost"], feature_cols)
    res = explainer.explain_instance(latest_row)
    
    return ExplainabilityResponse(
        commodity=req.commodity,
        market=req.market,
        feature_contributions=res["feature_contributions"],
        natural_language_advisory=res["natural_language_advisory"]
    )

