import streamlit as st
import pandas as pd
from llamaindex.llama_gen import init_engine, get_llm_response 

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'pending_response' not in st.session_state:
    st.session_state['pending_response'] = None

st.header("Agent V2: Autonomous (Llamaindex)")
st.title("SQL Data Analyst Agent")

if "db_path" not in st.session_state:
    st.write("File not uploaded.")
    st.stop()

db_path = st.session_state["db_path"]

if "current_db_path" not in st.session_state or st.session_state["current_db_path"] != db_path:
    with st.spinner("Initializing AI Agent & Indexing Database..."):
        engine, query_engine = init_engine(db_path)
        st.session_state["agent_engine"] = engine
        st.session_state["agent_query_engine"] = query_engine
        st.session_state["current_db_path"] = db_path
        st.toast("AI Agent Ready!", icon="🚀")

active_engine = st.session_state["agent_engine"]
active_query_engine = st.session_state["agent_query_engine"]

for i in st.session_state["message_history"]:
    with st.chat_message(i["role"]):
        st.write(i["message"])

        if "SELECT" in i["message"]:
            st.code(i["message"], language = "sql")
        
        if "chart" in i:
            st.bar_chart(i["chart"], x="Category", y="Value")
            csv = i["chart"].to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Data as CSV",
                csv,
                "query_results.csv",
                "text/csv"
            )

prompt = st.chat_input("Enter your question")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state['message_history'].append({"role": "user", "message": prompt})

    with st.spinner("Analyzing database schema..."):
        answer = get_llm_response(active_query_engine, prompt)

    st.session_state["pending_response"] = answer
    
    with st.chat_message("assistant"):
        st.write("A sql query has been generated. Please verify it before approving the execution.")


def run_sql():
    ans = st.session_state["pending_response"].response
    query = st.session_state["pending_response"].metadata["sql_query"]

    history_entry = {"role": "assistant", "message": ans}

    try:
        data = pd.read_sql(query, active_engine)

        if not data.empty and len(data) > 1 and data.shape[1] == 2:
            if isinstance(data.iloc[0, 1], (int, float)):
                data.columns = ["Category", "Value"]
                history_entry["chart"] = data
    
    except Exception as e:
        print(f"Chart generation failed:{e}")
    
    st.session_state["message_history"].append(history_entry)

    st.session_state["pending_response"] = None


def cancel():
    st.session_state["pending_response"] = None


if st.session_state["pending_response"] is not None:
    st.divider()
    st.code(st.session_state["pending_response"].metadata["sql_query"], language = "sql")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Run Query", on_click=run_sql, type="primary")
    with col2:
        st.button("Cancel", on_click=cancel)