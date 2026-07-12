import yaml
import json
from pathlib import Path
from typing import Dict, Any
from ..services.llm_service import llm_service

class SalaryAgent:
    def __init__(self):
        self.prompt_path = Path(__file__).resolve().parent.parent / "config" / "prompts.yaml"
        self.salary_path = Path(__file__).resolve().parent.parent / "config" / "salary_ranges.yaml"
        self._load_config()

    def _load_config(self):
        try:
            with open(self.prompt_path, "r") as f:
                self.prompts = yaml.safe_load(f)
        except Exception:
            self.prompts = {}
            
        try:
            with open(self.salary_path, "r") as f:
                self.salary_data = yaml.safe_load(f)
        except Exception:
            self.salary_data = {}

    def estimate_salary(self, job_title: str, location: str, years_exp: float) -> Dict[str, Any]:
        """
        Uses reference ranges and LLM to predict candidate target salary range.
        """
        # Determine seniority level based on years of experience
        level = "Junior" if years_exp < 2 else "Mid" if years_exp < 6 else "Senior"
        
        # Look up baseline ranges in salary_ranges.yaml
        baseline_min = 80000
        baseline_max = 110000
        
        roles = self.salary_data.get("roles", [])
        matched_role = None
        for role in roles:
            # Simple substring matching for job titles
            if role["title"].lower() in job_title.lower() or job_title.lower() in role["title"].lower():
                matched_role = role
                break
                
        if matched_role:
            bounds = matched_role.get(level, {})
            baseline_min = bounds.get("min", baseline_min)
            baseline_max = bounds.get("max", baseline_max)
        else:
            default_bounds = self.salary_data.get("default", {}).get(level, {})
            baseline_min = default_bounds.get("min", baseline_min)
            baseline_max = default_bounds.get("max", baseline_max)

        # Refine using LLM
        system_prompt = self.prompts.get("salary_estimation", "")
        prompt = system_prompt.format(job_title=job_title, location=location, years_exp=years_exp)
        
        response_text = llm_service.generate_content(prompt)
        parsed = self._parse_json_object(response_text)
        
        # Merge baseline if LLM failed
        if not parsed.get("estimated_min"):
            parsed["estimated_min"] = baseline_min
            parsed["estimated_max"] = baseline_max
            parsed["currency"] = "USD"
            parsed["explanation"] = "Using standard role database baseline."
            
        return parsed

    def _parse_json_object(self, text: str) -> Dict[str, Any]:
        try:
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                cleaned = cleaned[start:end+1]
                
            return json.loads(cleaned)
        except Exception:
            return {}

salary_agent = SalaryAgent()
