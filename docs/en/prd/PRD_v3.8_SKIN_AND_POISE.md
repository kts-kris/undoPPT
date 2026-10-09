# undoPPT v3.8.0 Product Requirements Document (PRD)
## Skin & Poise: Read Real Templates, Guarantee Contrast, Make Animation Honest

> English | [简体中文](../../PRD_v3.8_SKIN_AND_POISE.md)

---

## 1. Document Metadata

* **Product**: undoPPT (presentation deconstruction and reconstruction agent)
* **Version**: v3.8.0
* **Written**: 2026-10-06
* **Status**: Released / in production
* **Core goals**:
  1. Make `undo` **actually read the template's** colours, light/dark mode and fonts instead of falling back to defaults;
  2. Make **contrast and type size** a guarantee of the engine, whether the tokens come from a preset or a real template;
  3. Make animation **recognised and played by PowerPoint**, reduced to three narrative types, **off by default**;
  4. Use PowerPoint itself as the verifier instead of marking our own homework;
  5. 100% backward compatible: existing blueprints, token files and `motion_pace: "staged"` keep working.

---

## 2. Background and Problem Analysis

Before v3.8, three promises in the README were checked against real PowerPoint output. None held:

| # | Promise | Measured |
|---|---|---|
| 1 | "Deep master reverse-engineering: extract colours and light/dark theme" | With three Office themes built into PowerPoint (Dark Gradient, Parcel, Editorial; one is dark) as templates, `undo` returned **identical** tokens for all three: LIGHT mode, primary `#1A56DB`, background `#F8FAFC` |
| 2 | "Native `<p:timing>` click-step animation" | PowerPoint was asked how many animation objects it recognised: **0** for the v3.4 demo, against 2/2 for a hand-written control file in PowerPoint's own format |
| 3 | Four presets with readable colours | Rendered, success green `#10B981` is only 2.54:1 on white; the decision page of the dark preset used hard-coded light cards with light text and was nearly unreadable; white text on a light primary was 2.14:1 |

What the three share: **nobody had checked them in a real viewer**.

Root causes:
1. `undo` only scanned RGB values written explicitly on slides; a real template's colours live in `theme1.xml` and its slides are empty placeholders;
2. The animation XML used `delay="0"` for click steps (should be `indefinite`) and lacked `presetID` / `clickEffect` / `bldLst`;
3. About 25 hard-coded colours were scattered through the renderers, with no contrast check.

---

## 3. Requirements

### 3.1 Real theme reading (`core/theme_reader.py`, `core/undo_engine.py`)
- **R1** Read the colour scheme (dk1/lt1/dk2/lt2/accent1-6), the master colour map (bg1/tx1/bg2/tx2) and the master background (`solidFill` or `bgRef`, resolving `schemeClr` with `lumMod`/`lumOff`/`tint`/`shade`).
- **R2** Read theme fonts: major/minor Latin and East Asian fonts (`ea` or `Hans`/`Hant`/`Jpan`).
- **R3** Token source priority: theme > slide scan (fallback). `theme_source` records what was read.
- **R4** Light/dark is decided from the resolved real background colour; the brand primary is `accent1` and is never rewritten.
- **R5** Page margins are clamped to what the builder grid can use (≤0.8in); the header does not depend on the template's page width or large font sizes.
- **R6** Extracted tokens pass the design check; repairs are recorded in `design_notes`.

### 3.2 Contrast and type size (`core/contrast.py`, `core/design_check.py`, `core/layout_fit.py`)
- **R7** Contrast standard: 4.5:1 for body text, 3:1 for large text (≥18pt, or ≥14pt bold).
- **R8** Repair at render time: every run is checked against the **fill actually behind it**; if it fails, it is moved toward black/white along its own hue until it just passes. **Fills are never changed**: brand-coloured badges and table heads stay as they are, and the text on them switches to white or near-black.
- **R9** The static lint gains `LOW_CONTRAST`.
- **R10** Token validation: text colour against its background; minimum sizes (title 28, subtitle 16, body 12, KPI 40); hierarchy (title ≥ 1.5× body). `check_tokens` reports, `repair_tokens` repairs (without mutating its argument).
- **R11** `palette.primary` is not validated as a text colour (it is mainly a fill); R8 repairs it per run.
- **R12** Light fills still hard-coded in the renderers now read from the palette, so dark presets are self-consistent.
- **R13** Fonts that are already very heavy (Impact, Haettenschweiler, *Black/Heavy*) no longer get synthetic bold on top.

