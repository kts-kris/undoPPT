# undoPPT v3.3.0 Product Requirements Document (PRD)
## Kinetic Dynamics & Interactive Decision Sandbox

> English | [简体中文](../../PRD_v3.3_KINETIC_DYNAMICS_AND_INTERACTION_SANDBOX.md)

> **Correction (2026-10-06, v3.8.0)**: this is a historical requirements document and is kept as written. Its description of native `<p:timing>` click-step animation working in Office / Keynote / WPS does **not** hold: PowerPoint recognised 0 animation objects in the animation XML described here. v3.8.0 rewrote it, made it off by default and kept only three narrative types; see the [v3.8 PRD](PRD_v3.8_SKIN_AND_POISE.md) and the [CHANGELOG](../../../CHANGELOG.md).

> **Further corrections (2026-10-09, checked against v3.8.0 code)**:
> 1. **Implemented as described**: the Presenter HUD on the `P` key (cognitive compass, transition teleprompter, objection playbook), the HTML scenario switcher (conservative / baseline / aggressive), the architecture drill-down modal, and `SyncWatcher.analyze_intent_diff`.
> 2. **Not implemented**: the Sensitivity Slider (§4.2.2 item 2) does not exist in the code.
> 3. **Not implemented**: the per-primitive semantic dynamics of §4.1.2 (bottom-up gravity lock, flowing light beam with ripples) and the narrative-arc pacing clock of §4.1.3 (`narrative_arc` timings of 200-250ms / 400ms / 600ms). `narrative_arc` is only shown as a tag. What exists today is the HTML count-up and shimmer, which run only in narrative motion mode (v3.8).
> 4. The sandbox's `scenarios` are used when given in the blueprint; otherwise the switcher derives the three scenarios itself, so they are illustrative unless the author supplies real figures.
> 5. `presentation_config.motion_pace` is kept only as an alias of `narrative`; `kinetic_style` and `enable_sandbox` in §5 are not read by the code.

---

## 1. Document Metadata

* **Product**: undoPPT (presentation deconstruction and reconstruction agent)
* **Version**: v3.3.0
* **Written**: 2026-09-17
* **Status**: Approved / implementing
* **Core goals**:
  1. On motion, fully match the element-level timing choreography of `open-kimi-ppt-skill`, and go a generation beyond it in three directions: **primitive-native semantic dynamics**, **tiered heterogeneous rendering for both targets** and a **narrative speaking-beat clock**;
  2. On interaction, break out of the static canvas: build a **Live Presenter HUD** (a dual-vision cognitive hub for live presenting), a **millisecond intent-reflection flywheel across any toolchain (Intent Reflection)** and an **Active Decision Sandbox**.

---

## 2. Background and Motivation

In v3.2.0, `undoPPT` established the "scenario red-line system" and "native slide transitions". But for high-stakes business roadshows, architecture defences and executive strategy decisions, traditional decks still face three core bottlenecks:

```
┌────────────────────────────────────────────────────────┐     ┌────────────────────────────────────────────────────────┐
│  Bottleneck 1: mechanical, disconnected motion         │     │  Bottleneck 2: one-way delivery, cannot meet challenges│
├────────────────────────────────────────────────────────┤     ├────────────────────────────────────────────────────────┤
│ • Traditional AI tools must hard-code the fly-in and   │     │ • In a live defence, once an executive or judge        │
│   zoom coordinates of every small block;               │     │   interrupts with assumed parameters, a static deck    │
│ • Animation becomes dull art juggling and cannot       │     │   loses its answer at once and the speaker can only    │
│   reflect the inner flow of architecture and data;     │     │   explain weakly in words;                             │
│ • PPTX motion drops frames or shifts across software,  │     │ • The speaker has no live intelligent aid, no causal   │
│   and the HTML side leaves the web's potential unused. │     │   connectives and no ammunition against challenges.    │
└────────────────────────────────────────────────────────┘     └────────────────────────────────────────────────────────┘
```

To solve these, `undoPPT v3.3.0` proposes a two-wheel upgrade built on **"Semantic Dynamics"** and the **"Active Sandbox"**.

---

## 3. Feature Epics

