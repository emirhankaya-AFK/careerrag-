from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.storage_service import storage_service

router = APIRouter(prefix="/applications", tags=["applications"])

class ApplicationCreate(BaseModel):
    cv_id: int
    job_id: int
    status: str # Applied, Interviewing, Offered, Rejected
    applied_date: Optional[str] = None
    follow_up_date: Optional[str] = None

@router.post("")
def add_application(app: ApplicationCreate):
    try:
        app_id = storage_service.add_application(
            cv_id=app.cv_id,
            job_id=app.job_id,
            status=app.status,
            applied_date=app.applied_date,
            follow_up_date=app.follow_up_date
        )
        return {"id": app_id, "message": "Application tracked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record application: {e}")

@router.get("")
def list_applications(cv_id: Optional[int] = None):
    return storage_service.list_applications(cv_id)
