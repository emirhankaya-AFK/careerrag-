import streamlit as st
import requests

BACKEND_URL = "http://localhost:8003"

st.set_page_config(page_title="Interview Prep - CareerRAG", layout="wide")

st.title("🗣️ Mock Interview Preparation Coach")
st.write("Review customized mock interview questions and aligned talking points from your CV history.")

# Fetch CVs and Jobs
try:
    cv_res = requests.get(f"{BACKEND_URL}/cv")
    job_res = requests.get(f"{BACKEND_URL}/jobs")
    
    cvs = cv_res.json() if cv_res.status_code == 200 else []
    jobs = job_res.json() if job_res.status_code == 200 else []
except Exception as e:
    cvs, jobs = [], []
    st.error(f"Failed to fetch assets: {e}")

if not cvs:
    st.info("Please upload a resume first on the Upload CV page.")
elif not jobs:
    st.info("Please add or scrape job descriptions first on the Add Job page.")
else:
    cv_options = {cv["name"]: cv["id"] for cv in cvs}
    job_options = {f"{job['title']} at {job['company']}": job["id"] for job in jobs}
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        selected_cv_name = st.selectbox("Select Candidate Resume", list(cv_options.keys()), key="prep_cv")
        selected_cv_id = cv_options[selected_cv_name]
    with col_c2:
        selected_job_name = st.selectbox("Select Target Job Listing", list(job_options.keys()), key="prep_job")
        selected_job_id = job_options[selected_job_name]
        
    match_data = None
    try:
        details_res = requests.get(f"{BACKEND_URL}/recommendations/details/{selected_cv_id}/{selected_job_id}")
        if details_res.status_code == 200:
            match_data = details_res.json()
    except Exception:
        pass
        
    if not match_data:
        st.warning("No matching calculations found. Please run Compatibility Fit on the Matching page first.")
    else:
        st.success(f"Interview guidelines compiled for {selected_cv_name} applying to {selected_job_name}!")
        
        st.write("### AI-Generated Interview Preparation Guidelines")
        tips = match_data.get("interview_tips") or ""
        st.markdown(tips)
