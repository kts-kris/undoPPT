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
│ 1. Cognitive Contract Probe (Q1-Q4)  ➔  Clarify thesis, audience & goals    │
│ 2. Master Template Deconstruction    ➔  Decompile template AST & slots      │
│ 3. Blueprint Authoring & Audit       ➔  Compose 15-primitive JSON & check   │
│ 4. Dual-Format Rendering             ➔  Generate PPTX (Notes) & HTML        │
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

---

## 3. Rhythm A: Step-by-Step SOP

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

### Step 3: Blueprint Composition & Auditing
The Agent composes `.undoppt/blueprint.json` conforming to the [Blueprint Specification](blueprint_specification.md), mapping each slide into one of the 15 layout primitives.

The Agent immediately triggers the quality auditor:
```bash
python3 cli.py audit --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json
```
If the overall score is below 85, the Agent refines headlines into action-first statements and reinforces quantitative evidence.

### Step 4: Dual-Format Rendering
Once audited and approved:
```bash
python3 cli.py build --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json --format all
```
Deliverables produced:
- `output/presentation.pptx` (Editable vector shapes, formatted tables, vector charts, speaker notes);
- `output/presentation.html` (Standalone single-file HTML with `N`-key Cognitive Inspector).

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
