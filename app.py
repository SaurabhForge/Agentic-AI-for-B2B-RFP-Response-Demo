import os
import sys
from pathlib import Path
import traceback

# Vercel's Edge runtime sometimes fails to include the root directory in the Python path
# which causes a ModuleNotFoundError when trying to import `rfp_agentic`.
sys.path.append(str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from rfp_agentic.main import run

app = FastAPI(title="Agentic RFP Response API")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Use absolute path to ensure Vercel/local can find the file regardless of the cwd
    html_path = Path(__file__).resolve().parent / "static" / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    from fastapi.responses import FileResponse
    static_file = Path(__file__).resolve().parent / "static" / file_path
    if static_file.exists():
        return FileResponse(static_file)
    return HTMLResponse(status_code=404, content="File not found")

@app.post("/api/run")
async def run_agentic_rfp():
    """Triggers the multi-agent Orchestrator and writes to output/rfp_response.txt"""
    try:
        content = run()
        return {"status": "success", "message": "Agents completed execution", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

@app.get("/api/results")
async def get_results():
    """Reads the generated result from output/rfp_response.txt"""
    output_path = Path(__file__).resolve().parent / "output" / "rfp_response.txt"
    if not output_path.exists():
        return {"content": "No results yet. Run the system to generate output."}
    
    content = output_path.read_text()
    return {"content": content}
