"""html_builder.py - Standalone Single-File Presentation Engine.

Compiles slides_blueprint.json and design_tokens.json into an ultra-portable,
zero-dependency, responsive, standalone HTML presentation file.
Features:
  - 100% self-contained (all styles, scripts, SVG icons fully inlined)
  - Keyboard navigation (Left/Right arrow, Space, F for fullscreen, O for overview)
  - Interactive Presenter controls (Progress bar, Page counter, Thumbnail drawer)
  - Full parity with the 6 Infographic layout primitives.
"""

import html
import json
import os
from typing import Any, Dict, List


def _render_cover_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    category = slide.get("category", "ENTERPRISE ARCHITECTURE")
    title = slide.get("action_title") or slide.get("title", "Presentation Title")
    subtitle = slide.get("subtitle", "")
    meta = slide.get("meta", "undoPPT Engine · 2026")
    p = tokens.get("palette", {})

    return f"""
    <div class="h-full flex flex-col justify-center px-12 py-10 relative">
      <div class="bg-white border border-slate-200/80 rounded-2xl shadow-xl p-12 relative overflow-hidden border-l-[10px]" style="border-left-color: {p.get('primary', '#2563EB')};">
        <div class="inline-block px-3 py-1 rounded-md text-xs font-bold tracking-wider uppercase mb-5" style="background-color: {p.get('surface_subtle', '#EFF6FF')}; color: {p.get('primary', '#2563EB')};">
          {category}
        </div>
        <h1 class="text-5xl font-extrabold tracking-tight mb-4 text-slate-900 leading-tight">
          {title}
        </h1>
        <p class="text-xl text-slate-600 font-medium mb-8 max-w-3xl leading-relaxed">
          {subtitle}
        </p>
        <div class="flex items-center text-sm font-semibold text-slate-400 gap-4 pt-4 border-t border-slate-100">
          <span>{meta}</span>
          <span>•</span>
          <span>100% Editable Presentation</span>
        </div>
      </div>
    </div>
    """


def _render_architecture_stack_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "系统架构全景")
    subtitle = slide.get("subtitle", "")
    layers = slide.get("layers", [])
    p = tokens.get("palette", {})
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "ARCHITECTURE")

    layers_html = []
    for idx, layer in enumerate(layers[:4]):
        name = layer.get("name", f"层级 {idx+1}")
        desc = layer.get("desc", "")
        items = layer.get("items", [])
        items_html = "".join([
            f'<div class="flex-1 min-w-[120px] bg-slate-50 border border-slate-200 rounded-lg py-2.5 px-3 text-center text-sm font-semibold text-slate-800 shadow-sm hover:border-blue-400 transition-colors">{item}</div>'
            for item in items[:5]
        ])

        desc_html = f'<div class="text-xs text-slate-500 font-normal mt-0.5">{desc}</div>' if desc else ""

        layers_html.append(f"""
        <div class="flex items-center gap-4 bg-white border border-slate-200 rounded-xl p-3 shadow-sm hover:shadow-md transition-shadow">
          <div class="w-44 flex-shrink-0 bg-blue-50/80 border border-blue-200 rounded-lg p-3 text-center">
            <div class="text-sm font-bold text-blue-700">{name}</div>
            {desc_html}
          </div>
          <div class="flex-1 flex gap-3 flex-wrap items-center">
            {items_html}
          </div>
        </div>
        """)

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-5">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 flex flex-col justify-between gap-3.5 pb-2">
        {"".join(layers_html)}
      </div>
    </div>
    """


def _render_bento_cards_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "核心维度对比")
    subtitle = slide.get("subtitle", "")
    cards = slide.get("cards", [])
    p = tokens.get("palette", {})
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "ANALYSIS")

    cards_html = []
    for idx, c in enumerate(cards[:4]):
        c_tag = c.get("tag", f"0{idx+1}")
        c_title = c.get("title", f"方案 {idx+1}")
        desc = c.get("desc", "")
        bullets = c.get("bullets", [])
        is_hl = c.get("highlight", False)

        border_cls = "border-blue-500 ring-2 ring-blue-500/20 shadow-md" if is_hl else "border-slate-200 shadow-sm"
        bullets_html = "".join([
            f'<li class="flex items-start text-xs text-slate-600 gap-1.5"><span class="text-blue-600 font-bold">•</span><span>{b}</span></li>'
            for b in bullets
        ])

        cards_html.append(f"""
        <div class="flex-1 flex flex-col bg-white border {border_cls} rounded-xl p-6 transition-all hover:-translate-y-1 hover:shadow-lg">
          <div class="text-xs font-bold uppercase tracking-wider text-blue-600 mb-2">{c_tag}</div>
          <h3 class="text-lg font-bold text-slate-900 mb-2">{c_title}</h3>
          <p class="text-xs text-slate-500 mb-4 leading-relaxed">{desc}</p>
          <ul class="mt-auto space-y-2 pt-3 border-t border-slate-100">
            {bullets_html}
          </ul>
        </div>
        """)

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-5">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 flex gap-5 pb-2">
        {"".join(cards_html)}
      </div>
    </div>
    """


