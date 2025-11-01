"""
WebSocket handler for real-time communication with frontend
"""

import asyncio
import json
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from .models import WebSocketMessage


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        # Store active connections
        self.active_connections: Set[WebSocket] = set()
        
    async def connect(self, websocket: WebSocket):
        """Accept a WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        self.active_connections.discard(websocket)
        print(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
        
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
            self.disconnect(websocket)
            
    async def broadcast(self, message: str):
        """Broadcast a message to all connected WebSocket clients"""
        if not self.active_connections:
            print(f"⚠️  No active WebSocket connections to send message to")
            return
        
        print(f"📡 Broadcasting to {len(self.active_connections)} connection(s)...")
        
        # Create a list of connections to remove (disconnected ones)
        disconnected = set()
        sent_count = 0
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
                sent_count += 1
            except Exception as e:
                print(f"❌ Error broadcasting to connection: {e}")
                disconnected.add(connection)
        
        print(f"✅ Successfully sent message to {sent_count} connection(s)")
                
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
            
    async def send_websocket_message(self, message: WebSocketMessage):
        """Send a structured WebSocket message"""
        try:
            # Use model_dump with mode='json' for proper serialization
            import json as json_lib
            message_dict = message.model_dump(mode='json')
            message_json = json_lib.dumps(message_dict)
            await self.broadcast(message_json)
        except Exception as e:
            print(f"Error in send_websocket_message: {e}")
            import traceback
            traceback.print_exc()
        
    def get_connection_count(self) -> int:
        """Get the number of active connections"""
        return len(self.active_connections)


class WebSocketHandler:
    """Main WebSocket handler class"""
    
    def __init__(self):
        self.manager = ConnectionManager()
        self.logger_callback = None
        
    def set_logger_callback(self, callback):
        """Set the callback for logger messages"""
        self.logger_callback = callback
        
    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connection"""
        await self.manager.connect(websocket)
        
        try:
            while True:
                # Wait for messages from client
                data = await websocket.receive_text()
                
                try:
                    message_data = json.loads(data)
                    await self._handle_client_message(message_data, websocket)
                except json.JSONDecodeError:
                    await self.send_error(websocket, "Invalid JSON format")
                    
        except WebSocketDisconnect:
            self.manager.disconnect(websocket)
        except Exception as e:
            print(f"WebSocket error: {e}")
            self.manager.disconnect(websocket)
            
    async def _handle_client_message(self, message_data: Dict, websocket: WebSocket):
        """Handle messages from client"""
        message_type = message_data.get("type")
        
        if message_type == "ping":
            # Respond to ping with pong
            await self.manager.send_personal_message(
                json.dumps({"type": "pong", "timestamp": message_data.get("timestamp")}),
                websocket
            )
        elif message_type == "get_status":
            # Send current status
            status = {
                "type": "status",
                "connections": self.manager.get_connection_count(),
                "timestamp": message_data.get("timestamp")
            }
            await self.manager.send_personal_message(
                json.dumps(status),
                websocket
            )
        else:
            await self.send_error(websocket, f"Unknown message type: {message_type}")
            
    async def send_error(self, websocket: WebSocket, error_message: str):
        """Send error message to specific WebSocket"""
        error_data = {
            "type": "error",
            "message": error_message,
            "timestamp": str(asyncio.get_event_loop().time())
        }
        await self.manager.send_personal_message(
            json.dumps(error_data),
            websocket
        )
        
    async def send_message_to_all(self, message: WebSocketMessage):
        """Send message to all connected clients"""
        await self.manager.send_websocket_message(message)
        
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return self.manager.get_connection_count()


