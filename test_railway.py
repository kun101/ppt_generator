#!/usr/bin/env python3
"""
Railway deployment test script
This script tests if the application can start properly
"""

import sys
import os

def test_imports():
    """Test all critical imports"""
    try:
        print("Testing FastAPI import...")
        from fastapi import FastAPI
        print("✅ FastAPI import successful")
        
        print("Testing backend module imports...")
        from backend.app import app
        print("✅ Backend app import successful")
        
        print("Testing LLM providers...")
        from backend.llm import get_provider
        print("✅ LLM providers import successful")
        
        print("Testing PPTX engine...")
        from backend.pptx_engine.template_reader import analyze_template
        print("✅ PPTX engine import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_app_creation():
    """Test app creation"""
    try:
        from backend.app import app
        print(f"✅ App created successfully: {app}")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Railway Deployment Test")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PORT environment: {os.environ.get('PORT', 'Not set')}")
    print()
    
    success = True
    success &= test_imports()
    success &= test_app_creation()
    
    if success:
        print("\n🎉 All tests passed! App should start successfully.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed! Check the errors above.")
        sys.exit(1)