### 3.3 Narrative animation (`core/motion.py`)
- **R14** Three types: `reveal` (items appear one by one), `contrast` (before/after), `build` (data builds up). **Off by default.**
- **R15** Switches: `build --motion narrative`, `presentation_config.motion`, per-slide `motion: {"type": ...}`; `off` forces it off; `motion_pace: "staged"` and `{"staged_reveal": true}` remain aliases.
- **R16** The timing tree follows PowerPoint's own writing exactly: the outer click step has `delay="indefinite"`, the first effect is `clickEffect`, the rest of the group are `withEffect`, with `presetID`/`presetClass`/`grpId` and `bldLst`.
- **R17** Grouping: shapes are clustered by horizontal **centre line** (a roadmap node and its card appear together); arrows and badges join their step; headers, footers, badges and connectors do not animate; a single-step slide gets no animation.
- **R18** `validate_timing` checks structure; `render-check --render` asks PowerPoint how many animation objects it recognised and reports `MOTION_NOT_RECOGNIZED` / `MOTION_INVALID` on a mismatch.
- **R19** Decorative HTML effects (number count-up and shimmer on entering a slide) run only in narrative mode.

---

## 4. Acceptance Criteria

| Criterion | Result |
|---|---|
| All tests pass | 144 passed plus 1 PowerPoint integration test (`UNDOPPT_TEST_POWERPOINT=1`, passed). 105 existing + 39 new |
| `undo` on three real themes | Three different token sets: dark (`#0B0C12`, primary `#4970FF`), warm (`#F2F2F2`, primary `#F6A21D`), red (`#F7F6F3`, primary `#C8350F`); v3.7 gave identical ones |
| Brand colour | `palette.primary` keeps the template's value (`#F6A21D` was not turned brown) |
| 4 presets × demo | 0 `LOW_CONTRAST` findings (2 / 3 / 2 / 6 before repair); preset tokens all pass `check_tokens` (`enterprise_architecture` was fixed from 4.4995:1) |
| Real-template tokens × demo | 0 static lint findings; PowerPoint renders three distinct, readable looks |
| Header robustness to templates | Lint still 0 with tokens at title 48pt / subtitle 26pt / margin 2.0in |
| Animation: PowerPoint recognition | Per-slide recognised counts match the file for the demo (0/6/18/8/2/0/12/9); all 72 slides of the 12 enterprise scenarios match; the old v3.4 tree gives 0 |
| Animation: default | No timing tree unless asked; HTML `data-motion="off"` |
| Animation: structure | Click step `delay="indefinite"`; first effect `clickEffect`; the validator catches the v3.4 pattern |
| Mutation check | Changing a click step back to `delay="0"` makes `validate_timing` fail |

---

## 5. Out of Scope and Known Limits

- **Template fidelity is limited.** Colours, light/dark mode and fonts carry over; a template's master layouts, background art and logos are **not** placed on generated pages (the builder draws its own 16:9 layouts), and a 4:3 template is output as 16:9. This is the biggest remaining gap.
- **The "real templates" are Microsoft's built-in themes, not corporate ones.** No corporate template was available on the test machine. These themes have real masters and palettes, enough to expose `undo`'s defects, but they do not prove behaviour on a complex corporate master.
- **Keynote was not verified.** Scripting could not make Keynote open the file, and Keynote does not expose builds to automation. Playback outside PowerPoint is not promised.
- **HTML does not follow dark presets.** It takes the brand colour and fonts from the tokens, but the outer frame and card backgrounds are fixed light.
- Text measurement is still heuristic; the real render is the final authority.

---

## 6. Roadmap Status

The plans for v3.5 (skin floor) → v3.6 (skeleton) → v3.7 (flesh) → v3.8 (skin polish and poise) are all done. Worthwhile next steps, in order of value:

1. Carry a template's master layouts, background art and logos onto generated pages;
2. Make HTML follow dark presets;
3. Trial runs with real corporate templates (needs the user to supply them);
4. Animation verification in Keynote / WPS.
