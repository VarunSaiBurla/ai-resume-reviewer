import streamlit as st
from ai_resume_reviewer import review_resume, score_resume, extract_missing_sections
import tempfile
import openai

st.set_page_config(page_title="AI Resume Reviewer", page_icon="🧠")

st.title(":brain: AI Resume Reviewer")
st.markdown("Upload your resume PDF and get GPT-4 powered feedback with a score and improvement tips.")

with st.sidebar:
    st.header(":key: Settings")
    user_api_key = st.text_input("Enter your OpenAI API key", type="password")
    st.markdown("🔗 [Get your API Key](https://platform.openai.com/account/api-keys)")
    st.markdown("📄 [Download Sample Resume](https://example.com/sample_resume.pdf)")
    if not user_api_key:
        st.warning("Please enter your OpenAI API key to continue.")
        st.stop()

uploaded_file = st.file_uploader(":page_facing_up: Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Analyzing your resume..."):
        feedback = review_resume(tmp_path, user_api_key)
        score = score_resume(tmp_path)
        missing_sections = extract_missing_sections(tmp_path)

    st.success("Analysis complete!")

    col1, col2 = st.columns([1, 2])
    col1.metric("Resume Score", f"{score}/100")
    with col2:
        if score >= 80:
            st.success("Great job! Your resume looks strong.")
        elif score >= 60:
            st.info("Your resume is good, but there are areas to improve.")
        else:
            st.warning("Consider significant improvements for better impact.")

    st.markdown("### 📋 AI Feedback")
    with st.expander("View Detailed Feedback"):
        st.text_area("Suggestions", feedback, height=300)

    st.markdown("### 🧠 Suggested Improvements")
    with st.expander("Missing or Weak Sections"):
        for section in missing_sections:
            st.markdown(f"- {section}")

    st.download_button("🔗 Download Feedback", feedback, file_name="resume_feedback.txt")