# Audit Finding Codes

Every finding from `cli.py audit` has a code. Codes ending `_P<n>` are reported per slide (`<n>` is the page number); the rest apply to the whole deck. `warning` costs points; `info` is a nudge. (Message text in the tool is Chinese; this page is the English reference.)

For the rules behind the enterprise and evidence codes see [Scenario anti-patterns](scenario_anti_patterns.md); for layout, contrast and animation problems, which `audit` cannot see because it reads only the blueprint, see `render-check` in the [CLI reference](cli_reference.md).

## Cognitive contract (Q1-Q4)

| Code | Level | Meaning | Fix |
| :--- | :--- | :--- | :--- |
| `MISSING_COGNITIVE_CONTRACT` | warning | The blueprint has no `contract` block. | Add audience (Q2), knowledge gap (Q3) and target action (Q4). Run `cli.py probe` first. |
| `MISSING_CONTRACT` | warning | Same, hit by the semantic audit: audience objections cannot be checked. | As above. |
| `UNCLEAR_THESIS` | warning | The contract has no `core_thesis` (Q1). | State the one claim the deck stands for. |
| `NO_CORE_THESIS` | warning | Same, hit by the semantic audit: thesis drift cannot be measured. | As above. |
| `MISSING_AUDIENCE_PROFILE` | warning | No `audience` (Q2). | Say who is listening and what they fear. |
| `UNSPECIFIED_KNOWLEDGE_DELTA` | info | No blind spots or pains recorded (Q3). | List what the audience does not yet know. |
| `MISSING_ACTION_OUTCOME` | warning | No target action (Q4). | State what the audience must decide afterwards. |
| `ACT_OUTCOME_UNRESOLVED` | warning | The closing slide does not land the target action. | End on the decision, not a summary. |
| `PAINS_IGNORED` | warning | The deck never addresses the pains the contract names. | Meet at least one stated pain head-on. |

## Narrative flow

| Code | Level | Meaning | Fix |
| :--- | :--- | :--- | :--- |
| `DISCONNECTED_FLOW` | warning | Slides have no `transition` between them (Q10). | Add a causal or contrasting bridge. |
| `WEAK_TRANSITIONS` | info | Only some slides carry a transition. | Add one to the rest. |
| `MISSING_TRANSITION_P<n>` | warning | This slide has no transition. | Add one. |
| `UNSPECIFIED_NARRATIVE_ARC` | info | No `narrative_arc` set (Q5). | `hook`, `conflict`, `breakthrough`, `evidence`, `progression`, `call_to_action`. |
| `GENERIC_TRANSITION_P<n>` | info | The transition wording is weak. | Use a causal, contrast or breakthrough connective. |
| `MONOTONOUS_RHETORIC` | info | Every transition has the same register. | Alternate cause, contrast and breakthrough. |
| `ARC_TRANSITION_MISMATCH_P<n>` | info | A `conflict` slide whose transition does not sound like conflict. | Use "however", "the contradiction is". |
| `INVALID_TRANSITION_P<n>` | warning | `transition_effect` is not one of `fade`, `push`, `wipe`, `none`. | Pick a supported one. |

## Per-slide quality

| Code | Level | Meaning | Fix |
| :--- | :--- | :--- | :--- |
| `MISSING_MISSION_P<n>` | info | No `mission` (Q6). | State the slide's single job. |
| `PASSIVE_TITLE_P<n>` | warning | A neutral topic title ("Overview", "Status") (Q8). | Write the conclusion as the title. |
| `MISSING_CORE_EVIDENCE_P<n>` | info | No `core_evidence`. | Add the number or case that carries the slide. |
| `UNQUANTIFIED_EVIDENCE_P<n>` | info | `core_evidence` has no figure or concrete example. | Quantify it. |
| `EVIDENCE_POVERTY` | warning | Too few slides have real evidence. | Strengthen the evidence. |
| `THESIS_DRIFT_P<n>` | warning | The slide's vocabulary barely overlaps the thesis. | Tie it back or cut it. |
| `BUZZWORD_DETECTED_P<n>` | warning | An empty management or AI cliché. The finding carries a concrete rewrite (`suggestion`). | Apply it. |
| `LLM_JUDGE_BYPASS` | info | The optional LLM judge did not finish; rules were used instead. | None needed. |

## Content budget (density)

| Code | Level | Meaning | Limit |
| :--- | :--- | :--- | :--- |
| `DENSITY_EXCEEDED_P<n>` | warning | Too many cards. | From the preset's `content_budget` (default 4). |
| `LAYERS_EXCEEDED_P<n>` | warning | Too many architecture layers. | 3-4 |
| `MATRIX_QUADS_EXCEEDED_P<n>` | warning | More than four quadrants. | 4 |
| `LADDER_LEVELS_EXCEEDED_P<n>` | warning | Too many maturity levels. | 4-5 |
| `HORIZONS_EXCEEDED_P<n>` | warning | Not three horizons. | 3 (H1/H2/H3) |
| `MAPPING_ROWS_EXCEEDED_P<n>` | warning | Too many mapping rows. | 4-5 |
| `TABLE_ROWS_EXCEEDED_P<n>` | warning | Too many table rows. | 8 |
| `TABLE_COLS_EXCEEDED_P<n>` | warning | Too many table columns. | 5 |
| `COLUMNS_EXCEEDED_P<n>` | warning | More than four columns. | 4 |
| `FLOW_STEPS_EXCEEDED_P<n>` | warning | Too many process steps. | 6 |
| `CHART_CATEGORIES_EXCEEDED_P<n>` | warning | Too many chart categories. | 8 |

## Enterprise rigor (v3.4)

| Code | Level | Meaning |
| :--- | :--- | :--- |
| `DECISION_ASK_MISSING` | warning | A leadership-facing deck ends without `options` or `sign_off_items`. |
| `BENCHMARK_UNBALANCED_P<n>` | warning | A comparison table with no trade-offs: "ours all green, theirs all red". |
| `PROMOTION_LAUNDRY_LIST_P<n>` | warning | A promotion slide listing duties with no STAR attribution or quantified net contribution. |

## Evidence budget (v3.6) and provenance (v3.7)

| Code | Level | Meaning | Fix |
| :--- | :--- | :--- | :--- |
| `THIN_CONTENT_P<n>` | warning | The body is shorter than the layout needs (minimums in [scenario_outlines.md](../scenario_outlines.md)). | Add facts, or merge or drop the page. |
| `EVIDENCE_BUDGET_P<n>` | warning | A KPI slide where fewer than half the metrics carry a number. | Add real values or use a text layout. |
| `UNSOURCED_FIGURES_P<n>` | warning | Figures that no `source` covers. | Add `source`, or mark `status: "todo"`. |
| `EVIDENCE_TODO_P<n>` | warning | Figures marked `status: "todo"`. | Replace with real data before delivery. |
| `EVIDENCE_ESTIMATE_P<n>` | info | Estimated figures; the footer says 估算. | Be ready to state the basis. |
| `EVIDENCE_ILLUSTRATIVE_P<n>` | info | Invented figures; the footer says 示例数据. | Do not present as real data. |

Evidence-budget and provenance deductions are capped (12 and 10 points) so that a thin or unsourced draft is flagged without being scored to zero.
