# 🚀 Feature Development Crew Web UI

A modern, real-time web interface for running CrewAI feature development crews with live agent monitoring and output display.

## ✨ Features

- **Real-time Agent Monitoring**: Watch agents work in real-time with live logs
- **Modern Clean UI**: Beautiful, responsive interface built with vanilla HTML/CSS/JS
- **All Agent Outputs**: View product specs, wireframes, backend APIs, and HTML code
- **Live Progress Tracking**: Visual progress indicators and task status
- **WebSocket Communication**: Real-time updates without page refresh
- **Download & Copy**: Easy export of generated files and code
- **Error Handling**: Robust error handling with user-friendly messages

## 🏗️ Architecture

```
Frontend (Vanilla HTML/CSS/JS)
    ↕ WebSocket
Backend (FastAPI + WebSockets)
    ↕ Integration
CrewAI Feature Development Crew
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install web UI dependencies
pip install -r src/crewai_demo/web_ui/requirements.txt

# Or install all dependencies
pip install fastapi uvicorn[standard] websockets pydantic python-multipart
```

### 2. Start the Web UI

```bash
# From the project root
python src/crewai_demo/web_runner.py

# Or directly
cd src/crewai_demo
python web_runner.py
```

### 3. Access the Interface

- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws

## 📋 Usage

1. **Enter Feature Request**: Describe the feature you want to build
2. **Start Development**: Click "Start Development" to begin the crew execution
3. **Watch Progress**: Monitor real-time agent activity and progress
4. **View Outputs**: Check generated product specs, wireframes, APIs, and HTML
5. **Download Results**: Save generated files and copy code snippets

## 🎨 UI Components

### Main Interface
- **Feature Request Input**: Text area for describing requirements
- **Control Buttons**: Start, Stop, and Clear functionality
- **Progress Overview**: Visual progress bar and task status
- **Live Activity Log**: Real-time agent activity feed
- **Output Display**: Tabbed interface for all agent outputs

### Agent Outputs
- **Product Specification**: JSON formatted requirements
- **UI/UX Wireframe**: Design specifications and wireframes
- **Backend API**: API endpoints and database schemas
- **HTML Output**: Live preview and source code

## 🔧 Technical Details

### Backend (FastAPI)
- **REST API**: Standard HTTP endpoints for crew control
- **WebSocket**: Real-time communication for live updates
- **Custom Logger**: Captures all agent outputs and activities
- **Enhanced Executor**: Integrates with CrewAI with detailed logging

### Frontend (Vanilla JS)
- **WebSocket Client**: Handles real-time communication
- **Output Display**: Renders agent outputs with syntax highlighting
- **Task Progress**: Visual progress tracking and status updates
- **Modern CSS**: Clean, responsive design with animations

### Real-time Features
- **Per-Agent Logging**: Individual agent activity tracking
- **Per-Task Progress**: Task-by-task completion monitoring
- **Live Output Updates**: Real-time display of generated content
- **Error Handling**: Graceful error handling and recovery

## 📁 File Structure

```
src/crewai_demo/web_ui/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── websocket_handler.py    # WebSocket management
│   ├── crew_executor.py        # Enhanced crew execution
│   ├── custom_logger.py        # Agent output capture
│   └── models.py               # Data models
├── frontend/
│   ├── index.html              # Main UI page
│   ├── styles.css              # Modern CSS design
│   ├── app.js                  # Main application logic
│   ├── websocket-client.js     # WebSocket client
│   ├── output-display.js       # Output rendering
│   └── task-progress.js        # Progress tracking
└── web_runner.py               # Entry point
```

## 🎯 API Endpoints

- `GET /` - Main web interface
- `POST /api/start-crew` - Start crew execution
- `POST /api/stop-crew` - Stop crew execution
- `GET /api/status` - Get execution status
- `GET /api/outputs` - Get all agent outputs
- `GET /api/files/{filename}` - Download generated files
- `GET /api/health` - Health check
- `WebSocket /ws` - Real-time updates

## 🔌 WebSocket Messages

### Message Types
- `agent_start` - Agent begins working on a task
- `agent_thinking` - Agent's thinking process
- `agent_output` - Agent completes task with output
- `task_complete` - Task completion notification
- `crew_complete` - Entire crew execution finished
- `error` - Error occurred during execution

### Message Format
```json
{
  "type": "agent_output",
  "timestamp": "2024-01-15T14:32:15Z",
  "agent": "Product Manager",
  "task": "product_design_task",
  "data": {
    "output": "...",
    "output_type": "product_spec",
    "preview": "..."
  },
  "progress": 25
}
```

## 🎨 Design System

### Colors
- **Primary**: Indigo (#6366f1)
- **Success**: Emerald (#10b981)
- **Warning**: Amber (#f59e0b)
- **Error**: Red (#ef4444)
- **Background**: Slate (#f8fafc)
- **Surface**: White (#ffffff)

### Typography
- **Font**: Inter, system-ui, sans-serif
- **Sizes**: 12px, 14px, 16px, 18px, 24px, 32px
- **Weights**: 400 (regular), 500 (medium), 600 (semibold)

### Components
- **Cards**: Subtle shadows, rounded corners
- **Buttons**: Modern with hover states
- **Progress**: Smooth animations
- **Logs**: Monospace with color coding

## 🚀 Deployment

### Local Development
```bash
python src/crewai_demo/web_runner.py
```

### Production Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn crewai_demo.web_ui.backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Configuration

### Environment Variables
- `CREWAI_API_KEY` - CrewAI API key
- `OPENAI_API_KEY` - OpenAI API key
- `SERPER_API_KEY` - Serper search API key
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

### Customization
- Modify `frontend/styles.css` for styling changes
- Update `backend/models.py` for data model changes
- Customize `frontend/app.js` for behavior modifications

## 🐛 Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check if server is running
   - Verify firewall settings
   - Check browser console for errors

2. **Crew Execution Fails**
   - Verify API keys are set
   - Check CrewAI installation
   - Review server logs

3. **UI Not Loading**
   - Check if frontend files exist
   - Verify static file serving
   - Clear browser cache

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=debug
python src/crewai_demo/web_runner.py
```

## 📝 License

This project is part of the CrewAI demo and follows the same license terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy coding with CrewAI! 🚀**


