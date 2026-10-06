# 审计码速查

> [English](../en/audit_codes.md) | 简体中文

`cli.py audit` 的每一条发现都带一个码。以 `_P<n>` 结尾的码按页报告（`<n>` 是页码），其余适用于整份蓝图。`warning` 会扣分，`info` 只是提示。（工具输出的消息文字是中文；本页是它的对照参考。）

企业规则与证据类的规则背景见[场景避坑红线](scenario_anti_patterns.md)。版面、对比度与动画问题，`audit` 看不到（它只读蓝图），请看 [CLI 手册](cli_reference.md)里的 `render-check`。

## 认知契约 (Q1–Q4)

| 码 | 级别 | 含义 | 怎么改 |
| :--- | :--- | :--- | :--- |
| `MISSING_COGNITIVE_CONTRACT` | warning | 蓝图里没有 `contract` 块。 | 补上受众 (Q2)、认知差 (Q3)、终局行动 (Q4)。先跑 `cli.py probe`。 |
| `MISSING_CONTRACT` | warning | 同上，由语义审计报出：无法核验受众疑虑。 | 同上。 |
| `UNCLEAR_THESIS` | warning | 契约缺少 `core_thesis` (Q1)。 | 写出整份材料所代表的那一个论断。 |
| `NO_CORE_THESIS` | warning | 同上，由语义审计报出：无法计算主旨离心度。 | 同上。 |
| `MISSING_AUDIENCE_PROFILE` | warning | 没有 `audience` (Q2)。 | 说明谁在听、他们担心什么。 |
| `UNSPECIFIED_KNOWLEDGE_DELTA` | info | 没有记录受众的盲区或痛点 (Q3)。 | 列出受众还不知道的事。 |
| `MISSING_ACTION_OUTCOME` | warning | 没有终局行动 (Q4)。 | 写明讲完后受众必须做出什么决定。 |
| `ACT_OUTCOME_UNRESOLVED` | warning | 收尾页没有落到终局行动上。 | 以决策收尾，而不是以总结收尾。 |
| `PAINS_IGNORED` | warning | 方案从未正面回应契约里写明的痛点。 | 至少正面回应一个已声明的痛点。 |

## 叙事流

| 码 | 级别 | 含义 | 怎么改 |
| :--- | :--- | :--- | :--- |
| `DISCONNECTED_FLOW` | warning | 页与页之间没有 `transition` (Q10)。 | 补上因果或转折的承接语。 |
| `WEAK_TRANSITIONS` | info | 只有部分页配置了转折语。 | 给其余页补上。 |
| `MISSING_TRANSITION_P<n>` | warning | 这一页没有转折语。 | 补上。 |
| `UNSPECIFIED_NARRATIVE_ARC` | info | 没有设置 `narrative_arc` (Q5)。 | `hook`、`conflict`、`breakthrough`、`evidence`、`progression`、`call_to_action`。 |
| `GENERIC_TRANSITION_P<n>` | info | 转折语措辞偏弱。 | 用因果、转折或突破类的连词。 |
| `MONOTONOUS_RHETORIC` | info | 所有转折语都是同一种语气。 | 因果、转折、突破交替使用。 |
| `ARC_TRANSITION_MISMATCH_P<n>` | info | `conflict` 阶段的页，转折语却没有冲突感。 | 用"然而""矛盾在于"之类。 |
| `INVALID_TRANSITION_P<n>` | warning | `transition_effect` 不是 `fade`、`push`、`wipe`、`none` 之一。 | 选一个支持的值。 |

## 单页质量

