import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import cv, jobs, matching, recommendations, applications
from .config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for CareerRAG CV-to-Job Matching System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(cv.router)
app.include_router(jobs.router)
app.include_router(matching.router)
app.include_router(recommendations.router)
app.include_router(applications.router)

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "api_docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
