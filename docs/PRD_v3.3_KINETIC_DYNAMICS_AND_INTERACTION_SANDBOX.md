# undoPPT v3.3.0 产品需求文档 (PRD)
## 动效全能进化与活动决策沙盒 (Kinetic Dynamics & Interactive Decision Sandbox)

---

## 1. 文档基本信息 (Document Metadata)

* **产品名称**：undoPPT (演示文稿智能解构与重构超级智能体)
* **版本号**：v3.3.0
* **编写日期**：2026-09-17
* **状态**：已批准 / 实施中 (Approved / Implementing)
* **核心目标**：
  1. 动效层面全面看齐 `open-kimi-ppt-skill` 的元素级时序动画编排，并在**图元内生语义动力学**、**双端异构分级渲染**与**叙事口播节拍时钟**三大方向实现代际超越；
  2. 交互机制上彻底突破传统静态画布的限制，打造**现场演播双重视野认知中枢 (Live Presenter HUD)**、**跨任意工具链的毫秒级意图反思飞轮 (Intent Reflection)** 以及 **动态决策推演沙盒 (Active Sandbox)**。

---

## 2. 背景与系统升级动机 (Background & Strategic Rationale)

在 v3.2.0 中，`undoPPT` 成功确立了“场景避坑红线体系”与“原生切页过渡”。但面对高规格商业路演、技术架构答辩与高管战略决策等高价值汇报时，传统的演示文稿仍面临三大核心瓶颈：

```
┌────────────────────────────────────────────────────────┐     ┌────────────────────────────────────────────────────────┐
│            瓶颈一：动效机械割裂，缺乏业务语义          │     │            瓶颈二：现场单向灌输，无法应对发难          │
├────────────────────────────────────────────────────────┤     ├────────────────────────────────────────────────────────┤
│ • 传统 AI 工具需要硬编码每一个小方块的飞入/缩放坐标； │     │ • 现场答辩时，高管/评委一旦打断提问假定参数，静态 PPT │
│ • 动画沦为无聊的美术杂耍，无法反映架构与数据的内在流向│     │   瞬间失去应对力，演讲者只能苍白口头解释；             │
│ • PPTX 动效跨软件极易掉帧错位，HTML 端未释放 Web 潜力 │     │ • 演讲者没有现场智能辅助，缺乏因果连词与质疑应对弹药。 │
└────────────────────────────────────────────────────────┘     └────────────────────────────────────────────────────────┘
```

为了彻底解决上述痛点，`undoPPT v3.3.0` 提出以**“语义动力学（Semantic Dynamics）”**与**“活动决策沙盒（Active Sandbox）”**为核心的双轮驱动升级。

---

## 3. 功能特性清单 (Feature Epics)

| Epic 编号 | 模块分类 | 功能名称 | 优先级 | 简要说明 |
| :--- | :--- | :--- | :--- | :--- |
| **EPIC-01** | **动效架构** | PPTX 原生 OOXML `<p:timing>` 元素步进序列生成 | **P0** | 在 PPTX 中自动构建合规的时间节点树，在 Office/Keynote 中实现原生单击步进进入 |
| **EPIC-02** | **动效架构** | 15 大图元内生语义动力学 (Semantic Dynamics) | **P0** | 架构栈向下扎根、时间轴流光点亮、KPI 跑数(Count-up)、阶梯攀升动效无需 Agent 写坐标 |
| **EPIC-03** | **动效架构** | 叙事弧线感知节拍时钟 (Causal Pacing) | **P1** | 动效延迟与速度自适应 `narrative_arc` (冲突干脆紧迫 250ms，突破光晕扩散，实证平稳跑数) |
| **EPIC-04** | **演播交互** | 现场演播双重视野中枢 (Live Presenter HUD) | **P0** | HTML 单文件按 `P` 键激活现场中枢，包含认知罗盘、因果提词器与评委质疑应对弹药库 |
| **EPIC-05** | **演播交互** | 动态决策推演沙盒 (Active Decision Sandbox) | **P0** | 数据图表与 KPI 支持现场切换“保守/基准/激进”情境并动态重绘，架构层支持点击下钻 |
| **EPIC-06** | **协同交互** | 跨工具链毫秒级意图反思飞轮 (Intent Reflection) | **P1** | `SyncWatcher` 升级语义反思引擎，捕获人类在本地 Office/Keynote 中的微调战略动机 |

