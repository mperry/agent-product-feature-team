#!/usr/bin/env python3
"""
Environment setup script for CrewAI Demo
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with API key configuration"""
    env_path = Path(__file__).parent / ".env"
    
    if env_path.exists():
        print("✅ .env file already exists")
        return
    
    print("🔧 Creating .env file...")
    
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Other API Keys
# SERPER_API_KEY=your_serper_api_key_here
# CREWAI_API_KEY=your_crewai_api_key_here

# Server Configuration
PORT=8000
HOST=0.0.0.0
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created .env file at: {env_path}")
    print("📝 Please edit the .env file and add your OpenAI API key")
    print("🔗 Get your API key from: https://platform.openai.com/api-keys")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        print("✅ FastAPI installed")
    except ImportError:
        print("❌ FastAPI not installed. Run: pip install fastapi")
    
    try:
        import uvicorn
        print("✅ Uvicorn installed")
    except ImportError:
        print("❌ Uvicorn not installed. Run: pip install uvicorn[standard]")
    
    try:
        import dotenv
        print("✅ python-dotenv installed")
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install python-dotenv")
    
    try:
        import crewai
        print("✅ CrewAI installed")
    except ImportError:
        print("❌ CrewAI not installed. Run: pip install crewai[tools]")

def main():
    """Main setup function"""
    print("🚀 CrewAI Demo Environment Setup")
    print("=" * 40)
    
    create_env_file()
    print()
    check_dependencies()
    print()
    
    print("📋 Next steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Install missing dependencies if any")
    print("3. Run: python web_runner.py")

if __name__ == "__main__":
    main()

