# undoPPT v3.2.0 Product Requirements Document (PRD)
## Scenario Anti-Patterns & Motion Architecture

> English | [简体中文](../../PRD_v3.2_SCENARIO_REDLINES_AND_ANIMATION.md)

> **Correction (2026-10-06, v3.8.0)**: this is a historical requirements document and is kept as written. Its description of native `<p:timing>` click-step animation working in Office / Keynote / WPS does **not** hold: PowerPoint recognised 0 animation objects in the animation XML described here. v3.8.0 rewrote it, made it off by default and kept only three narrative types; see the [v3.8 PRD](PRD_v3.8_SKIN_AND_POISE.md) and the [CHANGELOG](../../../CHANGELOG.md).

> **Further corrections (2026-10-09, checked against v3.8.0 code and PowerPoint)**:
> 1. `--motion staged` (slide staging, §4.2.3) was never implemented. Today `--motion` accepts only `off` / `narrative`; `motion_pace: "staged"` is kept as an alias of `narrative`.
> 2. The eight rhythm names in the §4.2.3 table (`stagger`, `bottom_up`, `sequential`, `quadrant_reveal`, `step_climb`, `horizon_unfold`, `count_spotlight`, `row_by_row`) do not exist in the code. v3.8 reduced animation to `reveal` / `contrast` / `build`.
> 3. The "honesty bonus" for `[待实测]` / `[设计预估]` markers (§6.1 item 3) was not implemented. v3.7 replaced it with the `source` / `status` provenance model (a figure without a source is flagged "to verify").
> 4. HTML sub-step reveal exists, but is off by default: press `S` to turn on "Step: ON"; with it off, Space simply moves to the next slide.
> 5. Slide transitions (§4.2.2) are confirmed: PowerPoint reported an entry effect of "fade" on all 8 slides of the demo. Keynote and WPS playback were not verified.

---

## 1. Document Metadata

* **Product**: undoPPT (presentation deconstruction and reconstruction agent)
* **Version**: v3.2.0
* **Written**: 2026-09-17
* **Status**: Approved / implementing
* **Core themes**:
  1. Draw on the scenario pitfalls of `open-kimi-ppt-skill` to build a **"six-scenario anti-pattern red-line system"** and an automated audit net that eliminates hollow AI boilerplate and fake evidence;
  2. Establish a **"motion presentation and stepwise timing architecture"** that honours "decouple soft cognition from hard constraints" and "cognitive restraint", giving PPTX native slide transitions and an HTML step-by-step presenting mode.

---

## 2. Problem Statement and Background

### 2.1 Two chronic ailments of AI-generated decks
Deck generation driven by large models commonly has two extreme defects in content and audience experience:

```
┌────────────────────────────────────────────────────────┐     ┌────────────────────────────────────────────────────────┐
│     Ailment 1: inflated content and "AI jargon"        │     │   Ailment 2: no motion, or too much motion             │
├────────────────────────────────────────────────────────┤     ├────────────────────────────────────────────────────────┤
│ • Habitual formulas such as "not only X but Y", "X is  │     │ • Traditional tools are either wooden static slices    │
│   Y", "closed loop", "lever";                          │     │   with no visual guidance for live talks;              │
│ • Technical plans talk of "high availability" with no  │     │ • or imitate web effects with dizzying spins and zooms │
│   metric distribution, failure boundary or rollback;   │     │   that steal the show;                                 │
│ • Business pitches are grand narratives with no unit   │     │ • none gives step-by-step reveal while keeping native  │
│   economics and faked test data.                       │     │   Office compatibility in PPTX.                        │
└────────────────────────────────────────────────────────┘     └────────────────────────────────────────────────────────┘
```

### 2.2 Lessons from open-kimi-ppt-skill
Studying `open-kimi-ppt-skill` in reverse revealed two standout strengths:
1. **Scenario guides with strict "pitfall red lines" (General Prohibitions)**: very strict "anti-boilerplate" rules for finer scenarios such as engineering, management reports and academic research (no common AI sentence patterns, architecture diagrams must mark call direction and failure paths, no meaningless card walls);
2. **Systematic exploration of motion**: not only a smooth fade transition injected by default on PPTX export, but also in-page element entrance timing explored in the DSL.

