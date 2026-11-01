import os
import re
import pytest

def test_literature_review_matrix_exists_and_meets_standards():
    matrix_path = os.path.join("docs", "literature_review", "literature_review_matrix.md")
    assert os.path.exists(matrix_path), f"Literature review matrix not found at {matrix_path}"
    
    with open(matrix_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for canvas references
    assert "Sabu" in content and "Manoj Kumar" in content, "Procedia CS paper (Arecanuts in Kerala) must be present"
    assert "Arecanut" in content or "arecanut" in content
    assert "Garbled Black Pepper" in content or "Black Pepper" in content
    assert "TNAU" in content or "Tamil Nadu Agricultural University" in content
    assert "UAS Bangalore" in content or "University of Agricultural Sciences, Bangalore" in content
    
    # Count verified papers in the table (rows starting with | [0-9]+ |)
    rows = re.findall(r"^\|\s*\d+\s*\|", content, re.MULTILINE)
    assert len(rows) >= 28, f"Literature review matrix should contain at least 28 papers, found {len(rows)}"
    
    # Check for high-impact journals
    high_impact_journals = [
        "Computers and Electronics in Agriculture",
        "Expert Systems with Applications",
        "Applied Soft Computing",
        "IEEE",
        "International Journal of Forecasting"
    ]
    for journal in high_impact_journals:
        assert journal.lower() in content.lower(), f"Expected high-impact journal '{journal}' in literature review"
        
    # Check for research gap analysis
    gap_path = os.path.join("docs", "literature_review", "research_gap_analysis.md")
    assert os.path.exists(gap_path), f"Research gap analysis not found at {gap_path}"
    with open(gap_path, "r", encoding="utf-8") as f:
        gap_content = f.read()
    assert len(gap_content) > 1000, "Research gap analysis document must be comprehensive"
