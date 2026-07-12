import streamlit as st
import requests

BACKEND_URL = "http://localhost:8003"

st.set_page_config(page_title="Track Applications - CareerRAG", layout="wide")

st.title("📌 Job Application Tracker")
st.write("Monitor the status of your active job applications and calendar follow-ups.")

# Fetch applications list
try:
    res = requests.get(f"{BACKEND_URL}/applications")
    if res.status_code == 200:
        apps = res.json()
    else:
        apps = []
except Exception as e:
    apps = []
    st.error(f"Failed to fetch application records: {e}")

if not apps:
    st.info("No applications logged in tracker yet. Run match compatibility and track applications.")
else:
    # Summary Metrics
    c_applied = len([a for a in apps if a["status"] == "Applied"])
    c_interv = len([a for a in apps if a["status"] == "Interviewing"])
    c_offered = len([a for a in apps if a["status"] == "Offered"])
    c_rejected = len([a for a in apps if a["status"] == "Rejected"])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Applied", c_applied)
    col2.metric("Interviewing", c_interv)
    col3.metric("Offered", c_offered)
    col4.metric("Rejected", c_rejected)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("### Active Applications Directory")
    
    for app in apps:
        # Status color
        status = app["status"]
        color = "#3B82F6" if status == "Applied" else "#F59E0B" if status == "Interviewing" else "#10B981" if status == "Offered" else "#EF4444"
        
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1.2rem; border-radius: 8px; margin-bottom: 0.8rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div>
                <strong style="color: #0F172A; font-size: 1.1rem;">{app['title']}</strong>
                <div style="color: #475569; font-size: 0.90rem; margin-top: 4px;">🏢 {app['company']}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="font-size: 0.85rem; color: #64748B; text-align: right;">
                    <strong>Tracked Status</strong>
                </div>
                <div style="background-color: {color}20; color: {color}; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 0.90rem;">
                    {status.upper()}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
