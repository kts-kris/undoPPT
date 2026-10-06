# undoPPT v3.8.0 产品需求文档 (PRD)
## 皮囊与身姿：读懂真实模板、对比度有保证、动画名副其实 (Skin & Poise)

---

## 1. 文档基本信息 (Document Metadata)

* **产品名称**：undoPPT (演示文稿智能解构与重构超级智能体)
* **版本号**：v3.8.0
* **编写日期**：2026-10-06
* **状态**：正式发布 / 生产实施
* **核心目标**：
  1. 让 `undo` **真正读取模板**的配色、明暗与字体，而不是回落到默认值；
  2. 把**对比度与字号**做成引擎的保证，无论令牌来自预设还是真实模板；
  3. 让动画**真的能被 PowerPoint 识别并播放**，并把动画收敛为三种服务叙事的类型、默认关闭；
  4. 用 PowerPoint 自己作为验证手段，而不是自说自话；
  5. 100% 向后兼容：既有蓝图、令牌文件、`motion_pace: "staged"` 均仍可用。

---

## 2. 背景与问题剖析 (Background)

v3.8 立项前，用真实的 PowerPoint 输出检验 README 的三项承诺，结果都不成立：

| # | 承诺 | 实测 |
|---|---|---|
| 1 | "深度母版逆向解构：提取配色、明暗主题" | 用 PowerPoint 内置的三份 Office 主题（Dark Gradient、Parcel、Editorial，其中一份是深色）做模板，`undo` 对三份返回**完全相同**的令牌：模式 LIGHT、主色 `#1A56DB`、背景 `#F8FAFC` |
| 2 | "原生 `<p:timing>` 点击步进动画" | 让 PowerPoint 报告它识别的动画对象数：v3.4 的 demo 为 **0**；而一份手写的、按 PowerPoint 自己格式写的对照文件为 2/2 |
| 3 | 4 个预设的配色可读 | 渲染成品后，成功绿 `#10B981` 在白底只有 2.54:1；深色预设的决策页使用写死的浅色卡片与浅色文字，几乎不可读；浅主色上的白字只有 2.14:1 |

三项的共同点：**没有人用真实的查看器检验过**。

根因：
1. `undo` 只扫描幻灯片上显式写死的 RGB，真实模板的颜色在 `theme1.xml`、幻灯片是空占位符；
2. 动画 XML 的点击步骤用了 `delay="0"`（应为 `indefinite`），缺 `presetID` / `clickEffect` / `bldLst`；
3. 渲染器里散落约 25 处硬编码颜色，且没有任何对比度检查。

---

## 3. 需求 (Requirements)

### 3.1 真实主题读取 (`core/theme_reader.py`, `core/undo_engine.py`)
- **R1** 读取配色方案（dk1/lt1/dk2/lt2/accent1-6）、母版颜色映射（bg1/tx1/bg2/tx2）、母版背景（`solidFill` 或 `bgRef`，解析 `schemeClr` 及 `lumMod`/`lumOff`/`tint`/`shade`）。
- **R2** 读取主题字体：major/minor 拉丁字体与东亚字体（`ea` 或 `Hans`/`Hant`/`Jpan`）。
- **R3** 令牌来源优先级：主题 > 幻灯片扫描（回退）。`theme_source` 记录读取了什么。
- **R4** 明暗判定基于解析后的真实背景色；品牌主色取 `accent1`，不被改写。
- **R5** 页边距限制在构建器网格可用的范围（≤0.8in）；页眉不依赖模板的页面宽度与大字号。
- **R6** 提取后的令牌经过设计检查，修复记录在 `design_notes`。

### 3.2 对比度与字号 (`core/contrast.py`, `core/design_check.py`, `core/layout_fit.py`)
- **R7** 对比度标准：正文 4.5:1，大字（≥18pt，或 ≥14pt 粗体）3:1。
- **R8** 渲染期修复：按每个文字的**实际背后填充色**检查，不达标则沿原色相向黑/白调整至刚好达标；**不改填充**，品牌色徽标/表头保持原样，其上的文字自动换成白或近黑。
- **R9** 静态 lint 新增 `LOW_CONTRAST`。
- **R10** 令牌校验：文字色对其所在底色；最小字号（标题 28、副标题 16、正文 12、KPI 40）；层级（标题 ≥ 1.5× 正文）。`check_tokens` 报告，`repair_tokens` 修复（不改入参）。
- **R11** `palette.primary` 不作为文字色校验（它主要是填充），由 R8 逐字修复。
- **R12** 渲染器里仍写死的浅色填充改取调色板，使深色预设自洽。
- **R13** 已经很粗的字体（Impact、Haettenschweiler、*Black/Heavy*）不再叠加合成加粗。

