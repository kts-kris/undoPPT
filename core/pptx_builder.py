"""pptx_builder.py - High-Precision Native Vector Presentation Builder.

Transforms slides_blueprint.json and design_tokens.json into 100% editable,
pure vector PowerPoint slides using python-pptx.
Implements the 6 core Infographic Primitives:
  1. Title Cover & Section Dividers
  2. Product & Technical Architecture Stacks
  3. Bento Grid Multi-column Comparison Cards
  4. KPI Metric Spotlight Boards
  5. Process & Milestone Horizontal Timelines
  6. 2x2 Strategic Matrices & Key Takeaways
"""

import os
from typing import Any, Dict, List, Optional

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


def _hex_to_rgb(hex_str: str) -> RGBColor:
    """Convert hex string '#RRGGBB' to pptx RGBColor."""
    if not hex_str or not hex_str.startswith("#") or len(hex_str) < 7:
        return RGBColor(30, 41, 59)
    try:
        r = int(hex_str[1:3], 16)
        g = int(hex_str[3:5], 16)
        b = int(hex_str[5:7], 16)
        return RGBColor(r, g, b)
    except Exception:
        return RGBColor(30, 41, 59)


def _apply_background(slide, prs, bg_hex: str):
    """Fill slide background with a full-bleed shape or solid fill."""
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = _hex_to_rgb(bg_hex)
    bg_shape.line.fill.background()  # No border
    # Send to back if needed (in python-pptx, shapes added first are behind subsequent shapes)


def _add_header(slide, title: str, subtitle: str, tokens: Dict[str, Any], tag: Optional[str] = None):
    """Add standard structured header with tag badge, title, and subtitle."""
    typo = tokens.get("typography", {})
    palette = tokens.get("palette", {})
    canvas = tokens.get("canvas", {})

    left = Inches(canvas.get("margin_left_inches", 0.8))
    top = Inches(canvas.get("margin_top_inches", 0.7))
    width = Inches(11.7)
    height = Inches(1.3)

    # Optional Tag Badge
    if tag:
        badge_w = max(1.8, len(tag) * 0.11 + 0.4)
        tag_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(badge_w), Inches(0.32)
        )
        tag_box.fill.solid()
        tag_box.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface_subtle", "#EFF6FF"))
        tag_box.line.color.rgb = _hex_to_rgb(palette.get("secondary", "#3B82F6"))
        tag_box.line.width = Pt(1)
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.alignment = PP_ALIGN.CENTER
        run_tag = p_tag.add_run()
        run_tag.text = tag.upper()
        run_tag.font.name = typo.get("body", {}).get("font", "Arial")
        run_tag.font.size = Pt(10)
        run_tag.font.bold = True
        run_tag.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
        top += Inches(0.42)

    # Header text box
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Title
    p_title = tf.paragraphs[0]
    p_title.space_after = Pt(4)
    run_title = p_title.add_run()
    run_title.text = title
    run_title.font.name = typo.get("title", {}).get("font", "PingFang SC")
    run_title.font.size = Pt(typo.get("title", {}).get("size", 30))
    run_title.font.bold = True
    run_title.font.color.rgb = _hex_to_rgb(typo.get("title", {}).get("color", palette.get("text_primary", "#0F172A")))

    # Subtitle
    if subtitle:
        p_sub = tf.add_paragraph()
        run_sub = p_sub.add_run()
        run_sub.text = subtitle
        run_sub.font.name = typo.get("subtitle", {}).get("font", "PingFang SC")
        run_sub.font.size = Pt(typo.get("subtitle", {}).get("size", 16))
        run_sub.font.color.rgb = _hex_to_rgb(typo.get("subtitle", {}).get("color", palette.get("text_secondary", "#475569")))


def render_cover_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render Title Cover slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))

    # Decorative accent card or subtle backdrop
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.5), Inches(10.9), Inches(4.5)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface", "#FFFFFF"))
    card.line.color.rgb = _hex_to_rgb(palette.get("border", "#E2E8F0"))
    card.line.width = Pt(1.5)

    # Accent color bar on the left edge
    accent_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.5), Inches(0.18), Inches(4.5)
    )
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
    accent_bar.line.fill.background()

    # Text content box
    tb = slide.shapes.add_textbox(Inches(1.8), Inches(2.0), Inches(9.8), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True

    # Category badge
    category = slide_data.get("category", "ENTERPRISE SOLUTION ARCHITECTURE")
    p_cat = tf.paragraphs[0]
    p_cat.space_after = Pt(14)
    run_cat = p_cat.add_run()
    run_cat.text = category
    run_cat.font.name = typo.get("body", {}).get("font", "Arial")
    run_cat.font.size = Pt(12)
    run_cat.font.bold = True
    run_cat.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

    # Main Title
    p_title = tf.add_paragraph()
    p_title.space_after = Pt(12)
    run_title = p_title.add_run()
    run_title.text = slide_data.get("title", "Presentation Title")
    run_title.font.name = typo.get("title", {}).get("font", "PingFang SC")
    run_title.font.size = Pt(40)
    run_title.font.bold = True
    run_title.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#0F172A"))

    # Subtitle
    subtitle = slide_data.get("subtitle", "")
    if subtitle:
        p_sub = tf.add_paragraph()
        p_sub.space_after = Pt(28)
        run_sub = p_sub.add_run()
        run_sub.text = subtitle
        run_sub.font.name = typo.get("subtitle", {}).get("font", "PingFang SC")
        run_sub.font.size = Pt(20)
        run_sub.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))

    # Author & Date Meta
    meta = slide_data.get("meta", "undoPPT Intelligent Engine · 2026")
    p_meta = tf.add_paragraph()
    run_meta = p_meta.add_run()
    run_meta.text = meta
    run_meta.font.size = Pt(13)
    run_meta.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#64748B"))