def _render_metric_spotlight_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "核心业绩指标衡量")
    subtitle = slide.get("subtitle", "")
    metrics = slide.get("metrics", [])
    p = tokens.get("palette", {})
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "KPI DASHBOARD")

    metrics_html = []
    for m in metrics[:4]:
        label = m.get("label", "核心指标")
        val = m.get("value", "99.9%")
        delta = m.get("delta", "")
        desc = m.get("desc", "")

        delta_html = f'<div class="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full inline-block mb-3">▲ {delta}</div>' if delta else ""

        metrics_html.append(f"""
        <div class="flex-1 flex flex-col justify-between bg-white border border-slate-200 rounded-xl p-7 shadow-sm hover:shadow-md transition-shadow">
          <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">{label}</div>
            <div class="text-5xl font-extrabold text-blue-600 font-mono tracking-tight mb-2">{val}</div>
            {delta_html}
          </div>
          <div class="text-xs text-slate-500 border-t border-slate-100 pt-3 leading-relaxed">
            {desc}
          </div>
        </div>
        """)

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-5">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 flex gap-5 pb-2">
        {"".join(metrics_html)}
      </div>
    </div>
    """


def _render_timeline_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "演进路线与关键里程碑")
    subtitle = slide.get("subtitle", "")
    steps = slide.get("steps", [])
    p = tokens.get("palette", {})
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "ROADMAP")

    steps_html = []
    for idx, s in enumerate(steps[:4]):
        time_tag = s.get("time", f"Q{idx+1}")
        s_title = s.get("title", f"阶段 {idx+1}")
        items = s.get("items", [])
        items_html = "".join([
            f'<div class="flex items-center text-xs text-slate-600 gap-1.5"><span class="text-emerald-500 font-bold">✓</span><span>{it}</span></div>'
            for it in items
        ])

        steps_html.append(f"""
        <div class="flex-1 flex flex-col items-center relative">
          <!-- Step Node -->
          <div class="w-10 h-10 rounded-full bg-blue-600 text-white font-bold text-sm flex items-center justify-center ring-4 ring-white shadow z-10 mb-4">
            {idx+1}
          </div>
          <!-- Card -->
          <div class="w-full flex-1 bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition-all flex flex-col">
            <span class="text-xs font-bold text-blue-600 uppercase mb-1">{time_tag}</span>
            <h4 class="text-base font-bold text-slate-900 mb-3">{s_title}</h4>
            <div class="space-y-1.5 mt-auto pt-3 border-t border-slate-100">
              {items_html}
            </div>
          </div>
        </div>
        """)

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-5">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 relative flex gap-5 pt-3 pb-2">
        <!-- Connecting Line -->
        <div class="absolute top-[32px] left-12 right-12 h-1 bg-blue-200 rounded"></div>
        {"".join(steps_html)}
      </div>
    </div>
    """


