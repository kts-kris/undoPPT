# undoPPT v3.4.0 Product Requirements Document (PRD)
## Enterprise 12 Scenarios & Decision-Ready Rigor

> English | [简体中文](../../PRD_v3.4_ENTERPRISE_12_SCENARIOS_AND_DECISION_RIGOR.md)

> **Correction (2026-10-09, checked against v3.8.0 code)**: this is a historical requirements document and is kept as written. Three statements overstate what the audit enforces. (1) `BENCHMARK_UNBALANCED` is a keyword check: on a comparison table (title mentions 对比/选型/竞品/对标/benchmark/rfc) with at least two rows, it fires when no trade-off word (cost, friction, threshold, weakness, limitation, boundary …) appears. It does not detect "ours all green, theirs all red", and the 3-way reference frame and the boundary-of-applicability statement in §4.2 are guidance, not checked by code. (2) `PROMOTION_LAUNDRY_LIST` fires only when a `content_columns` / `bento_cards` page contains one of a few laundry phrases (参与了, 协助完成, 日常维护 …) **and** no quantified figure; it does not check STAR structure. (3) `DECISION_ASK_MISSING` also applies to `cross_team_alignment` and `strategic_planning` in code, and the real finding codes of the per-page rules carry a page suffix (`BENCHMARK_UNBALANCED_P<n>`, `PROMOTION_LAUNDRY_LIST_P<n>`); see the [audit codes](../audit_codes.md). In addition, the HTML checkboxes of §4.1.2 render already ticked rather than waiting to be ticked live. The test count in §7 is the count at the time of release.

---

## 1. Document Metadata

* **Product**: undoPPT (presentation deconstruction and reconstruction agent)
* **Version**: v3.4.0
* **Written**: 2026-09-17
* **Status**: Released / production (official engineering standard)
* **Core goals**:
  1. On top of v3.3.0's motion and interaction sandbox, **return fully to the core of enterprise communication and decision-making**;
  2. Exhaustively and specifically equip **12 typical high-frequency enterprise scenarios** (project charter defence, annual strategy, QBR review, cross-team alignment, headcount budget review, RFC architecture review, post-mortem, GTM product launch, major-client bid, promotion review, internal tech training, all-hands mobilisation);
  3. Establish and fix two core rules for upward reporting: the **"Decision-Ready Ask"** and an **"objective and sufficient external reference frame (Rigor in Benchmarking)"**;
  4. Establish an audit protocol of **"net incremental attribution and methodological depth (STAR Attribution & Methodological Depth)"** for promotion reviews;
  5. 100% backward compatible with the existing 6 archetypes and 15 primitives, advancing the whole chain from cognitive planning and primitive assembly through dual-target rendering to automated audit.

---

## 2. Background and Problem Analysis

Motion and visual impact address a deck's "appeal and polish", but in a serious enterprise setting a deck succeeds or fails on **the rigour of its logic**, **the depth of its problem analysis** and **whether it moves a business decision**.

Research found four serious common flaws in internal reporting:

```
┌────────────────────────────────────────────────────────┐     ┌────────────────────────────────────────────────────────┐
│     Flaw 1: no ending, no management decision          │     │  Flaw 2: one-sided, inflated external benchmarking     │
├────────────────────────────────────────────────────────┤     ├────────────────────────────────────────────────────────┤
│ • Much of the time goes on business complexity, then   │     │ • Benchmarks against vendors or competitors use a      │
│   it ends hollowly with "thank you" or "we will keep   │     │   falsely arrogant "ours all green ticks, theirs all   │
│   pushing";                                            │     │   red crosses" comparison;                             │
│ • The leader is left lost: "so are you here for money, │     │ • Migration cost, sunk cost and applicability limits   │
│   people, or a decision on the plan?" The best         │     │   are ignored, and the case collapses at the first     │
│   decision window is missed.                           │     │   question from management or the review committee.    │
└────────────────────────────────────────────────────────┘     └────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────┐     ┌────────────────────────────────────────────────────────┐
│  Flaw 3: promotion review as a laundry list            │     │  Flaw 4: scenario mismatch, one template for all       │
├────────────────────────────────────────────────────────┤     ├────────────────────────────────────────────────────────┤
│ • A year of work laid out flat, a pile of trivial      │     │ • A post-mortem written as a commendation; a project   │
│   tasks (took part in A, helped with B, followed up    │     │   charter written as a product manual;                 │
│   on C);                                               │     │ • Cross-department alignment without interface terms   │
│ • Natural market tailwind confused with real personal  │     │   or a dependency Gantt; headcount review without ROI;│
│   net contribution, no methodology left behind.        │     │   no attack-and-defence logic for the audience's       │
│                                                        │     │   psychological defences.                              │
└────────────────────────────────────────────────────────┘     └────────────────────────────────────────────────────────┘
```

