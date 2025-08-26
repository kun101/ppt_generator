#!/usr/bin/env python3
"""
Test if frontend files are accessible
"""

import os
from pathlib import Path

def test_frontend_files():
    """Test if frontend files exist and are accessible"""
    print("🔍 Testing frontend file accessibility...")
    
    # Test from current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    frontend_dir = current_dir / "frontend"
    print(f"Frontend directory: {frontend_dir}")
    print(f"Frontend exists: {frontend_dir.exists()}")
    
    if frontend_dir.exists():
        print(f"Frontend contents: {list(frontend_dir.iterdir())}")
        
        # Check specific files
        html_file = frontend_dir / "index.html"
        js_file = frontend_dir / "app.js"
        
        print(f"index.html exists: {html_file.exists()}")
        print(f"app.js exists: {js_file.exists()}")
        
        if html_file.exists():
            print(f"index.html size: {html_file.stat().st_size} bytes")
        if js_file.exists():
            print(f"app.js size: {js_file.stat().st_size} bytes")
            
        return True
    else:
        print("❌ Frontend directory not found!")
        return False

if __name__ == "__main__":
    test_frontend_files()
