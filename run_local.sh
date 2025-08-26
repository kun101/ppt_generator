#!/bin/bash
# Local development startup script for Unix/Linux/Mac
echo "Starting Text-to-PowerPoint Generator..."
echo ""
echo "Frontend will be available at: http://127.0.0.1:8000"
echo "API health check at: http://127.0.0.1:8000/api/health"
echo ""
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
