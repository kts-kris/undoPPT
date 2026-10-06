<div align="center">

# undoPPT (演示文稿智能解构与重构超级智能体)

**面向现代 AI Agent 的新一代演示文稿认知规划、母版解构与双端高保真渲染超级工程引擎**

[![Version](https://img.shields.io/badge/version-3.8.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Super%20Skill-orange.svg)](SKILL.md)

[English](README.md) | [简体中文](README_zh.md)

</div>

> **“认知契约（Contract）、解构母版（Undo）、图表化重构（Redo）、单文件极简交付（Zero-friction Delivery）、时刻与用户并肩（Always-in-Sync）”**  
> 📖 **深度阅读**：[《undoPPT 设计哲学与架构协同白皮书》](DESIGN_PHILOSOPHY_zh.md)（[English](DESIGN_PHILOSOPHY.md)）—— 彻底厘清 Agent 认知大脑与 Skill 执行底座的协同分工与五重质量保障闭环。  
> 📋 **PRD 需求文档**：[《undoPPT v3.4.0 企业 12 大场景专项提升与决策闭环 PRD》](docs/PRD_v3.4_ENTERPRISE_12_SCENARIOS_AND_DECISION_RIGOR.md) | [《v3.3.0 动效与决策沙盒 PRD》](docs/PRD_v3.3_KINETIC_DYNAMICS_AND_INTERACTION_SANDBOX.md) | [《场景避坑红线手册》](docs/zh/scenario_anti_patterns.md)

`undoPPT` 是为 **Cursor、Claude Code、OpenAI Codex、Windsurf、腾讯 WorkBuddy、Trae、Google Antigravity、OpenCode** 等现代办公与开发领域领先的 AI Agent 打造的新一代演示文稿超级 Skill 与自动化工程引擎。彻底终结传统 AI 生成 PPT **“通篇堆字、版面混乱、无法吸收企业母版、生成物不可二次编辑、逻辑因果断裂、人机交互单向割裂、企业汇报缺乏决策闭环与深度”** 的核心痛点。

---

## ✨ v3.8.0 新增：读懂真实模板、对比度有保证、动画名副其实

用真实的 PowerPoint 输出检验后，README 里原本承诺的三件事其实都不成立。v3.8 逐一修复。

- 🎨 **`undo` 现在能读真实模板。** 它只扫描幻灯片上显式写死的 RGB 填充，而真实模板根本没有，于是三份不同的 Office 主题（其中一份是深色）抽出来都是同一个浅蓝默认值。现在它读取主题的配色方案、母版背景和字体：同一份蓝图，三份模板，三种不同的设计。
- 🌗 **对比度是保证，不是愿望。** 低于 WCAG 4.5:1（大字 3:1）的文字，会按它背后的实际填充色被修复，保持色相；品牌色填充从不被改动。深色预设的决策页（此前几乎不可读）现在可用。`design_check` 校验令牌（对比度、最小字号、层级）。
- 🎬 **PowerPoint 真能播放的动画。** v3.3 起写入的动画 XML，PowerPoint 识别出的动画数是 **0**。新的时序树在每一页都被识别，且 `render-check` 会让 PowerPoint 来确认。动画现在**默认关闭**，只保留三种叙事动画：`reveal`、`contrast`、`build`。

详见 [v3.8 PRD](docs/PRD_v3.8_SKIN_AND_POISE.md) 与 [设计系统](docs/zh/design_system.md)。边界：模板的母版版式、背景图与 logo 不会放到生成的页面上；Keynote 未能验证。

---

## 🥩 v3.7.0 新增：每个数字都说清楚从哪来

没有出处的数字，读起来像证据，却无法核验。v3.7 把出处变成蓝图的一部分。

- 🏷️ **`source` / `status`**：可写在页面或条目上。没有出处的数字是 **待核**：页面右上角的琥珀色徽标、页脚的 `来源：…`，以及演讲备注和 `N` 键抽屉里的出处清单。
- 📥 **`cli.py ingest` 与 `cite`**：从 `.md` / `.txt` / `.csv` 抽取数字并保留 `文件:行号` 出处，再回填到蓝图。回填很保守：只匹配到一部分时，不会给没有出处的数字"背书"。
- 🚦 **`build --final`**：交付模式。仍有数字没有出处或是占位时拒绝构建。
- 🧪 **demo 现在遵守自己的规则**：以决策闭环页收尾，不含禁用词，编造的数字标注为"示例数据"，审计 100 分且无警告（v3.6 是 8 条）。
- ✍️ **套话替换建议**：每个被标记的词都附带具体改写方式。

详见 [v3.7 PRD](docs/PRD_v3.7_FLESH_PROVENANCE_AND_INGEST.md)。

---

## 🦴 v3.6.0 新增：先问清楚，再动笔

审计分数分不清"用真材料做的 PPT"和"凭空做的 PPT"：一句"帮我做一份关于 AI 的汇报"照样能拿 90 多分。v3.6 把质量闸门前移。

- 🧭 **`cli.py probe`**：写任何一页之前，先检查四个契约槽位（主旨、受众、认知差、决策）和场景专属事实，返回该问用户的问题。信息不足，不生成。
- 📚 **12 个场景的优秀提纲样例**（[docs/zh/scenario_outlines.md](docs/zh/scenario_outlines.md)）：每个场景的听众闸门、必须拍板的事，以及每一页需要的证据。没有证据，就不该有这一页。
- 🧱 **血肉预算**：`THIN_CONTENT` 与 `EVIDENCE_BUDGET` 标出内容撑不起版式的页面。
- 🐛 **修复静默丢字**：五种图元在规格书与渲染器里用了不同的字段名，`cross_mapping` 页丢掉 90% 的文字，`content_columns` 丢掉全部要点。现在蓝图里的每一个字符串都会进入 PPTX 与 HTML。

详见 [v3.6 PRD](docs/PRD_v3.6_SKELETON_CONTRACT_AND_EVIDENCE.md)。

---

## 🪞 v3.5.0 新增：皮囊底线与渲染验证闭环

一份审计 94 分的 PPT，打开仍可能是坏的。v3.5 在真实查看器（PowerPoint、Chrome）里渲染每一份交付物，并修复渲染中发现的问题：

- 📐 **内容自适应版面**：标题缩到单行，不再折行压住下方卡片；卡片按文字收缩；稀疏文字自动放大（上限 1.3 倍）；内容块在剩余空间居中。
- 🔤 **可读字号地板**：空间允许时正文不小于 12pt。v3.4 的决策页 64% 的字小于 11pt。
- 🌐 **真正离线的 HTML**：内联 Tailwind 运行时（无 CDN、无网络字体），固定 1340x754 画布等比缩放到任意屏幕，支持 `?slide=N` 深链接。
- 🔍 **`cli.py render-check`**：静态版面 lint（无需渲染器）+ PowerPoint/LibreOffice 与无头 Chrome 的真实渲染检查；`build` 会自动运行 lint。
- 🐛 **修复**：规划器会输出构建器不认识的 `kpi_dashboard` 图元，导致 QBR/OKR/人头评审的 PPT 出现空白页。

详见 [v3.5 PRD](docs/PRD_v3.5_SKIN_FLOOR_AND_RENDER_CHECK.md) 与 [更新日志](CHANGELOG.md)。

---

## 🧠 核心升级：企业 12 大实战场景深度穷尽与高管决策闭环 (v3.4.0)

在企业日常经营、向上管理、横向拉通与职级晋升中，**PPT 从来不是无病呻吟的汇报走过场，而是“以受众为中心的高效决策推动工程”**。`undoPPT v3.4.0` 针对企业 12 大典型实战场景展开系统化专项提升，带来四大决定性能力跨越：

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. 认知契约探针 (Cognitive Contract Probes)                                  │
│    • Q1: 我想表达什么？(主旨唯一性 / Core Message)                           │
│    • Q2: 我的对象是谁？(受众画像与防线 / Audience Profile & Defense)          │
│    • Q3: 对方知道什么、不知道什么？(认知差与盲区痛点 / Knowledge Delta)       │
│    • Q4: 希望对方看完后理解什么、相信什么、做什么？(决策与行动闭环 / Outcomes) │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. 企业 12 大典型场景认知推演骨架 (12 Enterprise Operational Scenarios)       │
│    • S01~S05 向上战略与管理: 立项答辩/年度战略OKR/经营复盘QBR/跨部门拉通/HC编制│
│    • S06~S07 研发与工程治理: 技术方案RFC评审 / 生产重大故障复盘与根因分析     │
│    • S08~S09 商业与客户开拓: 新产品发布GTM / 大客户商务提案与竞标RFP         │
│    • S10~S12 个人战功与组织宣导: 晋升述职答辩 / 内部技术分享培训 / 全员誓师大会│
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. 终局高管决策闭环 (Executive Decision-Ready Ask)                           │
│    • 多方案互斥决策矩阵 (Option A vs B vs C，明确利弊代价与预算)            │
│    • 权威推荐建议突出 (Highlighted Recommendation Callout)                   │
│    • 待批决议清单 (Sign-off Checklist): 现场可交互勾选 HC/预算/里程碑/仲裁点 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. 严谨性红线审查机制 (Rigor Enforcement Protocols)                          │
│    • 外部对标充分性审查: 严禁自嗨式全赢，强制三维参照系并自曝摩擦与适用边界 │
│    • 述职战功纯度审查: 强制 STAR 归因，剥离大盘红利突出个人净增量贡献         │
└─────────────────────────────────────────────────────────────────────────────┘
```

- 🎯 **企业 12 大典型实战场景推演引擎**：精准分类并深度定制 12 大企业场景的推演逻辑，从《立项答辩》、《年度战略 OKR》、《经营复盘 QBR》、《跨部门拉通》、《HC编制》、《技术方案RFC》、《故障复盘》、《新产品GTM》、《大客户竞标RFP》、《晋升答辩》、《内部技术培训》到《全员誓师大会》，彻底终结模板千篇一律的机械套用。
- ⚖️ **终局“请领导决策与审批清单”高阶图元**：收尾页告别空洞问答，结构化输出方案对比矩阵、推荐主选方案与审批清单（Sign-off Items）。在 PPTX 端渲染原生高对比度决策卡片，在 HTML 端支持现场点击勾选批准决议（现场演示即决议）。
- 🔬 **外部对标充分性审查协议（三维参照系）**：代码级拦截单维度浅层拉踩，要求覆盖「行业 Tier-1 标杆」、「开源/新锐方案」与「现状/自研方案」三维参照系；强制自述本方案的代价（成本、迁移摩擦、适用边界、复杂度），杜绝盲目宣称“全面领先”。
- 🎖️ **晋升述职战功真实归因协议**：严格执行 STAR 结构化归因，以代码规则严格拦截流水账（“参与了/负责了...”）；核验个人在团队成果中的“净增量贡献（Net Increment）”，严禁将公司业务自然增长的大盘红利包装为个人战功。
- 🎬 **叙事动画（默认关闭）**：三种类型，各有理由：`reveal` 逐条出现（一次点击一个观点）、`contrast` 对比先后（先出现备选，再出现推荐）、`build` 数据递进（数据一块一块出现）。时序树按 PowerPoint 自己的写法生成，`render-check` 会让 PowerPoint 确认它识别了每个动画对象；Keynote 未能验证。（v3.3–v3.7 写入的时序树，PowerPoint 一个也不识别。）
- ⚡ **叙事弧线节奏**：动画时长随页面的叙事弧线变化（冲突 250ms、实证 600ms）。HTML 中的数字跑表与流光仅在叙事模式下运行（`build --motion narrative`）。
- 🎙️ **现场演播双重视野中枢 (Live Presenter HUD，按 `P` 键)**：单文件 HTML 按 `P` 键激活现场中枢，内嵌认知罗盘（主旨与受众立场向心力）、因果提词器（切页口播连词）与评委质疑应对弹药库（典型发难与权威解题对策）。
- 🎛️ **活动决策推演沙盒 (Active Sandbox & 架构下钻)**：支持现场切换“保守 / 基准 / 突破”情景并动态重绘 KPI 跑表与图表；架构栈支持点击微服务组件即刻弹出技术规格（SLA 目标、P99、容灾回滚机制与故障隔离）。
- 🧠 **跨工具链毫秒级意图反思飞轮 (`cli.py sync`)**：`SyncWatcher` 升级语义反思引擎，捕获人类专家在 Office/Keynote 中修改数值与结构的深层战略动机，指导 AI 智能体保持意图并肩同频。
- 🚫 **场景避坑红线与代码级黑话拦截**：沉淀场景避坑红线手册（[scenario_anti_patterns.md](docs/zh/scenario_anti_patterns.md)），内置黑话过滤库，严禁“不仅是X更是Y”、“闭环/抓手/赋能/打法”等空洞套话，严禁伪造测试基准。
- 📊 **15 大信息图元与原生矢量图表**：原生 PowerPoint 矢量图表（柱状/折线/饼图）、规整数据表格、多栏并列卡片、金句引用与流程推演。详见 [图元蓝图规约手册](docs/zh/blueprint_specification.md)。
- 💡 **自动化内容与因果审计 (`cli.py audit`)**：内置场景感知审计器，兼顾商业量化数据与教学定性范例，实时评分并给出整改建议。
- 🔍 **HTML 认知动力学抽屉 (`N` 键)**：在单文件 HTML 演示文稿中按键盘 `N` 键，随时调出当前页的推演逻辑与论据层级。


---

## ⚡ 30 秒开始 (Quickstart)

```bash
npx skills add https://github.com/kts-kris/undoPPT --skill undo-ppt
```

也可以直接把这段话发给有 shell 权限的 AI Agent（Cursor、Claude Code、OpenAI Codex、Windsurf、腾讯 WorkBuddy、Trae、Google Antigravity 等）：

```text
帮我安装 undo-ppt。请把 https://github.com/kts-kris/undoPPT 克隆到你的 skills 目录（如 Cursor / Claude Code / Codex / WorkBuddy 对应 ~/.claude/skills/undo-ppt 或项目 .agents/skills/undo-ppt，Antigravity 对应 ~/.gemini/config/skills/undo-ppt）
```

已经安装过的话，用这段话更新：

```text
帮我更新 undo-ppt。请进入 ~/.gemini/config/skills/undo-ppt 执行 git pull，然后告诉我当前最新提交
```

**安装后直接对 Agent 说：**

> “我要编写某大型制造企业的数字化转型与 AI 战略规划，控制在 6 页，要求具备四层协同映射、2x2战略矩阵、四级阶梯进阶和三道地平线分池治理。”

---

## 🌟 六大工业级超级能力 (Super Capabilities)

### 1. 动态事实锚定规划器 (Dynamic Grounded Cognitive Planner)
- **自然语言与外部事实文档无缝双输入**：无需人工编写复杂的 JSON，内置 `CognitivePlanner` 不仅能从一句话提示词推演完整逻辑，更支持挂载外部参考文档（`--input-doc notes.md`）。
- **事实数据与业务实体精准挖掘**：自动从长文中提取组织层级、关键痛点与核心量化指标（如 `418个`、`71个`、`80%`、`7:2:1转向4:3:3`），动态编译进蓝图。
- **自反思自愈修正循环 (Self-Correction Loop)**：生成蓝图后自动发起认知审计，若检测到中性标题、缺少因果过渡或证据不足，自动触发自愈补丁（Auto-patching）完成二轮修复。

### 2. 深度语义认知审计器 (Deep Semantic Cognitive Auditor)
- **6 大因果本体修辞分类**：严格审计页间连接词在 `contrast`（对立冲突）、`causality`（因果推演）、`breakthrough`（方案突破）、`progression`（递进深化）、`evidence`（硬核实证）、`action`（决议行动）六大修辞本体的咬合与多样性。
- **顶层主旨离心漂移检测**：自动提取主旨关键词，核验每一页的向心力，杜绝跑题与信息孤岛。
- **Smoking Gun 铁证加权**：多维识别百分比、比率、工时、延迟等硬核数据，杜绝定性空洞口号。
- **受众疑虑对抗与闭环**：核验方案是否正面击穿痛点，收尾页是否坚决闭环目标行动决策。
- **可插拔 LLM 裁判**：提供 `llm_judge_fn` 钩子，支持规则本体与大模型裁判协同。

### 3. 十五大高阶原生图元组件库 (15 Infographic Primitives)
拒绝大段无聊文本，内置 15 大工业级图表化与数据组件元语（详见 [图元规范手册](docs/zh/blueprint_specification.md)）：
- 🏗️ **产品/技术架构堆叠图 (Architecture Stacks)**：分层底板、微服务组件卡片、分类标签。
- 🍱 **Bento 多栏对比卡片 (Bento Grid Cards)**：2/3/4 栏对比、高亮方案框、要点列表。
- 📊 **KPI 核心指标大字报 (Metric Spotlight)**：超大字体数值、同环比标签、下钻说明。
- ⏱️ **横向推进时间轴与里程碑 (Timeline Roadmap)**：节点圆环、连接轴线、阶段交付清单。
- 🎯 **2x2 战略矩阵与象限 (Matrix 2x2)**：技术广度 × 价值链控制力等四象限分布图与原则卡。
- 🪜 **多维成熟度阶梯模型 (Maturity Ladder)**：四级演进台阶、抓手、指标与全生命周期安全底线。
- 📈 **三道地平线发展模型 (Three Horizons)**：H1成熟效率、H2流程突破、H3模式验证分池治理。
- 🔀 **跨层级/跨组织映射对比表 (Cross Mapping)**：双向对齐箭头、标杆实践对比、落地机制责任链。
- 🏁 **收官要点速览 (Summary Takeaways)**：胶囊编号卡片与战略决策建议。
- 🖼️ **高保真标题封面卡 (Cover Hero)**：分类徽章、主副标题与作者元数据。
- 📋 **规整数据与能力对比表 (Standard Table) [v3.0]**：原生 PowerPoint/HTML 斑马纹双色规整数据矩阵。
- 📊 **原生矢量数据图表 (Data Chart) [v3.0]**：基于 `CategoryChartData` 的原生矢量柱状图、折线图与饼图（可在 Office/Keynote 中直接改数据）。
- 📑 **多栏并列内容卡片 (Content Columns) [v3.0]**：2~4 栏并列卡片，配备分类胶囊与清单要点。
- 💬 **金句引用与破局卡片 (Keynote Quote) [v3.0]**：大师名言/核心洞见视觉居中强化与 Key Takeaway 启示。
- 🔄 **横向流程推进步骤 (Process Flow) [v3.0]**：带序号胶囊与阶段推演的横向流程图。

### 4. 模板解构引擎 (Undo Engine)
- **真实主题读取（v3.8）**：读取模板自己的主题：配色方案（`theme1.xml`）、母版的颜色映射与背景（解析 `lumMod`/`lumOff`）、主题字体（含中文字体）。配色、明暗与字体都来自这里，品牌色从不被改写。三份 Office 主题实测得到三套不同的设计（v3.7 对它们返回的是同一个浅蓝默认值）。
- **对比度与字号校验（v3.8）**：抽取出的令牌会按 WCAG 对比度与最小字号检查，修正记录在 `design_notes`。详见 [设计系统](docs/zh/design_system.md)。
- **母版槽位绝对坐标 AST 提取**：深度遍历 Slide Masters 与 Layouts，提取 `Title`、`Body`、`Subtitle`、`Footer` 的绝对坐标（英寸）与相对网格尺寸。
- **诚实边界**：配色、明暗与字体会带过来；模板的母版版式、背景图与 logo **不会**放到生成的页面上（引擎自己绘制 16:9 版式）。
- **嵌入式高清视觉与 Logo 提取**：自动导出母版与页面中嵌入的图片与矢量 Logo 至 `.undoppt/assets/`。

### 5. 双端极简交付与认知自省 (Dual-Format Delivery & Notes Inspection)
- **PowerPoint PPTX**：100% 原生矢量形状、规整表格与矢量图表，可在 Microsoft PowerPoint / Apple Keynote 中自由二次编辑，**绝不贴图**；自动将单页使命、因果转折和核心证据注入底层 Speaker Notes 演讲备注。
- **单文件自包含 HTML**：将演示文稿打包为单个 `.html` 文件，内置精美排版、键盘导航（←/→/Space/F 全屏）、进度条，按 `N` 键滑出认知动力学抽屉，**双击即播，零依赖，极度易于分发**。

### 6. 毫秒级双向协同感知 (Always-in-Sync)
- 每一轮对话伊始，优先运行 **Sync Watcher**，在 `<10ms` 内完成 SHA-256 指纹比对。
- 若用户在外部对 PPTX 进行了手动修改（如调整标题、删减节点、微调颜色），智能体自动生成 AST 差异分析，并在回复开始前主动告知用户：“*检测到您在本地修改了第 3 页，已同步更新意图...*”，真正实现人机并肩共创。

---

## 📁 目录结构

```text
undoPPT/
├── .agents/skills/undo-ppt/         # Antigravity 工作区 Skill 注册目录
│   └── SKILL.md                    # 超级 Skill 主指令规范与 SOP (v3.5.0)
├── core/                           # 核心 Python 自动化引擎
│   ├── __init__.py                 # 版本号导出 (3.5.0)
│   ├── cognitive_planner.py        # 6 大场景通用解耦认知规划器与自愈修正循环 (v3.1.0)
│   ├── semantic_auditor.py         # 场景感知语义因果认知审计器 (修辞/离心/实证/疑虑)
│   ├── content_auditor.py          # 15 大图元 10 维认知质量与容量预算综合审计器
│   ├── undo_engine.py              # 母版 AST 槽位解析与明暗主题/资产逆向解构
│   ├── vision_extractor.py         # 视觉启发式解析器
│   ├── pptx_builder.py             # 15 大图元原生矢量 PPTX 构建器 (含原生图表与 Speaker Notes)
│   ├── html_builder.py             # 15 大图元单文件自包含 HTML 演示编译器 (含 N 键认知抽屉，可离线)
│   ├── motion.py                   # 叙事动画：reveal / contrast / build（默认关闭）
│   ├── theme_reader.py             # 读取真实模板主题：配色方案、母版背景、字体
│   ├── contrast.py                 # WCAG 对比度计算与逐字背景检测
│   ├── design_check.py             # 令牌的对比度、最小字号、层级（检查/修复）
│   ├── provenance.py               # 数字识别、出处覆盖、待核标记
│   ├── ingest.py                   # 抽取带 文件:行号 出处的数据点 (md/txt/csv)
│   ├── contract_probe.py           # 认知契约探针（动笔前还缺哪些信息）
│   ├── blueprint_compat.py         # 文档字段 -> 渲染器字段映射（杜绝静默丢字）
│   ├── layout_fit.py               # 内容自适应版面（标题适配、卡片收缩、字号地板、居中）
│   ├── layout_lint.py              # PPTX 静态几何 lint（溢出、重叠、标题折行）
│   ├── render_check.py             # 基于 PowerPoint/LibreOffice 与无头 Chrome 的真实渲染验证
│   ├── vendor/                     # 内联的 Tailwind 运行时 (MIT)，保证 HTML 离线可用
│   └── sync_watcher.py             # 毫秒级指纹追踪与语义 AST 差异对比器
├── docs/                           # 完整技术文档库
│   └── en/                         # 英文技术规格与手册
│       ├── blueprint_specification.md # 15 大图元完整 JSON Schema 与样例
│       ├── cli_reference.md        # CLI 全命令参数速查手册
│       ├── architecture.md         # 引擎深度架构与流水线解析
│       └── agent_integration.md    # 主流 AI Agent 接入指引
├── presets/                        # 4 大工业级预设设计系统 (含 content_budget 预算规则)
│   ├── modern_bento.json           # 现代企业 Bento 卡片 (默认)
│   ├── consulting_minimalist.json  # 顶级战略咨询高密度极简
│   ├── tech_keynote.json           # 科技暗黑大屏展演
│   └── enterprise_architecture.json# 架构工程实战容器
├── tests/                          # 自动化单元、回归、版面与契约测试套件 (165 passing)
│   ├── test_engine.py
│   ├── test_layout.py
│   ├── test_contract.py
│   ├── test_flesh.py
│   ├── test_motion_design.py
│   └── test_docs.py                # 文档必须跟上代码
├── output/                         # 生成的交付物（已加入 .gitignore，可用 `cli.py demo` 重建）
├── .undoppt/                       # 内部元数据缓存 (tokens, blueprint, sync, assets)
├── cli.py                          # 统一命令行交互入口 (plan / generate / undo / build / audit / sync / demo)
├── DESIGN_PHILOSOPHY.md            # 核心设计哲学与 Agent-Skill 协同白皮书 (英文版)
├── DESIGN_PHILOSOPHY_zh.md         # 核心设计哲学与 Agent-Skill 协同白皮书 (中文版)
├── README.md                       # 项目主说明文档 (默认英文)
├── README_zh.md                    # 项目中文说明文档
├── CONTRIBUTING.md                 # 贡献指南 (英文)
└── CHANGELOG.md                    # 语义化版本变更记录
```

---

## 🚀 快速上手 (CLI Quickstart)

### 1. 环境依赖
仅需 Python 3.10+ 及 `python-pptx`：
```bash
pip install -r requirements.txt
```

### 2. 自主规划与生成 (Plan & Generate)
支持一句话输入，可选挂载事实参考文档：
```bash
# 规划高分蓝图 (支持参考文档摄取与自愈修正)
python3 cli.py plan --prompt "某大型制造企业数字化战略规划" [--input-doc doc.md]

# 一键端到端极速交付 (规划 -> 事实锚定 -> 审计 -> 双端构建)
python3 cli.py generate --prompt "某大型制造企业数字化战略规划" [--input-doc doc.md] [--template /path/to/template.pptx]
```

### 3. 内容质量与深度语义因果审计 (Audit)
在生成前对蓝图进行严格的结构质量与语义修辞审计（综合分 + 结构分 + 语义分 + 4大子项）：
```bash
python3 cli.py audit --blueprint .undoppt/blueprint.json
```

### 4. 解析提取用户模板母版 (Undo)
深度解构企业 PPTX 模板母版、槽位坐标、明暗主题与多媒体资产：
```bash
python3 cli.py undo --template /path/to/company_template.pptx --out .undoppt/design_tokens.json
```

### 5. 基于蓝图与规范渲染 (Build)
```bash
python3 cli.py build --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json --format all
```

### 6. 毫秒级协同感知与 Diff 检查 (Sync)
当您在本地用 PowerPoint 或 Keynote 修改了交付物后，检查改动：
```bash
python3 cli.py sync --target output/presentation.pptx
```

### 7. 动笔前检查需求 (Probe)
```bash
python3 cli.py probe --prompt "智能客服业务立项答辩，申请首期预算，预期人效提升 40%"
```
报告哪些契约槽位和场景事实还不知道，以及应先问的问题。完备度低时，`plan`/`generate` 也会打印同样的提示。

### 8. 给每个数字一个出处 (Ingest / Cite / Final)
```bash
python3 cli.py ingest --input-doc notes.md --out .undoppt/facts.json
python3 cli.py cite --blueprint .undoppt/blueprint.json --facts .undoppt/facts.json
python3 cli.py build --blueprint .undoppt/blueprint.json --final   # 仍有待核数字时拒绝构建
```

### 9. 套用企业模板并加动画
```bash
python3 cli.py undo --template company.pptx --out .undoppt/design_tokens.json
python3 cli.py build --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json --motion narrative
```

### 10. 版面验证 (Render Check)
```bash
python3 cli.py render-check --pptx output/presentation.pptx                       # 静态 lint，无需渲染器
python3 cli.py render-check --pptx output/presentation.pptx --html output/presentation.html --render
```
`--render` 需要 `pip install -r requirements-dev.txt`，PPTX 渲染需要 PowerPoint (macOS) 或 LibreOffice，HTML 检查需要 Chrome。

---

## 🤖 在各大主流 AI Agent（Cursor、Claude Code、Codex、Windsurf、WorkBuddy 等）中使用

本项目支持在各大主流 AI Agent 环境中无缝挂载使用（详见 [Agent 集成指南](docs/zh/agent_integration.md)）：
1. **Cursor / Claude Code / OpenAI Codex**：克隆到对应 Agent 的标准 skills 路径（如 `~/.claude/skills/undo-ppt` 或工作区 `.agents/skills/undo-ppt`）；
2. **Windsurf / Trae**：在当前项目根目录 `.agents/skills/undo-ppt/` 或全局配置中直接挂载；
3. **腾讯 WorkBuddy / 办公智能体平台**：作为办公自动化或企业自定义工作流 Skill 直接导入；
4. **Google Antigravity**：支持工作区 `.agents/skills/undo-ppt/SKILL.md` 与全局 `~/.gemini/config/skills/undo-ppt/SKILL.md` 双重感知；
5. **OpenCode** 等开源智能体：直接识别根目录 `SKILL.md` 规范。

在任意对话中，只需自然表达您的 PPT 诉求即可触发：
> *“帮我准备一份面向管理层的企业级 AI 战略规划汇报，我有一个公司的模板 PPT。”*

Skill 会自动进入 **Rhythm A 深度引导流程**：
0. **就绪探针**：先用 `probe` 判断信息够不够——**信息不足就先向您提问，不直接生成**；
1. **认知契约与深度探针**：主动澄清核心论题、受众立场偏好、认知差与终局行动目标；
2. **模板解构与规范学习**：读取您模板的真实主题（配色、明暗、字体）；
3. **蓝图编排、出处与质量审计**：规划每页的图表化元语；用 `ingest` / `cite` 给每个数字一个出处；执行 10 维内容质量审核，以及"内容撑不撑得起版式""数字有没有出处"的检查；
4. **双模交付**：先出草稿（没有出处的数字带"待核"徽标），确认后用 `--final` 交付内置演讲备注的 PPTX + 可离线使用的单文件 HTML；需要现场演讲时再加 `--motion narrative`；
4.5. **渲染验证**：用 PowerPoint 与 Chrome 真实渲染并检查溢出、对比度与动画；
5. **实时协同**：感知您的每一次本地手动调整并持续保持同频！

---

## 🧪 自动化测试验证

运行单元、回归与版面测试套件：
```bash
pip install -r requirements-dev.txt
python3 -m pytest tests -q              # 或：python3 -m unittest discover -s tests
```

165 个测试通过（另有 1 个需要 macOS 上的 PowerPoint：`UNDOPPT_TEST_POWERPOINT=1`）。已在 Python 3.12 与 3.14 上验证；代码声明支持 3.10+，但 3.10、3.11、3.13 尚未实际运行。

---

## 📚 文档索引

> 下面的八份参考文档都有中英文两个版本：每份顶部都有语言切换，英文版在 `docs/en/`，中文版在 `docs/zh/`。

- 📖 [设计哲学白皮书](DESIGN_PHILOSOPHY_zh.md)（[English](DESIGN_PHILOSOPHY.md)）
- 📐 [Blueprint 规约手册](docs/zh/blueprint_specification.md)（含 `source` / `status` / `motion`）
- 💻 [CLI 命令参考](docs/zh/cli_reference.md)（`probe`、`ingest`、`cite`、`render-check`、`build --final / --motion`）
- 🚦 [审计码速查](docs/zh/audit_codes.md)：每个 `audit` 码的含义与修法
- 🎨 [设计系统](docs/zh/design_system.md)：令牌、对比度与字号保证、套用企业模板
- 🗂️ [12 个场景提纲样例](docs/zh/scenario_outlines.md)：每个企业场景的听众闸门、决策事项与每页所需证据
- 🚫 [场景避坑红线](docs/zh/scenario_anti_patterns.md)
- 🏗️ [引擎架构详解](docs/zh/architecture.md)
- 🔌 [AI Agent 集成指南](docs/zh/agent_integration.md)
- 🧾 [更新日志](CHANGELOG.md) 与各版 PRD：[v3.2](docs/PRD_v3.2_SCENARIO_REDLINES_AND_ANIMATION.md)、[v3.3](docs/PRD_v3.3_KINETIC_DYNAMICS_AND_INTERACTION_SANDBOX.md)、[v3.4](docs/PRD_v3.4_ENTERPRISE_12_SCENARIOS_AND_DECISION_RIGOR.md)、[v3.5](docs/PRD_v3.5_SKIN_FLOOR_AND_RENDER_CHECK.md)、[v3.6](docs/PRD_v3.6_SKELETON_CONTRACT_AND_EVIDENCE.md)、[v3.7](docs/PRD_v3.7_FLESH_PROVENANCE_AND_INGEST.md)、[v3.8](docs/PRD_v3.8_SKIN_AND_POISE.md)
- 🤝 [贡献指南](CONTRIBUTING.md)

---

## 📄 License & 版本演进

- 遵循 **MIT License** 开放许可，详见 [LICENSE](LICENSE)。
- 遵循 [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) 规范，详见 [CHANGELOG.md](CHANGELOG.md)。
