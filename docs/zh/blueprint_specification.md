# undoPPT 蓝图规格书 (v3.8.0)

> [English](../en/blueprint_specification.md) | 简体中文

> **图元别名**：`kpi_dashboard` 被接受为 `metric_spotlight` 的别名（认知规划器会在 QBR、年度 OKR 与人头评审场景里输出它）。未知的 `layout_type` 仍会回退到 `bento_cards`，但自 v3.5 起，构建器会发出警告，而不再静默回退。

本文定义 `blueprint.json` 完整的 JSON Schema 规格。它是 AI Agent 与 `undoPPT` 渲染引擎之间不可变的交付契约。

---

## 1. 顶层结构

一份合法的 `blueprint.json` 由两个主要键组成：
- `contract`：定义顶层的认知支柱与目标成果。
- `slides`：按顺序排列的页面定义数组，每一页符合 15 种图元之一。

另有两个可选键：
- `scenario`：12 个企业场景代码之一（`project_charter`、`qbr_business_review` 等）。它会打开该场景的审计规则；例如 `DECISION_ASK_MISSING` 只适用于面向领导的场景。
- `presentation_config`：整份文稿的设置，`{"transition_effect": "fade", "motion": "narrative"}`。`transition_effect` 可取 `fade`（默认）、`push`、`wipe` 或 `none`；`motion` 取 `narrative` 时开启叙事动画（默认关闭；v3.3 的 `motion_pace: "staged"` 是它的别名）。两者都可以按页覆盖，`build --motion` 会覆盖整份文稿的设置。

```json
{
  "contract": {
    "core_thesis": "贯穿全篇的核心主旨陈述",
    "audience": {
      "role": "目标受众角色（如 CTO、高管委员会、学员）",
      "stance": "受众的心态、风险偏好与关注重点"
    },
    "knowledge_delta": {
      "known_baseline": ["受众已知的事实 1", "事实 2"],
      "blindspots_and_pains": ["关键痛点 1", "核心误区 2"]
    },
    "target_outcomes": {
      "understand": "受众必须理解的关键概念",
      "believe": "受众必须接受的核心信念",
      "act": "要求受众立即采取的具体行动或决策"
    }
  },
  "slides": [
    { /* 第 1 页 */ },
    { /* 第 2 页 */ }
  ]
}
```

---

## 2. 通用页面元数据字段

无论是哪种图元，每个页面对象都**必须**包含下列标准元数据属性：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `layout_type` | `string` | 15 种图元标识符之一。 |
| `narrative_arc` | `string` | 叙事阶段：`hook`、`conflict`、`breakthrough`、`evidence`、`progression` 或 `call_to_action`。 |
| `mission` | `string` | 这一页唯一的认知职责（回答 Q6）。 |
| `transition` | `string` | 承接上一页的修辞桥梁（回答 Q10）。第 1 页之后的所有页都必须有。 |
| `action_title` | `string` | 结论先行的标题，陈述一个论断而不是一个话题。 |
| `core_evidence` | `string` | 主要的量化证据（如 `94.8%`、`4 倍效率`）或确凿的案例。 |
| `title` | `string` | 页面视觉上的主标题。 |
| `subtitle` | `string` | 情境化的副标题或框架性陈述。 |
| `transition_effect` | `string`（可选） | 切页动画：`"fade"`（默认）、`"push"`、`"wipe"` 或 `"none"`。 |
| `motion` | `object`（可选，v3.8） | 这一页的叙事动画：`{"type": "reveal" \| "contrast" \| "build" \| "none"}`。除非整份文稿设置了 `presentation_config.motion: "narrative"`，或这一页自行选择，否则关闭。`{"staged_reveal": true}`（v3.3）仍表示 `reveal`。 |
| `sandbox` | `object`（可选） | 活动决策沙盒配置：`{"enabled": true, "scenarios": { "conservative": {...}, "aggressive": {...} }}`。 |
| `hud_notes` | `object`（可选） | 演讲者 HUD 辅导备注：`{"objection_defense": [{"skepticism": "...", "counter": "..."}]}`。 |
| `source` | `string \| string[]`（可选，v3.7） | 这一页数字的来源：`"notes.md:L7"`、CSV 单元格、链接、`"用户口述 2026-10-06"`。写在页面上时覆盖该页所有数字；写在嵌套条目（一个指标、一张卡片）里时只覆盖该条目。 |
| `status` | `string`（可选，v3.7） | 数字的可信程度：`verified`（已核对）、`estimate`（估算，显示为"估算"）、`illustrative`（为展示版式而编造，显示为"示例数据"）、`todo`（占位，始终被标出）。作用范围与 `source` 相同。 |

