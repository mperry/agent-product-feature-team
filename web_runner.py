#!/usr/bin/env python3
"""
Web runner for Feature Development Crew with real-time UI
"""

import sys
import os
import uvicorn
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Or set environment variables manually.")

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main entry point for the web UI"""
    print("🚀 Starting Feature Development Crew Web UI...")
    print("📁 Project directory:", Path(__file__).parent)
    
    # Check for LLM configuration
    openai_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("MODEL", "ollama/llama3:latest")
    api_base = os.getenv("API_BASE", "http://localhost:11434")
    
    if openai_key:
        print("✅ OpenAI API key found - using OpenAI")
    elif "ollama" in model.lower():
        print(f"✅ Using Ollama model: {model}")
        print(f"   API Base: {api_base}")
        # Test Ollama connection
        try:
            import requests
            response = requests.get(f"{api_base}/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama server is running")
            else:
                print("❌ Ollama server not responding")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Cannot connect to Ollama server: {e}")
            print("   Make sure Ollama is running: ollama serve")
            sys.exit(1)
    else:
        print("❌ No LLM configuration found!")
        print("   Please either:")
        print("   1. Set OPENAI_API_KEY for OpenAI")
        print("   2. Set MODEL=ollama/llama3:latest for Ollama")
        sys.exit(1)
    
    print("🌐 Web UI will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/ws")
    print("-" * 60)
    
    try:
        uvicorn.run(
            "src.crewai_demo.web_ui.backend.main:app",
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
