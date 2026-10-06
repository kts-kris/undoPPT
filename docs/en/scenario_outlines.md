# Exemplar Outlines for the 12 Enterprise Scenarios

> English | [简体中文](../zh/scenario_outlines.md)
>
> **Version**: v3.8.0
> **Purpose**: before writing `blueprint.json`, the Agent checks each page against this document: should the page exist, what evidence does it need, which layout fits.
> **Relation to the engine**: the page order and layouts in each table match what `cli.py plan` produces (`kpi_dashboard` is an alias of `metric_spotlight`). The Agent may reorder pages, but **must not drop the "evidence required" column**. A test keeps this page and the Chinese version in step with the planner.

## How to use this document

1. Run `python3 cli.py probe --prompt "<the user's own words>"` to judge whether there is enough information. If not, ask first (see `SKILL.md`, stage 1).
2. Find the scenario below and go through the outline page by page: **did the user supply this page's evidence?**
3. Yes: write it into the blueprint. No: **go back and ask, or merge or drop the page**. Do not fill a layout with clichés and placeholder numbers.
4. Run `cli.py audit` when done. `THIN_CONTENT` and `EVIDENCE_BUDGET` are the signal that evidence is missing.

**One rule above all**: the number of pages follows the evidence; the evidence does not follow the number of pages. A page without enough evidence should not exist.

The example figures in the tables only illustrate *what kind* of evidence is needed. They are **not** facts to copy.

---

## S01 Project Charter Defense `project_charter`

**Audience gate**: investment review committee, finance, the sponsoring executive. They fear: an unclear ROI, no risk cover, money spent and nothing delivered.
**What they must decide**: approve the first-phase budget and people, and set the milestone gates.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required (no evidence, no page) |
|---|---|---|---|---|
| 1 | cover | Smart customer service: 3M for a 35% cost reduction | Say in one line what is asked and what it buys | The budget figure, the expected-return figure |
| 2 | bento_cards | Opportunity: manual channel cost is up 22% a year and the window is two quarters | Pain + window + return | Current cost data, market or competitor basis |
| 3 | matrix_2x2 | Positioning: this project sits in the high-return, high-feasibility quadrant | Prove this is the right opportunity | The scoring dimensions and how each option was rated |
| 4 | architecture_stack | Architecture: four decoupled layers, only the first two in phase one | Prove it can be built | The layered design, the phase-one boundary |
| 5 | timeline | Plan: four stages, MVP validated in Q3 before phase-two resources are released | Prove the risk is contained | Milestone dates, the pass criterion of each gate |
| 6 | summary (with options) | Decision: recommend option B; please approve budget, people and gates | Get the decision | At least 3 options (including "do nothing"), cost and risk of each, the approval list |

**Red lines**: never a single option; never without "the cost of not doing it"; the ROI must survive questioning.

---

## S02 Annual Strategy and OKRs `annual_strategy_okr`

**Audience gate**: the executive team and business-line heads. They fear: strategy as slogans, OKRs detached from resources, every line wanting all of the resources.
**What they must decide**: approve the strategy map and the resource split.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | 2027 strategy: one north-star metric, +30% | Fix the direction | The north-star metric and its target |
| 2 | horizons_curve | Portfolio: a 70:20:10 split protects the core and incubates growth | Say how resources are divided | The business and the success measure of each of the three horizons |
| 3 | cross_mapping | Cascade: vision to action in four aligned layers, each with an owner | Show the OKRs are not castles in the air | The current state, target and lever of each layer |
| 4 | bento_cards | Campaigns: four must-win battles, each with a commander and a success criterion | Focus | The campaigns, their owners, the success criteria |
| 5 | metric_spotlight | Measures: four leading indicators, visible monthly | Say how we will know we are winning | Metric definitions, current values, targets |
| 6 | summary (with options) | Decision: approve the strategy map and the resource allocation | Get the decision | Resource options compared, organisational support |

**Red lines**: more than four campaigns means no focus; a metric needs a current value.

---

