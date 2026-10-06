# undoPPT CLI 命令参考手册

> [English](../en/cli_reference.md) | 简体中文

本手册说明 `undoPPT` 超级 Skill 与自动化引擎的统一命令行接口 `cli.py`（v3.8.0）。

---

## 命令总览

```bash
python3 cli.py <command> [arguments...]
```

### 可用子命令

| 命令 | 用途 | 主要输入 | 交付物 |
| :--- | :--- | :--- | :--- |
| `plan` | 自主认知规划，生成蓝图 | 提示词、参考文档 | `.undoppt/blueprint.json` |
| `generate` | 一键端到端生成演示文稿 | 提示词、文档、模板 | `presentation.pptx`、`presentation.html` |
| `audit` | 结构与语义因果质量审计 | 蓝图、设计令牌 | 审计分数报告与诊断发现 |
| `undo` | 模板母版解构与令牌抽取 | 企业 `.pptx` | `.undoppt/design_tokens.json`、素材 |
| `build` | 双端矢量演示文稿渲染 | 蓝图、设计令牌 | `presentation.pptx`、`presentation.html` |
| `sync` | 检测演讲者在外部的手动修改 | 目标 `.pptx` | 语义 AST 差异摘要 |
| `ingest` | 从文档中抽取带出处的数据点 | `.md` / `.txt` / `.csv` | `.undoppt/facts.json` |
| `cite` | 把蓝图里的数字链接到抽取的事实并记录出处 | 蓝图、facts JSON | 带 `source` 字段的蓝图 |
| `probe` | 动笔前检查请求的信息是否足够 | 提示词、可选参考文档 | 就绪度、缺失事实、该问的问题 |
| `render-check` | 验证已构建交付物的版面 | `.pptx`、`.html` | 发现报告、渲染出的 PNG |
| `demo` | 运行完整的示范流水线 | *无* | 完整且经过审计的示范演示文稿 |

---

## 1. `plan`（自主认知规划器）

分析用户意图，把请求归入 12 个企业场景之一（或某个通用原型），从外部参考文档中抽取事实实体，生成经过审计的 `blueprint.json`。

```bash
python3 cli.py plan --prompt "<goal>" [options]
```

> 这是**兜底作者**（v3.6）：一个没有自己洞察的规则引擎。推荐的做法是由 Agent 运行 `probe`、问清缺失的信息，再根据用户的真实材料写蓝图（见 [Agent 集成指南](agent_integration.md)）。规划器写出的数字是编造的模板，会在成品里显示为"待核"。请求过于单薄时，它会打印就绪度提示（不会中止）。

### 参数

| 参数 | 必填 | 默认值 | 说明 |
| :--- | :---: | :--- | :--- |
| `--prompt` | **是** | — | 演示文稿的核心目标、主题或叙事指令。 |
| `--input-doc` | 否 | `None` | 用于事实依据的 Markdown 或文本文档路径（`.md`、`.txt`）。 |
| `--context` | 否 | `None` | 额外的受众背景、时间限制或风格约束。 |
| `--out` | 否 | `.undoppt/blueprint.json` | 生成的蓝图 JSON 的保存路径。 |

### 示例

```bash
python3 cli.py plan \
  --prompt "Enterprise Cloud Migration & Zero Trust Roadmap" \
  --input-doc internal_migration_brief.md \
  --out .undoppt/blueprint.json
```

---

## 2. `generate`（一键自主流水线）

一次调用完成整条端到端流水线：
1. 解构用户模板（若提供），否则加载预设令牌；
2. 摄取参考文档中的事实；
3. 合成结构化的认知蓝图；
4. 审计蓝图，分数低于 85 时触发自我修正；
5. 渲染带演讲备注的原生矢量 PPTX 与单文件 HTML；
6. 初始化同步基线。

```bash
python3 cli.py generate --prompt "<goal>" [options]
```

### 参数

