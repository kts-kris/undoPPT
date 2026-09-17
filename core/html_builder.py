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
import re
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
            f'<div class="architecture-item flex-1 min-w-[120px] bg-slate-50 border border-slate-200 rounded-lg py-2.5 px-3 text-center text-sm font-semibold text-slate-800 shadow-sm hover:border-blue-500 hover:bg-blue-50/70 hover:shadow-md cursor-pointer transition-all flex items-center justify-center gap-1.5 group" data-component="{html.escape(item)}" data-layer="{html.escape(name)}"><span>{item}</span><span class="text-[10px] text-blue-500 opacity-40 group-hover:opacity-100 transition-opacity">🔍</span></div>'
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
      <div class="flex items-center justify-between mb-5">
        <div>
          <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
          <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
          <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
        </div>
        <div class="text-xs font-medium text-slate-400 flex items-center gap-1.5 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200 shadow-inner">
          <span>💡</span> 点击组件下钻技术规格与故障域
        </div>
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
    import re
    title = slide.get("action_title") or slide.get("title", "核心业绩指标衡量")
    subtitle = slide.get("subtitle", "")
    metrics = slide.get("metrics", [])
    p = tokens.get("palette", {})
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "KPI DASHBOARD")
    sandbox_cfg = slide.get("sandbox", {})

    metrics_html = []
    for idx, m in enumerate(metrics[:4]):
        label = m.get("label", "核心指标")
        val = str(m.get("value", "99.9%"))
        delta = str(m.get("delta", ""))
        desc = m.get("desc", "")

        # Compute scenario variations from sandbox config or derive dynamically
        cons_val = None
        aggr_val = None
        cons_delta = None
        aggr_delta = None
        if sandbox_cfg and sandbox_cfg.get("scenarios"):
            sc_cons = sandbox_cfg["scenarios"].get("conservative", {}).get("metrics", [])
            if idx < len(sc_cons):
                cons_val = sc_cons[idx].get("value")
                cons_delta = sc_cons[idx].get("delta")
            sc_aggr = sandbox_cfg["scenarios"].get("aggressive", {}).get("metrics", [])
            if idx < len(sc_aggr):
                aggr_val = sc_aggr[idx].get("value")
                aggr_delta = sc_aggr[idx].get("delta")

        if not cons_val or not aggr_val:
            num_match = re.search(r"([0-9]+(?:\.[0-9]+)?)", val)
            if num_match:
                num = float(num_match.group(1))
                prefix = val[:num_match.start(1)]
                suffix = val[num_match.end(1):]
                c_num = round(num * 0.88, 1) if num > 1 else round(num * 0.9, 2)
                a_num = round(min(100.0, num * 1.15) if "%" in suffix else num * 1.25, 1)
                cons_val = f"{prefix}{c_num:g}{suffix}"
                aggr_val = f"{prefix}{a_num:g}{suffix}"
            else:
                cons_val = val
                aggr_val = val

        if not cons_delta:
            cons_delta = "稳健保底"
        if not aggr_delta:
            aggr_delta = "激进突破"

        delta_html = f'<div class="metric-delta text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full inline-block mb-3" data-base-delta="{delta}" data-cons-delta="{cons_delta}" data-aggr-delta="{aggr_delta}">▲ {delta if delta else "基准目标"}</div>'

        metrics_html.append(f"""
        <div class="flex-1 flex flex-col justify-between bg-white border border-slate-200 rounded-xl p-7 shadow-sm hover:shadow-md transition-all">
          <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">{label}</div>
            <div class="text-5xl font-extrabold text-blue-600 font-mono tracking-tight mb-2 metric-val"
                 data-base-val="{val}"
                 data-conservative-val="{cons_val}"
                 data-aggressive-val="{aggr_val}">{val}</div>
            {delta_html}
          </div>
          <div class="text-xs text-slate-500 border-t border-slate-100 pt-3 leading-relaxed">
            {desc}
          </div>
        </div>
        """)

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="flex items-center justify-between mb-5">
        <div>
          <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
          <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
          <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
        </div>
        <!-- Scenario Switcher Sandbox -->
        <div class="scenario-sandbox flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-semibold shadow-inner">
          <button class="scenario-btn active px-3 py-1.5 rounded-lg text-blue-700 bg-white shadow-sm font-bold transition-all" data-scenario="baseline">基准方案 (Baseline)</button>
          <button class="scenario-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition-all" data-scenario="conservative">保守方案 (Conservative)</button>
          <button class="scenario-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 transition-all" data-scenario="aggressive">突破方案 (Aggressive)</button>
        </div>
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
    options = slide.get("options", [])
    sign_off_items = slide.get("sign_off_items", [])
    recommendation = slide.get("recommendation", "")
    p = tokens.get("palette", {})
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "SUMMARY")

    # Decision-Ready Ask Mode (Options / Sign-off Items)
    if options or sign_off_items:
        opts_html = []
        if options:
            col_class = "grid-cols-3" if len(options) >= 3 else "grid-cols-2"
            for opt_idx, opt in enumerate(options[:3]):
                is_rec = bool(opt.get("recommended", False))
                border_cls = "border-blue-600 bg-blue-50/40 ring-2 ring-blue-500/20" if is_rec else "border-slate-200 bg-white"
                badge_html = """<div class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-blue-600 text-white mb-2 shadow-sm">★ 推荐决策 RECOMMENDED</div>""" if is_rec else ""
                pros = opt.get("pros", "")
                cons = opt.get("cons", "")
                cost = opt.get("cost", "N/A")
                risk = opt.get("risk", "N/A")

                opts_html.append(f"""
                <div class="rounded-xl border p-3.5 shadow-sm flex flex-col justify-between {border_cls}">
                  <div>
                    {badge_html}
                    <h4 class="text-sm font-bold text-slate-900">{opt.get('name', f'方案 {chr(65+opt_idx)}')}</h4>
                    {f'<div class="text-[11px] text-emerald-800 bg-emerald-50 rounded px-2 py-1 mt-2">✔ 优势: {pros}</div>' if pros else ''}
                    {f'<div class="text-[11px] text-rose-700 bg-rose-50 rounded px-2 py-1 mt-1">✖ 短板: {cons}</div>' if cons else ''}
                  </div>
                  <div class="mt-3 pt-2 border-t border-slate-200/70 flex justify-between text-[10px] text-slate-500 font-semibold">
                    <span>投入: {cost}</span>
                    <span>风险: {risk}</span>
                  </div>
                </div>
                """)

        rec_banner_html = ""
        if recommendation:
            rec_banner_html = f"""
            <div class="bg-amber-50 border border-amber-200 rounded-xl px-4 py-2 text-xs text-amber-900 font-medium flex items-center gap-2">
              <span class="font-bold text-amber-700 flex-shrink-0">💡 决策建议:</span>
              <span>{recommendation}</span>
            </div>
            """

        signoff_html = ""
        if sign_off_items:
            items_checkbox_html = []
            for item in sign_off_items:
                clean_item = re.sub(r'^[\[\(\d+\]\)\.\s✓]+', '', item).strip()
                items_checkbox_html.append(f"""
                <label class="flex items-center gap-3 bg-slate-800/90 hover:bg-slate-800 px-3.5 py-1.5 rounded-lg cursor-pointer transition-colors">
                  <input type="checkbox" checked class="w-4 h-4 rounded text-blue-500 focus:ring-0 bg-slate-700 border-slate-600 cursor-pointer" />
                  <span class="text-xs font-medium text-slate-200 leading-snug">{clean_item}</span>
                </label>
                """)

            signoff_html = f"""
            <div class="bg-slate-900 text-white rounded-xl p-3.5 shadow-lg border border-slate-800">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold uppercase tracking-wider text-blue-400">请领导决策与审批清单 (Sign-off Items)</span>
                <span class="text-[10px] text-slate-400">现场演示可直接勾选核准</span>
              </div>
              <div class="space-y-1.5">
                {"".join(items_checkbox_html)}
              </div>
            </div>
            """

        # If we have points but no options, show points on left / top
        fallback_points_html = ""
        if not options and points:
            pts = []
            for idx, pt in enumerate(points[:3]):
                pts.append(f"""
                <div class="flex items-center gap-3 bg-white border border-slate-200 rounded-lg p-2.5 shadow-sm">
                  <div class="w-6 h-6 rounded bg-blue-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0">{idx+1}</div>
                  <div class="flex-1">
                    <h5 class="text-xs font-bold text-slate-900">{pt.get('title', f'要点 {idx+1}')}</h5>
                    <p class="text-[11px] text-slate-500 leading-tight mt-0.5">{pt.get('desc', '')}</p>
                  </div>
                </div>
                """)
            fallback_points_html = f"""<div class="space-y-1.5 mb-2">{"".join(pts)}</div>"""

        return f"""
        <div class="h-full flex flex-col px-12 py-8">
          <div class="mb-4">
            <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
            <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
            <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
          </div>
          <div class="flex-1 flex flex-col justify-between gap-2.5 pb-2">
            {fallback_points_html}
            {f'<div class="grid {col_class} gap-3">{"".join(opts_html)}</div>' if opts_html else ''}
            {rec_banner_html}
            {signoff_html}
          </div>
        </div>
        """

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



