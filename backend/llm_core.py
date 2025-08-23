# backend/llm_core.py

import os
from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

# --- 1. SETUP THE DATABASE CONNECTION ---
# This part remains the same.
db = SQLDatabase.from_uri("sqlite:///sales_data.db")

# --- 2. SETUP THE OLLAMA LLM ---
# This part remains the same.
llm = Ollama(model="llama3:8b", temperature=0)

# --- 3. CREATE THE LANGCHAIN SQL AGENT ---
# This is the new, more powerful approach.
# The SQLDatabaseToolkit provides the tools the agent can use (e.g., query, get schema).
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# The create_sql_agent function initializes an agent with the LLM, the toolkit,
# and specific instructions on how to behave.
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,  # This is crucial for debugging; it shows the agent's thoughts.
    agent_type="openai-tools", # A standard agent type that works well.
    handle_parsing_errors=True # Helps the agent recover from its own mistakes.
)

# --- CUSTOM PROMPT (Optional but Recommended) ---
# We can give our agent a more defined personality and instructions.
# Note: The agent prompt structure is different from the old chain prompt.
AGENT_PROMPT = """
You are a helpful and friendly business intelligence assistant named DataTalk.
You are designed to answer questions about the company's sales data.
You have access to a database with the following table:

- **sales**: Contains records of each sale, including product name, category, region, sale date, quantity, unit price, and total price. When asked for "sales" or "revenue", you must use the `total_price` column.

Given a user's question, you must first understand the question and then use your tools to generate and execute a SQL query to find the answer.
Finally, provide a clear, natural language summary of the findings.
"""