## S03 Quarterly Business Review (QBR) `qbr_business_review`

**Audience gate**: the sponsoring executive, finance, cross-functional partners. They fear: good news only, vague attribution, the same methods next quarter.
**What they must decide**: accept the attribution, approve the corrective actions and the support they need.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Q3 review: 104% of target, but the mid-tier is under pressure | Lead with the verdict, bad news included | Overall attainment |
| 2 | metric_spotlight | Scoreboard: four core metrics, two up, one flat, one down | The whole picture on one screen | Metric values, year-on-year and quarter-on-quarter |
| 3 | data_chart | Gap: SMB conversion is 6 points below target | Locate the variance | Data by segment or channel |
| 4 | bento_cards | Reflection: three causes, one of them our own | Honest attribution | The evidence behind each cause |
| 5 | timeline | Actions: four corrective steps next quarter, each with a checkpoint | Prove we will change | Actions, owners, check dates |
| 6 | summary (with options) | Decision: approve option B and the sales-and-delivery coordination | Get the decision | Corrective options compared, the support needed |

**Red lines**: at least one metric must be a miss; the attribution cannot be external causes only.

---

## S04 Cross-Team Alignment `cross_team_alignment`

**Audience gate**: the heads of the teams involved, the PMO. They fear: being blamed, being scheduled, work added without people.
**What they must decide**: interface conventions, the schedule and the arbitration mechanism.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Three-way alignment: delivery efficiency target +40% | Set the shared goal | The shared goal and how it is measured |
| 2 | bento_cards | Consensus: what each of the three teams needs and will not give up | Let each side see it was heard | Each side's needs and non-negotiables |
| 3 | process_flow | Boundaries: four steps, one responsible party per step | Remove the grey areas | The steps and who owns each |
| 4 | standard_table | Contract: interfaces, SLAs and fallbacks agreed line by line | Turn consensus into verifiable terms | The interface list, SLA values |
| 5 | timeline | Schedule: three stages of joint integration, locked every two weeks | Align the timing | The joint schedule and gates |
| 6 | summary (with options) | Decision: approve the joint schedule and set an arbitration mechanism | Get the decision | The escalation path, the arbiter |

**Red lines**: every item has exactly one owner; "jointly responsible" is not an owner.

---

## S05 Team Review and Headcount Request `team_headcount_review`

**Audience gate**: the sponsoring executive, HR business partner, finance. They fear: productivity that did not improve, hires who do not produce, too much budget released at once.
**What they must decide**: the number of positions and the release schedule.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Request: 6 positions. Volume is up 180% and productivity is at its limit | Lead with the ask | The number of positions, the volume growth |
| 2 | metric_spotlight | Pressure: average load 145%, a three-month backlog | Prove current productivity is exhausted | Volume, productivity, backlog data |
| 3 | cross_mapping | Alignment: each position maps to a business line and an output metric | Prove this is not "asking for more people" | The position, business line and metric mapping |
| 4 | standard_table | Ledger: fully loaded cost per head against expected output | Let finance do the sums | Cost per head, expected output |
| 5 | timeline | Ramp-up: productive in the first month, full output by the third | Prove new hires pay off | The hiring pace, the onboarding plan |
| 6 | summary (with options) | Decision: release in two phases, the second gated on the first's output | Get the decision | Options compared, the release gates |

**Red lines**: "we are busy" is not evidence, show numbers; do not ask for everything at once, offer steps.

---

## S06 Technology Selection and Architecture RFC `tech_rfc_review`

