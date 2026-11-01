import os
import json
import pytest
import pandas as pd

def test_eda_engine_and_diagnostics():
    from src.data_pipeline.eda_engine import run_eda_diagnostics
    
    cleaned_path = os.path.join("data", "processed", "cleaned_agricultural_market_dataset.csv")
    assert os.path.exists(cleaned_path), "Preprocessed data required for EDA"
    
    df = pd.read_csv(cleaned_path)
    eda_results = run_eda_diagnostics(df, figures_dir="artifacts/figures", report_path="docs/reports/eda_report.md")
    
    assert isinstance(eda_results, dict)
    assert "stationarity_tests" in eda_results
    assert "correlation_matrix" in eda_results
    assert "price_volatility" in eda_results
    
    # Check ADF test output structure
    for commodity in ["Arecanut", "Black Pepper", "Banana"]:
        assert commodity in eda_results["stationarity_tests"]
        stat_res = eda_results["stationarity_tests"][commodity]
        assert "adf_statistic" in stat_res
        assert "p_value" in stat_res
        assert "is_stationary" in stat_res
        
    # Check figure artifacts exist
    expected_figures = [
        "eda_price_trends.png",
        "seasonal_decomposition.png",
        "arrival_price_elasticity.png",
        "correlation_heatmap.png",
        "market_price_distribution.png"
    ]
    for fig in expected_figures:
        fig_path = os.path.join("artifacts", "figures", fig)
        assert os.path.exists(fig_path), f"Figure missing: {fig_path}"
        
    # Check report exists and is substantial
    report_file = os.path.join("docs", "reports", "eda_report.md")
    assert os.path.exists(report_file)
    with open(report_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 2000, "EDA report should be comprehensive and detailed"
    assert "Augmented Dickey-Fuller" in content
    assert "Elasticity" in content

