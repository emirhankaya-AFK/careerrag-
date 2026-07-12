from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from ..services.storage_service import storage_service
from ..services.rag_service import rag_service
from ..agents.matching_agent import matching_agent
from ..agents.gap_agent import gap_agent
from ..agents.salary_agent import salary_agent
from ..agents.interview_agent import interview_agent

router = APIRouter(prefix="/matching", tags=["matching"])

class MatchRequest(BaseModel):
    cv_id: int
    job_id: int

class BatchMatchRequest(BaseModel):
    cv_id: int

@router.post("/run")
def run_matching(request: MatchRequest):
    cv = storage_service.get_cv(request.cv_id)
    job = storage_service.get_job(request.job_id)
    if not cv or not job:
        raise HTTPException(status_code=404, detail="CV or Job not found")
        
    try:
        # Reconstruct dicts for agents
        cv_data = {
            "skills": cv["skills"].split(",") if cv["skills"] else [],
            "experience": json.loads(cv["experience"] or "[]"),
            "education": json.loads(cv["education"] or "[]")
        }
        
        job_data = {
            "title": job["title"],
            "required_skills": job["required_skills"].split(",") if job["required_skills"] else [],
            "experience_level": job["experience_level"],
            "location": job["location"]
        }
        
        # 1. Match Score
        score_res = matching_agent.calculate_match_score(cv_data, job_data)
        score = score_res["match_score"]
        
        # 2. Gap Analysis
        roadmap = gap_agent.analyze_gaps(
            candidate_skills=cv_data["skills"],
            required_skills=job_data["required_skills"]
        )
        
        # 3. Salary Estimation
        salary_res = salary_agent.estimate_salary(
            job_title=job["title"],
            location=job["location"],
            years_exp=score_res["candidate_years"]
        )
        
        # 4. Interview Tips
        exp_summary = " ".join([e.get("description", "") for e in cv_data["experience"]])
        tips = interview_agent.generate_interview_tips(
            job_title=job["title"],
            company=job["company"],
            experience_summary=exp_summary[:1000]
        )
        
        # Save to DB
        storage_service.add_match(
            cv_id=request.cv_id,
            job_id=request.job_id,
            match_score=score,
            gap_analysis=roadmap,
            recommendations=tips,
            salary_min=salary_res.get("estimated_min", 0),
            salary_max=salary_res.get("estimated_max", 0)
        )
        
        return {
            "status": "success",
            "match_score": score,
            "skills_score": score_res["skills_score"],
            "level_score": score_res["level_score"],
            "location_score": score_res["location_score"],
            "candidate_years": score_res["candidate_years"],
            "candidate_level": score_res["candidate_level"],
            "gap_analysis": roadmap,
            "interview_tips": tips,
            "salary": salary_res
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Matching calculation failed: {e}")

@router.post("/batch")
def batch_match_cv(request: BatchMatchRequest):
    cv = storage_service.get_cv(request.cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
        
    try:
        # Build search query string based on skills
        skills_str = cv["skills"].replace(",", " ")
        
        # Retrieve top 20 semantic jobs matching candidate skills
        semantic_matches = rag_service.match_jobs(query_text=skills_str, n_results=20)
        
        results = []
        cv_skills = cv["skills"].split(",") if cv["skills"] else []
        cv_exp = json.loads(cv["experience"] or "[]")
        
        cv_data = {
            "skills": cv_skills,
            "experience": cv_exp
        }
        
        for sm in semantic_matches:
            job_id = sm["metadata"]["job_id"]
            job = storage_service.get_job(job_id)
            if not job:
                continue
                
            job_data = {
                "title": job["title"],
                "required_skills": job["required_skills"].split(",") if job["required_skills"] else [],
                "experience_level": job["experience_level"],
                "location": job["location"]
            }
            
            score_res = matching_agent.calculate_match_score(cv_data, job_data)
            
            results.append({
                "job_id": job_id,
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "match_score": score_res["match_score"],
                "distance": sm["distance"]
            })
            
        # Sort results by score (descending)
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch matching failed: {e}")

@router.get("/cv/{cv_id}")
def get_cv_matches(cv_id: int):
    return storage_service.get_matches_for_cv(cv_id)
