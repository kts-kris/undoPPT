"""motion.py - Three narrative animations for native PPTX (v3.8).

Motion is only worth having when it serves the telling. v3.8 keeps three, each tied to a reason:

  reveal    one idea per click, in reading order            (a list, a roadmap, a stack)
  contrast  the "before" first, then the answer on a click  (problem vs solution, current vs target)
  build     data arrives piece by piece                     (KPIs, a chart and then its takeaway)

Off by default. A deck turns it on with `presentation_config.motion: "narrative"` (or `build --motion
narrative`); a slide opts in or out with `motion: {"type": "reveal" | "contrast" | "build" | "none"}`.
`motion_pace: "staged"` (v3.3) is still accepted as an alias for "narrative".

The timing tree follows what PowerPoint itself writes: each click is an outer `par` with
`delay="indefinite"`, the first effect is a `clickEffect` and the rest of its group are `withEffect`.
(The v3.3/v3.4 tree used `delay="0"` and no preset ids; PowerPoint recognised none of it.)
"""

from typing import Any, Dict, List, Optional, Tuple

from pptx.oxml import parse_xml
from pptx.util import Inches

MOTION_TYPES = ("reveal", "contrast", "build")

# What a slide gets when the deck says "narrative" and the slide does not choose.
AUTO_BY_LAYOUT = {
    "bento_cards": "contrast",
    "content_columns": "reveal",
    "matrix_2x2": "contrast",
    "cross_mapping": "contrast",
    "metric_spotlight": "build",
    "kpi_dashboard": "build",
    "data_chart": "build",
    "chart": "build",
    "standard_table": "build",
}

ARC_DURATION_MS = {
    "conflict": 250, "breakthrough": 400, "evidence": 600,
    "progression": 400, "hook": 300, "call_to_action": 350,
}

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
HEADER_BOTTOM = Inches(1.8)
STATIC_PREFIX = "undoppt-"


def resolve_motion(slide_data: Dict[str, Any], deck_mode: Optional[str]) -> Optional[str]:
    """Which narrative animation (if any) this slide gets."""
    layout = slide_data.get("layout_type", "")
    if layout == "cover" or deck_mode == "off":
        return None
    m = slide_data.get("motion")
    if isinstance(m, str):
        m = {"type": m}
    if isinstance(m, dict):
        t = m.get("type")
        if t == "none":
            return None
        if t in MOTION_TYPES:
            return t
        if m.get("staged_reveal"):
            return "reveal"
    pace = slide_data.get("motion_pace")
    if pace == "instant":
        return None
    if pace == "staged" or deck_mode in ("narrative", "staged"):
        return AUTO_BY_LAYOUT.get(layout, "reveal")
    return None


# ----------------------------------------------------------------------------------------------
# Grouping
# ----------------------------------------------------------------------------------------------

def _is_background(shape) -> bool:
    return shape.left == 0 and shape.top == 0 and shape.width >= Inches(13)


def _kind(shape) -> str:
    if getattr(shape, "has_chart", False) and shape.has_chart:
        return "chart"
    if getattr(shape, "has_table", False) and shape.has_table:
        return "table"
    if shape.shape_type == 17:  # TEXT_BOX
        return "text"
    return "shape"


def animatable(slide) -> List[Any]:
    """Content shapes that may animate: not the background, the header, the footer/badge or scaffolding."""
    out = []
    for s in slide.shapes:
        if _is_background(s) or s.top < HEADER_BOTTOM or s.name.startswith(STATIC_PREFIX):
            continue
        if s.width > Inches(9) and s.height < Inches(0.3):
            continue  # connector lines and rules stay put
        out.append(s)
    return out


def _cx(shape) -> float:
    return shape.left + shape.width / 2


def _cluster(shapes: List[Any], axis: str, tol: float) -> List[List[Any]]:
    """Group shapes whose `axis` is within tol inches of the group's first shape.

    axis "left" clusters by horizontal *centre* (a roadmap node sits above its card, centred, not edge-aligned);
    axis "top" clusters by top edge.
    """
    key = (lambda x: _cx(x)) if axis == "left" else (lambda x: x.top)
    clusters: List[List[Any]] = []
    for s in sorted(shapes, key=lambda x: (key(x), x.top if axis == "left" else x.left)):
        for c in clusters:
            if abs(key(c[0]) - key(s)) < Inches(tol):
                c.append(s)
                break
        else:
            clusters.append([s])
    return clusters


def _is_small(shape) -> bool:
    return shape.width < Inches(0.7) and shape.height < Inches(0.7)


def _attach_small(clusters: List[List[Any]], small: List[Any]) -> List[List[Any]]:
    """Arrows, badges and bullets join the step they belong to: the one containing them, else the next one to the right."""
    if not clusters:
        return [[s] for s in small]

    def bbox(c):
        return (min(x.left for x in c), min(x.top for x in c),
                max(x.left + x.width for x in c), max(x.top + x.height for x in c))

    for s in small:
        cx, cy = _cx(s), s.top + s.height / 2
        host = next((c for c in clusters if bbox(c)[0] <= cx <= bbox(c)[2] and bbox(c)[1] <= cy <= bbox(c)[3]), None)
        if host is None:
            ahead = [c for c in clusters if bbox(c)[0] >= cx]
            pool = ahead or clusters
            host = min(pool, key=lambda c: abs(bbox(c)[0] - cx))
        host.append(s)
    return clusters


