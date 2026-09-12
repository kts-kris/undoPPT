# CHANGELOG

All notable changes to the `undoPPT` Super Skill and Engine are documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-09-12

### Added
- **15 High-Fidelity Layout Primitives Expansion (`core/pptx_builder.py` & `core/html_builder.py`)**:
  - Expanded layout primitives from 10 to 15, adding:
    1. `standard_table`: Native PowerPoint and responsive HTML tables with themed headers, alternating rows, borders, and structured cells.
    2. `data_chart`: Native PowerPoint vector charts powered by `pptx.chart.data.CategoryChartData` (clustered column, line, pie) and pure CSS/HTML responsive chart equivalents. Editable directly in PowerPoint/Keynote.
    3. `content_columns`: 2 to 4 parallel content cards with tags, header titles, and bullet point items.
    4. `keynote_quote`: High-impact hero quote layout with typography emphasis, author/source title, and key takeaway badge.
    5. `process_flow`: Horizontal progressive step-by-step process diagram with sequence chips and milestone descriptions.
- **Universal Multi-Scenario Planner Overhaul (`core/cognitive_planner.py`)**:
  - Fully decoupled architecture across **6 universal scenario archetypes**:
    1. `strategic_planning`: Corporate strategy, transformation roadmaps, organizational alignment.
    2. `tech_architecture`: Technical architecture proposals, platform design, high-availability SLA benchmarks.
    3. `product_pitch`: Commercial pitch decks, startup roadshows, product launch decks.
    4. `personal_resume`: Personal resumes, promotion defense, executive portfolio, talent profiles.
    5. `education_training`: Pedagogical teaching, courseware, training curricula, concept breakdown.
    6. `general_informative`: Enterprise summaries, progress briefings, general work presentations.
  - Zero hardcoding: Complete eradication of legacy static scripts, hardcoded 94.8% auto-patches, and domain-bound assumptions.
  - Dynamic Self-Correction Refinement Loop: Generates custom contextual action titles, quantitative or pedagogical proof points, and valid transitions dynamically.
- **Scenario-Aware Auditor Decoupling (`core/content_auditor.py` & `core/semantic_auditor.py`)**:
  - Scenario-aware evidence evaluation: Recognizes qualitative pedagogical/training evidence for education and training decks without penalizing them for absence of corporate ROI metrics.
  - Expanded rhetorical transition taxonomy: Added pedagogical, instructional, and analytical transition phrases.
  - Density checks extended to all 15 layouts (table rows/cols, column count, process flow steps, chart categories).
- **Direct Agent Authoring JSON Schema (`SKILL.md`)**:
  - Full JSON schema documentation for all 15 layout primitives enabling AI Agents to craft dynamic blueprints directly.

### Changed
- Bumped engine version to `3.0.0` across `core/__init__.py`, `cli.py`, `README.md`, `CHANGELOG.md`, `SKILL.md`, and `.agents/skills/undo-ppt/SKILL.md`.
- Updated `cli.py demo` to demonstrate `data_chart` and `standard_table` primitives.

### Added
- **Full Architecture Decoupling & Multi-Scenario Cognitive Engine (`core/cognitive_planner.py`)**:
  - **Complete Removal of Domain Hardcoding**: Eliminated all static company/benchmark scripts (e.g. Mengniu, Singapore NAIS, dairy buzzwords). The engine now dynamically extracts entities, subjects, and roles from natural language prompts and reference documents.
  - **Dynamic Scenario Archetype Classification (`_classify_scenario`)**:
    - `strategic_planning`: Enterprise strategy, organizational restructuring, transformation roadmaps.
    - `career_portfolio`: Personal resume, promotion defense, executive portfolio, talent profiles.
    - `tech_architecture`: Technical architecture proposals, platform design, high-availability system reviews.
    - `product_pitch`: Commercial pitch decks, startup roadshows, product launch decks.
  - **Scenario-Specific Narrative & Layout Assembly**:
    - For `career_portfolio`: Assembles `cover` (Career positioning) ➔ `bento_cards` (Execution vs Composite Leader) ➔ `architecture_stack` (3-tier competency stack) ➔ `metric_spotlight` (Hardcore performance metrics: 99.99%, 300%+, 40M+ savings) ➔ `timeline` (Career breakthrough milestones) ➔ `summary` (First 90-day execution roadmap).
    - Adaptable Speaker Notes generation: Automatically switches tone and voice from executive briefing ("各位领导...") to interview/defense presentation ("各位评委、面试官好...").
  - **Dynamic Linguistic Entity & Candidate Extraction**:
    - Strips conversational filler prefixes ("帮我生成一份", "我要写一个") and uses NLP splitting rules to isolate the authentic core entity or candidate role.
  - **Expanded Test Suite (`tests/test_engine.py`)**:
    - Added `test_career_resume_planner` validating full pipeline synthesis and dual PPTX/HTML compilation for personal resume decks (13/13 tests passing).

### Changed
- Bumped engine version to `2.6.0` in `core/__init__.py`, `cli.py`, `README.md`, `CHANGELOG.md`, and all `SKILL.md` configurations.

---

## [2.5.0] - 2026-09-12