| 参数 | 必填 | 默认值 | 说明 |
| :--- | :---: | :--- | :--- |
| `--prompt` | **是** | — | 用户提示词 / 演示目标。 |
| `--input-doc` | 否 | `None` | 用于事实依据的外部参考文档路径。 |
| `--context` | 否 | `None` | 额外约束或备注。 |
| `--template` | 否 | `None` | 可选的企业 PowerPoint 模板（`.pptx`）路径，用于解构。 |
| `--tokens` | 否 | `presets/modern_bento.json` | 未提供模板时的备用设计令牌 JSON 路径。 |
| `--format` | 否 | `all` | 输出格式：`pptx`、`html` 或 `all`。 |
| `--transition` | 否 | `fade` | 切页效果：`fade`、`push`、`wipe` 或 `none`。 |
| `--motion` | 否 | `off` | `narrative` 开启叙事动画（见 `build`）。 |
| `--out` | 否 | `output` | 交付物保存目录。 |

### 示例

```bash
python3 cli.py generate \
  --prompt "Series B Pitch Deck for Autonomous AI Agents" \
  --input-doc investor_deck_notes.md \
  --template templates/company_branding.pptx \
  --format all \
  --out output/
```

---

## 3. `audit`（认知质量与因果审计器）

对演示蓝图做严格、客观的质量检查：结构预算是否合规、叙事弧线、因果修辞转折、核心主旨向心度，以及实证权重。

```bash
python3 cli.py audit --blueprint <blueprint.json> [options]
```

### 参数

| 参数 | 必填 | 默认值 | 说明 |
| :--- | :---: | :--- | :--- |
| `--blueprint` | **是** | — | 要检查的蓝图 JSON 路径。 |
| `--tokens` | 否 | `presets/modern_bento.json` | 用于密度预算校验的设计令牌路径。 |

### 审计码

每个码的含义与改法的完整清单见[审计码速查](audit_codes.md)。v3.1 之后新增的：

| 码 | 起始版本 | 含义 |
| :--- | :--- | :--- |
| `DECISION_ASK_MISSING`、`BENCHMARK_UNBALANCED`、`PROMOTION_LAUNDRY_LIST` | v3.4 | 企业严谨性规则（见[场景避坑红线](scenario_anti_patterns.md)）。 |
| `THIN_CONTENT_P<n>` | v3.6 | 页面正文比其版式所需的更短。 |
| `EVIDENCE_BUDGET_P<n>` | v3.6 | 指标页里带数值的指标不足一半。 |
| `UNSOURCED_FIGURES_P<n>` | v3.7 | 没有任何 `source` 覆盖的数字。 |
| `EVIDENCE_TODO_P<n>` | v3.7 | 标为 `status: "todo"` 的数字。 |
| `EVIDENCE_ESTIMATE_P<n>`、`EVIDENCE_ILLUSTRATIVE_P<n>` | v3.7 | 提示：该页被标注为"估算"/"示例数据"。 |

套话告警带有 `suggestion`，给出具体改写。输出里有一行 `Figures:`（总数 / 无出处 / 占位 / 估算 / 示例）。版面与对比度问题不属于蓝图发现：它们来自 `render-check`，以及 `build` 打印的 lint。

### 示例

```bash
python3 cli.py audit --blueprint .undoppt/blueprint.json
```

### 输出示例

```text
================================================================
 COGNITIVE & NARRATIVE DYNAMICS QUALITY AUDIT REPORT
================================================================
 Overall Score:    94.5/100 (Grade: EXCELLENT)
 Structural Score: 95.0/100
 Semantic Score:   94.0/100

 [Detailed Sub-Scores]
   • Causal Cohesion:    95.0/100
   • Thesis Alignment:   92.5/100
   • Empirical Evidence: 95.0/100
   • Objection Resolv:   93.5/100

 [Structural Redlines]
   [✓] 6 slides inspected across 6 layout primitives.
   [✓] Zero passive titles detected. All slides use action-first conclusions.
   [✓] All slides conform to content budget constraints.

 [Deliverable Status]
   Status: APPROVED FOR RENDERING
================================================================
```

---

## 4. `undo`（模板母版解构器）

