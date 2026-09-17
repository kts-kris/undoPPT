# undoPPT Blueprint Specification (v3.1.0)

This document defines the complete JSON Schema specification for `blueprint.json`, the immutable delivery contract between the AI Agent and the `undoPPT` rendering engine.

---

## 1. Top-Level Structure

A valid `blueprint.json` consists of two primary keys:
- `contract`: Defines the top-level cognitive pillars and target outcomes.
- `slides`: An ordered array of slide definitions conforming to one of the 15 layout primitives.

```json
{
  "contract": {
    "core_thesis": "Overarching core thesis statement",
    "audience": {
      "role": "Target audience role (e.g., CTO, Executive Committee, Student)",
      "stance": "Audience mindset, risk profile, and priorities"
    },
    "knowledge_delta": {
      "known_baseline": ["Fact audience already knows 1", "Fact 2"],
      "blindspots_and_pains": ["Critical pain point 1", "Core misconception 2"]
    },
    "target_outcomes": {
      "understand": "Key concept audience must comprehend",
      "believe": "Core conviction audience must accept",
      "act": "Concrete immediate action or decision requested"
    }
  },
  "slides": [
    { /* Slide 1 */ },
    { /* Slide 2 */ }
  ]
}
```

---

## 2. Universal Slide Metadata Fields

Every slide object **must** include the following standard metadata attributes, regardless of its layout type:

| Field | Type | Description |
| :--- | :--- | :--- |
| `layout_type` | `string` | One of the 15 layout primitive identifiers. |
| `narrative_arc` | `string` | Narrative stage: `hook`, `conflict`, `breakthrough`, `evidence`, `progression`, or `call_to_action`. |
| `mission` | `string` | The single cognitive duty of this slide (answers Q6). |
| `transition` | `string` | Rhetorical bridge connecting from the previous slide (answers Q10). Required for all slides after slide 1. |
| `action_title` | `string` | Conclusion-first headline stating an assertion rather than a topic. |
| `core_evidence` | `string` | Primary quantitative proof (e.g. `94.8%`, `4x efficiency`) or definitive case study. |
| `title` | `string` | Visual primary slide headline. |
| `subtitle` | `string` | Contextual subtitle or framing statement. |
| `transition_effect` | `string` (optional) | Slide transition animation: `"fade"` (default), `"push"`, `"wipe"`, or `"none"`. |
| `motion` | `object` (optional) | Primitive-level staged reveal config: `{"staged_reveal": true, "stagger_delay_ms": 150}`. |
| `sandbox` | `object` (optional) | Active Decision Sandbox config: `{"enabled": true, "scenarios": { "conservative": {...}, "aggressive": {...} }}`. |
| `hud_notes` | `object` (optional) | Presenter HUD coaching notes: `{"objection_defense": [{"skepticism": "...", "counter": "..."}]}`. |

---



## 3. The 15 Layout Primitives

### 1. `cover` (Cover Hero Card)
Used for the opening slide. Sets tone, context, and executive framing.

```json
{
  "layout_type": "cover",
  "narrative_arc": "hook",
  "mission": "Establish the presentation's core proposition and capture attention",
  "category": "ENTERPRISE AI ARCHITECTURE 2026",
  "title": "Next-Generation Enterprise Agentic AI Platform",
  "subtitle": "Architecting Autonomous Multi-Agent Workflows for Scaled Operations",
  "meta": "Architecture Review Board · Prepared by Principal AI Systems Group"
}
```

---

### 2. `bento_cards` (Bento Grid Cards)
Displays 2 to 4 comparative cards with distinct tags, titles, and bullet lists. One card can be visually highlighted.

