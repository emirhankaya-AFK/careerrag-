import yaml
from pathlib import Path
from typing import Dict, Any
from ..services.llm_service import llm_service

class GapAgent:
    def __init__(self):
        self.prompt_path = Path(__file__).resolve().parent.parent / "config" / "prompts.yaml"
        self._load_prompts()

    def _load_prompts(self):
        try:
            with open(self.prompt_path, "r") as f:
                self.prompts = yaml.safe_load(f)
        except Exception:
            self.prompts = {}

    def analyze_gaps(self, candidate_skills: List[str], required_skills: List[str]) -> str:
        """
        Calculates skill gaps and generates markdown learning recommendations.
        """
        your_skills_str = ", ".join(candidate_skills)
        req_skills_str = ", ".join(required_skills)
        
        system_prompt = self.prompts.get("gap_analysis", "")
        prompt = system_prompt.format(your_skills=your_skills_str, required_skills=req_skills_str)
        
        return llm_service.generate_content(prompt)

from typing import List # Ensure import is correct
gap_agent = GapAgent()
