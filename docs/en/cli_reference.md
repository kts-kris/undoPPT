# undoPPT CLI Reference Manual

This manual documents the unified command-line interface (`cli.py`) for the `undoPPT` Super Skill and automation engine (v3.8.0).

---

## Command Overview

```bash
python3 cli.py <command> [arguments...]
```

### Available Subcommands

| Command | Purpose | Primary Inputs | Deliverables |
| :--- | :--- | :--- | :--- |
| `plan` | Autonomous cognitive blueprint authoring | Prompt, Reference Doc | `.undoppt/blueprint.json` |
| `generate` | One-shot end-to-end presentation authoring | Prompt, Doc, Template | `presentation.pptx`, `presentation.html` |
| `audit` | Structural & semantic causal quality auditing | Blueprint, Design Tokens | Audit score report & diagnostic findings |
| `undo` | Master template deconstruction & token extraction | Enterprise `.pptx` | `.undoppt/design_tokens.json`, assets |
| `build` | Dual-format vector presentation rendering | Blueprint, Design Tokens | `presentation.pptx`, `presentation.html` |
| `sync` | Detect external manual edits by human presenter | Target `.pptx` file | Semantic AST diff summary |
| `ingest` | Extract data points with their origin from a document | `.md` / `.txt` / `.csv` | `.undoppt/facts.json` |
| `cite` | Link blueprint figures to extracted facts and record sources | Blueprint, facts JSON | Blueprint with `source` fields |
| `probe` | Check whether a request has enough information before authoring | Prompt, optional Reference Doc | Readiness, missing facts, questions to ask |
| `render-check` | Verify the layout of built deliverables | `.pptx`, `.html` | Findings report, rendered PNGs |
| `demo` | Run full showcase demonstration pipeline | *None* | Complete audited demo presentations |

---

## 1. `plan` (Autonomous Cognitive Planner)

Analyzes user intent, classifies the request into one of 6 universal scenarios, extracts factual entities from external reference documents, and composes an audited `blueprint.json`.

```bash
python3 cli.py plan --prompt "<goal>" [options]
```

### Arguments

| Flag | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `--prompt` | **Yes** | — | Core presentation objective, topic, or narrative directive. |
| `--input-doc` | No | `None` | Path to Markdown or text document (`.md`, `.txt`) for factual grounding. |
| `--context` | No | `None` | Additional audience background, time limits, or styling constraints. |
| `--out` | No | `.undoppt/blueprint.json` | Destination filepath for the synthesized blueprint JSON. |

### Example

```bash
python3 cli.py plan \
  --prompt "Enterprise Cloud Migration & Zero Trust Roadmap" \
  --input-doc internal_migration_brief.md \
  --out .undoppt/blueprint.json
```

---

## 2. `generate` (One-Shot Autonomous Pipeline)

Executes the entire end-to-end pipeline in a single invocation:
1. Deconstructs user template (if provided) or loads preset tokens;
2. Ingests reference document facts;
3. Synthesizes a structured cognitive blueprint;
4. Audits the blueprint and triggers self-correction if score < 85;
5. Renders native vector PPTX with speaker notes and single-file HTML;
6. Initializes the sync baseline.

```bash
python3 cli.py generate --prompt "<goal>" [options]
```

### Arguments

| Flag | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `--prompt` | **Yes** | — | User prompt / presentation objective. |
| `--input-doc` | No | `None` | Path to external reference document for factual grounding. |
| `--context` | No | `None` | Extra constraints or notes. |
| `--template` | No | `None` | Optional path to enterprise PowerPoint template (`.pptx`) to deconstruct. |
| `--tokens` | No | `presets/modern_bento.json` | Fallback design tokens JSON path if no template is provided. |
| `--format` | No | `all` | Output format: `pptx`, `html`, or `all`. |
| `--out` | No | `output` | Directory where deliverables are saved. |

### Example

```bash
python3 cli.py generate \
  --prompt "Series B Pitch Deck for Autonomous AI Agents" \
  --input-doc investor_deck_notes.md \
  --template templates/company_branding.pptx \
  --format all \
  --out output/
```

---

## 3. `audit` (Cognitive Quality & Causal Auditor)

Performs a rigorous, objective quality inspection of the presentation blueprint. Evaluates structural budget compliance, narrative arcs, causal rhetorical transitions, core thesis centroid alignment, and empirical evidence weighting.

```bash
python3 cli.py audit --blueprint <blueprint.json> [options]
```

### Arguments

| Flag | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `--blueprint` | **Yes** | — | Path to the blueprint JSON file to inspect. |
| `--tokens` | No | `presets/modern_bento.json` | Design tokens path for density budget validation. |

### Example

```bash
python3 cli.py audit --blueprint .undoppt/blueprint.json
```

### Sample Output

