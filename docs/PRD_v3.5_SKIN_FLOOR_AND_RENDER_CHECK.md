# undoPPT v3.5.0 产品需求文档 (PRD)
## 皮囊底线与渲染验证闭环 (Skin Floor & Render Check Loop)

> [English](en/prd/PRD_v3.5_SKIN_FLOOR_AND_RENDER_CHECK.md) | 简体中文

> **后续变化**：R3 的字号地板在 v3.7 收窄（只抬高小于 12pt 的文字，不动标题，短标签不得折行），见 [v3.7 PRD](PRD_v3.7_FLESH_PROVENANCE_AND_INGEST.md)。§6 中 v3.8 计划的"Keynote"验证未能达成，见 [v3.8 PRD](PRD_v3.8_SKIN_AND_POISE.md)。

---

## 1. 文档基本信息 (Document Metadata)

* **产品名称**：undoPPT (演示文稿智能解构与重构超级智能体)
* **版本号**：v3.5.0
* **编写日期**：2026-10-06
* **状态**：正式发布 / 生产实施
* **核心目标**：
  1. 先让成品**不出错**：标题不折行压内容、卡片不留空洞、文字可读、HTML 窄屏不裁切；
  2. 让引擎**能自己发现错**：新增静态版面 lint 与真实渲染检查，把"审计 94 分但打开是坏的"这类问题纳入质量闭环；
  3. 兑现"零依赖、双击即用"：HTML 去除 CDN 依赖；
  4. 100% 向后兼容：不改变任何既有 blueprint 字段，仅新增别名与可选行为。

---

## 2. 背景与问题剖析 (Background)

产品的设计哲学把 PPT 拆成四层：**骨架**（主题与提纲）、**血肉**（内容）、**皮囊**（样式）、**身姿**（动画）。v3.4 把大量工作放在骨架与血肉上，但对皮囊没有任何验证手段：审计器只读蓝图 JSON，看不到渲染结果。

v3.5 立项前，在 PowerPoint 与 Chrome 中渲染 v3.4 的 demo，发现：

| # | 现象 | 根因 |
|---|---|---|
| 1 | 8 页中 5 页标题折成两行，压住下方卡片，副标题被卡片遮挡 | 标题固定 34pt，页眉文本框高度写死，内容区起点写死 |
| 2 | 卡片大片留白；HTML 里卡片被撑满整页 | PPTX 卡片高度与内容量无关；HTML 内容区 `flex-1` 拉伸 |
| 3 | 决策收尾页 64% 的字小于 11pt，成熟度阶梯 61%，2x2 矩阵 50% | 各渲染器各自硬编码小字号 |
| 4 | 高卡片呈胶囊形 | python-pptx 默认圆角为短边的 1/6 |
| 5 | QBR / OKR / 人头评审的 PPT 出现空白页 | 规划器输出 `kpi_dashboard`，两个构建器均无此图元，静默回退到空的 bento |
| 6 | 图表是 PowerPoint 默认的蓝红绿 | 未按主题着色 |
| 7 | 字体名写成 `"PingFang SC, Inter, sans-serif"` | PowerPoint 无法解析 CSS 字体栈 |
| 8 | HTML 离线时无样式 | 依赖 `cdn.tailwindcss.com` 与 Google Fonts，与"零依赖"承诺不符 |
| 9 | 窄屏下 HTML 内容被裁 | 画布比例固定、内部字号不缩放 |

---

## 3. 需求 (Requirements)

### 3.1 内容自适应版面 (`core/layout_fit.py`)
- **R1 标题适配**：标题在 [22pt, token 字号] 内缩小到单行；仍放不下则折行，并从页面上移除副标题（副标题保留在备注/HTML），绝不压住内容。
- **R2 圆角**：使用 token `card_style.border_radius`，不再使用默认比例。
- **R3 字号地板**：任何文本框中小于 12pt 的文字，整体放大（上限 1.4 倍）；若估算高度超出所在卡片则回退。椭圆等异形框不参与。
- **R4 卡片适配**：卡片收缩到文字高度（同行等高）；文字过稀时先放大（上限 1.3 倍）。覆盖"文字框叠在卡片上"与"文字在卡片内部"两种结构。
- **R5 垂直居中**：内容块在页眉下方的剩余空间里居中（位移上限 1.3 英寸）。
- **R6 字体**：字体栈取首个字体名，同时写入 latin 与 east-asian。
- **R7 图表**：系列色取自调色板；浅色网格线；类目×系列 ≤ 16 时显示数据标签；表格字号随行数自适应。