def render_architecture_stack_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render Product / Technology Multi-Layer Stack Slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "ARCHITECTURE")
    title = slide_data.get("action_title") or slide_data.get("title", "系统架构全景")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    layers = slide_data.get("layers", [])
    if not layers:
        return

    num_layers = min(len(layers), 4)
    start_y = 2.1
    avail_height = 4.8
    gap = 0.18
    layer_height = (avail_height - (num_layers - 1) * gap) / num_layers
    margin_left = 0.8
    total_width = 11.73

    badge_width = 2.0
    items_area_left = margin_left + badge_width + 0.15
    items_area_width = total_width - badge_width - 0.15

    for idx, layer in enumerate(layers[:num_layers]):
        curr_y = start_y + idx * (layer_height + gap)

        # 1. Outer Container Box
        container = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(margin_left),
            Inches(curr_y),
            Inches(total_width),
            Inches(layer_height)
        )
        container.fill.solid()
        container.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface", "#FFFFFF"))
        container.line.color.rgb = _hex_to_rgb(palette.get("border", "#E2E8F0"))
        container.line.width = Pt(1)

        # 2. Left Layer Badge
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(margin_left + 0.1),
            Inches(curr_y + 0.1),
            Inches(badge_width),
            Inches(layer_height - 0.2)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface_subtle", "#EFF6FF"))
        badge.line.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
        badge.line.width = Pt(1)

        tf_badge = badge.text_frame
        tf_badge.word_wrap = True
        p_badge = tf_badge.paragraphs[0]
        p_badge.alignment = PP_ALIGN.CENTER
        run_b = p_badge.add_run()
        run_b.text = layer.get("name", f"层级 {idx+1}")
        run_b.font.bold = True
        run_b.font.size = Pt(14)
        run_b.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

        # Layer description under name if space allows
        desc = layer.get("desc", "")
        if desc and layer_height > 1.1:
            p_desc = tf_badge.add_paragraph()
            p_desc.alignment = PP_ALIGN.CENTER
            run_d = p_desc.add_run()
            run_d.text = desc
            run_d.font.size = Pt(10)
            run_d.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#64748B"))

        # 3. Inside Component Micro-Cards
        items = layer.get("items", [])
        if items:
            item_count = min(len(items), 5)
            item_gap = 0.12
            item_w = (items_area_width - 0.2 - (item_count - 1) * item_gap) / item_count
            item_h = layer_height - 0.25

            for c_idx, item_name in enumerate(items[:item_count]):
                item_x = items_area_left + c_idx * (item_w + item_gap)
                item_y = curr_y + 0.12
                item_card = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    Inches(item_x),
                    Inches(item_y),
                    Inches(item_w),
                    Inches(item_h)
                )
                item_card.fill.solid()
                item_card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface_subtle", "#F8FAFC"))
                item_card.line.color.rgb = _hex_to_rgb(palette.get("border", "#CBD5E1"))
                item_card.line.width = Pt(1)

                tf_item = item_card.text_frame
                tf_item.word_wrap = True
                p_item = tf_item.paragraphs[0]
                p_item.alignment = PP_ALIGN.CENTER
                run_i = p_item.add_run()
                run_i.text = item_name
                run_i.font.size = Pt(12)
                run_i.font.bold = True
                run_i.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#1E293B"))


def render_bento_cards_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render Bento Grid Multi-Column Comparison Cards."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "ANALYSIS")
    title = slide_data.get("action_title") or slide_data.get("title", "核心维度对比")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    cards = slide_data.get("cards", [])
    if not cards:
        return

    num_cards = min(len(cards), 4)
    start_x = 0.8
    start_y = 2.1
    avail_width = 11.73
    card_height = 4.7
    gap = 0.2
    card_w = (avail_width - (num_cards - 1) * gap) / num_cards

    for idx, card_data in enumerate(cards[:num_cards]):
        cx = start_x + idx * (card_w + gap)

        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(cx),
            Inches(start_y),
            Inches(card_w),
            Inches(card_height)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface", "#FFFFFF"))
        is_highlight = card_data.get("highlight", False)
        card.line.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB") if is_highlight else palette.get("border", "#E2E8F0"))
        card.line.width = Pt(2 if is_highlight else 1)

        # Card Content Box
        tb = slide.shapes.add_textbox(Inches(cx + 0.18), Inches(start_y + 0.2), Inches(card_w - 0.36), Inches(card_height - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        # Category / Number tag
        p_badge = tf.paragraphs[0]
        p_badge.space_after = Pt(8)
        run_b = p_badge.add_run()
        run_b.text = card_data.get("tag", f"DIMENSION 0{idx+1}")
        run_b.font.size = Pt(11)
        run_b.font.bold = True
        run_b.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB") if is_highlight else palette.get("text_secondary", "#64748B"))

        # Card Title
        p_title = tf.add_paragraph()
        p_title.space_after = Pt(10)
        run_t = p_title.add_run()
        run_t.text = card_data.get("title", f"方案 {idx+1}")
        run_t.font.size = Pt(18)
        run_t.font.bold = True
        run_t.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#0F172A"))

        # Main description
        desc = card_data.get("desc", "")
        if desc:
            p_desc = tf.add_paragraph()
            p_desc.space_after = Pt(12)
            run_d = p_desc.add_run()
            run_d.text = desc
            run_d.font.size = Pt(13)
            run_d.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))

        # Bullet points
        bullets = card_data.get("bullets", [])
        for bullet in bullets:
            p_bullet = tf.add_paragraph()
            p_bullet.space_after = Pt(6)
            run_bullet_dot = p_bullet.add_run()
            run_bullet_dot.text = "• "
            run_bullet_dot.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
            run_bullet_dot.font.bold = True
            run_b_text = p_bullet.add_run()
            run_b_text.text = bullet
            run_b_text.font.size = Pt(12)
            run_b_text.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#334155"))