| 码 | 级别 | 含义 | 怎么改 |
| :--- | :--- | :--- | :--- |
| `MISSING_MISSION_P<n>` | info | 没有 `mission` (Q6)。 | 写明这一页唯一的职责。 |
| `PASSIVE_TITLE_P<n>` | warning | 中性的话题式标题（"概览""现状"）(Q8)。 | 把结论写成标题。 |
| `MISSING_CORE_EVIDENCE_P<n>` | info | 没有 `core_evidence`。 | 补上撑起这页的数字或案例。 |
| `UNQUANTIFIED_EVIDENCE_P<n>` | info | `core_evidence` 里没有数字或具体范例。 | 把它量化。 |
| `EVIDENCE_POVERTY` | warning | 有真实证据的页太少。 | 加厚证据。 |
| `THESIS_DRIFT_P<n>` | warning | 这页的用词与主旨几乎没有交集。 | 拉回主旨，或删掉。 |
| `BUZZWORD_DETECTED_P<n>` | warning | 空洞的管理或 AI 套话。告警附带具体改写建议（`suggestion`）。 | 照建议改写。 |
| `LLM_JUDGE_BYPASS` | info | 可选的 LLM 裁判没有完成，已回退到规则审计。 | 无需处理。 |

## 内容预算（密度）

| 码 | 级别 | 含义 | 上限 |
| :--- | :--- | :--- | :--- |
| `DENSITY_EXCEEDED_P<n>` | warning | 卡片太多。 | 取自预设的 `content_budget`（默认 4）。 |
| `LAYERS_EXCEEDED_P<n>` | warning | 架构层级太多。 | 3–4 |
| `MATRIX_QUADS_EXCEEDED_P<n>` | warning | 象限超过四个。 | 4 |
| `LADDER_LEVELS_EXCEEDED_P<n>` | warning | 成熟度阶数太多。 | 4–5 |
| `HORIZONS_EXCEEDED_P<n>` | warning | 地平线不是三层。 | 3（H1/H2/H3） |
| `MAPPING_ROWS_EXCEEDED_P<n>` | warning | 映射行数太多。 | 4–5 |
| `TABLE_ROWS_EXCEEDED_P<n>` | warning | 表格行数太多。 | 8 |
| `TABLE_COLS_EXCEEDED_P<n>` | warning | 表格列数太多。 | 5 |
| `COLUMNS_EXCEEDED_P<n>` | warning | 并列栏数超过四栏。 | 4 |
| `FLOW_STEPS_EXCEEDED_P<n>` | warning | 流程步骤太多。 | 6 |
| `CHART_CATEGORIES_EXCEEDED_P<n>` | warning | 图表类目太多。 | 8 |

## 企业规则（v3.4）

| 码 | 级别 | 含义 |
| :--- | :--- | :--- |
| `DECISION_ASK_MISSING` | warning | 面向领导的汇报，收尾页没有 `options` 或 `sign_off_items`。 |
| `BENCHMARK_UNBALANCED_P<n>` | warning | 对标表没有任何取舍："我方全绿、友商全红"。 |
| `PROMOTION_LAUNDRY_LIST_P<n>` | warning | 晋升页罗列职责，没有 STAR 归因，也没有量化的净增量。 |

## 证据预算（v3.6）与出处（v3.7）

| 码 | 级别 | 含义 | 怎么改 |
| :--- | :--- | :--- | :--- |
| `THIN_CONTENT_P<n>` | warning | 正文比该图元所需的更短（各图元下限见[场景提纲样例](scenario_outlines.md)）。 | 补事实，或合并、删除这一页。 |
| `EVIDENCE_BUDGET_P<n>` | warning | 指标页里带数值的指标不足一半。 | 补真实数值，或改用文字图元。 |
| `UNSOURCED_FIGURES_P<n>` | warning | 没有任何 `source` 覆盖的数字。 | 加 `source`，或标 `status: "todo"`。 |
| `EVIDENCE_TODO_P<n>` | warning | 标为 `status: "todo"` 的数字。 | 交付前换成真实数据。 |
| `EVIDENCE_ESTIMATE_P<n>` | info | 估算值；页脚会标"估算"。 | 准备好说明依据。 |
| `EVIDENCE_ILLUSTRATIVE_P<n>` | info | 编造的示例数字；页脚会标"示例数据"。 | 不要当作真实数据呈现。 |

证据预算与出处的扣分都有上限（分别为 12 分和 10 分），所以内容单薄或缺出处的草稿会被标出来，但不会被扣成零分。