### 出处（v3.7）

"数字"是指做出论断的数值：百分比、倍数、金额、时长或计量单位（`18%`、`3x`、`¥8,600`、`47分钟`、`5个人头`）。年份、季度（`Q3`）、优先级（`P0`）和结构性计数（"3 个支柱"）不算数字。没有任何 `source` 覆盖的数字叫做*无出处*。无出处和 `todo` 的数字都是 **待核**：

- PPTX/HTML 页面上显示琥珀色的 `待核 N 项` 徽标（`build --final` 会隐藏它，并且改为拒绝构建）；
- 页脚显示 `来源：…`（当状态说明时，前面加 `估算 ·` 或 `示例数据 ·`）；
- 演讲备注与认知检视器（`N` 键）列出出处和仍待核的数字；
- `audit` 报告 `UNSOURCED_FIGURES_P<n>` / `EVIDENCE_TODO_P<n>`，并给出数字汇总。

原生图表数据算作一组需要 `source` 的数字。`cli.py cite` 会根据抽取的文档补全 `source`，且从不写 `status`。

---

## 3. 15 种图元

### 1. `cover`（封面卡片）
用于开篇页。确立基调、背景和高管视角的框架。

```json
{
  "layout_type": "cover",
  "narrative_arc": "hook",
  "mission": "确立演示的核心主张并抓住注意力",
  "category": "ENTERPRISE AI ARCHITECTURE 2026",
  "title": "新一代企业级 Agentic AI 平台",
  "subtitle": "为规模化运营构建自主的多智能体工作流",
  "meta": "架构评审委员会 · 首席 AI 系统组出品"
}
```

---

### 2. `bento_cards`（Bento 网格卡片）
展示 2 到 4 张对比卡片，各带标签、标题与要点清单。其中一张卡片可以被视觉高亮。

```json
{
  "layout_type": "bento_cards",
  "narrative_arc": "conflict",
  "mission": "把旧方案的局限与拟议的现代架构对照起来",
  "transition": "【冲突】然而，现有架构在生产并发压力下无法扩展",
  "action_title": "瓶颈：单体流水线带来 80% 的人工维护开销",
  "core_evidence": "80% 人工开销；旧脚本在 15% 以上的波动下失效",
  "title": "旧方案与 Agentic 自主系统的对比",
  "subtitle": "从脆弱的工作流脚本走向动态自愈的智能体",
  "cards": [
    {
      "tag": "PASSIVE CHATBOT",
      "title": "单轮 LLM",
      "desc": "只能被动应答，没有上下文持久化，也不能执行工具。",
      "bullets": ["单向文本输出", "无状态执行，易出现幻觉", "需要 80% 的人工介入"],
      "highlight": false
    },
    {
      "tag": "AGENTIC CLUSTER",
      "title": "协同多智能体引擎",
      "desc": "编排专职子智能体，具备工具调用、共享记忆与确定性验证。",
      "bullets": ["动态推理与反思", "10 毫秒内的状态同步", "整体吞吐提升 400% 以上"],
      "highlight": true
    }
  ]
}
```

---

### 3. `architecture_stack`（多层架构栈）
展示 3 到 4 个水平的架构层级，每层包含若干模块化组件。

