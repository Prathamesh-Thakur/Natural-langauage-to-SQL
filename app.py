import streamlit as st
from utils import get_db_path 

st.set_page_config(page_title="AI Data Analyst", layout="wide")

uploaded_file = st.file_uploader("Upload a csv or sqlite file.", type = ["csv", "sqlite"])

if uploaded_file is not None:
    with st.spinner("Processing Data"):
        db_path = get_db_path(uploaded_file)

        st.session_state["db_path"] = db_path
        st.session_state["file_name"] = uploaded_file.name    
    
    st.success(f"Loaded: {uploaded_file.name}")
    st.info("Select an AI Agent from the sidebar to begin analysis.")
    
pages = [
        st.Page("groq_api/groq_app.py", title = "Agent V1: Manual (Groq API)"),
        st.Page("llamaindex/llamaindex_app.py", title = "Agent V2: Autonomous (Llamaindex)")
    ]

pg = st.navigation(pages)
pg.run()