**Audience gate**: the architecture committee and the technical leads concerned. They fear: selection bias, an irreversible migration, no rollback.
**What they must decide**: which option to adopt, and whether to proceed to scheduling.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | RFC: microservices for the trading system, target P99 < 15ms | State the problem and goal in one line | The current bottleneck, the target metric |
| 2 | bento_cards | Bottleneck: the monolith cannot scale out, three concrete symptoms | Prove change is unavoidable | Production data, incidents or load-test results |
| 3 | architecture_stack | Architecture: four decoupled layers, failure domains isolated layer by layer | Show the target design | The layered design, the failure-domain split |
| 4 | standard_table | Selection: build, open source and managed compared on every axis | Compare **objectively** | At least 3 candidates (including the status quo), TCO, migration friction, applicability limits |
| 5 | process_flow | Safety net: four-stage migration, one-click rollback | Prove it is reversible | Migration steps, rollout percentages, rollback triggers |
| 6 | summary (with options) | Decision: adopt option B and move to scheduling | Get the decision | The recommendation's rationale, the resources requested |

**Red lines**: the comparison cannot read "ours is best on everything": it must disclose its own costs (`BENCHMARK_UNBALANCED`); no rollback plan, no approval.

---

## S07 Production Incident Post-Mortem `post_mortem_review`

**Audience gate**: technical leads, the business owners affected, sometimes management. They fear: blame outweighing improvement, the same failure happening again.
**What they must decide**: accept the root cause, and accept the remediation items and the long-term mechanism.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Payment gateway P0 post-mortem: about the system, not the person; the goal is no repeat | Set the ground rules | One line on the incident, its duration |
| 2 | timeline | Timeline: 18 minutes to stop the bleeding, exposing slow alerting and response | Reconstruct the timeline | The exact times of onset, detection, mitigation and recovery |
| 3 | bento_cards | Root cause: no static validation of config changes, canary did not take effect | Five whys down to a mechanism | The evidence for each why (logs, monitoring) |
| 4 | matrix_2x2 | Impact: reach and severity | Quantify the loss | Users, orders or funds affected |
| 5 | content_columns | Remediation: three P0 safeguards that cut recurrence at the tool level | Turn the lesson into a mechanism | The items, owners and completion dates |
| 6 | summary (with options) | Decision: accept the remediation and issue the change red lines | Get the decision | The long-term mechanism, the acceptance criteria |

**Red lines**: the root cause must land on a process or a tool, not "someone was careless"; every remediation item has an owner and a date.

---

## S08 Product Launch and Go-to-Market `product_launch_gtm`

**Audience gate**: management, heads of sales and marketing. They fear: vague positioning, prices set by guesswork, channels without a rhythm.
**What they must decide**: approve the launch plan and the first-phase budget.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Launch: first target mid-to-large enterprises, 10M by Q4 | Goal first | The first-phase target and segment |
| 2 | matrix_2x2 | Positioning: the first wave goes only for high-value key accounts and growth-stage firms | Focus the ICP | The segmentation and why this one |
| 3 | bento_cards | Features: three killer features form the moat | Say why us | The features and their objective difference from competitors |
| 4 | standard_table | Pricing: tiered, gross margin held at 65% | Make the unit economics clear | Price bands, cost, margin |
| 5 | timeline | Rhythm: four stages across all channels | Prove there is a cadence | Stage targets and channels |
| 6 | summary (with options) | Decision: approve the launch plan and first-phase budget | Get the decision | Options compared, the budget |

**Red lines**: differentiation must be set against real competitors; the pricing page needs cost.

---

## S09 Enterprise Proposal and Bid `enterprise_rfp_pitch`

**Audience gate**: the client's business, technical, procurement and compliance evaluators. They fear: a proposal that does not fit, delivery they cannot trust, a compliance gap.
**What they must decide**: award the contract and start phase one.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Built for XX Bank: certain delivery for the core-system upgrade | Empathise first | The client's name and objective |
| 2 | bento_cards | Resonance: the three pains and compliance requirements we understand | Show we did the homework | The client's public information, the tender requirements |
| 3 | architecture_stack | Architecture: four highly available layers covering five years of elastic growth | Show the solution | A design tailored to the client's scenario |
| 4 | standard_table | Fit: every tender requirement answered, TCO 30% lower | Respond line by line | The response matrix, SLAs, the TCO calculation |
| 5 | content_columns | Proof: comparable benchmarks delivered, references available | Lower the evaluators' decision risk | Named cases with quantified results |
| 6 | summary (with options) | Recommendation: award the contract, start within a week | Get the decision | Delivery commitments, service assurances |

