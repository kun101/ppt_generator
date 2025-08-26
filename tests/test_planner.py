import pytest
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.pptx_engine.slide_planner import make_slide_plan
from backend.pptx_engine.heuristics import rule_based_plan

class MockLLM:
    """Mock LLM for testing."""
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
    
    async def generate(self, prompt, system="", json=True):
        if self.should_fail:
            raise Exception("Mock LLM failure")
        
        return '''
        {
            "slides": [
                {
                    "title": "Test Slide 1",
                    "layout_hint": "bullets",
                    "bullets": ["Point 1", "Point 2", "Point 3"],
                    "notes": "Test notes"
                },
                {
                    "title": "Test Slide 2", 
                    "layout_hint": "section",
                    "bullets": ["Point A", "Point B"],
                    "notes": "More notes"
                }
            ]
        }
        '''

def test_rule_based_plan_basic():
    """Test that rule-based planning works with basic text."""
    text = """
    # Introduction
    This is the introduction section.
    
    # Main Content  
    This is the main content with some details.
    
    # Conclusion
    This is the conclusion.
    """
    
    guidance = ""
    result = rule_based_plan(text, guidance)
    
    assert len(result) > 0
    assert all(isinstance(slide, dict) for slide in result)
    assert all("title" in slide for slide in result)
    assert all("layout_hint" in slide for slide in result)
    assert all("bullets" in slide for slide in result)

def test_rule_based_plan_with_guidance():
    """Test that guidance affects slide count."""
    text = "This is a long text that could be many slides. " * 100
    
    short_guidance = "short presentation"
    long_guidance = "detailed presentation"
    
    short_result = rule_based_plan(text, short_guidance)
    long_result = rule_based_plan(text, long_guidance)
    
    assert len(short_result) <= 12  # Should respect "short" guidance
    assert len(long_result) <= 18   # Should respect normal limits

def test_rule_based_plan_plain_text():
    """Test that plain text (no markdown) works."""
    text = """
    This is plain text without markdown headers.
    
    It has multiple paragraphs and should be converted into slides.
    
    Each paragraph might become a bullet point or slide.
    
    The algorithm should handle this gracefully.
    """
    
    result = rule_based_plan(text, "")
    
    assert len(result) > 0
    assert result[0]["title"]  # Should have a title
    assert len(result[0]["bullets"]) > 0  # Should have content

@pytest.mark.asyncio
async def test_make_slide_plan_success():
    """Test successful slide planning with mock LLM."""
    text = "This is test content for slide generation."
    guidance = "test presentation"
    style_ctx = {"theme": {"font_family": "Arial"}, "images": []}
    
    mock_llm = MockLLM(should_fail=False)
    result = await make_slide_plan(text, guidance, style_ctx, mock_llm)
    
    assert "slides" in result
    assert len(result["slides"]) == 2  # Based on mock response
    assert result["slides"][0]["title"] == "Test Slide 1"

@pytest.mark.asyncio  
async def test_make_slide_plan_fallback():
    """Test that fallback works when LLM fails."""
    text = """
    # Test Header
    This is test content.
    
    # Another Header  
    More test content here.
    """
    guidance = "test presentation"
    style_ctx = {"theme": {"font_family": "Arial"}, "images": []}
    
    mock_llm = MockLLM(should_fail=True)
    result = await make_slide_plan(text, guidance, style_ctx, mock_llm)
    
    assert "slides" in result
    assert len(result["slides"]) > 0  # Should fall back to heuristic planning

if __name__ == "__main__":
    pytest.main([__file__])
