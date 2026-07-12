import pytest
from backend.agents.cv_extraction_agent import cv_extraction_agent

def test_cv_extraction_and_taxonomy():
    mock_cv = "Jane Smith. Email: jane@example.com. Skills: py, AWS, ML."
    result = cv_extraction_agent.extract_cv(mock_cv)
    
    assert isinstance(result, dict)
    assert "skills" in result
    
    # Check if "py" standardized to "Python"
    skills = result["skills"]
    assert "Python" in skills