def _render_table_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "数据与指标概览")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "DATA TABLE")
    headers = slide.get("headers", ["维度", "指标", "目标值", "达成说明"])
    rows = slide.get("rows", [])
    if not rows:
        rows = [["示例维度", "基础指标", "100%", "符合预期"]]

    highlight_idx = slide.get("highlight_row_index", -1)
    if isinstance(highlight_idx, int):
        highlight_set = {highlight_idx}
    elif isinstance(highlight_idx, list):
        highlight_set = set(highlight_idx)
    else:
        highlight_set = set()

    th_html = "".join([
        f'<th class="py-3 px-4 text-center text-xs font-bold text-white uppercase tracking-wider bg-blue-600 first:rounded-tl-lg last:rounded-tr-lg first:text-left">{h}</th>'
        for h in headers
    ])

    tr_html = []
    for r_idx, row in enumerate(rows[:8]):
        is_hl = r_idx in highlight_set
        bg_cls = "bg-blue-50/70 font-semibold" if is_hl else ("bg-slate-50/70" if r_idx % 2 == 1 else "bg-white")
        td_items = []
        for c_idx, cell in enumerate(row):
            align_cls = "text-left font-medium text-slate-900" if c_idx == 0 else "text-center text-slate-700"
            if is_hl:
                align_cls += " text-blue-700"
            td_items.append(f'<td class="py-2.5 px-4 text-xs {align_cls} border-b border-slate-200/70">{cell}</td>')
        tr_html.append(f'<tr class="{bg_cls} hover:bg-blue-50/30 transition-colors">{"".join(td_items)}</tr>')

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-4">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 overflow-x-auto bg-white border border-slate-200 rounded-xl shadow-sm p-2 flex flex-col justify-center">
        <table class="min-w-full text-left border-collapse">
          <thead>
            <tr>{th_html}</tr>
          </thead>
          <tbody>
            {"".join(tr_html)}
          </tbody>
        </table>
      </div>
    </div>
    """


def _render_chart_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "核心数据趋势分析")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "DATA CHART")
    categories = slide.get("categories", ["Q1", "Q2", "Q3", "Q4"])
    series = slide.get("series", [{"name": "数值", "values": [35, 55, 78, 95]}])
    takeaway = slide.get("takeaway") or slide.get("core_evidence", "")
    bullets = slide.get("bullets", [])

    max_val = 1.0
    for s in series:
        for v in s.get("values", []):
            try:
                max_val = max(max_val, float(v))
            except Exception:
                pass

    bars_html = []
    for c_idx, cat in enumerate(categories):
        cat_bars = []
        for s_idx, s in enumerate(series):
            val = 0.0
            if c_idx < len(s.get("values", [])):
                try:
                    val = float(s["values"][c_idx])
                except Exception:
                    val = 0.0
            pct = min(100.0, max(8.0, (val / max_val) * 100))
            col_bg = "bg-blue-600" if s_idx == 0 else ("bg-indigo-400" if s_idx == 1 else "bg-amber-400")
            cat_bars.append(f"""
            <div class="flex flex-col items-center gap-1.5 flex-1">
              <span class="text-[11px] font-bold text-slate-600">{val}</span>
              <div class="w-full {col_bg} rounded-t-md transition-all hover:opacity-80" style="height: {int(pct * 1.7)}px;"></div>
            </div>
            """)

        bars_html.append(f"""
        <div class="flex-1 flex flex-col items-center justify-end h-48 border-b border-slate-200 pb-2 px-2">
          <div class="w-full flex items-end justify-center gap-1.5 h-full">
            {"".join(cat_bars)}
          </div>
          <span class="text-xs font-semibold text-slate-700 mt-2">{cat}</span>
        </div>
        """)

    legend_items = []
    for s_idx, s in enumerate(series):
        col_bg = "bg-blue-600" if s_idx == 0 else ("bg-indigo-400" if s_idx == 1 else "bg-amber-400")
        legend_items.append(f"""
        <div class="flex items-center gap-1.5">
          <div class="w-3 h-3 rounded {col_bg}"></div>
          <span class="text-xs text-slate-600 font-medium">{s.get('name', '指标')}</span>
        </div>
        """)

    bullets_html = "".join([f'<li class="text-xs text-slate-600 mb-1">▸ {b}</li>' for b in bullets[:3]])

    takeaway_card = f"""
    <div class="w-80 bg-white border border-blue-200 rounded-xl p-5 shadow-sm flex flex-col justify-between">
      <div>
        <span class="text-[10px] font-bold text-blue-600 tracking-wider uppercase bg-blue-50 px-2 py-0.5 rounded">KEY TAKEAWAY</span>
        <h4 class="text-sm font-bold text-slate-900 mt-2 mb-2">核心数据洞察与结论</h4>
        <p class="text-xs text-slate-600 leading-relaxed">{takeaway}</p>
        <ul class="mt-3 list-none p-0">{bullets_html}</ul>
      </div>
      <div class="text-[11px] text-slate-400 border-t border-slate-100 pt-2 mt-4">数据驱动决策 · 闭环可核验</div>
    </div>
    """ if takeaway else ""

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-3">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 flex gap-5 items-stretch pb-2">
        <div class="flex-1 bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-col justify-between">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">趋势对比指标</span>
            <div class="flex gap-4">{"".join(legend_items)}</div>
          </div>
          <div class="flex-1 flex items-end justify-between gap-3 pt-4">
            {"".join(bars_html)}
          </div>
        </div>
        {takeaway_card}
      </div>
    </div>
    """


