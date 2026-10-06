# AI Agent Integration Guide

This guide describes how to integrate and orchestrate `undoPPT` across modern AI Agents, including **Cursor, Claude Code, OpenAI Codex, Windsurf, Trae, Tencent WorkBuddy, Google Antigravity, and OpenCode**.

---

## 1. Installation Across Agent Environments

### 1.1 Universal NPX Installer
If your environment supports `npx skills`:
```bash
npx skills add https://github.com/kts-kris/undoPPT --skill undo-ppt
```

### 1.2 Manual Clone by Agent Platform

| AI Agent | Recommended Skill Directory | Discovery Mode |
| :--- | :--- | :--- |
| **Cursor** | `~/.cursor/skills/undo-ppt` or project `.agents/skills/undo-ppt` | Auto-discovered from workspace |
| **Claude Code** | `~/.claude/skills/undo-ppt` | Built-in skill loading |
| **OpenAI Codex / CLI** | `~/.codex/skills/undo-ppt` | Environment path discovery |
| **Windsurf / Trae** | `.agents/skills/undo-ppt/` in repo root | Workspace-level skill indexing |
| **Tencent WorkBuddy** | Enterprise Agent Skill store or custom tool directory | Workspace skill import |
| **Google Antigravity** | `~/.gemini/config/skills/undo-ppt` or `.agents/skills/undo-ppt` | Dual global/workspace detection |
| **OpenCode** | Root directory `SKILL.md` | Direct repo context ingestion |

---

## 2. Operating Rhythms

`undoPPT` supports two operational rhythms depending on the presentation's complexity and urgency:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Rhythm A: Deep Guided SOP (Default for High-Stakes Presentations)           │
│                                                                             │
│ 0. Readiness Probe (probe)           ➔  Not enough information: ask, don't  │
│                                         generate                            │
│ 1. Cognitive Contract Probe (Q1-Q4)  ➔  Clarify thesis, audience & goals    │
│ 2. Template Deconstruction (undo)    ➔  Read the template's real theme      │
│ 3. Blueprint Authoring, Provenance   ➔  Compose 15-primitive JSON; ingest / │
│    & Audit                              cite sources; audit                 │
│ 4. Dual-Format Rendering             ➔  Draft build, then --final to ship   │
│ 4.5 Render Check                     ➔  Verify in PowerPoint and Chrome     │
│ 5. Turn-by-Turn Sync Tracking        ➔  Sense human external modifications  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ Rhythm B: Rapid Direct Delivery (For Immediate Drafts & Low-Stakes Needs)   │
│                                                                             │
│ 1. Autonomous One-Shot CLI           ➔  cli.py generate --prompt "..."      │
│ 2. Automated Self-Correction Loop    ➔  Autonomous audit & auto-patching    │
│ 3. Instant Dual-Format Delivery      ➔  Ready in <45 seconds                │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **Rhythm B is a fallback.** The one-shot planner is a rule engine with no insight of its own: given a request as empty as "make a deck about AI" it still returns a 90+ audit score. Its numbers are invented templates (they show up as 待核 in the deck). Use it for a quick draft or when no Agent is available, and tell the user which figures are placeholders.

---

## 3. Rhythm A: Step-by-Step SOP

### Step 0: Readiness Probe (v3.6)
**Not enough information means no generation.** Run the probe on the user's request, verbatim:
```bash
python3 cli.py probe --prompt "<the user's request>" [--input-doc notes.md] --json
```
It classifies the scenario, reports which contract slots and scenario facts are still unknown, and returns the questions to ask, blocking ones first (audience and decision). If `ready` is false, ask 2 or 3 of them, with an example each, before writing anything. The 12 scenarios and what each page needs are in [scenario_outlines.md](../scenario_outlines.md).

### Step 1: Cognitive Contract Probe
The Agent should act as a senior management consultant. Instead of asking generic questions, ask targeted cognitive probes:
1. **Core Thesis (Q1)**: *"Stripping away all secondary details, what is the single central thesis or conclusion you want to convey?"*
2. **Audience Stance (Q2)**: *"Who is the primary audience (e.g., Board of Directors, Engineering Leads, Students), what risks are they defending against, and what is their default stance?"*
3. **Knowledge Delta (Q3)**: *"What does the audience already know (Baseline) versus what critical blindspots or pain points must be illuminated (Knowledge Delta)?"*
4. **Target Action (Q4)**: *"Immediately following the presentation, what specific decision or action should the audience approve or execute?"*

