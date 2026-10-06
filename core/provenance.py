"""provenance.py - Where does each number on a slide come from? (v3.7)

A slide full of confident numbers with no origin is the most dangerous kind of "flesh": it reads as
evidence and cannot be checked. v3.7 makes provenance part of the blueprint.

Optional fields (all backward compatible):
  source   str | list[str]   where the figures come from ("Q3财报.xlsx 营收!B12", a URL, "用户口述 2026-10-06")
  status   one of STATUSES   how much to trust it
  A `source`/`status` on a slide covers every figure on it; on a nested item (e.g. one metric) it covers
  that item only and overrides the slide.

Statuses:
  verified      checked against the source
  estimate      has a basis but is not exact; shown as "估算"
  illustrative  invented to show a layout (demos, templates); shown as "示例数据"
  todo          placeholder waiting for a real number; always flagged

A figure is *unsourced* when nothing covers it. Unsourced and `todo` figures are "待核" (to verify).
"""

import re
from typing import Any, Dict, List, Optional, Tuple

STATUSES = ("verified", "estimate", "illustrative", "todo")

# A figure is a number that makes a claim: percent, multiple, money, duration, or a counted unit.
# Bare integers, years, quarters (Q3), priorities (P0) and structural counts ("3 个支柱") are not figures.
_UNITS = (
    r"%|％|倍|x|X|ms|μs|s|秒|分钟|小时|天|周|个月|万元|万|亿|元|人|名|笔|次|家|台|GB|TB|MB|QPS|TPS"
)
FIGURE_RE = re.compile(
    r"(?<![A-Za-z0-9_.])"
    r"(?:[<>≤≥~约]\s*)?"
    r"(?:"
    r"[¥￥$]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:万|亿|k|K|M|B))?"
    r"|\d[\d,]*(?:\.\d+)?\s?(?:" + _UNITS + r")(?![A-Za-z])"
    r"|\d+\s?个(?=人头|名额|编制|HC)"
    r"|\d+\+"
    r")"
)

# Keys whose text is never a data claim.
_SKIP_KEYS = {
    "layout_type", "narrative_arc", "mission", "transition", "speaker_notes", "notes", "motion_pace",
    "transition_effect", "source", "status", "highlight", "recommended", "chart_type", "version", "tag",
}


def as_list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return [str(v).strip() for v in value if str(v).strip()]


def normalize_status(value: Any) -> Optional[str]:
    v = str(value or "").strip().lower()
    return v if v in STATUSES else None


def find_figures(text: str) -> List[str]:
    return [re.sub(r"\s+", "", m.group(0)) for m in FIGURE_RE.finditer(text or "")]


def _walk(node: Any, sourced: bool, status: Optional[str], path: str, out: List[Dict[str, Any]], sources: List[str]):
    if isinstance(node, dict):
        own = as_list(node.get("source"))
        for s in own:
            if s not in sources:
                sources.append(s)
        if own:
            sourced = True
        st = normalize_status(node.get("status"))
        if st:
            status = st
        for k, v in node.items():
            if k in _SKIP_KEYS:
                continue
            _walk(v, sourced, status, f"{path}.{k}", out, sources)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                continue
            _walk(v, sourced, status, f"{path}[{i}]", out, sources)
    elif isinstance(node, str):
        for fig in find_figures(node):
            out.append({"text": fig, "sourced": sourced, "status": status, "path": path})


def scan_slide(slide: Dict[str, Any]) -> Dict[str, Any]:
    """Figures on one slide, who covers them, and what still needs checking."""
    figures: List[Dict[str, Any]] = []
    sources: List[str] = []
    _walk(slide, False, None, "", figures, sources)

    # Native chart data is a set of figures that never appear as text.
    if slide.get("series") and slide.get("layout_type") in ("data_chart", "chart"):
        covered = bool(as_list(slide.get("source")))
        figures.append({"text": "图表数据", "sourced": covered,
                        "status": normalize_status(slide.get("status")), "path": ".series"})

    def pick(pred):
        return [f for f in figures if pred(f)]

    unsourced = pick(lambda f: not f["sourced"] and f["status"] not in ("illustrative",))
    todo = pick(lambda f: f["status"] == "todo")
    estimate = pick(lambda f: f["status"] == "estimate")
    illustrative = pick(lambda f: f["status"] == "illustrative")
    # "To verify": nothing covers the figure, or it is explicitly a placeholder.
    to_verify = {f["path"] + "|" + f["text"]: f for f in unsourced + todo}
    return {
        "figures": figures,
        "sources": sources,
        "unsourced": unsourced,
        "todo": todo,
        "estimate": estimate,
        "illustrative": illustrative,
        "to_verify": list(to_verify.values()),
    }


