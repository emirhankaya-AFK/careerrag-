import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    PROJECT_NAME: str = "CareerRAG"
    
    # Storage
    UPLOAD_DIR: Path = BASE_DIR / "storage" / "cvs"
    DB_PATH: str = str(BASE_DIR / "storage" / "careerrag.db")
    CHROMA_DB_DIR: str = str(BASE_DIR / "storage" / "chroma_db")
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    EMBEDDING_MODEL: str = "text-embedding-004"
    LLM_MODEL: str = "gemini-2.0-flash"
    
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8003
    
    def __init__(self):
        # Create directories if they don't exist
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        Path(self.CHROMA_DB_DIR).mkdir(parents=True, exist_ok=True)

settings = Settings()