### 2.3 undoPPT's advanced positioning
While borrowing both, `undoPPT` strictly keeps its foundations: **"never make the agent guess pixel coordinates"** and **"100% local offline closed-loop generation"**:
* The scenario guides' red-line rules are not just prompt constraints but are further **settled into deterministic code rules of `cli.py audit` (Blacklist & Rules Engine)**;
* Motion avoids fragile effects that break Office compatibility; it builds **"slide transition + cognitive disclosure timing for the 15 primitives (Primitive Staged Disclosure)"**, keeping PPTX 100% natively compatible while giving the single-file HTML delivery an unmatched live step-by-step presenting experience.

---

## 3. Feature Epics

| Epic | Module | Feature | Priority | Summary |
| :--- | :--- | :--- | :--- | :--- |
| **EPIC-01** | **Content and audit** | Code interceptor for generic AI tone and jargon | **P0** | A built-in jargon regex library; the auditor recognises and blocks "not only X but Y", "lever / empower / closed loop" and the like |
| **EPIC-02** | **Scenario rules** | Dedicated red-line handbook and rules for the 6 archetypes | **P0** | Hard evidence and logic red lines for strategy, technology, pitch, résumé, teaching and general reporting |
| **EPIC-03** | **Scenario rules** | Fake-evidence and fake-data interception | **P0** | No invented benchmarks; missing data must be marked `[待实测]` (to be measured); the auditor penalises empty adjectives |
| **EPIC-04** | **Motion** | Native PPTX slide transition | **P0** | Per OOXML, inject `<p:transition>` into PPTX, supporting fade/push/wipe |
| **EPIC-05** | **Motion** | Cognitive disclosure timing for the 15 primitives (Staged Reveal) | **P1** | Define appearance beats that fit cognitive psychology for bento, architecture stack, timeline, ladder, matrix and other primitives |
| **EPIC-06** | **Presenting** | HTML single-file step presenting mode | **P1** | The HTML deck reveals the components inside a primitive on Space / right arrow, giving visual focus when presenting live |
| **EPIC-07** | **Spec** | Blueprint Schema v3.2 upgrade | **P0** | Add `transition_effect` and `motion_pace` fields, backward compatible |

---

## 4. Detailed Requirements

### 4.1 Scenario Anti-Pattern Red Lines

#### 4.1.1 General red lines
All decks generated for any scenario must follow these red lines; violations are warned and penalised directly in `cli.py audit`:

1. **Language red line (no AI tone or empty words)**:
   - Forbidden patterns: *"not only … but also …"*, *"… is the cornerstone / the only way of …"*, *"why / on what basis / how"*, *"N battlefields / N-dimensional paths"*.
   - Forbidden empty management jargon: *"打法"* (play), *"闭环"* (closed loop), *"抓手"* (lever), *"赋能"* (empower), *"底层逻辑"* (underlying logic), *"颗粒度"* (granularity), *"对齐"* (align, when no concrete action follows), *"盘活"*, *"解构"*, *"破局"* and other filler that adds no information.
2. **Title-first red line (Action Titles)**:
   - Purely neutral, passive names are forbidden: *"Current analysis"*, *"Background"*, *"System architecture"*, *"Thoughts and exploration"*, *"Summary and review"* and other opinion-free titles.
   - Titles must be **verb-object phrases or conclusion-first sentences**, such as *"Pain point: the monolith avalanches at a peak of 50,000 QPS"*, *"Plan: three-layer decoupling and sharding cut latency to 8ms"*.
3. **Truth-in-Evidence**:
   - Forging benchmarks, inventing metrics and fabricating cases is forbidden.
   - When real data is missing, mark it `[待实测]` (to be measured), `[业务假设]` (business assumption) or `[行业参考]` (industry reference); never disguise invention as evidence with a precise-looking decimal.
   - Subjective adjectives alone (*"extremely high performance"*, *"super stability"*) are forbidden; a benchmark measure must come with them (*"P99 < 15ms"*, *"SLA 99.99%"*).
4. **Visual and structural de-noising red line**:
   - No meaningless walls of cards to fill space;
   - No deck that uses only rigid three-way or four-way splits throughout;
   - No overuse of blue-purple neon or glossy gradients that disturb reading.

#### 4.1.2 Pitfall red lines specific to the 6 archetypes

