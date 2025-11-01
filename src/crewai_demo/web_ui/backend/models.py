"""
Pydantic models for the web UI backend
"""

from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    AGENT_START = "agent_start"
    AGENT_THINKING = "agent_thinking"
    AGENT_OUTPUT = "agent_output"
    TASK_COMPLETE = "task_complete"
    CREW_COMPLETE = "crew_complete"
    ERROR = "error"


class WebSocketMessage(BaseModel):
    type: MessageType
    timestamp: datetime
    agent: Optional[str] = None
    task: Optional[str] = None
    data: Dict[str, Any]
    progress: Optional[int] = None


class FeatureRequest(BaseModel):
    feature_request: str


class CrewStatus(BaseModel):
    is_running: bool
    current_task: Optional[str] = None
    current_agent: Optional[str] = None
    progress: int = 0
    total_tasks: int = 4
    start_time: Optional[datetime] = None


class AgentOutput(BaseModel):
    agent_name: str
    task_name: str
    output: str
    timestamp: datetime
    output_type: str  # "product_spec", "wireframe", "backend_api", "html"


class CrewExecutionResult(BaseModel):
    success: bool
    outputs: List[AgentOutput]
    error_message: Optional[str] = None
    execution_time: float
    generated_files: List[str] = []
    final_result: Optional[str] = None
