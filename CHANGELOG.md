# CHANGELOG

All notable changes to the `undoPPT` Super Skill and Engine are documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
