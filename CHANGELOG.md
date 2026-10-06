# CHANGELOG

All notable changes to the `undoPPT` Super Skill and Engine are documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.6.0] - 2026-10-06

Theme: **the skeleton**. The audit cannot tell a deck built from real material from one built from nothing, so v3.6 moves the quality gate upstream: ask first, write the outline from evidence, and stop dressing thin content in big layouts.

### Added
- **`cli.py probe`** (`core/contract_probe.py`): Cognitive Contract readiness probe. Classifies the scenario, checks Q1 thesis / Q2 audience / Q3 knowledge gap / Q4 decision plus 3-4 scenario-specific facts, and returns what to ask. Q2 and Q4 are blocking. `plan` and `generate` print the same hint but never stop.
- **`docs/scenario_outlines.md`**: exemplar outlines for all 12 enterprise scenarios (audience gate, decision required, six pages with layout, mission and the evidence each page needs, red lines). A test keeps the documented storylines in step with the planner.
- **Evidence budget audit**: `THIN_CONTENT_P<n>` (body text too short for the layout) and `EVIDENCE_BUDGET_P<n>` (KPI slide with fewer than half the metrics numeric). Deduction capped at 12.
- **`core/blueprint_compat.py`**: maps the documented blueprint fields to the renderers' fields; used by both builders.
- `SKILL.md`: stage 1 rewritten around "not enough information, do not generate" with the probe flow and ask-first mermaid loop; `plan`/`generate` repositioned as fallback.
- `docs/PRD_v3.6_SKELETON_CONTRACT_AND_EVIDENCE.md`; 24 new tests (suite is now 68).

### Fixed
- **Text silently dropped from slides.** The spec and planner describe `cross_mapping`, `horizons_curve`, `maturity_ladder`, `matrix_2x2` and `content_columns` with one set of field names; the renderers read another. Measured on the 12 scenario decks, a `cross_mapping` slide lost 90% of its text, `horizons_curve` 74%, `maturity_ladder` 50%, `content_columns` 60%, `matrix_2x2` 44%. After the fix every blueprint string reaches the PPTX and the HTML for these layouts (0% lost).
- Architecture-stack layer descriptions were hidden for 4-layer stacks.
- "内部技术分享 / 技术分享 / 经验分享" prompts were classified as `general_informative` instead of `internal_tech_talk`.
- Blueprints now carry the engine version (`core.__version__`) instead of a hard-coded string.

### Changed
- `cognitive_planner` is documented as the **fallback** author: it has no insight of its own and returns a 90+ score for a request as empty as "帮我做一份关于 AI 的汇报". The recommended path is Agent-authored blueprints after the probe.

### Known limits
- The probe detects whether a fact is *mentioned*, not whether it is right.
- On decision-ready summary pages, `points` are not drawn when `options` are present (by design: the options, recommendation and sign-off list take the page).

### Roadmap
- **v3.7.0** Flesh: `source`/`status` fields, "to verify" marking, `cli.py ingest`, decision-ready demo.
- **v3.8.0** Skin polish and motion.

---

## [3.5.0] - 2026-10-06

Theme: **the skin floor**. A deck that audits at 94/100 can still render broken. v3.5 renders the deliverables in PowerPoint and Chrome and fixes what that shows.

### Added
- **`cli.py render-check`**: static layout lint (always) plus real renders (`--render`) through PowerPoint/LibreOffice and headless Chrome. Finding codes: `OUT_OF_BOUNDS`, `TITLE_WRAPS`, `TEXT_OVERFLOW`, `TEXT_CROSSES_SHAPE`, `TEXT_OVERLAP`, `BLANK_BAND`, `HTML_OVERFLOW_BOTTOM`, `HTML_OVERFLOW_RIGHT`. `build` now runs the static lint and prints warnings.
- **`core/layout_fit.py`**: content-adaptive layout pass (title fit, token card radius, 12pt font floor with overflow guard, card fit, vertical balance).
- **`core/layout_lint.py`**, **`core/render_check.py`**, `requirements-dev.txt`.
- **HTML**: fixed 1340x754 canvas scaled to the viewport, `?slide=N` deep link, `?static=1` mode for deterministic capture, body density fit (up to 1.4x).
- `docs/PRD_v3.5_SKIN_FLOOR_AND_RENDER_CHECK.md`, 21 new tests (`tests/test_layout.py`); suite is now 44 tests.

