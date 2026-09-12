"""undo_engine.py - PPTX Master & Template Reverse-Engineering Engine (v2.5.0).

Extracts Slide Masters, Layouts, Placeholders AST, Theme Mode (Dark/Light),
Card Geometry, Fonts, and Visual Media Assets from any user-supplied .pptx file,
standardizing them into a Design Tokens protocol.
"""

from collections import Counter
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.util import Inches, Pt


def _rgb_to_hex(rgb) -> Optional[str]:
    """Convert RGBColor to hex string #RRGGBB."""
    if rgb is None:
        return None
    try:
        return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
    except Exception:
        return None


def _calc_luminance(hex_code: str) -> float:
    """Calculate relative luminance (0 to 255) for hex color."""
    try:
        r = int(hex_code[1:3], 16)
        g = int(hex_code[3:5], 16)
        b = int(hex_code[5:7], 16)
        return (r * 299 + g * 587 + b * 114) / 1000.0
    except Exception:
        return 255.0


def extract_template_assets(pptx_path: str, assets_dir: str = ".undoppt/assets") -> List[Dict[str, Any]]:
    """Extract embedded images, logos, and media assets from PPTX into assets directory."""
    if not os.path.exists(pptx_path):
        return []

    os.makedirs(assets_dir, exist_ok=True)
    prs = Presentation(pptx_path)
    extracted = []
    seen_hashes = set()

    asset_idx = 0
    for slide_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE or hasattr(shape, "image"):
                try:
                    img = shape.image
                    blob = img.blob
                    blob_hash = hash(blob)
                    if blob_hash in seen_hashes:
                        continue
                    seen_hashes.add(blob_hash)

                    ext = img.ext or "png"
                    filename = f"asset_s{slide_idx+1}_{asset_idx}.{ext}"
                    filepath = os.path.join(assets_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(blob)

                    extracted.append({
                        "filename": filename,
                        "path": filepath,
                        "slide_index": slide_idx + 1,
                        "width_inches": round(shape.width.inches, 2) if shape.width else 0,
                        "height_inches": round(shape.height.inches, 2) if shape.height else 0,
                        "content_type": img.content_type
                    })
                    asset_idx += 1
                except Exception:
                    pass

    return extracted


def extract_template_tokens(pptx_path: str, extract_assets: bool = False, assets_dir: Optional[str] = None) -> Dict[str, Any]:
    """Deconstruct a PPTX file and extract its design system tokens and AST geometry."""
    if not os.path.exists(pptx_path):
        raise FileNotFoundError(f"Template file not found: {pptx_path}")

    prs = Presentation(pptx_path)

    # 1. Canvas dimensions & aspect ratio
    width_inches = prs.slide_width.inches
    height_inches = prs.slide_height.inches
    ratio_val = width_inches / height_inches if height_inches > 0 else 16 / 9
    aspect_ratio = "16:9" if abs(ratio_val - 16 / 9) < 0.1 else ("4:3" if abs(ratio_val - 4 / 3) < 0.1 else "custom")

    # 2. Extract color frequencies across text, shapes, and backgrounds
    color_counter: Counter = Counter()
    bg_color_counter: Counter = Counter()
    font_family_counter: Counter = Counter()
    title_fonts: Counter = Counter()
    body_fonts: Counter = Counter()
    font_sizes: List[float] = []

    # Safe margin tracking
    left_margins = []
    top_margins = []

    # Parse slides & slide masters
    for slide in prs.slides:
        # Check background fill if present
        try:
            if slide.background and slide.background.fill and slide.background.fill.type == 1:
                bg_hex = _rgb_to_hex(slide.background.fill.fore_color.rgb)
                if bg_hex:
                    bg_color_counter[bg_hex] += 5
        except Exception:
            pass

        for shape in slide.shapes:
            # Check margins
            if shape.has_text_frame:
                left_margins.append(shape.left.inches)
                top_margins.append(shape.top.inches)

            # Check shape fill
            try:
                if shape.fill and shape.fill.type == 1:  # Solid fill
                    hex_col = _rgb_to_hex(shape.fill.fore_color.rgb)
                    if hex_col:
                        color_counter[hex_col] += 1
                        # If shape is large enough to be a background container
                        if shape.width and shape.height:
                            if shape.width.inches > width_inches * 0.8 and shape.height.inches > height_inches * 0.8:
                                bg_color_counter[hex_col] += 3
            except Exception:
                pass

            # Check text runs
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        # Font name
                        if run.font.name:
                            font_family_counter[run.font.name] += 1
                            if run.font.size and run.font.size.pt >= 24:
                                title_fonts[run.font.name] += 1
                            else:
                                body_fonts[run.font.name] += 1

                        # Font size
                        if run.font.size:
                            font_sizes.append(run.font.size.pt)

                        # Text color
                        try:
                            if run.font.color and run.font.color.rgb:
                                hex_col = _rgb_to_hex(run.font.color.rgb)
                                if hex_col:
                                    color_counter[hex_col] += 1
                        except Exception:
                            pass

    # Default typography & colors if not extracted
    primary_font = font_family_counter.most_common(1)[0][0] if font_family_counter else "PingFang SC, Inter, sans-serif"
    title_font = title_fonts.most_common(1)[0][0] if title_fonts else primary_font
    body_font = body_fonts.most_common(1)[0][0] if body_fonts else primary_font

    top_colors = [c[0] for c in color_counter.most_common(8)]

    # Determine Theme Mode (Dark vs Light)
    bg_candidate = bg_color_counter.most_common(1)[0][0] if bg_color_counter else None
    if bg_candidate:
        is_dark = _calc_luminance(bg_candidate) < 128
    else:
        # Check overall colors
        is_dark = False

    theme_mode = "dark" if is_dark else "light"

    # Infer color palette roles
    if is_dark:
        palette = {
            "primary": "#3B82F6",
            "secondary": "#60A5FA",
            "accent": "#F59E0B",
            "background": bg_candidate or "#0F172A",
            "surface": "#1E293B",
            "text_primary": "#F8FAFC",
            "text_secondary": "#94A3B8",
        }
    else:
        palette = {
            "primary": "#1A56DB",
            "secondary": "#3B82F6",
            "accent": "#F59E0B",
            "background": bg_candidate or "#F8FAFC",
            "surface": "#FFFFFF",
            "text_primary": "#0F172A",
            "text_secondary": "#475569",
        }

    # Map discovered colors if available
    if top_colors:
        dark_colors = []
        light_colors = []
        vibrant_colors = []

        for hex_code in top_colors:
            lum = _calc_luminance(hex_code)
            if lum < 100:
                dark_colors.append(hex_code)
            elif lum > 220:
                light_colors.append(hex_code)
            else:
                vibrant_colors.append(hex_code)

        if not is_dark:
            if dark_colors:
                palette["text_primary"] = dark_colors[0]
            if vibrant_colors:
                palette["primary"] = vibrant_colors[0]
                if len(vibrant_colors) > 1:
                    palette["secondary"] = vibrant_colors[1]
                if len(vibrant_colors) > 2:
                    palette["accent"] = vibrant_colors[2]
            if light_colors:
                palette["background"] = light_colors[0]
        else:
            if light_colors:
                palette["text_primary"] = light_colors[0]
            if vibrant_colors:
                palette["primary"] = vibrant_colors[0]
                if len(vibrant_colors) > 1:
                    palette["secondary"] = vibrant_colors[1]
                if len(vibrant_colors) > 2:
                    palette["accent"] = vibrant_colors[2]
            if dark_colors:
                palette["background"] = dark_colors[0]

    # Calculate safe margin
    default_left_margin = min(left_margins) if left_margins else 0.8
    default_top_margin = min(top_margins) if top_margins else 0.8

    # Deep Master Layout Placeholders AST Deconstruction
    layouts_info = []
    master_slots_summary = {
        "title_slot": None,
        "body_slot": None,
        "footer_slot": None
    }

    for idx, layout in enumerate(prs.slide_layouts):
        slots = []
        for ph in layout.placeholders:
            ph_type_name = "UNKNOWN"
            ph_idx = None
            try:
                if hasattr(ph, "placeholder_format"):
                    ph_type_name = str(getattr(ph.placeholder_format, "type", "UNKNOWN")).replace("PP_PLACEHOLDER.", "")
                    ph_idx = getattr(ph.placeholder_format, "idx", None)
            except Exception:
                pass

            slot_geom = {
                "idx": ph_idx,
                "name": ph.name,
                "type": ph_type_name,
                "left_inches": round(ph.left.inches, 2) if ph.left else 0,
                "top_inches": round(ph.top.inches, 2) if ph.top else 0,
                "width_inches": round(ph.width.inches, 2) if ph.width else 0,
                "height_inches": round(ph.height.inches, 2) if ph.height else 0,
            }
            slots.append(slot_geom)

            # Record standard slots for top-level reference
            if "TITLE" in ph_type_name and not master_slots_summary["title_slot"]:
                master_slots_summary["title_slot"] = slot_geom
            elif "BODY" in ph_type_name and not master_slots_summary["body_slot"]:
                master_slots_summary["body_slot"] = slot_geom
            elif "FOOTER" in ph_type_name and not master_slots_summary["footer_slot"]:
                master_slots_summary["footer_slot"] = slot_geom

        layouts_info.append({
            "index": idx,
            "name": layout.name,
            "placeholders_count": len(slots),
            "slots": slots
        })

    # Optional media asset extraction
    extracted_assets = []
    if extract_assets:
        target_dir = assets_dir or os.path.join(os.path.dirname(os.path.abspath(pptx_path)), ".undoppt", "assets")
        extracted_assets = extract_template_assets(pptx_path, target_dir)

    tokens = {
        "source_template": os.path.basename(pptx_path),
        "theme_mode": theme_mode,
        "canvas": {
            "width_inches": round(width_inches, 2),
            "height_inches": round(height_inches, 2),
            "aspect_ratio": aspect_ratio,
            "margin_left_inches": round(max(0.5, default_left_margin), 2),
            "margin_top_inches": round(max(0.6, default_top_margin), 2)
        },
        "palette": palette,
        "typography": {
            "title": {
                "font": title_font,
                "size": 36,
                "weight": "bold",
                "color": palette["text_primary"]
            },
            "subtitle": {
                "font": body_font,
                "size": 20,
                "weight": "medium",
                "color": palette["text_secondary"]
            },
            "body": {
                "font": body_font,
                "size": 15,
                "weight": "normal",
                "color": palette["text_secondary"]
            },
            "kpi_number": {
                "font": "DIN Alternate, Helvetica Neue, Arial, sans-serif",
                "size": 54,
                "weight": "bold",
                "color": palette["primary"]
            }
        },
        "card_style": {
            "border_radius": 12,
            "border_color": "#334155" if is_dark else "#E2E8F0",
            "background": palette["surface"],
            "shadow": "0 4px 6px -1px rgba(0,0,0,0.2)" if is_dark else "0 4px 6px -1px rgba(0,0,0,0.05)"
        },
        "master_slots": master_slots_summary,
        "master_layouts_count": len(layouts_info),
        "layouts": layouts_info[:8],
        "extracted_assets": extracted_assets
    }

    return tokens


def save_tokens(tokens: Dict[str, Any], output_path: str) -> str:
    """Save extracted design tokens to a JSON file."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)
    return output_path
