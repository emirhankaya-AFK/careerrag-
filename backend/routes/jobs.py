from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..services.storage_service import storage_service
from ..services.job_scraper import job_scraper
from ..services.rag_service import rag_service
from ..agents.job_parsing_agent import job_parsing_agent

router = APIRouter(prefix="/jobs", tags=["jobs"])

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    required_skills: List[str]
    nice_to_have: List[str]
    experience_level: str
    description: str

class ScrapeRequest(BaseModel):
    url: str

@router.post("")
def create_job(job: JobCreate):
    try:
        req_skills_str = ",".join(job.required_skills)
        nice_skills_str = ",".join(job.nice_to_have)
        
        job_id = storage_service.add_job(
            title=job.title,
            company=job.company,
            location=job.location,
            required_skills=req_skills_str,
            nice_to_have=nice_skills_str,
            experience_level=job.experience_level,
            description=job.description
        )
        
        # Index in ChromaDB
        rag_service.add_job(
            job_id=job_id,
            title=job.title,
            description=job.description,
            company=job.company,
            skills=job.required_skills
        )
        
        return {"id": job_id, "message": "Job added and indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {e}")

@router.post("/scrape")
def scrape_job_posting(request: ScrapeRequest):
    try:
        # Scrape raw details
        scraped = job_scraper.scrape_job(request.url)
        
        # Parse details with AI
        parsed = job_parsing_agent.parse_job(scraped["description"])
        
        # If scraper did not identify company, merge scraped values
        company = parsed.get("company", scraped.get("company", "Unknown Company"))
        title = parsed.get("title", scraped.get("title", "Unknown Job"))
        location = parsed.get("location", scraped.get("location", "Remote"))
        
        # Save to database
        req_skills_str = ",".join(parsed.get("required_skills", []))
        nice_skills_str = ",".join(parsed.get("nice_to_have", []))
        
        job_id = storage_service.add_job(
            title=title,
            company=company,
            location=location,
            required_skills=req_skills_str,
            nice_to_have=nice_skills_str,
            experience_level=parsed.get("experience_level", "Mid"),
            description=scraped["description"]
        )
        
        # Index in ChromaDB
        rag_service.add_job(
            job_id=job_id,
            title=title,
            description=scraped["description"],
            company=company,
            skills=parsed.get("required_skills", [])
        )
        
        return {
            "id": job_id,
            "title": title,
            "company": company,
            "location": location,
            "required_skills": parsed.get("required_skills", []),
            "nice_to_have": parsed.get("nice_to_have", []),
            "experience_level": parsed.get("experience_level", "Mid"),
            "description": scraped["description"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape and parse job: {e}")

@router.get("")
def list_jobs():
    return storage_service.list_jobs()