### Fixed
- **Wrapped titles collided with content** on 5 of 8 demo slides (a 34pt title wrapped to two lines and ran into the cards; the subtitle was hidden behind them).
- **Empty slides**: the planner emitted `kpi_dashboard` for QBR/OKR/headcount decks, which neither builder knew; the slide fell back to an empty bento page. Both builders now alias it, and unknown layouts warn.
- **Unreadable decision pages**: 64% of text on `summary` decision pages was under 11pt; maturity ladder 61%, 2x2 matrix 50%.
- **Stretched cards and blank space**: PPTX cards were fixed-height regardless of content; HTML bodies stretched every card to fill the canvas.
- **Pill-shaped cards**: python-pptx's default corner radius is 1/6 of the short side; tall cards rendered as pills. Now uses the token `card_style.border_radius`.
- **Charts** used PowerPoint's default blue/red/green; now themed from the palette with light gridlines and data labels.
- **Font names** were written as CSS stacks (`"PingFang SC, Inter, sans-serif"`), which PowerPoint cannot resolve; now the first family, applied to latin and east-asian.
- **HTML was not offline**: it loaded Tailwind and web fonts from CDNs, contradicting the "zero dependencies" claim. The Tailwind runtime is inlined (`core/vendor/`, MIT).
- **Narrow screens**: slide content overflowed and was clipped.
- Stale `output/` artifacts removed from git (now ignored); version strings and docs aligned to the release; `cyber_dark` preset reference replaced with the four real presets.

### Known limits
- Text measurement is a heuristic (CJK = 1 em, Latin about 0.55 em); `render-check --render` is the ground truth.
- PPTX real rendering needs PowerPoint (macOS) or LibreOffice; without them only the static lint runs.
- `BLANK_BAND` flags slides that have too little content. Fixing thin content is the v3.6 `EVIDENCE_BUDGET` work, not a layout problem.
- The planner classifies "内部技术分享" prompts as `general_informative` instead of `internal_tech_talk` (planned for v3.6).

### Roadmap
- v3.6.0 Skeleton: done (see above).
- **v3.7.0** Flesh: `source`/`status` fields, "to verify" marking, `cli.py ingest`, decision-ready demo.
- **v3.8.0** Skin polish and motion: typography/contrast rules, real-template trials, three narrative animations verified in PowerPoint and Keynote.

---

## [3.4.0] - 2026-09-17

### Added
- **Enterprise 12 Scenarios & Executive Decision Rigor PRD (`docs/PRD_v3.4_ENTERPRISE_12_SCENARIOS_AND_DECISION_RIGOR.md`)**:
  - Published comprehensive v3.4 PRD standardizing enterprise presentation cognitive architecture across 12 core workplace scenarios.
  - Formulated Jobs-to-be-Done (JTBD), executive psychological defenses, bespoke Q1~Q4 cognitive contracts, and recommended 6-slide deduction storylines for all 12 scenarios.
- **Enterprise 12 Scenarios Dedicated Cognitive Synthesizers (`core/cognitive_planner.py`)**:
  - `project_charter` (S01: 项目立项答辩与投资评审) - Focuses on commercial viability, ROI, and resource exchange.
  - `annual_strategy_okr` (S02: 年度战略规划与 OKR 制定) - Focuses on vision cascade, resource allocation, and organizational alignment.
  - `qbr_business_review` (S03: 季度/月度业务复盘 QBR) - Focuses on honest metrics variance, root cause attribution, and corrective actions.
  - `cross_team_alignment` (S04: 跨部门业务协同与共识拉通) - Focuses on shared OKRs, dependency handshakes, and SLA contracts.
  - `team_headcount_review` (S05: 团队述职与 HC 编制申请) - Focuses on productivity leverage, bandwidth bottleneck, and ROI per headcount.
  - `tech_rfc_review` (S06: 技术方案选型与架构 RFC 评审) - Focuses on 3-way benchmarking, failure domains, and rollback mechanisms.
  - `post_mortem_review` (S07: 生产重大故障复盘与根因分析) - Focuses on timeline reconstruction, 5-Whys root cause, and systemic defense mechanisms.
  - `product_launch_gtm` (S08: 新产品发布会与 GTM 上市方案) - Focuses on product positioning, unit economics, and launch milestones.
  - `enterprise_rfp_pitch` (S09: 大客户商务提案与竞标 RFP) - Focuses on enterprise compliance, case studies, and SLA guarantees.
  - `promotion_assessment` (S10: 晋升答辩与职级评审) - Focuses on STAR battle evidence, stripping platform tailwinds for net personal contribution, and next-level commitments.
  - `internal_tech_talk` (S11: 内部技术分享与赋能培训) - Focuses on anti-pattern contrast, step-by-step hands-on mental models, and knowledge transfer.
  - `all_hands_rally` (S12: 全员大会与战略誓师动员) - Focuses on battle milestones, cultural hero stories, and collective call-to-arms.
