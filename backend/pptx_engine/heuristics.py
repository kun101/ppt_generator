from markdown_it import MarkdownIt

def rule_based_plan(text: str, guidance: str):
    """Generate a slide plan using heuristic rules when LLM fails."""
    md = MarkdownIt()
    tokens = md.parse(text)
    
    slides = []
    current_slide = {"title": "Overview", "layout_hint": "bullets", "bullets": []}
    
    for token in tokens:
        if token.type == "heading_open" and int(token.tag[1]) <= 2:
            # New section - save current slide and start new one
            if current_slide["bullets"] or current_slide["title"] != "Overview":
                slides.append(current_slide)
            current_slide = {"title": "", "layout_hint": "bullets", "bullets": []}
        elif token.type == "inline" and token.content.strip():
            if current_slide["title"] == "" or current_slide["title"] == "Overview":
                # Use as title
                current_slide["title"] = token.content.strip()[:90]
            else:
                # Add as bullet point
                for line in token.content.split("\n"):
                    if line.strip():
                        current_slide["bullets"].append(line.strip()[:180])
        elif token.type == "paragraph_open":
            # Handle regular paragraphs as bullets
            continue
    
    # Add the last slide if it has content
    if current_slide["bullets"] or current_slide["title"] != "Overview":
        slides.append(current_slide)
    
    # If no slides were created from markdown, create slides from raw text
    if not slides:
        slides = _create_slides_from_text(text, guidance)
    
    # Apply guidance-based limits
    max_slides = 12 if "short" in guidance.lower() else 18
    return slides[:max_slides]

def _create_slides_from_text(text: str, guidance: str):
    """Create slides from plain text by splitting into chunks."""
    slides = []
    
    # Split text into paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    if not paragraphs:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    # Group paragraphs into slides (roughly 3-4 bullets per slide)
    current_slide = {"title": "Introduction", "layout_hint": "bullets", "bullets": []}
    slide_count = 1
    
    for i, paragraph in enumerate(paragraphs):
        if len(current_slide["bullets"]) >= 4:
            # Start new slide
            slides.append(current_slide)
            slide_count += 1
            current_slide = {
                "title": f"Key Points {slide_count}",
                "layout_hint": "bullets",
                "bullets": []
            }
        
        # Split long paragraphs into multiple bullets
        if len(paragraph) > 200:
            sentences = paragraph.split('. ')
            for sentence in sentences:
                if sentence.strip():
                    current_slide["bullets"].append(sentence.strip()[:180])
                    if len(current_slide["bullets"]) >= 4:
                        break
        else:
            current_slide["bullets"].append(paragraph[:180])
    
    # Add the last slide
    if current_slide["bullets"]:
        slides.append(current_slide)
    
    # Ensure we have at least one slide
    if not slides:
        slides = [{
            "title": "Content Overview",
            "layout_hint": "bullets",
            "bullets": [text[:180]] if text else ["No content provided"]
        }]
    
    return slides
