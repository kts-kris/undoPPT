# AI Agent 集成指南

> [English](../en/agent_integration.md) | 简体中文

本指南说明如何在主流 AI Agent 中集成并编排 `undoPPT`，包括 **Cursor、Claude Code、OpenAI Codex、Windsurf、Trae、腾讯 WorkBuddy、Google Antigravity 与 OpenCode**。

---

## 1. 在各 Agent 环境中安装

### 1.1 通用 NPX 安装器
如果你的环境支持 `npx skills`：
```bash
npx skills add https://github.com/kts-kris/undoPPT --skill undo-ppt
```

### 1.2 按 Agent 平台手动克隆

| AI Agent | 推荐的 Skill 目录 | 发现方式 |
| :--- | :--- | :--- |
| **Cursor** | `~/.cursor/skills/undo-ppt` 或项目内 `.agents/skills/undo-ppt` | 自动从工作区发现 |
| **Claude Code** | `~/.claude/skills/undo-ppt` | 内置 Skill 加载 |
| **OpenAI Codex / CLI** | `~/.codex/skills/undo-ppt` | 通过环境路径发现 |
| **Windsurf / Trae** | 仓库根目录下的 `.agents/skills/undo-ppt/` | 工作区级 Skill 索引 |
| **腾讯 WorkBuddy** | 企业 Agent Skill 商店或自定义工具目录 | 工作区 Skill 导入 |
| **Google Antigravity** | `~/.gemini/config/skills/undo-ppt` 或 `.agents/skills/undo-ppt` | 全局/工作区双重检测 |
| **OpenCode** | 根目录的 `SKILL.md` | 直接读取仓库上下文 |

---

## 2. 运行节奏

`undoPPT` 按演示文稿的复杂度与紧迫度，支持两种运行节奏：

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 节奏 A：深度引导 SOP（高风险演示的默认节奏）                                │
│                                                                             │
│ 0. 就绪探针 (probe)               ➔  信息不足：先问，不生成                │
│ 1. 认知契约探针 (Q1-Q4)           ➔  澄清主旨、受众与目标                  │
│ 2. 模板解构 (undo)                ➔  读取模板的真实主题                    │
│ 3. 蓝图编排、出处与审计           ➔  编排 15 图元 JSON；ingest / cite      │
│                                      补出处；审计                          │
│ 4. 双端渲染                       ➔  先出草稿，交付时用 --final            │
│ 4.5 渲染检查                      ➔  在 PowerPoint 与 Chrome 里验证        │
│ 5. 逐轮同步追踪                   ➔  感知人在外部做的修改                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 节奏 B：快速直出（用于即时草稿与低风险需求）                                │
│                                                                             │
│ 1. 自主一键 CLI                   ➔  cli.py generate --prompt "..."        │
│ 2. 自动自我修正循环               ➔  自主审计与自动补丁                    │
│ 3. 即时双端交付                   ➔  45 秒内就绪                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **节奏 B 是兜底。** 一键规划器是没有自己洞察的规则引擎：对一个像"做一份关于 AI 的 PPT"这么空的请求，它照样返回 90 多分的审计成绩。它写的数字是编造的模板（在成品里会显示为"待核"）。把它用在快速草稿，或没有 Agent 可用的时候，并告诉用户哪些数字是占位。

---

## 3. 节奏 A：分步 SOP

### 步骤 0：就绪探针（v3.6）
**信息不足，就不生成。** 对用户的请求原话运行探针：
```bash
python3 cli.py probe --prompt "<用户的请求>" [--input-doc notes.md] --json
```
它会给场景分类，报告哪些契约槽位与场景事实仍然未知，并返回该问的问题，阻塞项在前（受众与决策）。如果 `ready` 为 false，先问其中的 2～3 个，每个附上例子，再动笔。12 个场景以及每页需要什么，见[场景提纲样例](scenario_outlines.md)。

### 步骤 1：认知契约探针
Agent 应当像资深管理咨询顾问一样行事。不要问泛泛的问题，而要问有针对性的认知探针：
1. **核心主旨 (Q1)**：*"抛开所有次要细节，您想传达的那一个中心论点或结论是什么？"*
2. **受众立场 (Q2)**：*"主要受众是谁（比如董事会、工程负责人、学员），他们在防范什么风险，默认立场是什么？"*
3. **认知差 (Q3)**：*"受众已经知道什么（基线），又有哪些关键的盲区或痛点必须点亮（认知差）？"*
4. **终局行动 (Q4)**：*"演示结束后，受众应当当场批准或执行的具体决定或动作是什么？"*

