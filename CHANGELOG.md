# CHANGELOG

All notable changes to the `undoPPT` Super Skill and Engine are documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-09-11

### Added
- **10-Dimension Cognitive Content Architecture**:
  - Integrated the 10 essential questions determining presentation quality directly into data schemas, agent SOP, and rendering compilers.
  - **Cognitive Contract Schema**: Q1 (Core Thesis), Q2 (Audience Profile & Stance), Q3 (Knowledge Delta & Pain Points), Q4 (Understand-Believe-Act Closure).
  - **Narrative Dynamics**: Q5 (Narrative Arc: Hook → Conflict → Breakthrough → Evidence → Call to Action), Q10 (Inter-slide rhetorical transitions and causal connectors).
  - **Slide-Level Precision**: Q6 (Single Slide Mission), Q7 (Content Density Budget enforcement), Q8 (Action Titles priority), Q9 (Weight of Evidence: core proof vs footnotes).
- **Automated Content Quality Auditor (`core/content_auditor.py`)**:
  - Rule-based cognitive auditor evaluating blueprint coherence, information density thresholds, passive title detection, and causal transitions.
  - New CLI command: `python3 cli.py audit --blueprint <blueprint.json>`.
- **PowerPoint Native Speaker Notes Injection (`core/pptx_builder.py`)**:
  - Automatically compiles slide mission, transition connectors, and core evidence into native PowerPoint notes (`notes_slide`) for presenter assistance.
- **Interactive Cognitive Inspector Drawer in Standalone HTML (`core/html_builder.py`)**:
  - Toggleable via keyboard `N` key or presenter bar button, displaying real-time slide mission, narrative arc, transition logic, and evidence breakdown.
- **Design Tokens Content Density Budgets (`presets/*.json`)**:
  - Added `content_budget` parameters (`density_tier`, `max_cards`, `max_title_words`, `max_desc_words`) across all 4 presets.
- **Expanded Test Suite (`tests/test_engine.py`)**:
  - Added unit tests for ContentAuditor, Speaker Notes injection, and HTML Cognitive Drawer (7/7 passing).

### Changed
- Upgraded `DEMO_BLUEPRINT` in `cli.py` to showcase full Cognitive Contract and 10-dimension slide metadata.
- Updated Skill principles and 5-stage SOP in `SKILL.md` (Principle 1 & 2 enhanced with cognitive contract & narrative dynamics).
- Synchronized `SKILL.md` across workspace root, `.agents/skills/undo-ppt/`, and `~/.gemini/config/skills/undo-ppt/`.
- Bumped version to `1.1.0` across `core/__init__.py`, `cli.py`, `README.md`, and `SKILL.md`.

---

## [1.0.0] - 2026-09-11

### Added
- **Information Sufficiency Probe (Rhythm A)**: Multi-turn proactive discovery mechanism ensuring depth, business metrics, and structural clarity prior to drafting.
- **Dual-Mode Undo Engine (`core/undo_engine.py`)**:
  - Mode A: Direct AST extraction of Slide Masters, layouts, color schemes, font ladders, and safe margins from user `.pptx` templates.
  - Mode B: Visual heuristic standardization (`core/vision_extractor.py`) for non-standard slides and style references.
- **6 Infographic Primitives (`core/pptx_builder.py`)**:
  - `cover`: Structured title hero card.
  - `architecture_stack`: Multi-layer system containers with micro-service cards.
  - `bento_cards`: 2, 3, 4-column Bento Grid comparison cards.
  - `metric_spotlight`: High-impact KPI dashboard with delta badges.
  - `timeline`: Horizontal milestone pipeline with status nodes.
  - `summary`: Numbered strategic takeaway cards.
- **Single-File Standalone HTML Compiler (`core/html_builder.py`)**:
  - Fully inlined, zero-dependency, double-click to present.
  - Keyboard navigation (Left/Right, Space, F for fullscreen).
  - Responsive 16:9 canvas with progress bar.
- **Turn-by-Turn Sync Watcher (`core/sync_watcher.py`)**:
  - Sub-10ms SHA-256 fingerprint check.
  - Semantic AST diff engine detecting modified titles, text paragraphs, and shape counts.
  - Automatic synchronization with user local modifications in PowerPoint / Keynote.
- **4 Industrial Preset Design Tokens (`presets/`)**:
  - `modern_bento.json`: Modern B2B business card grid.
  - `consulting_minimalist.json`: High-contrast strategy consulting.
  - `tech_keynote.json`: Immersive dark-mode developer summit.
  - `enterprise_architecture.json`: Industrial engineering container boxes.
- **Unified CLI Tool (`cli.py`)**:
  - `undo`: Deconstruct templates.
  - `build`: Render vector presentations.
  - `sync`: Inspect external modifications.
  - `demo`: Full end-to-end enterprise Agentic AI showcase pipeline.
- **Antigravity Skill Definition (`SKILL.md`)**:
  - Registered both in workspace `.agents/skills/undo-ppt/` and globally `~/.gemini/config/skills/undo-ppt/`.
- **Automated Test Suite (`tests/test_engine.py`)**:
  - 100% test pass rate across deconstruction, rendering, compiling, and sync watching.