把一份 PowerPoint 模板解构为设计令牌。自 v3.8 起，它读取模板的**真实主题**：配色方案（`ppt/theme/theme1.xml`）、母版的颜色映射与背景（解析 `schemeClr` 及 `lumMod` / `lumOff`）、以及主题字体（主标题字体、正文字体和东亚字体）。配色、明暗模式与字体都来自这里；输出里的 `theme_source` 记录了读到了什么。

v3.8 之前，`undo` 只扫描幻灯片上显式写死的 RGB 填充，而真实模板里没有这些，所以每份模板（即使是深色的）都返回同一个浅蓝主题。现在抽取出的令牌会经过设计检查（对比度、最小字号），所做的修正列在 `design_notes` 里。品牌色（`palette.primary`）从不被改写；页边距会被限制到构建器网格可用的范围。幻灯片几何信息与嵌入的素材也会一并抽取。

构建器始终绘制 16:9 的页面：4:3 的模板只贡献它的配色与字体，不贡献它的宽高比。

```bash
python3 cli.py undo --template <template.pptx> [options]
```

### 参数

| 参数 | 必填 | 默认值 | 说明 |
| :--- | :---: | :--- | :--- |
| `--template` | **是** | — | 输入的 `.pptx` 模板文件路径。 |
| `--out` | 否 | `.undoppt/design_tokens.json` | 抽取出的令牌保存路径。 |

### 示例

```bash
python3 cli.py undo \
  --template corporate_theme.pptx \
  --out .undoppt/design_tokens.json
```

---

## 5. `build`（双端矢量演示文稿构建器）

根据已校验的蓝图与设计令牌渲染演示文稿。输出 100% 原生矢量的 PowerPoint 形状、规整表格、矢量图表与演讲备注，同时生成单文件的独立 HTML 演示文稿。

```bash
python3 cli.py build --blueprint <blueprint.json> [options]
```

### 参数

| 参数 | 必填 | 默认值 | 说明 |
| :--- | :---: | :--- | :--- |
| `--blueprint` | **是** | — | 已校验的蓝图 JSON 路径。 |
| `--tokens` | 否 | `presets/modern_bento.json` | 设计令牌或模板令牌 JSON。 |
| `--format` | 否 | `all` | 输出格式：`pptx`、`html` 或 `all`。 |
| `--transition` | 否 | `fade` | 切页效果：`fade`、`push`、`wipe` 或 `none`。 |
| `--out` | 否 | `output` | 输出目录。 |
| `--motion` | 否 | `off` | `narrative` 开启三种叙事动画（见下）。 |
| `--final` | 否 | 关 | 交付模式（v3.7）：仍有数字没有出处时拒绝构建。 |

### 叙事动画（v3.8）

动画**默认关闭**。`--motion narrative`（或 `presentation_config.motion: "narrative"`）会按版式给每页配上合适的动画；单页可以用 `motion: {"type": "reveal" | "contrast" | "build" | "none"}` 自行选择。

| 类型 | 一次点击是…… | 适用于 |
| :--- | :--- | :--- |
| `reveal` | 下一个观点，按阅读顺序 | 清单、路线图（节点与卡片同步）、架构栈（自下而上）、决策页 |
| `contrast` | 先出现备选，再出现推荐 | 带 `highlight` 的卡片、2x2 矩阵、现状→目标映射 |
| `build` | 下一块数据 | KPI 卡片（划入）、先图表后结论 |

时序树严格按 PowerPoint 自己的写法生成（每次点击是一个外层步骤，带 `delay="indefinite"`；首个效果为 `clickEffect`，其余为 `withEffect`）。`render-check --render` 会问 PowerPoint 它识别了多少个动画对象，不一致就报 `MOTION_NOT_RECOGNIZED` / `MOTION_INVALID`。v3.3–v3.7 写入的时序树，PowerPoint 完全不识别（动画对象数为 0）；`motion_pace: "staged"` 保留为 `narrative` 的别名。在 HTML 中，数字跑表和流光脉冲属于装饰性效果，只在叙事模式下运行；`S` 键分步模式始终可用。Keynote 无法通过脚本验证：它不向自动化暴露"构建"。

