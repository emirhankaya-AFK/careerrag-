import streamlit as st
import requests

BACKEND_URL = "http://localhost:8003"

st.set_page_config(page_title="Upload CV - CareerRAG", layout="wide")

st.title("📂 Upload Resume / CV")
st.write("Upload candidate resumes (PDF or DOCX) to extract parameters and index qualifications.")

uploaded_file = st.file_uploader("Choose CV file", type=["pdf", "docx"])

if uploaded_file:
    if st.button("🚀 Parse & Extract Resume"):
        with st.spinner("Parsing text blocks and running entity extraction..."):
            try:
                # Setup files multipart
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/octet-stream")}
                res = requests.post(f"{BACKEND_URL}/cv/upload", files=files)
                if res.status_code == 200:
                    st.success("CV uploaded and indexed successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to parse CV: {res.json().get('detail')}")
            except Exception as e:
                st.error(f"Connection error to backend: {e}")

st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.subheader("📋 Managed Resumes")

try:
    res = requests.get(f"{BACKEND_URL}/cv")
    if res.status_code == 200:
        cvs = res.json()
        if not cvs:
            st.info("No resumes uploaded yet.")
        else:
            for cv in cvs:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"📄 **{cv['name']}** (`{cv['email']}`) | File: `{cv['filename']}` | Uploaded: {cv['upload_date']}")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{cv['id']}"):
                        del_res = requests.delete(f"{BACKEND_URL}/cv/{cv['id']}")
                        if del_res.status_code == 200:
                            st.success(f"Deleted {cv['name']}")
                            st.rerun()
                        else:
                            st.error("Failed to delete resume.")
    else:
        st.error("Could not fetch resumes from backend.")
except Exception as e:
    st.error(f"Connection error: {e}")
