from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.utils.security import scrub_logs
from backend.pptx_engine.template_reader import analyze_template
from backend.pptx_engine.slide_planner import make_slide_plan
from backend.pptx_engine.slide_writer import build_presentation
from backend.llm import get_provider
from tempfile import NamedTemporaryFile
import io
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Text→PPTX", description="Convert text to PowerPoint presentations")

# Log startup
logger.info("Starting Text-to-PowerPoint Generator")
logger.info(f"Python path: {os.getcwd()}")
logger.info(f"PORT environment variable: {os.environ.get('PORT', 'Not set')}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"], 
    allow_headers=["*"]
)

@app.get("/api/health")
def health():
    logger.info("Health check endpoint called")
    return {"ok": True, "service": "text-to-pptx", "status": "healthy"}

@app.get("/api/info")
async def api_info():
    """API info endpoint."""
    return {"message": "Text-to-PowerPoint Generator API", "status": "running", "health": "/api/health"}

@app.get("/api/debug/routes")
def debug_routes():
    """Debug endpoint to show all available routes."""
    routes = []
    for route in app.routes:
        routes.append({
            "path": getattr(route, 'path', 'N/A'),
            "methods": getattr(route, 'methods', 'N/A'),
            "name": getattr(route, 'name', 'N/A')
        })
    return {"routes": routes}

@app.post("/api/generate")
async def generate_pptx(
    text: str = Form(...),
    guidance: str = Form(""),
    provider: str = Form(...),        # "openai" | "gemini"
    api_key: str = Form(...),
    template: UploadFile = File(...)
):
    print(f"DEBUG: Received request with provider={provider}")  # Debug log
    scrub_logs()  # ensure no sensitive logs

    # Validate file type
    if not template.filename.lower().endswith(('.pptx', '.potx')):
        raise HTTPException(status_code=400, detail="Template must be a .pptx or .potx file")

    # Save template to a temp file
    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(template.filename)[1]) as tf:
        tf.write(await template.read())
        template_path = tf.name

    try:
        # 1) Read template style & assets
        style_ctx = analyze_template(template_path)

        # 2) Plan slides via LLM (with heuristic fallback)
        llm = get_provider(provider, api_key)
        slide_plan = await make_slide_plan(text, guidance, style_ctx, llm)

        # 3) Build PPTX
        pptx_bytes = build_presentation(slide_plan, style_ctx, template_path)

        return StreamingResponse(
            io.BytesIO(pptx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": 'attachment; filename="generated.pptx"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        try: 
            os.remove(template_path)
        except: 
            pass

# Setup paths for static files
current_dir = Path(__file__).parent.parent  # Go up from backend/ to root
frontend_dir = current_dir / "frontend"

logger.info(f"Current directory: {current_dir}")
logger.info(f"Frontend directory: {frontend_dir}")
logger.info(f"Frontend directory exists: {frontend_dir.exists()}")

# Serve static files for frontend
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# Serve the main HTML file at root
@app.get("/")
async def serve_frontend():
    """Serve the main frontend HTML file."""
    html_path = frontend_dir / "index.html"
    logger.info(f"Serving frontend from: {html_path}")
    logger.info(f"HTML file exists: {html_path.exists()}")
    if html_path.exists():
        return FileResponse(str(html_path))
    else:
        # Fallback if file not found
        return {
            "error": "Frontend not found",
            "message": "Please access the API at /api/info",
            "health": "/api/health",
            "frontend_path": str(html_path),
            "working_dir": str(current_dir)
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
