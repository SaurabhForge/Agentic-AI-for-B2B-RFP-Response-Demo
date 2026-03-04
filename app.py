import traceback

try:
    import os
    import sys
    from pathlib import Path

    # Vercel's Edge runtime sometimes fails to include the root directory in the Python path
    # which causes a ModuleNotFoundError when trying to import `rfp_agentic`.
    sys.path.append(str(Path(__file__).resolve().parent))

    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    from rfp_agentic.main import run

    app = FastAPI(title="Agentic RFP Response API")

    @app.get("/", response_class=HTMLResponse)
    async def read_index():
        # Use absolute path to ensure Vercel can find the file regardless of the cwd
        html_path = Path(__file__).resolve().parent / "static" / "index.html"
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()

    # On Vercel, trying to mount StaticFiles globally can crash the ASGI cold start 
    # if the worker's temp path isn't fully ready. We'll handle static manually or let Vercel route it.
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

except Exception as e:
    # If anything during module initialization fails, we stand up a minimal
    # FastAPI app just to serve the error to the frontend instantly
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    
    error_trace = traceback.format_exc()
    app = FastAPI()
    
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(path_name: str):
        return HTMLResponse(
            status_code=500,
            content=f"<h1>App Initialization Failed on Vercel Edge</h1><pre>{error_trace}</pre>"
        )