### 3.3 叙事动画 (`core/motion.py`)
- **R14** 三种类型：`reveal` 逐条出现、`contrast` 对比先后、`build` 数据递进；**默认关闭**。
- **R15** 开关：`build --motion narrative`、`presentation_config.motion`、单页 `motion: {"type": ...}`；`off` 强制关闭；`motion_pace: "staged"` 与 `{"staged_reveal": true}` 仍作别名。
- **R16** 时序树严格按 PowerPoint 自己的写法：点击步骤外层 `delay="indefinite"`，首个效果 `clickEffect`，同组其余 `withEffect`，含 `presetID`/`presetClass`/`grpId` 与 `bldLst`。
- **R17** 分组规则：按水平**中心线**聚类（路线图的节点与其卡片同步）；箭头、徽标并入所属步骤；页眉、页脚、徽标、连接线不参与动画；单步页面不加动画。
- **R18** 提供 `validate_timing`（结构校验）；`render-check --render` 让 PowerPoint 报告识别的动画对象数，不一致则报 `MOTION_NOT_RECOGNIZED` / `MOTION_INVALID`。
- **R19** HTML 的装饰性效果（进入页面时的数字跑表、流光）仅在叙事模式下运行。

---

## 4. 验收标准 (Acceptance Criteria)

| 标准 | 结果 |
|---|---|
| 全部测试通过 | 144 项通过 + 1 项需 PowerPoint 的集成测试（`UNDOPPT_TEST_POWERPOINT=1`，已通过）。原 105 + 新增 39 |
| `undo` 三份真实主题 | 三份得到三套不同令牌：深色（`#0B0C12`，主色 `#4970FF`）、暖色（`#F2F2F2`，主色 `#F6A21D`）、红色（`#F7F6F3`，主色 `#C8350F`）；v3.7 三份相同 |
| 品牌色 | `palette.primary` 保持模板原值（`#F6A21D` 未被改成棕色） |
| 4 个预设 × demo | `LOW_CONTRAST` 0 条（修复前 2 / 3 / 2 / 6 条）；预设令牌均通过 `check_tokens`（修复了 `enterprise_architecture` 的 4.4995:1） |
| 真实模板令牌 × demo | 静态 lint 0 条；PowerPoint 渲染三种风格各异且可读 |
| 页眉对模板的鲁棒性 | 令牌标题 48pt / 副标题 26pt / 页边距 2.0in 时 lint 仍为 0 |
| 动画：PowerPoint 识别 | demo 逐页识别数与文件内一致（0/6/18/8/2/0/12/9）；12 个企业场景共 72 页全部一致；v3.4 的旧树为 0 |
| 动画：默认 | 未指定时不生成任何时序树；HTML `data-motion="off"` |
| 动画：结构 | 点击步骤 `delay="indefinite"`；首个 `clickEffect`；校验器能抓出 v3.4 的写法 |
| 变异验证 | 把点击步骤改回 `delay="0"` 后 `validate_timing` 报错 |

---

## 5. 范围外与已知限制 (Out of Scope & Known Limits)

- **模板保真度有限。** 配色、明暗、字体会带过来；模板的母版版式、背景图与 logo **不会**放到生成的页面上（构建器自己绘制 16:9 版式），4:3 模板按 16:9 输出。这是下一步最大的差距。
- **"真实模板"是微软内置主题，不是企业模板。** 这台机器上没有企业模板；这些主题带有真实的母版与配色，足以暴露 `undo` 的缺陷，但不能证明对复杂企业母版的表现。
- **Keynote 未验证。** 脚本无法让 Keynote 打开该文件，且 Keynote 不向自动化暴露"构建"。PowerPoint 之外的播放器效果不做承诺。
- **HTML 不跟随深色预设。** HTML 取令牌里的品牌色与字体，但外框与卡片底色固定为浅色。
- 文字测量仍是启发式，真实渲染才是最终依据。

---

## 6. 路线图完成情况 (Roadmap Status)

v3.5（皮囊底线）→ v3.6（骨架）→ v3.7（血肉）→ v3.8（皮囊精修与身姿）四个版本的计划已全部完成。后续值得做的方向，按价值排序：

1. 把模板的母版版式、背景图与 logo 真正带到生成的页面上；
2. HTML 跟随深色预设；
3. 用真实的企业模板做试跑（需要用户提供）；
4. Keynote / WPS 的动画验证。
