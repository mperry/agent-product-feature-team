"""
FastAPI backend for Feature Development Crew Web UI
"""

import asyncio
import os
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import FeatureRequest, CrewStatus, WebSocketMessage
from .websocket_handler import WebSocketHandler
from .custom_logger import AgentOutputLogger
from .crew_executor import EnhancedCrewExecutor


# Initialize FastAPI app
app = FastAPI(
    title="Feature Development Crew API",
    description="API for running CrewAI feature development with real-time updates",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
websocket_handler = WebSocketHandler()
crew_executor = None
current_execution = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global crew_executor
    
    # Initialize crew executor with WebSocket callback
    logger = AgentOutputLogger(websocket_handler.send_message_to_all)
    crew_executor = EnhancedCrewExecutor(logger)
    
    print("🚀 Feature Development Crew API started")


@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the main HTML page"""
    # Get the path to the frontend index.html
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
    index_path = os.path.join(frontend_path, "index.html")
    
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return HTMLResponse("""
        <html>
            <head><title>Feature Development Crew</title></head>
            <body>
                <h1>🚀 Feature Development Crew</h1>
                <p>Frontend not found. Please ensure index.html exists in the frontend directory.</p>
                <p>API is running at <a href="/docs">/docs</a></p>
            </body>
        </html>
        """)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket_handler.handle_websocket(websocket)


@app.post("/api/start-crew")
async def start_crew(feature_request: FeatureRequest, background_tasks: BackgroundTasks):
    """Start the crew execution"""
    global current_execution
    
    if crew_executor and crew_executor.is_running:
        raise HTTPException(status_code=400, detail="Crew is already running")
    
    try:
        # Clear previous outputs
        if crew_executor:
            crew_executor.logger.clear_outputs()
        
        # Start execution in background
        background_tasks.add_task(
            execute_crew_background,
            feature_request.feature_request
        )
        
        return {
            "message": "Crew execution started",
            "status": "started",
            "feature_request": feature_request.feature_request
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/stop-crew")
async def stop_crew():
    """Stop the crew execution"""
    global current_execution
    
    if not crew_executor or not crew_executor.is_running:
        raise HTTPException(status_code=400, detail="No crew is currently running")
    
    try:
        crew_executor.stop_execution()
        return {"message": "Crew execution stopped", "status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def get_status():
    """Get current crew execution status"""
    if not crew_executor:
        return CrewStatus(is_running=False)
    
    status = crew_executor.get_status()
    return CrewStatus(**status)


@app.get("/api/outputs")
async def get_outputs():
    """Get all agent outputs"""
    if not crew_executor:
        return {"outputs": []}
    
    return {
        "outputs": crew_executor.logger.get_all_outputs(),
        "count": len(crew_executor.logger.get_all_outputs())
    }


@app.get("/api/files/{filename}")
async def get_generated_file(filename: str):
    """Serve generated files"""
    # Security check - only allow specific files
    allowed_files = ["frontend_code.html"]
    
    if filename not in allowed_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    if os.path.exists(filename):
        return FileResponse(
            filename,
            media_type="text/html" if filename.endswith(".html") else "application/octet-stream"
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "websocket_connections": websocket_handler.get_connection_count(),
        "crew_running": crew_executor.is_running if crew_executor else False
    }


async def execute_crew_background(feature_request: str):
    """Execute crew in background task"""
    global current_execution
    
    try:
        print(f"DEBUG: Starting crew execution for: {feature_request}")
        current_execution = await crew_executor.execute_crew(feature_request)
        print(f"DEBUG: Crew execution completed: {current_execution.success}")
    except Exception as e:
        print(f"DEBUG: Crew execution failed: {e}")
        import traceback
        traceback.print_exc()
        current_execution = None


# Mount static files (for serving frontend assets)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
