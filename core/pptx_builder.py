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
        tag_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(1.8), Inches(0.32)
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
    _add_header(slide, slide_data.get("title", "系统架构全景"), slide_data.get("subtitle", ""), tokens, tag="ARCHITECTURE")

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
    _add_header(slide, slide_data.get("title", "核心维度对比"), slide_data.get("subtitle", ""), tokens, tag="ANALYSIS")

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
    _add_header(slide, slide_data.get("title", "核心业绩指标衡量"), slide_data.get("subtitle", ""), tokens, tag="KPI DASHBOARD")

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
    _add_header(slide, slide_data.get("title", "演进路线与关键里程碑"), slide_data.get("subtitle", ""), tokens, tag="ROADMAP")

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
    _add_header(slide, slide_data.get("title", "核心总结与实施建议"), slide_data.get("subtitle", ""), tokens, tag="SUMMARY")

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


RENDERERS = {
    "cover": render_cover_slide,
    "architecture_stack": render_architecture_stack_slide,
    "bento_cards": render_bento_cards_slide,
    "metric_spotlight": render_metric_spotlight_slide,
    "timeline": render_timeline_slide,
    "summary": render_summary_slide,
}


def build_presentation(blueprint: List[Dict[str, Any]], tokens: Dict[str, Any], output_path: str) -> str:
    """Compile blueprint into a clean vector PowerPoint presentation."""
    prs = Presentation()
    # 16:9 standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    for slide_data in blueprint:
        layout_type = slide_data.get("layout_type", "bento_cards")
        renderer = RENDERERS.get(layout_type, render_bento_cards_slide)
        renderer(prs, slide_data, tokens)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    prs.save(output_path)
    return output_path