```json
{
  "layout_type": "architecture_stack",
  "narrative_arc": "breakthrough",
  "mission": "展示平台各层之间清晰的关注点分离",
  "transition": "【突破】因此，我们建立一个解耦的三层架构",
  "action_title": "架构：解耦的三层底座保障企业级安全",
  "core_evidence": "严格的沙箱隔离防止跨租户数据泄露；99.95% 的 SLA 保证",
  "title": "企业级 Agentic 平台架构",
  "subtitle": "解耦、多租户的运行环境，工具调用受治理",
  "layers": [
    {
      "name": "交互与客户端层",
      "desc": "统一的界面与协议网关",
      "items": ["聊天工作区", "IDE 插件", "OpenAPI 网关", "CLI 工具"]
    },
    {
      "name": "编排与规划层",
      "desc": "认知推理与记忆状态",
      "items": ["意图探针", "AST 解构器", "同步哨兵", "质量审计员"]
    },
    {
      "name": "执行与工具层",
      "desc": "安全的沙箱环境",
      "items": ["MCP 工具服务器", "Python 代码沙箱", "向量库", "模型网关"]
    }
  ]
}
```

---

### 4. `metric_spotlight`（KPI 看板）
用超大数字、增量标签与说明，突出 3 到 4 项高影响力的指标。

```json
{
  "layout_type": "metric_spotlight",
  "narrative_arc": "evidence",
  "mission": "为性能与业务影响提供无可争辩的量化证明",
  "transition": "【举证】基准测试证明所有 KPI 都有可量化的提升",
  "action_title": "成效：自主完成率达到 94.8%，节省 90% 人力",
  "core_evidence": "94.8% 任务完成率、<8ms 同步延迟、45 秒端到端交付",
  "title": "关键运营与效率基准",
  "subtitle": "相对于行业标准基线的实测性能",
  "metrics": [
    {
      "label": "自主任务完成率",
      "value": "94.8%",
      "delta": "较基线 +38.4%",
      "desc": "复杂的多步工程任务，无需人工重试即可完成"
    },
    {
      "label": "状态同步延迟",
      "value": "<8ms",
      "delta": "延迟 -85%",
      "desc": "实时 SHA-256 指纹差异计算的开销"
    },
    {
      "label": "完整演示构建",
      "value": "45s",
      "delta": "提速 10 倍",
      "desc": "从非结构化文档摄取到经验证的双端交付"
    }
  ]
}
```

---

### 5. `timeline`（路线图与里程碑）
按时间顺序呈现 3 到 4 个里程碑，各带具体交付物。

```json
{
  "layout_type": "timeline",
  "narrative_arc": "progression",
  "mission": "明确分阶段推进与交付的预期",
  "transition": "【递进】执行分四个阶段分步部署",
  "action_title": "路线图：分阶段推进，60 天内交付试点价值",
  "core_evidence": "第 1 阶段试点在 60 天内、3 个核心小队中证明 ROI",
  "title": "实施路线图与里程碑",
  "subtitle": "从试点验证到全企业推广的结构化分阶段推进",
  "steps": [
    {
      "time": "第 1 阶段（第 1–2 月）",
      "title": "试点验证",
      "items": ["核心 POC 验证", "模板标准库搭建", "私有 VPC 沙箱部署"]
    },
    {
      "time": "第 2 阶段（第 3–4 月）",
      "title": "平台推广",
      "items": ["多智能体集群上线", "MCP 工具服务器集成", "接入 30% 的工程团队"]
    },
    {
      "time": "第 3 阶段（第 5–6 月）",
      "title": "企业规模化",
      "items": ["全公司统一规范", "实时向量记忆同步", "运营分析看板"]
    }
  ]
}
```

---

### 6. `matrix_2x2`（战略 2x2 矩阵）
把概念放在两条正交的坐标轴（如技术范围 vs. 治理控制）上，分到 4 个象限。