def render_metric_spotlight_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render KPI Metric Big Numbers Spotlight Board."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "KPI DASHBOARD")
    title = slide_data.get("action_title") or slide_data.get("title", "核心业绩指标衡量")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    metrics = slide_data.get("metrics", [])
    if not metrics:
        return

    num_metrics = min(len(metrics), 4)
    start_x = 0.8
    start_y = 2.2
    avail_width = 11.73
    card_h = 4.5
    gap = 0.22
    card_w = (avail_width - (num_metrics - 1) * gap) / num_metrics

    for idx, m in enumerate(metrics[:num_metrics]):
        cx = start_x + idx * (card_w + gap)

        # Background card
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(cx),
            Inches(start_y),
            Inches(card_w),
            Inches(card_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface", "#FFFFFF"))
        card.line.color.rgb = _hex_to_rgb(palette.get("border", "#E2E8F0"))
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(Inches(cx + 0.15), Inches(start_y + 0.3), Inches(card_w - 0.3), Inches(card_h - 0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        # Metric Title / Label
        p_lbl = tf.paragraphs[0]
        p_lbl.space_after = Pt(12)
        run_l = p_lbl.add_run()
        run_l.text = m.get("label", "核心指标")
        run_l.font.size = Pt(14)
        run_l.font.bold = True
        run_l.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#64748B"))

        # Big Number
        p_num = tf.add_paragraph()
        p_num.space_after = Pt(6)
        run_n = p_num.add_run()
        run_n.text = str(m.get("value", "99.9%"))
        run_n.font.name = typo.get("kpi_number", {}).get("font", "DIN Alternate, Arial")
        run_n.font.size = Pt(typo.get("kpi_number", {}).get("size", 48))
        run_n.font.bold = True
        run_n.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

        # Delta / Growth Badge
        delta = m.get("delta", "")
        if delta:
            p_delta = tf.add_paragraph()
            p_delta.space_after = Pt(14)
            run_delta = p_delta.add_run()
            run_delta.text = f"▲ {delta}"
            run_delta.font.size = Pt(13)
            run_delta.font.bold = True
            run_delta.font.color.rgb = _hex_to_rgb("#10B981")  # Emerald Green

        # Description
        desc = m.get("desc", "")
        if desc:
            p_desc = tf.add_paragraph()
            run_d = p_desc.add_run()
            run_d.text = desc
            run_d.font.size = Pt(12)
            run_d.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))


def render_timeline_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render Process Flow & Milestone Horizontal Timeline."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "ROADMAP")
    title = slide_data.get("action_title") or slide_data.get("title", "演进路线与关键里程碑")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    steps = slide_data.get("steps", [])
    if not steps:
        return

    num_steps = min(len(steps), 4)
    start_x = 0.8
    start_y = 2.4
    avail_width = 11.73
    gap = 0.25
    step_w = (avail_width - (num_steps - 1) * gap) / num_steps

    # Horizontal connector line behind steps
    connector = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(start_x + 0.3),
        Inches(start_y + 0.4),
        Inches(avail_width - 0.6),
        Inches(0.06)
    )
    connector.fill.solid()
    connector.fill.fore_color.rgb = _hex_to_rgb(palette.get("secondary", "#93C5FD"))
    connector.line.fill.background()

    for idx, step in enumerate(steps[:num_steps]):
        cx = start_x + idx * (step_w + gap)

        # Step Node Circle
        node = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(cx + step_w / 2 - 0.4),
            Inches(start_y),
            Inches(0.8),
            Inches(0.8)
        )
        node.fill.solid()
        node.fill.fore_color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
        node.line.color.rgb = _hex_to_rgb(palette.get("surface", "#FFFFFF"))
        node.line.width = Pt(3)

        tf_node = node.text_frame
        p_n = tf_node.paragraphs[0]
        p_n.alignment = PP_ALIGN.CENTER
        run_num = p_n.add_run()
        run_num.text = f"{idx+1}"
        run_num.font.bold = True
        run_num.font.size = Pt(16)
        run_num.font.color.rgb = RGBColor(255, 255, 255)

        # Phase Card below node
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(cx),
            Inches(start_y + 1.1),
            Inches(step_w),
            Inches(3.3)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface", "#FFFFFF"))
        card.line.color.rgb = _hex_to_rgb(palette.get("border", "#E2E8F0"))
        card.line.width = Pt(1)

        tb = slide.shapes.add_textbox(Inches(cx + 0.15), Inches(start_y + 1.25), Inches(step_w - 0.3), Inches(3.0))
        tf = tb.text_frame
        tf.word_wrap = True

        # Phase Time Tag
        p_time = tf.paragraphs[0]
        p_time.space_after = Pt(6)
        run_time = p_time.add_run()
        run_time.text = step.get("time", f"阶段 Q{idx+1}")
        run_time.font.size = Pt(11)
        run_time.font.bold = True
        run_time.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

        # Step Title
        p_t = tf.add_paragraph()
        p_t.space_after = Pt(8)
        run_t = p_t.add_run()
        run_t.text = step.get("title", f"阶段目标 {idx+1}")
        run_t.font.size = Pt(16)
        run_t.font.bold = True
        run_t.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#0F172A"))

        # Deliverables
        items = step.get("items", [])
        for item in items:
            p_item = tf.add_paragraph()
            p_item.space_after = Pt(4)
            run_dot = p_item.add_run()
            run_dot.text = "✓ "
            run_dot.font.bold = True
            run_dot.font.color.rgb = _hex_to_rgb("#10B981")
            run_i = p_item.add_run()
            run_i.text = item
            run_i.font.size = Pt(12)
            run_i.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))