### 示例

```bash
python3 cli.py build \
  --blueprint .undoppt/blueprint.json \
  --tokens .undoppt/design_tokens.json \
  --format all \
  --out output
```

---

## 6. `sync`（协作监视器与差异检查器）

把当前交付文件与记录的 SHA-256 基线指纹比对。如果发生了手动修改（例如在 PowerPoint 里改了文字），它会做 AST 检查并报告变化。

```bash
python3 cli.py sync [options]
```

### 参数

| 参数 | 必填 | 默认值 | 说明 |
| :--- | :---: | :--- | :--- |
| `--target` | 否 | `output/presentation.pptx` | 要检查的演示文稿文件。 |

### 示例

```bash
python3 cli.py sync --target output/presentation.pptx
```

---

## 7. `ingest` 与 `cite`（数据出处，v3.7）

`ingest` 把源文档里的每一个数字抽取出来并保留它的来源；`cite` 把这些来源写进蓝图。

```bash
python3 cli.py ingest --input-doc notes.md --out .undoppt/facts.json
python3 cli.py cite --blueprint .undoppt/blueprint.json --facts .undoppt/facts.json
```

每条事实形如：`{"label": "营收", "value": "1.2亿", "context": "...", "section": "立项", "source": "notes.md:L3"}`。Markdown 与文本给出 `文件:L<行号>`；CSV 给出 `文件:第<行>行·<列名>`，并会使用表头里的单位，例如 `数值(万元)` 加 `1200` 变成 `1200万元`。Excel 会被拒绝：请先把工作表导出为 CSV。

`cite` 按数值把蓝图里的数字匹配到事实。页面级的 `source` 覆盖该页的**所有**数字，所以只有**该页每一个没有出处的数字都匹配到了**才会写入；部分匹配时改为写 `source_candidates`，数字仍然保持待核。`cite` 从不设置 `status`：匹配只说明这个数字出现在文档里，不说明它支撑的是同一个论断。

`build --final` 是交付模式：只要有数字没有出处或是 `todo`，就拒绝构建（退出码 1），并隐藏"待核"徽标。普通的 `build` 保留徽标，让草稿显示出还缺哪些数据。

---

## 8. `probe`（认知契约就绪度，v3.6）

审计只给蓝图的结构打分，分不清"用真材料做的"和"凭空做的"：一个像"帮我做一份关于 AI 的汇报"这么单薄的请求，照样能拿 90 多分。`probe` 在动笔**之前**运行，报告还有什么是未知的。

它先给场景分类（12 个企业场景之一或某个通用原型），然后检查四个通用槽位（Q1 主旨、Q2 受众、Q3 认知差、Q4 决策）加上三到四个场景专属事实（QBR 要有偏差，RFC 要有回滚方案，故障复盘要有时间线）。Q2 与 Q4 是**阻塞项**：不知道谁来拍板、要拍板什么，就不要生成。

```bash
python3 cli.py probe --prompt "智能客服业务立项答辩，申请首期预算，预期人效提升 40%"
python3 cli.py probe --prompt "..." --input-doc notes.md --json
```

| 参数 | 说明 |
| :--- | :--- |
| `--prompt` | 用户的请求，原话。 |
| `--input-doc` | 参考文档；其文本算作证据。 |
| `--context` | 额外的上下文文本。 |
| `--json` | 机器可读输出（`ready`、`readiness`、`blocking`、`slots`、`questions`）。 |

当至少 70% 的槽位已知、且没有阻塞项缺失时，`ready` 为真。`questions` 列出该问什么，阻塞项在前。这个检查是启发式的：它检测一个事实是否被**提及**，不判断它是否**正确**。完备度低时，`plan` 与 `generate` 也会打印同样的提示，但不会中止。

---

## 9. `render-check`（版面验证，v3.5）

审计给蓝图打分，看不到渲染出来的结果。`render-check` 分两层补上这个缺口：

