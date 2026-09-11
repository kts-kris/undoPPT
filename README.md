# undoPPT (演示文稿智能解构与重构超级智能体)

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-purple.svg)]()
[![Antigravity](https://img.shields.io/badge/Antigravity-Super%20Skill-orange.svg)]()

> **“解构母版（Undo）、图表化重构（Redo）、单文件极简交付（Zero-friction Delivery）、时刻与用户并肩（Always-in-Sync）”**

`undoPPT` 是为 Google Antigravity 打造的新一代演示文稿超级 Skill 与自动化工程引擎。彻底终结传统 AI 生成 PPT **“通篇堆字、版面混乱、无法吸收企业母版、生成物不可二次编辑、人机交互单向割裂”** 的核心痛点。

---

## 🌟 四大超级能力 (Super Capabilities)

### 1. 模板智能解构引擎 (Dual-Mode Deconstruction Engine)
- **模式 A（原生母版 AST 解析）**：基于 `python-pptx` 深度遍历 Slide Masters、版式槽位、配色方案、字体阶梯与安全边距，将用户的 PPTX 模板精准提取为强一致性的 `design_tokens.json`，确保输出完全符合用户预期的演示文稿。
- **模式 B（视觉启发式解析）**：针对散装样张或风格参考图，通过视觉启发式规则将色彩配比、阴影、卡片圆角标准化为统一协议。
- **规范绝对穿透**：一旦标准确立，全任务周期不可篡改地统领所有页面的生成排版。

### 2. 六大原生图元组件库 (Infographic Primitives)
拒绝大段无聊文本，内置 6 大工业级图表化组件元语：
- 🏗️ **产品/技术架构堆叠图 (Architecture Stacks)**：分层底板、微服务组件卡片、分类标签。
- 🍱 **Bento 多栏对比卡片 (Bento Grid Cards)**：2/3/4 栏对比、高亮方案框、要点列表。
- 📊 **KPI 核心指标大字报 (Metric Spotlight)**：超大字体数值、同环比标签、下钻说明。
- ⏱️ **横向推进时间轴与里程碑 (Timeline Roadmap)**：节点圆环、连接轴线、阶段交付清单。
- 🎯 **2x2 战略矩阵与象限 (Matrix)**：多维象限分布与业务评估。
- 🏁 **收官要点速览 (Key Takeaways)**：胶囊编号卡片与决策建议。

### 3. 双端极简交付 (Dual-Format Delivery)
- **PowerPoint PPTX**：100% 原生矢量形状与独立文本框，可在 Microsoft PowerPoint / Apple Keynote 中自由二次编辑，**绝不贴图**。
- **单文件自包含 HTML**：将演示文稿打包为单个 `.html` 文件，内置精美排版、键盘导航（←/→/Space/F 全屏）、进度条，**双击即播，零依赖，极度易于分发**。

### 4. 毫秒级双向协同感知 (Always-in-Sync)
- 每一轮对话伊始，优先运行 **Sync Watcher**，在 `<10ms` 内完成 SHA-256 指纹比对。
- 若用户在外部对 PPTX 进行了手动修改（如调整标题、删减节点、微调颜色），智能体自动生成 AST 差异分析，并在回复开始前主动告知用户：“*检测到您在本地修改了第 3 页，已同步更新意图...*”，真正实现人机并肩共创。

---

## 🏗️ 系统拓扑架构

```mermaid
graph TD
    User([用户发起任务 / 提出需求]) --> Guide[1. 意图研判与信息充分性探针 Guide]
    Guide --> Probe{信息是否达到充分标准?}
    Probe -- 否 --> Guide
    Probe -- 是 --> UndoDecision{是否提供企业模板?}
    
    UndoDecision -- 是 --> UndoEngine[2. 模板智能解构引擎 Mode A/B]
    UndoDecision -- 否 --> Presets[2. 匹配内置 4 大工业级设计系统]
    
    UndoEngine --> Tokens[标准设计协议 design_tokens.json]
    Presets --> Tokens
    
    Tokens --> InfoArch[3. 信息架构与图表化蓝图 slides_blueprint.json]
    InfoArch --> Compiler[4. 渲染构建集群]
    
    Compiler --> PPTX[100% 原生矢量 PPTX]
    Compiler --> HTML[单文件自包含 HTML]
    
    PPTX --> Deliverable[(交付物 output/)]
    HTML --> Deliverable
    
    Deliverable --> LocalEdit[用户本地外部编辑]
    LocalEdit --> SyncWatcher[5. 毫秒级指纹比对与 AST Diff]
    SyncWatcher -->|主动向用户同步理解| Guide
```

---

## 📁 目录结构

```text
undoPPT/
├── .agents/skills/undo-ppt/         # Antigravity 工作区 Skill 注册目录
│   └── SKILL.md                    # 超级 Skill 主指令规范与 SOP
├── core/                           # 核心 Python 自动化引擎
│   ├── __init__.py                 # 版本号导出 (1.0.0)
│   ├── undo_engine.py              # PPTX 模板解析解构器 (Mode A)
│   ├── vision_extractor.py         # 视觉启发式解析器 (Mode B)
│   ├── pptx_builder.py             # 100% 原生矢量 PPTX 构建器
│   ├── html_builder.py             # 单文件自包含 HTML 演示编译器
│   └── sync_watcher.py             # 毫秒级指纹追踪与语义 AST 差异对比器
├── presets/                        # 4 大工业级预设设计系统
│   ├── modern_bento.json           # 现代企业 Bento 卡片 (默认)
│   ├── consulting_minimalist.json  # 顶级战略咨询高密度极简
│   ├── tech_keynote.json           # 科技暗黑大屏展演
│   └── enterprise_architecture.json# 架构工程实战容器
├── tests/                          # 自动化单元与回归测试套件
│   └── test_engine.py
├── output/                         # 最终交付物目录
│   ├── presentation.pptx           # 可二次编辑的 PPTX
│   └── presentation.html           # 单文件自包含 HTML
├── .undoppt/                       # 内部元数据缓存 (tokens, blueprint, sync)
├── cli.py                          # 统一命令行交互入口
├── README.md                       # 本说明文档
└── CHANGELOG.md                    # 语义化版本变更记录
```

---

## 🚀 快速上手 (CLI Quickstart)

### 1. 环境依赖
仅需 Python 3.10+ 及 `python-pptx`：
```bash
pip install python-pptx
```

### 2. 一键运行端到端演示 (Demo)
运行内置的企业级 Agentic AI 方案生成演示：
```bash
python3 cli.py demo
```
输出：
- `output/presentation.pptx`：完全可编辑的 6 页矢量幻灯片。
- `output/presentation.html`：双击即可在浏览器全屏播放的动态演示文稿。

### 3. 解析提取用户模板 (Undo)
将任意已有的企业 PPTX 模板解构为标准规范，确保生成结果完全符合模板风格：
```bash
python3 cli.py undo --template /path/to/company_template.pptx --out .undoppt/design_tokens.json
```

### 4. 基于蓝图与规范渲染 (Build)
```bash
python3 cli.py build --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json --format all
```

### 5. 毫秒级协同感知与 Diff 检查 (Sync)
当您在本地用 PowerPoint 或 Keynote 修改了交付物后，检查改动：
```bash
python3 cli.py sync --target output/presentation.pptx
```

---

## 🤖 在 Antigravity 中使用 undoPPT 超级 Skill

本项目已在以下两个层级完成 Skill 自动注册：
1. **工作区层级**：`.agents/skills/undo-ppt/SKILL.md`
2. **全局用户层级**：`~/.gemini/config/skills/undo-ppt/SKILL.md`

在任意对话中，只需自然表达您的 PPT 诉求即可触发：
> *“帮我准备一份面向管理层的企业级 AI 战略规划汇报，我有一个公司的模板 PPT。”*

Skill 会自动进入 **Rhythm A 深度引导流程**：
1. **深度探针**：主动询问核心业务痛点、受众层级，并提醒提供关键数据；
2. **模板解构**：接收您的模板并输出色彩与版面规范；
3. **蓝图确认**：展示每页的图表化元语规划（如哪一页用架构图、哪一页用 KPI 大字报）；
4. **双模交付**：交付 PPTX + 单文件 HTML；
5. **实时同步**：感知您的每一次本地手动调整并持续保持同频！

---

## 🧪 自动化测试验证

运行单元与集成测试套件：
```bash
python3 -m unittest discover -s tests -v
```

---

## 📄 License & 版本演进

- 遵循 **MIT License** 开放许可。
- 遵循 [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) 规范，详见 [CHANGELOG.md](CHANGELOG.md)。
