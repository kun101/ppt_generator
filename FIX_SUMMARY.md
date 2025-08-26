# 🔧 Bug Fix: API Route Resolution

## Problem
The FastAPI application was returning `405 Method Not Allowed` for POST requests to `/api/generate`.

## Root Cause
The issue was caused by mounting static files at the root path `/` which intercepted all routes, preventing API endpoints from being accessible.

## Solution
1. **Restructured route mounting**: Moved static files to `/static/` path instead of root
2. **Added explicit root handler**: Created a dedicated route handler for serving the main HTML file at `/`
3. **Updated frontend paths**: Modified HTML to reference static assets at `/static/` paths

## Changes Made

### Backend (`backend/app.py`)
```python
# Before: Static files mounted at root (blocking API routes)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# After: Proper route separation
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")
```

### Frontend (`frontend/index.html`)
```html
<!-- Before: Relative paths that worked with root mounting -->
<link rel="stylesheet" href="styles.css">
<script src="app.js"></script>

<!-- After: Absolute paths to static directory -->
<link rel="stylesheet" href="/static/styles.css">
<script src="/static/app.js"></script>
```

## Result
- ✅ **API endpoints now working**: `/api/health` and `/api/generate` return proper responses
- ✅ **Static files served correctly**: CSS and JS files load from `/static/` path
- ✅ **Frontend accessible**: Main application loads at root `/` path
- ✅ **CORS properly configured**: All HTTP methods allowed for API routes

## Testing
The fix was verified by:
1. Health endpoint returning `{"ok": true, "service": "text-to-pptx"}`
2. Frontend loading properly with all assets
3. Successful presentation generation (logged in server output)

The application is now fully functional and ready for use! 🎉