1. **静态 lint**（始终运行，不需要渲染器）：用文字去量它所在的容器，报告查看者会看到的缺陷。
2. **真实渲染**（`--render`）：PPTX 通过 PowerPoint（macOS，AppleScript）或 LibreOffice 渲染，转成 PNG 后检查空白带；HTML 通过无头 Chrome 在 1600x900 与 500x900 下渲染，读回内容超出画布多少。

`build` 已经会运行静态 lint 并打印非致命的警告。

```bash
python3 cli.py render-check --pptx output/presentation.pptx
python3 cli.py render-check --pptx output/presentation.pptx --html output/presentation.html --render
```

### 参数

| 参数 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `--pptx` | — | 要 lint 的 PPTX（加 `--render` 时也会渲染）。 |
| `--html` | — | 要检查的 HTML。需要 `--render` 与 Chrome。 |
| `--render` | 关 | 同时用 PowerPoint/LibreOffice 与无头 Chrome 渲染。 |
| `--engine` | 自动 | `powerpoint` 或 `libreoffice`。 |
| `--slides` | 0 | 未给 `--pptx` 时，HTML 检查所用的页数。 |
| `--out` | `.undoppt/render` | 渲染出的 PNG 的保存目录。 |
| `--json` | — | 把完整报告写入该文件。 |

只要报告了任何发现，退出码为 `1`，否则为 `0`。

### 发现码

| 码 | 含义 |
| :--- | :--- |
| `OUT_OF_BOUNDS` | 有形状超出了页面边缘。 |
| `TITLE_WRAPS` | 标题即使缩到最小字号（22pt）也需要多于一行。请缩短它。 |
| `TEXT_OVERFLOW` | 估算文字比容纳它的卡片更高。删减文字或拆页。 |
| `TEXT_CROSSES_SHAPE` | 一段文字跨在另一个形状的边缘上。 |
| `TEXT_OVERLAP` | 两段文字重叠。 |
| `BLANK_BAND` | 页面高度超过 35% 是一整条空白横带（这一页的内容太少）。 |
| `HTML_OVERFLOW_BOTTOM` / `HTML_OVERFLOW_RIGHT` | HTML 内容超出了 1340x754 的画布。 |
| `HTML_NO_REPORT` | 页面在静态模式下没有回报它的版面（页面加载失败）。 |
| `LOW_CONTRAST` | （v3.8）文字颜色与其背后的填充太接近：低于 4.5:1，或（18pt 及以上、14pt 粗体及以上的文字）低于 3:1。版式阶段通常会修复这类问题，所以在这里出现，说明有一种颜色它没能修到达标。 |
| `MOTION_INVALID` | （v3.8）动画树格式有误：某个点击步骤不等待点击、某个效果指向不存在的形状、id 重复。 |
| `MOTION_NOT_RECOGNIZED` | （v3.8）文件里有 N 个形状带动画，但 PowerPoint 识别出的更少。需要在装有 PowerPoint 的机器上用 `--render`。 |

### `--render` 的准备

```bash
pip install -r requirements-dev.txt     # pypdfium2 + pillow（PDF 转 PNG）、pytest
```

PowerPoint 是沙盒应用，只能写入用户授权过的文件夹，所以检查器会把文件暂存到 `~/Documents/.undoppt_render`，用完即删。第一次运行时可能会请求文件夹访问权限。没有 PowerPoint 或 LibreOffice 时，会跳过 PPTX 渲染，静态 lint 仍会运行。

---

## 10. `demo`（示范流水线）

用内置蓝图构建一份示范文稿：审计、带演讲备注的原生矢量 PPTX、独立 HTML、同步基线。这份文稿有 8 页，用到 15 种版式中的 8 种（封面、Bento 卡片、架构栈、KPI 看板、图表、表格、时间轴、总结），以决策页收尾，审计得分 100/100。其中的数字是为展示版式而编造的，所以标注为 `illustrative`，页脚显示"示例数据"。输出写入 `output/`（已被 git 忽略）。

```bash
python3 cli.py demo
```
