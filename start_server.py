#!/usr/bin/env python3
"""
Simple server to serve the web UI (bypasses LLM check for viewing the page)
"""
import sys
from pathlib import Path
import uvicorn

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Start the web server without LLM checks"""
    print("🚀 Starting Feature Development Crew Web UI...")
    print("📁 Project directory:", Path(__file__).parent)
    print("🌐 Web UI will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/ws")
    print("-" * 60)
    print("⚠️  Note: Crew execution will require API keys (OPENAI_API_KEY or Ollama)")
    print("-" * 60)
    
    try:
        uvicorn.run(
            "crewai_demo.web_ui.backend.main:app",
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
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