```json
{
  "layout_type": "bento_cards",
  "narrative_arc": "conflict",
  "mission": "Contrast legacy limitations against the proposed modern architecture",
  "transition": "[Conflict] However, existing architectures fail to scale under production concurrency",
  "action_title": "Bottleneck: Monolithic pipelines incur 80% manual maintenance overhead",
  "core_evidence": "80% manual overhead; legacy scripts fail under 15%+ variance",
  "title": "Legacy Approaches vs. Agentic Autonomous Systems",
  "subtitle": "Moving from brittle workflow scripts to dynamic self-healing agents",
  "cards": [
    {
      "tag": "PASSIVE CHATBOT",
      "title": "Single-Turn LLMs",
      "desc": "Limited to reactive query response without contextual persistence or tool execution.",
      "bullets": ["One-way textual output", "Stateless execution prone to hallucination", "Requires 80% human intervention"],
      "highlight": false
    },
    {
      "tag": "AGENTIC CLUSTER",
      "title": "Collaborative Multi-Agent Engine",
      "desc": "Orchestrates specialized subagents with tool calling, shared memory, and deterministic verification.",
      "bullets": ["Dynamic reasoning & reflection", "Sub-10ms state synchronization", "400%+ overall throughput lift"],
      "highlight": true
    }
  ]
}
```

---

### 3. `architecture_stack` (Multi-Layer Architecture Stack)
Displays 3 to 4 horizontal architectural layers containing modular components.

```json
{
  "layout_type": "architecture_stack",
  "narrative_arc": "breakthrough",
  "mission": "Demonstrate clear separation of concerns across platform tiers",
  "transition": "[Breakthrough] Therefore, we establish a decoupled three-tier architecture",
  "action_title": "Architecture: Decoupled three-tier foundation guarantees enterprise security",
  "core_evidence": "Strict sandboxing prevents cross-tenant data leaks; 99.95% SLA guarantee",
  "title": "Enterprise Agentic Platform Architecture",
  "subtitle": "A decoupled, multi-tenant runtime environment with governed tool calling",
  "layers": [
    {
      "name": "Interaction & Client Tier",
      "desc": "Unified interface & protocol gateway",
      "items": ["Chat Workspaces", "IDE Plugins", "OpenAPI Gateway", "CLI Tooling"]
    },
    {
      "name": "Orchestration & Planning Tier",
      "desc": "Cognitive reasoning & memory state",
      "items": ["Intent Probe", "AST Decompiler", "Sync Watcher", "Quality Auditor"]
    },
    {
      "name": "Execution & Tooling Tier",
      "desc": "Secure sandboxed environment",
      "items": ["MCP Tool Servers", "Python Code Sandbox", "Vector Store", "Model Gateways"]
    }
  ]
}
```

---

### 4. `metric_spotlight` (KPI Spotlight Dashboard)
Highlights 3 to 4 high-impact metrics with oversized numbers, delta tags, and descriptions.

```json
{
  "layout_type": "metric_spotlight",
  "narrative_arc": "evidence",
  "mission": "Provide indisputable quantitative proof of performance and business impact",
  "transition": "[Evidence] Benchmarking demonstrates quantifiable improvements across all KPIs",
  "action_title": "Impact: Autonomous completion rate reaches 94.8% with 90% labor savings",
  "core_evidence": "94.8% task completion, <8ms sync latency, 45s end-to-end delivery",
  "title": "Key Operational & Efficiency Benchmarks",
  "subtitle": "Measured performance against industrial standard baseline benchmarks",
  "metrics": [
    {
      "label": "Autonomous Task Completion",
      "value": "94.8%",
      "delta": "+38.4% vs. baseline",
      "desc": "Complex multi-step engineering tasks completed without human retry"
    },
    {
      "label": "State Sync Latency",
      "value": "<8ms",
      "delta": "-85% delay",
      "desc": "Real-time SHA-256 fingerprint diff calculation overhead"
    },
    {
      "label": "Full Presentation Build",
      "value": "45s",
      "delta": "10x acceleration",
      "desc": "From unstructured document ingest to dual-format verified delivery"
    }
  ]
}
```

---

### 5. `timeline` (Roadmap & Milestone Progression)
Presents 3 to 4 sequential chronological milestones with specific deliverables.

