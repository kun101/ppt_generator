# Usage Guide - Text to PowerPoint Generator

## 🚀 Getting Started

### 1. Start the Server

```bash
# Navigate to project directory
cd c:\Users\kunal\Documents\ppt_generator

# Start the FastAPI server
C:/Users/kunal/miniforge3/Scripts/conda.exe run -p C:\Users\kunal\miniforge3 --no-capture-output python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

### 2. Access the Application

Open your web browser and navigate to: http://127.0.0.1:8000

### 3. Create a Sample Template (Optional)

If you don't have a PowerPoint template, you can create a sample one:

```bash
C:/Users/kunal/miniforge3/Scripts/conda.exe run -p C:\Users\kunal\miniforge3 --no-capture-output python create_sample_template.py
```

This will create `sample_template.pptx` in your project directory.

## 📝 Using the Web Interface

1. **Select AI Provider**: Choose between OpenAI or Google Gemini
2. **Enter API Key**: Provide your API key for the selected provider
3. **Add Guidance** (optional): Describe the type of presentation you want
4. **Paste Content**: Add your text or Markdown content to be converted
5. **Upload Template**: Select your PowerPoint template file (.pptx or .potx)
6. **Generate**: Click the generate button to create your presentation

## 🔑 API Keys

You'll need an API key from one of these providers:

- **OpenAI**: https://platform.openai.com/api-keys (starts with `sk-`)
- **Google AI Studio**: https://makersuite.google.com/app/apikey

## 📄 Content Examples

### Basic Text
```
Introduction to Machine Learning

Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.

Key Concepts:
- Supervised Learning
- Unsupervised Learning  
- Reinforcement Learning

Applications include image recognition, natural language processing, and predictive analytics.
```

### Markdown Format
```markdown
# Introduction to Machine Learning

## What is Machine Learning?
Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience.

## Key Concepts
- **Supervised Learning**: Learning with labeled data
- **Unsupervised Learning**: Finding patterns in unlabeled data
- **Reinforcement Learning**: Learning through interaction and feedback

## Applications
- Image Recognition
- Natural Language Processing
- Predictive Analytics
```

## 🎨 Guidance Examples

- "investor pitch deck" - Creates a business-focused presentation
- "technical overview" - Focuses on technical details and explanations
- "training materials" - Educational format with clear explanations
- "short presentation" - Limits the number of slides
- "detailed analysis" - Creates more comprehensive slides

## 🔧 API Usage

You can also use the API programmatically:

```bash
curl -X POST http://127.0.0.1:8000/api/generate \
  -F "provider=openai" \
  -F "api_key=your-api-key-here" \
  -F "guidance=investor pitch deck" \
  -F "text=Your content here..." \
  -F "template=@your-template.pptx" \
  -o generated-presentation.pptx
```

## 🏥 Health Check

Test if the server is running:
```bash
curl http://127.0.0.1:8000/api/health
```

Should return: `{"ok": true, "service": "text-to-pptx"}`

## 🐛 Troubleshooting

### Server Won't Start
- Make sure you're using the correct Python environment
- Check that all dependencies are installed
- Verify the port 8000 is not already in use

### Template Upload Issues
- Ensure your template is a valid .pptx or .potx file
- Try creating a simple template using PowerPoint
- Use the sample template creation script

### API Key Errors
- Double-check your API key format
- Ensure your API key has sufficient credits/permissions
- Try a different provider if one is not working

### Generation Fails
- The system has fallback mechanisms, so it should work even if AI fails
- Check your internet connection for API calls
- Try with shorter content if you get token limit errors

## 📊 Features Overview

### Content Processing
- Supports plain text and Markdown
- Automatically structures content into logical slides
- Fallback system works without AI providers

### Template Integration
- Preserves your template's design and branding
- Maintains fonts, colors, and layout styles
- Reuses images from template when appropriate

### AI Integration
- Multiple provider support (OpenAI, Google)
- Intelligent slide structuring
- Customizable presentation styles

### Privacy & Security
- API keys are never stored
- Content is processed in memory only
- Temporary files are automatically cleaned up

## 🎯 Best Practices

1. **Content Preparation**: Structure your content with clear sections and bullet points
2. **Template Selection**: Use a well-designed template with consistent styling
3. **Guidance**: Provide specific guidance for better AI-generated structure
4. **Testing**: Try with shorter content first to verify everything works
5. **Backup**: Always keep your original content and template files

## 📈 Scaling and Deployment

For production deployment, consider:
- Using a proper WSGI server like Gunicorn
- Setting up reverse proxy with Nginx
- Implementing rate limiting
- Adding authentication if needed
- Monitoring and logging setup