```text
┌───────────────────────────┬──────────────────────────────────────────────────────────────────┐
│ Archetype                 │ Specific red lines and hard quality constraints                  │
├───────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 1. Strategic planning     │ • No unbounded grand vision; an explicit "Not-to-do list"        │
│    strategic_planning     │ • A strategy matrix needs clear X/Y axis definitions and         │
│                           │   concrete trade-off actions per quadrant                        │
│                           │ • Three horizons (H1/H2/H3) must state resource split and exit   │
│                           │   criteria per stage                                             │
├───────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 2. Technical architecture │ • No empty talk of "high availability / microservices"; state    │
│    tech_architecture      │   SLA, throughput, latency distribution (P50/P99)                │
│                           │ • Stacks and call chains must show control-flow / data-flow      │
│                           │   boundaries and external dependencies                           │
│                           │ • Provide failure recovery, circuit-breaking and a clear         │
│                           │   Rollback Plan                                                  │
│                           │ • Option comparisons must list migration cost, operating         │
│                           │   complexity and technical debt as equal costs                   │
├───────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 3. Business pitch         │ • No castle-in-the-air sizing like "assume 1% of the country     │
│    product_pitch          │   buys"                                                          │
│                           │ • Pain must be concrete, a real blocking point in the target     │
│                           │   user's workflow                                                │
│                           │ • Provide unit economics (LTV/CAC) and an acquisition flywheel   │
│                           │ • Funding milestones bound to deliverables and key validation    │
│                           │   points                                                         │
├───────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 4. Personal résumé /      │ • No job-description laundry lists ("responsible for system      │
│    promotion review       │   maintenance of ...")                                           │
│    personal_resume        │ • Follow STAR (Situation-Task-Action-Result)                     │
│                           │ • Quantify results (hours saved, delivery speed-up, cost saved)  │
│                           │ • Separate personal ownership from team collaboration; no        │
│                           │   claiming credit falsely                                        │
├───────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 5. Education / training   │ • No piling from abstract concept to dogmatic terms; start from  │
│    education_training     │   what the audience already knows                                │
│                           │ • Dissect the blind spots and common errors of the audience      │
│                           │ • Pair each core concept with "typical Anti-pattern vs best      │
│                           │   practice"                                                      │
│                           │ • Provide in-class checks or practice, closing the learning loop │
├───────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 6. General government /   │ • No exhaustive listing of daily affairs; core results and data  │
│    enterprise reporting   │   in large type                                                  │
│    general_informative    │ • When reporting difficulties, give at least one contingency     │
│                           │   plan alongside                                                 │
│                           │ • Follow-up plans must contain a clear WBS schedule, owners and  │
│                           │   resource guarantees                                            │
└───────────────────────────┴──────────────────────────────────────────────────────────────────┘
```

---

### 4.2 Motion Architecture Specification

#### 4.2.1 Guiding principle: cognitive restraint and stepwise focus
* **Serve the audience's cognitive rhythm**: the only value of motion is to help the speaker control where the audience looks, moving cognition along `thesis first ➔ facts unfold ➔ data evidence ➔ summary and decision`.
* **No juggling effects**: spinning, tumbling, violent bouncing and aimless wandering are forbidden; only **Fade, smooth Push and slight-offset Stagger Reveal** are used.

#### 4.2.2 Level 1: Slide Transition
* **Spec fields**:
  * A global `transition_effect` at the blueprint root (default `"fade"`);
  * A slide may override `transition_effect`.
* **Supported effects**:
  * `"fade"` (recommended default): elegant and restrained, smooth cross-fade, 0.4s;
  * `"push"`: pushes left, for timeline progress, evolution ladders or milestones;
  * `"wipe"`: wipes right, for sharp before/after contrasts;
  * `"none"`: instant cut, for minimal printing or quick flipping.
* **PPTX implementation**:
  * Using python-pptx's low-level `oxml`, inject a standard OOXML node into the slide XML tree:
    ```xml
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="fast" advClick="1">
        <p:fade/>
    </p:transition>
    ```
  * Strictly follow the PPTX CT_Slide schema: insert after `<p:cSld>` (and the optional `<p:clrMapOvr>`) and before `<p:timing>`, so the XML passes PowerPoint, WPS and Keynote validation.
* **HTML single-file implementation**:
  * On slide change, add a hardware-accelerated `opacity-0` to `opacity-100` transition through the Tailwind CSS animation container.

#### 4.2.3 Level 2: Cognitive disclosure timing for the 15 primitives (Primitive Staged Reveal)
Timing strategies matched to the human mental rhythm for the core primitives:

