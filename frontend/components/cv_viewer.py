import streamlit as st

def render_cv_header(name: str, email: str, filename: str):
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h3 style="margin: 0; color: #1E3B8B;">👤 {name}</h3>
            <span style="color: #64748B; font-size: 0.9rem;">Email: {email} | File: {filename}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
