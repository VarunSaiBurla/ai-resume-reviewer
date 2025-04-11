import streamlit as st

st.set_page_config(page_title="AI Resume Reviewer", page_icon="🧠")

st.title("🧠 AI Resume Reviewer")
st.markdown("Hello! If you're seeing this, the app is rendering correctly. 🎉")

# Check API key input
api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

if not api_key:
    st.warning("Please enter your API key to continue.")
    st.stop()

st.success("API key received.")
