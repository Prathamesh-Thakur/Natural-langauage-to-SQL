import time
import pandas as pd
from llamaindex.llama_gen import init_engine, get_llm_response

# Configuration
DB_PATH = "data/Chinook_Sqlite.sqlite"
DELAY_BETWEEN_CALLS = 10 # Seconds to wait to bypass Groq rate limits

# # Benchmark Dataset (Mix of easy, medium, and hard)
questions = [
    "How many total tracks are in the database?", # Easy (Count)
    "What are the names of all the genres?", # Easy (Select)
    "List the top 5 longest tracks.", # Easy (Order By, Limit)
    "Who is the manager of employee Jane Peacock?", # Medium (Self Join)
    "How many tracks does the album 'Restless and Wild' have?", # Medium (Join 2 tables)
    "Which artist has the most albums?", # Medium (Group By, Join)
    "Show me the total sales (invoice lines) for the track 'The Trooper'.", # Hard (Join 3 tables)
    "Which customer has spent the most money in total?", # Hard (Join, Group By, Sum)
    "What is the most popular genre by total tracks sold?", # Hard (Join 4 tables, Aggregation)
    "List all employees who have never supported a customer." # Hard (Left Join / Subquery)
]

def run_benchmark():
    print("🚀 Initializing AI Agent for Benchmarking...")
    engine, query_engine = init_engine(DB_PATH)
    
    results = []
    
    print(f"📊 Starting benchmark of {len(questions)} queries...")
    print("-" * 50)
    
    for idx, q in enumerate(questions, 1):
        print(f"[{idx}/{len(questions)}] Asking: {q}")
        
        start_time = time.time()
        try:
            # Run the AI
            answer = get_llm_response(query_engine, q)
            latency = time.time() - start_time
            
            # Extract SQL (LlamaIndex stores it in metadata)
            sql_query = answer.metadata.get("sql_query", "No SQL extracted")
            
            # Test Execution (Does the SQL actually run without crashing?)
            pd.read_sql(sql_query, engine)
            execution_status = "Pass"
            
        except Exception as e:
            latency = time.time() - start_time
            sql_query = str(e)
            execution_status = "Fail"
            
        print(f"   ⏱️ Latency: {latency:.2f}s | 🛠️ Execution: {execution_status}")
        
        results.append({
            "Question": q,
            "Latency (s)": round(latency, 2),
            "Execution": execution_status,
            "Generated SQL": sql_query
        })
        
        # Rate Limit Buffer
        if idx < len(questions):
            print(f"   ⏳ Sleeping for {DELAY_BETWEEN_CALLS}s to respect rate limits...\n")
            time.sleep(DELAY_BETWEEN_CALLS)
            
    # Calculate and Save Metrics
    df = pd.DataFrame(results)
    avg_latency = df["Latency (s)"].mean()
    success_rate = (len(df[df["Execution"] == "Pass"]) / len(df)) * 100
    
    print("-" * 50)
    print("🏁 BENCHMARK COMPLETE")
    print(f"Average Latency: {avg_latency:.2f} seconds")
    print(f"Execution Success Rate: {success_rate:.0f}%")
    
    df.to_csv("benchmark_results.csv", index=False)
    print("Detailed results saved to 'benchmark_results.csv'.")

if __name__ == "__main__":
    run_benchmark()