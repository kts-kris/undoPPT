"""layout_fit.py - Content-adaptive layout pass for the native PPTX builder (v3.5).

The slide renderers place shapes at fixed coordinates. This module measures the
text that actually sits in those shapes and then:
  1. fits the header title to one line (shrinks the font, never wraps into content);
  2. rounds cards with a token-driven radius instead of python-pptx's default 1/6;
  3. shrinks over-sized cards to their content and scales sparse text up;
  4. vertically balances the remaining content block;
  5. applies the token font to every run (latin + east-asian).

Text measurement is a heuristic (CJK = 1 em, Latin ~ 0.55 em); the visual
render check (core/render_check.py) is the ground-truth verification.
"""

import math
from typing import Any, Dict, List, Optional, Tuple

from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

LINE_HEIGHT = 1.25
DEFAULT_FONT_PT = 18.0
HEADER_BOTTOM_IN = 1.95
CONTENT_FLOOR_IN = 7.0
FIT_LAYOUTS = {"bento_cards", "metric_spotlight", "timeline", "content_columns", "kpi_dashboard", "process_flow"}
BALANCE_ONLY_LAYOUTS = {"standard_table", "table"}
MIN_FONT_PT = 12.0
MAX_FLOOR_SCALE = 1.4
NO_FLOOR_LAYOUTS = {"cover"}


def pick_font(spec: Optional[str], default: str = "PingFang SC") -> str:
    """Token font specs are CSS stacks ('PingFang SC, Inter, sans-serif'); PowerPoint needs one name."""
    if not spec:
        return default
    first = spec.split(",")[0].strip().strip("'\"")
    return first or default


def char_width_em(ch: str) -> float:
    o = ord(ch)
    if o >= 0x2E80 or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF:
        return 1.0
    if ch == " ":
        return 0.3
    if ch in ".,:;'|!":
        return 0.3
    if ch in "-/()[]":
        return 0.38
    if ch == "%":
        return 0.85
    if ch.isdigit():
        return 0.56
    if ch.isupper():
        return 0.64
    if ch.isalpha():
        return 0.54
    return 0.6


def text_width_pt(text: str, size_pt: float, bold: bool = False) -> float:
    w = sum(char_width_em(c) for c in text) * size_pt
    return w * 1.05 if bold else w


def fit_title_size(title: str, width_in: float, max_pt: float, min_pt: float = 22.0) -> Tuple[float, bool]:
    """Return (font_pt, fits_one_line). Shrinks until the title fits one line or min_pt is hit."""
    avail = width_in * 72 * 0.93
    size = float(max_pt)
    while size >= min_pt:
        if text_width_pt(title, size, bold=True) <= avail:
            return size, True
        size -= 1
    return float(min_pt), text_width_pt(title, min_pt, bold=True) <= avail


def _para_runs(p) -> List[Tuple[str, float, bool]]:
    out = []
    for r in p.runs:
        size = r.font.size.pt if r.font.size is not None else None
        out.append((r.text, size, bool(r.font.bold)))
    return out


def estimate_text_height_in(tf, width_in: float, scale: float = 1.0) -> float:
    """Estimated rendered height (inches) of a text frame laid out at width_in."""
    ml = (tf.margin_left if tf.margin_left is not None else Inches(0.1))
    mr = (tf.margin_right if tf.margin_right is not None else Inches(0.1))
    mt = (tf.margin_top if tf.margin_top is not None else Inches(0.05))
    mb = (tf.margin_bottom if tf.margin_bottom is not None else Inches(0.05))
    avail_pt = (width_in * 72) - (Emu(ml).pt + Emu(mr).pt)
    avail_pt = max(avail_pt * 0.96, 10)
    total_pt = Emu(mt).pt + Emu(mb).pt
    for p in tf.paragraphs:
        runs = _para_runs(p)
        if not runs:
            total_pt += DEFAULT_FONT_PT * scale * LINE_HEIGHT
            continue
        width = 0.0
        max_size = 0.0
        for text, size, bold in runs:
            s = (size or DEFAULT_FONT_PT) * scale
            width += text_width_pt(text, s, bold)
            max_size = max(max_size, s)
        lines = max(1, math.ceil(width / avail_pt))
        total_pt += lines * max_size * LINE_HEIGHT
        if p.space_before is not None:
            total_pt += p.space_before.pt * scale
        if p.space_after is not None:
            total_pt += p.space_after.pt * scale
    return total_pt / 72.0


