"""
Spatial Market Recommender & Arbitrage Optimizer for KrishiMitra AI.
Calculates net farm-gate price realization across regional mandis
by factoring in road transit distances, freight rates, and predicted market prices.
"""

# Distance matrix (km) between origin districts and key terminal/regional markets
MANDI_DISTANCE_REGISTRY = {
    "Palakkad": {
        "Palakkad APMC": 8,
        "Thrissur APMC": 68,
        "Kochi Terminal Yard": 142,
        "Pollachi APMC (TN)": 45,
        "Coimbatore APMC (TN)": 54
    },
    "Wayanad": {
        "Sulthan Bathery Mandi": 12,
        "Kalpetta Market": 24,
        "Kozhikode Main Yard": 85,
        "Kochi Terminal Yard": 245,
        "Mysuru APMC (KA)": 115
    },
    "Idukki": {
        "Nedumkandam Spices Market": 10,
        "Vandanmedu Yard": 22,
        "Kochi Terminal Yard": 135,
        "Bodinaickanur Mandi (TN)": 48
    },
    "Kozhikode": {
        "Kozhikode Main": 6,
        "Vatakara APMC": 48,
        "Kannur APMC": 88,
        "Kochi Terminal Yard": 185
    },
    "Kottayam": {
        "Kottayam Rubber Yard": 5,
        "Kochi Terminal Yard": 62,
        "Alappuzha Main Yard": 46,
        "Pathanamthitta APMC": 58
    },
    "Kasaragod": {
        "Kasaragod Mandi": 8,
        "Kanhangad APMC": 28,
        "Mangaluru APMC (KA)": 52,
        "Kannur APMC": 95
    }
}

# Baseline mandi price offsets relative to state average (due to terminal buyer competition)
MARKET_PRICE_OFFSETS = {
    "Kochi Terminal Yard": 1.045,          # Major export terminal hub (+4.5% premium)
    "Bodinaickanur Mandi (TN)": 1.038,     # Major national cardamom auction center
    "Pollachi APMC (TN)": 1.025,           # Major copra/coconut oil milling cluster
    "Vatakara APMC": 1.030,                # High demand arecanut terminal
    "Thrissur APMC": 1.015,
    "Palakkad APMC": 1.000,
    "Sulthan Bathery Mandi": 0.985,
    "Nedumkandam Spices Market": 1.010,
    "Kottayam Rubber Yard": 1.020,
    "Kasaragod Mandi": 0.995,
    "Kozhikode Main": 1.010
}

COMMODITY_BASE_PRICES = {
    "Arecanut": 42000.0,
    "Black Pepper": 54000.0,
    "Copra": 11500.0,
    "Banana": 3850.0,
    "Rubber": 17800.0,
    "Cardamom": 195000.0
}

class SpatialMarketRecommender:
    def __init__(self, freight_rate_per_km_tonne: float = 6.5, handling_cost_per_qtl: float = 45.0):
        self.freight_rate = freight_rate_per_km_tonne
        self.handling_cost = handling_cost_per_qtl

    def recommend_best_market(
        self,
        origin_district: str = "Wayanad",
        commodity: str = "Black Pepper",
        quantity_quintals: float = 10.0
    ) -> list[dict]:
        """
        Evaluates reachable mandis and ranks by net realization:
        Net Price (₹/Qtl) = Predicted Market Price - Logistics Cost Per Qtl
        """
        distances = MANDI_DISTANCE_REGISTRY.get(origin_district, MANDI_DISTANCE_REGISTRY["Palakkad"])
        base_price = COMMODITY_BASE_PRICES.get(commodity, 15000.0)
        
        results = []
        quantity_tonnes = max(quantity_quintals / 10.0, 0.1)
        
        for market_name, dist_km in distances.items():
            price_mult = MARKET_PRICE_OFFSETS.get(market_name, 1.0)
            pred_price = round(base_price * price_mult, 2)
            
            # Transport cost calculation
            # Total transport INR = distance_km * freight_per_km_tonne * quantity_tonnes + (handling * qty_qtl)
            total_freight_inr = dist_km * self.freight_rate * quantity_tonnes
            total_handling_inr = self.handling_cost * quantity_quintals
            total_logistics_inr = total_freight_inr + total_handling_inr
            logistics_per_qtl = round(total_logistics_inr / quantity_quintals, 2)
            
            net_realization_per_qtl = round(pred_price - logistics_per_qtl, 2)
            net_total_revenue = round(net_realization_per_qtl * quantity_quintals, 2)
            
            results.append({
                "market": market_name,
                "distance_km": dist_km,
                "predicted_price": pred_price,
                "logistics_cost_per_qtl": logistics_per_qtl,
                "net_realization_per_qtl": net_realization_per_qtl,
                "net_total_revenue_inr": net_total_revenue,
                "is_arbitrage_profitable": False
            })
            
        # Sort descending by net price realization
        results.sort(key=lambda x: x["net_realization_per_qtl"], reverse=True)
        
        # Mark top market as recommended and check arbitrage
        local_market = min(results, key=lambda x: x["distance_km"])
        best_market = results[0]
        
        arbitrage_gain = round(best_market["net_realization_per_qtl"] - local_market["net_realization_per_qtl"], 2)
        if arbitrage_gain > 50.0 and best_market["market"] != local_market["market"]:
            best_market["is_arbitrage_profitable"] = True
            best_market["arbitrage_gain_per_qtl"] = arbitrage_gain
            best_market["arbitrage_advice"] = f"Recommended: Transport to {best_market['market']} yields net extra ₹{arbitrage_gain:,.0f}/Qtl after deducting ₹{best_market['logistics_cost_per_qtl']:.0f} transport cost."
        else:
            best_market["arbitrage_gain_per_qtl"] = 0.0
            best_market["arbitrage_advice"] = f"Sell locally at {local_market['market']}: Distance transit cost exceeds price premium."
            
        return results