def render_summary_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render Conclusion & Key Takeaways Summary Slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "SUMMARY")
    title = slide_data.get("action_title") or slide_data.get("title", "核心总结与实施建议")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    points = slide_data.get("points", [])
    if not points:
        return

    num_points = min(len(points), 4)
    start_x = 0.8
    start_y = 2.1
    total_w = 11.73
    avail_h = 4.8
    gap = 0.16
    row_h = (avail_h - (num_points - 1) * gap) / num_points

    for idx, p_data in enumerate(points[:num_points]):
        curr_y = start_y + idx * (row_h + gap)

        # Row card
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(start_x),
            Inches(curr_y),
            Inches(total_w),
            Inches(row_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface", "#FFFFFF"))
        card.line.color.rgb = _hex_to_rgb(palette.get("border", "#E2E8F0"))
        card.line.width = Pt(1)

        # Number badge on left
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(start_x + 0.15),
            Inches(curr_y + 0.12),
            Inches(0.6),
            Inches(row_h - 0.24)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
        badge.line.fill.background()
        tf_b = badge.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        run_b = p_b.add_run()
        run_b.text = f"{idx+1}"
        run_b.font.bold = True
        run_b.font.size = Pt(16)
        run_b.font.color.rgb = RGBColor(255, 255, 255)

        # Text on right
        tb = slide.shapes.add_textbox(Inches(start_x + 0.9), Inches(curr_y + 0.08), Inches(total_w - 1.1), Inches(row_h - 0.16))
        tf = tb.text_frame
        tf.word_wrap = True

        p_title = tf.paragraphs[0]
        p_title.space_after = Pt(2)
        run_t = p_title.add_run()
        run_t.text = p_data.get("title", f"建议要点 {idx+1}")
        run_t.font.size = Pt(15)
        run_t.font.bold = True
        run_t.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#0F172A"))

        desc = p_data.get("desc", "")
        if desc:
            p_desc = tf.add_paragraph()
            run_d = p_desc.add_run()
            run_d.text = desc
            run_d.font.size = Pt(12)
            run_d.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))