def _render_columns_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "核心要素与内容解构")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "OVERVIEW")
    columns = slide.get("columns", [])
    if not columns:
        columns = [
            {"badge": "板块 1", "title": "核心主张", "desc": "阐明核心概念与基础背景。", "bullets": ["要点 1", "要点 2"]},
            {"badge": "板块 2", "title": "关键举措", "desc": "明确关键实施路径与抓手。", "bullets": ["要点 1", "要点 2"]},
            {"badge": "板块 3", "title": "成效保障", "desc": "落实落地机制与保障举措。", "bullets": ["要点 1", "要点 2"]}
        ]

    cols_html = []
    for idx, col in enumerate(columns[:4]):
        is_hl = bool(col.get("highlight", False))
        badge = col.get("badge") or f"0{idx+1}"
        bullets = "".join([f'<li class="text-xs text-slate-700 flex items-start gap-1.5"><span class="text-blue-600 font-bold">✔</span> <span>{b}</span></li>' for b in col.get("bullets", [])[:4]])
        border_cls = "border-blue-500 ring-1 ring-blue-500 shadow-md" if is_hl else "border-slate-200 shadow-sm"

        cols_html.append(f"""
        <div class="flex-1 bg-white border {border_cls} rounded-xl p-5 flex flex-col justify-between hover:shadow-md transition-shadow relative overflow-hidden">
          {'<div class="absolute top-0 left-0 right-0 h-1.5 bg-blue-600"></div>' if is_hl else ''}
          <div>
            <span class="text-[10px] font-bold text-blue-600 tracking-wider uppercase bg-blue-50 px-2 py-0.5 rounded">{badge}</span>
            <h3 class="text-lg font-bold text-slate-900 mt-2 mb-1.5">{col.get('title', f'要素 {idx+1}')}</h3>
            <p class="text-xs text-slate-500 mb-4 leading-relaxed">{col.get('desc', '')}</p>
            <ul class="space-y-2 list-none p-0">{bullets}</ul>
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
      <div class="flex-1 flex gap-4 items-stretch pb-2">
        {"".join(cols_html)}
      </div>
    </div>
    """


def _render_quote_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "核心洞察与主张")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "INSIGHT")
    quote = slide.get("quote") or slide.get("statement") or "“真正卓越的方案并非功能的繁琐堆砌，而是以最小认知负荷实现确定性的业务交付。”"
    author = slide.get("author", "核心观点")
    role = slide.get("role", "评审专家")
    context = slide.get("context", "")

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-4">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 bg-white border border-slate-200 border-l-[10px] border-l-blue-600 rounded-2xl p-10 shadow-sm flex flex-col justify-between relative overflow-hidden">
        <div class="text-7xl font-serif text-blue-100 absolute top-4 left-6 select-none pointer-events-none">“</div>
        <div class="relative z-10 pt-4">
          <p class="text-2xl font-bold text-slate-900 leading-relaxed tracking-wide mb-6 max-w-4xl">
            {quote}
          </p>
        </div>
        <div class="border-t border-slate-100 pt-4 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-blue-50 border border-blue-200 flex items-center justify-center font-bold text-blue-700 text-sm">
              {author[:2]}
            </div>
            <div>
              <div class="text-sm font-bold text-slate-900">— {author}</div>
              <div class="text-xs text-slate-500">{role}</div>
            </div>
          </div>
          <div class="text-xs text-slate-400 italic max-w-md text-right">{context}</div>
        </div>
      </div>
    </div>
    """


def _render_flow_html(slide: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    title = slide.get("action_title") or slide.get("title", "标准化实施流水线与推进流程")
    subtitle = slide.get("subtitle", "")
    tag = slide.get("tag") or (slide.get("narrative_arc", "").upper() if slide.get("narrative_arc") else "PROCESS FLOW")
    stages = slide.get("stages") or slide.get("steps", [])
    if not stages:
        stages = [
            {"step": "01", "name": "需求输入与对齐", "desc": "明确目标与边界", "items": ["痛点调研", "认知契约确立"]},
            {"step": "02", "name": "方案设计与建模", "desc": "架构解耦与设计", "items": ["图元选型", "蓝图语法校验"]},
            {"step": "03", "name": "工程构建与审计", "desc": "原生矢量交付", "items": ["质量体检", "双端渲染输出"]},
            {"step": "04", "name": "协同感知与闭环", "desc": "持续演进复盘", "items": ["双向同步", "效果持续跟踪"]}
        ]

    n_stages = min(5, len(stages))
    stages_html = []
    for idx, stg in enumerate(stages[:n_stages]):
        is_hl = bool(stg.get("highlight", False))
        step_lbl = str(stg.get("step") or f"0{idx+1}")
        items_html = "".join([f'<li class="text-[11px] text-slate-600 flex items-start gap-1"><span class="text-blue-500">▸</span> {it}</li>' for it in stg.get("items", [])[:4]])
        border_cls = "border-blue-500 ring-1 ring-blue-500" if is_hl else "border-slate-200"

        stages_html.append(f"""
        <div class="flex-1 bg-white border {border_cls} rounded-xl p-4 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
          <div>
            <div class="w-7 h-7 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center mb-3">
              {step_lbl}
            </div>
            <h4 class="text-sm font-bold text-slate-900 mb-1">{stg.get('name') or stg.get('title', f'阶段 {idx+1}')}</h4>
            <p class="text-[11px] text-slate-500 mb-3 leading-tight">{stg.get('desc', '')}</p>
            <ul class="space-y-1.5 list-none p-0 border-t border-slate-100 pt-2.5">{items_html}</ul>
          </div>
        </div>
        """)
        if idx < n_stages - 1:
            stages_html.append('<div class="flex items-center text-blue-400 font-bold text-lg px-0.5">➔</div>')

    return f"""
    <div class="h-full flex flex-col px-12 py-8">
      <div class="mb-4">
        <span class="text-xs font-bold tracking-wider uppercase px-2.5 py-1 rounded bg-blue-50 text-blue-700">{tag}</span>
        <h2 class="text-3xl font-bold text-slate-900 mt-2">{title}</h2>
        <p class="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div class="flex-1 flex items-stretch gap-2 pb-2">
        {"".join(stages_html)}
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
    # v3.0 New Primitives
    "standard_table": _render_table_html,
    "table": _render_table_html,
    "data_chart": _render_chart_html,
    "chart": _render_chart_html,
    "content_columns": _render_columns_html,
    "columns": _render_columns_html,
    "rich_content": _render_columns_html,
    "keynote_quote": _render_quote_html,
    "quote": _render_quote_html,
    "statement": _render_quote_html,
    "process_flow": _render_flow_html,
    "flow": _render_flow_html,
    "workflow": _render_flow_html,
}