```json
{
  "layout_type": "timeline",
  "narrative_arc": "progression",
  "mission": "Establish clear execution phased rollout and delivery expectations",
  "transition": "[Progression] Execution follows a four-phase phased deployment model",
  "action_title": "Roadmap: Phased rollout delivers immediate pilot value within 60 days",
  "core_evidence": "Phase 1 pilot delivers ROI proof in 60 days across 3 core squads",
  "title": "Implementation Roadmap & Milestones",
  "subtitle": "Structured phased rollout from pilot validation to enterprise-wide scaling",
  "steps": [
    {
      "time": "Phase 1 (Months 1–2)",
      "title": "Pilot Validation",
      "items": ["Core POC validation", "Template standard library setup", "Private VPC sandbox deployment"]
    },
    {
      "time": "Phase 2 (Months 3–4)",
      "title": "Platform Rollout",
      "items": ["Multi-agent cluster launch", "MCP tool server integration", "Onboard 30% engineering teams"]
    },
    {
      "time": "Phase 3 (Months 5–6)",
      "title": "Enterprise Scale",
      "items": ["Company-wide standardization", "Live vector memory sync", "Operational analytics dashboard"]
    }
  ]
}
```

---

### 6. `matrix_2x2` (Strategic 2x2 Matrix)
Positions concepts across two orthogonal axes (e.g. Technical Scope vs. Governance Control) into 4 quadrants.

```json
{
  "layout_type": "matrix_2x2",
  "narrative_arc": "breakthrough",
  "mission": "Categorize strategic options to justify target architectural positioning",
  "transition": "[Breakthrough] Evaluating alternatives requires balancing velocity and governance",
  "action_title": "Matrix: Target positioning balances dynamic adaptability with zero-trust safety",
  "core_evidence": "Top-right quadrant achieves optimal risk-adjusted operational velocity",
  "title": "Strategic Architecture Positioning Matrix",
  "subtitle": "Mapping autonomy vs. compliance across enterprise solution models",
  "axes": {
    "x": "Automation Autonomy",
    "y": "Governance & Compliance Control"
  },
  "quadrants": [
    { "name": "Ad-Hoc Scripts", "desc": "Low autonomy, low governance; high manual friction", "tag": "Retire" },
    { "name": "Rigid Workflows", "desc": "Low autonomy, high governance; brittle to changes", "tag": "Transition" },
    { "name": "Rogue Bots", "desc": "High autonomy, low governance; unacceptable risk", "tag": "Avoid" },
    { "name": "Governed Agentic Cluster", "desc": "High autonomy, rigorous policy guardrails", "tag": "Target" }
  ]
}
```

---

### 7. `maturity_ladder` (Maturity Evolution Ladder)
Illustrates a 3 to 5 step advancement from initial ad-hoc status to autonomous maturity.

```json
{
  "layout_type": "maturity_ladder",
  "narrative_arc": "progression",
  "mission": "Provide a concrete path for organizational and technical evolution",
  "transition": "[Progression] Capability advances through four distinct maturity tiers",
  "action_title": "Maturity: Progressive capability gates prevent premature operational exposure",
  "core_evidence": "Each tier requires 95%+ audit pass rates before gate progression",
  "title": "Capability Maturity Evolution Model",
  "subtitle": "Stepwise capability growth with concrete milestone verification criteria",
  "levels": [
    { "step": "L1", "name": "Manual Assist", "desc": "Isolated prompt completion", "target": "Individual efficiency", "focus": "Prompt libraries", "metric": "+15% speed" },
    { "step": "L2", "name": "Workflow Integration", "desc": "Chained pipelines", "target": "Team productivity", "focus": "Task automation", "metric": "-40% manual steps" },
    { "step": "L3", "name": "Autonomous Agents", "desc": "Multi-agent collaboration", "target": "Systemic leverage", "focus": "MCP tool sandboxes", "metric": "90%+ autonomous completion" },
    { "step": "L4", "name": "Self-Optimizing Cluster", "desc": "Dynamic reflection", "target": "Organizational agility", "focus": "Evolutionary memory", "metric": "Continuous optimization" }
  ]
}
```

