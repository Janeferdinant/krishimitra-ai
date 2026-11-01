"""
Alerts and Notification Engine for KrishiMitra AI.
Monitors price threshold crossings, optimal selling windows, and market volatility triggers.
"""

import numpy as np

class AlertEngine:
    def __init__(self):
        self.active_alerts = []

    def check_price_threshold(
        self,
        commodity: str,
        current_price: float,
        threshold_price: float,
        condition: str = "above"
    ) -> dict:
        """
        Evaluates whether a current or predicted price crosses a user-defined threshold.
        """
        condition = condition.lower()
        triggered = False
        
        if condition == "above" and current_price >= threshold_price:
            triggered = True
            msg = f"Alert: {commodity} market price (₹{current_price:,.0f}/Qtl) has Crossed Above target threshold ₹{threshold_price:,.0f}/Qtl."
        elif condition == "below" and current_price <= threshold_price:
            triggered = True
            msg = f"Alert: {commodity} market price (₹{current_price:,.0f}/Qtl) has Crossed Below floor threshold ₹{threshold_price:,.0f}/Qtl."
        else:
            msg = f"Normal: {commodity} trading at ₹{current_price:,.0f}/Qtl (Threshold: ₹{threshold_price:,.0f}/Qtl {condition})."
            
        return {
            "commodity": commodity,
            "current_price": current_price,
            "threshold_price": threshold_price,
            "condition": condition,
            "triggered": triggered,
            "message": msg
        }

    def evaluate_selling_window(
        self,
        commodity: str,
        forecast_series: list[float],
        storage_cost_per_day: float = 3.5
    ) -> dict:
        """
        Evaluates upcoming price trajectory to advise whether to SELL IMMEDIATELY or HOLD for peak window.
        Takes holding/storage cost into account.
        """
        prices = np.array(forecast_series, dtype=float)
        current_p = prices[0]
        
        # Net returns adjusted for daily storage cost
        days = np.arange(len(prices))
        net_prices = prices - (days * storage_cost_per_day)
        
        best_day = int(np.argmax(net_prices))
        max_net_p = float(net_prices[best_day])
        
        gain_potential = max_net_p - current_p
        
        if best_day > 0 and gain_potential > (current_p * 0.02):
            recommendation = "HOLD"
            action_text = f"Recommendation: HOLD produce for ~{best_day} days. Projected net gain of +₹{gain_potential:,.0f}/Qtl at peak window."
        else:
            recommendation = "SELL"
            action_text = f"Recommendation: SELL NOW. Prices are at or near peak; delayed sales risk storage cost loss."
            
        return {
            "commodity": commodity,
            "current_price": round(current_p, 2),
            "peak_forecast_price": round(float(prices[best_day]), 2),
            "optimal_day": best_day,
            "recommendation": recommendation,
            "expected_gain_inr_per_qtl": round(gain_potential, 2),
            "advisory": action_text
        }

