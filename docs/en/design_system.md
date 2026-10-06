# Design System: Tokens, Contrast and Typography (v3.8)

> English | [简体中文](../zh/design_system.md)

A deck takes its look from a **design tokens** file: one of the four presets in `presets/`, or the output of `cli.py undo` on a real template. This page says what the tokens contain and what the engine guarantees whatever they say.

## Token fields

| Field | Meaning |
| :--- | :--- |
| `theme_mode` | `light` or `dark` |
| `palette.background / surface / surface_subtle / border` | the slide, a card, a quiet card, a card outline |
| `palette.text_primary / text_secondary` | body and supporting text |
| `palette.primary / secondary / accent` | brand colours (fills, badges, chart series) |
| `typography.title / subtitle / body / kpi_number` | `font`, `size`, `color` |
| `typography.font_ea` | East Asian font for Chinese/Japanese text (from the theme, else PingFang SC) |
| `card_style.border_radius` | corner radius in px (96 px = 1 inch) |
| `canvas.margin_left_inches / margin_top_inches` | clamped to 0.8in by `undo`; the header never uses more than 1.0in |
| `theme_source` | what `undo` read: scheme name, master background, theme fonts |
| `design_notes` | fixes the design check made |

## Guarantees

1. **Contrast.** Every text run reaches 4.5:1 against the fill behind it (3:1 for text of 18pt, or 14pt bold, and up). A colour that falls short is nudged toward black or white, keeping its hue. Fills are never changed, so a brand colour used as a badge or table header stays exactly as supplied, and the text on it switches to white or near-black as needed.
2. **Size floor.** Text under 12pt is raised to 12pt where the card has room, and left alone where it does not (the layout lint then reports an overflow rather than the text silently shrinking).
3. **One-line header.** The title shrinks (to 22pt) until it fits one line; template sizes above 34pt (title) and 18pt (subtitle) are capped to the header height the grid reserves.
4. **Heavy fonts.** A font that is already heavy (Impact, Haettenschweiler, anything named Black or Heavy) is not faux-bolded.

## Checking tokens

```python
from core.design_check import check_tokens, repair_tokens
findings = check_tokens(tokens)          # TOKEN_LOW_CONTRAST, TOKEN_SIZE_TOO_SMALL, TOKEN_WEAK_HIERARCHY
fixed, notes = repair_tokens(tokens)     # same hue, lightness moved; sizes raised; input untouched
```

`palette.primary` is not checked as text: it is a brand colour used mostly as a fill, and the layout pass repairs the individual runs that use it as text.

## Bringing a corporate template

```bash
python3 cli.py undo --template company.pptx --out .undoppt/design_tokens.json
python3 cli.py build --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json
python3 cli.py render-check --pptx output/presentation.pptx --render
```

What carries over: palette, light/dark mode, fonts (including the East Asian font). What does not: the template's slide masters, background artwork and logos are not placed on the generated slides (the builders draw their own 16:9 layouts), and a 4:3 template is rendered 16:9.