---

### 8. `horizons_curve` (Three Horizons Growth Model)
Categorizes investments into Horizon 1 (Core Operations), Horizon 2 (Emerging Capabilities), and Horizon 3 (Future Transformation).

```json
{
  "layout_type": "horizons_curve",
  "narrative_arc": "breakthrough",
  "mission": "Allocate organizational bandwidth and budget across temporal horizons",
  "transition": "[Breakthrough] Resource allocation must balance immediate ROI with long-term leadership",
  "action_title": "Allocation: Rebalance resource mix from 70:20:10 to 50:30:20 across 3 horizons",
  "core_evidence": "Reallocating 30% budget into H2 generates 3x downstream pipeline value",
  "title": "Three Horizons Growth & Investment Model",
  "subtitle": "Balancing immediate business efficiency against long-term strategic transformation",
  "horizons": [
    { "horizon": "H1", "name": "Core Efficiency", "desc": "Automating routine document & code generation", "focus": "Immediate cost reduction", "kpi": "Cut 80% manual hours" },
    { "horizon": "H2", "name": "Platform Scaling", "desc": "Enterprise agent orchestration & shared memory", "focus": "Cross-team leverage", "kpi": "50+ teams onboarded" },
    { "horizon": "H3", "name": "Autonomous Operations", "desc": "Self-learning multi-agent ecosystem", "focus": "New business models", "kpi": "Net-new automated products" }
  ]
}
```

---

### 9. `cross_mapping` (Cross-Layer Alignment Table)
Maps challenges to solutions and accountable owners across organizational or architectural layers.

```json
{
  "layout_type": "cross_mapping",
  "narrative_arc": "evidence",
  "mission": "Align technical solutions directly with operational stakeholders",
  "transition": "[Evidence] Every technical intervention maps directly to a concrete operational owner",
  "action_title": "Alignment: Direct mapping across business, platform, and data tiers",
  "core_evidence": "Single owner assigned to each tier ensures zero cross-silo deadlock",
  "title": "Cross-Layer Transformation Mapping",
  "subtitle": "Traceable resolution mapping from existing pain points to strategic levers",
  "mapping_rows": [
    { "layer": "Executive Governance", "current": "Opaque AI adoption metrics", "target": "Real-time compliance dashboard", "action": "Establish AI Governance Committee" },
    { "layer": "Platform Engineering", "current": "Brittle individual API calls", "target": "Standardized MCP tool mesh", "action": "Deploy sandboxed runtime nodes" },
    { "layer": "Operations & Teams", "current": "Fragmented employee tools", "target": "Unified workspace agent skill", "action": "Mandate undoPPT Super Skill SOP" }
  ]
}
```

---

### 10. `summary` (Executive Takeaways & Resolutions)
Summarizes 3 to 4 strategic takeaways and issues a concrete call to action.

```json
{
  "layout_type": "summary",
  "narrative_arc": "call_to_action",
  "mission": "Secure executive approval and initiate execution immediately",
  "transition": "[Call to Action] The platform and governance plan are fully primed for initiation",
  "action_title": "Decision: Approve Phase 1 pilot project and allocate engineering squad",
  "core_evidence": "Cognitive Contract and architecture validated; pilot ROI estimated in 60 days",
  "title": "Strategic Resolutions & Next Steps",
  "subtitle": "Guiding principles for rapid kickoff and governed pilot execution",
  "points": [
    { "title": "Commit to Cognitive Contract Disciplines", "desc": "Enforce strict Q1–Q4 stakeholder alignment before authoring presentations." },
    { "title": "Adopt Master Template Penetration", "desc": "Standardize all decks using automated master decompilation and design tokens." },
    { "title": "Deploy Dual-Format Delivery", "desc": "Deliver native editable vector PPTX with speaker notes alongside zero-friction HTML." },
    { "title": "Maintain Always-in-Sync Collaboration", "desc": "Track external modifications in <10ms to keep AI and human creators unified." }
  ]
}
```

---

