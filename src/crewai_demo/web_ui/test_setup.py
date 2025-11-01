#!/usr/bin/env python3
"""
Test script to verify web UI setup
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import websockets
        print("✅ WebSockets imported successfully")
    except ImportError as e:
        print(f"❌ WebSockets import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    return True

def test_crew_import():
    """Test if crew modules can be imported"""
    print("\n🧪 Testing crew imports...")
    
    try:
        from crewai_demo.crew_product_feature import CrewFeatureDevelopment
        print("✅ CrewFeatureDevelopment imported successfully")
    except ImportError as e:
        print(f"❌ CrewFeatureDevelopment import failed: {e}")
        return False
    
    try:
        from crewai import Agent, Task, Crew, Process
        print("✅ CrewAI core modules imported successfully")
    except ImportError as e:
        print(f"❌ CrewAI core import failed: {e}")
        return False
    
    return True

def test_web_ui_modules():
    """Test if web UI modules can be imported"""
    print("\n🧪 Testing web UI modules...")
    
    try:
        from crewai_demo.web_ui.backend.models import WebSocketMessage, MessageType
        print("✅ Web UI models imported successfully")
    except ImportError as e:
        print(f"❌ Web UI models import failed: {e}")
        return False
    
    try:
        from crewai_demo.web_ui.backend.custom_logger import AgentOutputLogger
        print("✅ AgentOutputLogger imported successfully")
    except ImportError as e:
        print(f"❌ AgentOutputLogger import failed: {e}")
        return False
    
    try:
        from crewai_demo.web_ui.backend.websocket_handler import WebSocketHandler
        print("✅ WebSocketHandler imported successfully")
    except ImportError as e:
        print(f"❌ WebSocketHandler import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing file structure...")
    
    base_path = Path(__file__).parent
    
    required_files = [
        "backend/main.py",
        "backend/models.py",
        "backend/custom_logger.py",
        "backend/websocket_handler.py",
        "backend/crew_executor.py",
        "frontend/index.html",
        "frontend/styles.css",
        "frontend/app.js",
        "frontend/websocket-client.js",
        "frontend/output-display.js",
        "frontend/task-progress.js",
        "README.md"
    ]
    
    all_exist = True
    
    # Check for web_runner.py in project root
    project_root = base_path.parent.parent.parent
    web_runner_path = project_root / "web_runner.py"
    if web_runner_path.exists():
        print("✅ web_runner.py exists (in project root)")
    else:
        print("❌ web_runner.py missing (should be in project root)")
        all_exist = False
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🚀 Feature Development Crew Web UI - Setup Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_crew_import,
        test_web_ui_modules,
        test_file_structure
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    
    if all(results):
        print("🎉 All tests passed! Web UI setup is ready.")
        print("\n🚀 To start the web UI, run:")
        print("   python src/crewai_demo/web_runner.py")
        print("\n🌐 Then visit: http://localhost:8000")
        return 0
    else:
        print("❌ Some tests failed. Please check the setup.")
        print("\n📋 To install missing dependencies:")
        print("   pip install fastapi uvicorn[standard] websockets pydantic python-multipart")
        return 1

if __name__ == "__main__":
    sys.exit(main())
