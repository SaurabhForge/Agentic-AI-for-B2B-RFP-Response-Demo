import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from rfp_agentic.main import run

app = FastAPI(title="Agentic RFP Response API")

# Serve the static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/api/run")
async def run_agentic_rfp():
    """Triggers the multi-agent Orchestrator and writes to output/rfp_response.txt"""
    try:
        content = run()
        return {"status": "success", "message": "Agents completed execution", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/results")
async def get_results():
    """Reads the generated result from output/rfp_response.txt"""
    output_path = Path(__file__).resolve().parent / "output" / "rfp_response.txt"
    if not output_path.exists():
        return {"content": "No results yet. Run the system to generate output."}
    
    content = output_path.read_text()
    return {"content": content}
