#!/bin/bash
# Railway startup script

# Set the port from environment variable (Railway provides this)
export PORT=${PORT:-8000}

# Start the application
exec uvicorn backend.app:app --host 0.0.0.0 --port $PORT
