"""
Pydantic Schemas for KrishiMitra AI REST API.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal

class ForecastRequest(BaseModel):
    commodity: str = Field(..., example="Arecanut")
    market: str = Field(..., example="Vatakara APMC")
    district: Optional[str] = Field("Kozhikode", example="Kozhikode")
    horizon_days: int = Field(15, ge=1, le=60, example=15)
    model_type: Literal["hybrid", "xgboost", "lightgbm", "sarima", "mlp"] = "hybrid"

class ForecastResponse(BaseModel):
    commodity: str
    market: str
    district: str
    model_used: str
    current_price: float
    forecast_dates: list[str]
    predicted_prices: list[float]
    confidence_80_lower: list[float]
    confidence_80_upper: list[float]
    confidence_95_lower: list[float]
    confidence_95_upper: list[float]
    unit: str = "INR per Quintal (100 kg)"
    advisory_summary: str

class MarketCompareRequest(BaseModel):
    origin_district: str = Field(..., example="Wayanad")
    commodity: str = Field(..., example="Black Pepper")
    quantity_quintals: float = Field(10.0, gt=0, example=10.0)

class MarketCompareResponse(BaseModel):
    origin_district: str
    commodity: str
    quantity_quintals: float
    markets: list[dict]
    best_market: str
    arbitrage_advice: str

class CropPlanRequest(BaseModel):
    district: str = Field(..., example="Palakkad")
    season: str = Field("Southwest Monsoon", example="Southwest Monsoon")
    land_area_acres: float = Field(2.5, gt=0, example=2.5)
    risk_tolerance: Literal["low", "moderate", "high"] = "moderate"

class CropPlanResponse(BaseModel):
    district: str
    season: str
    land_area_acres: float
    recommendations: list[dict]

class ExplainabilityRequest(BaseModel):
    commodity: str = Field(..., example="Banana")
    market: str = Field(..., example="Palakkad APMC")

class ExplainabilityResponse(BaseModel):
    commodity: str
    market: str
    feature_contributions: list[dict]
    natural_language_advisory: str

class AlertCheckRequest(BaseModel):
    commodity: str
    current_price: float
    threshold_price: float
    condition: Literal["above", "below"] = "above"

class AlertCheckResponse(BaseModel):
    commodity: str
    current_price: float
    threshold_price: float
    condition: str
    triggered: bool
    message: str
