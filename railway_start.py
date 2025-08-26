#!/usr/bin/env python3
"""
Railway startup script with error handling
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Log environment info
        logger.info("=== Railway Startup ===")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"PORT: {os.environ.get('PORT', 'Not set')}")
        logger.info(f"Python path: {sys.path}")
        
        # Test imports
        logger.info("Testing imports...")
        from backend.app import app
        logger.info("✅ App imported successfully")
        
        # Get port
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"Starting server on port {port}")
        
        # Start uvicorn
        import uvicorn
        uvicorn.run(
            "backend.app:app",
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
