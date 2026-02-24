import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.ingest_routes import router as ingest_router
from api.query_routes import router as query_router

app = FastAPI(
    title="Founder Knowledge OS",
    description="Local AI-Powered Personal Knowledge Operating System",
    version="1.0.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(ingest_router, tags=["Ingestion"])
app.include_router(query_router, tags=["Query"])

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
def serve_landing():
    """Serve the landing page."""
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Landing page not found."}


@app.get("/app")
def serve_app():
    """Serve the main knowledge application."""
    app_path = os.path.join(frontend_dir, "app.html")
    if os.path.exists(app_path):
        return FileResponse(app_path)
    return {"message": "Application interface not found."}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Founder Knowledge OS"}