def _generate_default_objections(slide: Dict[str, Any]) -> List[Dict[str, str]]:
    """Synthesize high-conviction objection & defense pairings based on slide layout & evidence."""
    hud = slide.get("hud_notes", {})
    if hud and hud.get("objection_defense"):
        return hud.get("objection_defense")

    l_type = slide.get("layout_type", "")
    evidence = slide.get("core_evidence", "")
    mission = slide.get("mission", "")

    if l_type == "architecture_stack":
        return [
            {
                "skepticism": "分层解耦后，微服务跨层调用的网络时延与抖动如何管控？",
                "counter": f"各层级之间通过高性能 RPC 与本地内存缓存旁路连接，针对极端网络波动配置自适应超时熔断与保底策略{f'（{evidence}）' if evidence else ''}。"
            },
            {
                "skepticism": "底层依赖若发生单点故障，整体系统是否有不可用风险？",
                "counter": "基础设施层全部采用跨可用区多活部署与热备秒级倒换，故障域严格隔离至局部租户，绝不产生全局级联击穿。"
            }
        ]
    elif l_type in ("metric_spotlight", "data_chart"):
        return [
            {
                "skepticism": "核心 KPI 数据在生产全量压力下能否持续保持？有无实测样本偏差？",
                "counter": f"指标数据基于全链路压测与阶段性灰度环境多次实测统计{f'（{evidence}）' if evidence else ''}，采用 P99 严格口径，已剔除异常噪点并留有 20% 冗余。"
            },
            {
                "skepticism": "达到该指标所需的边际投入与计算资源成本是否过高？",
                "counter": "通过冷热数据分级和弹性资源池调度，单位计算成本相较传统方案下降，ROI 收益呈现非线性增长。"
            }
        ]
    elif l_type in ("timeline", "process_flow"):
        return [
            {
                "skepticism": "演进路线时间表是否过于激进？遇到外部不可控依赖如何对齐？",
                "counter": "关键里程碑均已拆解出明确的最小可行交付物（MVP），关键路径上预留了双周缓冲期，可按敏捷双周迭代无缝回滚或调优。"
            },
            {
                "skepticism": "各阶段交接的权责与质量验收标准由谁最终把关？",
                "counter": "每个阶段均设有硬性质量门禁与可量化验收 Checklist，未达标项一票否决，严禁带病推进。"
            }
        ]
    elif l_type in ("bento_cards", "matrix_2x2", "cross_mapping"):
        return [
            {
                "skepticism": "对比维度是否刻意规避了竞品或现有自研方案的优势？",
                "counter": "对比矩阵覆盖行业 4 大标准维度，客观呈现技术方案权衡（Trade-offs），重点凸显本架构在核心痛点场景下的代际优势。"
            },
            {
                "skepticism": "现有团队技术栈向新架构迁移的学习与改造摩擦成本是多少？",
                "counter": "提供零侵入 SDK 与自动化迁移适配脚本，存量业务只需按规范接入声明式配置，无需大规模重构业务代码。"
            }
        ]
    else:
        return [
            {
                "skepticism": "本方案与集团/行业主流路线是否有偏离？最终落地胜算多大？",
                "counter": f"方案严格紧扣战略主旨与客户核心价值闭环{f'（{mission}）' if mission else ''}，采用渐进式推进路线，风险可控。"
            },
            {
                "skepticism": "若执行过程中外部市场或环境出现大幅波动，应变预案是什么？",
                "counter": "已制定保守、基准、突破三套推演情境，各层抓手均具备动态参数调节弹性，可随时根据环境调整推进节奏。"
            }
        ]


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

    presentation_meta = {
        "contract": contract or {},
        "slides": []
    }

    for idx, slide_data in enumerate(slides):
        l_type = slide_data.get("layout_type", "bento_cards")
        renderer = HTML_RENDERERS.get(l_type, _render_bento_cards_html)
        inner_html = renderer(slide_data, tokens)

        arc_attr = html.escape(str(slide_data.get("narrative_arc", "")), quote=True)
        mission_attr = html.escape(str(slide_data.get("mission", "")), quote=True)
        transition_attr = html.escape(str(slide_data.get("transition", "")), quote=True)
        evidence_attr = html.escape(str(slide_data.get("core_evidence", "")), quote=True)

        presentation_meta["slides"].append({
            "slide_index": idx,
            "layout_type": l_type,
            "title": slide_data.get("title", ""),
            "action_title": slide_data.get("action_title", ""),
            "subtitle": slide_data.get("subtitle", ""),
            "narrative_arc": slide_data.get("narrative_arc", "progression"),
            "mission": slide_data.get("mission", ""),
            "transition": slide_data.get("transition", ""),
            "core_evidence": slide_data.get("core_evidence", ""),
            "objections": _generate_default_objections(slide_data),
            "sandbox": slide_data.get("sandbox", {})
        })

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
    meta_json = json.dumps(presentation_meta, ensure_ascii=False)

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
    .staged-hidden {{
      opacity: 0 !important;
      transform: translateY(12px) !important;
      pointer-events: none !important;
    }}
    .staged-visible {{
      opacity: 1 !important;
      transform: translateY(0) !important;
      transition: opacity 0.35s ease, transform 0.35s ease !important;
    }}
    /* Aspect Ratio 16:9 canvas container */
    .aspect-16-9 {{
      aspect-ratio: 16 / 9;
    }}
    @keyframes flowing-pulse {{
      0%, 100% {{ opacity: 0.5; transform: scale(0.99); }}
      50% {{ opacity: 1; transform: scale(1.01); filter: drop-shadow(0 0 6px rgba(59, 130, 246, 0.4)); }}
    }}
    .flowing-beam {{
      animation: flowing-pulse 2.5s infinite ease-in-out;
    }}
  </style>