| Epic | Module | Feature | Priority | Summary |
| :--- | :--- | :--- | :--- | :--- |
| **EPIC-01** | **Motion architecture** | Native OOXML `<p:timing>` step-sequence generation in PPTX | **P0** | Automatically build a compliant timing-node tree in PPTX for native click-by-click entrance in Office/Keynote |
| **EPIC-02** | **Motion architecture** | Primitive-native Semantic Dynamics for the 15 primitives | **P0** | Architecture stack rooting downward, timeline light flow, KPI count-up and ladder climb, with no coordinates written by the agent |
| **EPIC-03** | **Motion architecture** | Narrative-arc-aware beat clock (Causal Pacing) | **P1** | Motion delay and speed adapt to `narrative_arc` (conflict crisp and urgent at 250ms, breakthrough with a spreading glow, evidence steady count-up) |
| **EPIC-04** | **Presenting** | Live Presenter HUD | **P0** | In the HTML file, `P` opens a live hub with a cognitive compass, a causal teleprompter and an objection playbook |
| **EPIC-05** | **Presenting** | Active Decision Sandbox | **P0** | Charts and KPIs switch live between "conservative / baseline / aggressive" and redraw dynamically; architecture layers drill down on click |
| **EPIC-06** | **Collaboration** | Millisecond intent-reflection flywheel across toolchains (Intent Reflection) | **P1** | `SyncWatcher` gains a semantic reflection engine that captures the strategic motive behind human tweaks made in local Office/Keynote |

---

## 4. Detailed Requirements

### 4.1 Kinetic Dynamics Architecture

#### 4.1.1 Full parity, and native OOXML timing in PPTX (EPIC-01)
* **Goal**: completely fix the earlier situation where PPTX had only slide transitions and could not reveal in-page elements click by click.
* **Technical spec**:
  - In `core/pptx_builder.py`, use `parse_xml` to build a standard ECMA-376 `<p:timing>` tree:
    ```xml
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
      <p:tnLst>
        <p:par>
          <p:cTn id="1" dur="indefinite" restart="always" nodeType="tmRoot">
            <p:childTnLst>
              <p:seq concurrent="1" nextAc="seek">
                <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                  <p:childTnLst>
                    <!-- key-press entrance time nodes of the components inside a primitive -->
                  </p:childTnLst>
                </p:cTn>
                <p:prevCondLst><p:cond evt="onPrev" delay="0"/></p:prevCondLst>
                <p:nextCondLst><p:cond evt="onNext" delay="0"/></p:nextCondLst>
              </p:seq>
            </p:childTnLst>
          </p:cTn>
        </p:par>
      </p:tnLst>
    </p:timing>
    ```
  - Automatically assign incrementing Shape IDs to bento cards, architecture layers and timeline nodes and link them to a `<p:bldLst>` or `<p:anim>` sequence;
  - When playing in PowerPoint / WPS / Keynote, with no plug-in at all, pressing Space or the left mouse button summons the key components one by one.

#### 4.1.2 Primitive-native Semantic Dynamics for the 15 primitives (EPIC-02)
* **Design principle**: **"Structure decides motion; semantics give it weight."** The agent configures nothing; the engine assembles itself:
  1. **Layered architecture stack (`architecture_stack`)**:
     - Bottom layer, infrastructure (IaaS/data sources): locks into place by gravity from the bottom up;
     - Middle layer (runtime/scheduling): converges and unfolds from left and right toward the centre;
     - Top layer, business applications (gateway/terminals): lit by a spotlight from top to bottom.
  2. **Timeline and flow (`timeline` / `process_flow`)**:
     - The main axis carries a Flowing Light Beam of pulses;
     - Stage nodes trigger a ripple and light up in turn as the beam passes, showing cause and evolution.
  3. **Core KPI poster (`metric_spotlight`)**:
     - The HTML side gets a native web count-up physics engine: the value rolls smoothly from 0 to the target (for example 94.8%), with the year-on-year label locking in a highlight.
  4. **Maturity ladder (`maturity_ladder`)**:
     - The steps from L1 starting stage ➔ L4 mature stage appear in turn with the momentum of climbing, highlighting the target maturity layer.

#### 4.1.3 Narrative arc and speaking-beat clock (EPIC-03)
* **Dynamic adaptive rhythm**:
  - `narrative_arc == "conflict"`: motion lasts 200~250ms with a tight `ease-in`, reinforcing the pressure of the pain point;
  - `narrative_arc == "breakthrough"`: motion lasts 400ms with radial expansion from the centre and a flowing glow, setting off the sense of breaking the deadlock;
  - `narrative_arc == "evidence"`: motion lasts 600ms, ending with a gentle KPI count-up, leaving time for the audience to build trust;
  - `narrative_arc == "call_to_action"`: the closing action points are drawn out steadily from left to right, strengthening the sense of decision and execution.

---

### 4.2 Interaction and Active Decision Sandbox

