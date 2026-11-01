import os
import pytest

def test_ieee_paper_and_experimental_reports():
    paper_md = os.path.join("docs", "paper", "ieee_paper.md")
    paper_tex = os.path.join("docs", "paper", "ieee_paper.tex")
    exp_report = os.path.join("docs", "reports", "experimental_analysis_report.md")
    
    assert os.path.exists(paper_md), f"IEEE Markdown paper missing at {paper_md}"
    assert os.path.exists(paper_tex), f"IEEE LaTeX paper missing at {paper_tex}"
    assert os.path.exists(exp_report), f"Experimental analysis report missing at {exp_report}"
    
    with open(paper_md, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    # Check for all 22 required sections
    required_sections = [
        "Abstract", "Keywords", "Introduction", "Problem Definition",
        "Related Work", "Research Gap", "Objectives and Contributions",
        "Dataset Description", "Proposed Methodology", "Data Preprocessing",
        "Exploratory Data Analysis", "Feature Engineering and Selection",
        "Model Architecture", "Experimental Setup", "Performance Evaluation",
        "Comparative Analysis", "Explainability", "Discussion",
        "Limitations", "Conclusion", "Future Work", "References"
    ]
    for sec in required_sections:
        assert sec.lower() in md_text.lower(), f"Missing required section: {sec}"
        
    # Check for mathematical formulation
    assert "\\text{SARIMA}" in md_text or "SARIMA" in md_text
    assert "Shapley" in md_text or "SHAP" in md_text
    assert "\\phi_i" in md_text or "phi_i" in md_text or "marginal contribution" in md_text.lower()
    
    # Check 10 experiments in experimental report
    with open(exp_report, "r", encoding="utf-8") as f:
        exp_text = f.read()
    for i in range(1, 11):
        assert f"Experiment {i}" in exp_text or f"Experiment {i}:" in exp_text, f"Missing Experiment {i} in experimental analysis report"
