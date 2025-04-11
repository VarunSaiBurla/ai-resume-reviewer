import streamlit as st

st.set_page_config(page_title="Debugger", page_icon="🐞")
st.title("🐞 Streamlit App Debugger")

try:
    st.success("✅ Streamlit started successfully!")

    import os
    st.write("Working directory:", os.getcwd())

    st.write("Trying to render input field...")
    val = st.text_input("Just a test input")
    if val:
        st.success(f"You typed: {val}")

except Exception as e:
    st.error(f"❌ An error occurred: {e}")
