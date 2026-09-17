# undoPPT Scenario Anti-Pattern & Red Lines Specification

> **Version**: v3.2.0  
> **Status**: Official Engineering Standard  
> **Audience**: AI Agents (Cognitive Planners) & Reviewers

This document defines the strict anti-pattern guidelines, red lines, buzzword blacklists, and rhetorical quality requirements across all 6 scenario archetypes supported by `undoPPT`. Both the AI Agent (during prompt composition) and the deterministic auditor (`cli.py audit`) strictly adhere to these rules.

---

## 1. Universal Red Lines (All Scenarios)

These prohibitions apply universally across the entire presentation regardless of scenario archetype:

### 1.1 Prohibited AI Fluff & Empty Buzzword Blacklist
The following phrases and jargon patterns are strictly prohibited. The automated semantic auditor treats their occurrence as high-severity deductions:

| Category | Prohibited Phrases / Patterns | Rationale & Recommended Alternative |
| :--- | :--- | :--- |
| **Formulaic AI Clichés** | `不仅是...，更是...`<br>`不仅...而且...`<br>`...是...的必由之路/坚实基石`<br>`为什么/凭什么/怎么做` | Empty rhetorical inflation. State the factual assertion directly with concrete causal mechanisms. |
| **Abstract Management Jargon** | `打法`, `闭环`, `抓手`, `赋能`, `底层逻辑`<br>`颗粒度`, `盘活`, `破局`, `解构`, `对齐` (without concrete actions) | Empty buzzwords masking lack of substance. Use specific verbs: `构建`, `降低`, `交付`, `测试`, `重构`, `量化`. |
| **Passive / Neutral Titles** | `现状分析`, `系统架构`, `背景介绍`<br>`项目概况`, `思考与探索`, `总结与回顾`<br>`Overview`, `Introduction`, `Architecture` | Every slide title must be an **Action Title** stating a conclusion or judgment (e.g., `Pain Point: ...` or `Result: ...`). |
| **Fabricated Metrics & False Proof** | Inventing decimal numbers, fake benchmarks, or unverified outage root causes | If empirical proof is unavailable, explicitly label with `[Pending Verification]` or `[Business Assumption]`. Never disguise assumptions as verified data. |
| **Decorative Clutter & Card Walls** | Stacking 8+ cards just to fill canvas; rainbow neon gradients; glow card effects | Brevity and structure force clarity. Stick strictly to primitive capacity budgets (e.g., 2~4 Bento cards max). |

---

## 2. Archetype-Specific Red Lines (The 6 Scenarios)

### 2.1 Strategic Planning (`strategic_planning`)
* **Focus**: High-level alignment, trade-offs, resource allocation, three horizons.
* **Prohibitions & Red Lines**:
  1. **No Vision Without Boundaries**: Reject vague vision statements like "Building world-class digital capabilities". Must state concrete strategic scope and boundaries.
  2. **Mandatory Not-to-do List**: True strategy is about what NOT to do. Slides must explicitly state trade-offs and deprioritized paths.
  3. **Three Horizons Governance**: H1 (Core Business), H2 (Emerging Growth), and H3 (Disruptive Future) must specify resource allocation ratios (e.g., `70:20:10`) and stage-gate exit/sunsetting criteria.
  4. **Matrix Precision**: 2x2 matrices must clearly define both X and Y axes with quantifiable or unambiguous criteria; each quadrant must map to a distinct strategic stance.

### 2.2 Tech Architecture (`tech_architecture`)
* **Focus**: Layer decoupling, trade-offs, SLA metrics, evolution roadmap.
* **Prohibitions & Red Lines**:
  1. **No Handwaving on "High Availability / High Performance"**: Strictly forbid unqualified claims like "massively scalable" or "ultra-low latency". Must provide empirical percentiles (`P50/P95/P99 latency`), QPS/TPS thresholds, and concurrency limits.
  2. **Explicit Trust & Failure Boundaries**: Architecture stacks and process flows must state external dependencies, directional call flows, and failure isolation domains.
  3. **Disaster Recovery & Rollback Gates**: Must document fallback mechanisms, circuit breakers, and rollback paths. A solution without a rollback plan is an incomplete solution.
  4. **Equal Trade-off Dimensions**: When contrasting candidate technologies, list costs (migration friction, cognitive load, vendor lock-in, infra costs) alongside benefits.

