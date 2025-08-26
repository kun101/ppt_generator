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
from pathlib import Path

app = FastAPI(title="Text→PPTX", description="Convert text to PowerPoint presentations")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"], 
    allow_headers=["*"]
)

@app.get("/api/health")
def health():
    return {"ok": True, "service": "text-to-pptx"}

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

# Serve static files for frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the main HTML file at root
@app.get("/")
async def serve_frontend():
    """Serve the main frontend HTML file."""
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