To end these habits, `undoPPT v3.4.0` proposes an upgrade built on three pillars: **the Decision-Ready Ask**, **Rigor in Benchmarking** and **professional rehearsal of 12 core scenarios**.

---

## 3. The 12 Enterprise Scenarios: Mapping Rules

While staying 100% compatible with the underlying 6 archetypes, `undoPPT v3.4.0` splits out 12 core enterprise scenarios. Each defines the **job to be done (JTBD)**, the **audience profile and psychological defences**, a **recommended primitive sequence** and **red-line pitfalls**:

| No. | Scenario ID (`scenario_type`) | Scenario | Base archetype (`archetype`) | Job to be done (JTBD) | Audience's psychological defences | Recommended primitive sequence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S01** | `project_charter` | Project charter and investment defence | `strategic_planning` | Prove why it must be done now, what the return on investment is, and whether the risk is controllable | "Why can't the existing team do it? What are the serious consequences of not doing it?" | `cover` → `bento_cards` (background pain points) → `matrix_2x2` (opportunity positioning) → `architecture_stack` (solution overview) → `timeline` (phase milestones) → `summary` (investment budget and decision request) |
| **S02** | `annual_strategy_okr` | Annual strategy and OKR breakdown | `strategic_planning` | Set the annual north-star metric and win agreement from the big picture down to departmental goals | "Are the targets detached from reality? Can resources support them? How do they break down into execution?" | `cover` → `horizons_curve` (three-horizon portfolio) → `cross_mapping` (strategy-to-goal mapping) → `bento_cards` (key campaigns) → `kpi_dashboard` (north-star KPIs) → `summary` (organisational support and decision request) |
| **S03** | `qbr_business_review` | Monthly / quarterly business review (QBR) | `general_informative` | Report attainment and operating swings, attribute them in depth, and propose next-stage corrections | "Is the gap from the external market or internal execution? Will the proposed measures work?" | `cover` → `kpi_dashboard` (core results) → `data_chart` (structured gap attribution) → `bento_cards` (what worked and what did not) → `timeline` (next-stage action plan) → `summary` (cross-department needs and decision) |
| **S04** | `cross_team_alignment` | Cross-department alignment | `general_informative` | Clarify responsibility boundaries, prerequisite dependencies and joint-debug SLA commitments | "Why do you need our team? Will the interface change affect our main schedule?" | `cover` → `bento_cards` (business background and value of collaboration) → `process_flow` (end-to-end flow and split of responsibilities) → `standard_table` (dependency list and SLA) → `timeline` (joint schedule) → `summary` (resolutions awaiting decision) |
| **S05** | `team_headcount_review` | Team headcount and budget review | `general_informative` | Justify hiring or funding with incremental business output, not by pleading | "How much marginal return will this many hires bring? Could internal efficiency or outsourcing solve it?" | `cover` → `kpi_dashboard` (growth and productivity pressure) → `cross_mapping` (new business lines to headcount) → `standard_table` (budget ledger and phased release) → `summary` (ROI commitment and headcount approval request) |
| **S06** | `tech_rfc_review` | Architecture selection and RFC defence | `tech_architecture` | Prove the design is sound, state the availability targets, migration cost and rollback plan | "Is it over-engineered? How does the old system migrate smoothly? If it fails, how do we roll back?" | `cover` → `bento_cards` (current bottlenecks and non-functional requirements) → `architecture_stack` (core layering) → `standard_table` (full selection comparison) → `process_flow` (disaster recovery and gray rollback) → `summary` (technical committee vote request) |
| **S07** | `post_mortem_review` | Core system post-mortem | `tech_architecture` | Find the root cause, remove similar hazards, build lasting foolproof mechanisms, avoid blame-shifting | "Why did monitoring not alert at once? Why was stopping the bleed so slow? How do we guarantee it never recurs?" | `cover` → `timeline` (full sequence: occurrence, detection, mitigation, recovery) → `bento_cards` (5 Whys root cause and mechanism) → `matrix_2x2` (impact assessment) → `content_columns` (P0/P1 corrective actions) → `summary` (accountability review and lasting governance) |
| **S08** | `product_launch_gtm` | New product launch and GTM | `product_pitch` | Settle target customer positioning, differentiated selling points and the omnichannel acquisition rhythm | "Will users really pay for our selling point? Can channels scale? How does the first cold-start wave run?" | `cover` → `matrix_2x2` (ICP segmentation) → `bento_cards` (core features and killer features) → `standard_table` (competitor pricing and business model) → `timeline` (four-phase GTM roadmap) → `summary` (marketing resource request and launch approval) |
| **S09** | `enterprise_rfp_pitch` | Major-client solution bid (RFP) | `product_pitch` | Show we deeply understand the client's pain and that delivery ability and overall TCO far exceed competitors | "Does your product suit our industry? Is the after-sales team reliable? Are the cases real?" | `cover` → `bento_cards` (client strategy and empathy for pain) → `architecture_stack` (end-to-end industry solution) → `standard_table` (feature fit and SLA comparison) → `content_columns` (reference customer successes) → `summary` (commercial quote and delivery commitment) |
| **S10** | `promotion_assessment` | Annual / half-year promotion review | `career_portfolio` | Prove with facts, data and methodology that one already meets the next level | "Is this the person's own net contribution or the market lifting everyone? Do they have a global methodology?" | `cover` → `bento_cards` (results overview and core positioning) → `content_columns` (2-3 hard-fought campaigns, STAR attribution) → `maturity_ladder` (capability model progression and distilled methodology) → `timeline` (organisational enablement and talent development) → `summary` (commitments at the next level) |
| **S11** | `internal_tech_talk` | Internal training on technical / business methodology | `education_training` | Help learners master new tools or standards quickly, remove blind spots and apply them at once | "I understood but don't know how to use it on a real project; theory is dull and there are no practical cases." | `cover` → `bento_cards` (common misconceptions and pain reflection) → `architecture_stack` (core concepts and model) → `standard_table` (right vs wrong practice) → `process_flow` (standard practical SOP) → `summary` (self-test homework and practice guide) |
| **S12** | `all_hands_rally` | Strategic mobilisation and all-hands | `education_training` | Unify everyone's thinking, state the crisis and the opportunity, and ignite mission and fighting spirit | "What does this strategy have to do with me? Will there still be a year-end bonus? Where should we push?" | `cover` → `bento_cards` (external upheaval and decisive moves) → `horizons_curve` (new strategic heading and growth space) → `kpi_dashboard` (campaign goals pledge) → `content_columns` (culture, values and incentives) → `summary` (call to action and pledge) |