### 2.3 Product Pitch Deck (`product_pitch`)
* **Focus**: Customer pain points, proprietary breakthroughs, business model, milestones.
* **Prohibitions & Red Lines**:
  1. **No Top-Down Macro Fallacy**: Never assert "The global market is \$500B, we only need 1% to reach \$5B". Tam/Sam/Som must be built bottom-up from target account counts and willingness-to-pay.
  2. **Workflow Pain Points Over General Gripes**: Pain points must be grounded in specific workflow friction (e.g., "Manual reconciliation takes 6 hours per batch"), not vague complaints.
  3. **Unit Economics & Flywheel**: Must present clear unit economics (CAC, LTV, Payback period, or Gross Margin trajectory) rather than handwaving monetization.
  4. **Milestone Deliverables**: Funding roadmap must tie capital drawdowns directly to product deliverables and validation gates.

### 2.4 Personal Resume & Executive Review (`personal_resume`)
* **Focus**: Role profile, core technical stack, quantified track record, forward commitments.
* **Prohibitions & Red Lines**:
  1. **No Job Description Regurgitation**: Reject passive duty statements like "Responsible for maintenance of payment system".
  2. **Enforce STAR Methodology**: Every key accomplishment must follow Situation-Task-Action-Result.
  3. **Quantified Track Record**: Results must be measured in percentages, speedups, or dollar figures (e.g., "Reduced MTTR by 45%", "Saved \$1.2M annual cloud spend").
  4. **Ownership Boundaries**: Explicitly distinguish between individual contributions (Owner) and group collaboration (Contributor). No inflating individual scope.

### 2.5 Education, Training & Courseware (`education_training`)
* **Focus**: Knowledge delta, misconception breakdown, progressive concepts, exercises.
* **Prohibitions & Red Lines**:
  1. **No Dogmatic Terminology Dumps**: Never define a complex concept purely through abstract academic jargon without anchoring in a familiar baseline.
  2. **Target Knowledge Delta**: Identify common learner blind spots and common misconceptions upfront.
  3. **Mandatory Anti-Pattern vs. Best Practice Contrast**: Every core principle must be reinforced with a concrete "Don't do this" vs. "Do this instead" visual contrast.
  4. **Actionable Knowledge Check**: Must include a self-check question, scenario exercise, or hands-on challenge to close the learning loop.

### 2.6 General Corporate & Informative Briefing (`general_informative`)
* **Focus**: Context status, core initiatives, data outcomes, execution schedule.
* **Prohibitions & Red Lines**:
  1. **No Chronological Laundry Lists**: Avoid exhaustive blow-by-blow daily updates. Highlight key decisions and metric inflections.
  2. **Pair Obstacles with Mitigations**: Never report risks or blockers without proposing at least one concrete mitigation proposal.
  3. **WBS & Accountability Schedule**: Closing summary must specify a Work Breakdown Structure (WBS) with clear milestones, dates, and designated owners.

---

## 3. Automated Enforcement Mechanism (`cli.py audit`)

The `ContentAuditor` and `SemanticAuditor` verify these red lines deterministically:

1. **Buzzword Scanning**: Regex pattern match against `BUZZWORD_BLACKLIST`. Each match triggers a structural deduction and an actionable finding.
2. **Action Title Check**: Verifies that titles start with conclusion keywords or active verbs, flagging passive titles like "Overview" or "Status".
3. **Core Evidence Density**: Scans for verifiable numbers (`%`, `ms`, `x`, currency, counts) or explicit assumption markers (`[Pending Verification]`).
4. **Inter-Slide Transitions**: Ensures transitions belong to recognized rhetorical families (`contrast`, `causality`, `breakthrough`, `progression`, `evidence`, `action`).