def _scale_fonts(tf, scale: float):
    for p in tf.paragraphs:
        for r in p.runs:
            if r.font.size is not None:
                r.font.size = Pt(round(r.font.size.pt * scale * 2) / 2)
        if p.space_before is not None:
            p.space_before = Pt(p.space_before.pt * scale)
        if p.space_after is not None:
            p.space_after = Pt(p.space_after.pt * scale)


def _in(emu) -> float:
    return Emu(emu).inches


def _is_empty_card(shape) -> bool:
    return (
        shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE
        and shape.auto_shape_type == MSO_SHAPE.ROUNDED_RECTANGLE
        and (not shape.has_text_frame or not shape.text_frame.text.strip())
    )


def _contains(card, box, eps_in: float = 0.02) -> bool:
    e = Inches(eps_in)
    return (
        box.left >= card.left - e
        and box.top >= card.top - e
        and box.left + box.width <= card.left + card.width + e
        and box.top + box.height <= card.top + card.height + e
    )


def _runs(tf):
    return [r for p in tf.paragraphs for r in p.runs if r.text.strip() and r.font.size is not None]


def _holder_height_in(shape, cards) -> float:
    """Vertical room (inches) available to the text in `shape`."""
    if shape.shape_type == MSO_SHAPE_TYPE.TEXT_BOX:
        for c in cards:
            if _contains(c, shape):
                return _in(c.top + c.height) - _in(shape.top) - 0.05
        return _in(shape.height)
    return _in(shape.height)


def enforce_min_font(slide, floor_pt: float = MIN_FONT_PT):
    """Scale up frames whose smallest run is under floor_pt, backing off if the text would overflow."""
    cards = [s for s in slide.shapes if _is_empty_card(s)]
    changed = 0
    for shape in slide.shapes:
        if not shape.has_text_frame or shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            continue
        if shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and shape.auto_shape_type not in (
            MSO_SHAPE.RECTANGLE, MSO_SHAPE.ROUNDED_RECTANGLE
        ):
            continue  # ovals etc. have an inscribed text area narrower than the frame; sizes are set by the renderer
        tf = shape.text_frame
        runs = _runs(tf)
        if not runs:
            continue
        smallest = min(r.font.size.pt for r in runs)
        if smallest >= floor_pt:
            continue
        factor = min(MAX_FLOOR_SCALE, floor_pt / smallest)
        avail = _holder_height_in(shape, cards)
        width = _in(shape.width)
        while factor > 1.02 and estimate_text_height_in(tf, width, scale=factor) > avail:
            factor -= 0.04
        if factor > 1.02:
            _scale_fonts(tf, factor)
            changed += 1
    return changed


def fit_self_text_cards(slide):
    """Cards that carry their own text (e.g. content_columns): scale sparse text up, shrink to content."""
    cards = [
        s for s in slide.shapes
        if s.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE
        and s.auto_shape_type == MSO_SHAPE.ROUNDED_RECTANGLE
        and s.has_text_frame and s.text_frame.text.strip()
        and _in(s.top) >= HEADER_BOTTOM_IN - 0.1 and _in(s.height) > 1.6
    ]
    if not cards:
        return 0
    for c in cards:
        tf = c.text_frame
        need = estimate_text_height_in(tf, _in(c.width))
        fill = need / max(_in(c.height), 0.1)
        if 0.05 < fill < 0.6:
            scale = min(1.3, math.sqrt(0.7 / fill))
            if scale > 1.04:
                _scale_fonts(tf, scale)
        elif fill > 1.0:
            _scale_fonts(tf, max(0.85, 1.0 / fill))
    rows: Dict[int, List[Any]] = {}
    for c in cards:
        rows.setdefault(round(_in(c.top) / 0.1), []).append(c)
    for row in rows.values():
        needs = [estimate_text_height_in(c.text_frame, _in(c.width)) for c in row]
        orig = max(_in(c.height) for c in row)
        target = min(orig, max(max(needs) * 1.12, 1.6))
        for c in row:
            c.height = Inches(target)
            c.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    return len(cards)


def apply_card_radius(slide, radius_in: float):
    for shape in slide.shapes:
        if (
            shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE
            and shape.auto_shape_type == MSO_SHAPE.ROUNDED_RECTANGLE
        ):
            short = min(_in(shape.width), _in(shape.height))
            if short <= 0:
                continue
            shape.adjustments[0] = max(0.02, min(0.5, radius_in / short))


