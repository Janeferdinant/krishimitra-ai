import os
import json
import pandas as pd
import pytest

def test_data_pipeline_outputs_and_quality():
    from src.data_pipeline.acquisition import acquire_market_and_weather_data
    from src.data_pipeline.preprocessing import preprocess_market_data
    
    # 1. Test data acquisition
    raw_df, source_meta = acquire_market_and_weather_data(output_dir="data/raw")
    assert isinstance(raw_df, pd.DataFrame), "Raw data must be a pandas DataFrame"
    assert len(raw_df) > 5000, f"Raw data should have substantial records, got {len(raw_df)}"
    
    required_cols = [
        "date", "state", "district", "market", "commodity", "variety",
        "arrivals_tonnes", "min_price", "max_price", "modal_price",
        "temp_mean", "temp_max", "temp_min", "rainfall_mm", "rel_humidity_pct"
    ]
    for col in required_cols:
        assert col in raw_df.columns, f"Missing required column: {col}"
        
    # Check source register exists
    source_reg_path = os.path.join("data", "raw", "sources_register.json")
    assert os.path.exists(source_reg_path), "sources_register.json must exist"
    with open(source_reg_path, "r", encoding="utf-8") as f:
        sources = json.load(f)
    assert "agmarknet" in sources
    assert "nasa_power_imd" in sources
    
    # 2. Test preprocessing
    cleaned_df, quality_report = preprocess_market_data(
        raw_df, 
        output_dir="data/processed",
        reports_dir="data/quality_reports"
    )
    
    assert isinstance(cleaned_df, pd.DataFrame)
    assert len(cleaned_df) > 0
    # No nulls in critical target column
    assert cleaned_df["modal_price"].isnull().sum() == 0, "No missing values allowed in modal_price after preprocessing"
    # Ensure all prices are positive
    assert (cleaned_df["modal_price"] > 0).all(), "All modal prices must be strictly positive"
    assert (cleaned_df["max_price"] >= cleaned_df["min_price"]).all(), "max_price must be >= min_price"
    
    # Verify outputs on disk
    cleaned_path = os.path.join("data", "processed", "cleaned_agricultural_market_dataset.csv")
    assert os.path.exists(cleaned_path), f"Cleaned dataset missing at {cleaned_path}"
    
    dict_path = os.path.join("data", "processed", "data_dictionary.json")
    assert os.path.exists(dict_path), f"Data dictionary missing at {dict_path}"
    
    report_path = os.path.join("data", "quality_reports", "data_quality_report.json")
    assert os.path.exists(report_path), f"Data quality report missing at {report_path}"
    
    outlier_path = os.path.join("data", "quality_reports", "outlier_analysis.json")
    assert os.path.exists(outlier_path), f"Outlier report missing at {outlier_path}"

