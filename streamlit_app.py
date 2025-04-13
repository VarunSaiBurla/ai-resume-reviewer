import streamlit as st
import tempfile
from ai_resume_reviewer import review_resume

st.set_page_config(page_title="AI Resume Reviewer", page_icon="🧠")
st.title("🧠 AI Resume Reviewer")
st.markdown("Upload your resume PDF and get GPT-4 powered feedback.")

# 🔐 User provides their own key
user_api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

if not user_api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

uploaded_file = st.file_uploader("📄 Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())

    with st.spinner("Analyzing your resume..."):
        try:
            feedback = review_resume(tmp.name, user_api_key)
            st.subheader("📋 AI Feedback:")
            st.text_area("Suggestions", feedback, height=400)
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
