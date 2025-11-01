/**
 * Output display component for showing agent outputs
 */

class OutputDisplay {
    constructor() {
        this.outputs = {
            'product_spec': null,
            'wireframe': null,
            'backend_api': null,
            'html': null
        };
        
        this.initializeTabs();
        this.initializeOutputPanels();
    }
    
    initializeTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabName = button.getAttribute('data-tab');
                this.switchTab(tabName);
            });
        });
    }
    
    initializeOutputPanels() {
        // Initialize all output panels
        Object.keys(this.outputs).forEach(key => {
            const panel = document.getElementById(key.replace('_', '-'));
            if (panel) {
                panel.classList.remove('active');
            }
        });
        
        // Show first tab by default
        this.switchTab('product-spec');
    }
    
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        const activeTab = document.querySelector(`[data-tab="${tabName}"]`);
        if (activeTab) {
            activeTab.classList.add('active');
        }
        
        // Update output panels
        document.querySelectorAll('.output-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        
        const activePanel = document.getElementById(tabName);
        if (activePanel) {
            activePanel.classList.add('active');
        }
    }
    
    updateOutput(agentName, taskName, output, outputType) {
        // Map task names to output types
        const taskMapping = {
            'product_design_task': 'product_spec',
            'uiux_design_task': 'wireframe',
            'backend_development_task': 'backend_api',
            'frontend_development_task': 'html'
        };
        
        const mappedType = taskMapping[taskName] || outputType;
        
        if (this.outputs.hasOwnProperty(mappedType)) {
            this.outputs[mappedType] = {
                agentName,
                taskName,
                output,
                outputType: mappedType,
                timestamp: new Date()
            };
            
            this.renderOutput(mappedType);
        }
    }
    
    renderOutput(outputType) {
        const outputData = this.outputs[outputType];
        if (!outputData) return;
        
        const panelId = outputType.replace('_', '-');
        const panel = document.getElementById(panelId);
        if (!panel) return;
        
        // Clear existing content
        panel.innerHTML = '';
        
        // Create output header
        const header = document.createElement('div');
        header.className = 'output-header';
        header.innerHTML = `
            <div class="output-meta">
                <span class="agent-name">${outputData.agentName}</span>
                <span class="output-type">${outputData.outputType.replace('_', ' ').toUpperCase()}</span>
                <span class="timestamp">${outputData.timestamp.toLocaleTimeString()}</span>
            </div>
            <div class="output-actions">
                <button class="btn btn-sm btn-outline" onclick="outputDisplay.copyToClipboard('${outputType}')">
                    📋 Copy
                </button>
                ${outputType === 'html' ? `
                    <button class="btn btn-sm btn-outline" onclick="outputDisplay.downloadFile('${outputType}')">
                        💾 Download
                    </button>
                    <button class="btn btn-sm btn-outline" onclick="outputDisplay.previewHTML('${outputType}')">
                        👁️ Preview
                    </button>
                ` : ''}
            </div>
        `;
        panel.appendChild(header);
        
        // Create output content
        const content = document.createElement('div');
        content.className = 'output-content-wrapper';
        
        if (outputType === 'html') {
            this.renderHTMLOutput(content, outputData.output);
        } else {
            this.renderJSONOutput(content, outputData.output);
        }
        
        panel.appendChild(content);
    }
    
    renderJSONOutput(container, output) {
        try {
            // Try to parse as JSON
            const jsonData = JSON.parse(output);
            const formattedJSON = JSON.stringify(jsonData, null, 2);
            
            const pre = document.createElement('pre');
            pre.textContent = formattedJSON;
            container.appendChild(pre);
            
        } catch (error) {
            // If not valid JSON, display as plain text
            const pre = document.createElement('pre');
            pre.textContent = output;
            container.appendChild(pre);
        }
    }
    
    renderHTMLOutput(container, output) {
        // Create tabbed interface for HTML output
        const tabs = document.createElement('div');
        tabs.className = 'html-tabs';
        tabs.innerHTML = `
            <button class="html-tab-btn active" data-html-tab="source">Source Code</button>
            <button class="html-tab-btn" data-html-tab="preview">Live Preview</button>
        `;
        
        const content = document.createElement('div');
        content.className = 'html-content';
        
        // Source code tab
        const sourceDiv = document.createElement('div');
        sourceDiv.className = 'html-tab-content active';
        sourceDiv.id = 'html-source';
        const pre = document.createElement('pre');
        pre.textContent = output;
        sourceDiv.appendChild(pre);
        
        // Preview tab
        const previewDiv = document.createElement('div');
        previewDiv.className = 'html-tab-content';
        previewDiv.id = 'html-preview';
        const iframe = document.createElement('iframe');
        iframe.sandbox = 'allow-scripts allow-same-origin';
        previewDiv.appendChild(iframe);
        
        content.appendChild(sourceDiv);
        content.appendChild(previewDiv);
        
        container.appendChild(tabs);
        container.appendChild(content);
        
        // Add tab switching functionality
        tabs.addEventListener('click', (e) => {
            if (e.target.classList.contains('html-tab-btn')) {
                const tabType = e.target.getAttribute('data-html-tab');
                this.switchHTMLTab(tabType, iframe, output);
            }
        });
        
        // Load HTML into iframe for preview
        this.loadHTMLPreview(iframe, output);
    }
    
    switchHTMLTab(tabType, iframe, output) {
        // Update tab buttons
        document.querySelectorAll('.html-tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-html-tab="${tabType}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.html-tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`html-${tabType}`).classList.add('active');
        
        if (tabType === 'preview') {
            this.loadHTMLPreview(iframe, output);
        }
    }
    
    loadHTMLPreview(iframe, output) {
        try {
            const blob = new Blob([output], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            iframe.src = url;
            
            // Clean up URL after a delay
            setTimeout(() => {
                URL.revokeObjectURL(url);
            }, 10000);
        } catch (error) {
            console.error('Error loading HTML preview:', error);
            iframe.src = 'about:blank';
        }
    }
    
    copyToClipboard(outputType) {
        const outputData = this.outputs[outputType];
        if (!outputData) return;
        
        navigator.clipboard.writeText(outputData.output).then(() => {
            // Show temporary success message
            this.showToast('Copied to clipboard!');
        }).catch(error => {
            console.error('Failed to copy to clipboard:', error);
            this.showToast('Failed to copy to clipboard', 'error');
        });
    }
    
    downloadFile(outputType) {
        const outputData = this.outputs[outputType];
        if (!outputData) return;
        
        const filename = `feature_output_${outputType}.${outputType === 'html' ? 'html' : 'json'}`;
        const blob = new Blob([outputData.output], { 
            type: outputType === 'html' ? 'text/html' : 'application/json' 
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showToast(`Downloaded ${filename}`);
    }
    
    previewHTML(outputType) {
        const outputData = this.outputs[outputType];
        if (!outputData || outputType !== 'html') return;
        
        // Switch to preview tab
        this.switchTab('html-output');
        const previewBtn = document.querySelector('[data-html-tab="preview"]');
        if (previewBtn) {
            previewBtn.click();
        }
    }
    
    showToast(message, type = 'success') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        // Style the toast
        Object.assign(toast.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            background: type === 'error' ? '#ef4444' : '#10b981',
            color: 'white',
            padding: '12px 20px',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            zIndex: '10000',
            fontSize: '14px',
            fontWeight: '500',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
    
    clearAll() {
        this.outputs = {
            'product_spec': null,
            'wireframe': null,
            'backend_api': null,
            'html': null
        };
        
        // Reset all panels to placeholder state
        document.querySelectorAll('.output-panel').forEach(panel => {
            const placeholder = document.createElement('div');
            placeholder.className = 'output-placeholder';
            
            const iconMap = {
                'product-spec': '📋',
                'wireframe': '🎨',
                'backend-api': '⚙️',
                'html-output': '💻'
            };
            
            const textMap = {
                'product-spec': 'Product specification will appear here after Product Manager completes their task.',
                'wireframe': 'UI/UX wireframe will appear here after Designer completes their task.',
                'backend-api': 'Backend API specification will appear here after Backend Engineer completes their task.',
                'html-output': 'Generated HTML will appear here after Frontend Engineer completes their task.'
            };
            
            placeholder.innerHTML = `
                <span class="placeholder-icon">${iconMap[panel.id]}</span>
                <p>${textMap[panel.id]}</p>
            `;
            
            panel.innerHTML = '';
            panel.appendChild(placeholder);
        });
        
        // Switch back to first tab
        this.switchTab('product-spec');
    }
}

// Create global instance
window.outputDisplay = new OutputDisplay();