### Step 2: Master Decompilation (Optional)
If the user provides an enterprise PowerPoint template:
```bash
python3 cli.py undo --template /path/to/template.pptx --out .undoppt/design_tokens.json
```
If no template is provided, default to `presets/modern_bento.json`.

`undo` (v3.8) reads the template's **real theme**: colour scheme, master background, and fonts including the East Asian font; dark templates come out dark and the brand colour is kept. What it does not do: place the template's master layouts, background artwork or logos on the generated slides, or output 4:3. Say so to the user rather than promising a full master carry-over. See the [Design System](design_system.md).

### Step 3: Blueprint Composition & Auditing
The Agent composes `.undoppt/blueprint.json` conforming to the [Blueprint Specification](blueprint_specification.md), mapping each slide into one of the 15 layout primitives.

**Give every number an origin (v3.7).** If the user supplied a document or table, extract its figures with their origins and link them into the blueprint; never invent a number, and mark a placeholder `status: "todo"`:
```bash
python3 cli.py ingest --input-doc notes.md --out .undoppt/facts.json     # .md / .txt / .csv
python3 cli.py cite --blueprint .undoppt/blueprint.json --facts .undoppt/facts.json
```

The Agent then triggers the quality auditor:
```bash
python3 cli.py audit --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json
```
If the overall score is below 85, the Agent refines headlines into action-first statements and reinforces quantitative evidence. `THIN_CONTENT` and `EVIDENCE_BUDGET` mean the content cannot carry the layout: go back for material, do not adjust the layout. `UNSOURCED_FIGURES` and `EVIDENCE_TODO` mean figures still need an origin or a real value.

### Step 4: Dual-Format Rendering
Once audited and approved:
```bash
python3 cli.py build --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json --format all
```
Deliverables produced:
- `output/presentation.pptx` (Editable vector shapes, formatted tables, vector charts, speaker notes with sources);
- `output/presentation.html` (Standalone single-file HTML that works offline, with `N`-key Cognitive Inspector).

A plain `build` is for drafts: figures with no source carry an amber `待核` badge, which is the honest marker of work still to do. To ship, use `--final`: it refuses to build while any figure lacks a source or is a placeholder, and hides the badges.

**Motion is off by default.** Add `--motion narrative` only for a deck that will be presented live (types: `reveal`, `contrast`, `build`; see the [CLI reference](cli_reference.md)). A deck for reading should have none. Keynote playback is unverified.

### Step 4.5: Verify What Was Built (v3.5, v3.8)
The audit sees the blueprint, not the result. Check the deliverables:
```bash
python3 cli.py render-check --pptx output/presentation.pptx --html output/presentation.html --render
```
It renders in PowerPoint and Chrome and reports overflow, wrapped titles, empty bands, low contrast and animations PowerPoint does not recognise. `build` already runs the static layout lint and prints warnings.

### Step 5: Always-in-Sync Tracking
At the start of subsequent conversation turns, the Agent runs:
```bash
python3 cli.py sync --target output/presentation.pptx
```
If changes are detected:
> *"I noticed you refined the headline on Slide 3 in PowerPoint to highlight the 15% latency reduction. I have synchronized our state with your changes. How would you like to proceed?"*

---

## 4. Prompt Engineering Patterns

### Triggering Full Strategy Planning
```text
I need to prepare a 6-slide executive presentation on our company's cloud-native modernization strategy. 
Target audience: Enterprise Architecture Committee.
Core thesis: Migrating from monolithic VMs to a containerized service mesh cuts infrastructure cost by 40% while achieving 99.99% availability.
Attached is our background brief (architecture_notes.md) and corporate PPT template (company_template.pptx).
Please guide me through undo-ppt.
```

### Triggering Rapid Draft Generation
```text
Generate a quick 5-slide pitch deck for our AI Developer Tooling startup using undo-ppt. 
Include a bento comparison card, an architecture stack, a KPI metrics spotlight, and a timeline roadmap. 
Deliver both PPTX and HTML.
```
