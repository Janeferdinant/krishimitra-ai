import pytest
from fastapi.testclient import TestClient

def test_fastapi_endpoints():
    from src.api.main import app
    client = TestClient(app)
    
    # 1. Health check
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "KrishiMitra AI" in data["app_name"]
    
    # 2. Metadata
    res = client.get("/api/v1/meta/commodities")
    assert res.status_code == 200
    meta = res.json()
    assert "commodities" in meta
    assert "Arecanut" in meta["commodities"]
    assert "Black Pepper" in meta["commodities"]
    
    # 3. Forecast endpoint
    forecast_req = {
        "commodity": "Arecanut",
        "market": "Vatakara APMC",
        "district": "Kozhikode",
        "horizon_days": 15,
        "model_type": "hybrid"
    }
    res = client.post("/api/v1/forecast", json=forecast_req)
    assert res.status_code == 200
    fc = res.json()
    assert "forecast_dates" in fc
    assert "predicted_prices" in fc
    assert len(fc["predicted_prices"]) == 15
    assert "confidence_80_lower" in fc
    assert "confidence_80_upper" in fc
    assert "current_price" in fc
    
    # 4. Market Arbitrage endpoint
    market_req = {
        "origin_district": "Wayanad",
        "commodity": "Black Pepper",
        "quantity_quintals": 12.0
    }
    res = client.post("/api/v1/markets/compare", json=market_req)
    assert res.status_code == 200
    m_data = res.json()
    assert "markets" in m_data
    assert len(m_data["markets"]) >= 2
    assert "best_market" in m_data
    
    # 5. Crop Planning endpoint
    plan_req = {
        "district": "Palakkad",
        "season": "Southwest Monsoon",
        "land_area_acres": 3.0,
        "risk_tolerance": "moderate"
    }
    res = client.post("/api/v1/planning/recommend", json=plan_req)
    assert res.status_code == 200
    plans = res.json()
    assert "recommendations" in plans
    assert len(plans["recommendations"]) > 0
    
    # 6. Explainability endpoint
    xai_req = {
        "commodity": "Banana",
        "market": "Palakkad APMC"
    }
    res = client.post("/api/v1/explainability/shap", json=xai_req)
    assert res.status_code == 200
    xai = res.json()
    assert "feature_contributions" in xai
    assert "natural_language_advisory" in xai
    
    # 7. Admin endpoint
    res = client.get("/api/v1/admin/models")
    assert res.status_code == 200
    admin = res.json()
    assert "model_leaderboard" in admin