### 11. `standard_table` (Standard Formatted Data Table)
Renders a high-density, alternating zebra-striped data matrix with formatted headers.

```json
{
  "layout_type": "standard_table",
  "narrative_arc": "evidence",
  "mission": "Provide detailed comparative data across feature matrices",
  "transition": "[Evidence] Detailed benchmark telemetry confirms superiority across all facets",
  "action_title": "Comparison: Standardized engine outperforms legacy tools in all 5 criteria",
  "core_evidence": "100% native vector support, sub-10ms diff detection, zero bitmap artifacting",
  "title": "Enterprise Solution Feature Comparison",
  "subtitle": "Benchmarking undoPPT against legacy template systems and generic AI generators",
  "headers": ["Evaluation Metric", "Legacy AI PPT", "Static Templates", "undoPPT Engine"],
  "rows": [
    ["Output Format", "Raster Images / Non-editable", "Static XML replacements", "100% Native Vector PPTX + HTML"],
    ["Master Decompilation", "Unsupported", "Manual authoring", "Automated AST Decompiler"],
    ["Human Co-editing", "One-way overwrite", "Manual only", "Sub-10ms Always-in-Sync"],
    ["Quality Auditing", "None", "None", "10-Dimension Dual Auditor"],
    ["Speaker Notes", "Generic text", "None", "Automated Mission & Script Injection"]
  ]
}
```

---

### 12. `data_chart` (Native PowerPoint Vector Chart)
Renders native Office/Keynote charts editable via spreadsheet data.

```json
{
  "layout_type": "data_chart",
  "narrative_arc": "evidence",
  "mission": "Present quantifiable trend data using native editable charts",
  "transition": "[Evidence] Quantitative telemetry demonstrates consistent 4-quarter efficiency growth",
  "action_title": "Trend: Automated delivery volume surged 400% while cycle time dropped 85%",
  "core_evidence": "400% volume increase from Q1 to Q4; cycle time reduced from 8 hrs to 45 mins",
  "title": "Quarterly Efficiency & Delivery Velocity",
  "subtitle": "Measured enterprise presentation cycle times over the 2026 fiscal year",
  "chart_type": "column_clustered",
  "categories": ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"],
  "series": [
    {
      "name": "Manual Delivery (Hours)",
      "values": [8.5, 7.8, 6.2, 5.0]
    },
    {
      "name": "undoPPT Assisted (Hours)",
      "values": [1.5, 0.9, 0.7, 0.4]
    }
  ]
}
```
*Supported `chart_type` values*: `column_clustered`, `line`, `pie`.

---

### 13. `content_columns` (Multi-Column Themed Cards)
Renders 2 to 4 parallel vertical columns with header tags, titles, and itemized bullet points.

```json
{
  "layout_type": "content_columns",
  "narrative_arc": "breakthrough",
  "mission": "Present multi-faceted capability pillars side-by-side",
  "transition": "[Breakthrough] The framework is built upon three foundational operational pillars",
  "action_title": "Pillars: Three operational pillars anchor the enterprise transformation",
  "core_evidence": "Three distinct squads formed with cross-functional leadership representation",
  "title": "Core Strategic Implementation Pillars",
  "subtitle": "Modular execution streams designed to prevent operational bottlenecks",
  "columns": [
    {
      "tag": "STREAM A",
      "title": "Infrastructure & Tooling",
      "points": ["Private VPC deployment", "MCP tool server clusters", "Sub-10ms sync watcher daemon"]
    },
    {
      "tag": "STREAM B",
      "title": "Governance & Compliance",
      "points": ["Zero-trust API policies", "10-dimension audit gates", "Automated PII scrubbing"]
    },
    {
      "tag": "STREAM C",
      "title": "Enablement & Training",
      "points": ["Agent prompt patterns", "Master template onboardings", "Executive debrief templates"]
    }
  ]
}
```

---

### 14. `keynote_quote` (Keynote Hero Quote)
Renders a centered hero quote layout with typography emphasis, author credentials, and an actionable takeaway badge.

