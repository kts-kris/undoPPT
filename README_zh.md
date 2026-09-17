<div align="center">

# undoPPT (演示文稿智能解构与重构超级智能体)

**面向现代 AI Agent 的新一代演示文稿认知规划、母版解构与双端高保真渲染超级工程引擎**

[![Version](https://img.shields.io/badge/version-3.2.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Super%20Skill-orange.svg)](SKILL.md)

[English](README.md) | [简体中文](README_zh.md)

</div>

> **“认知契约（Contract）、解构母版（Undo）、图表化重构（Redo）、单文件极简交付（Zero-friction Delivery）、时刻与用户并肩（Always-in-Sync）”**  
> 📖 **深度阅读**：[《undoPPT 设计哲学与架构协同白皮书》](DESIGN_PHILOSOPHY_zh.md)（[English](DESIGN_PHILOSOPHY.md)）—— 彻底厘清 Agent 认知大脑与 Skill 执行底座的协同分工与五重质量保障闭环。  
> 📋 **PRD 需求文档**：[《undoPPT v3.2.0 场景避坑红线与动效呈现 PRD》](docs/PRD_v3.2_SCENARIO_REDLINES_AND_ANIMATION.md) | [《6大场景避坑红线手册》](docs/en/scenario_anti_patterns.md)

`undoPPT` 是为 **Cursor、Claude Code、OpenAI Codex、Windsurf、腾讯 WorkBuddy、Trae、Google Antigravity、OpenCode** 等现代办公与开发领域领先的 AI Agent 打造的新一代演示文稿超级 Skill 与自动化工程引擎。彻底终结传统 AI 生成 PPT **“通篇堆字、版面混乱、无法吸收企业母版、生成物不可二次编辑、逻辑因果断裂、人机交互单向割裂”** 的核心痛点。

---

## 🧠 核心升级：15 大图元、6 大场景避坑红线与动效呈现架构 (v3.2.0)

在专业商业、战略咨询、技术架构、学术教学与个人述职场景下，**PPT 的本质不是美术画册，而是“以受众为中心的认知重塑与决策干预工程”**。`undoPPT v3.2.0` 全面汲取前沿 Skill 实践，沉淀严密的场景避坑红线与步进动效体系：

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. 认知基座 (Cognitive Contract)                                             │
│    • Q1: 我想表达什么？(主旨唯一性 / Core Message)                           │
│    • Q2: 我的对象是谁？(受众画像与立场偏好 / Audience Profile)               │
│    • Q3: 对方知道什么、不知道什么？(认知差与盲区痛点 / Knowledge Delta)       │
│    • Q4: 希望对方看完后理解什么、相信什么、做什么？(行动转化闭环 / Outcomes) │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. 全局叙事 (Narrative Dynamics)                                            │
│    • Q5: 演示按什么节奏展开？(叙事弧线: Hook → Conflict → Breakthrough...)  │
│    • Q10: 页面之间如何形成因果、冲突、递进、转折与结论？(页间推演语法)       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. 单页切片 (Slide Slicing & Budget)                                        │
│    • Q6: 每一页到底承担什么任务？(单页使命纯粹度 / Single Responsibility)    │
│    • Q7: 一页应该放多少信息？(信息容量预算红线 / Content Budget)            │
│    • Q8: 哪些信息先出现、哪些延后？(行动结论标题先行 / Action Titles)         │
│    • Q9: 哪些是核心证据、哪些只是补充？(铁证突出与次级降噪 / Proof vs Note)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

- 🚫 **场景避坑红线与代码级黑话拦截**：沉淀 6 大场景避坑红线手册（[scenario_anti_patterns.md](docs/en/scenario_anti_patterns.md)），内置黑话过滤库，严禁“不仅是X更是Y”、“闭环/抓手/赋能/打法”等空洞套话，严禁伪造测试基准（[PRD_v3.2](docs/PRD_v3.2_SCENARIO_REDLINES_AND_ANIMATION.md)）。
- 🎬 **动效呈现与步进式时序架构**：PPTX 自动注入标准 OOXML 原生切页过渡（`<p:transition>`，默认淡入淡出 `fade`）；单文件 HTML 原生支持 `S` 键开启步进演讲模式（空格键时序逐个展开图元组件，现场演示提供聚焦引导）。
- 🤖 **自主认知规划器 (`cli.py plan` / `cli.py generate`)**：从一句话提示词自主推演《认知契约》、叙事弧线、15 大信息图元与完备演讲脚本，支持 6 大场景自适应。
- 📊 **15 大信息图元与原生矢量图表**：新增原生 PowerPoint 矢量图表（柱状/折线/饼图）、规整数据表格、多栏并列卡片、金句引用与流程推演。详见 [图元蓝图规约手册](docs/en/blueprint_specification.md)。
- 💡 **自动化内容与因果审计 (`cli.py audit`)**：内置场景感知审计器，兼顾商业量化数据与教学定性范例，实时评分并给出整改建议。
- 🎙️ **PPTX 原生演讲备注注入**：单页使命（Mission）、承上启下连词（Transition）与核心证据（Core Evidence）自动编译进 PowerPoint Speaker Notes，自适应口播口吻。
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
拒绝大段无聊文本，内置 15 大工业级图表化与数据组件元语（详见 [图元规范手册](docs/en/blueprint_specification.md)）：
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

### 4. 母版 AST 深度逆向解构引擎 (Deep Master AST Decompiler)
- **母版槽位绝对坐标 AST 提取**：深度遍历 Slide Masters 与 Layouts，提取 `Title`、`Body`、`Subtitle`、`Footer` 的绝对坐标（英寸）与相对网格尺寸。
- **自动明亮/暗黑主题模式识别**：智能检测背景与形状亮度，自适应判定 `theme_mode` 并映射高对比度文字与卡片配色。
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
│   └── SKILL.md                    # 超级 Skill 主指令规范与 SOP (v3.1.0)
├── core/                           # 核心 Python 自动化引擎
│   ├── __init__.py                 # 版本号导出 (3.1.0)
│   ├── cognitive_planner.py        # 6 大场景通用解耦认知规划器与自愈修正循环 (v3.1.0)
│   ├── semantic_auditor.py         # 场景感知语义因果认知审计器 (修辞/离心/实证/疑虑)
│   ├── content_auditor.py          # 15 大图元 10 维认知质量与容量预算综合审计器
│   ├── undo_engine.py              # 母版 AST 槽位解析与明暗主题/资产逆向解构
│   ├── vision_extractor.py         # 视觉启发式解析器
│   ├── pptx_builder.py             # 15 大图元原生矢量 PPTX 构建器 (含原生图表与 Speaker Notes)
│   ├── html_builder.py             # 15 大图元单文件自包含 HTML 演示编译器 (含 N 键认知抽屉)
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
├── tests/                          # 自动化单元与回归测试套件 (15/15 passing)
│   └── test_engine.py
├── output/                         # 最终交付物目录
│   ├── presentation.pptx           # 可二次编辑的 PPTX (含备注)
│   └── presentation.html           # 单文件自包含 HTML (含认知抽屉)
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

---

## 🤖 在各大主流 AI Agent（Cursor、Claude Code、Codex、Windsurf、WorkBuddy 等）中使用

本项目支持在各大主流 AI Agent 环境中无缝挂载使用（详见 [Agent 集成指南](docs/en/agent_integration.md)）：
1. **Cursor / Claude Code / OpenAI Codex**：克隆到对应 Agent 的标准 skills 路径（如 `~/.claude/skills/undo-ppt` 或工作区 `.agents/skills/undo-ppt`）；
2. **Windsurf / Trae**：在当前项目根目录 `.agents/skills/undo-ppt/` 或全局配置中直接挂载；
3. **腾讯 WorkBuddy / 办公智能体平台**：作为办公自动化或企业自定义工作流 Skill 直接导入；
4. **Google Antigravity**：支持工作区 `.agents/skills/undo-ppt/SKILL.md` 与全局 `~/.gemini/config/skills/undo-ppt/SKILL.md` 双重感知；
5. **OpenCode** 等开源智能体：直接识别根目录 `SKILL.md` 规范。

在任意对话中，只需自然表达您的 PPT 诉求即可触发：
> *“帮我准备一份面向管理层的企业级 AI 战略规划汇报，我有一个公司的模板 PPT。”*

Skill 会自动进入 **Rhythm A 深度引导流程**：
1. **认知契约与深度探针**：主动澄清核心论题、受众立场偏好、认知差与终局行动目标；
2. **模板解构与规范学习**：接收并解析您的模板，提炼色彩与版式规范；
3. **蓝图编排与质量审计**：规划每页的图表化元语并执行 10 维内容质量动力学审核；
4. **双模交付**：交付内置演讲备注的 PPTX + 内置认知动力学抽屉的单文件 HTML；
5. **实时协同**：感知您的每一次本地手动调整并持续保持同频！

---

## 🧪 自动化测试验证

运行单元与集成测试套件：
```bash
python3 -m unittest discover -s tests -v
```

---

## 📄 License & 版本演进

- 遵循 **MIT License** 开放许可，详见 [LICENSE](LICENSE)。
- 遵循 [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) 规范，详见 [CHANGELOG.md](CHANGELOG.md)。
