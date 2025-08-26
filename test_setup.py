#!/usr/bin/env python3
"""
Simple test script to verify the application components work correctly.
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_heuristic_planning():
    """Test the heuristic slide planning."""
    from backend.pptx_engine.heuristics import rule_based_plan
    
    text = """
    # Introduction
    This is the introduction section with some content.
    
    # Main Points
    Here are the main points:
    - Point one
    - Point two
    - Point three
    
    # Conclusion
    This is the conclusion section.
    """
    
    result = rule_based_plan(text, "")
    print(f"✅ Heuristic planning created {len(result)} slides")
    
    for i, slide in enumerate(result):
        print(f"   Slide {i+1}: {slide.get('title', 'Untitled')}")

def test_llm_providers():
    """Test that LLM providers can be instantiated."""
    from backend.llm import get_provider
    
    try:
        openai_provider = get_provider("openai", "sk-test-key")
        print("✅ OpenAI provider instantiated")
    except Exception as e:
        print(f"❌ OpenAI provider failed: {e}")
    
    try:
        gemini_provider = get_provider("gemini", "test-key")
        print("✅ Gemini provider instantiated")
    except Exception as e:
        print(f"❌ Gemini provider failed: {e}")

async def test_slide_planning():
    """Test slide planning with mock LLM."""
    from backend.pptx_engine.slide_planner import make_slide_plan
    
    class MockLLM:
        async def generate(self, prompt, system="", json=True):
            return '''
            {
                "slides": [
                    {
                        "title": "Test Slide",
                        "layout_hint": "bullets",
                        "bullets": ["Point 1", "Point 2"],
                        "notes": "Test notes"
                    }
                ]
            }
            '''
    
    text = "This is test content for slide generation."
    guidance = "test presentation"
    style_ctx = {"theme": {"font_family": "Arial"}, "images": []}
    
    mock_llm = MockLLM()
    result = await make_slide_plan(text, guidance, style_ctx, mock_llm)
    
    print(f"✅ Slide planning successful with {len(result['slides'])} slides")

def test_imports():
    """Test that all required modules can be imported."""
    try:
        from pptx import Presentation
        print("✅ python-pptx imported successfully")
    except ImportError as e:
        print(f"❌ python-pptx import failed: {e}")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import httpx
        print("✅ httpx imported successfully")
    except ImportError as e:
        print(f"❌ httpx import failed: {e}")
        return False
    
    try:
        from markdown_it import MarkdownIt
        print("✅ markdown-it-py imported successfully")
    except ImportError as e:
        print(f"❌ markdown-it-py import failed: {e}")
        return False
    
    return True

def main():
    print("🧪 Running Text-to-PowerPoint Generator Tests\n")
    
    # Test imports first
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        return
    
    print()
    
    # Test heuristic planning
    try:
        test_heuristic_planning()
    except Exception as e:
        print(f"❌ Heuristic planning test failed: {e}")
    
    print()
    
    # Test LLM providers
    try:
        test_llm_providers()
    except Exception as e:
        print(f"❌ LLM provider test failed: {e}")
    
    print()
    
    # Test slide planning
    try:
        asyncio.run(test_slide_planning())
    except Exception as e:
        print(f"❌ Slide planning test failed: {e}")
    
    print("\n🎉 Test suite completed!")

if __name__ == "__main__":
    main()