### Added
- **v1.3 True 100% Completion - Semantic Cognitive Auditor (`core/semantic_auditor.py`)**:
  - **Rhetorical Causal Taxonomy**: Evaluates inter-slide logical connectors against 6 causal dimensions (contrast, causality, breakthrough, progression, evidence, action).
  - **Centrifugal Thesis Alignment**: Keyword extraction and semantic drift detection to ensure every slide reinforces the core thesis.
  - **Quantitative Smoking-Gun Evidence Weighting**: Evaluates numerical metrics, percentages, ratios, and timeframes (Q9) across core evidence and content.
  - **Audience Skepticism Defense**: Verifies explicit defense against declared stakeholder pains and alignment with Understand-Believe-Act outcomes.
  - **Pluggable LLM-as-a-Judge Hook**: Enables optional high-order nuanced qualitative evaluation alongside zero-dependency heuristic auditing.
  - **Integrated into ContentAuditor (`core/content_auditor.py`)**: Reports Composite Score, Structural Score, Semantic Score, and 4 detailed subscores.

- **v1.5 True 100% Completion - Dynamic Grounded Planner (`core/cognitive_planner.py`)**:
  - **Document Context Ingestor (`DocumentContextIngestor`)**: Ingests external reference documents (Markdown, TXT, JSON) via `--input-doc` or context.
  - **Quantitative Fact Extraction**: Automatically discovers domain numbers, ratios (e.g., 418, 71, 7:2:1, 4:3:3, 90%), pains, and entity anchors.
  - **Autonomous Self-Correction Refinement Loop**: Proactively detects and auto-fixes passive titles, missing missions, weak evidence, and density warnings prior to final output.

- **v2.0 True 100% Completion - Deep Master AST Decompiler (`core/undo_engine.py`)**:
  - **Master Layout Slots Geometry Extraction**: Deconstructs title, body, subtitle, and footer placeholder coordinates and dimensions.
  - **Automatic Dark/Light Theme Mode Detection**: Determines canvas luminance and dynamically configures high-contrast surface and typography palettes.
  - **Visual Asset & Logo Extraction**: Automatically extracts embedded images and logos to `.undoppt/assets/`.

- **Expanded Regression Test Suite (`tests/test_engine.py`)**:
  - 12 comprehensive unit and integration tests covering semantic subscores, document ingestion, self-refinement, master slots, and theme modes (12/12 passing).

### Changed
- CLI upgraded to `v2.5.0` with `--input-doc` support in `plan` and `generate`, and detailed semantic audit score breakdowns.
- Synchronized `SKILL.md` and `.agents/skills/undo-ppt/SKILL.md` to `v2.5.0`.
- Bumped engine version to `2.5.0` in `core/__init__.py`, `cli.py`, `README.md`, and `CHANGELOG.md`.

---

## [2.0.0] - 2026-09-12

### Added
- **Autonomous Cognitive Planner (`core/cognitive_planner.py`)**:
  - Automatically synthesizes natural language user prompts into 10-dimension audited blueprints (`blueprint.json`).
  - Implements domain knowledge archetype detection (e.g. dairy/consumer goods, smart manufacturing, enterprise tech).
  - Automatically constructs rigid Cognitive Contracts (Q1~Q4) and multi-slide narrative arcs (Hook → Conflict → Breakthrough → Evidence → Call to Action).
  - Injects full脱稿口播演讲备注 (Speaker Notes) and causal transition connectors across all slides.
  - New CLI command: `python3 cli.py plan --prompt "<prompt>" [--context "<notes>"] [--out <blueprint.json>]`.
  - New one-shot generation command: `python3 cli.py generate --prompt "<prompt>" [--template <template.pptx>] [--format pptx|html|all] [--out <dir>]`.
- **4 Advanced Strategic Infographic Primitives (Expanded from 6 to 10 Primitives)**:
  - `matrix_2x2` (`render_matrix_slide`, `_render_matrix_html`): 2x2 four-quadrant strategic decision matrix with X/Y axes, strategy subtitles, quadrant chips, and principles sidebar.
  - `maturity_ladder` (`render_ladder_slide`, `_render_ladder_html`): Multi-tier progressive capability maturity model (Level 1..Level 4) with mechanisms, metrics, collaboration roles, and spanning safety line.
  - `horizons_curve` (`render_horizons_slide`, `_render_horizons_html`): Three Horizons (H1/H2/H3) portfolio governance model with distinct horizon cards, management styles, and KPI criteria.
  - `cross_mapping` (`render_cross_mapping_slide`, `_render_cross_mapping_html`): Cross-organization / cross-tier strategic alignment mapping table with tier badges, source practices, bridging arrows, and target enterprise mechanisms.
- **Enhanced Content Density Auditor (`core/content_auditor.py`)**:
  - Added dedicated capacity budget and structure audits for the 4 new infographic primitives.
- **Expanded Regression Test Suite (`tests/test_engine.py`)**:
  - Added unit and integration tests for `CognitivePlanner`, all 10 layout primitives, and dual build pipelines (8/8 tests passing).

### Changed
- Upgraded `cli.py` to version `2.0.0` with `plan` and `generate` subparsers.
- Synchronized `SKILL.md` and `.agents/skills/undo-ppt/SKILL.md` to `v2.0.0`.
- Bumped engine version to `2.0.0` in `core/__init__.py` and `README.md`.

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
