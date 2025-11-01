"""
Custom logger for capturing CrewAI agent outputs and streaming them via WebSocket
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from .models import WebSocketMessage, MessageType


class AgentOutputLogger:
    """Custom logger that captures agent outputs and sends them via WebSocket"""
    
    def __init__(self, websocket_send_callback: Optional[Callable] = None):
        self.websocket_send = websocket_send_callback
        self.agent_outputs: Dict[str, Dict[str, Any]] = {}
        self.current_task = None
        self.current_agent = None
        
    async def log_agent_start(self, agent_name: str, task_name: str):
        """Log when an agent starts working on a task"""
        self.current_agent = agent_name
        self.current_task = task_name
        
        message = WebSocketMessage(
            type=MessageType.AGENT_START,
            timestamp=datetime.now(),
            agent=agent_name,
            task=task_name,
            data={
                "message": f"{agent_name} started working on {task_name}",
                "status": "starting"
            }
        )
        
        await self._send_message(message)
        
    async def log_agent_thinking(self, agent_name: str, thought: str):
        """Log agent's thinking process"""
        message = WebSocketMessage(
            type=MessageType.AGENT_THINKING,
            timestamp=datetime.now(),
            agent=agent_name,
            task=self.current_task,
            data={
                "message": f"{agent_name} is thinking: {thought}",
                "thought": thought
            }
        )
        
        await self._send_message(message)
        
    async def log_agent_output(self, agent_name: str, task_name: str, output: str, output_type: str = "text"):
        """Log agent's output"""
        # Store the output
        if task_name not in self.agent_outputs:
            self.agent_outputs[task_name] = {}
            
        self.agent_outputs[task_name][agent_name] = {
            "output": output,
            "output_type": output_type,
            "timestamp": datetime.now()
        }
        
        message = WebSocketMessage(
            type=MessageType.AGENT_OUTPUT,
            timestamp=datetime.now(),
            agent=agent_name,
            task=task_name,
            data={
                "message": f"{agent_name} completed {task_name}",
                "output": output,
                "output_type": output_type,
                "preview": self._get_output_preview(output, output_type)
            }
        )
        
        await self._send_message(message)
        
    async def log_task_complete(self, task_name: str, agent_name: str, progress: int):
        """Log when a task is completed"""
        message = WebSocketMessage(
            type=MessageType.TASK_COMPLETE,
            timestamp=datetime.now(),
            agent=agent_name,
            task=task_name,
            data={
                "message": f"Task {task_name} completed by {agent_name}",
                "status": "completed"
            },
            progress=progress
        )
        
        await self._send_message(message)
        
    async def log_crew_complete(self, success: bool, execution_time: float, final_result: str = None):
        """Log when the entire crew execution is complete"""
        message = WebSocketMessage(
            type=MessageType.CREW_COMPLETE,
            timestamp=datetime.now(),
            data={
                "message": "Crew execution completed",
                "success": success,
                "execution_time": execution_time,
                "final_result": final_result,
                "outputs": self.agent_outputs
            },
            progress=100
        )
        
        await self._send_message(message)
        
    async def log_error(self, error_message: str, agent_name: str = None, task_name: str = None):
        """Log errors"""
        message = WebSocketMessage(
            type=MessageType.ERROR,
            timestamp=datetime.now(),
            agent=agent_name,
            task=task_name,
            data={
                "message": f"Error: {error_message}",
                "error": error_message
            }
        )
        
        await self._send_message(message)
        
    def _get_output_preview(self, output: str, output_type: str) -> str:
        """Get a preview of the output for display"""
        if output_type == "html":
            return "HTML file generated"
        elif output_type == "json":
            try:
                data = json.loads(output)
                return f"JSON with {len(data)} fields"
            except:
                return "JSON data"
        else:
            # Return first 100 characters
            return output[:100] + "..." if len(output) > 100 else output
            
    async def _send_message(self, message: WebSocketMessage):
        """Send message via WebSocket"""
        # Show WebSocket updates in terminal
        timestamp = message.timestamp.strftime('%H:%M:%S')
        
        if message.type.value == "agent_start":
            print(f"   🔵 [{timestamp}] Agent Started: {message.agent} → {message.task}")
        elif message.type.value == "agent_output":
            print(f"   ✅ [{timestamp}] Agent Output: {message.agent} completed {message.task}")
        elif message.type.value == "task_complete":
            print(f"   ✓  [{timestamp}] Task Complete: {message.task} ({message.progress}%)")
        elif message.type.value == "crew_complete":
            success = "✅ SUCCESS" if message.data.get("success") else "❌ FAILED"
            exec_time = message.data.get("execution_time", 0)
            print(f"   {success} [{timestamp}] Crew Complete in {exec_time:.2f}s")
        
        if self.websocket_send:
            try:
                # Pass the WebSocketMessage object directly (not JSON string)
                # The websocket_handler will handle serialization
                print(f"   📤 Sending WebSocket message: {message.type.value}")
                await self.websocket_send(message)
                print(f"   ✅ WebSocket message sent successfully")
            except Exception as e:
                print(f"   ❌ Error sending WebSocket message: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("   ⚠️  No WebSocket send callback available")
                
    def get_all_outputs(self) -> Dict[str, Dict[str, Any]]:
        """Get all captured outputs"""
        return self.agent_outputs.copy()
        
    def clear_outputs(self):
        """Clear all captured outputs"""
        self.agent_outputs.clear()
        self.current_task = None
        self.current_agent = None