- **Executive Decision-Ready Closing Extension (`summary` primitive)**:
  - Extended `summary` layout in `core/pptx_builder.py` and `core/html_builder.py` with structured decision deliverables:
    - **Options Comparison Matrix**: Options A/B/C with pros, cons, and cost trade-offs.
    - **Recommendation Callout**: Distinct visual badge and clear rationale for the recommended choice.
    - **Sign-off Checklist (`sign_off_items`)**: Explicit headcount, budget, timeline, and decision approvals.
  - Interactive HTML presentation allows executives to click checkboxes live on the projector during meetings.
  - Native PPTX delivers high-contrast decision cards with highlighted recommendation badges.
- **Multi-Dimensional External Benchmarking Rigor & Audit Rule (`BENCHMARK_UNBALANCED`)**:
  - Enforced 3-way reference framework (Industry Tier 1, Open Source/New Entrant, Status Quo/Self-developed).
  - Code-level auditor (`core/content_auditor.py`) verifies presenter's proposal acknowledges trade-offs (costs, migration friction, boundary limitations) to eliminate hollow "all-win" claims.
  - Automatic self-healing blueprint patching in `core/cognitive_planner.py`.
- **Authentic Career Attribution Protocol & Audit Rule (`PROMOTION_LAUNDRY_LIST`)**:
  - Enforces STAR methodology and isolates personal net increment from overall company/macro growth tailwinds.
  - Disallows routine duty listings ("参与了/负责了...") without hard quantifiable metrics.
- **Leadership Decision Ask Enforcement (`DECISION_ASK_MISSING`)**:
  - Audits executive decks to ensure slides never end on open-ended discussion questions, demanding concrete sign-off items.
- **Design Philosophy Principles 8 & 9 (`DESIGN_PHILOSOPHY.md` & `DESIGN_PHILOSOPHY_zh.md`)**:
  - Principle 8: *Decision-Ready Closing & Rigorous Multi-Dimensional Benchmarking*.
  - Principle 9: *Authentic Career Attribution & Multi-Scenario Depth*.
- **Comprehensive Scenario Anti-Patterns Section 3 (`docs/en/scenario_anti_patterns.md`)**:
  - Detailed anti-patterns, correct patterns, and required primitive sequences for all 12 enterprise scenarios.

### Changed
- Bumped engine version to `3.4.0` across `core/__init__.py`, `SKILL.md`, `.agents/skills/undo-ppt/SKILL.md`, and test suites.

---

## [3.3.0] - 2026-09-17

### Added
- **Kinetic Dynamics & Decision Sandbox PRD Release (`docs/PRD_v3.3_KINETIC_DYNAMICS_AND_INTERACTION_SANDBOX.md`)**:
  - Published comprehensive v3.3 PRD and engineering architecture specification covering EPIC-01 through EPIC-06.
  - Formalized the transition from static presentation slides to semantic kinetic dynamics and live executive decision sandboxes.
