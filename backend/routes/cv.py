from fastapi import APIRouter, UploadFile, File, HTTPException
import json
from pathlib import Path
from ..services.storage_service import storage_service
from ..services.cv_parser import cv_parser
from ..agents.cv_extraction_agent import cv_extraction_agent

router = APIRouter(prefix="/cv", tags=["cv"])

@router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX CVs are supported.")
        
    try:
        content = await file.read()
        saved_path = storage_service.save_file(content, file.filename)
        
        # Parse text from file
        text = cv_parser.extract_text(saved_path)
        
        # Run AI extraction
        extracted_data = cv_extraction_agent.extract_cv(text)
        
        # Add to SQLite DB
        cv_record = storage_service.add_cv(
            filename=file.filename,
            file_path=str(saved_path),
            name=extracted_data.get("name", "Unknown Candidate"),
            email=extracted_data.get("email", ""),
            skills=",".join(extracted_data.get("skills", [])),
            experience=json.dumps(extracted_data.get("experience", [])),
            education=json.dumps(extracted_data.get("education", []))
        )
        
        return {
            "message": "CV uploaded and parsed successfully",
            "cv": cv_record
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process CV: {e}")

@router.get("")
def list_cvs():
    return storage_service.list_cvs()

@router.get("/{cv_id}")
def get_cv_details(cv_id: int):
    cv = storage_service.get_cv(cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
        
    return {
        "id": cv["id"],
        "filename": cv["filename"],
        "name": cv["name"],
        "email": cv["email"],
        "skills": cv["skills"].split(",") if cv["skills"] else [],
        "experience": json.loads(cv["experience"] or "[]"),
        "education": json.loads(cv["education"] or "[]"),
        "upload_date": cv["upload_date"]
    }

@router.delete("/{cv_id}")
def delete_cv(cv_id: int):
    success = storage_service.delete_cv(cv_id)
    if not success:
        raise HTTPException(status_code=404, detail="CV not found or could not delete")
    return {"message": "CV deleted successfully"}
