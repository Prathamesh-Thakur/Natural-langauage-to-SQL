import sqlite3
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# db_file = r"..\data\Chinook_Sqlite.sqlite"

def init_data(db_path):
    conn = sqlite3.connect(db_path)

    cur = conn.cursor()

    cur.execute("SELECT name from sqlite_master WHERE type = 'table';")
    all_tables = cur.fetchall()
    db_info = ""

    for table_name in all_tables:
        db_info += f"Table: {table_name[0]}\n"
        query = f"PRAGMA table_info({table_name[0]});"
        cur.execute(query)
        schema = cur.fetchall()
        columns = []
        for column in schema:
            columns.append(f"{column[1]} ({column[2]})")
        
        db_info += f"Columns: {', '.join(columns)}\n\n"
    
    conn.close()

    return "\n\n".join(db_info)

def generate_sql(user_prompt, schema):
    system_prompt = f"""Consider yourself to be an expert SQLite Analyst. You are given a database with these specific tables
                    and their schemas: {schema}. Based on the given user prompt, give a valid SQL sqlite query that can be executed
                    on the database. Only give SELECT statement queries, and reject any other types that require modification of the
                    database. Return only the query without any markdown or other formatting. If any other type of statements are asked,
                    just reject it, do not provide any reasoning or alternative queries."""
    
    client = Groq(
        api_key = os.getenv("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature = 0
    )

    query = chat_completion.choices[0].message.content
    query = query.replace("```", "")

    return query


def get_results(db_path, sql_query):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri = True)
    cur = conn.cursor()

    try:
        cur.execute(sql_query)
        results = cur.fetchall()
        conn.close()

        return results
    except Exception as e:
        conn.close()
        return f"Error:{e}"
    finally:
        conn.close()


def summarize_results(user_question, results):
    system_prompt = f"""Consider yourself to be an expert data analyst. The user asked the following question: {user_question}
                    Based on the results which will be provided, create a clean, concise summary which addresses the question.
                    Return only the answer without any formatting."""
    
    user_prompt = f"Given these results: {results}, give an answer to the user question."
    
    client = Groq(
        api_key = os.getenv("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature = 0
    )

    answer = chat_completion.choices[0].message.content
    answer = answer.replace("```", "")
    answer = answer.strip()

    return answer