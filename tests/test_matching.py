import pytest
from backend.agents.matching_agent import matching_agent

def test_match_score_weights():
    # 100% skills match, 100% experience match, 80% location match
    cv_data = {
        "skills": ["Python", "FastAPI"],
        "experience": [{"title": "Software Engineer", "duration": "3 years", "description": "Backend developer"}]
    }
    
    job_data = {
        "title": "FastAPI Developer",
        "required_skills": ["Python", "FastAPI"],
        "experience_level": "Mid",
        "location": "Austin, TX (Hybrid)"
    }
    
    result = matching_agent.calculate_match_score(cv_data, job_data)
    
    assert "match_score" in result
    assert result["match_score"] > 80 # expected ~96%
    assert result["candidate_level"] == "Mid"
