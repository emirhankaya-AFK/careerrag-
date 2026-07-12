import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
from ..services.llm_service import llm_service

class CVExtractionAgent:
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

    def extract_cv(self, text: str) -> Dict[str, Any]:
        """
        Extracts structured parameters from CV text and standardizes skill tokens.
        """
        system_prompt = self.prompts.get("cv_extraction", "")
        prompt = f"{system_prompt}\n\nCV Text:\n{text[:30000]}"
        
        response_text = llm_service.generate_content(prompt)
        extracted = self._parse_json_object(response_text)
        
        # Standardize skills using taxonomy
        skills = extracted.get("skills", [])
        standardized_skills = []
        for sk in skills:
            sk_clean = sk.strip().lower()
            std = self.taxonomy.get(sk_clean, sk.strip())
            if std not in standardized_skills:
                standardized_skills.append(std)
                
        extracted["skills"] = standardized_skills
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
            print(f"Failed to parse CV JSON: {e}")
            return {
                "name": "Unknown Candidate",
                "email": "",
                "skills": [],
                "experience": [],
                "education": []
            }

cv_extraction_agent = CVExtractionAgent()
