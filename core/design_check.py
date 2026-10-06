"""design_check.py - Typography and contrast rules for design tokens (v3.8).

Tokens come from presets or from `undo` on a real template. Whatever their source, text must be readable:

  contrast   every text colour reaches 4.5:1 on the surface it is set on (3:1 for large text)
  sizes      title >= 28pt, subtitle >= 16pt, body >= 12pt, KPI number >= 40pt
  hierarchy  title is at least 1.5x the body size

`check_tokens` reports; `repair_tokens` fixes what can be fixed without changing a colour's hue.
"""

import copy
from typing import Any, Dict, List, Tuple

from core.contrast import EPS, LARGE_MIN, NORMAL_MIN, contrast_ratio, fix_color

MIN_SIZES = {"title": 28, "subtitle": 16, "body": 12, "kpi_number": 40}
MIN_HIERARCHY = 1.5

# (token path, text colour key, backgrounds it appears on, large text?)
_PAIRS = [
    ("typography.title.color", ("background",), True),
    ("typography.subtitle.color", ("background",), True),
    ("typography.body.color", ("background", "surface"), False),
    ("typography.kpi_number.color", ("surface",), True),
    ("palette.text_primary", ("background", "surface"), False),
    ("palette.text_secondary", ("background", "surface", "surface_subtle"), False),
]
# palette.primary is deliberately absent: it is a brand colour used mostly as a fill (badges, table headers).
# Where it is set as text, the layout pass nudges that one run (core/layout_fit.py: repair_contrast), so the
# brand colour itself is never changed.


def _get(tokens: Dict[str, Any], path: str):
    node = tokens
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def _set(tokens: Dict[str, Any], path: str, value: Any):
    parts = path.split(".")
    node = tokens
    for part in parts[:-1]:
        node = node[part]
    node[parts[-1]] = value


def check_tokens(tokens: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    palette = tokens.get("palette", {})
    for path, bg_keys, large in _PAIRS:
        fg = _get(tokens, path)
        if not fg:
            continue
        for key in bg_keys:
            bg = palette.get(key)
            if not bg:
                continue
            need = LARGE_MIN if large else NORMAL_MIN
            ratio = contrast_ratio(fg, bg)
            if ratio < need - EPS:
                findings.append({"code": "TOKEN_LOW_CONTRAST", "path": path, "on": key,
                                 "message": f"{path} {fg} on {key} {bg} is {ratio:.2f}:1, needs {need:g}:1"})
    typo = tokens.get("typography", {})
    for role, minimum in MIN_SIZES.items():
        size = (typo.get(role) or {}).get("size")
        if size is not None and size < minimum:
            findings.append({"code": "TOKEN_SIZE_TOO_SMALL", "path": f"typography.{role}.size",
                             "message": f"{role} is {size}pt, minimum {minimum}pt"})
    t, b = (typo.get("title") or {}).get("size"), (typo.get("body") or {}).get("size")
    if t and b and t < b * MIN_HIERARCHY:
        findings.append({"code": "TOKEN_WEAK_HIERARCHY", "path": "typography.title.size",
                         "message": f"title {t}pt is under {MIN_HIERARCHY}x the body size {b}pt"})
    return findings


def repair_tokens(tokens: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """Return (repaired copy, notes). Colours keep their hue; sizes are raised to the minimum."""
    out = copy.deepcopy(tokens)
    notes: List[str] = []
    palette = out.get("palette", {})
    for path, bg_keys, large in _PAIRS:
        for _ in range(2):  # a colour fixed for one background can break another
            changed = False
            for key in bg_keys:
                fg, bg = _get(out, path), palette.get(key)
                if not fg or not bg:
                    continue
                need = LARGE_MIN if large else NORMAL_MIN
                if contrast_ratio(fg, bg) < need - EPS:
                    fixed = "#" + fix_color(fg, bg, need)
                    notes.append(f"{path}: {fg} -> {fixed} (on {key}, {need:g}:1)")
                    _set(out, path, fixed)
                    changed = True
            if not changed:
                break
    typo = out.get("typography", {})
    for role, minimum in MIN_SIZES.items():
        spec = typo.get(role)
        if spec and spec.get("size") is not None and spec["size"] < minimum:
            notes.append(f"typography.{role}.size: {spec['size']} -> {minimum}")
            spec["size"] = minimum
    t, b = (typo.get("title") or {}).get("size"), (typo.get("body") or {}).get("size")
    if t and b and t < b * MIN_HIERARCHY:
        new_t = int(round(b * MIN_HIERARCHY))
        notes.append(f"typography.title.size: {t} -> {new_t} (hierarchy)")
        typo["title"]["size"] = new_t
    return out, notes