### 步骤 2：母版解构（可选）
如果用户提供了企业 PowerPoint 模板：
```bash
python3 cli.py undo --template /path/to/template.pptx --out .undoppt/design_tokens.json
```
没有模板时，默认用 `presets/modern_bento.json`。

`undo`（v3.8）读取模板的**真实主题**：配色方案、母版背景，以及字体（包括东亚字体）；深色模板会被识别为深色，品牌色会被保留。它不做的事：不会把模板的母版版式、背景图或 logo 放到生成的页面上，也不输出 4:3。请把这一点告诉用户，不要承诺"完整继承母版"。见[设计系统](design_system.md)。

### 步骤 3：蓝图编排与审计
Agent 按[蓝图规格书](blueprint_specification.md)编写 `.undoppt/blueprint.json`，把每一页映射到 15 种图元之一。

**给每个数字一个出处（v3.7）。** 如果用户提供了文档或表格，就抽取其中的数字及其出处，并链接进蓝图；绝不编造数字，占位的数字标 `status: "todo"`：
```bash
python3 cli.py ingest --input-doc notes.md --out .undoppt/facts.json     # .md / .txt / .csv
python3 cli.py cite --blueprint .undoppt/blueprint.json --facts .undoppt/facts.json
```

然后 Agent 触发质量审计器：
```bash
python3 cli.py audit --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json
```
总分低于 85 时，Agent 把标题改成行动先行的陈述，并加强量化证据。出现 `THIN_CONTENT` 和 `EVIDENCE_BUDGET`，说明内容撑不起版式：回去找材料，而不是调版式。出现 `UNSOURCED_FIGURES` 和 `EVIDENCE_TODO`，说明还有数字需要出处或真实数值。

### 步骤 4：双端渲染
审计通过并确认后：
```bash
python3 cli.py build --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json --format all
```
产出的交付物：
- `output/presentation.pptx`（可编辑的矢量形状、规整表格、矢量图表，以及带出处的演讲备注）；
- `output/presentation.html`（可离线使用的独立单文件 HTML，带 `N` 键认知检视器）。

普通的 `build` 用于草稿：没有出处的数字会带一个琥珀色的"待核"徽标，这是"还有事没做完"的诚实标记。要交付，请用 `--final`：只要有数字没有出处或是占位，它就拒绝构建，并隐藏徽标。

**动画默认关闭。** 只有现场演讲的文稿才加 `--motion narrative`（类型：`reveal`、`contrast`、`build`；见 [CLI 手册](cli_reference.md)）。给人阅读的文稿不应有动画。Keynote 的播放效果未经验证。

### 步骤 4.5：验证构建结果（v3.5、v3.8）
审计看的是蓝图，不是成品。要检查交付物：
```bash
python3 cli.py render-check --pptx output/presentation.pptx --html output/presentation.html --render
```
它会在 PowerPoint 与 Chrome 里渲染，并报告溢出、折行的标题、空白带、低对比度，以及 PowerPoint 不识别的动画。`build` 已经会运行静态版面 lint 并打印警告。

### 步骤 5：始终同步追踪
在之后每一轮对话开始时，Agent 运行：
```bash
python3 cli.py sync --target output/presentation.pptx
```
如果检测到变化：
> *"我注意到您在 PowerPoint 里改了第 3 页的标题，突出了延迟下降 15%。我已经和您的改动同步了状态。接下来您想怎么处理？"*

---

## 4. 提示词模式

### 触发完整的战略规划
```text
我需要准备一份 6 页的高管汇报，主题是公司的云原生现代化战略。
目标受众：企业架构委员会。
核心主旨：从单体虚拟机迁移到容器化服务网格，可以把基础设施成本降低 40%，同时达到 99.99% 的可用性。
附件是背景简报（architecture_notes.md）和公司 PPT 模板（company_template.pptx）。
请用 undo-ppt 带我走一遍。
```

### 触发快速草稿
```text
用 undo-ppt 为我们的 AI 开发者工具创业公司快速做一份 5 页的路演稿。
包含一张 Bento 对比卡片、一个架构栈、一页 KPI 指标看板和一条时间轴路线图。
同时交付 PPTX 和 HTML。
```

这么单薄的请求，会让 Agent 先运行 `probe`，并在动笔之前问清楚：投资人是谁、要什么、哪些数字是真的。这是预期的行为。如果用户坚持用已有的信息先出一份草稿，Agent 就用标为 `status: "todo"` 的占位数字做一份，并说明哪些页因为缺证据被省掉了。
