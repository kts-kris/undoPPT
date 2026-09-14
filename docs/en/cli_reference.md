# undoPPT CLI Reference Manual

This manual documents the unified command-line interface (`cli.py`) for the `undoPPT` Super Skill and automation engine (v3.1.0).

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

Deeply deconstructs an enterprise PowerPoint template. Extracts geometry bounds for title and body slots, detects background canvas luminance to infer light/dark mode, and dumps embedded raster and vector media into `.undoppt/assets/`.

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

## 7. `demo` (Showcase Pipeline)

Runs a comprehensive demonstration that highlights the complete cognitive pipeline, compiles all 15 layout primitives, renders native vector charts and tables, injects speaker notes, and generates the standalone HTML drawer.

```bash
python3 cli.py demo
```
