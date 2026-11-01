import pytest

def test_decision_support_suite():
    from src.decision_support.crop_planner import IntelligentCropPlanner
    from src.decision_support.market_recommender import SpatialMarketRecommender
    from src.decision_support.alert_engine import AlertEngine
    
    # 1. Test Crop Planner
    planner = IntelligentCropPlanner()
    recommendations = planner.recommend_crops(
        district="Palakkad",
        season="Southwest Monsoon",
        land_area_acres=2.5,
        risk_tolerance="moderate"
    )
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    top_crop = recommendations[0]
    assert "commodity" in top_crop
    assert "suitability_score" in top_crop
    assert "expected_net_margin_inr" in top_crop
    assert "risk_level" in top_crop
    assert top_crop["suitability_score"] > 0
    
    # 2. Test Market Recommender
    recommender = SpatialMarketRecommender()
    market_comparisons = recommender.recommend_best_market(
        origin_district="Wayanad",
        commodity="Black Pepper",
        quantity_quintals=15.0
    )
    assert isinstance(market_comparisons, list)
    assert len(market_comparisons) >= 2
    best = market_comparisons[0]
    assert "market" in best
    assert "predicted_price" in best
    assert "logistics_cost_per_qtl" in best
    assert "net_realization_per_qtl" in best
    assert best["net_realization_per_qtl"] == best["predicted_price"] - best["logistics_cost_per_qtl"]
    
    # 3. Test Alert Engine
    alerts = AlertEngine()
    # Test threshold alert
    alert_res = alerts.check_price_threshold(
        commodity="Arecanut",
        current_price=43500.0,
        threshold_price=42000.0,
        condition="above"
    )
    assert alert_res["triggered"] is True
    assert "Crossed" in alert_res["message"]
    
    # Test selling window advisory
    window_res = alerts.evaluate_selling_window(
        commodity="Banana",
        forecast_series=[3800, 3950, 4200, 4400, 4600]
    )
    assert window_res["recommendation"] == "HOLD"
    assert window_res["optimal_day"] == 4

