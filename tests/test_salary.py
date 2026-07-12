import pytest
from backend.agents.salary_agent import salary_agent

def test_salary_estimation_baseline():
    result = salary_agent.estimate_salary(
        job_title="Data Scientist",
        location="Austin, TX",
        years_exp=3.0 # Mid
    )
    
    assert "estimated_min" in result
    assert "estimated_max" in result
    assert result["estimated_min"] >= 80000
