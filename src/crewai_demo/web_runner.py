#!/usr/bin/env python3
"""
Web runner for Feature Development Crew with real-time UI
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main entry point for the web UI"""
    print("🚀 Starting Feature Development Crew Web UI...")
    print("📁 Project directory:", Path(__file__).parent)
    print("🌐 Web UI will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/ws")
    print("-" * 60)
    
    try:
        # Import and run the FastAPI app
        from crewai_demo.web_ui.backend.main import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Feature Development Crew Web UI...")
    except Exception as e:
        print(f"❌ Error starting web UI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