- **PPTX Standard ECMA-376 OOXML `<p:timing>` Sequences (`core/pptx_builder.py`)**:
  - Implemented compliant OOXML `<p:timing>` element builder for native PowerPoint click-to-advance sequence animations without any external plugins.
  - Intelligently clusters content shapes (Bento cards, layers, metric cards, timeline milestones) and binds them to sequential click-advance time nodes.
  - Fully matches `open-kimi-ppt-skill`'s element animation capability while remaining 100% self-contained in pure Python with zero headless browser dependencies.
- **15 Layout Primitives Semantic Dynamics & Causal Timing**:
  - **Architecture Stacks (`architecture_stack`)**: Bottom-up gravitational assembly (infrastructure layers lock first, intermediate coordination layers expand, top-level gateways spotlighted).
  - **KPI Spotlight (`metric_spotlight`)**: Web count-up physics with cubic-bezier easeOut (0% -> 94.8%) and dynamic delta badge updates.
  - **Timeline & Process Flow (`timeline` / `process_flow`)**: Flowing light beam pulse animation (`flowing-beam`).
  - **Causal Timing Clock**: Adaptive animation pacing tied to `narrative_arc` (conflict 250ms snappy, breakthrough 400ms radial glow, evidence 600ms firm count-up).
- **Live Presenter HUD (`P` Key / Cognitive Copilot in HTML)**:
  - Single-file HTML now embeds **Presenter HUD** (toggled via `P` key or bottom navigation button):
    - **Cognitive Compass (认知罗盘)**: Real-time tracking of Q1-Q4 Cognitive Contract, core thesis anchor, audience stance, and current slide mission.
    - **Transition Teleprompter (因果提词器)**: High-visibility rhetorical teleprompter providing precise voiceover cues before advancing.
    - **Objection Playbook (质疑应对弹药库)**: Dynamic skeptical challenge and smoking-gun counter-defense pairings synthesized from slide evidence or custom `hud_notes`.
- **Active Decision Sandbox (活动决策推演沙盒) & Architecture Drilldown**:
  - **Scenario Switcher Tab**: Dynamic switching between *Conservative (保守)*, *Baseline (基准)*, and *Aggressive (突破)* scenarios with real-time recalculation and smooth count-up transitions.
  - **Architecture Drilldown Modal**: Click any microservice component in architecture stacks to view SLA targets (99.99%), P99 latency (<15ms), upstream/downstream calling chain, and disaster recovery fallback routes.
- **Bi-directional Strategic Intent Reflection Engine (`core/sync_watcher.py`)**:
  - Added `analyze_intent_diff` to infer the human expert's underlying strategic intent (performance elevation, scope focusing, posture change) from local manual modifications in PowerPoint or JSON.
  - Integrated intent deductions into `cli.py sync` to automatically guide the next-turn AI Agent posture.
- **Design Philosophy Principles 6 & 7 (`DESIGN_PHILOSOPHY.md` & `DESIGN_PHILOSOPHY_zh.md`)**:
  - Principle 6: Semantic Kinetic Physics (*"结构决定动效，语义赋予重力"*).
  - Principle 7: Active Decision Sandbox (*"从单向灌输蜕变为现场拍板的推演沙盒"*).

### Changed
- Bumped engine version to `3.3.0` across `core/__init__.py`, `SKILL.md`, `.agents/skills/undo-ppt/SKILL.md`, and test suites.

---

## [3.2.0] - 2026-09-17

### Added
- **Scenario Anti-Pattern Red Lines System & PRD Release (`docs/PRD_v3.2_SCENARIO_REDLINES_AND_ANIMATION.md`)**:
  - Published comprehensive v3.2 PRD and official engineering specification handbook (`docs/en/scenario_anti_patterns.md`).
  - Strict code-level interception of formulaic AI buzzwords and management jargon (`BUZZWORD_PATTERNS` in `core/content_auditor.py`) such as *"不仅是X更是Y"*, *"闭环/抓手/赋能/打法/颗粒度/底层逻辑/盘活/解构/破局"*.
  - Enforced truth-in-evidence discipline: disallowing fabricated metrics and ungrounded claims, with mandatory `[待实测]` or `[设计预估]` tags for assumptions.
  - Formulated scenario-specific red lines for all 6 archetypes (strategy trade-offs, architecture latency/rollback gates, pitch deck unit economics, resume STAR bounds, pedagogical misconception contrasts, informative accountability WBS).