def _reading_order(shapes: List[Any]) -> List[List[Any]]:
    """Columns left to right; full-width blocks (a recommendation bar, a sign-off box) form their own step."""
    small = [s for s in shapes if _is_small(s)]
    big = [s for s in shapes if not _is_small(s)]
    wide = [s for s in big if s.width > Inches(8)]
    narrow = [s for s in big if s.width <= Inches(8)]
    clusters = _cluster(narrow, "left", 0.6)
    clusters += [[w] for w in sorted(wide, key=lambda x: x.top)]
    clusters = _attach_small(clusters, small)
    return sorted(clusters, key=lambda c: (round(min(s.top for s in c) / Inches(0.9)), min(_cx(s) for s in c)))


def _highlight_flags(slide_data: Dict[str, Any]) -> List[bool]:
    items = (slide_data.get("cards") or slide_data.get("columns") or slide_data.get("levels") or [])
    return [bool(isinstance(i, dict) and i.get("highlight")) for i in items]


def _group(shapes: List[Any], effect: str = "fade") -> Dict[str, Any]:
    return {"shapes": shapes, "effect": effect}


def plan_groups(slide, slide_data: Dict[str, Any], mtype: str) -> List[Dict[str, Any]]:
    layout = slide_data.get("layout_type", "")
    shapes = animatable(slide)
    if not shapes:
        return []

    if layout in ("data_chart", "chart"):
        charts = [s for s in shapes if _kind(s) == "chart"]
        rest = [s for s in shapes if _kind(s) != "chart"]
        return [g for g in (_group(charts, "wipe_left"), _group(rest, "fade")) if g["shapes"]]

    if layout in ("standard_table", "table"):
        return [_group(shapes, "fade")]

    if layout in ("architecture_stack", "cross_mapping") and mtype != "contrast":
        rows = _cluster(shapes, "top", 0.8)
        if layout == "architecture_stack":
            rows = list(reversed(rows))  # foundations first: the stack assembles from the bottom
        return [_group(r) for r in rows]

    if mtype == "contrast":
        if layout == "cross_mapping":
            before = [s for s in shapes if s.left < Inches(7.0)]
            after = [s for s in shapes if s.left >= Inches(7.0)]
            return [g for g in (_group(before), _group(after)) if g["shapes"]]
        if layout == "matrix_2x2":
            quads = _reading_order([s for s in shapes if s.width <= Inches(8)])
            flags = _highlight_flags({"cards": slide_data.get("quadrants", [])}) if isinstance(slide_data.get("quadrants"), list) else []
            if len(quads) >= 4:
                hi_index = flags.index(True) if True in flags else 3
                body = quads[:4]
                hi = body[hi_index] if hi_index < len(body) else body[-1]
                others = [s for c in body if c is not hi for s in c]
                extra = [_group(c) for c in quads[4:]]
                return [_group(others), _group(hi)] + extra
        else:
            cols = _reading_order(shapes)
            flags = _highlight_flags(slide_data)
            if flags and len(cols) == len(flags) and any(flags) and not all(flags):
                before = [s for c, f in zip(cols, flags) if not f for s in c]
                after = [s for c, f in zip(cols, flags) if f for s in c]
                return [_group(before), _group(after)]
        mtype = "reveal"  # nothing to contrast: fall back

    if mtype == "build":
        return [_group(c, "wipe_left") for c in _reading_order(shapes)]

    return [_group(c) for c in _reading_order(shapes)]


# ----------------------------------------------------------------------------------------------
# OOXML
# ----------------------------------------------------------------------------------------------

_EFFECTS = {
    # name: (presetID, presetSubtype, filter)
    "fade": (10, 0, "fade"),
    "wipe_left": (22, 8, "wipe(left)"),
}


def _effect_xml(cid: int, spid: int, effect: str, node_type: str, dur: int, grp_id: int = 0) -> Tuple[str, int]:
    preset, subtype, flt = _EFFECTS[effect]
    xml = (
        f'<p:par><p:cTn id="{cid}" presetID="{preset}" presetClass="entr" presetSubtype="{subtype}" fill="hold" '
        f'grpId="{grp_id}" nodeType="{node_type}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
        f'<p:set><p:cBhvr><p:cTn id="{cid + 1}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
        f'<p:animEffect transition="in" filter="{flt}"><p:cBhvr><p:cTn id="{cid + 2}" dur="{dur}"/>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'
        f'</p:childTnLst></p:cTn></p:par>'
    )
    return xml, cid + 3


