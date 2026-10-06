"""blueprint_compat.py - Documented blueprint schema -> renderer schema (v3.6).

The Blueprint Specification and the cognitive planner describe several layouts with one set
of field names; the PPTX and HTML renderers were written against another. Until v3.5 the gap
was silent: a `cross_mapping` slide lost 90% of its text, `content_columns` lost every bullet.

`normalize_slide` flattens the documented fields into the renderer's richer cards. It only
fills a renderer field when that field is absent, so slides already written in the renderer
schema are untouched. Both builders call it, so PPTX and HTML stay in step.
"""

import copy
from typing import Any, Dict, List


def _first(*values):
    for v in values:
        if v:
            return v
    return ""


def _cross_mapping(slide: Dict[str, Any]):
    rows = slide.get("mapping_rows") or slide.get("rows") or []
    out = []
    for r in rows:
        if not isinstance(r, dict):
            out.append(r)
            continue
        r = dict(r)
        if "layer" in r and "tier" not in r:
            r["tier"] = r["layer"]
        if "current" in r and not (r.get("source_role") or r.get("source_title")):
            r["source_role"] = "现状 / 痛点"
            r.setdefault("source_desc", r["current"])
        if "target" in r and not (r.get("target_role") or r.get("target_title")):
            r["target_role"] = "目标 / 解法"
            desc = r["target"]
            if r.get("action"):
                desc = f"{desc}\n牵引抓手：{r['action']}"
            r.setdefault("target_desc", desc)
        out.append(r)
    slide["mapping_rows"] = out


def _horizons(slide: Dict[str, Any]):
    out = []
    for h in slide.get("horizons", []):
        if not isinstance(h, dict):
            out.append(h)
            continue
        h = dict(h)
        if "horizon" in h and "id" not in h:
            h["id"] = h["horizon"]
        if "name" in h and "title" not in h:
            h["title"] = h["name"]
        if "kpi" in h and "metric" not in h:
            h["metric"] = h["kpi"]
        if not (h.get("focus") or h.get("items")):
            h["items"] = [x for x in (h.get("desc"),) if x]
        elif h.get("desc") and isinstance(h.get("focus"), str):
            h["items"] = [h["desc"], h["focus"]]
            h.pop("focus")
        elif h.get("desc"):
            h.setdefault("items", [h["desc"]])
        out.append(h)
    slide["horizons"] = out


def _ladder(slide: Dict[str, Any]):
    out = []
    for lv in slide.get("levels", []):
        if not isinstance(lv, dict):
            out.append(lv)
            continue
        lv = dict(lv)
        if "step" in lv and "level" not in lv:
            lv["level"] = lv["step"]
        if "focus" in lv and "mechanism" not in lv:
            lv["mechanism"] = lv["focus"]
        if lv.get("target") and "阶段目标" not in str(lv.get("desc", "")):
            lv["desc"] = _first(lv.get("desc"), "") + (f"\n阶段目标：{lv['target']}" if lv.get("desc") else f"阶段目标：{lv['target']}")
        out.append(lv)
    slide["levels"] = out


def _matrix(slide: Dict[str, Any]):
    out = []
    for q in slide.get("quadrants", []):
        if not isinstance(q, dict):
            out.append(q)
            continue
        q = dict(q)
        # Renderers print `strategy or desc` as the description and `items` as bullets: keep both documented fields.
        if q.get("desc") and "strategy" not in q:
            q["strategy"] = q["desc"]
        if q.get("tag") and not (q.get("items") or q.get("bullets")):
            q["items"] = [f"策略：{q['tag']}"]
        elif q.get("tag") and "strategy" not in q:
            q["strategy"] = q["tag"]
        out.append(q)
    slide["quadrants"] = out
    axes = slide.get("axes")
    if isinstance(axes, dict):
        if axes.get("x") and "x_axis" not in slide:
            slide["x_axis"] = {"title": axes["x"]}
        if axes.get("y") and "y_axis" not in slide:
            slide["y_axis"] = {"title": axes["y"]}


def _columns(slide: Dict[str, Any]):
    out = []
    for c in slide.get("columns", []):
        if not isinstance(c, dict):
            out.append(c)
            continue
        c = dict(c)
        if "points" in c and "bullets" not in c:
            c["bullets"] = c["points"]
        if "tag" in c and "badge" not in c:
            c["badge"] = c["tag"]
        out.append(c)
    slide["columns"] = out


_NORMALIZERS = {
    "cross_mapping": _cross_mapping,
    "mapping": _cross_mapping,
    "horizons_curve": _horizons,
    "horizons": _horizons,
    "three_horizons": _horizons,
    "maturity_ladder": _ladder,
    "ladder": _ladder,
    "matrix_2x2": _matrix,
    "matrix": _matrix,
    "content_columns": _columns,
    "columns": _columns,
    "rich_content": _columns,
}


def normalize_slide(slide: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of `slide` with documented fields mapped to the renderer's field names."""
    fn = _NORMALIZERS.get(slide.get("layout_type", ""))
    if fn is None:
        return slide
    out = copy.deepcopy(slide)
    fn(out)
    return out
