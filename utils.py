import pandas as pd
import sqlite3
import os

def get_db_path(uploaded_file):
    if not os.path.exists("temp_data"):
        os.makedirs("temp_data")

    file_path = os.path.join("temp_data", uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith(".csv"):
        db_path = file_path.replace(".csv", ".sqlite")
        
        df = pd.read_csv(file_path)
        
        df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
        
        conn = sqlite3.connect(db_path)
        df.to_sql("uploaded_data", conn, if_exists="replace", index=False)
        conn.close()
        
        return db_path
        
    else:
        return file_path