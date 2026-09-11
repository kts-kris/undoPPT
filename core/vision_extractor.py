"""vision_extractor.py - Visual Heuristic Template Extractor (Mode B).

For non-standard templates, slides with ad-hoc shapes, or visual style references,
this module standardizes typography hierarchy, color harmony, and layout grids
into the undoPPT Design Tokens protocol.
"""

from typing import Any, Dict, Optional


def create_tokens_from_style_spec(
    theme_name: str = "modern_bento",
    primary_color: str = "#1A56DB",
    background_color: str = "#F8FAFC",
    dark_mode: bool = False,
    custom_font: Optional[str] = None
) -> Dict[str, Any]:
    """Generate standardized Design Tokens from high-level visual styling parameters."""
    font_stack = custom_font or "PingFang SC, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"

    if dark_mode:
        palette = {
            "primary": primary_color,
            "secondary": "#60A5FA",
            "accent": "#F59E0B",
            "background": "#0F172A",
            "surface": "#1E293B",
            "surface_subtle": "#334155",
            "text_primary": "#F8FAFC",
            "text_secondary": "#94A3B8",
            "border": "#334155"
        }
    else:
        palette = {
            "primary": primary_color,
            "secondary": "#3B82F6",
            "accent": "#F59E0B",
            "background": background_color,
            "surface": "#FFFFFF",
            "surface_subtle": "#F1F5F9",
            "text_primary": "#0F172A",
            "text_secondary": "#475569",
            "border": "#E2E8F0"
        }

    tokens = {
        "source_template": f"heuristic_{theme_name}",
        "canvas": {
            "width_inches": 13.333,
            "height_inches": 7.5,
            "aspect_ratio": "16:9",
            "margin_left_inches": 0.8,
            "margin_top_inches": 0.8
        },
        "palette": palette,
        "typography": {
            "title": {
                "font": font_stack,
                "size": 34,
                "weight": "bold",
                "color": palette["text_primary"]
            },
            "subtitle": {
                "font": font_stack,
                "size": 18,
                "weight": "medium",
                "color": palette["text_secondary"]
            },
            "body": {
                "font": font_stack,
                "size": 14,
                "weight": "normal",
                "color": palette["text_secondary"]
            },
            "kpi_number": {
                "font": "DIN Alternate, Helvetica Neue, Arial, sans-serif",
                "size": 52,
                "weight": "bold",
                "color": palette["primary"]
            }
        },
        "card_style": {
            "border_radius": 12,
            "border_color": palette["border"],
            "background": palette["surface"],
            "shadow": "0 4px 6px -1px rgba(0,0,0,0.06)"
        }
    }

    return tokens
