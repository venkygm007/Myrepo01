import streamlit as st

st.set_page_config(page_title="Azure Streamlit App", page_icon="🚀")

st.title("🚀 Streamlit on Azure App Service")

st.write("""
This is a Streamlit application running on Azure!
""")

name = st.text_input("What's your name?")
if name:
    st.success(f"Hello, {name}! Welcome to your Azure-hosted Streamlit app.")

st.sidebar.header("Settings")
st.sidebar.write("Configure your app here.")
