import streamlit as st

def render_match_metric(score: int):
    # Determine color
    color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
    st.markdown(f"""
    <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 1.5rem;">
        <span style="font-size: 0.95rem; font-weight: bold; color: #64748B; text-transform: uppercase;">Job Compatibility Match</span>
        <h1 style="color: {color}; font-size: 3.5rem; margin: 0.5rem 0;">{score}%</h1>
        <div style="background-color: #F1F5F9; border-radius: 9999px; height: 12px; width: 100%; overflow: hidden; margin-top: 10px;">
            <div style="background-color: {color}; height: 100%; width: {score}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
