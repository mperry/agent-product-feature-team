/**
 * WebSocket client for real-time communication with the backend
 */

class WebSocketClient {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectInterval = 3000;
        this.heartbeatInterval = null;
        this.isConnecting = false;
        this.messageHandlers = new Map();
        
        // Bind methods
        this.connect = this.connect.bind(this);
        this.disconnect = this.disconnect.bind(this);
        this.send = this.send.bind(this);
        this.handleMessage = this.handleMessage.bind(this);
    }
    
    connect() {
        if (this.isConnecting || (this.ws && this.ws.readyState === WebSocket.OPEN)) {
            return Promise.resolve();
        }
        
        this.isConnecting = true;
        
        return new Promise((resolve, reject) => {
            try {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws`;
                
                this.ws = new WebSocket(wsUrl);
                
                this.ws.onopen = () => {
                    console.log('WebSocket connected');
                    this.isConnecting = false;
                    this.reconnectAttempts = 0;
                    this.updateConnectionStatus(true);
                    this.startHeartbeat();
                    this.emit('connected');
                    resolve();
                };
                
                this.ws.onmessage = (event) => {
                    this.handleMessage(event);
                };
                
                this.ws.onclose = (event) => {
                    console.log('WebSocket disconnected:', event.code, event.reason);
                    this.isConnecting = false;
                    this.updateConnectionStatus(false);
                    this.stopHeartbeat();
                    this.emit('disconnected', event);
                    
                    // Attempt to reconnect if not a clean close
                    if (!event.wasClean && this.reconnectAttempts < this.maxReconnectAttempts) {
                        this.scheduleReconnect();
                    }
                };
                
                this.ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                    this.isConnecting = false;
                    this.updateConnectionStatus(false);
                    this.emit('error', error);
                    reject(error);
                };
                
            } catch (error) {
                this.isConnecting = false;
                reject(error);
            }
        });
    }
    
    disconnect() {
        this.stopHeartbeat();
        if (this.ws) {
            this.ws.close(1000, 'Client disconnect');
            this.ws = null;
        }
        this.updateConnectionStatus(false);
    }
    
    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
            return true;
        } else {
            console.warn('WebSocket not connected, cannot send message');
            return false;
        }
    }
    
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            
            // Debug logging
            console.log('📨 WebSocket message received:', data.type, data);
            
            // Handle different message types
            switch (data.type) {
                case 'pong':
                    // Heartbeat response
                    break;
                case 'status':
                    this.emit('status', data);
                    break;
                case 'agent_start':
                case 'agent_thinking':
                case 'agent_output':
                case 'task_complete':
                case 'crew_complete':
                case 'error':
                    console.log('📤 Emitting crew_update event:', data.type);
                    this.emit('crew_update', data);
                    break;
                default:
                    console.log('⚠️ Unknown message type:', data.type, data);
            }
            
        } catch (error) {
            console.error('❌ Error parsing WebSocket message:', error, event.data);
        }
    }
    
    scheduleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.log('Max reconnection attempts reached');
            return;
        }
        
        this.reconnectAttempts++;
        const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1);
        
        console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        
        setTimeout(() => {
            this.connect().catch(error => {
                console.error('Reconnection failed:', error);
            });
        }, delay);
    }
    
    startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            this.send({
                type: 'ping',
                timestamp: Date.now()
            });
        }, 30000); // Send ping every 30 seconds
    }
    
    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }
    
    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connectionStatus');
        if (statusElement) {
            const statusDot = statusElement.querySelector('.status-dot');
            const statusText = statusElement.querySelector('.status-text');
            
            if (statusDot && statusText) {
                if (connected) {
                    statusDot.className = 'status-dot connected';
                    statusText.textContent = 'Connected';
                } else {
                    statusDot.className = 'status-dot disconnected';
                    statusText.textContent = 'Disconnected';
                }
            }
        }
    }
    
    // Event system
    on(event, handler) {
        if (!this.messageHandlers.has(event)) {
            this.messageHandlers.set(event, []);
        }
        this.messageHandlers.get(event).push(handler);
    }
    
    off(event, handler) {
        if (this.messageHandlers.has(event)) {
            const handlers = this.messageHandlers.get(event);
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
        }
    }
    
    emit(event, data) {
        if (this.messageHandlers.has(event)) {
            this.messageHandlers.get(event).forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error('Error in event handler:', error);
                }
            });
        }
    }
    
    // Utility methods
    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }
    
    getConnectionState() {
        if (!this.ws) return 'CLOSED';
        
        switch (this.ws.readyState) {
            case WebSocket.CONNECTING: return 'CONNECTING';
            case WebSocket.OPEN: return 'OPEN';
            case WebSocket.CLOSING: return 'CLOSING';
            case WebSocket.CLOSED: return 'CLOSED';
            default: return 'UNKNOWN';
        }
    }
}

// Create global instance
window.wsClient = new WebSocketClient();