```json
{
  "layout_type": "keynote_quote",
  "narrative_arc": "breakthrough",
  "mission": "Provide philosophical grounding through expert authority and core insight",
  "transition": "[Breakthrough] As management theory dictates, cognitive clarity precedes execution",
  "action_title": "Insight: Technology without cognitive alignment merely accelerates chaos",
  "core_evidence": "Consensus across 40+ enterprise transformation case studies",
  "title": "The Guiding Transformation Principle",
  "subtitle": "Framing the mindset shift required for human-AI collaborative workflows",
  "quote_text": "The greatest danger in times of turbulence is not the turbulence—it is to act with yesterday's logic.",
  "author": "Peter F. Drucker",
  "author_title": "Father of Modern Management",
  "key_takeaway": "Legacy slide generation paradigms must be replaced with cognitive contract disciplines."
}
```

---

### 15. `process_flow` (Horizontal Process Flow)
Renders 3 to 6 sequential progressive process steps with ordered numeric badges.

```json
{
  "layout_type": "process_flow",
  "narrative_arc": "progression",
  "mission": "Explain step-by-step pipeline mechanics clearly and concisely",
  "transition": "[Progression] The end-to-end execution follows a continuous 5-step pipeline",
  "action_title": "Workflow: 5-step deterministic pipeline transforms raw ideas into verified decks",
  "core_evidence": "Full pipeline executes in under 45 seconds with 100% audit compliance",
  "title": "End-to-End Cognitive Engineering Workflow",
  "subtitle": "From unstructured document ingestion to dual-format verified presentation delivery",
  "steps": [
    { "step": "01", "name": "Contract Probe", "desc": "Clarify Q1–Q4 cognitive objectives and audience expectations." },
    { "step": "02", "name": "AST Decompile", "desc": "Deconstruct template master layouts, slot coordinates, and tokens." },
    { "step": "03", "name": "Blueprint Synthesize", "desc": "Map content into 15 layout primitives with strict budget limits." },
    { "step": "04", "name": "Dual Audit & Heal", "desc": "Verify structural redlines and causal transitions with self-healing." },
    { "step": "05", "name": "Native Delivery", "desc": "Render editable PPTX with speaker notes and single-file HTML." }
  ]
}
```

---

## 4. Content Budget Rules & Redlines

To maintain visual hierarchy and prevent visual overflow, the engine enforces strict budget limits:

| Primitive | Max Entities | Max Title Length | Text Density Recommendation |
| :--- | :--- | :--- | :--- |
| `bento_cards` | 2–4 cards | ≤ 32 chars | 3 bullets per card, ≤ 20 words each |
| `architecture_stack` | 3–4 layers | ≤ 28 chars | 3–5 component tags per layer |
| `metric_spotlight` | 3–4 metrics | ≤ 30 chars | Value ≤ 8 chars, description ≤ 25 words |
| `timeline` | 3–4 steps | ≤ 30 chars | 2–3 deliverables per step |
| `matrix_2x2` | 4 quadrants | ≤ 24 chars | 1 tag + 1 description sentence per quadrant |
| `maturity_ladder` | 3–5 levels | ≤ 24 chars | 1 target, 1 focus, 1 metric per level |
| `horizons_curve` | 3 horizons | ≤ 24 chars | 1 focus, 1 KPI per horizon |
| `cross_mapping` | 3–5 rows | ≤ 28 chars | 3 columns: current, target, action |
| `standard_table` | ≤ 8 rows, ≤ 5 cols | ≤ 28 chars | Concise cell strings (≤ 15 words) |
| `data_chart` | ≤ 8 categories | ≤ 32 chars | 1–3 series with clean numeric arrays |
| `content_columns` | 2–4 columns | ≤ 24 chars | 2–4 bullet points per column |
| `keynote_quote` | 1 quote | ≤ 32 chars | Quote text ≤ 40 words, 1 key takeaway |
| `process_flow` | 3–6 steps | ≤ 24 chars | 1 title + 1 concise mechanism description |
