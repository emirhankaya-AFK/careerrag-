import streamlit as st
import requests
from ..components.match_card import render_match_metric
from ..components.salary_chart import render_salary_chart

BACKEND_URL = "http://localhost:8003"

st.set_page_config(page_title="Resume Matching - CareerRAG", layout="wide")

st.title("🎯 Resume-to-Job Matching")
st.write("Compare resumes against job requirements, calculate fit percentages, and identify skill roadmaps.")

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
    
    tab1, tab2 = st.tabs(["🎯 Single Job Match", "⚡ Batch Match Top Jobs"])
    
    with tab1:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            selected_cv_name = st.selectbox("Select Candidate Resume", list(cv_options.keys()), key="match_cv")
            selected_cv_id = cv_options[selected_cv_name]
        with col_c2:
            selected_job_name = st.selectbox("Select Target Job Listing", list(job_options.keys()), key="match_job")
            selected_job_id = job_options[selected_job_name]
            
        if st.button("🚀 Calculate Compatibility Fit"):
            with st.spinner("Analyzing matching taxonomy metrics..."):
                try:
                    payload = {"cv_id": selected_cv_id, "job_id": selected_job_id}
                    res = requests.post(f"{BACKEND_URL}/matching/run", json=payload)
                    if res.status_code == 200:
                        st.session_state[f"match_{selected_cv_id}_{selected_job_id}"] = res.json()
                        st.success("Matching evaluation complete!")
                    else:
                        st.error(f"Scoring failed: {res.json().get('detail')}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
                    
        # Render match details
        match_key = f"match_{selected_cv_id}_{selected_job_id}"
        match_data = st.session_state.get(match_key)
        
        # Fallback fetch in case it exists in database
        if not match_data:
            try:
                details_res = requests.get(f"{BACKEND_URL}/recommendations/details/{selected_cv_id}/{selected_job_id}")
                if details_res.status_code == 200:
                    match_data = details_res.json()
            except Exception:
                pass
                
        if match_data:
            # Re-key compatibility mapping
            score = match_data.get("match_score", 0)
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_sc, col_sal = st.columns([1, 2])
            
            with col_sc:
                render_match_metric(score)
                
                # Render subscores if present
                if "skills_score" in match_data:
                    st.write(f"- Required Skills Match: **{match_data['skills_score']}%**")
                    st.write(f"- Seniority Level Fit: **{match_data['level_score']}%** ({match_data.get('candidate_level', 'Mid')})")
                    st.write(f"- Location Alignment: **{match_data['location_score']}%**")
            
            with col_sal:
                st.subheader("💰 Estimated Compensation Bounds")
                sal_min = match_data.get("salary_min") or match_data.get("salary", {}).get("estimated_min", 0)
                sal_max = match_data.get("salary_max") or match_data.get("salary", {}).get("estimated_max", 0)
                
                render_salary_chart(sal_min, sal_max)
                
                # Check explanation
                expl = match_data.get("salary", {}).get("explanation", "Standard competitive salary range forecast.")
                st.caption(expl)
                
            st.markdown("<br><hr><br>", unsafe_allow_html=True)
            st.subheader("🛣️ Skills Gap Analysis & Roadmap")
            gap = match_data.get("gap_analysis") or ""
            st.markdown(gap)
            
            # Simple Add to applications tracker
            st.markdown("<br><hr><br>", unsafe_allow_html=True)
            st.subheader("📌 Track Application")
            app_status = st.selectbox("Current Status", ["Applied", "Interviewing", "Offered", "Rejected"])
            if st.button("Save to Application Tracker"):
                try:
                    app_payload = {
                        "cv_id": selected_cv_id,
                        "job_id": selected_job_id,
                        "status": app_status
                    }
                    app_res = requests.post(f"{BACKEND_URL}/applications", json=app_payload)
                    if app_res.status_code == 200:
                        st.success("Successfully logged in Application Tracker!")
                    else:
                        st.error("Failed to log application.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("Run the Compatibility Fit calculation to display gap analysis and compensation ranges.")

    with tab2:
        st.subheader("Which 20 jobs am I best for?")
        batch_cv_name = st.selectbox("Select Candidate Resume for Batch Match", list(cv_options.keys()), key="batch_cv")
        batch_cv_id = cv_options[batch_cv_name]
        
        if st.button("⚡ Find Top Job Fits"):
            with st.spinner("Retrieving jobs from vector index and scoring candidates..."):
                try:
                    payload = {"cv_id": batch_cv_id}
                    res = requests.post(f"{BACKEND_URL}/matching/batch", json=payload)
                    if res.status_code == 200:
                        st.session_state[f"batch_matches_{batch_cv_id}"] = res.json()
                        st.success("Batch matching calculations complete!")
                    else:
                        st.error("Batch matching calculation failed.")
                except Exception as e:
                    st.error(f"Error: {e}")
                    
        batch_results = st.session_state.get(f"batch_matches_{batch_cv_id}")
        if batch_results:
            st.markdown("### Top Compatible Positions")
            for idx, item in enumerate(batch_results):
                color = "#10B981" if item['match_score'] >= 80 else "#F59E0B" if item['match_score'] >= 60 else "#EF4444"
                st.markdown(f"""
                <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1.2rem; border-radius: 8px; margin-bottom: 0.8rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div>
                        <strong style="color: #1E3A8A; font-size: 1.1rem;">#{idx+1} {item['title']}</strong>
                        <div style="color: #475569; font-size: 0.9rem; margin-top: 4px;">🏢 {item['company']} | 📍 {item['location']}</div>
                    </div>
                    <div style="background-color: {color}20; color: {color}; padding: 8px 16px; border-radius: 6px; font-weight: bold; font-size: 1.1rem;">
                        {item['match_score']}% Fit
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Execute top job fit query to list matches.")
