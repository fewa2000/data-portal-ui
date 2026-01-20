"""
Data Portal UI - Main Entry Point
"""

import streamlit as st

st.set_page_config(
    page_title="Data Portal",
    page_icon="📊",
    layout="wide",
)

st.title("Data Portal")
st.markdown("Welcome to the Data Portal. Use the sidebar to navigate.")

st.info("Select a page from the sidebar to get started.")