**Red lines**: cases must be real and checkable; every tender requirement needs a matching response.

---

## S10 Promotion Defense `promotion_assessment`

**Audience gate**: the promotion review committee. They fear: a laundry list, a team's work claimed as an individual's, no evidence for the next level.
**What they must decide**: recognise that the candidate already works at the next level.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Promotion to senior engineer: led a rewrite, 3x performance | Land it in one line | The target level, the strongest result |
| 2 | bento_cards | Position: personal net increment +45%, after stripping out market growth | Strip out the tailwind | Personal figures, the team or market baseline |
| 3 | content_columns | Campaigns: STAR attribution of three battles | Prove capability | For each battle the situation, task, action and quantified result |
| 4 | maturity_ladder | Leap: from executor to system-wide guide, a four-level methodology | Prove it has been distilled | Reusable methods and where they were adopted |
| 5 | timeline | Influence: mentoring, standards and developing people | Prove organisational contribution | Named people, concrete outputs |
| 6 | summary | Commitment: the goals I will lead after promotion | Prove a plan for the next level | Measurable commitments |

**Red lines**: no "took part in / was responsible for" laundry list (`PROMOTION_LAUNDRY_LIST`); every result needs a baseline.

---

## S11 Internal Tech Talk `internal_tech_talk`

**Audience gate**: colleagues and trainees. They fear: leaving with nothing, all concepts and no examples.
**What must happen**: the audience changes one concrete practice.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Cache design: three things three production incidents taught us | Promise the takeaway | What they will take away |
| 2 | bento_cards | Anti-patterns: the three most common mistakes | Break through the blind spot | Real code or a production case |
| 3 | architecture_stack | The fix: layered caching and invalidation | Give a mental model | The structure and its trade-offs |
| 4 | standard_table | Contrast: the metric gap between the wrong and the right way | Persuade with data | A load test or production comparison |
| 5 | process_flow | Hands on: a four-step self-check | Usable on the spot | Executable steps |
| 6 | summary | Action: check these three things first when you get back | Land in action | Specific checks |

**Red lines**: every point needs a real example; a "best practice" with no counter-example is a slogan.

---

## S12 All-Hands and Strategic Rally `all_hands_rally`

**Audience gate**: all employees. They fear: empty slogans, nothing to do with them, another round of pressure.
**What must happen**: everyone sees the direction and knows their place in it.

| Page | Layout | Conclusion-first title (example) | Mission | Evidence required |
|---|---|---|---|---|
| 1 | cover | Annual rally: a 1B target, reached on one direction | Plant the flag | The annual hard target |
| 2 | bento_cards | Momentum: what is changing outside and our window | Say why now | Industry data, competitor moves |
| 3 | horizons_curve | Heading: three must-win campaigns | Say where we are going | The three fronts and their goals |
| 4 | metric_spotlight | Pledge: four must-hit metrics | Make the target visible | The metrics and current progress |
| 5 | content_columns | Culture: three organisational rules | Say how we win | The rules, real people and real stories |
| 6 | summary | Call to action: everyone's first move | Land it on the individual | The incentive mechanism, the action list |

**Red lines**: every call to action maps to a concrete mechanism or action; slogans alone are not enough.

---

## The evidence floor per layout

The engine uses `THIN_CONTENT` to check that the body can carry the layout (characters of body text, headers excluded):

| Layout | Minimum body | Layout | Minimum body |
|---|---|---|---|
| bento_cards | 80 | cross_mapping | 90 |
| content_columns | 90 | maturity_ladder | 90 |
| timeline | 70 | horizons_curve | 60 |
| process_flow | 70 | matrix_2x2 | 60 |
| standard_table | 60 | summary | 60 |
| metric_spotlight | 40 | architecture_stack | 30 |

At least half the metrics on a KPI page (`metric_spotlight`) must carry a number, otherwise `EVIDENCE_BUDGET` is reported.