| Primitive | Motion rhythm | Disclosure semantics |
| :--- | :--- | :--- |
| `bento_cards` | `stagger` | Cards fade in staggered left to right or by weight; the highlighted key card enters last as the focus |
| `architecture_stack` | `bottom_up` | Infrastructure at the bottom ➔ scheduling base in the middle ➔ business applications on top, stacking layer by layer |
| `timeline` / `process_flow` | `sequential` | Time / flow nodes light up along the main axis, conveying causal progression |
| `matrix_2x2` | `quadrant_reveal` | Axes first ➔ quadrant cards in order of strategic priority |
| `maturity_ladder` | `step_climb` | Climbing from L1 up to maturity, showing the momentum of progression |
| `horizons_curve` | `horizon_unfold` | H1 core business ➔ H2 breakout growth ➔ H3 disruptive long-term, unfolding in turn |
| `metric_spotlight` | `count_spotlight` | The large core number first, the comparison label locking in afterwards |
| `standard_table` | `row_by_row` | After the header is set, the key comparison rows appear one by one |

* **HTML single-file delivery (step presenting mode)**:
  * In the single-file HTML, **"Sub-step Reveal"** works with `Space` or `→`:
  * On first entering a slide, only the headline, subtitle and base frame show;
  * Each light press of Space highlights the next card, architecture layer or timeline node inside the primitive;
  * Only when everything is revealed does the next Space turn to the next slide;
  * `N` slides out the cognitive-dynamics drawer at any time, working seamlessly with the above.
* **PPTX compatibility and fallback**:
  * PPTX by default shows each scene complete out of the box (so exports can be printed, distributed and edited at once), injecting a slide-level transition while keeping vectors and formats lossless;
  * An advanced mode offers the `--motion staged` option, which arranges pages with complex timed primitives into progressive slices (Slide Staging), so any projector can step through with a single key and no plug-in.

---

## 5. Blueprint Schema v3.2 Extension

On top of the existing `blueprint.json` spec, these optional fields are added, 100% backward compatible:

```json
{
  "contract": {
    "core_thesis": "...",
    "audience": { ... },
    "knowledge_delta": { ... },
    "target_outcomes": { ... }
  },
  "presentation_config": {
    "transition_effect": "fade | push | wipe | none",
    "motion_pace": "staged | instant",
    "theme_preset": "modern_bento"
  },
  "slides": [
    {
      "layout_type": "bento_cards",
      "narrative_arc": "conflict",
      "mission": "...",
      "transition": "...",
      "action_title": "...",
      "core_evidence": "...",
      "title": "...",
      "subtitle": "...",
      "transition_effect": "fade",
      "motion": {
        "staged_reveal": true,
        "stagger_delay_ms": 150
      },
      "cards": [ ... ]
    }
  ]
}
```

---

## 6. Audit and Acceptance Criteria

### 6.1 Automated audit interception (`cli.py audit`)
1. **Jargon interception rate**: a blueprint containing words from the jargon library ("not only X but Y", "lever closed loop") must be warned and flagged 100% by the auditor, with a deduction in `structural_score` or `semantic_score` and a clear fix suggestion;
2. **Scenario-specific rule detection**: a technical-architecture blueprint with no quantified measure or SLA anywhere loses "evidence density" points and is warned;
3. **Tolerance for honesty markers**: a blueprint with explicit assumption markers (such as `[待实测]`, `[设计预估]`) is not treated as fake evidence and earns an integrity bonus.

### 6.2 Dual-target motion acceptance
1. **PPTX playback**: the exported `presentation.pptx`, played full-screen in Microsoft PowerPoint, Apple Keynote and WPS Office, should show a smooth fade (or the specified push) between slides, with no XML error or corruption warning;
2. **HTML step presenting**: the exported `presentation.html`, opened in Chrome/Safari/Edge/Firefox, should reveal primitives in sequence on Space, open the cognitive drawer on `N`, and adapt to mobile and PC.

---

## 7. Implementation Roadmap

1. **Milestone 1 (Week 1)**:
   - Build the `BUZZWORD_BLACKLIST` filter library and the anti-boilerplate rule engine for the 6 scenarios;
   - Upgrade `core/content_auditor.py` and `core/semantic_auditor.py`.
2. **Milestone 2 (Week 1)**:
   - Write `docs/zh/scenario_anti_patterns.md` and update `SKILL.md`;
   - Update the `DESIGN_PHILOSOPHY_zh.md` white paper with the two new principles.
3. **Milestone 3 (Week 2)**:
   - Implement standard OOXML `<p:transition>` injection in `core/pptx_builder.py`;
   - Implement smooth CSS transitions and step-presenting control in `core/html_builder.py`.
4. **Milestone 4 (Week 2)**:
   - Write unit tests and demo documents, and run end-to-end regression.
