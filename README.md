# Text → PowerPoint Generator

Transform your text content into professional PowerPoint presentations using AI. This tool leverages your existing PowerPoint templates to maintain consistent branding while intelligently structuring your content into well-organized slides.

![Text to PowerPoint Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Text+%E2%86%92+PowerPoint+Generator)

## 🌟 Features

- **Multiple AI Providers**: Supports OpenAI (GPT-4) and Google (Gemini)
- **Template Preservation**: Maintains your PowerPoint template's design, fonts, and branding
- **Smart Content Structure**: Automatically organizes text into logical slide sequences
- **Image Reuse**: Intelligently reuses images from your template when appropriate
- **Markdown Support**: Handles both plain text and Markdown formatting
- **Privacy First**: API keys and content are never stored or logged
- **Fallback System**: Works even if AI services are unavailable

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- An API key from one of the supported providers:
  - [OpenAI API Key](https://platform.openai.com/api-keys)
  - [Google AI Studio API Key](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/text-to-pptx.git
   cd text-to-pptx
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux  
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open your browser**
   Navigate to [http://localhost:8000](http://localhost:8000)

## 🚀 Deploy to Railway

For easy cloud deployment, this application is Railway-ready:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

**Quick Deploy Steps**:
1. Push your code to GitHub
2. Connect your GitHub repo to Railway
3. Railway will auto-detect and deploy your app
4. Get your live URL instantly!

See [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) for detailed deployment instructions.

## 📖 How to Use

1. **Select AI Provider**: Choose from OpenAI or Google
2. **Enter API Key**: Provide your API key (never stored)
3. **Add Guidance** (optional): Specify presentation style (e.g., "investor pitch", "training materials")
4. **Paste Content**: Add your text or Markdown content
5. **Upload Template**: Select your PowerPoint template (.pptx or .potx)
6. **Generate**: Click to create your presentation

## 🔧 API Usage

The service provides a REST API for programmatic access:

```bash
curl -X POST http://localhost:8000/api/generate \
  -F "provider=openai" \
  -F "api_key=sk-your-api-key" \
  -F "guidance=investor pitch deck" \
  -F "text=@your-content.txt" \
  -F "template=@your-template.pptx" \
  -o generated.pptx
```

### API Endpoints

- `GET /api/health` - Service health check
- `POST /api/generate` - Generate presentation (multipart/form-data)

### Request Parameters

- `text` (string, required): Content to convert
- `provider` (string, required): AI provider ("openai", "gemini")
- `api_key` (string, required): Your API key
- `guidance` (string, optional): Presentation style guidance
- `template` (file, required): PowerPoint template (.pptx/.potx)

## 🏗️ Architecture

### How It Works

**Content Processing**: The system uses Large Language Models to analyze your text and create a structured slide plan. Each slide gets a title, layout suggestion, bullet points, and optional speaker notes. If the AI service fails, a heuristic fallback parser uses Markdown headers and text structure to create slides.

**Style Preservation**: The generator starts from your uploaded template to inherit slide masters, layouts, fonts, and color schemes. It analyzes the template to extract reusable design elements and applies your brand consistently across all generated slides.

**Image Intelligence**: Rather than generating new images, the system intelligently reuses pictures already present in your template. It exports image blobs from template slides and re-inserts them contextually (e.g., section headers, content illustrations) to maintain visual consistency.

### Project Structure

```
text-to-pptx/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── llm/                   # AI provider abstraction
│   │   ├── base.py
│   │   ├── openai_provider.py
│   │   └── gemini_provider.py
│   ├── pptx_engine/           # PowerPoint generation
│   │   ├── template_reader.py # Template analysis
│   │   ├── slide_planner.py   # AI-powered planning
│   │   ├── slide_writer.py    # PPTX creation
│   │   └── heuristics.py      # Fallback planning
│   └── utils/
│       └── security.py        # Privacy & security
├── frontend/                  # Vanilla HTML/CSS/JS
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/                     # Unit tests
└── requirements.txt
```

## 🔒 Privacy & Security

- **No Data Persistence**: API keys and content are processed in memory only
- **Secure Logging**: Sensitive information is never logged
- **Temporary Files**: All uploaded files are automatically cleaned up
- **No Tracking**: No analytics or user tracking
- **Open Source**: Full transparency in code and data handling

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

## 📋 Limitations

- **Template Dependency**: Requires a PowerPoint template for styling
- **AI Service Dependency**: Best results require working AI provider (though fallback exists)
- **Style Inference**: Complex template layouts may not be perfectly preserved
- **No Image Generation**: Only reuses existing template images
- **Token Limits**: Very long content may be truncated

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [python-pptx](https://github.com/scanny/python-pptx) for PowerPoint manipulation
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [markdown-it-py](https://github.com/executablebooks/markdown-it-py) for Markdown parsing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/text-to-pptx/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/text-to-pptx/discussions)
- **Email**: your-email@example.com

---

**Made with ❤️ for content creators who value design consistency**
