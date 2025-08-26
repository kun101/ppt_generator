from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def analyze_template(path: str):
    """Analyze a PowerPoint template to extract reusable style and assets."""
    prs = Presentation(path)

    # Collect layouts by index
    layouts = {i: layout for i, layout in enumerate(prs.slide_layouts)}
    
    # Simple theme hints (python-pptx exposes limited theme info)
    theme = {
        "font_family": _infer_font(prs),
        "accent_colors": _infer_colors(prs)
    }

    # Harvest images from all slides in template
    reusable_images = []
    for s_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                try:
                    reusable_images.append({
                        "slide_index": s_idx,
                        "name": getattr(shape, "name", f"pic_{s_idx}"),
                        "blob": shape.image.blob,     # bytes
                        "width": shape.width, 
                        "height": shape.height
                    })
                except Exception:
                    # Skip if image extraction fails
                    continue
    
    return {
        "layouts": layouts,          # not JSON-serializable; used in-process
        "theme": theme,
        "images": reusable_images,
        "prs": prs
    }

def _infer_font(prs):
    """Infer the primary font from the template."""
    try:
        # Look at title placeholder on first layout as a heuristic
        layout = prs.slide_layouts[0]
        if hasattr(layout.shapes, 'title') and layout.shapes.title:
            text_frame = layout.shapes.title.text_frame
            if text_frame.paragraphs:
                font = text_frame.paragraphs[0].font
                if font and font.name:
                    return font.name
    except Exception:
        pass
    return "Calibri"

def _infer_colors(prs):
    """Infer accent colors from the template."""
    colors = []
    try:
        # Look at fills from shapes in first few layouts
        for layout in prs.slide_layouts[:3]:
            for shape in layout.shapes:
                if hasattr(shape, "fill") and shape.fill:
                    try:
                        if hasattr(shape.fill, "fore_color") and shape.fill.fore_color:
                            if hasattr(shape.fill.fore_color, "rgb"):
                                colors.append(str(shape.fill.fore_color.rgb))
                    except Exception:
                        continue
                if len(colors) >= 6:
                    break
            if len(colors) >= 6:
                break
    except Exception:
        pass
    return colors[:6]