def build_timing_xml(groups: List[Dict[str, Any]], dur_ms: int) -> str:
    cid = 3
    steps = []
    kinds: Dict[int, str] = {}
    for g in groups:
        outer, inner = cid, cid + 1
        cid += 2
        effects = []
        for i, shape in enumerate(g["shapes"]):
            kinds[shape.shape_id] = _kind(shape)
            dur = dur_ms + (300 if g["effect"] == "wipe_left" and _kind(shape) == "chart" else 0)
            xml, cid = _effect_xml(cid, shape.shape_id, g["effect"], "clickEffect" if i == 0 else "withEffect", dur)
            effects.append(xml)
        steps.append(
            f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{inner}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'{"".join(effects)}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
        )

    bld = []
    for spid, kind in kinds.items():
        if kind == "shape":
            bld.append(f'<p:bldP spid="{spid}" grpId="0" animBg="1"/>')
        elif kind == "text":
            bld.append(f'<p:bldP spid="{spid}" grpId="0"/>')
        elif kind == "chart":
            bld.append(f'<p:bldGraphic spid="{spid}" grpId="0"><p:bldAsOne/></p:bldGraphic>')
    bld_xml = f'<p:bldLst>{"".join(bld)}</p:bldLst>' if bld else ""

    return (
        f'<p:timing xmlns:p="{P_NS}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
        f'<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">'
        f'<p:childTnLst>{"".join(steps)}</p:childTnLst></p:cTn>'
        f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
        f'<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
        f'</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>{bld_xml}</p:timing>'
    )


def apply_motion(slide, slide_data: Dict[str, Any], deck_mode: Optional[str]) -> Optional[Dict[str, Any]]:
    """Add the slide's narrative animation. Returns {"type", "steps", "shapes"} or None when there is none."""
    for child in list(slide._element):
        if child.tag.endswith("}timing"):
            slide._element.remove(child)

    mtype = resolve_motion(slide_data, deck_mode)
    if not mtype:
        return None
    groups = plan_groups(slide, slide_data, mtype)
    if len(groups) < 2:
        return None  # a single step animates nothing worth clicking

    dur = ARC_DURATION_MS.get(slide_data.get("narrative_arc", "progression"), 400)
    timing = parse_xml(build_timing_xml(groups, dur))
    insert_idx = len(slide._element)
    for i, child in enumerate(slide._element):
        if child.tag.endswith("}extLst"):
            insert_idx = i
            break
    slide._element.insert(insert_idx, timing)
    return {"type": mtype, "steps": len(groups), "shapes": sum(len(g["shapes"]) for g in groups)}


# ----------------------------------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------------------------------

def _ns(tag: str) -> str:
    return f"{{{P_NS}}}{tag}"


def timing_summary(slide) -> Dict[str, Any]:
    """Read a slide's timing tree: click steps and the shape ids animated."""
    timing = next((c for c in slide._element if c.tag == _ns("timing")), None)
    if timing is None:
        return {"present": False, "steps": 0, "spids": []}
    steps = 0
    for ctn in timing.iter(_ns("cTn")):
        if ctn.get("nodeType") == "clickEffect":
            steps += 1
    spids = []
    for tgt in timing.iter(_ns("spTgt")):
        sid = int(tgt.get("spid"))
        if sid not in spids:
            spids.append(sid)
    return {"present": True, "steps": steps, "spids": spids}


def validate_timing(slide) -> List[str]:
    """Problems that make PowerPoint ignore or repair an animation tree (empty list means well-formed)."""
    problems: List[str] = []
    timing = next((c for c in slide._element if c.tag == _ns("timing")), None)
    if timing is None:
        return problems
    shape_ids = {s.shape_id for s in slide.shapes}
    ids = [int(c.get("id")) for c in timing.iter(_ns("cTn"))]
    if len(ids) != len(set(ids)):
        problems.append("duplicate cTn ids")
    main = next((c for c in timing.iter(_ns("cTn")) if c.get("nodeType") == "mainSeq"), None)
    if main is None:
        return problems + ["no mainSeq"]
    child_list = next((c for c in main if c.tag == _ns("childTnLst")), None)
    for outer in (child_list if child_list is not None else []):
        cond = next(outer.iter(_ns("cond")), None)
        if cond is None or cond.get("delay") != "indefinite":
            problems.append("a click step does not wait for a click (delay must be 'indefinite')")
    first_in_step = set()
    for outer in (child_list if child_list is not None else []):
        effs = [c for c in outer.iter(_ns("cTn")) if c.get("nodeType") in ("clickEffect", "withEffect")]
        if not effs or effs[0].get("nodeType") != "clickEffect":
            problems.append("a click step must start with a clickEffect")
        first_in_step.update(e.get("nodeType") for e in effs[1:])
    if first_in_step - {"withEffect"}:
        problems.append("only the first effect of a step may be a clickEffect")
    for tgt in timing.iter(_ns("spTgt")):
        if int(tgt.get("spid")) not in shape_ids:
            problems.append(f"effect targets missing shape {tgt.get('spid')}")
    for bld in timing.iter(_ns("bldP")):
        if int(bld.get("spid")) not in shape_ids:
            problems.append(f"bldLst names missing shape {bld.get('spid')}")
    return problems