```json
{
  "layout_type": "matrix_2x2",
  "narrative_arc": "breakthrough",
  "mission": "对战略选项分类，论证目标架构的定位",
  "transition": "【突破】评估备选方案需要在速度与治理之间取得平衡",
  "action_title": "矩阵：目标定位兼顾动态适应性与零信任安全",
  "core_evidence": "右上象限实现了风险调整后的最优运营速度",
  "title": "战略架构定位矩阵",
  "subtitle": "在各类企业方案模型上映射自主性与合规性",
  "axes": {
    "x": "自动化自主性",
    "y": "治理与合规控制"
  },
  "quadrants": [
    { "name": "临时脚本", "desc": "自主性低、治理弱；人工摩擦大", "tag": "淘汰" },
    { "name": "僵化工作流", "desc": "自主性低、治理强；对变化很脆弱", "tag": "过渡" },
    { "name": "失控机器人", "desc": "自主性高、治理弱；风险不可接受", "tag": "避免" },
    { "name": "受治理的 Agentic 集群", "desc": "自主性高，有严格的策略护栏", "tag": "目标" }
  ]
}
```

---

### 7. `maturity_ladder`（成熟度阶梯）
展示从初始的临时状态到自主成熟的 3 到 5 级演进。

```json
{
  "layout_type": "maturity_ladder",
  "narrative_arc": "progression",
  "mission": "为组织与技术的演进提供具体路径",
  "transition": "【递进】能力经过四个不同的成熟度层级逐级提升",
  "action_title": "成熟度：逐级的能力门禁防止过早暴露于运营风险",
  "core_evidence": "每一级都需要 95% 以上的审计通过率才能过门禁",
  "title": "能力成熟度演进模型",
  "subtitle": "逐级的能力成长，每一级都有具体的里程碑验证标准",
  "levels": [
    { "step": "L1", "name": "人工辅助", "desc": "孤立的提示词补全", "target": "个人效率", "focus": "提示词库", "metric": "+15% 速度" },
    { "step": "L2", "name": "工作流集成", "desc": "串联的流水线", "target": "团队生产力", "focus": "任务自动化", "metric": "-40% 人工步骤" },
    { "step": "L3", "name": "自主智能体", "desc": "多智能体协作", "target": "系统性杠杆", "focus": "MCP 工具沙箱", "metric": "90% 以上自主完成" },
    { "step": "L4", "name": "自优化集群", "desc": "动态反思", "target": "组织敏捷性", "focus": "演化式记忆", "metric": "持续优化" }
  ]
}
```

---

### 8. `horizons_curve`（三道地平线增长模型）
把投入归入地平线 1（核心运营）、地平线 2（新兴能力）和地平线 3（未来转型）。

```json
{
  "layout_type": "horizons_curve",
  "narrative_arc": "breakthrough",
  "mission": "在不同时间跨度上分配组织的精力与预算",
  "transition": "【突破】资源分配必须在眼前的 ROI 与长期的领先之间取得平衡",
  "action_title": "分配：把三道地平线的资源配比从 70:20:10 调整为 50:30:20",
  "core_evidence": "把 30% 的预算转入 H2，带来 3 倍的下游管线价值",
  "title": "三道地平线增长与投资模型",
  "subtitle": "在眼前的业务效率与长期的战略转型之间取得平衡",
  "horizons": [
    { "horizon": "H1", "name": "核心提效", "desc": "自动化常规的文档与代码生成", "focus": "立竿见影的降本", "kpi": "削减 80% 人工工时" },
    { "horizon": "H2", "name": "平台扩展", "desc": "企业级智能体编排与共享记忆", "focus": "跨团队杠杆", "kpi": "接入 50 个以上团队" },
    { "horizon": "H3", "name": "自主运营", "desc": "自学习的多智能体生态", "focus": "新商业模式", "kpi": "全新的自动化产品" }
  ]
}
```

---

### 9. `cross_mapping`（跨层对齐表）
把挑战映射到解法，以及各组织层或架构层上的负责人。

