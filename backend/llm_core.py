# backend/llm_core.py

import os
from pathlib import Path

# Load .env from project root explicitly (robust even if imported elsewhere)
from dotenv import load_dotenv
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

from langchain_community.utilities import SQLDatabase

# Updated imports for LangChain v0.2+
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# Google Gemini chat model via LangChain
from langchain_google_genai import ChatGoogleGenerativeAI

# -- 1. SETUP THE DATABASE CONNECTION --
db = SQLDatabase.from_uri("sqlite:///sales_data.db")

# -- 2. SETUP THE GEMINI LLM --
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise RuntimeError(
        "GOOGLE_API_KEY environment variable is not set. "
        "Ensure .env at project root contains 'GOOGLE_API_KEY=...' (no quotes), "
        "or set it in your shell before running."
    )

# Use gemini-1.5-flash-latest (fast, tool-capable)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0,
    convert_system_message_to_human=True,
    api_key=google_api_key  # critical: pass explicitly to avoid ADC fallback
)

# -- 3. CREATE THE LANGCHAIN SQL AGENT --
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,               # helpful for debugging
    agent_type="openai-tools",  # tool-call pattern used across providers
    handle_parsing_errors=True
)

# -- CUSTOM PROMPT --
AGENT_PROMPT = """
You are a helpful and friendly business intelligence assistant named DataTalk.
You are designed to answer questions about the company's sales data.
You have access to a database with the following table:

- sales: Contains records of each sale, including product name, category, region, sale date, quantity, unit price, and total price.
  When asked for "sales" or "revenue", you must use the `total_price` column.

Process:
1) Understand the user's question precisely.
2) Use your tools to generate and execute an appropriate SQL query.
3) Summarize the findings clearly and concisely.

Rules:
- Use only the available database schema.
- Prefer accurate SQL that returns the minimal necessary columns.
- If grouping or filtering by dates, be explicit about the range.
- For revenue/sales totals, always aggregate on `total_price`.
"""