```text
================================================================
 COGNITIVE & NARRATIVE DYNAMICS QUALITY AUDIT REPORT (v3.1.0)
================================================================
 Overall Score:    94.5/100 (Grade: EXCELLENT)
 Structural Score: 95.0/100
 Semantic Score:   94.0/100

 [Detailed Sub-Scores]
   • Causal Cohesion:    95.0/100
   • Thesis Alignment:   92.5/100
   • Empirical Evidence: 95.0/100
   • Objection Resolv:   93.5/100

 [Structural Redlines]
   [✓] 6 slides inspected across 6 layout primitives.
   [✓] Zero passive titles detected. All slides use action-first conclusions.
   [✓] All slides conform to content budget constraints.

 [Deliverable Status]
   Status: APPROVED FOR RENDERING
================================================================
```

---

## 4. `undo` (Template Master Decompiler)

Deconstructs a PowerPoint template into design tokens. As of v3.8 it reads the template's **real theme**: the colour scheme (`ppt/theme/theme1.xml`), the master's colour map and background (resolving scheme colours with `lumMod` / `lumOff`), and the theme fonts (major, minor and the East Asian font). The palette, light/dark mode and fonts come from there; `theme_source` in the output records what was read.

Before v3.8 `undo` only scanned explicit RGB fills on slides, which real templates do not have, so every template came back as the same light blue theme (even a dark one). The extracted tokens now go through the design check (contrast, minimum sizes) and any fixes are listed in `design_notes`. The brand colour (`palette.primary`) is never rewritten; the margins are clamped to what the builders' grid can use. Slide geometry and embedded media are also extracted.

The builders always draw a 16:9 slide: a 4:3 template contributes its colours and fonts, not its aspect ratio.

```bash
python3 cli.py undo --template <template.pptx> [options]
```

### Arguments

| Flag | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `--template` | **Yes** | — | Path to the input `.pptx` template file. |
| `--out` | No | `.undoppt/design_tokens.json` | Filepath where extracted tokens will be stored. |

### Example

```bash
python3 cli.py undo \
  --template corporate_theme.pptx \
  --out .undoppt/design_tokens.json
```

---

## 5. `build` (Dual-Format Vector Presentation Builder)

Renders the presentation from a validated blueprint and design tokens. Outputs 100% native vector PowerPoint shapes, formatted tables, vector charts, and speaker notes, alongside a single-file standalone HTML presentation.

```bash
python3 cli.py --blueprint <blueprint.json> [options]
```

### Arguments

| Flag | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `--blueprint` | **Yes** | — | Path to the validated blueprint JSON. |
| `--tokens` | No | `presets/modern_bento.json` | Design tokens or master template tokens JSON. |
| `--format` | No | `all` | Output format: `pptx`, `html`, or `all`. |
| `--out` | No | `output` | Output directory. |
| `--motion` | No | `off` | `narrative` turns on the three narrative animations (see below). |
| `--final` | No | off | Delivery mode (v3.7): refuse to build while figures lack a source. |

### Narrative animations (v3.8)

Motion is **off by default**. `--motion narrative` (or `presentation_config.motion: "narrative"`) gives each slide the animation that suits its layout; a slide can choose with `motion: {"type": "reveal" | "contrast" | "build" | "none"}`.

| Type | One click is... | Used for |
| :--- | :--- | :--- |
| `reveal` | the next idea, in reading order | lists, roadmaps (node and card together), stacks (bottom-up), decision pages |
| `contrast` | first the alternatives, then the recommended one | cards with a `highlight`, 2x2 matrices, current-vs-target mappings |
| `build` | the next piece of data | KPI cards (wipe in), a chart and then its takeaway |

The timing tree follows what PowerPoint itself writes (each click is an outer step with `delay="indefinite"`; the first effect is a `clickEffect`, the rest `withEffect`). `render-check --render` asks PowerPoint how many shapes it recognises as animated and reports `MOTION_NOT_RECOGNIZED` / `MOTION_INVALID` on a mismatch. v3.3-v3.7 wrote a tree PowerPoint did not recognise at all (0 animated shapes); `motion_pace: "staged"` is kept as an alias for `narrative`. In the HTML, count-up and flowing-pulse effects are decorative and run only in narrative mode; the `S` step mode is always available. Keynote could not be verified from a script: it does not expose builds to automation.

### Example

```bash
python3 cli.py build \
  --blueprint .undoppt/blueprint.json \
  --tokens .undoppt/design_tokens.json \
  --format all \
  --out output
```

---

## 6. `sync` (Collaboration Watcher & Diff Inspector)

Compares current delivery files against recorded SHA-256 baseline fingerprints. If manual modifications have occurred (e.g. text edited in PowerPoint), it performs AST inspection and reports changes.

```bash
python3 cli.py sync [options]
```

### Arguments

| Flag | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `--target` | No | `output/presentation.pptx` | Target presentation file to inspect. |

### Example

```bash
python3 cli.py sync --target output/presentation.pptx
```

---

## 7. `ingest` and `cite` (Data Provenance, v3.7)

`ingest` pulls every figure out of a source document and keeps where it came from; `cite` writes those origins into a blueprint.

```bash
python3 cli.py ingest --input-doc notes.md --out .undoppt/facts.json
python3 cli.py cite --blueprint .undoppt/blueprint.json --facts .undoppt/facts.json
```

