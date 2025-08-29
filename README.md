# Text → PowerPoint Generator

Transform your text content into professional PowerPoint presentations using AI. This tool leverages your existing PowerPoint templates to maintain consistent branding while intelligently structuring your content into well-organized slides.

![Text to PowerPoint Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Text+%E2%86%92+PowerPoint+Generator)

## 🌟 Features

- **Smart Template Analysis (Default)**: The generator now performs deep structural analysis of your template (masters, layouts, placeholders, image slots) and drives slide planning directly from that structure.
- **Multiple AI Providers**: Supports OpenAI (GPT-4) and Google (Gemini)
- **Deterministic Placeholder Mapping**: Each AI instruction is mapped to an existing placeholder exactly—no arbitrary new shapes created.
- **Strict Image Placeholder Usage**: Images are inserted ONLY into existing image/object/media placeholders; size and position are preserved 1:1 with the template.
- **Overflow-Safe Text Fitting**: Ultra‑conservative sizing + truncation logic prevents text spill beyond placeholder bounds.
- **Duplicate Content Prevention**: Title, bullets, subtitles, and secondary text are tracked so nothing appears twice on a slide.
- **Complete Placeholder Filling**: Eliminates all "click here to add text" artifacts where content exists.
- **Template-Aware Layout Selection**: Chooses layouts the template actually contains; honors their semantic roles.
- **Intelligent Image Reuse**: Reuses embedded template images (no external generation) following contextual hints.
- **Markdown Support**: Bold/italic parsing for inline formatting.
- **Privacy First**: API keys & content processed in-memory only; nothing persisted.
- **Graceful Fallback**: If LLM guidance fails, a heuristic legacy planner activates automatically.

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

4. **Run the application (smart template mode is automatic)**
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

## 📖 How to Use

1. **Select AI Provider**: OpenAI or Google Gemini
2. **Enter API Key**: Not stored; used only for this request
3. **(Optional) Guidance**: Style hints ("investor pitch", "technical training")
4. **Paste Content**: Plain text or Markdown
5. **Upload Template**: .pptx / .potx with your brand layout
6. **Generate**: Smart template-guided mode runs by default
7. **(Optional) Legacy Mode**: Pass `use_template_guidance=false` (form field) to force the older heuristic pipeline

## 🔧 API Usage

The service provides a REST API for programmatic access:

```bash
curl -X POST http://localhost:8000/api/generate \
   -F "provider=openai" \
   -F "api_key=sk-your-api-key" \
   -F "guidance=investor pitch deck" \
   -F "text=@your-content.txt" \
   -F "template=@your-template.pptx" \
   -F "use_template_guidance=true" \
   -o generated.pptx

# Legacy (non-structural) mode:
curl -X POST http://localhost:8000/api/generate \
   -F "provider=gemini" \
   -F "api_key=sk-your-api-key" \
   -F "text=@your-content.txt" \
   -F "template=@your-template.pptx" \
   -F "use_template_guidance=false" \
   -o legacy_generated.pptx
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

**Content Processing**: Default pipeline performs deep template analysis (layout indices, placeholder taxonomy, image slots) and feeds that context into an LLM prompt. The LLM returns a structured JSON plan mapping semantic content → concrete placeholder indices. If the AI service fails or returns invalid JSON, a heuristic Markdown-based fallback activates.

**Style Preservation**: Your uploaded template is cloned; original masters, color themes, fonts, and placeholder geometries remain untouched. Text is only inserted into existing placeholders—no freestyle shape creation—guaranteeing design fidelity.

**Image Intelligence**: Only existing template images are reused; images are inserted strictly into image/media/object placeholders (types 7, 18, 19, 20). Exact position & dimensions are preserved—no overlap, no drift. If a slide has no available image placeholder or the content doesn't call for one, no image is forced.

### Project Structure

```
ppt_generator/
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
│   ├── test_planner.py
│   └── test_writer.py
├── railway_start.py           # Railway deployment entry
├── start.sh                   # Deployment script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── railway.toml               # Railway configuration
├── nixpacks.toml              # Build configuration
└── README.md                  # This file
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

- **Template Required**: A well-structured template yields best results
- **LLM Variability**: Although structured, extremely ambiguous input can reduce precision (fallback covers failures)
- **No New Image Generation**: Only existing template images are reused (by design)
- **Very Long Text**: Ultra-long bodies may be truncated to prevent overflow
- **Exotic Templates**: Rare custom placeholder types may be ignored if unmapped

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
