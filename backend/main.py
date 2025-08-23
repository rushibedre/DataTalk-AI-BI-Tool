# backend/main.py
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env from project root BEFORE importing llm_core
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

# Optional debug (remove after verifying):
print("DEBUG .env:", ROOT_DIR / ".env")
print("DEBUG GOOGLE_API_KEY length:", len(os.getenv("GOOGLE_API_KEY") or ""))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Import after .env is loaded
from llm_core import agent_executor, AGENT_PROMPT

# FastAPI app
app = FastAPI()

# Resolve frontend directory and mount it for static files
FRONTEND_DIR = ROOT_DIR / "frontend"  # Make sure the folder is named 'frontend'
if not FRONTEND_DIR.exists():
    raise RuntimeError(f"Frontend directory not found at: {FRONTEND_DIR}")

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

class Query(BaseModel):
    question: str

INDEX_FILE = FRONTEND_DIR / "index.html"
if not INDEX_FILE.exists():
    raise RuntimeError(f"index.html not found at: {INDEX_FILE}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the main index.html file."""
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/query")
async def handle_query(query: Query):
    """
    Handles user questions by invoking the LangChain SQL Agent.
    Also instructs the agent to return a JSON object with 'rows' for rendering.
    """
    try:
        print("--- 1. Received query from frontend ---")

        prompt = f"""{AGENT_PROMPT}

Question: {query.question}

Return format requirement:
- In addition to the natural language answer, also return a pure JSON object on a new line with the exact key "rows" containing the SQL result set as an array of arrays (one entry per row).
- Do not wrap JSON in markdown code fences.
- Example:
Answer: <your explanation here>
{{"rows": [[...], [...]]}}
"""

        print("--- 2. Sending prompt to LangChain Agent... ---")

        result = agent_executor.invoke({"input": prompt})
        print("--- 3. Received result from Agent ---")

        # Preferred final answer slot
        summary = result.get("output", "I couldn't find an answer.")

        # Try to extract the trailing {"rows": [...]} from the summary
        rows = []
        try:
            import json, re
            json_candidates = re.findall(r'(\{.*\})', summary, flags=re.DOTALL)
            for candidate in reversed(json_candidates):
                try:
                    obj = json.loads(candidate)
                    if isinstance(obj, dict) and "rows" in obj and isinstance(obj["rows"], list):
                        rows = obj["rows"]
                        # Strip the JSON blob from the summary shown to the user
                        summary = summary.replace(candidate, "").strip()
                        break
                except Exception:
                    continue
        except Exception:
            pass

        return JSONResponse(content={
            "question": query.question,
            "data_result": rows,   # structured array; frontend renders a table
            "summary": summary
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    # Run with: python backend\main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
