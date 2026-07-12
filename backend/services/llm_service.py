import os
import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from ..config.settings import settings

class CareerLLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.has_api_key = bool(self.api_key and self.api_key != "YOUR_GEMINI_API_KEY")
        if self.has_api_key:
            genai.configure(api_key=self.api_key)
        else:
            print("WARNING: GEMINI_API_KEY is not configured for CareerRAG. Running in Mock Mode.")

    def generate_content(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        if not self.has_api_key:
            return self._mock_llm_response(prompt)
            
        try:
            model = genai.GenerativeModel(
                model_name=settings.LLM_MODEL,
                system_instruction=system_instruction
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini LLM failed in CareerRAG: {e}. Falling back to Mock.")
            return self._mock_llm_response(prompt)

    def generate_embeddings(self, text: str) -> List[float]:
        if not self.has_api_key:
            return self._mock_embeddings(text)
            
        try:
            result = genai.embed_content(
                model=f"models/{settings.EMBEDDING_MODEL}",
                content=text,
                task_type="retrieval_document"
            )
            return result["embedding"]
        except Exception as e:
            print(f"Gemini Embedding failed in CareerRAG: {e}. Falling back to Mock.")
            return self._mock_embeddings(text)

    def _mock_embeddings(self, text: str) -> List[float]:
        import random
        random.seed(hash(text))
        return [random.uniform(-0.1, 0.1) for _ in range(768)]

    def _mock_llm_response(self, prompt: str) -> str:
        lower_prompt = prompt.lower()
        if "cv_extraction" in prompt or "recruitment parser" in lower_prompt or "cv content" in lower_prompt or "parse this cv" in lower_prompt:
            return json.dumps({
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "skills": ["Python", "FastAPI", "SQL", "Docker", "Git"],
                "experience": [
                    {
                        "company": "Enterprise Software Co.",
                        "title": "Software Developer",
                        "duration": "24 months",
                        "description": "Engineered web API endpoints using Django and PostgreSQL. Configured dockerized local run environment."
                    }
                ],
                "education": [
                    {
                        "school": "University of Austin",
                        "degree": "B.S. in Computer Science",
                        "year": "2024"
                    }
                ]
            })
        elif "job_parsing" in prompt or "job description parser" in lower_prompt or "job listing" in lower_prompt:
            return json.dumps({
                "title": "Python Backend Developer (FastAPI/AWS)",
                "company": "CloudVentures LLC",
                "location": "Austin, TX (Hybrid)",
                "required_skills": ["Python", "FastAPI", "SQL", "AWS"],
                "nice_to_have": ["Docker", "Kubernetes", "PyTorch"],
                "experience_level": "Mid"
            })
        elif "gap_analysis" in prompt:
            return (
                "### Gap Analysis & Career Development Plan\n\n"
                "**Missing Skills**:\n"
                "- AWS (Amazon Web Services)\n"
                "- PyTorch (Nice-to-have)\n\n"
                "**Roadmap**:\n"
                "1. **AWS Cloud Practitioner (Week 1-2)**: Review AWS free tier labs. Focus on EC2, S3, and RDS.\n"
                "2. **FastAPI deployment on AWS ECS (Week 3)**: Dockerize a microservice and release it using AWS Fargate.\n"
                "3. **PyTorch Basics (Week 4)**: Code simple neural networks via PyTorch tutorials."
            )
        elif "interview_tips" in prompt:
            return (
                "### Recruiter Mock Interview Preparation\n\n"
                "**Question 1**: Can you discuss your experience containerizing APIs with Docker?\n"
                "- *CV Talking Point*: Describe your dockerized setup at Enterprise Software Co.\n\n"
                "**Question 2**: Explain a complex SQL migration you handled.\n"
                "- *CV Talking Point*: Mention working with PostgreSQL endpoints and schema design.\n\n"
                "**Question 3**: Why FastAPI over Django for microservices?\n"
                "- *CV Talking Point*: Compare performance benchmarks based on your Python background."
            )
        elif "salary_estimation" in prompt:
            return json.dumps({
                "estimated_min": 95000,
                "estimated_max": 125000,
                "currency": "USD",
                "explanation": "Predicted salary of $95k - $125k is highly aligned with Austin, TX market rates for mid-level python developers."
            })
        else:
            return "Mock Career Agent response: Please configure GEMINI_API_KEY."

llm_service = CareerLLMService()
