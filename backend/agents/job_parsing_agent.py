import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
from ..services.llm_service import llm_service

class JobParsingAgent:
    def __init__(self):
        self.prompt_path = Path(__file__).resolve().parent.parent / "config" / "prompts.yaml"
        self.taxonomy_path = Path(__file__).resolve().parent.parent / "config" / "skill_taxonomy.yaml"
        self._load_config()

    def _load_config(self):
        try:
            with open(self.prompt_path, "r") as f:
                self.prompts = yaml.safe_load(f)
        except Exception:
            self.prompts = {}
            
        try:
            with open(self.taxonomy_path, "r") as f:
                self.taxonomy = yaml.safe_load(f).get("taxonomy", {})
        except Exception:
            self.taxonomy = {}

    def parse_job(self, description_text: str) -> Dict[str, Any]:
        """
        Extracts ATS parameters from job description and standardizes skills.
        """
        system_prompt = self.prompts.get("job_parsing", "")
        prompt = f"{system_prompt}\n\nJob Description:\n{description_text[:30000]}"
        
        response_text = llm_service.generate_content(prompt)
        extracted = self._parse_json_object(response_text)
        
        # Standardize required skills
        req_skills = extracted.get("required_skills", [])
        std_req = []
        for sk in req_skills:
            sk_clean = sk.strip().lower()
            std = self.taxonomy.get(sk_clean, sk.strip())
            if std not in std_req:
                std_req.append(std)
        extracted["required_skills"] = std_req

        # Standardize nice-to-have skills
        nice_skills = extracted.get("nice_to_have", [])
        std_nice = []
        for sk in nice_skills:
            sk_clean = sk.strip().lower()
            std = self.taxonomy.get(sk_clean, sk.strip())
            if std not in std_nice:
                std_nice.append(std)
        extracted["nice_to_have"] = std_nice
        
        return extracted

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
        except Exception as e:
            print(f"Failed to parse Job JSON: {e}")
            return {
                "title": "Unknown Job",
                "company": "Unknown",
                "location": "Remote",
                "required_skills": [],
                "nice_to_have": [],
                "experience_level": "Mid"
            }

job_parsing_agent = JobParsingAgent()
