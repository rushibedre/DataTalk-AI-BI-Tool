from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Import the agent_executor and the custom prompt from our other file
from llm_core import agent_executor, AGENT_PROMPT

# This is the line the server was looking for!
app = FastAPI()

# Mount the frontend directory to serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

class Query(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the main index.html file."""
    with open("../frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/query")
async def handle_query(query: Query):
    """
    Handles user questions by invoking the LangChain SQL Agent.
    """
    try:
        print("--- 1. Received query from frontend ---") # ADD THIS LINE

        prompt = f"{AGENT_PROMPT}\n\nQuestion: {query.question}"
        
        print("--- 2. Sending prompt to LangChain Agent... ---") # ADD THIS LINE
        
        result = agent_executor.invoke({"input": prompt})

        print("--- 3. Received result from Agent ---") # ADD THIS LINE

        summary = result.get('output', "I couldn't find an answer.")
        
        return JSONResponse(content={
            "question": query.question,
            "data_result": "Data is processed internally by the agent.",
            "summary": summary
        })
    except Exception as e:
        print(f"An error occurred: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
