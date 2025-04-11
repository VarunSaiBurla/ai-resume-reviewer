import streamlit as st
from ai_resume_reviewer import review_resume
import tempfile

st.title("🧠 AI Resume Reviewer")
st.markdown("Upload your resume PDF and get AI-generated feedback.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        feedback = review_resume(tmp.name)
        st.subheader("Feedback:")
        st.text_area("AI Suggestions", feedback, height=400)