---

## 4. Two Core Rules for Executive Briefing

### 4.1 The final "decisions requested of leadership" rule (EPIC-DECISION-ASK)

For any report to management, a review committee or decision makers, the final delivered value is not the information itself but **bringing about a high-quality, low-friction management decision**.

#### 4.1.1 Primitive contract extension (enhanced `summary` primitive)
The existing `summary` primitive gains these decision-specific fields:
```json
{
  "layout_type": "summary",
  "title": "方案比选与请领导决策事项",
  "action_title": "决策决议：推荐全面启动方案 B 实施改造，申请首期 50 万预算与 3 个人头",
  "tag": "DECISION REQUIRED",
  "narrative_arc": "call_to_action",
  "options": [
    {
      "name": "方案 A：局部打补丁（保守）",
      "pros": "零前期资本投入，对现网无扰动",
      "cons": "技术债累积，预计半年内再度爆仓",
      "cost": "0 元追加 / 人力隐性损耗",
      "risk": "高（系统可用性不可持续）",
      "recommended": false
    },
    {
      "name": "方案 B：分层重构与平滑演进（推荐）",
      "pros": "彻底消除单点瓶颈，兼顾现有业务连续性",
      "cons": "需要 2 个月并行过渡期",
      "cost": "50 万 / 3 个人头支持",
      "risk": "低（具备完备灰度回滚机制）",
      "recommended": true
    },
    {
      "name": "方案 C：全新自研重构（激进）",
      "pros": "技术架构完全自主可控",
      "cons": "周期长达 18 个月，业务停摆风险极大",
      "cost": "200 万+ / 专班团队",
      "risk": "极高（ROI 存在严重不确定性）",
      "recommended": false
    }
  ],
  "recommendation": "综合 ROI 与交付确定性，推荐采纳方案 B：分层重构与平滑演进。在 Q3 阶段性跑通核心集群后视成效释放后续资源。",
  "sign_off_items": [
    "1. 批准《方案 B 架构改造立项》并下发首期 50 万元专用实施预算",
    "2. 协调基础架构团队与安全团队各指派 1 名核心研发专人对接联调",
    "3. 批准设立 Q3 双周项目进展汇报机制并锁定 10 月 31 日灰度上线里程碑"
  ]
}
```
(The sample content is Chinese because the product's primary output language is Chinese: three options, A conservative "patch locally", B recommended "layered refactor with smooth evolution", C aggressive "full in-house rebuild", a recommendation sentence, and three approval items.)

#### 4.1.2 Rendering specification
* **PPTX (vector)**:
  - Render `options` automatically as 2-3 side-by-side comparison cards;
  - Give the `recommended: true` card a primary-colour highlighted outline and a "★ RECOMMENDED" corner badge;
  - At the bottom render a recommendation banner and a checklist of `sign_off_items` with box checkboxes.
* **HTML**:
  - Render a high-fidelity glassmorphic decision hub card;
  - Render `sign_off_items` as **real, interactive checkbox controls**, so a manager can tick the resolutions on the spot while presenting, giving a strong sense of ritual and closure.

---

### 4.2 External benchmarking rule (EPIC-RIGOR-BENCHMARK)

For pages involving external benchmarks, technology selection or competitor analysis (such as `standard_table`, `matrix_2x2`), strict quality criteria apply:

1. **3-Way Reference Frame**:
   - A single competitor as lone evidence is forbidden;
   - Three reference frames are required: ① the industry leader (Leader Benchmark); ② the direct like-for-like competitor (Direct Competitor); ③ the do-nothing / in-house status quo.
2. **Balanced Trade-offs**:
   - A falsely arrogant table where "we are all good, competitors all bad" is forbidden;
   - Our own weaknesses and compromises must be stated objectively (for example "high migration learning cost", "mature cases are still being cultivated");
   - Benchmark dimensions must cover cost (TCO), delivery time, migration friction, team learning threshold and technical evolution flexibility.
3. **Boundary of Applicability**:
   - State clearly the best-fit and the forbidden scenarios of each option.

---

## 5. Attribution Rule for Promotion Reviews and Routine Work (EPIC-PROMOTION-ATTRIBUTION)

In promotion reviews (`promotion_assessment`) and annual results reviews, the AI agent and the cognitive planning engine must follow these iron rules for distilling achievement:

1. **De-noising and net incremental attribution (Net Incremental Contribution)**:
   - Never package the natural tailwind of the business as a personal core contribution (for example "our department's revenue grew 50%": one must ask "how much of that net increment came from a strategy you led?");
   - A strict **STAR structure** is required: Situation (the core predicament and resistance faced) → Task (the role boundary taken on) → Action (the original actions and key solutions adopted) → Result (the quantified net gain after stripping out the market).
2. **Methodological depth and organisational lift**:
   - What separates a good executor from a backbone or expert is depth of thinking;
   - Results should show not just a finished project but a one-off solution distilled into a reusable component library, SOP or technical standard, lifting the organisation's understanding.
3. **Next-level commitment and forward-looking horizon**:
   - A review must end with a clear positioning and plan for the next level, showing a business scope and ownership that go beyond the current post.

---

## 6. Automated Audit Rule Extensions

`core/content_auditor.py` gains these enterprise-specific audit rules:

| Rule code | Severity | Trigger | Deduction | Suggested fix |
| :--- | :--- | :--- | :--- | :--- |
| `DECISION_ASK_MISSING` | `warning` | A management briefing (`strategic_planning`, `project_charter`, `annual_strategy_okr`, `team_headcount_review`, `tech_rfc_review`) has no explicit decision item or approval list on the closing page | 4 | Add `sign_off_items` or an `options` comparison to the closing page, stating what the leader is asked to approve. |
| `BENCHMARK_UNBALANCED` | `warning` | In a selection or benchmark table, all of our dimensions are strengths and all of the competitors' are weaknesses, with no cost, friction or weakness trade-off | 3 | Add objective trade-off dimensions, such as learning cost, migration period or applicability boundary, to strengthen credibility. |
| `PROMOTION_LAUNDRY_LIST`| `warning` | A promotion page lists tasks as a laundry list, with no quantified output metric or no STAR attribution | 4 | Use the STAR attribution structure and mark the personally led actions and the quantified net result. |

---

## 7. Acceptance Criteria

1. **Scenario recognition accuracy**: tests cover typical prompts for the 12 enterprise scenarios; the system identifies the right `scenario_type` and `archetype` and matches the dedicated Q1-Q4 cognitive contract and rehearsal skeleton.
2. **Decision primitive rendering**:
   - PPTX: fully renders the `options` comparison cards (with the recommended badge highlighted) and the `sign_off_items` approval checklist;
   - HTML: fully renders the decision console and the interactive checkbox approval resolutions.
3. **Audit rules take effect**:
   - A management report lacking decision items precisely triggers a `DECISION_ASK_MISSING` deduction with advice;
   - One-sided benchmarking triggers `BENCHMARK_UNBALANCED`;
   - A laundry-list promotion review triggers `PROMOTION_LAUNDRY_LIST`.
4. **All tests pass**: all 20 existing test cases stay 100% green, with new full-coverage test cases for the 12 enterprise scenarios.