def render_matrix_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render 2x2 Strategic Matrix with X/Y axes and 4 quadrant cards."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "STRATEGY MATRIX")
    title = slide_data.get("action_title") or slide_data.get("title", "战略决策矩阵")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    principles = slide_data.get("principles") or slide_data.get("takeaways", [])
    has_side = bool(principles)

    start_x = 1.3
    start_y = 2.1
    matrix_w = 7.6 if has_side else 10.8
    matrix_h = 4.8
    gap = 0.2
    card_w = (matrix_w - gap) / 2
    card_h = (matrix_h - gap) / 2

    x_axis = slide_data.get("x_axis", {"title": "X 轴维度", "min_label": "低/弱", "max_label": "高/强"})
    y_axis = slide_data.get("y_axis", {"title": "Y 轴维度", "min_label": "低/弱", "max_label": "高/强"})

    # Y-axis title on left
    tb_y = slide.shapes.add_textbox(Inches(0.2), Inches(start_y + card_h - 0.4), Inches(0.9), Inches(0.8))
    tf_y = tb_y.text_frame
    tf_y.word_wrap = True
    p_y = tf_y.paragraphs[0]
    p_y.alignment = PP_ALIGN.CENTER
    run_y = p_y.add_run()
    run_y.text = y_axis.get("title", "Y 轴")
    run_y.font.size = Pt(12)
    run_y.font.bold = True
    run_y.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

    # Y-axis max/min
    tb_y_max = slide.shapes.add_textbox(Inches(0.2), Inches(start_y), Inches(0.9), Inches(0.3))
    tb_y_max.text_frame.paragraphs[0].text = y_axis.get("max_label", "高")
    tb_y_max.text_frame.paragraphs[0].font.size = Pt(10)
    tb_y_max.text_frame.paragraphs[0].font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#64748B"))

    tb_y_min = slide.shapes.add_textbox(Inches(0.2), Inches(start_y + matrix_h - 0.35), Inches(0.9), Inches(0.3))
    tb_y_min.text_frame.paragraphs[0].text = y_axis.get("min_label", "低")
    tb_y_min.text_frame.paragraphs[0].font.size = Pt(10)
    tb_y_min.text_frame.paragraphs[0].font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#64748B"))

    # X-axis title at bottom
    tb_x = slide.shapes.add_textbox(Inches(start_x + matrix_w / 2 - 2.0), Inches(start_y + matrix_h + 0.05), Inches(4.0), Inches(0.35))
    tf_x = tb_x.text_frame
    p_x = tf_x.paragraphs[0]
    p_x.alignment = PP_ALIGN.CENTER
    run_x = p_x.add_run()
    run_x.text = f"{x_axis.get('min_label', '弱')} ← {x_axis.get('title', 'X 轴')} → {x_axis.get('max_label', '强')}"
    run_x.font.size = Pt(11)
    run_x.font.bold = True
    run_x.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

    quadrants = slide_data.get("quadrants", [])
    quad_coords = [
        ("top_left", start_x, start_y),
        ("top_right", start_x + card_w + gap, start_y),
        ("bottom_left", start_x, start_y + card_h + gap),
        ("bottom_right", start_x + card_w + gap, start_y + card_h + gap),
    ]

    for idx, (pos_key, qx, qy) in enumerate(quad_coords):
        q_data = {}
        if isinstance(quadrants, dict):
            q_data = quadrants.get(pos_key, {})
        elif isinstance(quadrants, list) and idx < len(quadrants):
            q_data = quadrants[idx]

        is_hl = q_data.get("highlight", False) or pos_key == "bottom_right"

        q_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(qx), Inches(qy), Inches(card_w), Inches(card_h)
        )
        q_card.fill.solid()
        q_card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface_subtle", "#EFF6FF") if is_hl else "#FFFFFF")
        q_card.line.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB") if is_hl else palette.get("border", "#CBD5E1"))
        q_card.line.width = Pt(2 if is_hl else 1)

        tf_q = q_card.text_frame
        tf_q.word_wrap = True
        tf_q.margin_left = Inches(0.18)
        tf_q.margin_top = Inches(0.18)
        tf_q.margin_right = Inches(0.18)

        p_qt = tf_q.paragraphs[0]
        p_qt.space_after = Pt(3)
        run_qt = p_qt.add_run()
        run_qt.text = q_data.get("name") or q_data.get("title", f"象限 {idx+1}")
        run_qt.font.bold = True
        run_qt.font.size = Pt(13)
        run_qt.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB") if is_hl else palette.get("text_primary", "#0F172A"))

        strategy = q_data.get("strategy") or q_data.get("desc", "")
        if strategy:
            p_qs = tf_q.add_paragraph()
            p_qs.space_after = Pt(4)
            run_qs = p_qs.add_run()
            run_qs.text = strategy
            run_qs.font.size = Pt(10)
            run_qs.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))

        items = q_data.get("items") or q_data.get("bullets", [])
        for item in items[:3]:
            p_item = tf_q.add_paragraph()
            run_item = p_item.add_run()
            run_item.text = f"•  {item}"
            run_item.font.size = Pt(10)
            run_item.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#1E293B"))

    if has_side:
        side_x = start_x + matrix_w + 0.35
        side_w = 3.2
        side_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(side_x), Inches(start_y), Inches(side_w), Inches(matrix_h)
        )
        side_card.fill.solid()
        side_card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface", "#FFFFFF"))
        side_card.line.color.rgb = _hex_to_rgb(palette.get("accent", "#F59E0B"))
        side_card.line.width = Pt(1.5)

        tf_side = side_card.text_frame
        tf_side.word_wrap = True
        tf_side.margin_left = Inches(0.18)
        tf_side.margin_top = Inches(0.2)
        tf_side.margin_right = Inches(0.18)

        p_sh = tf_side.paragraphs[0]
        p_sh.space_after = Pt(6)
        run_sh = p_sh.add_run()
        run_sh.text = slide_data.get("principles_title", "战略选择原则")
        run_sh.font.bold = True
        run_sh.font.size = Pt(13)
        run_sh.font.color.rgb = _hex_to_rgb(palette.get("accent", "#F59E0B"))

        for p_idx, p_text in enumerate(principles[:5]):
            p_p = tf_side.add_paragraph()
            p_p.space_after = Pt(4)
            run_p = p_p.add_run()
            run_p.text = f"0{p_idx+1}  {p_text}"
            run_p.font.size = Pt(10)
            run_p.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#1E293B"))