```json
{
  "layout_type": "cross_mapping",
  "narrative_arc": "evidence",
  "mission": "把技术方案与运营相关方直接对齐",
  "transition": "【举证】每一项技术举措都直接对应一个具体的运营负责人",
  "action_title": "对齐：业务、平台、数据三层的直接映射",
  "core_evidence": "每一层指定唯一负责人，确保不出现跨部门僵局",
  "title": "跨层转型映射",
  "subtitle": "从现有痛点到战略杠杆的可追溯映射",
  "mapping_rows": [
    { "layer": "高管治理", "current": "AI 采用指标不透明", "target": "实时合规看板", "action": "成立 AI 治理委员会" },
    { "layer": "平台工程", "current": "脆弱的零散 API 调用", "target": "标准化的 MCP 工具网格", "action": "部署沙箱运行时节点" },
    { "layer": "运营与团队", "current": "零散的员工工具", "target": "统一的工作区智能体技能", "action": "强制执行 undoPPT 超级 Skill 的 SOP" }
  ]
}
```

---

### 10. `summary`（高管要点与决议）
总结 3 到 4 条战略要点，并发出具体的行动号召。对于需要领导拍板的文稿，请用下面的决策闭环字段（v3.4）：此时页面显示的是方案选项、推荐结论和待批清单，而不是要点。

```json
{
  "layout_type": "summary",
  "narrative_arc": "call_to_action",
  "mission": "争取高管批准并立即启动执行",
  "transition": "【行动号召】平台与治理方案已经就绪，可以启动",
  "action_title": "决议：批准第 1 阶段试点项目并配置工程小队",
  "core_evidence": "认知契约与架构已验证；试点 ROI 预计 60 天内可见",
  "title": "战略决议与下一步",
  "subtitle": "快速启动与受治理的试点执行的指导原则",
  "points": [
    { "title": "坚守认知契约纪律", "desc": "在编写演示文稿之前，严格对齐 Q1–Q4 相关方认知。" },
    { "title": "采用母版穿透", "desc": "用自动化的母版解构与设计令牌统一所有文稿。" },
    { "title": "部署双端交付", "desc": "交付带演讲备注的原生可编辑矢量 PPTX，以及零摩擦的 HTML。" },
    { "title": "保持始终同步的协作", "desc": "在 10 毫秒内追踪外部修改，让 AI 与人类创作者保持一致。" }
  ]
}
```

**决策闭环变体**（`options`、`recommendation`、`sign_off_items`）。对于面向领导的场景，审计要求必须有（`DECISION_ASK_MISSING`）。存在 `options` 时，页面绘制方案卡片、推荐条和待批清单，不绘制 `points`。

```json
{
  "layout_type": "summary",
  "narrative_arc": "call_to_action",
  "action_title": "决议：批准方案 B，Q1 启动试点，首期 300 万与 5 个人头",
  "core_evidence": "试点预算 300 万、5 个人头；Q3 完成率达 90% 作为二期的门禁",
  "options": [
    { "name": "方案 A：继续打补丁", "pros": "没有新增预算", "cons": "人工成本维持在 80%",
      "cost": "0 / 隐性人力", "risk": "高", "recommended": false },
    { "name": "方案 B：分阶段试点（推荐）", "pros": "两条业务线先行，每个阶段都有止损点", "cons": "需要两个团队参与联调",
      "cost": "300 万 + 5 个人头", "risk": "低", "recommended": true },
    { "name": "方案 C：全面重构", "pros": "天花板最高", "cons": "约 18 个月，连续性风险",
      "cost": "2,000 万以上", "risk": "极高", "recommended": false }
  ],
  "recommendation": "推荐方案 B：以 300 万换取 Q3 前可验证的 94.8% 完成率；达标后才释放二期预算。",
  "sign_off_items": [
    "1. 批准 300 万预算与 5 个人头，Q1 正式立项",
    "2. 指派平台组与两条试点业务线各 1 名负责人",
    "3. 确认 Q3 门禁：完成率不低于 90% 才进入二期"
  ]
}
```

使用 2 到 3 个方案，且恰好有一个 `recommended: true`，待批事项 3 条。

