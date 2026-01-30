import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, inspect
from llama_index.llms.groq import Groq
from llama_index.core import SQLDatabase, Settings
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine

load_dotenv()

Settings.llm = Groq(model = "llama-3.3-70b-versatile", api_key = os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def init_engine(db_path):
    engine = create_engine(f"sqlite:///{db_path}?mode=ro", connect_args = {"uri": True})
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    sql_database = SQLDatabase(engine)
    table_node_mapping = SQLTableNodeMapping(sql_database)
    table_schema_objs = [SQLTableSchema(table_name = table) for table in table_names]

    obj_index = ObjectIndex.from_objects(table_schema_objs, table_node_mapping, VectorStoreIndex)
    
    query_engine = SQLTableRetrieverQueryEngine(sql_database, obj_index.as_retriever(similarity_top_k = 3))

    return engine, query_engine

def get_llm_response(query_engine, query_str):
    response = query_engine.query(query_str)
    return response

if __name__ == "__main__":
    query = "Who is the top selling artist?"
    print(get_llm_response(query))