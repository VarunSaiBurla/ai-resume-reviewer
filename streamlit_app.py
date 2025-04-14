# streamlit_app.py
import streamlit as st
from ai_resume_reviewer import review_resume, score_resume, extract_missing_sections
import tempfile
import openai

st.set_page_config(page_title="AI Resume Reviewer", page_icon="🧠")

st.title(":brain: AI Resume Reviewer")
st.markdown("Upload your resume PDF and get GPT-4 powered feedback with a score and improvement tips.")

with st.sidebar:
    st.header(":lock: Settings")
    user_api_key = st.text_input("Enter your OpenAI API key", type="password")
    if not user_api_key:
        st.warning("Please enter your OpenAI API key to continue.")
        st.stop()

openai.api_key = user_api_key

uploaded_file = st.file_uploader(":page_facing_up: Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        uploaded_file.seek(0)
        tmp.write(uploaded_file.read())
        with st.spinner("Analyzing your resume..."):
            feedback = review_resume(tmp.name, user_api_key)
            score = score_resume(tmp.name)
            missing_sections = extract_missing_sections(tmp.name)

    st.success("Analysis complete!")

    st.metric("Resume Score", f"{score}/100")

    with st.expander(":clipboard: AI Feedback"):
        st.text_area("Suggestions", feedback, height=300)

    with st.expander(":mag: Suggested Improvements"):
        for section in missing_sections:
            st.markdown(f"- {section}")

    if score >= 80:
        st.success("Great job! Your resume looks strong.")
    elif score >= 60:
        st.info("Your resume is good, but there are areas to improve.")
    else:
        st.warning("Consider significant improvements for better impact.")