def render_ladder_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render Multi-tier Progressive Maturity Ladder."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "MATURITY LADDER")
    title = slide_data.get("action_title") or slide_data.get("title", "能力梯队成熟度模型")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    levels = slide_data.get("levels", [])
    if not levels:
        return

    num_levels = min(len(levels), 4)
    start_x = 0.8
    start_y = 2.1
    avail_w = 11.73
    gap = 0.2
    col_w = (avail_w - (num_levels - 1) * gap) / num_levels
    safety_rule = slide_data.get("safety_line") or slide_data.get("footer_rule")
    card_h = 4.2 if safety_rule else 4.8

    for idx, lvl in enumerate(levels[:num_levels]):
        curr_x = start_x + idx * (col_w + gap)
        is_high = lvl.get("highlight", False) or idx == num_levels - 1

        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(curr_x), Inches(start_y), Inches(col_w), Inches(card_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface_subtle", "#EFF6FF") if is_high else "#FFFFFF")
        card.line.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB") if is_high else palette.get("border", "#CBD5E1"))
        card.line.width = Pt(2 if is_high else 1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.16)
        tf.margin_top = Inches(0.18)
        tf.margin_right = Inches(0.16)

        # Level tag
        p_lvl = tf.paragraphs[0]
        run_lvl = p_lvl.add_run()
        run_lvl.text = lvl.get("level", f"Level {idx+1}").upper()
        run_lvl.font.bold = True
        run_lvl.font.size = Pt(11)
        run_lvl.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

        # Tier Name
        p_name = tf.add_paragraph()
        p_name.space_after = Pt(4)
        run_name = p_name.add_run()
        run_name.text = lvl.get("name") or lvl.get("title", f"阶段 {idx+1}")
        run_name.font.bold = True
        run_name.font.size = Pt(15)
        run_name.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#0F172A"))

        # Description
        desc = lvl.get("desc", "")
        if desc:
            p_desc = tf.add_paragraph()
            p_desc.space_after = Pt(6)
            run_d = p_desc.add_run()
            run_d.text = desc
            run_d.font.size = Pt(10)
            run_d.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))

        # Core Mechanism Box
        mech = lvl.get("mechanism", "")
        if mech:
            p_m = tf.add_paragraph()
            p_m.space_after = Pt(3)
            run_mh = p_m.add_run()
            run_mh.text = "核心抓手: "
            run_mh.font.bold = True
            run_mh.font.size = Pt(10)
            run_mh.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
            run_m = p_m.add_run()
            run_m.text = mech
            run_m.font.size = Pt(10)
            run_m.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#1E293B"))

        # Metric Box
        metric = lvl.get("metric", "")
        if metric:
            p_met = tf.add_paragraph()
            p_met.space_after = Pt(3)
            run_meth = p_met.add_run()
            run_meth.text = "衡量指标: "
            run_meth.font.bold = True
            run_meth.font.size = Pt(10)
            run_meth.font.color.rgb = _hex_to_rgb(palette.get("accent", "#F59E0B"))
            run_met = p_met.add_run()
            run_met.text = metric
            run_met.font.size = Pt(10)
            run_met.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#1E293B"))

        # Role tag
        roles = lvl.get("roles", "")
        if roles:
            p_r = tf.add_paragraph()
            run_rh = p_r.add_run()
            run_rh.text = "协同角色: "
            run_rh.font.bold = True
            run_rh.font.size = Pt(10)
            run_rh.font.color.rgb = _hex_to_rgb(palette.get("secondary", "#3B82F6"))
            run_r = p_r.add_run()
            run_r.text = roles
            run_r.font.size = Pt(10)
            run_r.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))

    # Spanning Safety Line / Footer Rule
    if safety_rule:
        bar_y = start_y + card_h + 0.15
        bar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(start_x), Inches(bar_y), Inches(avail_w), Inches(0.42)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface_subtle", "#EFF6FF"))
        bar.line.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
        bar.line.width = Pt(1)

        tf_bar = bar.text_frame
        p_bar = tf_bar.paragraphs[0]
        p_bar.alignment = PP_ALIGN.CENTER
        run_bar = p_bar.add_run()
        run_bar.text = f"★  {safety_rule}"
        run_bar.font.bold = True
        run_bar.font.size = Pt(11)
        run_bar.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))


def render_horizons_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render Three Horizons (H1/H2/H3) Portfolio Governance Model."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "THREE HORIZONS")
    title = slide_data.get("action_title") or slide_data.get("title", "一体两翼三道地平线分池管理")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    horizons = slide_data.get("horizons", [])
    if not horizons:
        return

    start_x = 0.8
    start_y = 2.1
    avail_w = 11.73
    summary_text = slide_data.get("summary_card") or slide_data.get("core_principle", "")

    top_offset = 0.6 if summary_text else 0.0
    if summary_text:
        s_bar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(start_x), Inches(start_y), Inches(avail_w), Inches(0.46)
        )
        s_bar.fill.solid()
        s_bar.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface_subtle", "#EFF6FF"))
        s_bar.line.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
        s_bar.line.width = Pt(1)
        p_sb = s_bar.text_frame.paragraphs[0]
        p_sb.alignment = PP_ALIGN.CENTER
        run_sb = p_sb.add_run()
        run_sb.text = f"分池管理原则: {summary_text}"
        run_sb.font.bold = True
        run_sb.font.size = Pt(11)
        run_sb.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

    num_h = min(len(horizons), 3)
    gap = 0.25
    col_w = (avail_w - (num_h - 1) * gap) / num_h
    card_h = 4.8 - top_offset
    col_y = start_y + top_offset

    colors = [
        {"bg": "#FFFFFF", "border": palette.get("primary", "#1A56DB"), "badge_bg": palette.get("primary", "#1A56DB")},
        {"bg": "#FFFFFF", "border": palette.get("secondary", "#3B82F6"), "badge_bg": palette.get("secondary", "#3B82F6")},
        {"bg": "#FFFFFF", "border": palette.get("accent", "#F59E0B"), "badge_bg": palette.get("accent", "#F59E0B")},
    ]

    for idx, h in enumerate(horizons[:num_h]):
        curr_x = start_x + idx * (col_w + gap)
        c_spec = colors[idx % len(colors)]

        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(curr_x), Inches(col_y), Inches(col_w), Inches(card_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = _hex_to_rgb(c_spec["bg"])
        card.line.color.rgb = _hex_to_rgb(c_spec["border"])
        card.line.width = Pt(2)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.2)
        tf.margin_right = Inches(0.2)

        # Horizon ID badge
        p_hid = tf.paragraphs[0]
        run_hid = p_hid.add_run()
        run_hid.text = h.get("id", f"H{idx+1}")
        run_hid.font.bold = True
        run_hid.font.size = Pt(20)
        run_hid.font.color.rgb = _hex_to_rgb(c_spec["badge_bg"])

        # Horizon Title
        p_ht = tf.add_paragraph()
        p_ht.space_after = Pt(6)
        run_ht = p_ht.add_run()
        run_ht.text = h.get("title", f"业务地平线 {idx+1}")
        run_ht.font.bold = True
        run_ht.font.size = Pt(15)
        run_ht.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#0F172A"))

        # Horizon Focus
        focus_items = h.get("focus") or h.get("items", [])
        if isinstance(focus_items, str):
            focus_items = [f.strip() for f in focus_items.split("、") if f.strip()]
        for f_item in focus_items[:4]:
            p_f = tf.add_paragraph()
            run_f = p_f.add_run()
            run_f.text = f"• {f_item}"
            run_f.font.size = Pt(11)
            run_f.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#1E293B"))

        p_sp = tf.add_paragraph()
        p_sp.space_after = Pt(4)

        # Governance model
        gov = h.get("governance", "")
        if gov:
            p_gov = tf.add_paragraph()
            p_gov.space_after = Pt(2)
            run_gh = p_gov.add_run()
            run_gh.text = "管理方式: "
            run_gh.font.bold = True
            run_gh.font.size = Pt(10)
            run_gh.font.color.rgb = _hex_to_rgb(c_spec["badge_bg"])
            run_g = p_gov.add_run()
            run_g.text = gov
            run_g.font.size = Pt(10)
            run_g.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#1E293B"))

        # Metric
        metric = h.get("metric", "")
        if metric:
            p_met = tf.add_paragraph()
            p_met.space_after = Pt(2)
            run_mh = p_met.add_run()
            run_mh.text = "考核标准: "
            run_mh.font.bold = True
            run_mh.font.size = Pt(10)
            run_mh.font.color.rgb = _hex_to_rgb(c_spec["badge_bg"])
            run_m = p_met.add_run()
            run_m.text = metric
            run_m.font.size = Pt(10)
            run_m.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#1E293B"))

        # Risk Profile
        risk = h.get("risk_profile", "")
        if risk:
            p_r = tf.add_paragraph()
            run_rh = p_r.add_run()
            run_rh.text = "风险定位: "
            run_rh.font.bold = True
            run_rh.font.size = Pt(10)
            run_rh.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#64748B"))
            run_r = p_r.add_run()
            run_r.text = risk
            run_r.font.size = Pt(10)
            run_r.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#64748B"))