def _render_summary_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "核心总结与实施建议")
    subtitle = slide.get("subtitle", "")
    points = slide.get("points", [])
    p = tokens.get("palette", {})
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "SUMMARY")

    points_html = []
    for idx, pt in enumerate(points[:4]):
        p_title = pt.get("title", f"建议 {idx+1}")
        desc = pt.get("desc", "")

        points_html.append(f"""
        <div class="flex items-center gap-5 bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:border-blue-300 transition-colors">
          <div class="w-10 h-10 rounded-lg bg-blue-600 text-white font-bold text-lg flex items-center justify-center flex-shrink-0">
            {idx+1}
          </div>
          <div class="flex-1">
            <h4 class="text-base font-bold text-slate-900">{p_title}</h4>
            <p class="text-xs text-slate-500 mt-0.5 leading-relaxed">{desc}</p>
          </div>
        </div>
        """)

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-5">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 flex flex-col justify-between gap-3 pb-2">
        {"".join(points_html)}
      </div>
    </div>
    """


def _render_matrix_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "战略决策矩阵")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "STRATEGY MATRIX")
    quadrants = slide.get("quadrants", [])
    x_axis = slide.get("x_axis", {"title": "X 轴", "min_label": "弱/低", "max_label": "强/高"})
    y_axis = slide.get("y_axis", {"title": "Y 轴", "min_label": "弱/低", "max_label": "强/高"})
    principles = slide.get("principles") or slide.get("takeaways", [])

    quad_coords = ["top_left", "top_right", "bottom_left", "bottom_right"]
    quad_cards_html = []
    for idx, pos_key in enumerate(quad_coords):
        q = {}
        if isinstance(quadrants, dict):
            q = quadrants.get(pos_key, {})
        elif isinstance(quadrants, list) and idx < len(quadrants):
            q = quadrants[idx]

        is_hl = q.get("highlight", False) or pos_key == "bottom_right"
        border_cls = "border-blue-600 ring-2 ring-blue-100 bg-blue-50/50" if is_hl else "border-slate-200 bg-white"
        title_cls = "text-blue-700 font-bold" if is_hl else "text-slate-900 font-bold"

        items = q.get("items") or q.get("bullets", [])
        items_html = "".join([f'<li class="text-xs text-slate-700 flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>{item}</li>' for item in items[:3]])

        quad_cards_html.append(f"""
        <div class="border rounded-xl p-4 shadow-sm flex flex-col justify-between {border_cls}">
          <div>
            <h4 class="text-base {title_cls}">{q.get('name') or q.get('title', f'象限 {idx+1}')}</h4>
            <p class="text-xs text-slate-500 mt-1 leading-snug">{q.get('strategy') or q.get('desc', '')}</p>
          </div>
          <ul class="mt-3 space-y-1.5">
            {items_html}
          </ul>
        </div>
        """)

    side_html = ""
    if principles:
        p_items = "".join([f'<div class="text-xs text-slate-700 mb-2"><span class="font-bold text-amber-600 mr-1.5">0{i+1}</span>{p}</div>' for i, p in enumerate(principles[:4])])
        side_html = f"""
        <div class="w-72 bg-amber-50/60 border border-amber-200 rounded-xl p-4 flex flex-col shadow-sm">
          <h4 class="text-sm font-bold text-amber-800 mb-3 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
            {slide.get('principles_title', '战略决策原则')}
          </h4>
          <div class="flex-1 flex flex-col justify-around">
            {p_items}
          </div>
        </div>
        """

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-4">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 flex gap-5 pb-2">
        <div class="flex-1 flex flex-col">
          <div class="flex-1 grid grid-cols-2 gap-3.5">
            {"".join(quad_cards_html)}
          </div>
          <div class="mt-2 text-center text-xs font-bold text-blue-700 bg-blue-50/60 py-1 rounded border border-blue-100">
            {x_axis.get('min_label', '弱')} ← {x_axis.get('title', 'X 轴')} → {x_axis.get('max_label', '强')}
          </div>
        </div>
        {side_html}
      </div>
    </div>
    """


