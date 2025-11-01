/**
 * Main application controller for Feature Development Crew Web UI
 */

class FeatureDevelopmentApp {
    constructor() {
        this.isRunning = false;
        this.currentExecution = null;
        
        this.initializeElements();
        this.initializeEventListeners();
        this.initializeWebSocket();
        this.initializeComponents();
    }
    
    initializeElements() {
        // Form elements
        this.featureRequestInput = document.getElementById('featureRequest');
        this.startButton = document.getElementById('startCrew');
        this.stopButton = document.getElementById('stopCrew');
        this.clearButton = document.getElementById('clearAll');
        
        // Status elements
        this.activityLogs = document.getElementById('activityLogs');
    }
    
    initializeEventListeners() {
        // Button events
        this.startButton.addEventListener('click', () => this.startCrew());
        this.stopButton.addEventListener('click', () => this.stopCrew());
        this.clearButton.addEventListener('click', () => this.clearAll());
        
        // Form events
        this.featureRequestInput.addEventListener('input', () => this.validateForm());
        this.featureRequestInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.startCrew();
            }
        });
        
        // Prevent form submission on Enter
        this.featureRequestInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.ctrlKey) {
                e.preventDefault();
            }
        });
    }
    
    initializeWebSocket() {
        // WebSocket event handlers
        window.wsClient.on('connected', () => {
            this.logActivity('WebSocket connected', 'success');
            this.updateUI();
        });
        
        window.wsClient.on('disconnected', () => {
            this.logActivity('WebSocket disconnected', 'warning');
            this.updateUI();
        });
        
        window.wsClient.on('error', (error) => {
            this.logActivity(`WebSocket error: ${error}`, 'error');
        });
        
        window.wsClient.on('crew_update', (data) => {
            this.handleCrewUpdate(data);
        });
        
        // Connect WebSocket
        window.wsClient.connect().catch(error => {
            console.error('Failed to connect WebSocket:', error);
            this.logActivity('Failed to connect to server', 'error');
        });
    }
    
    initializeComponents() {
        // Components are already initialized as global instances
        // Just validate the form initially
        this.validateForm();
    }
    
    async startCrew() {
        const featureRequest = this.featureRequestInput.value.trim();
        
        if (!featureRequest) {
            this.showNotification('Please enter a feature request', 'error');
            this.featureRequestInput.focus();
            return;
        }
        
        if (this.isRunning) {
            this.showNotification('Crew is already running', 'warning');
            return;
        }
        
        try {
            this.isRunning = true;
            this.updateUI();
            this.logActivity('🚀 Starting crew execution...', 'info');
            
            // Clear previous outputs
            window.outputDisplay.clearAll();
            window.taskProgress.reset();
            this.clearActivityLogs();
            
            // Start crew execution
            const response = await fetch('/api/start-crew', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    feature_request: featureRequest
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to start crew');
            }
            
            const result = await response.json();
            this.logActivity(`Crew execution started: ${result.message}`, 'success');
            
        } catch (error) {
            console.error('Error starting crew:', error);
            this.logActivity(`Error starting crew: ${error.message}`, 'error');
            this.isRunning = false;
            this.updateUI();
            this.showNotification('Failed to start crew execution', 'error');
        }
    }
    
    async stopCrew() {
        if (!this.isRunning) {
            this.showNotification('No crew is currently running', 'warning');
            return;
        }
        
        try {
            const response = await fetch('/api/stop-crew', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to stop crew');
            }
            
            const result = await response.json();
            this.logActivity(`Crew execution stopped: ${result.message}`, 'warning');
            
        } catch (error) {
            console.error('Error stopping crew:', error);
            this.logActivity(`Error stopping crew: ${error.message}`, 'error');
            this.showNotification('Failed to stop crew execution', 'error');
        }
    }
    
    clearAll() {
        if (this.isRunning) {
            this.showNotification('Cannot clear while crew is running. Please stop first.', 'warning');
            return;
        }
        
        // Clear form
        this.featureRequestInput.value = '';
        
        // Clear outputs
        window.outputDisplay.clearAll();
        window.taskProgress.reset();
        this.clearActivityLogs();
        
        // Reset UI
        this.updateUI();
        
        this.logActivity('All data cleared', 'info');
        this.showNotification('All data cleared', 'success');
    }
    
    handleCrewUpdate(data) {
        console.log('🎯 Crew update received:', data.type, data);
        
        if (!data || !data.type) {
            console.error('❌ Invalid crew update data:', data);
            return;
        }
        
        switch (data.type) {
            case 'agent_start':
                this.handleAgentStart(data);
                break;
            case 'agent_thinking':
                this.handleAgentThinking(data);
                break;
            case 'agent_output':
                this.handleAgentOutput(data);
                break;
            case 'task_complete':
                this.handleTaskComplete(data);
                break;
            case 'crew_complete':
                this.handleCrewComplete(data);
                break;
            case 'error':
                this.handleError(data);
                break;
            default:
                console.warn('⚠️ Unknown crew update type:', data.type);
        }
    }
    
    handleAgentStart(data) {
        const message = `🚀 ${data.agent} started working on ${data.task}`;
        this.logActivity(message, 'info');
        
        window.taskProgress.onAgentStart(data.agent, data.task);
    }
    
    handleAgentThinking(data) {
        const message = `💭 ${data.agent} is thinking: ${data.data.thought}`;
        this.logActivity(message, 'info');
        
        window.taskProgress.onAgentThinking(data.agent, data.data.thought);
    }
    
    handleAgentOutput(data) {
        const message = `✅ ${data.agent} completed ${data.task}`;
        this.logActivity(message, 'success');
        
        // Update output display
        window.outputDisplay.updateOutput(
            data.agent,
            data.task,
            data.data.output,
            data.data.output_type
        );
        
        window.taskProgress.onAgentOutput(
            data.agent,
            data.task,
            data.data.output,
            data.data.output_type
        );
    }
    
    handleTaskComplete(data) {
        const message = `🎯 Task ${data.task} completed by ${data.agent}`;
        this.logActivity(message, 'success');
        
        window.taskProgress.onTaskComplete(
            data.task,
            data.agent,
            data.progress || 0
        );
    }
    
    handleCrewComplete(data) {
        this.isRunning = false;
        this.updateUI();
        
        if (data.data.success) {
            const message = `🎉 Crew execution completed successfully in ${data.data.execution_time.toFixed(2)}s`;
            this.logActivity(message, 'success');
            this.showNotification('Crew execution completed successfully!', 'success');
            
            // Show the final HTML output if available
            if (data.data.final_result) {
                this.logActivity('📄 Final HTML output generated and ready for preview!', 'success');
                // Switch to HTML output tab
                const htmlTab = document.querySelector('[data-tab="html-output"]');
                if (htmlTab) {
                    htmlTab.click();
                }
            }
        } else {
            const message = `❌ Crew execution failed: ${data.data.error_message}`;
            this.logActivity(message, 'error');
            this.showNotification('Crew execution failed', 'error');
        }
        
        window.taskProgress.onCrewComplete(
            data.data.success,
            data.data.execution_time,
            data.data.error_message
        );
    }
    
    handleError(data) {
        const message = `❌ Error: ${data.data.error}`;
        this.logActivity(message, 'error');
        
        window.taskProgress.onError(
            data.data.error,
            data.agent,
            data.task
        );
    }
    
    validateForm() {
        const featureRequest = this.featureRequestInput.value.trim();
        const isValid = featureRequest.length > 10;
        
        this.startButton.disabled = !isValid || this.isRunning;
        
        return isValid;
    }
    
    updateUI() {
        // Update button states
        this.startButton.disabled = !this.validateForm() || this.isRunning;
        this.stopButton.disabled = !this.isRunning;
        
        // Update button text and icons
        if (this.isRunning) {
            this.startButton.innerHTML = '<span class="btn-icon">⏳</span> Running...';
            this.stopButton.innerHTML = '<span class="btn-icon">⏹️</span> Stop';
        } else {
            this.startButton.innerHTML = '<span class="btn-icon">🚀</span> Start Development';
            this.stopButton.innerHTML = '<span class="btn-icon">⏹️</span> Stop';
        }
    }
    
    logActivity(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        
        logEntry.innerHTML = `
            <span class="log-time">${timestamp}</span>
            <span class="log-message">${message}</span>
        `;
        
        this.activityLogs.appendChild(logEntry);
        
        // Auto-scroll to bottom with smooth scrolling
        this.activityLogs.scrollTo({
            top: this.activityLogs.scrollHeight,
            behavior: 'smooth'
        });
        
        // Limit log entries to prevent memory issues
        const maxEntries = 50;
        while (this.activityLogs.children.length > maxEntries) {
            this.activityLogs.removeChild(this.activityLogs.firstChild);
        }
        
        // Add visual feedback for important messages
        if (type === 'success' || type === 'error') {
            logEntry.style.animation = 'slideInUp 0.5s ease-out';
        }
    }
    
    clearActivityLogs() {
        this.activityLogs.innerHTML = `
            <div class="log-entry info">
                <span class="log-time">Ready</span>
                <span class="log-message">Waiting for feature request...</span>
            </div>
        `;
    }
    
    
    showNotification(message, type = 'info') {
        // Use the toast system from output display
        if (window.outputDisplay) {
            window.outputDisplay.showToast(message, type);
        }
    }
    
    // Utility methods
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    formatFileSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Bytes';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new FeatureDevelopmentApp();
    console.log('🚀 Feature Development Crew Web UI initialized');
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.wsClient) {
        // Reconnect WebSocket when page becomes visible
        if (!window.wsClient.isConnected()) {
            window.wsClient.connect().catch(error => {
                console.error('Failed to reconnect WebSocket:', error);
            });
        }
    }
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.wsClient) {
        window.wsClient.disconnect();
    }
});
