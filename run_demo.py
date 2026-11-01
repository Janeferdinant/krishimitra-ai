"""
Top-Level Demonstration & Launch Script for KrishiMitra AI.
Kerala Young Innovators Programme (YIP 9.0).
Executes pipeline checks and boots the web server & interactive dashboard.
"""

import os
import sys
import webbrowser
import uvicorn
import pandas as pd

def check_and_prepare_artifacts():
    print("=" * 75)
    print("       KRISHIMITRA AI - AGRICULTURAL MARKET INTELLIGENCE PLATFORM       ")
    print("              Kerala Young Innovators Programme (YIP 9.0)               ")
    print("=" * 75)
    
    # 1. Check Cleaned Data
    data_path = os.path.join("data", "processed", "analytical_features_dataset.csv")
    if not os.path.exists(data_path):
        print("[*] Generating authentic agricultural and meteorological dataset...")
        from src.data_pipeline.acquisition import acquire_market_and_weather_data
        from src.data_pipeline.preprocessing import preprocess_market_data
        from src.data_pipeline.feature_engineering import generate_features
        
        raw, _ = acquire_market_and_weather_data()
        cleaned, _ = preprocess_market_data(raw)
        generate_features(cleaned)
        print("[+] Analytical features dataset prepared successfully.")
    else:
        df = pd.read_csv(data_path)
        print(f"[+] Found preprocessed analytical dataset: {len(df):,} records across {df['commodity'].nunique()} commodities.")

    # 2. Check Presentation Deck
    pptx_path = os.path.join("docs", "presentation", "KrishiMitra_AI_YIP_Presentation.pptx")
    if not os.path.exists(pptx_path):
        print("[*] Generating 20-slide PowerPoint research presentation...")
        from docs.presentation.generate_pptx import create_presentation
        create_presentation(pptx_path)
        print("[+] PowerPoint generated.")
    else:
        print(f"[+] Found PowerPoint research deck: {pptx_path}")

    # 3. Print Deliverables Manifest
    print("\n[+] DELIVERABLES MANIFEST:")
    print("  • Deliverable 1: Complete Source Code Repository (Modular Architecture)")
    print("  • Deliverable 2: Research Dataset Repository (19,728 Daily Records)")
    print("  • Deliverable 3: Complete EDA Report (docs/reports/eda_report.md)")
    print("  • Deliverable 4: Model Evaluation Report (docs/reports/model_evaluation_report.md)")
    print("  • Deliverable 5: Full IEEE Research Paper (docs/paper/ieee_paper.md & .tex)")
    print("  • Deliverable 6: 20-Slide Research Presentation (.pptx & presentation.html)")
    print("  • Deliverable 7: Production Interactive Web Application & REST APIs")
    print("\n[*] Starting FastAPI Server on http://localhost:8000 ...")
    print("    -> Interactive Web Dashboard : http://localhost:8000/")
    print("    -> OpenAPI REST Documentation: http://localhost:8000/docs")
    print("    -> Research Presentation Deck: file://" + os.path.abspath("docs/presentation/presentation.html"))
    print("=" * 75)

if __name__ == "__main__":
    check_and_prepare_artifacts()
    try:
        uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\n[!] KrishiMitra AI server stopped gracefully.")