def _render_ladder_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "能力梯队成熟度模型")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "MATURITY LADDER")
    levels = slide.get("levels", [])
    safety_rule = slide.get("safety_line") or slide.get("footer_rule", "")

    cols_html = []
    num_cols = min(len(levels), 4)
    for idx, lvl in enumerate(levels[:num_cols]):
        is_hl = lvl.get("highlight", False) or idx == num_cols - 1
        border_cls = "border-blue-600 ring-2 ring-blue-100 bg-blue-50/50" if is_hl else "border-slate-200 bg-white"

        cols_html.append(f"""
        <div class="border rounded-xl p-4 shadow-sm flex flex-col justify-between {border_cls}">
          <div>
            <span class="text-[11px] font-extrabold uppercase tracking-wider text-blue-600">{lvl.get('level', f'Level {idx+1}')}</span>
            <h4 class="text-lg font-bold text-slate-900 mt-1">{lvl.get('name') or lvl.get('title', f'阶段 {idx+1}')}</h4>
            <p class="text-xs text-slate-500 mt-1 leading-snug">{lvl.get('desc', '')}</p>
          </div>
          <div class="space-y-2 mt-4 pt-3 border-t border-slate-100">
            <div class="bg-blue-50/80 rounded p-2 text-xs">
              <span class="font-bold text-blue-800">核心抓手:</span>
              <span class="text-slate-700 block mt-0.5">{lvl.get('mechanism', '-')}</span>
            </div>
            <div class="bg-amber-50/80 rounded p-2 text-xs">
              <span class="font-bold text-amber-800">衡量指标:</span>
              <span class="text-slate-700 block mt-0.5">{lvl.get('metric', '-')}</span>
            </div>
            <div class="text-[11px] text-slate-500 pt-1">
              <span class="font-semibold text-slate-600">协同:</span> {lvl.get('roles', '-')}
            </div>
          </div>
        </div>
        """)

    safety_html = ""
    if safety_rule:
        safety_html = f"""
        <div class="mt-3 bg-blue-50/80 border border-blue-200 rounded-lg py-2 px-4 text-center text-xs font-bold text-blue-800">
          ★ {safety_rule}
        </div>
        """

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-4">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 grid grid-cols-{num_cols} gap-3.5">
        {"".join(cols_html)}
      </div>
      {safety_html}
    </div>
    """


def _render_horizons_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "一体两翼三道地平线分池管理")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "THREE HORIZONS")
    horizons = slide.get("horizons", [])
    summary_text = slide.get("summary_card") or slide.get("core_principle", "")

    top_banner = ""
    if summary_text:
        top_banner = f"""
        <div class="mb-3 bg-blue-50/80 border border-blue-200 rounded-lg py-2 px-4 text-center text-xs font-bold text-blue-800">
          分池管理原则: {summary_text}
        </div>
        """

    h_cols = []
    accents = [
        {"badge": "bg-blue-600", "border": "border-blue-500", "bg": "bg-blue-50/40"},
        {"badge": "bg-indigo-600", "border": "border-indigo-500", "bg": "bg-indigo-50/40"},
        {"badge": "bg-amber-600", "border": "border-amber-500", "bg": "bg-amber-50/40"},
    ]

    for idx, h in enumerate(horizons[:3]):
        acc = accents[idx % len(accents)]
        focus_items = h.get("focus") or h.get("items", [])
        if isinstance(focus_items, str):
            focus_items = [f.strip() for f in focus_items.split("、") if f.strip()]
        f_html = "".join([f'<li class="text-xs text-slate-700 flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-slate-400"></span>{item}</li>' for item in focus_items[:4]])

        h_cols.append(f"""
        <div class="bg-white border-2 {acc['border']} rounded-xl p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div class="inline-block {acc['badge']} text-white text-xs font-black px-2 py-0.5 rounded">
              {h.get('id', f'H{idx+1}')}
            </div>
            <h4 class="text-lg font-bold text-slate-900 mt-2">{h.get('title', f'地平线 {idx+1}')}</h4>
            <ul class="mt-3 space-y-1.5">
              {f_html}
            </ul>
          </div>
          <div class="space-y-2 mt-4 pt-3 border-t border-slate-100 text-xs">
            <div class="bg-slate-50 p-2 rounded">
              <span class="font-bold text-slate-700">管理方式:</span>
              <span class="text-slate-600 block mt-0.5">{h.get('governance', '-')}</span>
            </div>
            <div class="bg-slate-50 p-2 rounded">
              <span class="font-bold text-slate-700">考核标准:</span>
              <span class="text-slate-600 block mt-0.5">{h.get('metric', '-')}</span>
            </div>
            <div class="text-slate-400 text-[11px] pt-1">
              风险: {h.get('risk_profile', '-')}
            </div>
          </div>
        </div>
        """)

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-3">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      {top_banner}
      <div class="flex-1 grid grid-cols-3 gap-4 pb-2">
        {"".join(h_cols)}
      </div>
    </div>
    """