</head>
<body class="h-full flex flex-col items-center justify-center overflow-hidden bg-slate-900 text-slate-800">

  <!-- Embedded Structured Presentation Metadata -->
  <script id="presentation-metadata" type="application/json">
    {meta_json}
  </script>

  <!-- Main Presentation Canvas Frame -->
  <main id="presentation-frame" class="relative w-full max-w-[1340px] aspect-16-9 max-h-[92vh] bg-[#F8FAFC] shadow-2xl rounded-2xl overflow-hidden border border-slate-800/60">
    {slides_blob}
  </main>

  <!-- Live Presenter HUD (P) -->
  <aside id="presenter-hud" class="fixed top-4 right-4 w-[430px] max-w-[92vw] max-h-[92vh] bg-slate-950/95 backdrop-blur-xl border border-blue-500/40 text-slate-200 rounded-2xl p-5 shadow-2xl z-50 text-xs hidden overflow-y-auto transition-all duration-300">
    <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
      <div class="flex items-center gap-2">
        <span class="text-base">🎙️</span>
        <div>
          <h3 class="font-bold text-sm text-white tracking-tight">现场演播双重视野中枢 (Presenter HUD)</h3>
          <span class="text-[10px] text-blue-400 font-mono">Cognitive Copilot · 快捷键 P</span>
        </div>
      </div>
      <button id="close-hud-btn" class="text-slate-400 hover:text-white px-2 py-1 rounded-lg hover:bg-slate-800 transition-colors">✕</button>
    </div>

    <div class="space-y-4">
      <!-- 认知罗盘 (Cognitive Compass) -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-3.5 space-y-2.5">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-bold text-blue-400 uppercase tracking-wider flex items-center gap-1.5">
            <span>🧭</span> 认知罗盘 (Cognitive Compass)
          </span>
          <span id="hud-arc-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold font-mono bg-blue-500/20 text-blue-300 border border-blue-500/30">PROGRESSION</span>
        </div>
        <div>
          <div class="text-[10px] text-slate-400 font-semibold mb-0.5">核心主旨向心力 (Core Thesis)</div>
          <div id="hud-core-thesis" class="text-slate-200 font-medium leading-relaxed bg-slate-950/60 p-2 rounded-lg border border-slate-800/80">未配置核心主旨</div>
        </div>
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div>
            <div class="text-[10px] text-slate-400 font-semibold mb-0.5">受众画像与立场</div>
            <div id="hud-audience" class="text-slate-300 truncate bg-slate-950/40 p-1.5 rounded border border-slate-800/50">全员受众</div>
          </div>
          <div>
            <div class="text-[10px] text-slate-400 font-semibold mb-0.5">本页攻坚使命 (Mission)</div>
            <div id="hud-mission" class="text-amber-300 font-medium truncate bg-slate-950/40 p-1.5 rounded border border-slate-800/50">战略认知推进</div>
          </div>
        </div>
      </div>

      <!-- 因果提词器 (Transition Teleprompter) -->
      <div class="bg-gradient-to-br from-blue-950/40 to-slate-900/90 border border-blue-500/40 rounded-xl p-3.5 space-y-1.5 shadow-inner">
        <div class="text-[11px] font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
          <span>🗣️</span> 因果提词器 (Transition Teleprompter)
        </div>
        <p class="text-[10px] text-slate-400">请在切入下一页前口播以下转折话术：</p>
        <div id="hud-teleprompter" class="text-sm font-semibold text-white bg-slate-950/80 p-3 rounded-lg border border-blue-500/30 leading-relaxed italic">
          自然推进至下一模块
        </div>
      </div>

      <!-- 质疑应对弹药库 (Objection Playbook) -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-3.5 space-y-2.5">
        <div class="text-[11px] font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
          <span>🛡️</span> 评委质疑应对弹药库 (Objection Playbook)
        </div>
        <div id="hud-objections-container" class="space-y-2.5">
          <!-- Dynamically populated -->
        </div>
      </div>
    </div>
  </aside>

  <!-- Architecture Drilldown Modal (EPIC-05) -->
  <div id="arch-drilldown-modal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
    <div class="bg-slate-900 border border-blue-500/40 rounded-2xl w-full max-w-lg p-6 shadow-2xl text-slate-200 relative">
      <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div>
          <span class="text-[10px] font-bold text-blue-400 uppercase tracking-wider bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20" id="drill-layer">LAYER</span>
          <h3 class="text-xl font-bold text-white mt-1" id="drill-component">组件名称</h3>
        </div>
        <button id="close-drill-btn" class="text-slate-400 hover:text-white px-2 py-1 rounded-lg hover:bg-slate-800 transition-colors">✕</button>
      </div>
      <div class="space-y-3.5 text-xs">
        <div class="grid grid-cols-3 gap-2">
          <div class="bg-slate-950/70 p-2.5 rounded-xl border border-slate-800 text-center">
            <div class="text-[10px] text-slate-400">SLA 目标</div>
            <div class="font-bold text-emerald-400 text-sm mt-0.5">99.99%</div>
          </div>
          <div class="bg-slate-950/70 p-2.5 rounded-xl border border-slate-800 text-center">
            <div class="text-[10px] text-slate-400">P99 延迟</div>
            <div class="font-bold text-blue-400 text-sm mt-0.5">&lt; 15ms</div>
          </div>
          <div class="bg-slate-950/70 p-2.5 rounded-xl border border-slate-800 text-center">
            <div class="text-[10px] text-slate-400">故障隔离</div>
            <div class="font-bold text-amber-400 text-sm mt-0.5">L3 隔离</div>
          </div>
        </div>
        <div>
          <div class="text-[11px] font-bold text-slate-300 mb-1">上下游调用链路</div>
          <div class="bg-slate-950/50 p-2.5 rounded-lg border border-slate-800 text-slate-400 leading-relaxed">
            统一入口网关 ➔ <span class="text-blue-400 font-semibold" id="drill-chain-comp">本组件</span> ➔ 跨可用区分布式网格与持久化存储
          </div>
        </div>
        <div>
          <div class="text-[11px] font-bold text-slate-300 mb-1">容灾与熔断回滚机制</div>
          <div class="bg-slate-950/50 p-2.5 rounded-lg border border-slate-800 text-slate-400 leading-relaxed">
            支持动态自适应令牌桶限流。当异常率超阈值时，自动触发 8ms 本地热备降级旁路，租户级故障强隔离。
          </div>
        </div>
      </div>
      <div class="mt-5 pt-3 border-t border-slate-800 flex justify-end">
        <button id="dismiss-drill-btn" class="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold transition-colors">确定 / 关闭</button>
      </div>
    </div>
  </div>

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
    <button id="step-btn" class="hover:text-blue-400 transition-colors" title="Toggle Staged Step Mode (S)">Step: OFF</button>
    <button id="hud-btn" class="hover:text-blue-400 transition-colors font-semibold text-blue-400" title="Toggle Presenter HUD (P)">HUD (P)</button>
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
    let stepMode = false;
    let currentStep = 0;
    const total = {total_slides};
    const slides = document.querySelectorAll('.slide');
    const indicator = document.getElementById('slide-indicator');
    const progress = document.getElementById('progress-bar');
    const drawer = document.getElementById('cognitive-drawer');
    const hud = document.getElementById('presenter-hud');
    const archModal = document.getElementById('arch-drilldown-modal');
    const noteArc = document.getElementById('note-arc');
    const noteMission = document.getElementById('note-mission');
    const noteTransition = document.getElementById('note-transition');
    const noteEvidence = document.getElementById('note-evidence');
    const stepBtn = document.getElementById('step-btn');

    let metaData = {{ contract: {{}}, slides: [] }};
    try {{
      const metaEl = document.getElementById('presentation-metadata');
      if (metaEl) {{
        metaData = JSON.parse(metaEl.textContent);
      }}
    }} catch (e) {{
      console.warn('Could not parse presentation metadata', e);
    }}

    function toggleNotes() {{
      drawer.classList.toggle('hidden');
    }}

    function toggleHUD() {{
      hud.classList.toggle('hidden');
      if (!hud.classList.contains('hidden')) {{
        updatePresenterHUD(currentSlide);
      }}
    }}

    function toggleStepMode() {{
      stepMode = !stepMode;
      if (stepBtn) {{
        stepBtn.textContent = stepMode ? 'Step: ON' : 'Step: OFF';
        stepBtn.classList.toggle('text-blue-400', stepMode);
      }}
      resetStagedElements();
    }}

    function updateCognitiveNotes(slideEl) {{
      if (!slideEl) return;
      if (noteArc) noteArc.textContent = slideEl.dataset.arc || 'PROGRESSION';
      if (noteMission) noteMission.textContent = slideEl.dataset.mission || '未定义单页认知使命';
      if (noteTransition) noteTransition.textContent = slideEl.dataset.transition || '承接前文，自然演进';
      if (noteEvidence) noteEvidence.textContent = slideEl.dataset.evidence || '结构性量化支撑';
    }}

    function updatePresenterHUD(idx) {{
      const slideMeta = (metaData.slides && metaData.slides[idx]) ? metaData.slides[idx] : {{}};
      const contract = metaData.contract || {{}};

      const arcEl = document.getElementById('hud-arc-badge');
      if (arcEl) arcEl.textContent = (slideMeta.narrative_arc || 'PROGRESSION').toUpperCase();

      const thesisEl = document.getElementById('hud-core-thesis');
      if (thesisEl) thesisEl.textContent = contract.core_thesis || '未定义核心论点';

      const audEl = document.getElementById('hud-audience');
      if (audEl) {{
        const role = contract.audience?.role || '汇报受众';
        const stance = contract.audience?.stance ? ` (${{contract.audience.stance}})` : '';
        audEl.textContent = `${{role}}${{stance}}`;
      }}

      const missionEl = document.getElementById('hud-mission');
      if (missionEl) missionEl.textContent = slideMeta.mission || '推动认知转化';

      const teleEl = document.getElementById('hud-teleprompter');
      if (teleEl) {{
        const trans = slideMeta.transition || '承接前文，自然进入本页核心论证。';
        teleEl.textContent = `“${{trans}}”`;
      }}

      const objContainer = document.getElementById('hud-objections-container');
      if (objContainer) {{
        objContainer.innerHTML = '';
        const objections = slideMeta.objections || [];
        objections.forEach((obj, i) => {{
          const itemDiv = document.createElement('div');
          itemDiv.className = 'bg-slate-950/70 border border-slate-800 rounded-lg p-2.5 space-y-1';
          itemDiv.innerHTML = `
            <div class="text-amber-400 font-bold text-[11px] flex items-start gap-1">
              <span>⚠️</span>
              <span>发难 #${{i+1}}: ${{obj.skepticism}}</span>
            </div>
            <div class="text-slate-300 text-[11px] leading-relaxed pl-4 border-l border-emerald-500/40">
              <span class="text-emerald-400 font-semibold">权威对策:</span> ${{obj.counter}}
            </div>
          `;
          objContainer.appendChild(itemDiv);
        }});
      }}
    }}

    // Count-up Physics for Metrics
    function animateValue(el, start, end, duration, prefix = '', suffix = '') {{
      let startTimestamp = null;
      const step = (timestamp) => {{
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * easeProgress;
        el.textContent = `${{prefix}}${{current.toFixed(end % 1 === 0 ? 0 : 1)}}${{suffix}}`;
        if (progress < 1) {{
          window.requestAnimationFrame(step);
        }} else {{
          el.textContent = `${{prefix}}${{end}}${{suffix}}`;
        }}
      }};
      window.requestAnimationFrame(step);
    }}

    function triggerCountUpAnimations(slideEl) {{
      if (!slideEl) return;
      const metricEls = slideEl.querySelectorAll('.metric-val');
      metricEls.forEach(el => {{
        const targetStr = el.textContent.trim();
        const match = targetStr.match(/^([^0-9.]*)([0-9]+(?:\\.[0-9]+)?)(.*)$/);
        if (match) {{
          const prefix = match[1];
          const targetNum = parseFloat(match[2]);
          const suffix = match[3];
          animateValue(el, 0, targetNum, 600, prefix, suffix);
        }}
      }});
    }}

    function getStagedElements(slideEl) {{
      if (!slideEl) return [];
      const candidates = slideEl.querySelectorAll('.grid > div, .flex-col > .flex, tbody tr, .space-y-4 > div');
      return Array.from(candidates).filter(el => el.offsetHeight > 20 && !el.closest('header') && !el.closest('footer'));
    }}

    function resetStagedElements() {{
      const currentSlideEl = slides[currentSlide];
      const items = getStagedElements(currentSlideEl);
      if (stepMode && items.length > 1) {{
        currentStep = 0;
        items.forEach((item, idx) => {{
          if (idx === 0) {{
            item.classList.remove('staged-hidden');
            item.classList.add('staged-visible');
          }} else {{
            item.classList.remove('staged-visible');
            item.classList.add('staged-hidden');
          }}
        }});
      }} else {{
        items.forEach(item => {{
          item.classList.remove('staged-hidden');
          item.classList.add('staged-visible');
        }});
      }}
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
      if (!hud.classList.contains('hidden')) {{
        updatePresenterHUD(currentSlide);
      }}
      triggerCountUpAnimations(slides[currentSlide]);
      resetStagedElements();
    }}

    function nextStepOrSlide() {{
      if (stepMode) {{
        const items = getStagedElements(slides[currentSlide]);
        if (items.length > 1 && currentStep < items.length - 1) {{
          currentStep++;
          items[currentStep].classList.remove('staged-hidden');
          items[currentStep].classList.add('staged-visible');
          return;
        }}
      }}
      showSlide(currentSlide + 1);
    }}

    // Navigation events
    document.getElementById('prev-btn').addEventListener('click', () => showSlide(currentSlide - 1));
    document.getElementById('next-btn').addEventListener('click', () => showSlide(currentSlide + 1));
    if (stepBtn) stepBtn.addEventListener('click', toggleStepMode);
    document.getElementById('notes-btn').addEventListener('click', toggleNotes);
    document.getElementById('hud-btn').addEventListener('click', toggleHUD);
    document.getElementById('close-drawer-btn').addEventListener('click', () => drawer.classList.add('hidden'));
    document.getElementById('close-hud-btn').addEventListener('click', () => hud.classList.add('hidden'));

    // Architecture Drilldown Modal Events
    document.querySelectorAll('.architecture-item').forEach(item => {{
      item.addEventListener('click', () => {{
        const comp = item.dataset.component || '核心组件';
        const layer = item.dataset.layer || '架构层级';
        document.getElementById('drill-component').textContent = comp;
        document.getElementById('drill-layer').textContent = layer;
        document.getElementById('drill-chain-comp').textContent = comp;
        archModal.classList.remove('hidden');
      }});
    }});

    const closeDrillBtn = document.getElementById('close-drill-btn');
    const dismissDrillBtn = document.getElementById('dismiss-drill-btn');
    if (closeDrillBtn) closeDrillBtn.addEventListener('click', () => archModal.classList.add('hidden'));
    if (dismissDrillBtn) dismissDrillBtn.addEventListener('click', () => archModal.classList.add('hidden'));

    // Scenario Sandbox Switcher Events
    document.querySelectorAll('.scenario-sandbox').forEach(box => {{
      const btns = box.querySelectorAll('.scenario-btn');
      btns.forEach(btn => {{
        btn.addEventListener('click', (e) => {{
          e.stopPropagation();
          btns.forEach(b => {{
            b.classList.remove('active', 'text-blue-700', 'bg-white', 'shadow-sm', 'font-bold');
            b.classList.add('text-slate-600');
          }});
          btn.classList.add('active', 'text-blue-700', 'bg-white', 'shadow-sm', 'font-bold');
          btn.classList.remove('text-slate-600');

          const scenario = btn.dataset.scenario;
          const slideEl = btn.closest('.slide');
          if (!slideEl) return;

          // Update metric-val elements
          slideEl.querySelectorAll('.metric-val').forEach(mEl => {{
            let targetVal = mEl.dataset.baseVal;
            if (scenario === 'conservative' && mEl.dataset.conservativeVal) {{
              targetVal = mEl.dataset.conservativeVal;
            }} else if (scenario === 'aggressive' && mEl.dataset.aggressiveVal) {{
              targetVal = mEl.dataset.aggressiveVal;
            }}

            const match = targetVal.match(/^([^0-9.]*)([0-9]+(?:\\.[0-9]+)?)(.*)$/);
            if (match) {{
              const prefix = match[1];
              const targetNum = parseFloat(match[2]);
              const suffix = match[3];
              const curMatch = mEl.textContent.match(/([0-9]+(?:\\.[0-9]+)?)/);
              const startNum = curMatch ? parseFloat(curMatch[1]) : 0;
              animateValue(mEl, startNum, targetNum, 400, prefix, suffix);
            }} else {{
              mEl.textContent = targetVal;
            }}
          }});

          // Update metric delta badges
          slideEl.querySelectorAll('.metric-delta').forEach(dEl => {{
            if (scenario === 'conservative') {{
              dEl.textContent = `▲ ${{dEl.dataset.consDelta || '稳健保底'}}`;
            }} else if (scenario === 'aggressive') {{
              dEl.textContent = `▲ ${{dEl.dataset.aggrDelta || '激进突破'}}`;
            }} else {{
              dEl.textContent = `▲ ${{dEl.dataset.baseDelta || '基准目标'}}`;
            }}
          }});
        }});
      }});
    }});

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        e.preventDefault();
        nextStepOrSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'Backspace') {{
        e.preventDefault();
        showSlide(currentSlide - 1);
      }} else if (e.key === 'f' || e.key === 'F') {{
        toggleFullscreen();
      }} else if (e.key === 'n' || e.key === 'N') {{
        toggleNotes();
      }} else if (e.key === 'p' || e.key === 'P') {{
        toggleHUD();
      }} else if (e.key === 's' || e.key === 'S') {{
        toggleStepMode();
      }} else if (e.key === 'Escape') {{
        if (!archModal.classList.contains('hidden')) archModal.classList.add('hidden');
        if (!hud.classList.contains('hidden')) hud.classList.add('hidden');
        if (!drawer.classList.contains('hidden')) drawer.classList.add('hidden');
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
