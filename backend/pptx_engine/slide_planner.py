import json
from .heuristics import rule_based_plan

SYSTEM_PROMPT = """You are an expert presentation designer. Turn long text into a concise, well-structured slide deck. 

Rules:
1. Output strict JSON in this format: {"slides": [...]}. DO NOT INCLUDE UNNECESSARY TEXT OR MARKUP, OUTPUT SHOULD ALWAYS BE VALID JSON. DO NOT START WITH MARKDOWN OR SOMETHING, STRICTLY FOLLOW THE MENTIONED FORMAT.
2. Use 6-18 slides unless guidance suggests otherwise
3. Each slide should have: title, layout_hint, bullets (max 6 per slide), optional notes
4. Available layout_hints: "title+content", "section", "two-column", "bullets", "image-left", "image-right", "image-content", "quote"
5. Template images are available for reuse - use "image-left", "image-right", or "image-content" layouts strategically
6. Keep bullet points concise and actionable
7. Match the tone and structure specified in guidance
8. Use image layouts for key concepts, examples, or visual sections

Be strategic about information hierarchy and flow. When the template has images, use them to enhance key messages."""

USER_PROMPT_TEMPLATE = """INPUT TEXT:
```
{text}
```

GUIDANCE (optional):
```
{guidance}
```

TEMPLATE INFO:
- Template has {image_count} reusable images
- Image layouts available: {has_image_layouts}

Convert this into a presentation following the rules. Return JSON with a 'slides' array where each slide has:
- title: Clear, engaging slide title
- layout_hint: Choose from available options (use image layouts strategically when template images are available)
- bullets: Array of key points (max 6 per slide)
- notes: Optional speaker notes

Focus on creating logical flow and clear messaging. Use image layouts for approximately 30-40% of slides when template images are available."""

async def make_slide_plan(text: str, guidance: str, style_ctx, llm):
    """Generate a slide plan using LLM with heuristic fallback."""
    try:
        # Analyze template capabilities
        image_count = len(style_ctx.get("images", []))
        layout_info = style_ctx.get("theme", {}).get("layout_info", {})
        
        has_image_layouts = any(
            any(p.get("is_image_placeholder", False) for p in layout.get("placeholders", []))
            for layout in layout_info.values()
        )
        
        # Truncate text to avoid token limits
        truncated_text = text[:16000]
        truncated_guidance = guidance[:500]
        
        prompt = USER_PROMPT_TEMPLATE.format(
            text=truncated_text,
            guidance=truncated_guidance,
            image_count=image_count,
            has_image_layouts="Yes" if has_image_layouts else "No"
        )
        
        response = await llm.generate(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            json=True
        )
        
        print(f"DEBUG: LLM response received: {response[:200]}...")  # Log first 200 chars
        
        # Parse and validate the JSON response
        data = json.loads(response)
        
        if not isinstance(data, dict) or "slides" not in data:
            raise ValueError("Invalid response format")
        
        if not isinstance(data["slides"], list) or len(data["slides"]) == 0:
            raise ValueError("No slides in response")
        
        # Validate each slide has required fields
        for slide in data["slides"]:
            if not isinstance(slide, dict):
                raise ValueError("Invalid slide format")
            if "title" not in slide:
                slide["title"] = "Untitled Slide"
            if "layout_hint" not in slide:
                slide["layout_hint"] = "bullets"
            if "bullets" not in slide:
                slide["bullets"] = []
        
        return data
        
    except Exception as e:
        print(f"LLM planning failed: {e}. Using heuristic fallback.")
        
        # Log more details for debugging
        import traceback
        print(f"Full error traceback: {traceback.format_exc()}")
        
        # Fallback to rule-based planning
        fallback_slides = rule_based_plan(text, guidance)
        return {"slides": fallback_slides}
