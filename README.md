DataTalk: Conversational BI with LangChain + Gemini + FastAPI
DataTalk is a proof-of-concept application that bridges the gap between complex databases and everyday users. It provides a simple chat interface where anyone can ask questions in plain English and receive immediate, AI-powered insights and data from a connected database.

✨ Key Features
Natural Language to SQL: Ask complex questions like "What were the total sales for the North region last week?" and get real answers.

AI-Powered Summaries: The LangChain SQL Agent, powered by Google's Gemini model, provides a human-readable summary of the findings.

Raw Data Display: The frontend dynamically renders a table to show the exact data used for the summary.

Simple & Fast Backend: Built with FastAPI for a high-performance, asynchronous API.

Secure Configuration: Uses a .env file to safely manage your API keys.

🔧 Tech Stack
AI Core: LangChain, LangChain Community (v0.2+), Google Gemini (gemini-1.5-flash-latest)

Backend: FastAPI, Uvicorn, Pydantic

Database: SQLite (for this demo)

Frontend: Vanilla HTML, CSS, and JavaScript

🚀 Getting Started
Follow these steps to get a local copy up and running.

Prerequisites
Python 3.10+

A Google AI Studio API key with the Gemini API enabled.

Git installed on your system.

1. Clone the Repository
git clone https://github.com/rushibedre/DataTalk-AI-BI-Tool.git
cd DataTalk-AI-BI-Tool

2. Create and Activate Virtual Environment
It's highly recommended to use a virtual environment to keep dependencies isolated.

Windows (PowerShell):

python -m venv venv
.\venv\Scripts\Activate.ps1

macOS / Linux:

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
python -m pip install -U fastapi uvicorn langchain langchain-community langchain-google-genai google-generativeai python-dotenv pydantic

4. Configure Your API Key
Create a file named .env in the root of the project folder.

Add your Google API key to this file like so:

GOOGLE_API_KEY=your_real_google_api_key_here

(Important: Do not use quotes around the key.)

5. Initialize the Database
This one-time command creates the sales_data.db file and fills it with sample data.

python backend/database.py

You should see the message: Database 'sales_data.db' created successfully with sample data.

6. Run the Application!
python backend/main.py

Your DataTalk application is now running! Open your browser and navigate to:
http://localhost:8000

💡 How It Works
The application's logic is straightforward:

The FastAPI backend serves the static HTML/CSS/JS frontend and exposes a /query API endpoint.

When a user asks a question, the frontend sends a POST request to /query.

The backend invokes a LangChain SQL Agent.

The agent, powered by Google Gemini, uses its SQLDatabaseToolkit to inspect the database schema.

It constructs a SQL query, executes it, and analyzes the results.

Finally, it generates a natural language summary and returns it to the frontend to be displayed.

🛠️ Customization & Troubleshooting
<details>
<summary><strong>Error: "GOOGLE_API_KEY environment variable is not set."</strong></summary>

Ensure the .env file is in the project's root folder (at the same level as backend and frontend).

Make sure the file is named exactly .env and not .env.txt.

Confirm the content is GOOGLE_API_KEY=yourkey with no quotes.

Restart the server after creating or modifying the .env file.

</details>

<details>
<summary><strong>How do I change the AI model?</strong></summary>

In backend/llm_core.py, you can change the model name in the ChatGoogleGenerativeAI initialization. For example, to use the more powerful Pro model:
model="gemini-1.5-pro"
(Note: This may have different pricing and rate limits.)

</details>

<details>
<summary><strong>How do I use a different port?</strong></summary>

In the last line of backend/main.py, change the port number:
uvicorn.run(app, host="0.0.0.0", port=8001)

</details>

🔐 Security
API Keys: The .env file is included in .gitignore to prevent you from accidentally committing your secrets to GitHub. Always use environment variables for sensitive data.

Deployment: This application is a demo and does not include production-level security features like authentication or rate limiting.

🙏 Acknowledgments
FastAPI

LangChain

Google AI & Gemini
