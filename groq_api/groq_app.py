import streamlit as st
import pandas as pd
from groq_api.sql_gen import init_data, generate_sql, get_results, summarize_results 

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'sql_query' not in st.session_state:
    st.session_state['sql_query'] = None

if 'user_question' not in st.session_state:
    st.session_state['user_question'] = None

st.header("Agent V1: Manual (Groq API)")
st.title("SQL Data Analyst Agent")

if "db_path" not in st.session_state:
    st.write("File not uploaded.")
    st.stop()

db_path = st.session_state["db_path"]

if "current_db_path" not in st.session_state or st.session_state["current_db_path"] != db_path:
    with st.spinner("Initializing AI Agent & Extracting schemas..."):
        db_info = init_data(db_path)
        st.session_state["db_info"] = db_info
        st.session_state["current_db_path"] = db_path
        st.toast("AI Agent Ready!", icon="🚀")

db_info = st.session_state["db_info"]

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
        query = generate_sql(prompt, db_info)

    st.session_state["sql_query"] = query
    st.session_state["user_question"] = prompt
    
    msg = "A sql query has been generated. Please verify it before approving the execution."
    st.session_state['message_history'].append({"role": "assistant", "message": query})

    with st.chat_message("assistant"):
        st.write(msg)


def run_sql():
    query = st.session_state["sql_query"]
    prompt = st.session_state["user_question"]

    res = get_results(st.session_state["current_db_path"], query)

    if isinstance(res, (str)):
        with st.chat_message("assistant"):
            st.write("The query could not be executed.")
        st.session_state["sql_query"] = None
        st.session_state['user_question'] = None

    else:
        final_res = summarize_results(prompt, res)

        history_entry = {"role": "assistant", "message": final_res}

        if res and len(res) > 1 and len(res[0]) == 2:
            if isinstance(res[0][1], (int, float)):
                df = pd.DataFrame(res, columns = ['Category', 'Value'])
                history_entry["chart"] = df
                
        st.session_state['message_history'].append(history_entry)

        st.session_state["sql_query"] = None

def cancel():
    st.session_state["sql_query"] = None
    st.session_state['user_question'] = None

if st.session_state["sql_query"] is not None:
    st.divider()
    st.code(st.session_state["sql_query"], language = "sql")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Run Query", on_click=run_sql, type="primary")
    with col2:
        st.button("Cancel", on_click=cancel)