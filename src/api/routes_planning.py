"""
Crop Planning Endpoints for KrishiMitra AI.
"""

from fastapi import APIRouter
from src.api.schemas import CropPlanRequest, CropPlanResponse
from src.decision_support.crop_planner import IntelligentCropPlanner

router = APIRouter(prefix="/api/v1", tags=["Intelligent Crop Planning"])

planner = IntelligentCropPlanner()

@router.post("/planning/recommend", response_model=CropPlanResponse)
def plan_crops(req: CropPlanRequest):
    recs = planner.recommend_crops(
        district=req.district,
        season=req.season,
        land_area_acres=req.land_area_acres,
        risk_tolerance=req.risk_tolerance
    )
    return CropPlanResponse(
        district=req.district,
        season=req.season,
        land_area_acres=req.land_area_acres,
        recommendations=recs
    )
