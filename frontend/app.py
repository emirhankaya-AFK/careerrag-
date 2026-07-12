import streamlit as st

st.set_page_config(
    page_title="CareerRAG - AI Job Matcher",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styles
st.markdown("""
<style>
    .title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #475569;
        margin-bottom: 2rem;
    }
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border: 1px solid #E2E8F0;
        text-align: center;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💼 CareerRAG</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Agentic Resume Parser, ATS Job Matcher, and Interview Prep System</div>', unsafe_allow_html=True)

st.write(
    "Welcome to **CareerRAG**, your AI recruiter copilot. "
    "Upload CVs in PDF/DOCX formats, parse experience parameters, "
    "automatically search and scrape jobs, perform detailed skill gap analysis, "
    "and simulate mock interview questions customized to your CV."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📄 CV Parser</h3>
        <p>Extracts contact details, standardized skills, duration-mapped experiences, and academic qualifications.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📊 ATS Matcher</h3>
        <p>Applies exact matching weights for required skills, location fits, and experience seniorities.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>💬 Interview Coach</h3>
        <p>Generates custom technical questions and aligns key talking points from your CV history.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

st.subheader("Implementation Steps")
st.markdown("""
1. Navigate to **01_upload_cv** in the sidebar to upload your PDF/DOCX resume.
2. Review your structured CV profile and standard skills list in **02_my_profile**.
3. Import job descriptions or paste LinkedIn posting URLs in **03_add_job**.
4. Score your matching and roadmap gaps under **04_matching**.
5. Practice customized mock interview questions under **05_interviews**.
6. Track applications workflow under **06_applications**.
""")
st.sidebar.info("Select a page above to start.")
st.sidebar.markdown("---")
st.sidebar.caption("CareerRAG Engine v1.0.0")