---

### 11. `standard_table`（规整数据表）
渲染高密度的、斑马纹交替的数据矩阵，带格式化的表头。

```json
{
  "layout_type": "standard_table",
  "narrative_arc": "evidence",
  "mission": "提供跨功能矩阵的详细对比数据",
  "transition": "【举证】详细的基准遥测数据证实了在所有方面的优势",
  "action_title": "对比：标准化引擎在全部 5 项标准上胜过旧工具",
  "core_evidence": "100% 原生矢量支持、10 毫秒内的差异检测、零位图伪影",
  "title": "企业方案功能对比",
  "subtitle": "把 undoPPT 与旧的模板系统及通用 AI 生成器做基准对比",
  "headers": ["评估指标", "旧式 AI PPT", "静态模板", "undoPPT 引擎"],
  "rows": [
    ["输出格式", "位图 / 不可编辑", "静态 XML 替换", "100% 原生矢量 PPTX + HTML"],
    ["母版解构", "不支持", "手工编写", "自动化 AST 解构器"],
    ["人类共同编辑", "单向覆盖", "只能手动", "亚 10 毫秒始终同步"],
    ["质量审计", "无", "无", "10 维双重审计器"],
    ["演讲备注", "通用文本", "无", "自动注入使命与讲稿"]
  ]
}
```

---

### 12. `data_chart`（原生 PowerPoint 矢量图表）
渲染原生的 Office/Keynote 图表，可通过表格数据编辑。

```json
{
  "layout_type": "data_chart",
  "narrative_arc": "evidence",
  "mission": "用原生可编辑的图表呈现可量化的趋势数据",
  "transition": "【举证】量化的遥测数据表明四个季度的效率持续增长",
  "action_title": "趋势：自动化交付量增长 400%，周期缩短 85%",
  "core_evidence": "Q1 到 Q4 交付量增长 400%；周期从 8 小时缩短到 45 分钟",
  "title": "季度效率与交付速度",
  "subtitle": "2026 财年企业演示文稿制作周期的实测数据",
  "chart_type": "column_clustered",
  "categories": ["2026 Q1", "2026 Q2", "2026 Q3", "2026 Q4"],
  "series": [
    {
      "name": "人工交付（小时）",
      "values": [8.5, 7.8, 6.2, 5.0]
    },
    {
      "name": "undoPPT 辅助（小时）",
      "values": [1.5, 0.9, 0.7, 0.4]
    }
  ]
}
```
*支持的 `chart_type` 取值*：`column_clustered`、`line`、`pie`。

---

### 13. `content_columns`（多栏主题卡片）
渲染 2 到 4 个并列的竖栏，各带头部标签、标题与条目化要点。

```json
{
  "layout_type": "content_columns",
  "narrative_arc": "breakthrough",
  "mission": "并列呈现多面的能力支柱",
  "transition": "【突破】这个框架建立在三根基础性的运营支柱之上",
  "action_title": "支柱：三根运营支柱支撑企业转型",
  "core_evidence": "组建了三个不同的小队，跨职能领导层均有代表",
  "title": "核心战略实施支柱",
  "subtitle": "为避免运营瓶颈而设计的模块化执行流",
  "columns": [
    {
      "tag": "STREAM A",
      "title": "基础设施与工具",
      "points": ["私有 VPC 部署", "MCP 工具服务器集群", "10 毫秒内的同步哨兵守护进程"]
    },
    {
      "tag": "STREAM B",
      "title": "治理与合规",
      "points": ["零信任 API 策略", "10 维审计门禁", "自动化的敏感信息脱敏"]
    },
    {
      "tag": "STREAM C",
      "title": "赋能与培训",
      "points": ["智能体提示词模式", "母版模板上手指南", "高管复盘模板"]
    }
  ]
}
```

---

### 14. `keynote_quote`（主题演讲金句）
渲染居中的金句版式：强调字体排印、作者身份，以及一枚可行动的要点徽标。

