import streamlit as st
from ai_resume_reviewer import review_resume
import tempfile
import openai

st.set_page_config(page_title="AI Resume Reviewer", page_icon="🧠")

st.title("🧠 AI Resume Reviewer")
st.markdown("Upload your resume PDF and get GPT-4 powered feedback.")

# --- API Key Input ---
user_api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

if not user_api_key:
    with st.spinner("Waiting for API key input..."):
        st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

openai.api_key = user_api_key

# --- Resume Upload ---
uploaded_file = st.file_uploader("📄 Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    with st.spinner("Analyzing your resume..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            feedback = review_resume(tmp.name)
        st.subheader("📋 AI Feedback:")
        st.text_area("Suggestions", feedback, height=400)
