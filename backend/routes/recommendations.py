from fastapi import APIRouter, HTTPException
from ..services.storage_service import storage_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/details/{cv_id}/{job_id}")
def get_recommendation_details(cv_id: int, job_id: int):
    match = storage_service.get_match(cv_id, job_id)
    if not match:
        raise HTTPException(status_code=404, detail="No matching record found. Run match first.")
        
    return {
        "cv_id": match["cv_id"],
        "job_id": match["job_id"],
        "match_score": match["match_score"],
        "gap_analysis": match["gap_analysis"],
        "interview_tips": match["recommendations"],
        "salary_min": match["salary_min"],
        "salary_max": match["salary_max"]
    }
