from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE_TYPE
import tempfile
import os
import re
from io import BytesIO

def build_presentation(plan, style_ctx, template_path: str) -> bytes:
    """Build a PowerPoint presentation from the slide plan and template."""
    # Create new presentation from template
    prs = Presentation(template_path)
    
    # Clear existing slides but keep the template structure
    slide_idxs = list(range(len(prs.slides) - 1, -1, -1))
    for i in slide_idxs:
        rId = prs.slides._sldIdLst[i].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[i]
    
    # Collect image blobs for reuse
    image_pool = []
    for img_data in style_ctx["images"]:
        image_pool.append(img_data["blob"])
    
    # Generate slides from plan
    for i, slide_def in enumerate(plan["slides"]):
        # Choose layout based on hint
        layout = _pick_layout(prs, slide_def.get("layout_hint", "bullets"))
        slide = prs.slides.add_slide(layout)
        
        # Set title
        title_text = slide_def.get("title", f"Slide {i+1}")
        if hasattr(slide.shapes, "title") and slide.shapes.title:
            # Apply formatted text to title as well
            title_frame = slide.shapes.title.text_frame
            title_frame.clear()
            title_paragraph = title_frame.paragraphs[0]
            _apply_formatted_text(title_paragraph, title_text, style_ctx["theme"]["font_family"], is_title=True)
        
        # Add content
        bullets = slide_def.get("bullets", [])
        if bullets:
            body_shape = _find_body_placeholder(slide)
            if body_shape:
                _populate_bullets(body_shape, bullets, style_ctx["theme"]["font_family"])
        
        # Note: Automatic image insertion removed to prevent random icons from appearing
        
        # Add speaker notes
        notes = slide_def.get("notes", "")
        if notes and slide.has_notes_slide:
            slide.notes_slide.notes_text_frame.text = notes
    
    # Save to bytes
    output = BytesIO()
    prs.save(output)
    output.seek(0)
    return output.read()

def _pick_layout(prs, hint: str):
    """Select an appropriate layout based on the hint."""
    hint = hint.lower()
    layouts = prs.slide_layouts
    
    # Map hints to layout indices (varies by template)
    if "section" in hint and len(layouts) > 2:
        return layouts[2]  # Section header layout
    elif "two" in hint and len(layouts) > 3:
        return layouts[3]  # Two-column layout
    elif "title" in hint and len(layouts) > 0:
        return layouts[0]  # Title slide
    else:
        # Default to title+content layout
        return layouts[1] if len(layouts) > 1 else layouts[0]

def _find_body_placeholder(slide):
    """Find the main content placeholder on a slide."""
    for shape in slide.shapes:
        if shape.is_placeholder:
            ph_type = shape.placeholder_format.type
            # Type 2 is typically the body/content placeholder
            if ph_type == 2:  # PP_PLACEHOLDER.BODY
                return shape
    
    # Fallback: look for any text placeholder that's not the title
    for shape in slide.shapes:
        if (shape.is_placeholder and 
            hasattr(shape, 'text_frame') and 
            shape != getattr(slide.shapes, 'title', None)):
            return shape
    
    return None

def _populate_bullets(shape, bullets, font_family):
    """Populate a text shape with bullet points."""
    if not hasattr(shape, 'text_frame'):
        return
    
    text_frame = shape.text_frame
    text_frame.clear()
    
    for i, bullet in enumerate(bullets[:6]):  # Limit to 6 bullets
        if i == 0:
            # Use the first paragraph
            p = text_frame.paragraphs[0]
        else:
            # Add new paragraphs for additional bullets
            p = text_frame.add_paragraph()
        
        # Apply formatted text instead of plain text
        _apply_formatted_text(p, str(bullet), font_family, is_title=False)
        p.level = 0