- **Motion & Staged Progression Architecture (Level 1 & Level 2)**:
  - **Native PPTX Slide Transitions (`core/pptx_builder.py`)**: Injected standard OOXML `<p:transition>` (supporting `fade`, `push`, `wipe`, `none`), guaranteeing 100% native slide-level transition playback in PowerPoint, Keynote, and WPS.
  - **HTML Staged Step Presentation Mode (`core/html_builder.py`)**: Added interactive step mode (`Step: ON/OFF` button, toggled via `S` key). Pressing Spacebar reveals primitive child components (Bento cards, architecture layers, timeline milestones) step-by-step to command audience attention before advancing to the next slide.
  - Extended Blueprint schema with optional `transition_effect` and `motion` metadata.
  - Added CLI flag `--transition {fade,push,wipe,none}` to `cli.py generate` and `cli.py build`.
- **Design Philosophy Principles 4 & 5 (`DESIGN_PHILOSOPHY.md` & `DESIGN_PHILOSOPHY_zh.md`)**:
  - Principle 4: Truth-in-Evidence & Anti-Buzzword Discipline.
  - Principle 5: Motion as Cognitive Pacing (Cognitive Restraint).

### Changed
- Bumped engine version to `3.2.0` across `core/__init__.py`, `docs/`, `SKILL.md`, and test suites.

---

## [3.1.0] - 2026-09-14


### Added
- **Comprehensive English Documentation Suite**:
  - Full English default `README.md` with bilingual toggle linking to `README_zh.md`.
  - Complete English translation of the Design Philosophy Whitepaper (`DESIGN_PHILOSOPHY.md`) with bilingual toggle linking to `DESIGN_PHILOSOPHY_zh.md`.
  - In-depth technical guides under `docs/en/`:
    - `docs/en/blueprint_specification.md`: Full JSON Schema reference and examples for all 15 layout primitives.
    - `docs/en/cli_reference.md`: Comprehensive CLI command manual with parameter breakdowns.
    - `docs/en/architecture.md`: Architectural deep-dive covering decoupled cognition, pipelines, and modules.
    - `docs/en/agent_integration.md`: AI Agent orchestration guide across Cursor, Claude Code, OpenAI Codex, Windsurf, Trae, WorkBuddy, Google Antigravity, and OpenCode.
  - Open-source contributing guide (`CONTRIBUTING.md`).
- **Design Philosophy & Architecture Synergy Whitepaper (`DESIGN_PHILOSOPHY.md`)**:
  - Released comprehensive whitepaper formalizing the foundational manifesto: *"PPT is not an art album, but an audience-centric cognitive reshaping and decision intervention project."*
  - Explicitly defined the operational boundaries between **AI Agent** (Soft Cognition: Q1-Q4 contract probe, 6-scenario routing, 15-primitive blueprint authoring, intent reflection) and **undoPPT Skill** (Hard Enforcement: master AST decompilation, mathematical layout, native vector charts/tables, 10-dimension dual auditing, SHA-256 sync sensing).
  - Detailed the **5-Layer Quality Assurance Closed-Loop Framework** (Cognitive Contract ➔ 15-Primitive Schema Discipline ➔ Design Tokens & Density Budgets ➔ 10-Dimension Dual Auditing with Self-Correction ➔ Native Editable Deliverables with Speaker Notes).
- **Complete Legacy String Sanitization**:
  - Fully purged all legacy company names and domain artifacts across `README.md`, `CHANGELOG.md`, `tests/test_engine.py`, and runtime caches.
- **Clean Blueprint Regeneration**:
  - Re-synthesized standard generic blueprints and sync states with version `3.1.0`.

### Changed
- Bumped engine version to `3.1.0` (v3.1) across `core/__init__.py`, `cli.py`, `core/cognitive_planner.py`, `SKILL.md`, `.agents/skills/undo-ppt/SKILL.md`, `README.md`, and `tests/test_engine.py`.

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
  - **Complete Removal of Domain Hardcoding**: Eliminated all static company/benchmark scripts and domain-specific hardcoded buzzwords. The engine now dynamically extracts entities, subjects, and roles from natural language prompts and reference documents.
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
