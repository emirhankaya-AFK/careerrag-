import yaml
from pathlib import Path
from typing import Dict, Any
from ..services.llm_service import llm_service

class InterviewAgent:
    def __init__(self):
        self.prompt_path = Path(__file__).resolve().parent.parent / "config" / "prompts.yaml"
        self._load_prompts()

    def _load_prompts(self):
        try:
            with open(self.prompt_path, "r") as f:
                self.prompts = yaml.safe_load(f)
        except Exception:
            self.prompts = {}

    def generate_interview_tips(self, job_title: str, company: str, experience_summary: str) -> str:
        """
        Calls Gemini to create customized interview tips based on candidate profile.
        """
        system_prompt = self.prompts.get("interview_tips", "")
        prompt = system_prompt.format(
            job_title=job_title,
            company=company,
            experience_summary=experience_summary
        )
        
        return llm_service.generate_content(prompt)

interview_agent = InterviewAgent()
