"""
Intelligent Crop Planning Module for KrishiMitra AI.
Assists farmers in identifying profitable and ecologically suitable crops
based on agro-climatic seasonality, input costs, price projections, and risk indices.
"""

# Authentic Kerala Crop Agronomic & Economic Profiles
CROP_AGRONOMIC_PROFILES = {
    "Banana": {
        "variety": "Nendran",
        "suitable_districts": ["Palakkad", "Thrissur", "Ernakulam", "Malappuram", "Wayanad"],
        "suitable_seasons": ["Southwest Monsoon", "Northeast Monsoon", "Year-Round"],
        "duration_months": 10,
        "yield_qtl_per_acre": 75.0,
        "cost_of_cultivation_per_acre": 95000.0,
        "base_harvest_price": 4100.0,
        "price_volatility": "High (CV 22.4%)",
        "water_requirement": "High"
    },
    "Black Pepper": {
        "variety": "Garbled / Panniyur-1",
        "suitable_districts": ["Wayanad", "Idukki", "Kannur", "Kottayam"],
        "suitable_seasons": ["Southwest Monsoon", "Year-Round"],
        "duration_months": 36,  # Perennial vine
        "yield_qtl_per_acre": 8.5,
        "cost_of_cultivation_per_acre": 65000.0,
        "base_harvest_price": 54500.0,
        "price_volatility": "Moderate (CV 14.1%)",
        "water_requirement": "Moderate"
    },
    "Arecanut": {
        "variety": "Chali / Mangala",
        "suitable_districts": ["Kasaragod", "Kozhikode", "Kannur", "Malappuram", "Palakkad"],
        "suitable_seasons": ["Southwest Monsoon", "Year-Round"],
        "duration_months": 48,  # Plantation crop
        "yield_qtl_per_acre": 12.0,
        "cost_of_cultivation_per_acre": 72000.0,
        "base_harvest_price": 42500.0,
        "price_volatility": "Moderate (CV 13.8%)",
        "water_requirement": "High"
    },
    "Copra": {
        "variety": "Milling Copra (West Coast Tall)",
        "suitable_districts": ["Kozhikode", "Alappuzha", "Thrissur", "Malappuram", "Kollam"],
        "suitable_seasons": ["Year-Round"],
        "duration_months": 60,
        "yield_qtl_per_acre": 18.0,
        "cost_of_cultivation_per_acre": 45000.0,
        "base_harvest_price": 11800.0,
        "price_volatility": "Low (CV 10.2%)",
        "water_requirement": "Moderate"
    },
    "Rubber": {
        "variety": "RSS-4 Sheet",
        "suitable_districts": ["Kottayam", "Pathanamthitta", "Ernakulam", "Kollam", "Palakkad"],
        "suitable_seasons": ["Southwest Monsoon", "Year-Round"],
        "duration_months": 72,
        "yield_qtl_per_acre": 15.0,
        "cost_of_cultivation_per_acre": 68000.0,
        "base_harvest_price": 18200.0,
        "price_volatility": "Low (CV 11.5%)",
        "water_requirement": "High"
    },
    "Cardamom": {
        "variety": "Small Green (7-8mm)",
        "suitable_districts": ["Idukki", "Wayanad", "Palakkad (High Ranges)"],
        "suitable_seasons": ["Southwest Monsoon", "Northeast Monsoon"],
        "duration_months": 36,
        "yield_qtl_per_acre": 2.2,
        "cost_of_cultivation_per_acre": 110000.0,
        "base_harvest_price": 198000.0,
        "price_volatility": "High (CV 24.8%)",
        "water_requirement": "High"
    }
}

class IntelligentCropPlanner:
    def __init__(self):
        self.profiles = CROP_AGRONOMIC_PROFILES

    def recommend_crops(
        self,
        district: str = "Palakkad",
        season: str = "Southwest Monsoon",
        land_area_acres: float = 2.0,
        risk_tolerance: str = "moderate"
    ) -> list[dict]:
        """
        Ranks candidate crops based on multi-criteria utility score:
        Score = 0.40 * NetMargin + 0.35 * AgroClimaticFit + 0.25 * RiskPenalty
        """
        recommendations = []
        
        for crop_name, p in self.profiles.items():
            # 1. District Suitability (1.0 or 0.4)
            district_match = 1.0 if district in p["suitable_districts"] else 0.4
            
            # 2. Season Suitability (1.0 or 0.5)
            season_match = 1.0 if (season in p["suitable_seasons"] or "Year-Round" in p["suitable_seasons"]) else 0.5
            agro_fit = 0.6 * district_match + 0.4 * season_match
            
            # 3. Economics (Projected Revenue & Margin)
            total_yield = p["yield_qtl_per_acre"] * land_area_acres
            gross_revenue = total_yield * p["base_harvest_price"]
            total_cost = p["cost_of_cultivation_per_acre"] * land_area_acres
            net_margin = gross_revenue - total_cost
            roi_pct = round((net_margin / (total_cost + 1e-5)) * 100.0, 1)
            
            # 4. Risk Factor
            risk_penalty = 0.0
            is_high_risk = "High" in p["price_volatility"]
            if risk_tolerance == "low" and is_high_risk:
                risk_penalty = 0.35
            elif risk_tolerance == "moderate" and is_high_risk:
                risk_penalty = 0.15
            elif risk_tolerance == "high":
                risk_penalty = 0.0
                
            # Composite Suitability Score (0 to 100 scale)
            margin_factor = min(max(roi_pct / 150.0, 0.1), 1.0)
            composite_score = round((0.45 * margin_factor + 0.35 * agro_fit - 0.20 * risk_penalty) * 100.0, 1)
            composite_score = max(composite_score, 10.0)
            
            recommendations.append({
                "commodity": crop_name,
                "variety": p["variety"],
                "suitability_score": composite_score,
                "expected_gross_revenue_inr": round(gross_revenue, 2),
                "estimated_cultivation_cost_inr": round(total_cost, 2),
                "expected_net_margin_inr": round(net_margin, 2),
                "roi_percentage": roi_pct,
                "projected_yield_qtl": round(total_yield, 2),
                "projected_price_per_qtl": p["base_harvest_price"],
                "risk_level": "High Risk" if is_high_risk else "Moderate / Stable",
                "water_need": p["water_requirement"],
                "disclaimer": "Projections represent estimated market scenarios based on historical cycles; not a guaranteed financial return."
            })
            
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        return recommendations