### 3.2 渲染验证 (`cli.py render-check`)
- **R8 静态 lint**（无需渲染器）：`OUT_OF_BOUNDS`、`TITLE_WRAPS`、`TEXT_OVERFLOW`、`TEXT_CROSSES_SHAPE`、`TEXT_OVERLAP`。对 v3.4 的 demo 报 19 条，对 v3.5 报 0 条。
- **R9 真实渲染**（`--render`）：PPTX 经 PowerPoint (macOS) 或 LibreOffice 转 PDF 再转 PNG，检查空白带 `BLANK_BAND`（阈值 35%）；HTML 经无头 Chrome 在 1600×900 与 500×900 下读取内容越界量。
- **R10** `build` 自动运行静态 lint 并打印非致命警告。
- **R11** 无渲染器时降级为仅静态 lint，不报错。

### 3.3 HTML
- **R12 离线**：内联 Tailwind 运行时（`core/vendor/`，MIT），移除 Google Fonts 导入。
- **R13 固定画布**：1340×754 画布按视口等比缩放。
- **R14 密度适配**：正文区放大至多 1.4 倍以利用页眉下的剩余高度，超出则回退。
- **R15** `?slide=N` 深链接；`?static=1` 冻结动画并回报版面（供检查器使用）。

### 3.4 缺陷修复
- **R16** `kpi_dashboard` 作为 `metric_spotlight` 的别名；未知 `layout_type` 发出警告而非静默回退。
- **R17** 版本号、文档、预设引用对齐；`output/` 产物不再提交。

---

## 4. 验收标准 (Acceptance Criteria)

| 标准 | 结果 |
|---|---|
| 全部测试通过 | 44 项（原 23 + 新增 21） |
| demo：PPTX 静态 lint | 0 条（v3.4 为 19 条） |
| demo：PowerPoint 真实渲染 | 8 页标题全部单行、无重叠 |
| 12 个企业场景各生成一套 PPTX | 静态 lint 共 0 条；PowerPoint 渲染空白带均 ≤ 35% |
| 小于 11pt 的文字占比（12 场景合计） | < 8%（v3.4 决策页为 64%） |
| HTML：断网可用 | 无任何外部 `src` / `href` / `@import` |
| HTML：桌面与 500px 窄屏 | 8 页均无越界 |
| 反向验证 | 构造的过载页能被 lint 与 HTML 检查同时报出 |

---

## 5. 范围外与已知限制 (Out of Scope & Known Limits)

- 文字测量是启发式（中文 1 em，西文约 0.55 em），真实渲染才是最终依据。
- 内容本身过稀的页面（只有三行短标题）会触发 `BLANK_BAND`，这是**内容问题**而非版面问题，由 v3.6 的 `EVIDENCE_BUDGET` 处理。
- 规划器把"内部技术分享"类提示误判为 `general_informative`，留待 v3.6。
- 动画与审美精修不在本版范围，留待 v3.8。

---

## 6. 后续路线图 (Roadmap)

| 版本 | 主题 | 要点 |
|---|---|---|
| v3.6.0 | 骨架 | 分场景追问清单；12 个场景的优秀提纲样例；`EVIDENCE_BUDGET` 血肉预检；规划器降级为兜底与审查 |
| v3.7.0 | 血肉 | blueprint 新增可选 `source` / `status`；无出处数字标"待核"；`cli.py ingest`；demo 改为展示决策闭环 |
| v3.8.0 | 皮囊精修与身姿 | 字体层级与对比度规范；真实企业模板试跑；三种叙事动画并在 PowerPoint / Keynote 实测 |