def scan_blueprint(blueprint: Any) -> Dict[str, Any]:
    slides = blueprint.get("slides", []) if isinstance(blueprint, dict) else (blueprint or [])
    per_slide = [scan_slide(s) for s in slides]
    totals = {
        "figures": sum(len(s["figures"]) for s in per_slide),
        "unsourced": sum(len(s["unsourced"]) for s in per_slide),
        "todo": sum(len(s["todo"]) for s in per_slide),
        "estimate": sum(len(s["estimate"]) for s in per_slide),
        "illustrative": sum(len(s["illustrative"]) for s in per_slide),
        "to_verify": sum(len(s["to_verify"]) for s in per_slide),
    }
    return {"slides": per_slide, "totals": totals}


def provenance_labels(slide: Dict[str, Any]) -> Dict[str, Any]:
    """What a renderer should print on the slide face: footer text and the 待核 count."""
    scan = scan_slide(slide)
    statuses = {f["status"] for f in scan["figures"] if f["status"]}
    slide_status = normalize_status(slide.get("status"))
    if slide_status:
        statuses.add(slide_status)
    prefix = ""
    if "illustrative" in statuses:
        prefix = "示例数据 · "
    elif "estimate" in statuses:
        prefix = "估算 · "
    sources = scan["sources"]
    if sources:
        footer = f"{prefix}来源：{'；'.join(sources)}"
    elif prefix:
        footer = prefix.rstrip(" · ") + "，非真实业务数据" if "illustrative" in statuses else prefix.rstrip(" · ")
    else:
        footer = ""
    if len(footer) > 140:
        footer = footer[:137] + "…"
    return {"footer": footer, "to_verify": len(scan["to_verify"]), "scan": scan}


def notes_block(slide: Dict[str, Any]) -> List[str]:
    """Speaker-note lines listing sources and what still needs verification."""
    scan = scan_slide(slide)
    lines: List[str] = []
    if scan["sources"]:
        lines.append("【数据出处 / Sources】" + "；".join(scan["sources"]))
    if scan["illustrative"]:
        lines.append("【示例数据】本页数字为示例，不是真实业务数据。")
    if scan["estimate"]:
        lines.append("【估算】" + "、".join(dict.fromkeys(f["text"] for f in scan["estimate"])) + " 为估算值，宣讲时请说明依据。")
    if scan["to_verify"]:
        figs = "、".join(dict.fromkeys(f["text"] for f in scan["to_verify"]))
        lines.append(f"【待核 / To verify】{len(scan['to_verify'])} 项数字没有出处或仍是占位：{figs}")
    return lines


def attach_sources(blueprint: Dict[str, Any], facts: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Link figures in a blueprint to extracted facts (core/ingest.py) by value and record their sources.

    A page-level `source` covers *every* figure on the slide, so it is written only when every unsourced
    figure on that slide was matched. A partial match writes `source_candidates` instead and leaves the
    figures flagged, so provenance is never credited to a number that has none. A match also proves only
    that the number appears in the document, not that it is used for the same claim, so `status` is never
    set here: a human decides what is `verified`.
    """
    import copy

    by_value: Dict[str, List[Dict[str, Any]]] = {}
    for fact in facts:
        by_value.setdefault(re.sub(r"\s+", "", str(fact.get("value", ""))), []).append(fact)

    out = copy.deepcopy(blueprint)
    slides = out.get("slides", []) if isinstance(out, dict) else out
    linked: List[Dict[str, Any]] = []
    partial: List[Dict[str, Any]] = []
    unmatched: List[Dict[str, Any]] = []
    for idx, slide in enumerate(slides):
        scan = scan_slide(slide)
        pending = scan["unsourced"]
        if not pending:
            continue
        matched: Dict[str, Dict[str, Any]] = {}
        for fig in pending:
            hits = by_value.get(fig["text"])
            if hits:
                matched[fig["text"]] = hits[0]
            else:
                unmatched.append({"slide": idx + 1, "figure": fig["text"]})
        if not matched:
            continue
        entry = [{"figure": f, "source": m["source"]} for f, m in matched.items()]
        if len(matched) == len({f["text"] for f in pending}):
            existing = as_list(slide.get("source"))
            slide["source"] = existing + [m["source"] for m in matched.values() if m["source"] not in existing]
            linked.append({"slide": idx + 1, "matches": entry})
        else:
            slide["source_candidates"] = entry
            partial.append({"slide": idx + 1, "matches": entry})
    return out, {"linked": linked, "partial": partial, "unmatched": unmatched}
