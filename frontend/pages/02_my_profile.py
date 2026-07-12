import streamlit as st
import requests
from ..components.cv_viewer import render_cv_header

BACKEND_URL = "http://localhost:8003"

st.set_page_config(page_title="My Profile - CareerRAG", layout="wide")

st.title("👤 Candidate Profile View")
st.write("Review parsed resume entities and standardized skills mapped via taxonomy rules.")

try:
    cv_res = requests.get(f"{BACKEND_URL}/cv")
    cvs = cv_res.json() if cv_res.status_code == 200 else []
except Exception as e:
    cvs = []
    st.error(f"Failed to load candidates: {e}")

if not cvs:
    st.info("Please upload a resume first on the Upload CV page.")
else:
    cv_options = {cv["name"]: cv["id"] for cv in cvs}
    selected_candidate = st.selectbox("Select Candidate Profile", list(cv_options.keys()))
    selected_id = cv_options[selected_candidate]
    
    with st.spinner("Retrieving profile data..."):
        try:
            res = requests.get(f"{BACKEND_URL}/cv/{selected_id}")
            if res.status_code == 200:
                data = res.json()
                
                # Render header
                render_cv_header(
                    name=data["name"],
                    email=data["email"],
                    filename=data["filename"]
                )
                
                tab1, tab2, tab3 = st.tabs(["🛠️ Technical Skills", "💼 Work History", "🎓 Education"])
                
                with tab1:
                    st.write("### Standardized Technical Competencies")
                    skills = data.get("skills", [])
                    if not skills:
                        st.info("No skills extracted.")
                    else:
                        # Display skills as color tags
                        tags_html = ""
                        for sk in skills:
                            tags_html += f'<span style="background-color: #DBEAFE; color: #1E40AF; padding: 6px 12px; border-radius: 9999px; margin-right: 8px; margin-bottom: 8px; font-weight: 500; display: inline-block; font-size: 0.85rem;">{sk}</span>'
                        st.markdown(tags_html, unsafe_allow_html=True)
                        
                with tab2:
                    st.write("### Professional Work Experience")
                    experience = data.get("experience", [])
                    if not experience:
                        st.info("No work history found.")
                    else:
                        for exp in experience:
                            st.markdown(f"""
                            <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1.2rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                    <strong style="color: #0F172A; font-size: 1.05rem;">{exp.get('title')}</strong>
                                    <span style="color: #64748B; font-size: 0.85rem; font-weight: bold;">{exp.get('duration')}</span>
                                </div>
                                <div style="color: #1E3A8A; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.8rem;">🏢 {exp.get('company')}</div>
                                <p style="color: #475569; font-size: 0.95rem; line-height: 1.5; white-space: pre-wrap;">
                                    {exp.get('description')}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                with tab3:
                    st.write("### Academic Background")
                    education = data.get("education", [])
                    if not education:
                        st.info("No education details found.")
                    else:
                        for edu in education:
                            st.markdown(f"""
                            <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 8px; margin-bottom: 0.8rem;">
                                <div style="font-weight: bold; color: #0F172A;">🎓 {edu.get('degree')}</div>
                                <div style="color: #64748B; font-size: 0.85rem;">{edu.get('school')} | Graduation Year: {edu.get('year')}</div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.error("Failed to load details.")
        except Exception as e:
            st.error(f"Error fetching profile details: {e}")