#### 4.2.1 Live Presenter HUD, a dual-vision cognitive hub (EPIC-04)
* **Trigger**: in the single-file HTML deck, press **`P`** or click the **`HUD` button** in the control bar to open the **"Presenter Dynamics Hub"** at the right of the screen (or in a split window).
* **Core functions of the hub**:
  1. **Cognitive Radar**:
     - Shows where the current slide sits in the Cognitive Contract (Q1 pull of the core thesis, Q3 coverage of the knowledge-gap pain points, Q4 end-action requirement);
     - Warns of cognitive conversion goals the current page has not yet reached.
  2. **Transition Teleprompter**:
     - Extracts `slide.transition` automatically and shows, in large highlighted type, the spoken connective to say before changing slides (for example: *"[Speaking cue] Stress: however, both existing plans have hit their ceiling under production concurrency ..."*).
  3. **Objection Playbook**:
     - From the `SemanticAuditor` review, distil **2-3 typical Hard Skepticisms** the current page may face, with the **standard authoritative answer (Smoking Gun Defense)**, so the speaker can respond calmly in a defence.

#### 4.2.2 Active Decision Sandbox (EPIC-05)
* **Design philosophy**: **from a one-way static deck to a simulator where executives decide on the spot.**
* **Three interactive sandbox components**:
  1. **Scenario Switcher Tab**:
     - On pages with a `data_chart` or `metric_spotlight`, a light switcher is embedded at the top: `[Conservative]` | `[Baseline]` | `[Aggressive breakthrough]`;
     - When an executive asks a question live, a light tap by the speaker recomputes bar heights, line trends and KPI key numbers at once, with smooth redraw.
  2. **Sensitivity Slider**:
     - Drag key variables on the presentation surface (such as "R&D budget ±30%", "QPS range") and live-simulate the ROI return curve.
  3. **Architecture Drilldown Modal**:
     - On an `architecture_stack` page, clicking any middleware or microservice component immediately pops up that component's SLA metrics, upstream and downstream call chain, failure-domain isolation and rollback mechanism.

#### 4.2.3 Millisecond intent-reflection flywheel across toolchains (EPIC-06: Intent Reflection)
* **Mechanism**:
  - Add an `analyze_intent_diff(old_bp, new_bp)` function in `core/sync_watcher.py`;
  - When a person changes a metric, deletes a primitive card or edits a title in Office / Keynote / a local JSON, SyncWatcher produces not only a file-level diff but derives its **strategic intent** in a structured way:
    - For example: *"Detected: the person changed P99 latency from 20ms to 5ms and removed the third-party gateway layer ➔ Intent reflection: the person is making performance targets more aggressive and pursuing a minimal in-house design"*;
  - This reflection is injected as context into the agent's next planning round, so the AI stays in step with the human expert's intent in later iterations.

---

## 5. Blueprint Schema v3.3 Extension

On top of the existing `blueprint.json` spec, extend these fields, 100% backward compatible:

```json
{
  "contract": { ... },
  "presentation_config": {
    "transition_effect": "fade | push | wipe | none",
    "motion_pace": "staged | instant",
    "kinetic_style": "semantic_physics | minimal",
    "enable_sandbox": true
  },
  "slides": [
    {
      "layout_type": "metric_spotlight",
      "narrative_arc": "evidence",
      "sandbox": {
        "enabled": true,
        "scenarios": {
          "conservative": { "metrics": [ { "value": "85.2%" } ] },
          "baseline": { "metrics": [ { "value": "94.8%" } ] },
          "aggressive": { "metrics": [ { "value": "99.1%" } ] }
        }
      },
      "hud_notes": {
        "objection_defense": [
          { "skepticism": "如何保障极端高峰下的 SLA 不劣化？", "counter": "依靠第三层工具沙箱的自适应熔断与 8ms 降级旁路。" }
        ]
      }
    }
  ]
}
```
(In the sample, the skepticism asks how the SLA is kept from degrading at extreme peaks, and the counter answers with the third-layer tool sandbox's adaptive circuit-breaking and an 8ms degradation bypass.)

---

## 6. Acceptance Criteria and Deliverables

1. **Native PPTX step timing**: the exported PPTX played full-screen in Microsoft PowerPoint steps through components in order on Space;
2. **HTML Presenter HUD**: pressing `P` in the single-file HTML deck opens the Presenter HUD smoothly, showing the cognitive compass, transition cues and the objection playbook;
3. **HTML Active Sandbox**: on a page with data metrics, clicking the conservative / baseline / aggressive tabs refreshes the page values smoothly;
4. **Intent reflection**: `SyncWatcher.analyze_intent_diff` outputs meaningful strategic-intent analysis for data and structure changes.
