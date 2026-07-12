import streamlit as st
import requests

BACKEND_URL = "http://localhost:8003"

st.set_page_config(page_title="Add Job - CareerRAG", layout="wide")

st.title("💼 Manage Job Descriptions")
st.write("Add job listings manually or import details from job posting links (e.g. LinkedIn).")

tab1, tab2 = st.tabs(["🔗 Scrape Job Listing", "📝 Add Job Manually"])

with tab1:
    st.subheader("Import Listing from URL")
    st.write("CareerRAG will scrape details and run AI parsers to extract required competencies and salaries.")
    
    job_url = st.text_input("Job Posting URL", placeholder="https://www.linkedin.com/jobs/view/...")
    
    if st.button("🚀 Import Posting"):
        if not job_url:
            st.warning("Please enter a URL.")
        else:
            with st.spinner("Scraping and mapping ATS parameters..."):
                try:
                    payload = {"url": job_url}
                    res = requests.post(f"{BACKEND_URL}/jobs/scrape", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        st.success(f"Successfully scraped job: '{data['title']}' at {data['company']}")
                        st.rerun()
                    else:
                        st.error(f"Failed to scrape: {res.json().get('detail')}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

with tab2:
    st.subheader("Create Manual Job description")
    title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    location = st.text_input("Location", placeholder="e.g. Austin, TX or Remote")
    req_skills_input = st.text_input("Required Skills (comma-separated)", placeholder="e.g. Python, SQL, Git")
    nice_skills_input = st.text_input("Nice-to-have Skills (comma-separated)", placeholder="e.g. Docker, PyTorch")
    exp_level = st.selectbox("Experience Level Required", ["Junior", "Mid", "Senior"])
    description = st.text_area("Job Description Details", height=150)
    
    if st.button("Add Job Listing"):
        if not title or not company or not description:
            st.warning("Please complete all required fields.")
        else:
            try:
                req_skills = [s.strip() for s in req_skills_input.split(",") if s.strip()]
                nice_skills = [s.strip() for s in nice_skills_input.split(",") if s.strip()]
                
                payload = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "required_skills": req_skills,
                    "nice_to_have": nice_skills,
                    "experience_level": exp_level,
                    "description": description
                }
                res = requests.post(f"{BACKEND_URL}/jobs", json=payload)
                if res.status_code == 200:
                    st.success(f"Added job: '{title}' at {company}")
                    st.rerun()
                else:
                    st.error(f"Failed to add: {res.json().get('detail')}")
            except Exception as e:
                st.error(f"Connection error: {e}")

st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.subheader("📚 Managed Jobs Directory")

try:
    res = requests.get(f"{BACKEND_URL}/jobs")
    if res.status_code == 200:
        jobs = res.json()
        if not jobs:
            st.info("No job postings added yet.")
        else:
            for job in jobs:
                st.markdown(f"""
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 8px; margin-bottom: 0.8rem;">
                    <strong>{job['title']}</strong> - 🏢 {job['company']} ({job['location']})
                    <div style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">
                        Level: {job['experience_level']} | Skills: {job['required_skills']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error fetching directory: {e}")
