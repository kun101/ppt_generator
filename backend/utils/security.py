import logging

def scrub_logs():
    """Disable sensitive logging to protect user data and API keys."""
    # Disable access logs that might contain sensitive data
    logging.getLogger("uvicorn.access").disabled = True
    
    # Keep error logs enabled for debugging
    logging.getLogger("uvicorn.error").disabled = False
    
    # Disable httpx debug logs that might contain API keys
    logging.getLogger("httpx").setLevel(logging.WARNING)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal attacks."""
    import os
    # Remove any path separators and keep only the filename
    return os.path.basename(filename)

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate that file has an allowed extension."""
    if not filename:
        return False
    
    extension = filename.lower().split('.')[-1]
    return f".{extension}" in [ext.lower() for ext in allowed_extensions]
