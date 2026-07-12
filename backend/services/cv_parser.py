import pdfplumber
import docx
from pathlib import Path
from typing import Dict, Any

class CVParser:
    def extract_text(self, file_path: Path) -> str:
        """
        Detects file extension and extracts all readable text from PDF or DOCX documents.
        """
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext == ".docx":
            return self._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}. Only PDF and DOCX CVs are supported.")

    def _parse_pdf(self, file_path: Path) -> str:
        full_text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    full_text += text + "\n"
            return full_text
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {e}")

    def _parse_docx(self, file_path: Path) -> str:
        try:
            doc = docx.Document(file_path)
            full_text = []
            for p in doc.paragraphs:
                full_text.append(p.text)
            return "\n".join(full_text)
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX document: {e}")

cv_parser = CVParser()