def apply_font_family(slide, latin: str):
    """Set latin + east-asian typeface on every run so CJK text does not fall back to the theme font."""
    for shape in slide.shapes:
        frames = []
        if shape.has_text_frame:
            frames.append(shape.text_frame)
        if getattr(shape, "has_table", False) and shape.has_table:
            for row in shape.table.rows:
                for cell in row.cells:
                    frames.append(cell.text_frame)
        for tf in frames:
            for p in tf.paragraphs:
                for r in p.runs:
                    rpr = r._r.get_or_add_rPr()
                    latin_el = rpr.find(qn("a:latin"))
                    if latin_el is None or latin_el.get("typeface") in (None, ""):
                        r.font.name = latin
                    elif "," in latin_el.get("typeface", ""):
                        r.font.name = pick_font(latin_el.get("typeface"))
                    ea = rpr.find(qn("a:ea"))
                    if ea is None:
                        ea = rpr.makeelement(qn("a:ea"), {})
                        latin_el = rpr.find(qn("a:latin"))
                        if latin_el is not None:
                            latin_el.addnext(ea)
                        else:
                            rpr.append(ea)
                    ea.set("typeface", latin)


def fit_cards(slide):
    """Shrink cards to their text and scale sparse text up. Returns the number of cards adjusted."""
    cards = [s for s in slide.shapes if _is_empty_card(s) and s.top > Inches(HEADER_BOTTOM_IN) - Inches(0.1)]
    textboxes = [s for s in slide.shapes if s.shape_type == MSO_SHAPE_TYPE.TEXT_BOX and s.text_frame.text.strip()]
    pairs = []
    for c in cards:
        inside = [t for t in textboxes if _contains(c, t)]
        if len(inside) == 1:
            pairs.append((c, inside[0]))
    if not pairs:
        return 0

    # 1. Scale sparse text up (cards at most 1.3x) so shrinking does not leave tiny text.
    for card, tb in pairs:
        pad = _in(tb.top - card.top)
        inner_h = _in(card.height) - 2 * pad
        need = estimate_text_height_in(tb.text_frame, _in(tb.width))
        fill = need / max(inner_h, 0.1)
        if 0.05 < fill < 0.6:
            scale = min(1.3, math.sqrt(0.7 / fill))
            if scale > 1.04:
                _scale_fonts(tb.text_frame, scale)
        elif fill > 1.0:
            scale = max(0.85, 1.0 / fill)
            _scale_fonts(tb.text_frame, scale)

    # 2. Row-equalised card heights.
    rows: Dict[int, List[Tuple[Any, Any]]] = {}
    for card, tb in pairs:
        rows.setdefault(round(_in(card.top) / 0.1), []).append((card, tb))
    for row in rows.values():
        needs = []
        for card, tb in row:
            pad = _in(tb.top - card.top)
            needs.append(estimate_text_height_in(tb.text_frame, _in(tb.width)) + 2 * pad)
        orig_h = max(_in(c.height) for c, _ in row)
        target = min(orig_h, max(max(needs) * 1.08, 1.6))
        for card, tb in row:
            pad = _in(tb.top - card.top)
            card.height = Inches(target)
            tb.height = Inches(target - 2 * pad)
    return len(pairs)


def balance_vertically(slide, max_shift_in: float = 1.3):
    """Center the content block in the free area below the header."""
    shapes = list(slide.shapes)
    if not shapes:
        return 0.0
    content = [
        s for s in shapes[1:]  # shapes[0] is the full-bleed background
        if _in(s.top) >= HEADER_BOTTOM_IN
    ]
    if not content:
        return 0.0
    bottom = max(_in(s.top + s.height) for s in content)
    free = CONTENT_FLOOR_IN - bottom
    if free <= 0.2:
        return 0.0
    shift = min(max_shift_in, free / 2)
    for s in content:
        s.top = s.top + Inches(shift)
    return shift


def normalize_slide(slide, tokens: Dict[str, Any], layout_type: str):
    """Entry point called by the PPTX builder after a slide is rendered."""
    card_style = tokens.get("card_style", {})
    radius_in = float(card_style.get("border_radius", 12)) / 96.0
    apply_card_radius(slide, radius_in)
    body_font = pick_font(tokens.get("typography", {}).get("body", {}).get("font"))
    apply_font_family(slide, body_font)
    if layout_type not in NO_FLOOR_LAYOUTS:
        enforce_min_font(slide)
    if layout_type in FIT_LAYOUTS:
        fit_cards(slide)
        fit_self_text_cards(slide)
        balance_vertically(slide)
    elif layout_type in BALANCE_ONLY_LAYOUTS:
        balance_vertically(slide)