---

## 4. 详细功能规约 (Detailed Requirements Specification)

### 4.1 动效架构规约 (Kinetic Dynamics Architecture)

#### 4.1.1 全面看齐与 PPTX OOXML 原生时序生成 (EPIC-01)
* **实现目标**：彻底解决此前 PPTX 仅有切页转场、缺乏页内元素逐个单击展开的问题。
* **技术规范**：
  - 在 `core/pptx_builder.py` 中利用 `parse_xml` 自动构建标准 ECMA-376 `<p:timing>` 树：
    ```xml
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
      <p:tnLst>
        <p:par>
          <p:cTn id="1" dur="indefinite" restart="always" nodeType="tmRoot">
            <p:childTnLst>
              <p:seq concurrent="1" nextAc="seek">
                <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                  <p:childTnLst>
                    <!-- 图元内部组件的按键进入时间节点 -->
                  </p:childTnLst>
                </p:cTn>
                <p:prevCondLst><p:cond evt="onPrev" delay="0"/></p:prevCondLst>
                <p:nextCondLst><p:cond evt="onNext" delay="0"/></p:nextCondLst>
              </p:seq>
            </p:childTnLst>
          </p:cTn>
        </p:par>
      </p:tnLst>
    </p:timing>
    ```
  - 支持将 Bento 卡片、架构栈各层级、时间轴节点自动分配递增的 Shape ID，并关联至 `<p:bldLst>` 或 `<p:anim>` 序列；
  - 在 PowerPoint / WPS / Keynote 放映时，无需安装任何插件，直接按下空格或鼠标左键即可逐个呼出关键组件。

#### 4.1.2 15 大图元内生语义动力学 (EPIC-02)
* **设计原则**：**“结构决定动效，语义赋予重力”**。Agent 零配置，引擎自装配：
  1. **分层架构栈 (`architecture_stack`)**：
     - 底层基础设施（IaaS/数据源）：自下而上重力落锁；
     - 中间层（运行时/调度调度）：左右向中心聚合展开；
     - 顶层业务应用（Gateway/终端）：由上至下聚光点亮。
  2. **时间轴与流程 (`timeline` / `process_flow`)**：
     - 主推进轴线呈现流光粒子脉冲（Flowing Light Beam）；
     - 阶段节点在流光经过时触发波纹（Ripple）并依序点亮，直观展现因果演化。
  3. **核心 KPI 大字报 (`metric_spotlight`)**：
     - HTML 端注入原生 Web 跑表物理引擎（Count-up Physics），数值从 0 丝滑滚动至目标值（如 94.8%），伴随同环比标签的高光锁定。
  4. **成熟度阶梯 (`maturity_ladder`)**：
     - L1 起步期 ➔ L4 成熟期阶梯依次呈现向上攀升的动能势能，高亮成熟度目标层。

#### 4.1.3 叙事弧线与口播节拍时钟 (EPIC-03)
* **动态自适应节奏**：
  - `narrative_arc == "conflict"`：动效时长 200~250ms，采用 `ease-in` 紧凑切入，强化痛点压迫感；
  - `narrative_arc == "breakthrough"`：动效时长 400ms，采用中心径向膨胀与微光流转，烘托方案破局感；
  - `narrative_arc == "evidence"`：动效时长 600ms，配合 KPI 跑数平缓结束，留出充足时间让受众产生信赖；
  - `narrative_arc == "call_to_action"`：收尾行动要点自左向右依次笃定划出，增强决策落地执行感。

---

### 4.2 演播交互与动态决策沙盒 (Interaction & Sandbox Architecture)

#### 4.2.1 现场演播双重视野认知中枢 (EPIC-04: Presenter HUD)
* **触发机制**：在单文件 HTML 演示文稿中，按下键盘 **`P` 键** 或点击控制栏的 **`HUD` 按钮**，即可在画面右侧（或分屏窗口）调出 **“演播动力学中枢”**。
* **中枢核心功能**：
  1. **认知罗盘 (Cognitive Radar)**：
     - 显示当前幻灯片在《认知契约》中的具体位置（Q1 核心主旨向心力、Q3 认知差痛点覆盖率、Q4 终局行动要求）；
     - 警示当前页尚未达成的认知转化目标。
  2. **因果提词器 (Transition Teleprompter)**：
     - 自动提取 `slide.transition`，以显著高亮字号提示演讲者切页前的口播连词（例如：*“【口播提示】请强调：然而现存两大方案在生产高并发下已达天花板...”*）。
  3. **评委质疑应对弹药库 (Objection Playbook)**：
     - 基于 `SemanticAuditor` 的审查结果，自动提炼出当前页可能遭遇的 **2~3 个典型发难质疑（Hard Skepticisms）** 与 **标准权威解题口吻（Smoking Gun Defense）**，让演讲者在答辩时从容应对。

