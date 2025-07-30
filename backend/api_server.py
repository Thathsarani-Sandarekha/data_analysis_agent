from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from main import run_agent_pipeline
import os
import webbrowser
import threading

def open_browser():
    webbrowser.open("http://localhost:8000")

threading.Timer(1.0, open_browser).start()

app = FastAPI()

# Allow frontend + API to work together
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount React static files
app.mount("/static", StaticFiles(directory="frontend_build/static"), name="static")

# Serve index.html from root "/"
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return FileResponse("frontend_build/index.html")

# API endpoint
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def handle_query(req: QueryRequest):
    return run_agent_pipeline(req.query)

# Chart image route (must be above catch-all)
@app.get("/charts/{filename}")
async def serve_chart(filename: str):
    return FileResponse(path=os.path.join("charts", filename), media_type="image/png")

# Catch-all fallback for React Router
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_react_router(full_path: str):
    file_path = os.path.join("frontend_build", full_path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return FileResponse(file_path)
    return FileResponse("frontend_build/index.html")