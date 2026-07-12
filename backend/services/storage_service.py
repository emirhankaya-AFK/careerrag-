import sqlite3
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..config.settings import settings

class CareerStorageService:
    def __init__(self):
        self.db_path = settings.DB_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # CVs Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cvs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                name TEXT,
                email TEXT,
                skills TEXT, -- comma-separated
                experience TEXT, -- JSON string
                education TEXT, -- JSON string
                upload_date TEXT NOT NULL
            );
            """)

            # Jobs Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                required_skills TEXT, -- comma-separated
                nice_to_have TEXT, -- comma-separated
                experience_level TEXT,
                description TEXT,
                added_date TEXT NOT NULL
            );
            """)

            # Matches Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cv_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                match_score INTEGER NOT NULL,
                gap_analysis TEXT,
                recommendations TEXT,
                salary_min INTEGER,
                salary_max INTEGER,
                match_date TEXT NOT NULL,
                FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE
            );
            """)

            # Applications Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cv_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                status TEXT NOT NULL, -- Applied, Interviewing, Offered, Rejected
                applied_date TEXT,
                follow_up_date TEXT,
                FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE
            );
            """)
            conn.commit()

    # --- CV Operations ---
    def save_file(self, file_content: bytes, filename: str) -> Path:
        target_path = settings.UPLOAD_DIR / filename
        if target_path.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            filename = f"{stem}_{int(datetime.utcnow().timestamp())}{suffix}"
            target_path = settings.UPLOAD_DIR / filename

        with open(target_path, "wb") as f:
            f.write(file_content)
        return target_path

    def add_cv(self, filename: str, file_path: str, name: str, email: str, skills: str, experience: str, education: str) -> Dict[str, Any]:
        upload_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO cvs (filename, file_path, name, email, skills, experience, education, upload_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (filename, file_path, name, email, skills, experience, education, upload_date))
            cv_id = cursor.lastrowid
            conn.commit()
            return {"id": cv_id, "filename": filename, "file_path": file_path, "name": name, "email": email, "skills": skills, "upload_date": upload_date}

    def get_cv(self, cv_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cvs WHERE id = ?;", (cv_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_cvs(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cvs ORDER BY upload_date DESC;")
            return [dict(row) for row in cursor.fetchall()]

    def delete_cv(self, cv_id: int) -> bool:
        cv = self.get_cv(cv_id)
        if not cv:
            return False
        
        file_path = Path(cv["file_path"])
        if file_path.exists():
            file_path.unlink()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cvs WHERE id = ?;", (cv_id,))
            conn.commit()
            return True

    # --- Job Operations ---
    def add_job(self, title: str, company: str, location: str, required_skills: str, nice_to_have: str, experience_level: str, description: str) -> int:
        added_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO jobs (title, company, location, required_skills, nice_to_have, experience_level, description, added_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (title, company, location, required_skills, nice_to_have, experience_level, description, added_date))
            job_id = cursor.lastrowid
            conn.commit()
            return job_id

    def get_job(self, job_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs WHERE id = ?;", (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_jobs(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs ORDER BY added_date DESC;")
            return [dict(row) for row in cursor.fetchall()]

    # --- Matching Operations ---
    def add_match(self, cv_id: int, job_id: int, match_score: int, gap_analysis: str, recommendations: str, salary_min: int, salary_max: int) -> int:
        match_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM matches WHERE cv_id = ? AND job_id = ?;", (cv_id, job_id))
            cursor.execute("""
            INSERT INTO matches (cv_id, job_id, match_score, gap_analysis, recommendations, salary_min, salary_max, match_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (cv_id, job_id, match_score, gap_analysis, recommendations, salary_min, salary_max, match_date))
            match_id = cursor.lastrowid
            conn.commit()
            return match_id

    def get_match(self, cv_id: int, job_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matches WHERE cv_id = ? AND job_id = ?;", (cv_id, job_id))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_matches_for_cv(self, cv_id: int) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT m.*, j.title, j.company, j.location 
            FROM matches m 
            JOIN jobs j ON m.job_id = j.id 
            WHERE m.cv_id = ? 
            ORDER BY m.match_score DESC;
            """, (cv_id,))
            return [dict(row) for row in cursor.fetchall()]

    # --- Application Operations ---
    def add_application(self, cv_id: int, job_id: int, status: str, applied_date: str, follow_up_date: str) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM applications WHERE cv_id = ? AND job_id = ?;", (cv_id, job_id))
            cursor.execute("""
            INSERT INTO applications (cv_id, job_id, status, applied_date, follow_up_date)
            VALUES (?, ?, ?, ?, ?);
            """, (cv_id, job_id, status, applied_date, follow_up_date))
            app_id = cursor.lastrowid
            conn.commit()
            return app_id

    def list_applications(self, cv_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if cv_id is not None:
                cursor.execute("""
                SELECT a.*, j.title, j.company 
                FROM applications a 
                JOIN jobs j ON a.job_id = j.id 
                WHERE a.cv_id = ?;
                """, (cv_id,))
            else:
                cursor.execute("""
                SELECT a.*, j.title, j.company 
                FROM applications a 
                JOIN jobs j ON a.job_id = j.id;
                """)
            return [dict(row) for row in cursor.fetchall()]

storage_service = CareerStorageService()
