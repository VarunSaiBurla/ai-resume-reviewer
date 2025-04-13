import streamlit as st
import openai
from ai_resume_reviewer import review_resume
import tempfile

st.set_page_config(page_title="AI Resume Reviewer", page_icon="🧠")
st.title("🧠 AI Resume Reviewer")
st.markdown("Upload your resume PDF and get GPT-4 powered feedback.")

user_api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")
if not user_api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

openai.api_key = user_api_key  # Must be set before import functions are called

uploaded_file = st.file_uploader("📄 Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp.flush()
        feedback = review_resume(tmp.name)
        st.subheader("📋 AI Feedback:")
        st.text_area("Suggestions", feedback, height=400)
