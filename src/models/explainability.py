"""
Explainable AI (XAI) Module for KrishiMitra AI.
Implements SHAP feature attribution and translates mathematical Shapley values
into actionable, farmer-friendly natural language advisories.
"""

import numpy as np
import pandas as pd
import shap

class AgriculturalShapExplainer:
    def __init__(self, model, feature_names: list[str]):
        self.model = model
        self.feature_names = feature_names
        try:
            self.explainer = shap.TreeExplainer(model)
        except Exception:
            self.explainer = shap.Explainer(model)

    def explain_instance(self, row: pd.Series or pd.DataFrame) -> dict:
        """
        Computes SHAP attribution for a single observation and generates natural language guidance.
        """
        if isinstance(row, pd.Series):
            X_df = pd.DataFrame([row[self.feature_names]])
        else:
            X_df = row[self.feature_names]
            
        shap_values = self.explainer(X_df)
        values = shap_values.values[0]
        
        # Sort features by absolute contribution
        feat_contribs = []
        for name, val, raw_val in zip(self.feature_names, values, X_df.values[0]):
            feat_contribs.append({
                "feature": name,
                "shap_value": round(float(val), 2),
                "raw_value": round(float(raw_val), 2),
                "direction": "positive" if val > 0 else "negative"
            })
            
        feat_contribs.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        top_factors = feat_contribs[:5]
        
        # Translate to natural language advisory
        advisory_text = self._synthesize_advisory(top_factors, row)
        
        return {
            "feature_contributions": top_factors,
            "natural_language_advisory": advisory_text
        }

    def _synthesize_advisory(self, top_factors: list[dict], row) -> str:
        sentences = []
        commodity = row.get("commodity", "Crop")
        market = row.get("market", "market")
        
        sentences.append(f"Forecasting insights for {commodity} in {market}:")
        
        for f in top_factors[:3]:
            fname = f["feature"]
            direction = "supporting higher prices" if f["direction"] == "positive" else "putting downward pressure on prices"
            impact_amt = abs(f["shap_value"])
            
            if "lag_1" in fname or "ema_7" in fname:
                sentences.append(f"• Recent price momentum is {direction} (contribution: ±₹{impact_amt:,.0f}/Qtl).")
            elif "arrival" in fname:
                sentences.append(f"• Mandi arrival volume trends are {direction} due to prevailing supply flows (impact: ±₹{impact_amt:,.0f}/Qtl).")
            elif "rainfall" in fname:
                sentences.append(f"• Regional rainfall patterns are {direction} by affecting transit and drying operations (impact: ±₹{impact_amt:,.0f}/Qtl).")
            elif "onam" in fname or "festival" in fname:
                sentences.append(f"• Seasonal festival demand is {direction} across retail and wholesale channels (impact: ±₹{impact_amt:,.0f}/Qtl).")
            elif "harvest" in fname or "month" in fname:
                sentences.append(f"• Annual harvest seasonality is {direction} (impact: ±₹{impact_amt:,.0f}/Qtl).")
            else:
                sentences.append(f"• {fname} is {direction} (impact: ±₹{impact_amt:,.0f}/Qtl).")
                
        sentences.append("Farmer Recommendation: Monitor nearby mandis and consider favorable selling windows when arrivals dip.")
        return "\n".join(sentences)

