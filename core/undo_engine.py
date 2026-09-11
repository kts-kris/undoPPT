"""undo_engine.py - PPTX Master & Template Reverse-Engineering Engine.

Extracts Slide Masters, Layouts, Placeholders, Colors, Fonts, and Grid Geometry
from any user-supplied .pptx file, standardizing them into a Design Tokens protocol.
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


def extract_template_tokens(pptx_path: str) -> Dict[str, Any]:
    """Deconstruct a PPTX file and extract its design system tokens."""
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
    font_family_counter: Counter = Counter()
    title_fonts: Counter = Counter()
    body_fonts: Counter = Counter()
    font_sizes: List[float] = []

    # Safe margin tracking
    left_margins = []
    top_margins = []

    # Parse slides & slide masters
    for slide in prs.slides:
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

    # Infer color palette roles
    # Default fallbacks
    palette = {
        "primary": "#1A56DB",
        "secondary": "#3B82F6",
        "accent": "#F59E0B",
        "background": "#F8FAFC",
        "surface": "#FFFFFF",
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
    }

    # Map discovered colors if available
    if top_colors:
        # Separate light vs dark colors
        dark_colors = []
        light_colors = []
        vibrant_colors = []

        for hex_code in top_colors:
            r = int(hex_code[1:3], 16)
            g = int(hex_code[3:5], 16)
            b = int(hex_code[5:7], 16)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            if brightness < 100:
                dark_colors.append(hex_code)
            elif brightness > 220:
                light_colors.append(hex_code)
            else:
                vibrant_colors.append(hex_code)

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

    # Calculate safe margin
    default_left_margin = min(left_margins) if left_margins else 0.8
    default_top_margin = min(top_margins) if top_margins else 0.8

    # Layout templates mapping
    layouts_info = []
    for idx, layout in enumerate(prs.slide_layouts):
        ph_names = [ph.name for ph in layout.placeholders]
        layouts_info.append({
            "index": idx,
            "name": layout.name,
            "placeholders": ph_names
        })

    tokens = {
        "source_template": os.path.basename(pptx_path),
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
            "border_color": "#E2E8F0",
            "background": palette["surface"],
            "shadow": "0 4px 6px -1px rgba(0,0,0,0.05)"
        },
        "master_layouts_count": len(layouts_info),
        "layouts": layouts_info[:8]
    }

    return tokens


def save_tokens(tokens: Dict[str, Any], output_path: str) -> str:
    """Save extracted design tokens to a JSON file."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)
    return output_path
