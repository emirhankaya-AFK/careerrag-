# CareerRAG - AI Job Matcher Agent

[English](README.md) | [Türkçe](README_TR.md)

CareerRAG is a CV-to-Job Matching and mock interview preparation system.

## Setup Instructions

1. **Navigate to Project Directory**:
   ```bash
   cd careerrag
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure API Key**:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```
   *Note: If no API key is provided, the application automatically runs in Mock Mode.*

4. **Start the FastAPI Backend**:
   ```bash
   uvicorn backend.main:app --port 8003 --reload
   ```

5. **Start the Streamlit Frontend**:
   ```bash
   streamlit run frontend/app.py --server.port 8503
   ```

## Features
- **Resume parsing**: Upload PDF and DOCX files to extract profile fields.
- **ATS matching engine**: Score candidate fit on skills (60%), seniority (20%), and location (20%).
- **Web import**: Paste a job board link (e.g. LinkedIn details page) to scrape and parse JDs.
- **Gap analysis**: Identify missing skills and generate a structured training roadmap.
- **Mock coaching**: Customized technical mock interview questions based on candidate profile.
- **Salary chart visualization**: Horizontal range bar demonstrating market alignment.
- **Batch matching**: Identify top 20 compatible job listings from vector database indexing.