Each fact: `{"label": "营收", "value": "1.2亿", "context": "...", "section": "立项", "source": "notes.md:L3"}`. Markdown and text give `file:L<line>`; CSV gives `file:第<row>行·<column>` and uses a unit in the header, e.g. `数值(万元)` + `1200` becomes `1200万元`. Excel is rejected: export the sheet to CSV.

`cite` matches blueprint figures to facts by value. A slide-level `source` covers every figure on the slide, so it is written **only when every unsourced figure on that slide was matched**; a partial match writes `source_candidates` instead and the figures stay flagged. `cite` never sets `status`: a match shows the number appears in the document, not that it supports the same claim.

`build --final` is the delivery mode: it refuses to build (exit 1) while any figure lacks a source or is `todo`, and hides the `待核` badges. A plain `build` keeps the badges so a draft shows what still needs data.

---

## 8. `probe` (Cognitive Contract Readiness, v3.6)

The audit scores a blueprint's structure and cannot tell a deck built from real material from one built from nothing: a request as thin as "帮我做一份关于 AI 的汇报" still scores 90+. `probe` runs *before* authoring and reports what is still unknown.

It classifies the scenario (one of the 12 enterprise scenarios or a generic archetype), then checks four universal slots (Q1 thesis, Q2 audience, Q3 knowledge gap, Q4 decision) plus three or four scenario-specific facts (a QBR needs the variance, an RFC needs the rollback plan, a post-mortem needs the timeline). Q2 and Q4 are *blocking*: without knowing who decides and what they must decide, do not generate.

```bash
python3 cli.py probe --prompt "智能客服业务立项答辩，申请首期预算，预期人效提升 40%"
python3 cli.py probe --prompt "..." --input-doc notes.md --json
```

| Flag | Description |
| :--- | :--- |
| `--prompt` | The user's request, verbatim. |
| `--input-doc` | Reference document; its text counts as evidence. |
| `--context` | Extra context text. |
| `--json` | Machine-readable output (`ready`, `readiness`, `blocking`, `slots`, `questions`). |

`ready` is true when at least 70% of the slots are known and no blocking slot is missing. `questions` lists what to ask, blocking questions first. The check is a heuristic: it detects whether a fact is *mentioned*, not whether it is right. `plan` and `generate` print the same hint when readiness is low but never stop.

---

## 9. `render-check` (Layout Verification, v3.5)

The audit scores a blueprint; it cannot see the rendered result. `render-check` closes that gap in two layers:

1. **Static lint** (always runs, no renderer needed): measures text against its container and reports defects a viewer would see.
2. **Real renders** (`--render`): PPTX through PowerPoint (macOS, AppleScript) or LibreOffice, converted to PNG and checked for empty bands; HTML through headless Chrome at 1600x900 and 500x900, reading back how far content extends past the canvas.

`build` already runs the static lint and prints non-fatal warnings.

```bash
python3 cli.py render-check --pptx output/presentation.pptx
python3 cli.py render-check --pptx output/presentation.pptx --html output/presentation.html --render
```

### Arguments

| Flag | Default | Description |
| :--- | :--- | :--- |
| `--pptx` | — | PPTX to lint (and render with `--render`). |
| `--html` | — | HTML to check. Needs `--render` and Chrome. |
| `--render` | off | Also render with PowerPoint/LibreOffice and headless Chrome. |
| `--engine` | auto | `powerpoint` or `libreoffice`. |
| `--slides` | 0 | Slide count for the HTML check when `--pptx` is not given. |
| `--out` | `.undoppt/render` | Directory for rendered PNGs. |
| `--json` | — | Write the full report to this file. |

Exit code is `1` when any finding is reported, `0` otherwise.

### Finding codes

| Code | Meaning |
| :--- | :--- |
| `OUT_OF_BOUNDS` | A shape extends past the slide edge. |
| `TITLE_WRAPS` | The title needs more than one line even at the minimum size (22pt). Shorten it. |
| `TEXT_OVERFLOW` | Text is estimated taller than the card that holds it. Cut text or split the slide. |
| `TEXT_CROSSES_SHAPE` | A text block straddles the edge of another shape. |
| `TEXT_OVERLAP` | Two text blocks overlap. |
| `BLANK_BAND` | More than 35% of the slide height is one empty horizontal band (the slide has too little content). |
| `HTML_OVERFLOW_BOTTOM` / `HTML_OVERFLOW_RIGHT` | HTML content extends past the 1340x754 canvas. |

### Setup for `--render`

```bash
pip install -r requirements-dev.txt     # pypdfium2 + pillow (PDF to PNG), pytest
```

PowerPoint is sandboxed and can only write to folders the user has granted, so the checker stages files in `~/Documents/.undoppt_render` and removes them afterwards. The first run may ask for folder access. Without PowerPoint or LibreOffice the PPTX render is skipped and the static lint still runs.

---

## 10. `demo` (Showcase Pipeline)

Runs a comprehensive demonstration that highlights the complete cognitive pipeline, compiles all 15 layout primitives, renders native vector charts and tables, injects speaker notes, and generates the standalone HTML drawer.

```bash
python3 cli.py demo
```