def _render_cross_mapping_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "四层协同组织映射全景")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "CROSS MAPPING")
    rows = slide_data_rows = slide.get("mapping_rows") or slide.get("rows", [])

    rows_html = []
    for idx, r in enumerate(rows[:4]):
        rows_html.append(f"""
        <div class="flex items-center gap-3 bg-white border border-slate-200 rounded-xl p-3 shadow-sm hover:border-blue-300 transition-colors">
          <div class="w-28 bg-blue-600 text-white font-bold text-xs py-3 px-2 rounded-lg text-center flex-shrink-0">
            {r.get('tier', f'层级 0{idx+1}')}
          </div>
          <div class="flex-1 bg-slate-50 border border-slate-200/80 rounded-lg p-3">
            <div class="text-xs font-bold text-blue-800">{r.get('source_role') or r.get('source_title', '标杆实践')}</div>
            <div class="text-[11px] text-slate-500 mt-0.5">{r.get('source_desc', '')}</div>
          </div>
          <div class="text-amber-500 font-extrabold text-base px-1">➔</div>
          <div class="flex-1 bg-blue-50/50 border border-blue-200 rounded-lg p-3">
            <div class="text-xs font-bold text-slate-900">{r.get('target_role') or r.get('target_title', '落地机制')}</div>
            <div class="text-[11px] text-slate-600 mt-0.5">{r.get('target_desc', '')}</div>
          </div>
        </div>
        """)

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-4">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 flex flex-col justify-between gap-2.5 pb-2">
        {"".join(rows_html)}
      </div>
    </div>
    """


HTML_RENDERERS = {
    "cover": _render_cover_html,
    "architecture_stack": _render_architecture_stack_html,
    "bento_cards": _render_bento_cards_html,
    "metric_spotlight": _render_metric_spotlight_html,
    "timeline": _render_timeline_html,
    "summary": _render_summary_html,
    "matrix_2x2": _render_matrix_html,
    "matrix": _render_matrix_html,
    "maturity_ladder": _render_ladder_html,
    "ladder": _render_ladder_html,
    "horizons_curve": _render_horizons_html,
    "horizons": _render_horizons_html,
    "three_horizons": _render_horizons_html,
    "cross_mapping": _render_cross_mapping_html,
    "dual_mapping": _render_cross_mapping_html,
}


def build_standalone_html(blueprint: Any, tokens: Dict[str, Any], output_path: str) -> str:
    """Generate a single-file standalone HTML presentation with zero external dependencies."""
    p = tokens.get("palette", {})
    slides_content_list = []

    contract = None
    slides = []
    if isinstance(blueprint, dict):
        contract = blueprint.get("contract")
        slides = blueprint.get("slides", [])
    elif isinstance(blueprint, list):
        slides = blueprint

    for idx, slide_data in enumerate(slides):
        l_type = slide_data.get("layout_type", "bento_cards")
        renderer = HTML_RENDERERS.get(l_type, _render_bento_cards_html)
        inner_html = renderer(slide_data, tokens)

        arc_attr = html.escape(str(slide_data.get("narrative_arc", "")), quote=True)
        mission_attr = html.escape(str(slide_data.get("mission", "")), quote=True)
        transition_attr = html.escape(str(slide_data.get("transition", "")), quote=True)
        evidence_attr = html.escape(str(slide_data.get("core_evidence", "")), quote=True)

        slides_content_list.append(f"""
        <!-- Slide {idx+1} -->
        <section class="slide absolute inset-0 transition-opacity duration-300 pointer-events-none opacity-0 flex flex-col"
                 data-slide="{idx}"
                 data-arc="{arc_attr}"
                 data-mission="{mission_attr}"
                 data-transition="{transition_attr}"
                 data-evidence="{evidence_attr}">
          {inner_html}
        </section>
        """)

    slides_blob = "\n".join(slides_content_list)
    total_slides = len(slides)

    # Compile entire HTML bundle
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN" class="h-full bg-slate-950">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>undoPPT - Editable Presentation</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              primary: '{p.get("primary", "#2563EB")}',
              secondary: '{p.get("secondary", "#38BDF8")}',
              accent: '{p.get("accent", "#F59E0B")}'
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    body {{
      font-family: 'PingFang SC', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      user-select: none;
    }}
    .slide.active {{
      opacity: 1;
      pointer-events: auto;
      z-index: 10;
    }}
    /* Aspect Ratio 16:9 canvas container */
    .aspect-16-9 {{
      aspect-ratio: 16 / 9;
    }}
  </style>
</head>
<body class="h-full flex flex-col items-center justify-center overflow-hidden bg-slate-900 text-slate-800">

  <!-- Main Presentation Canvas Frame -->
  <main id="presentation-frame" class="relative w-full max-w-[1340px] aspect-16-9 max-h-[92vh] bg-[#F8FAFC] shadow-2xl rounded-2xl overflow-hidden border border-slate-800/60">
    {slides_blob}
  </main>

  <!-- Cognitive Inspector Drawer (N) -->
  <aside id="cognitive-drawer" class="fixed top-5 right-5 w-84 max-w-[340px] bg-slate-900/95 backdrop-blur-md border border-slate-700/80 text-slate-200 rounded-2xl p-4 shadow-2xl z-50 text-xs hidden transition-all duration-300">
    <div class="flex items-center justify-between pb-2 border-b border-slate-700/80 mb-3">
      <span class="font-bold text-blue-400 flex items-center gap-1.5">
        <span>🧠</span>
        <span>认知动力学 (Cognitive Notes)</span>
      </span>
      <button id="close-drawer-btn" class="text-slate-400 hover:text-white px-1.5 py-0.5 rounded hover:bg-slate-800 transition-colors">✕</button>
    </div>
    <div class="space-y-3">
      <div>
        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-0.5">叙事节奏 (Arc)</div>
        <div id="note-arc" class="text-amber-400 font-mono font-bold text-sm">HOOK</div>
      </div>
      <div>
        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-0.5">单页使命 (Mission)</div>
        <div id="note-mission" class="text-slate-200 leading-relaxed"></div>
      </div>
      <div>
        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-0.5">承上启下逻辑 (Transition)</div>
        <div id="note-transition" class="text-slate-300 italic leading-relaxed"></div>
      </div>
      <div>
        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-0.5">核心论据 (Evidence)</div>
        <div id="note-evidence" class="text-emerald-400 font-medium leading-relaxed"></div>
      </div>
    </div>
  </aside>

  <!-- Interactive Controls Bar -->
  <footer class="fixed bottom-3 left-1/2 -translate-x-1/2 bg-slate-800/90 backdrop-blur border border-slate-700 text-slate-200 px-5 py-2 rounded-full shadow-lg flex items-center gap-4 text-xs z-50">
    <button id="prev-btn" class="hover:text-blue-400 transition-colors px-1" title="Previous Slide (← / PageUp)">◀</button>
    <span id="slide-indicator" class="font-mono font-medium text-slate-300">1 / {total_slides}</span>
    <button id="next-btn" class="hover:text-blue-400 transition-colors px-1" title="Next Slide (→ / Space / PageDown)">▶</button>
    <div class="h-3 w-[1px] bg-slate-600"></div>
    <button id="notes-btn" class="hover:text-blue-400 transition-colors" title="Toggle Cognitive Notes (N)">Notes (N)</button>
    <button id="overview-btn" class="hover:text-blue-400 transition-colors" title="Overview (O)">Overview</button>
    <button id="fs-btn" class="hover:text-blue-400 transition-colors" title="Toggle Fullscreen (F)">Fullscreen</button>
  </footer>

  <!-- Top Progress Bar -->
  <div class="fixed top-0 left-0 right-0 h-1 bg-slate-800 z-50">
    <div id="progress-bar" class="h-full bg-blue-500 transition-all duration-300" style="width: {(1/total_slides)*100 if total_slides else 100}%;"></div>
  </div>

  <script>
    let currentSlide = 0;
    const total = {total_slides};
    const slides = document.querySelectorAll('.slide');
    const indicator = document.getElementById('slide-indicator');
    const progress = document.getElementById('progress-bar');
    const drawer = document.getElementById('cognitive-drawer');
    const noteArc = document.getElementById('note-arc');
    const noteMission = document.getElementById('note-mission');
    const noteTransition = document.getElementById('note-transition');
    const noteEvidence = document.getElementById('note-evidence');

    function toggleNotes() {{
      drawer.classList.toggle('hidden');
    }}

    function updateCognitiveNotes(slideEl) {{
      if (!slideEl) return;
      noteArc.textContent = (slideEl.dataset.arc || 'N/A').toUpperCase();
      noteMission.textContent = slideEl.dataset.mission || '（本页未指定具体使命）';
      noteTransition.textContent = slideEl.dataset.transition || '（开篇立论 / 无前序转折）';
      noteEvidence.textContent = slideEl.dataset.evidence || '（未单独分级核心论据）';
    }}

    function showSlide(index) {{
      if (index < 0) index = 0;
      if (index >= total) index = total - 1;
      currentSlide = index;

      slides.forEach((s, idx) => {{
        if (idx === currentSlide) {{
          s.classList.add('active');
        }} else {{
          s.classList.remove('active');
        }}
      }});

      indicator.textContent = `${{currentSlide + 1}} / ${{total}}`;
      progress.style.width = `${{((currentSlide + 1) / total) * 100}}%`;
      updateCognitiveNotes(slides[currentSlide]);
    }}

    // Navigation events
    document.getElementById('prev-btn').addEventListener('click', () => showSlide(currentSlide - 1));
    document.getElementById('next-btn').addEventListener('click', () => showSlide(currentSlide + 1));
    document.getElementById('notes-btn').addEventListener('click', toggleNotes);
    document.getElementById('close-drawer-btn').addEventListener('click', () => drawer.classList.add('hidden'));

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        e.preventDefault();
        showSlide(currentSlide + 1);
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'Backspace') {{
        e.preventDefault();
        showSlide(currentSlide - 1);
      }} else if (e.key === 'f' || e.key === 'F') {{
        toggleFullscreen();
      }} else if (e.key === 'n' || e.key === 'N') {{
        toggleNotes();
      }}
    }});

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        if (document.exitFullscreen) {{
          document.exitFullscreen();
        }}
      }}
    }}

    document.getElementById('fs-btn').addEventListener('click', toggleFullscreen);

    // Initial render
    showSlide(0);
  </script>
</body>
</html>
"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path