```json
{
  "layout_type": "keynote_quote",
  "narrative_arc": "breakthrough",
  "mission": "借专家权威与核心洞见，提供哲学层面的立足点",
  "transition": "【突破】正如管理学理论所说，认知清晰先于执行",
  "action_title": "洞见：没有认知对齐的技术，只会加速混乱",
  "core_evidence": "40 多个企业转型案例的共识",
  "title": "转型的指导原则",
  "subtitle": "为人机协作的工作流确立心态转变的框架",
  "quote_text": "动荡时代最大的危险不是动荡本身，而是仍然用昨天的逻辑行事。",
  "author": "彼得·德鲁克",
  "author_title": "现代管理学之父",
  "key_takeaway": "旧的幻灯片生成范式，必须被认知契约的纪律所取代。"
}
```

---

### 15. `process_flow`（横向流程）
渲染 3 到 6 个依次递进的流程步骤，带有序号徽标。

```json
{
  "layout_type": "process_flow",
  "narrative_arc": "progression",
  "mission": "清晰简洁地讲解流水线的运作机制",
  "transition": "【递进】端到端的执行遵循一条连续的 5 步流水线",
  "action_title": "工作流：5 步确定性流水线把原始想法变成经过验证的文稿",
  "core_evidence": "完整流水线在 45 秒内跑完，审计合规率 100%",
  "title": "端到端的认知工程工作流",
  "subtitle": "从非结构化文档摄取到经验证的双端演示交付",
  "steps": [
    { "step": "01", "name": "契约探针", "desc": "澄清 Q1–Q4 认知目标与受众预期。" },
    { "step": "02", "name": "AST 解构", "desc": "解构模板的母版版式、槽位坐标与令牌。" },
    { "step": "03", "name": "蓝图合成", "desc": "把内容映射到 15 种图元，严守预算上限。" },
    { "step": "04", "name": "双重审计与自愈", "desc": "校验结构红线与因果转折，并自我修复。" },
    { "step": "05", "name": "原生交付", "desc": "渲染带演讲备注的可编辑 PPTX 与单文件 HTML。" }
  ]
}
```

---

## 4. 内容预算规则与红线

为保持视觉层级、防止视觉溢出，引擎强制执行严格的预算上限：

| 图元 | 最大条目数 | 标题最大长度 | 文字密度建议 |
| :--- | :--- | :--- | :--- |
| `bento_cards` | 2–4 张卡片 | ≤ 32 字符 | 每张卡片 3 个要点，每个 ≤ 20 词 |
| `architecture_stack` | 3–4 层 | ≤ 28 字符 | 每层 3–5 个组件标签 |
| `metric_spotlight` | 3–4 项指标 | ≤ 30 字符 | 数值 ≤ 8 字符，说明 ≤ 25 词 |
| `timeline` | 3–4 步 | ≤ 30 字符 | 每步 2–3 个交付物 |
| `matrix_2x2` | 4 个象限 | ≤ 24 字符 | 每个象限 1 个标签 + 1 句说明 |
| `maturity_ladder` | 3–5 级 | ≤ 24 字符 | 每级 1 个目标、1 个侧重点、1 个指标 |
| `horizons_curve` | 3 道地平线 | ≤ 24 字符 | 每道地平线 1 个侧重点、1 个 KPI |
| `cross_mapping` | 3–5 行 | ≤ 28 字符 | 3 列：现状、目标、行动 |
| `standard_table` | ≤ 8 行、≤ 5 列 | ≤ 28 字符 | 单元格字符串精炼（≤ 15 词） |
| `data_chart` | ≤ 8 个类目 | ≤ 32 字符 | 1–3 个系列，数值数组干净 |
| `content_columns` | 2–4 栏 | ≤ 24 字符 | 每栏 2–4 个要点 |
| `keynote_quote` | 1 句金句 | ≤ 32 字符 | 金句 ≤ 40 词，1 条要点 |
| `process_flow` | 3–6 步 | ≤ 24 字符 | 1 个标题 + 1 句精炼的机制说明 |