#### 4.2.2 动态决策推演沙盒 (EPIC-05: Active Sandbox)
* **设计哲学**：**从“单向灌输的静态幻灯片”蜕变为“高管现场拍板的推演模拟器”**。
* **三大交互沙盒组件**：
  1. **情景预案动态切换 (Scenario Switcher Tab)**：
     - 在包含 `data_chart` 或 `metric_spotlight` 的页面，顶部自动嵌入轻量情境切换器：`[保守方案 (Conservative)]` | `[基准方案 (Baseline)]` | `[突破方案 (Aggressive)]`；
     - 现场汇报高管提问时，演讲者轻轻一点，柱状图高度、折线趋势与 KPI 关键数字即刻动态重新计算并流畅过渡重绘！
  2. **敏感性参数调节滑块 (Sensitivity Slider)**：
     - 允许在演示界面拖动关键变量（如“研发投入预算 ±30%”、“并发请求 QPS 范围”），现场联动推演 ROI 收益曲线。
  3. **架构层级下钻弹窗 (Architecture Drilldown Modal)**：
     - 在 `architecture_stack` 页面，演讲者点击任何一个中间件或微服务组件，立即弹出该组件的 SLA 指标、调用链上下游、故障域隔离策略与回滚机制。

#### 4.2.3 跨工具链毫秒级意图反思飞轮 (EPIC-06: Intent Reflection)
* **实现机制**：
  - 在 `core/sync_watcher.py` 中增加 `analyze_intent_diff(old_bp, new_bp)` 函数；
  - 当人类在 Office / Keynote / 本地 JSON 中修改了指标数值、删减了图元卡片或修改了标题，SyncWatcher 不仅生成文件级 Diff，更能结构化推导其**战略意图**：
    - 例如：*“检测到人类将 P99 延迟由 20ms 改为 5ms，删除了第三方网关层 ➔ 战略意图反思：人类正在激进化性能指标并追求极简内生自研”*；
  - 该意图反思作为上下文直接注入下一轮 Agent 规划流程，确保 AI 智能体在后续迭代中与人类专家的意志深度并肩。

---

## 5. Blueprint Schema v3.3 规范扩展

在原有 `blueprint.json` 规范基础上扩展以下字段，保持 100% 向后兼容：

```json
{
  "contract": { ... },
  "presentation_config": {
    "transition_effect": "fade | push | wipe | none",
    "motion_pace": "staged | instant",
    "kinetic_style": "semantic_physics | minimal",
    "enable_sandbox": true
  },
  "slides": [
    {
      "layout_type": "metric_spotlight",
      "narrative_arc": "evidence",
      "sandbox": {
        "enabled": true,
        "scenarios": {
          "conservative": { "metrics": [ { "value": "85.2%" } ] },
          "baseline": { "metrics": [ { "value": "94.8%" } ] },
          "aggressive": { "metrics": [ { "value": "99.1%" } ] }
        }
      },
      "hud_notes": {
        "objection_defense": [
          { "skepticism": "如何保障极端高峰下的 SLA 不劣化？", "counter": "依靠第三层工具沙箱的自适应熔断与 8ms 降级旁路。" }
        ]
      }
    }
  ]
}
```

---

## 6. 验收标准与交付物 (Acceptance Criteria)

1. **PPTX 原生步进时序**：导出的 PPTX 在 Microsoft PowerPoint 中全屏播放时，按空格键能够实现组件顺序步进显现；
2. **HTML 演播 HUD**：在单文件 HTML 演示文稿中按下 `P` 键，能够顺畅呼出 Presenter HUD，展示认知罗盘、转折提示词与质疑答辩库；
3. **HTML 动态沙盒**：在包含数据指标的页面，点击保守/基准/激进情境标签，页面数值能够动态流畅刷新；
4. **意图反思分析**：`SyncWatcher.analyze_intent_diff` 能够针对数据与结构变化输出有意义的战略意图分析。