def render_cross_mapping_slide(prs, slide_data: Dict[str, Any], tokens: Dict[str, Any]):
    """Render Cross-Organization / Cross-Tier Strategic Alignment Mapping Table."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    palette = tokens.get("palette", {})
    typo = tokens.get("typography", {})

    _apply_background(slide, prs, palette.get("background", "#F8FAFC"))
    tag = slide_data.get("tag") or (slide_data.get("narrative_arc", "").upper() if slide_data.get("narrative_arc") else "CROSS MAPPING")
    title = slide_data.get("action_title") or slide_data.get("title", "四层协同组织映射全景")
    _add_header(slide, title, slide_data.get("subtitle", ""), tokens, tag=tag)

    rows = slide_data.get("mapping_rows") or slide_data.get("rows", [])
    if not rows:
        return

    num_rows = min(len(rows), 4)
    start_x = 0.8
    start_y = 2.1
    avail_w = 11.73
    avail_h = 4.8
    gap = 0.15
    row_h = (avail_h - (num_rows - 1) * gap) / num_rows

    tier_w = 1.8
    src_w = 4.3
    arrow_w = 0.5
    tgt_w = avail_w - tier_w - src_w - arrow_w - 0.3

    for idx, r in enumerate(rows[:num_rows]):
        curr_y = start_y + idx * (row_h + gap)

        # 1. Tier Badge
        t_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(start_x), Inches(curr_y), Inches(tier_w), Inches(row_h)
        )
        t_card.fill.solid()
        t_card.fill.fore_color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
        t_card.line.fill.background()
        tf_t = t_card.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.alignment = PP_ALIGN.CENTER
        run_t = p_t.add_run()
        run_t.text = r.get("tier", f"层级 0{idx+1}")
        run_t.font.bold = True
        run_t.font.size = Pt(13)
        run_t.font.color.rgb = RGBColor(255, 255, 255)

        # 2. Source Card
        sx = start_x + tier_w + 0.1
        s_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(sx), Inches(curr_y), Inches(src_w), Inches(row_h)
        )
        s_card.fill.solid()
        s_card.fill.fore_color.rgb = _hex_to_rgb(palette.get("surface_subtle", "#F8FAFC"))
        s_card.line.color.rgb = _hex_to_rgb(palette.get("border", "#E2E8F0"))
        s_card.line.width = Pt(1)

        tf_s = s_card.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = Inches(0.15)
        tf_s.margin_top = Inches(0.12)
        p_st = tf_s.paragraphs[0]
        run_st = p_st.add_run()
        run_st.text = r.get("source_role") or r.get("source_title", "标杆实践")
        run_st.font.bold = True
        run_st.font.size = Pt(12)
        run_st.font.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))

        s_desc = r.get("source_desc", "")
        if s_desc:
            p_sd = tf_s.add_paragraph()
            run_sd = p_sd.add_run()
            run_sd.text = s_desc
            run_sd.font.size = Pt(10)
            run_sd.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#64748B"))

        # 3. Middle Arrow
        ax = sx + src_w + 0.05
        tb_a = slide.shapes.add_textbox(Inches(ax), Inches(curr_y + row_h / 2 - 0.25), Inches(arrow_w), Inches(0.5))
        p_a = tb_a.text_frame.paragraphs[0]
        p_a.alignment = PP_ALIGN.CENTER
        run_a = p_a.add_run()
        run_a.text = "➔"
        run_a.font.bold = True
        run_a.font.size = Pt(16)
        run_a.font.color.rgb = _hex_to_rgb(palette.get("accent", "#F59E0B"))

        # 4. Target Card
        tx = ax + arrow_w + 0.05
        t_card_tgt = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(tx), Inches(curr_y), Inches(tgt_w), Inches(row_h)
        )
        t_card_tgt.fill.solid()
        t_card_tgt.fill.fore_color.rgb = _hex_to_rgb("#FFFFFF")
        t_card_tgt.line.color.rgb = _hex_to_rgb(palette.get("primary", "#1A56DB"))
        t_card_tgt.line.width = Pt(1.5)

        tf_tgt = t_card_tgt.text_frame
        tf_tgt.word_wrap = True
        tf_tgt.margin_left = Inches(0.15)
        tf_tgt.margin_top = Inches(0.12)
        p_tt = tf_tgt.paragraphs[0]
        run_tt = p_tt.add_run()
        run_tt.text = r.get("target_role") or r.get("target_title", "企业落地")
        run_tt.font.bold = True
        run_tt.font.size = Pt(12)
        run_tt.font.color.rgb = _hex_to_rgb(palette.get("text_primary", "#0F172A"))

        t_desc = r.get("target_desc", "")
        if t_desc:
            p_td = tf_tgt.add_paragraph()
            run_td = p_td.add_run()
            run_td.text = t_desc
            run_td.font.size = Pt(10)
            run_td.font.color.rgb = _hex_to_rgb(palette.get("text_secondary", "#475569"))


RENDERERS = {
    "cover": render_cover_slide,
    "architecture_stack": render_architecture_stack_slide,
    "bento_cards": render_bento_cards_slide,
    "metric_spotlight": render_metric_spotlight_slide,
    "timeline": render_timeline_slide,
    "summary": render_summary_slide,
    "matrix_2x2": render_matrix_slide,
    "matrix": render_matrix_slide,
    "maturity_ladder": render_ladder_slide,
    "ladder": render_ladder_slide,
    "horizons_curve": render_horizons_slide,
    "horizons": render_horizons_slide,
    "three_horizons": render_horizons_slide,
    "cross_mapping": render_cross_mapping_slide,
    "dual_mapping": render_cross_mapping_slide,
}


def _inject_cognitive_notes(slide, slide_data: Dict[str, Any], contract: Optional[Dict[str, Any]] = None):
    """Inject cognitive metadata into native PowerPoint speaker notes."""
    notes_lines = []

    # If first slide and contract exists, record Cognitive Contract
    if contract:
        notes_lines.append("【认知契约 / Cognitive Contract】")
        if contract.get("core_thesis"):
            notes_lines.append(f"• 核心主旨: {contract.get('core_thesis')}")
        aud = contract.get("audience", {})
        if aud:
            role = aud.get("role", "")
            stance = aud.get("stance", "")
            notes_lines.append(f"• 目标受众: {role} ({stance})" if stance else f"• 目标受众: {role}")
        delta = contract.get("knowledge_delta", {})
        if delta.get("blindspots_and_pains"):
            pains = ", ".join(delta["blindspots_and_pains"]) if isinstance(delta["blindspots_and_pains"], list) else delta["blindspots_and_pains"]
            notes_lines.append(f"• 认知差/痛点: {pains}")
        outcomes = contract.get("target_outcomes", {})
        if outcomes.get("act"):
            notes_lines.append(f"• 目标行动(Act): {outcomes.get('act')}")
        notes_lines.append("-" * 36)

    narrative_arc = slide_data.get("narrative_arc")
    mission = slide_data.get("mission")
    transition = slide_data.get("transition")
    core_evidence = slide_data.get("core_evidence")
    notes_custom = slide_data.get("notes") or slide_data.get("speaker_notes")

    if narrative_arc:
        notes_lines.append(f"【叙事阶段 / Arc】{str(narrative_arc).upper()}")
    if mission:
        notes_lines.append(f"【单页使命 / Mission】{mission}")
    if transition:
        notes_lines.append(f"【承上启下 / Transition】{transition}")
    if core_evidence:
        notes_lines.append(f"【核心论据 / Evidence】{core_evidence}")
    if notes_custom:
        notes_lines.append(f"【演讲备注 / Notes】\n{notes_custom}")

    if notes_lines:
        try:
            notes_slide = slide.notes_slide
            tf = notes_slide.notes_text_frame
            tf.text = "\n".join(notes_lines)
        except Exception:
            pass


def build_presentation(blueprint: Any, tokens: Dict[str, Any], output_path: str) -> str:
    """Compile blueprint into a clean vector PowerPoint presentation."""
    prs = Presentation()
    # 16:9 standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    contract = None
    slides = []
    if isinstance(blueprint, dict):
        contract = blueprint.get("contract")
        slides = blueprint.get("slides", [])
    elif isinstance(blueprint, list):
        slides = blueprint

    for idx, slide_data in enumerate(slides):
        layout_type = slide_data.get("layout_type", "bento_cards")
        renderer = RENDERERS.get(layout_type, render_bento_cards_slide)
        renderer(prs, slide_data, tokens)

        current_slide = prs.slides[-1]
        slide_contract = contract if idx == 0 else None
        _inject_cognitive_notes(current_slide, slide_data, contract=slide_contract)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    prs.save(output_path)
    return output_path
