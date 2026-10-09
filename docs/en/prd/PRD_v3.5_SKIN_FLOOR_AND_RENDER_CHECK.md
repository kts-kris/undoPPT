# undoPPT v3.5.0 Product Requirements Document (PRD)
## Skin Floor & Render Check Loop

> English | [简体中文](../../PRD_v3.5_SKIN_FLOOR_AND_RENDER_CHECK.md)

> **Later changes**: the font-size floor in R3 was narrowed in v3.7 (only runs under 12pt are raised; titles are untouched; short labels may not wrap), see the [v3.7 PRD](PRD_v3.7_FLESH_PROVENANCE_AND_INGEST.md). In §6, the "Keynote" verification planned for v3.8 was not achieved; see the [v3.8 PRD](PRD_v3.8_SKIN_AND_POISE.md).

---

## 1. Document Metadata

* **Product**: undoPPT (presentation deconstruction and reconstruction agent)
* **Version**: v3.5.0
* **Written**: 2026-10-06
* **Status**: Released / in production
* **Core goals**:
  1. First make the output **not wrong**: titles do not wrap onto content, cards leave no voids, text is readable, narrow HTML screens do not clip;
  2. Let the engine **find its own mistakes**: add a static layout lint and a real render check, bringing "audit scores 94 but opens broken" into the quality loop;
  3. Deliver "zero dependencies, double-click to use": remove the HTML's CDN dependency;
  4. 100% backward compatible: no existing blueprint field changes; only aliases and optional behaviour are added.

---

## 2. Background and Problem Analysis

The design philosophy splits a deck into four layers: **skeleton** (theme and outline), **flesh** (content), **skin** (style), **poise** (animation). v3.4 put much work into skeleton and flesh but had no way to verify the skin: the auditor reads only blueprint JSON and cannot see the rendered result.

Before v3.5, the v3.4 demo was rendered in PowerPoint and Chrome, with these findings:

| # | Symptom | Root cause |
|---|---|---|
| 1 | On 5 of 8 slides the title wraps to two lines, covering the cards below; the subtitle is hidden by the cards | Title fixed at 34pt, header text box height hard-coded, content start hard-coded |
| 2 | Cards with large empty areas; in HTML cards stretched to fill the page | PPTX card height was independent of content; HTML content area used `flex-1` |
| 3 | 64% of text on the decision closing page is under 11pt, 61% on the maturity ladder, 50% on the 2x2 matrix | Each renderer hard-coded its own small sizes |
| 4 | Tall cards were pill-shaped | python-pptx's default corner radius is 1/6 of the short side |
| 5 | QBR / OKR / headcount decks had blank pages | The planner emitted `kpi_dashboard`, which neither builder had; it silently fell back to an empty bento |
| 6 | Charts used PowerPoint's default blue/red/green | Not coloured from the theme |
| 7 | Font names written as `"PingFang SC, Inter, sans-serif"` | PowerPoint cannot resolve CSS font stacks |
| 8 | HTML unstyled offline | Depended on `cdn.tailwindcss.com` and Google Fonts, against the "zero dependencies" promise |
| 9 | HTML content clipped on narrow screens | Fixed canvas ratio, internal font sizes did not scale |

---

## 3. Requirements

### 3.1 Content-adaptive layout (`core/layout_fit.py`)
- **R1 Title fit**: shrink the title within [22pt, token size] to one line; if it still does not fit, wrap and remove the subtitle from the page (it stays in notes/HTML), never covering content.
- **R2 Corner radius**: use the token `card_style.border_radius` instead of the default ratio.
- **R3 Font-size floor**: text under 12pt in any text box is enlarged together (at most 1.4×); if the estimated height then exceeds its card, fall back. Ellipses and other odd shapes are exempt.
- **R4 Card fit**: cards shrink to their text height (cards in a row stay equal); if the text is too sparse it is enlarged first (at most 1.3×). Covers both structures: "text box on top of a card" and "text inside the card".
- **R5 Vertical centring**: the content block is centred in the space below the header (shift limit 1.3 in).
- **R6 Fonts**: take the first name of the font stack and write it to both latin and east-asian.
- **R7 Charts**: series colours from the palette; light grid lines; data labels when categories × series ≤ 16; table font size adapts to row count.

### 3.2 Render verification (`cli.py render-check`)
- **R8 Static lint** (no renderer needed): `OUT_OF_BOUNDS`, `TITLE_WRAPS`, `TEXT_OVERFLOW`, `TEXT_CROSSES_SHAPE`, `TEXT_OVERLAP`. It reports 19 findings on the v3.4 demo and 0 on v3.5.
- **R9 Real render** (`--render`): PPTX goes through PowerPoint (macOS) or LibreOffice to PDF and then PNG, checking for blank bands `BLANK_BAND` (threshold 35%); HTML is loaded in headless Chrome at 1600×900 and 500×900 to read how far content overflows.
- **R10** `build` runs the static lint automatically and prints non-fatal warnings.
- **R11** Without a renderer, it degrades to the static lint only, without error.

### 3.3 HTML
- **R12 Offline**: inline the Tailwind runtime (`core/vendor/`, MIT) and remove the Google Fonts import.
- **R13 Fixed canvas**: a 1340×754 canvas scales proportionally to the viewport.
- **R14 Density fit**: the body area grows by up to 1.4× to use the height left below the header, falling back if it overflows.
- **R15** `?slide=N` deep links; `?static=1` freezes animation and reports layout (for the checker).

### 3.4 Defect fixes
- **R16** `kpi_dashboard` is an alias of `metric_spotlight`; an unknown `layout_type` warns instead of silently falling back.
- **R17** Version numbers, docs and preset references aligned; `output/` artefacts are no longer committed.

---

## 4. Acceptance Criteria

| Criterion | Result |
|---|---|
| All tests pass | 44 (23 existing + 21 new) |
| Demo: PPTX static lint | 0 findings (19 in v3.4) |
| Demo: real PowerPoint render | all 8 titles on one line, no overlap |
| One PPTX for each of the 12 enterprise scenarios | 0 static lint findings in total; PowerPoint blank bands all ≤ 35% |
| Share of text under 11pt (12 scenarios combined) | < 8% (64% on v3.4 decision pages) |
| HTML works offline | no external `src` / `href` / `@import` |
| HTML at desktop and 500px narrow | no overflow on all 8 slides |
| Reverse check | a deliberately overloaded page is reported by both the lint and the HTML check |

---

## 5. Out of Scope and Known Limits

- Text measurement is heuristic (CJK 1 em, Latin about 0.55 em); the real render is the final authority.
- A page whose content is itself too thin (three short lines) triggers `BLANK_BAND`; that is a **content problem** rather than a layout problem and is handled by v3.6's `EVIDENCE_BUDGET`.
- The planner misclassified "internal tech talk" prompts as `general_informative`; left to v3.6.
- Animation and aesthetic polish are out of scope here; left to v3.8.

---

## 6. Follow-up Roadmap

| Version | Theme | Highlights |
|---|---|---|
| v3.6.0 | Skeleton | Per-scenario questions to ask; model outlines for the 12 scenarios; `EVIDENCE_BUDGET` flesh pre-check; planner demoted to fallback and reviewer |
| v3.7.0 | Flesh | Optional `source` / `status` in the blueprint; unsourced figures marked "to verify"; `cli.py ingest`; demo shows the decision loop |
| v3.8.0 | Skin polish and poise | Type hierarchy and contrast rules; trial with real corporate templates; three narrative animations verified in PowerPoint / Keynote |
