"""layout_lint.py - Static geometry lint for built PPTX files (v3.5).

Needs no renderer. It measures text with the same heuristic as core/layout_fit.py
and reports layout defects that a viewer would see:

  OUT_OF_BOUNDS      a shape extends past the slide edge
  TITLE_WRAPS        the header title needs more than one line
  TEXT_OVERFLOW      text is estimated taller than the card/box that holds it
  TEXT_CROSSES_SHAPE a text block straddles the edge of another shape (e.g. a wrapped
                     title running into the cards below)
  TEXT_OVERLAP       two text blocks overlap
  LOW_CONTRAST       text whose colour is too close to the fill behind it (WCAG: 4.5:1, 3:1 for large text)
"""

from typing import Any, Dict, List

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu

from core.contrast import EPS, contrast_ratio, required_ratio, text_runs_with_backdrop
from core.layout_fit import _in, estimate_text_height_in

TOL_IN = 0.06


def _effective_rect(shape):
    """(left, top, right, bottom) in inches; text boxes use their estimated text height."""
    l, t = _in(shape.left), _in(shape.top)
    w, h = _in(shape.width), _in(shape.height)
    if shape.shape_type == MSO_SHAPE_TYPE.TEXT_BOX and shape.text_frame.text.strip():
        h = min(max(estimate_text_height_in(shape.text_frame, w), 0.1), max(h, 0.1) + 4)
    return l, t, l + w, t + h


def _intersect(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return (w, h) if w > 0 and h > 0 else (0.0, 0.0)


def _contains(outer, inner, tol=TOL_IN) -> bool:
    return (
        outer[0] - tol <= inner[0]
        and outer[1] - tol <= inner[1]
        and outer[2] + tol >= inner[2]
        and outer[3] + tol >= inner[3]
    )


def lint_slide(slide, index: int, sw_in: float, sh_in: float) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    shapes = list(slide.shapes)

    def add(code, msg):
        findings.append({"slide": index, "code": code, "message": msg})

    for s in shapes[1:]:
        r = (_in(s.left), _in(s.top), _in(s.left + s.width), _in(s.top + s.height))
        if r[0] < -TOL_IN or r[1] < -TOL_IN or r[2] > sw_in + TOL_IN or r[3] > sh_in + TOL_IN:
            add("OUT_OF_BOUNDS", f"shape '{s.name}' extends past the slide ({r[0]:.2f},{r[1]:.2f})-({r[2]:.2f},{r[3]:.2f})in")

    text_boxes = [
        s for s in shapes if s.shape_type == MSO_SHAPE_TYPE.TEXT_BOX and s.text_frame.text.strip()
    ]

    # Header title: first text box that is not inside the cover card.
    for tb in text_boxes:
        first = tb.text_frame.paragraphs[0]
        size = first.runs[0].font.size.pt if first.runs and first.runs[0].font.size else None
        if size and size >= 20 and 0.9 < _in(tb.top) < 1.9:
            one_line = estimate_text_height_in(
                _single_paragraph_frame(first), _in(tb.width)
            ) <= size * 1.25 / 72 + 0.12
            if not one_line:
                add("TITLE_WRAPS", f"title '{first.text[:24]}...' wraps to more than one line at {size:.0f}pt")
            break

    # Containment-based checks.
    cards = [
        s for s in shapes[1:]
        if s.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE
        and not (s.has_text_frame and s.text_frame.text.strip())
        and (_in(s.width) < sw_in - 0.2 or _in(s.height) < sh_in - 0.2)
    ]
    for tb in text_boxes:
        er = _effective_rect(tb)
        declared = (_in(tb.left), _in(tb.top), _in(tb.left + tb.width), _in(tb.top + tb.height))
        holder = next((c for c in cards if _contains((_in(c.left), _in(c.top), _in(c.left + c.width), _in(c.top + c.height)), declared)), None)
        if holder is not None:
            hb = _in(holder.top + holder.height)
            if er[3] > hb + TOL_IN:
                add("TEXT_OVERFLOW", f"text '{tb.text_frame.text[:20]}...' needs {er[3] - er[1]:.2f}in but its card ends {hb - er[1]:.2f}in below the text start")
            continue
        for c in cards:
            cr = (_in(c.left), _in(c.top), _in(c.left + c.width), _in(c.top + c.height))
            w, h = _intersect(er, cr)
            if w > 0.3 and h > 0.08 and not _contains(cr, er):
                add("TEXT_CROSSES_SHAPE", f"text '{tb.text_frame.text[:20]}...' runs into a shape starting at y={cr[1]:.2f}in")
                break

    # Decorative glyphs (e.g. the oversized quotation mark on quote slides) are meant to sit behind text.
    prose = [t for t in text_boxes if len(t.text_frame.text.strip()) > 2]
    for i in range(len(prose)):
        for j in range(i + 1, len(prose)):
            a, b = _effective_rect(prose[i]), _effective_rect(prose[j])
            w, h = _intersect(a, b)
            if w > 0.3 and h > 0.1:
                add("TEXT_OVERLAP", f"'{prose[i].text_frame.text[:16]}...' overlaps '{prose[j].text_frame.text[:16]}...'")
    return findings


# ------------------------------------------------------------------------------------------------
# Contrast (v3.8)
# ------------------------------------------------------------------------------------------------

def lint_contrast(slide, index: int) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    seen = set()
    for run, fg, bg, size, bold in text_runs_with_backdrop(slide):
        need = required_ratio(size, bold)
        ratio = contrast_ratio(fg, bg)
        key = (fg, bg, need)
        if ratio < need - EPS and key not in seen:
            seen.add(key)
            findings.append({
                "slide": index, "code": "LOW_CONTRAST",
                "message": f"'{run.text.strip()[:18]}' is #{fg} on #{bg}: contrast {ratio:.2f}:1, needs {need:g}:1 ({size:g}pt)",
            })
    return findings


class _OneParagraph:
    """Adapter exposing a single paragraph through the text-frame interface used by the estimator."""

    def __init__(self, p, src_tf):
        self.paragraphs = [p]
        self.margin_left = src_tf.margin_left
        self.margin_right = src_tf.margin_right
        self.margin_top = src_tf.margin_top
        self.margin_bottom = src_tf.margin_bottom


def _single_paragraph_frame(p):
    return _OneParagraph(p, p._parent)


def lint_pptx(path: str) -> Dict[str, Any]:
    prs = Presentation(path)
    sw, sh = _in(prs.slide_width), _in(prs.slide_height)
    findings: List[Dict[str, Any]] = []
    for i, slide in enumerate(prs.slides, 1):
        findings.extend(lint_slide(slide, i, sw, sh))
        findings.extend(lint_contrast(slide, i))
    return {"slides": len(prs.slides), "findings": findings, "ok": not findings}
