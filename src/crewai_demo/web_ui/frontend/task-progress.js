/**
 * Task progress component for tracking crew execution progress
 */

class TaskProgress {
    constructor() {
        this.tasks = {
            'product_design_task': {
                id: 'task-product',
                name: 'Product Manager',
                icon: '📋',
                status: 'pending'
            },
            'uiux_design_task': {
                id: 'task-ui',
                name: 'UI/UX Designer',
                icon: '🎨',
                status: 'pending'
            },
            'backend_development_task': {
                id: 'task-backend',
                name: 'Backend Engineer',
                icon: '⚙️',
                status: 'pending'
            },
            'frontend_development_task': {
                id: 'task-frontend',
                name: 'Frontend Engineer',
                icon: '💻',
                status: 'pending'
            }
        };
        
        this.currentProgress = 0;
        this.currentTask = null;
        this.currentAgent = null;
        
        this.initializeElements();
    }
    
    initializeElements() {
        this.progressFill = document.getElementById('progressFill');
        this.progressPercent = document.getElementById('progressPercent');
        this.progressStatus = document.getElementById('progressStatus');
    }
    
    updateProgress(progress, status = null) {
        this.currentProgress = Math.min(100, Math.max(0, progress));
        
        if (this.progressFill) {
            this.progressFill.style.width = `${this.currentProgress}%`;
        }
        
        if (this.progressPercent) {
            this.progressPercent.textContent = `${this.currentProgress}%`;
        }
        
        if (this.progressStatus && status) {
            this.progressStatus.textContent = status;
        }
    }
    
    setTaskStatus(taskName, status) {
        const task = this.tasks[taskName];
        if (!task) return;
        
        task.status = status;
        this.updateTaskUI(task);
    }
    
    setAgentActive(agentName, taskName) {
        // Reset all tasks to pending first
        Object.values(this.tasks).forEach(task => {
            if (task.status === 'active') {
                task.status = 'pending';
                this.updateTaskUI(task);
            }
        });
        
        // Set current task as active
        const task = this.tasks[taskName];
        if (task) {
            task.status = 'active';
            this.updateTaskUI(task);
            this.currentTask = taskName;
            this.currentAgent = agentName;
        }
    }
    
    setTaskComplete(taskName, agentName) {
        const task = this.tasks[taskName];
        if (!task) return;
        
        task.status = 'completed';
        this.updateTaskUI(task);
        
        // Update progress
        const completedTasks = Object.values(this.tasks).filter(t => t.status === 'completed').length;
        const totalTasks = Object.keys(this.tasks).length;
        const progress = Math.round((completedTasks / totalTasks) * 100);
        
        this.updateProgress(progress, `${agentName} completed ${task.name} task`);
    }
    
    setTaskError(taskName, errorMessage) {
        const task = this.tasks[taskName];
        if (!task) return;
        
        task.status = 'error';
        this.updateTaskUI(task);
        
        if (this.progressStatus) {
            this.progressStatus.textContent = `Error: ${errorMessage}`;
        }
    }
    
    updateTaskUI(task) {
        const taskElement = document.getElementById(task.id);
        if (!taskElement) return;
        
        const statusBadge = taskElement.querySelector('.task-status-badge');
        if (!statusBadge) return;
        
        // Remove all status classes
        statusBadge.classList.remove('pending', 'active', 'completed', 'error');
        
        // Add appropriate status class
        statusBadge.classList.add(task.status);
        
        // Update status text
        switch (task.status) {
            case 'pending':
                statusBadge.textContent = 'Pending';
                break;
            case 'active':
                statusBadge.textContent = 'Working...';
                break;
            case 'completed':
                statusBadge.textContent = 'Completed';
                break;
            case 'error':
                statusBadge.textContent = 'Error';
                break;
        }
        
        // Add visual feedback for active tasks
        if (task.status === 'active') {
            taskElement.style.background = 'rgba(99, 102, 241, 0.05)';
            taskElement.style.borderColor = 'rgba(99, 102, 241, 0.2)';
        } else {
            taskElement.style.background = '';
            taskElement.style.borderColor = '';
        }
    }
    
    reset() {
        // Reset all tasks to pending
        Object.values(this.tasks).forEach(task => {
            task.status = 'pending';
            this.updateTaskUI(task);
        });
        
        // Reset progress
        this.updateProgress(0, 'Ready to start');
        this.currentTask = null;
        this.currentAgent = null;
    }
    
    // Handle crew execution events
    onAgentStart(agentName, taskName) {
        this.setAgentActive(agentName, taskName);
        
        // Update progress based on task sequence
        const taskIndex = Object.keys(this.tasks).indexOf(taskName);
        const progress = Math.round((taskIndex / Object.keys(this.tasks).length) * 100);
        this.updateProgress(progress, `${agentName} started working...`);
    }
    
    onAgentThinking(agentName, thought) {
        if (this.currentAgent === agentName && this.currentTask) {
            this.updateProgress(this.currentProgress, `${agentName} is thinking...`);
        }
    }
    
    onAgentOutput(agentName, taskName, output, outputType) {
        this.setTaskComplete(taskName, agentName);
    }
    
    onTaskComplete(taskName, agentName, progress) {
        // Update progress immediately if provided
        if (progress !== undefined && progress !== null) {
            this.updateProgress(progress, `${agentName} completed ${taskName}`);
        }
        this.setTaskComplete(taskName, agentName);
    }
    
    onCrewComplete(success, executionTime, errorMessage) {
        if (success) {
            this.updateProgress(100, 'All tasks completed successfully!');
            
            // Mark any remaining tasks as completed
            Object.values(this.tasks).forEach(task => {
                if (task.status === 'active') {
                    task.status = 'completed';
                    this.updateTaskUI(task);
                }
            });
        } else {
            this.updateProgress(this.currentProgress, `Execution failed: ${errorMessage}`);
            
            // Mark current task as error
            if (this.currentTask) {
                this.setTaskError(this.currentTask, errorMessage);
            }
        }
    }
    
    onError(errorMessage, agentName, taskName) {
        if (taskName) {
            this.setTaskError(taskName, errorMessage);
        }
        
        this.updateProgress(this.currentProgress, `Error: ${errorMessage}`);
    }
    
    // Get current status
    getStatus() {
        return {
            progress: this.currentProgress,
            currentTask: this.currentTask,
            currentAgent: this.currentAgent,
            tasks: Object.entries(this.tasks).map(([name, task]) => ({
                name,
                ...task
            }))
        };
    }
    
    // Animation helpers
    animateProgress(fromProgress, toProgress, duration = 500) {
        const startTime = performance.now();
        const progressDiff = toProgress - fromProgress;
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentProgress = fromProgress + (progressDiff * this.easeInOutQuad(progress));
            this.updateProgress(currentProgress);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }
}

// Create global instance
window.taskProgress = new TaskProgress();