def _apply_formatted_text(paragraph, text, font_family, font_size=None, is_title=False):
    """Apply Markdown formatting to a paragraph."""
    # Clear existing text
    paragraph.text = ""
    
    # Parse markdown formatting in the text
    parts = _parse_markdown_formatting(text)
    
    # Default font sizes
    if font_size is None:
        font_size = Pt(24) if is_title else Pt(18)
    
    for part_text, is_bold, is_italic in parts:
        if not part_text:
            continue
            
        # Add a text run to the paragraph
        run = paragraph.add_run()
        run.text = part_text
        
        # Apply base font styling
        run.font.name = font_family
        run.font.size = font_size
        
        # Apply formatting
        if is_bold:
            run.font.bold = True
        if is_italic:
            run.font.italic = True

def _parse_markdown_formatting(text):
    """Parse text with Markdown formatting and return list of (text, is_bold, is_italic) tuples."""
    parts = []
    current_pos = 0
    
    # Pattern for **bold** and *italic*
    bold_pattern = r'\*\*(.*?)\*\*'
    italic_pattern = r'\*(.*?)\*'
    
    # Find all bold matches first
    bold_matches = list(re.finditer(bold_pattern, text))
    italic_matches = list(re.finditer(italic_pattern, text))
    
    # Remove italic matches that are inside bold matches (to avoid double processing **)
    filtered_italic_matches = []
    for italic_match in italic_matches:
        is_inside_bold = False
        for bold_match in bold_matches:
            if bold_match.start() <= italic_match.start() and italic_match.end() <= bold_match.end():
                is_inside_bold = True
                break
        if not is_inside_bold:
            filtered_italic_matches.append(italic_match)
    
    # Combine and sort all matches
    all_matches = []
    for match in bold_matches:
        all_matches.append((match.start(), match.end(), match.group(1), True, False))
    for match in filtered_italic_matches:
        all_matches.append((match.start(), match.end(), match.group(1), False, True))
    
    all_matches.sort(key=lambda x: x[0])
    
    # Build parts list
    for start, end, matched_text, is_bold, is_italic in all_matches:
        # Add text before this match
        if current_pos < start:
            plain_text = text[current_pos:start]
            if plain_text:
                parts.append((plain_text, False, False))
        
        # Add the formatted text
        parts.append((matched_text, is_bold, is_italic))
        current_pos = end
    
    # Add remaining text
    if current_pos < len(text):
        remaining_text = text[current_pos:]
        if remaining_text:
            parts.append((remaining_text, False, False))
    
    # If no formatting was found, return the whole text as plain
    if not parts:
        parts = [(text, False, False)]
    
    return parts

def _apply_font_style(shape, font_family):
    """Apply font styling to a text shape."""
    if not hasattr(shape, 'text_frame'):
        return
    
    for paragraph in shape.text_frame.paragraphs:
        if paragraph.font:
            paragraph.font.name = font_family

def _add_reused_image(slide, image_blob, layout_hint):
    """Add a reused image to the slide."""
    try:
        # Create temporary file for the image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            tmp_file.write(image_blob)
            tmp_path = tmp_file.name
        
        # Determine position and size based on layout hint
        if "section" in layout_hint:
            # Full-width banner image
            left = Inches(0.5)
            top = Inches(2.0)
            width = Inches(9.0)
            height = None  # Maintain aspect ratio
        elif "image-left" in layout_hint:
            # Left side image
            left = Inches(0.5)
            top = Inches(1.5)
            width = Inches(4.0)
            height = None
        elif "image-right" in layout_hint:
            # Right side image
            left = Inches(5.5)
            top = Inches(1.5)
            width = Inches(4.0)
            height = None
        else:
            # Default centered image
            left = Inches(3.0)
            top = Inches(2.0)
            width = Inches(4.0)
            height = None
        
        # Add the image
        if height:
            slide.shapes.add_picture(tmp_path, left, top, width, height)
        else:
            slide.shapes.add_picture(tmp_path, left, top, width)
        
    except Exception as e:
        print(f"Failed to add image: {e}")
    finally:
        # Clean up temporary file
        try:
            os.remove(tmp_path)
        except:
            pass
