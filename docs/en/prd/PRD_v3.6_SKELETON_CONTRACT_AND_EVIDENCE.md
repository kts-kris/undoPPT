# undoPPT v3.6.0 Product Requirements Document (PRD)
## Skeleton: Ask First, Evidence Before Pages

> English | [简体中文](../../PRD_v3.6_SKELETON_CONTRACT_AND_EVIDENCE.md)

> **Later changes**: the data-provenance work listed for v3.7 shipped as planned. In §6, the "Keynote" verification planned for v3.8 was not achieved; see the [v3.8 PRD](PRD_v3.8_SKIN_AND_POISE.md).

---

## 1. Document Metadata

* **Product**: undoPPT (presentation deconstruction and reconstruction agent)
* **Version**: v3.6.0
* **Written**: 2026-10-06
* **Status**: Released / in production
* **Core goals**:
  1. Move the quality gate **earlier**: when information is insufficient, do not generate; ask the user first;
  2. Give the agent **a model outline to compare against**: for each of the 12 enterprise scenarios, the audience gate, what must be decided, and the evidence each page needs;
  3. Let the engine recognise pages whose **content cannot carry the layout** (thin flesh), not just check structure;
  4. Fix the renderer defect that **silently dropped text**, so every string written in the blueprint reaches the output;
  5. 100% backward compatible: no existing blueprint field changes; everything new is optional behaviour.

---

## 2. Background and Problem Analysis

Of the product's four layers, the skeleton (theme and outline) sets the ceiling. Before v3.5, skeleton quality depended entirely on the rule engine and the agent's improvisation, and **nothing stopped generation when information was insufficient**.

Measured before v3.6:

| # | Symptom | Root cause |
|---|---|---|
| 1 | For the input "make me a report about AI" the planner produced 6 pages and the audit gave **91.7, grade A**; the core thesis read as boilerplate | The audit only sees blueprint structure and is blind to "garbage in"; the planner fills in with templates and clichés |
| 2 | Planner pages often had only three short headings, which could not carry the chosen layout | No check on whether the body is sufficient |
| 3 | `columns[].points` written in a blueprint produced not one bullet in the output | The spec and planner use `points`/`tag`; the renderer reads `bullets`/`badge` |
| 4 | In a blueprint `cross_mapping` page 90% of the text did not appear in the PPTX; `horizons_curve` 74%, `content_columns` 60%, `maturity_ladder` 50%, `matrix_2x2` 44% | Same: field names of five primitives differed between spec and renderer, and the fallback was silent |
| 5 | "Internal tech sharing" requests were classified as general reports | Missing keywords in scenario classification |

Items 3 and 4 are **content correctness** problems and worse than layout problems: what users cannot see, they cannot notice is missing.

---

## 3. Requirements

### 3.1 Cognitive contract probe `cli.py probe`
- **R1** Before writing any page, judge from the user's request (and optional reference documents): the scenario; whether Q1 thesis, Q2 audience and stance, Q3 knowledge gap and Q4 end action are known; and whether the scenario's 3-4 specific facts are known.
- **R2** Q2 (who is listening) and Q4 (what they should do) are **blocking**: if either is missing, `ready` must be false.
- **R3** `ready` = known slots ≥ 70% and no blocking item missing.
- **R4** Return a prioritised list of questions: blocking items first, general contract next, scenario facts last.
- **R5** All 12 enterprise scenarios have their own fact checks (project charter asks about budget and alternatives, QBR about variance and attribution, RFC about rollback, post-mortem about the timeline, promotion about net contribution, and so on).
- **R6** `plan` / `generate` print the same hint when completeness is low but **do not abort** (backward compatibility).
- **R7** The probe is heuristic: it judges whether something is **mentioned**, not whether it is **correct**. Docs and output say so.

### 3.2 Model outlines `docs/en/scenario_outlines.md`
- **R8** One per each of the 12 scenarios: audience gate, what must be decided, a six-page outline (primitive, example conclusion-style title, the page's mission, **required flesh**), red lines.
- **R9** Page order and primitives match what the planner actually outputs; tests keep the doc from drifting.
- **R10** The doc states the overriding rule: **page count follows evidence, not evidence follows page count**.

### 3.3 Flesh budget audit
- **R11** `THIN_CONTENT_P<n>`: the page body (excluding header title) is shorter than the primitive's minimum. Each minimum is about half of the planner's own lowest output, catching only clearly thin pages.
- **R12** `EVIDENCE_BUDGET_P<n>`: on a metrics page, fewer than half the metrics carry a number.
- **R13** Cover pages and native charts are exempt; the two together cost at most 12 points.

### 3.4 Blueprint compatibility layer `core/blueprint_compat.py`
- **R14** Map the spec's and planner's fields to the renderer's: `columns[].points→bullets`, `tag→badge`; `cross_mapping` `layer/current/target/action`; `horizons` `horizon/name/kpi`; `levels` `step/focus/target`; `quadrants` `desc/tag` and `axes`.
- **R15** Fill only when the renderer field is absent, never overwrite existing fields, do not mutate the argument; shared by PPTX and HTML.
- **R16** Regression test: in blueprints generated for the 12 scenarios, on the affected primitives, every string must appear in both the PPTX and the HTML.

### 3.5 Other
- **R17** `SKILL.md` phase 1 is rewritten as "insufficient information, do not generate", with the probe flow and the "ask first" loop; `plan`/`generate` are positioned as fallback.
- **R18** Fix scenario classification for "tech sharing / internal sharing / experience sharing"; the blueprint version comes from `core.__version__`.
- **R19** The architecture stack's layer note is no longer hidden at 4 layers.

---

## 4. Acceptance Criteria

| Criterion | Result |
|---|---|
| All tests pass | 68 (44 existing + 24 new) |
| Vague requests ("make a PPT", "make me a report about AI") | `ready: false`, blockers Q2 and Q4, completeness ≤ 25% |
| Well-informed requests | `ready: true` |
| Prompts for the 12 scenarios classified correctly | Yes (including the previously misjudged "internal tech sharing") |
| Text fidelity on affected primitives (12 scenarios × PPTX/HTML) | 0 lost (v3.5: cross_mapping 90%, horizons 74%, columns 60%, ladder 50%, matrix 44%) |
| Mutation check: disable the compatibility layer | Both fidelity tests fail |
| The planner's own output | Triggers neither `THIN_CONTENT` nor `EVIDENCE_BUDGET`; all 12 decks pass v3.5's static lint and the PowerPoint blank-band check |
| Outline doc vs planner | Primitive sequences match for all 12 scenarios |

---

## 5. Out of Scope and Known Limits

- The probe judges only whether something is **mentioned**, not whether it is **correct**; it cannot replace asking the user.
- The planner is still a rule engine with no real insight. This version demotes it to fallback and does not rewrite it.
- When `options` are present the decision closing page does not draw `points` (by design: options, recommendation and the approval list fill the page).
- Data source tracing, the "to verify" marker and `ingest` are left to v3.7.

---

## 6. Follow-up Roadmap

| Version | Theme | Highlights |
|---|---|---|
| v3.7.0 | Flesh | Optional `source` / `status` in the blueprint; unsourced numbers marked "to verify"; `cli.py ingest` extracts sourced data points from documents and tables; the demo shows the decision loop |
| v3.8.0 | Skin polish and poise | Type hierarchy and contrast rules; trial with real corporate templates; three narrative animations verified in PowerPoint / Keynote |
