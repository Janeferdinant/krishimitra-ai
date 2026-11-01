"""
Market Arbitrage and Decision Support Endpoints for KrishiMitra AI.
"""

from fastapi import APIRouter
from src.api.schemas import (
    MarketCompareRequest, 
    MarketCompareResponse, 
    AlertCheckRequest, 
    AlertCheckResponse
)
from src.decision_support.market_recommender import SpatialMarketRecommender
from src.decision_support.alert_engine import AlertEngine

router = APIRouter(prefix="/api/v1", tags=["Market Intelligence & Arbitrage"])

recommender = SpatialMarketRecommender()
alert_engine = AlertEngine()

@router.post("/markets/compare", response_model=MarketCompareResponse)
def compare_regional_markets(req: MarketCompareRequest):
    markets_ranked = recommender.recommend_best_market(
        origin_district=req.origin_district,
        commodity=req.commodity,
        quantity_quintals=req.quantity_quintals
    )
    
    best_market = markets_ranked[0]
    return MarketCompareResponse(
        origin_district=req.origin_district,
        commodity=req.commodity,
        quantity_quintals=req.quantity_quintals,
        markets=markets_ranked,
        best_market=best_market["market"],
        arbitrage_advice=best_market.get("arbitrage_advice", f"Best net realization at {best_market['market']}")
    )

@router.post("/alerts/check", response_model=AlertCheckResponse)
def check_price_alert(req: AlertCheckRequest):
    res = alert_engine.check_price_threshold(
        commodity=req.commodity,
        current_price=req.current_price,
        threshold_price=req.threshold_price,
        condition=req.condition
    )
    return AlertCheckResponse(**res)

