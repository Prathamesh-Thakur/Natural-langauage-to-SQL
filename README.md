# Text-to-SQL AI Data Analyst

An intelligent data analysis application that converts natural language questions into SQL queries and provides insights from your data. This project features two AI agents powered by Groq's LLM API and LlamaIndex, enabling both manual and autonomous query generation.

## Project Overview

This application provides a Streamlit-based interface for analyzing data through conversational AI. Users can upload CSV or SQLite files and ask natural language questions to get instant SQL queries and data-driven answers.

### Features

- **Dual AI Agents**: Choose between two approaches for data analysis
  - **Agent V1 (Groq API)**: Manual SQL generation with step-by-step control
  - **Agent V2 (LlamaIndex)**: Autonomous agent with intelligent query planning
- **Multi-format Support**: Upload CSV files or existing SQLite databases
- **Natural Language Processing**: Ask questions in plain English
- **SQL Query Visualization**: View generated SQL queries and results
- **Data Export**: Download query results as CSV files
- **Interactive Chat Interface**: Real-time conversation with the AI agent

## Project Structure

```
Text-to-SQL/
├── app.py                          # Main Streamlit application entry point
├── utils.py                        # Utility functions for file handling and database conversion
├── requirements.txt                # Project dependencies
├── LICENSE                         # License file
├── README.md                       # Project documentation
├── groq_api/                       # Groq API-based agent (Manual)
│   ├── groq_app.py                # Streamlit UI for Groq agent
│   └── sql_gen.py                 # SQL generation and query execution logic
├── llamaindex/                    # LlamaIndex-based agent (Autonomous)
│   ├── llamaindex_app.py          # Streamlit UI for LlamaIndex agent
│   └── llama_gen.py               # LlamaIndex engine initialization and response
├── data/                          # Sample data directory
├── temp_data/                     # Temporary storage for uploaded files
└── myenv/                         # Python virtual environment

```

## Technology Stack

### Core Framework
- **Streamlit**: Web application framework for the UI
- **SQLAlchemy**: SQL database access and ORM
- **SQLite3**: Database engine

### AI & Language Models
- **Groq API**: Fast inference for Llama 3.3-70B model
- **LlamaIndex**: Structured data indexing and querying framework
- **HuggingFace Embeddings**: BAAI/bge-small-en-v1.5 for semantic understanding

### Data Processing
- **Pandas**: Data manipulation and analysis
- **Python-dotenv**: Environment variable management

## Setup Instructions

### Prerequisites
- Python 3.13+
- Groq API key (get one at https://console.groq.com)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "Text-to-SQL"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   # On Windows
   myenv\Scripts\activate
   # On macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs all required packages for both agents:
   - pandas
   - dotenv
   - streamlit
   - groq
   - llama-index
   - llama-index-llms-groq
   - llama-index-embeddings-huggingface
   - sqlalchemy

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Running the Application

### Start the Streamlit app
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Usage Workflow

1. **Upload Data**: Click the file uploader and select a CSV or SQLite file
2. **Select Agent**: Choose between Agent V1 (Manual) or Agent V2 (Autonomous) from the sidebar
3. **Ask Questions**: Type your question in natural language (e.g., "What are the top 5 customers by sales?")
4. **View Results**: The agent generates SQL, executes it, and displays results
5. **Export Data**: Download results as CSV if needed

## Agent Comparison

| Feature | Agent V1 (Groq) | Agent V2 (LlamaIndex) |
|---------|-----------------|----------------------|
| **Approach** | Manual SQL generation | Autonomous with planning |
| **LLM** | Groq Llama 3.3-70B | Groq Llama 3.3-70B |
| **Processing** | Step-by-step | End-to-end autonomous |
| **Best For** | Direct SQL queries | Complex multi-step analysis |
| **Speed** | Fast | Moderate |

## Example Queries

- "Show me the top 10 highest-selling products"
- "What is the average customer spending by region?"
- "List all orders placed in the last 30 days"
- "Which customer has made the most purchases?"
- "Generate a summary of monthly sales trends"

## API Keys & Authentication

The application uses Groq's API for LLM inference. Ensure you have:
1. A valid Groq API key from https://console.groq.com
2. The key stored in your `.env` file as `GROQ_API_KEY`

## File Format Support

### CSV Files
- Automatically converted to SQLite database
- Column names are normalized (spaces removed, lowercase)
- Stored as `uploaded_data` table

### SQLite Files
- Used directly without conversion
- All existing tables are available for querying

## Troubleshooting

### Common Issues

**"File not uploaded" error**
- Make sure to upload a file before selecting an agent

**API Key errors**
- Verify `GROQ_API_KEY` is set correctly in `.env`
- Check key validity at https://console.groq.com

**Query execution errors**
- Ensure table and column names are correct
- Check if your question matches the available data structure

**Slow performance**
- Large files may take time to process initially
- Agent V2 is more thorough but slower than Agent V1

## Development Notes

- The application uses read-only database connections for safety
- Temporary uploaded files are stored in `temp_data/`
- Session state management maintains chat history and database context
- SQL queries are generated using system prompts that enforce safety constraints

## Future Enhancements

- Support for more database types (PostgreSQL, MySQL, etc.)
- Advanced data visualization options
- Query optimization suggestions
- Multi-table join support improvements
- Custom model fine-tuning for domain-specific queries


## Support

For issues or questions, please check:
- Groq API documentation: https://console.groq.com/docs
- LlamaIndex documentation: https://docs.llamaindex.ai
- Streamlit documentation: https://docs.streamlit.io
