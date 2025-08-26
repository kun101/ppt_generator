// Modern Presentation Generator Application
class PresentationGenerator {
    constructor() {
        this.form = document.getElementById('generatorForm');
        this.statusEl = document.getElementById('status');
        this.generateBtn = document.getElementById('generateBtn');
        this.btnText = this.generateBtn.querySelector('.btn-text');
        this.btnLoading = this.generateBtn.querySelector('.btn-loading');
        
        this.init();
    }

    init() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        this.addFileValidation();
        this.addProviderInfo();
        this.addCharacterCounter();
        this.addFileUploadEnhancements();
        this.addAnimations();
    }

    addCharacterCounter() {
        const textArea = document.getElementById('text');
        const charCounter = document.getElementById('charCounter');
        
        const updateCounter = () => {
            const count = textArea.value.length;
            charCounter.textContent = `${count.toLocaleString()} characters`;
            
            // Color coding based on length
            charCounter.classList.remove('text-red-400', 'text-yellow-400', 'text-gray-300');
            if (count > 40000) {
                charCounter.classList.add('text-red-400');
            } else if (count > 20000) {
                charCounter.classList.add('text-yellow-400');
            } else {
                charCounter.classList.add('text-gray-300');
            }
        };
        
        textArea.addEventListener('input', updateCounter);
        updateCounter(); // Initial count
    }

    addFileUploadEnhancements() {
        const fileInput = document.getElementById('template');
        const uploadArea = document.getElementById('fileUploadArea');
        const uploadContent = uploadArea.querySelector('.upload-content');
        
        // Drag and drop functionality
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-gray-600');
            uploadArea.classList.add('border-blue-500', 'bg-gray-800/70');
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-blue-500', 'bg-gray-800/70');
            uploadArea.classList.add('border-gray-600');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-blue-500', 'bg-gray-800/70');
            uploadArea.classList.add('border-gray-600');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                this.updateUploadDisplay(files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                this.updateUploadDisplay(e.target.files[0]);
            }
        });
    }

    updateUploadDisplay(file) {
        const uploadArea = document.getElementById('fileUploadArea');
        const uploadContent = uploadArea.querySelector('.upload-content');
        
        if (file) {
            const validExtensions = ['.pptx', '.potx'];
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            
            if (!validExtensions.includes(fileExtension)) {
                this.showStatus('Please select a valid PowerPoint template (.pptx or .potx)', 'error');
                document.getElementById('template').value = '';
                return;
            }
            
            // Truncate filename if too long
            const truncatedName = file.name.length > 40 ? 
                file.name.substring(0, 37) + '...' : file.name;
            
            uploadContent.innerHTML = `
                <div class="upload-icon text-green-400 mb-4">
                    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" class="mx-auto">
                        <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="2" fill="none"/>
                        <path d="M16 24l6 6 12-12" stroke="currentColor" stroke-width="2" fill="none"/>
                    </svg>
                </div>
                <div class="upload-text space-y-2 w-full">
                    <div class="text-lg font-medium text-green-400 break-words px-2" title="${file.name}">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" class="inline mr-2">
                            <polyline points="20,6 9,17 4,12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        ${truncatedName}
                    </div>
                    <div class="text-gray-400">${this.formatFileSize(file.size)}</div>
                    <div class="text-xs text-gray-500">Click to change template</div>
                </div>
            `;
            uploadArea.classList.remove('border-gray-600');
            uploadArea.classList.add('border-green-500');
            this.hideStatus();
        }
    }

    addAnimations() {
        // Add fade-in animation to cards - handled by Tailwind and CSS
        const cards = document.querySelectorAll('.bg-gray-800\\/50');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    addHoverEffects() {
        // Hover effects are now handled by Tailwind classes
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                if (input.parentElement.classList.contains('relative')) {
                    input.parentElement.style.transform = 'translateY(-2px)';
                }
            });
            
            input.addEventListener('blur', () => {
                if (input.parentElement.classList.contains('relative')) {
                    input.parentElement.style.transform = 'translateY(0)';
                }
            });
        });
    }

    addFileValidation() {
        const fileInput = document.getElementById('template');
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const validExtensions = ['.pptx', '.potx'];
                const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
                
                if (!validExtensions.includes(fileExtension)) {
                    this.showStatus('Please select a valid PowerPoint template (.pptx or .potx)', 'error');
                    fileInput.value = '';
                } else {
                    this.hideStatus();
                }
            }
        });
    }

    addProviderInfo() {
        const providerSelect = document.getElementById('provider');
        const apiKeyInput = document.getElementById('api_key');
        
        providerSelect.addEventListener('change', (e) => {
            const provider = e.target.value;
            let placeholder = 'Enter your API key';
            
            switch (provider) {
                case 'openai':
                    placeholder = 'sk-... (OpenAI API key)';
                    break;
                case 'gemini':
                    placeholder = 'AI... (Google API key)';
                    break;
            }
            
            apiKeyInput.placeholder = placeholder;
            
            // Add visual feedback
            providerSelect.classList.add('border-green-500');
            setTimeout(() => {
                providerSelect.classList.remove('border-green-500');
            }, 1000);
        });
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            return;
        }

        this.setLoading(true);
        this.showStatus('AI is analyzing your content and generating slides...', 'loading');

        try {
            const formData = new FormData(this.form);
            
            // Add progress updates
            setTimeout(() => {
                if (this.generateBtn.disabled) {
                    this.showStatus('Structuring presentation layout...', 'loading');
                }
            }, 3000);
            
            setTimeout(() => {
                if (this.generateBtn.disabled) {
                    this.showStatus('Applying template styling...', 'loading');
                }
            }, 6000);
            
            const response = await fetch('/api/generate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            // Handle the file download
            const blob = await response.blob();
            this.downloadFile(blob, 'generated-presentation.pptx');
            
            this.showStatus('Presentation generated successfully! Download started.', 'success');
            
            // Clear sensitive data with animation
            const apiKeyInput = document.getElementById('api_key');
            apiKeyInput.style.transition = 'opacity 0.3s ease';
            apiKeyInput.style.opacity = '0';
            setTimeout(() => {
                apiKeyInput.value = '';
                apiKeyInput.style.opacity = '1';
            }, 300);
            
        } catch (error) {
            console.error('Generation failed:', error);
            this.showStatus(`Generation failed: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    validateForm() {
        const provider = document.getElementById('provider').value;
        const apiKey = document.getElementById('api_key').value;
        const text = document.getElementById('text').value;
        const template = document.getElementById('template').files[0];

        if (!provider) {
            this.showStatus('Please select an LLM provider', 'error');
            document.getElementById('provider').focus();
            return false;
        }

        if (!apiKey.trim()) {
            this.showStatus('Please enter your API key', 'error');
            document.getElementById('api_key').focus();
            return false;
        }

        if (!text.trim()) {
            this.showStatus('Please enter some text content', 'error');
            document.getElementById('text').focus();
            return false;
        }

        if (text.length > 50000) {
            this.showStatus('Text content is too long (max 50,000 characters)', 'error');
            document.getElementById('text').focus();
            return false;
        }

        if (!template) {
            this.showStatus('Please upload a PowerPoint template', 'error');
            document.getElementById('template').focus();
            return false;
        }

        // Basic API key format validation
        if (!this.validateApiKeyFormat(provider, apiKey)) {
            this.showStatus('API key format appears invalid for the selected provider', 'error');
            document.getElementById('api_key').focus();
            return false;
        }

        return true;
    }

    validateApiKeyFormat(provider, apiKey) {
        switch (provider) {
            case 'openai':
                return apiKey.startsWith('sk-');
            case 'gemini':
                return apiKey.length > 20; // Basic length check
            default:
                return true;
        }
    }

    downloadFile(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    setLoading(isLoading) {
        this.generateBtn.disabled = isLoading;
        
        if (isLoading) {
            this.btnText.style.display = 'none';
            this.btnLoading.classList.remove('hidden');
            this.btnLoading.classList.add('flex');
        } else {
            this.btnText.style.display = 'inline-flex';
            this.btnLoading.classList.add('hidden');
            this.btnLoading.classList.remove('flex');
        }
    }

    showStatus(message, type) {
        this.statusEl.textContent = message;
        this.statusEl.className = `mt-8 max-w-2xl mx-auto p-4 rounded-xl border backdrop-blur-xl ${this.getStatusClasses(type)}`;
        this.statusEl.classList.remove('hidden');
        
        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                this.hideStatus();
            }, 5000);
        }
    }

    getStatusClasses(type) {
        switch (type) {
            case 'success':
                return 'bg-green-900/50 border-green-500 text-green-300';
            case 'error':
                return 'bg-red-900/50 border-red-500 text-red-300';
            case 'loading':
                return 'bg-blue-900/50 border-blue-500 text-blue-300';
            default:
                return 'bg-gray-800/50 border-gray-600 text-gray-300';
        }
    }

    hideStatus() {
        this.statusEl.classList.add('hidden');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Utility functions
class UIUtils {
    static formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    static validateTextLength(text, maxChars = 50000) {
        return text.length <= maxChars;
    }

    static truncateText(text, maxChars = 16000) {
        if (text.length <= maxChars) return text;
        return text.substring(0, maxChars) + '\n\n[Content truncated for processing...]';
    }
}

// Health check function
async function checkServerHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('Server health:', data);
        return data.ok;
    } catch (error) {
        console.error('Server health check failed:', error);
        return false;
    }
}

// Initialize the application with enhanced animations
document.addEventListener('DOMContentLoaded', () => {
    new PresentationGenerator();
    
    // Add loading animation to page elements
    const cards = document.querySelectorAll('.bg-gray-800\\/50');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Check server health on load
    checkServerHealth().then(isHealthy => {
        if (!isHealthy) {
            console.warn('Server may not be responding correctly');
        }
    });
});

// Enhanced keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('generatorForm');
        if (form) {
            form.requestSubmit();
        }
    }
    
    // Escape to clear status messages
    if (e.key === 'Escape') {
        const statusEl = document.getElementById('status');
        if (statusEl && !statusEl.classList.contains('hidden')) {
            statusEl.classList.add('hidden');
        }
    }
});
