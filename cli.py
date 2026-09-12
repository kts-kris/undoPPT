"""cli.py - Unified Command Line Interface for undoPPT Super Skill Engine (v2.6.0).

Usage:
  python3 cli.py plan --prompt "<prompt>" [--input-doc <file.md>] [--context "<notes>"] [--out <blueprint.json>]
  python3 cli.py generate --prompt "<prompt>" [--input-doc <file.md>] [--template <template.pptx>] [--format pptx|html|all] [--out <dir>]
  python3 cli.py undo --template <template.pptx> [--out <tokens.json>]
  python3 cli.py build --blueprint <blueprint.json> [--tokens <tokens.json>] [--format pptx|html|all] [--out <dir>]
  python3 cli.py audit --blueprint <blueprint.json> [--tokens <tokens.json>]
  python3 cli.py sync [--target <file.pptx>]
  python3 cli.py demo
"""

import argparse
import json
import os
import sys

from core.cognitive_planner import CognitivePlanner
from core.content_auditor import ContentAuditor
from core.html_builder import build_standalone_html
from core.pptx_builder import build_presentation
from core.sync_watcher import SyncWatcher
from core.undo_engine import extract_template_tokens, save_tokens


DEMO_BLUEPRINT = {
    "contract": {
        "core_thesis": "从单一认知对话全面迈向自主协同的 Agentic AI 企业级架构演进",
        "audience": {
            "role": "CTO 及技术决策委员会",
            "stance": "关注落地可靠性、改造成本与人机交互确定性"
        },
        "knowledge_delta": {
            "known_baseline": ["传统单轮 LLM 对话无法闭环长程任务", "企业系统异构且复杂度高"],
            "blindspots_and_pains": ["传统被动方案人工介入成本高达 80%", "固定规则 RPA 面对非结构化长尾场景极其脆弱"]
        },
        "target_outcomes": {
            "understand": "多智能体协同运行时的‘交互-调度-工具’三层解耦架构",
            "believe": "标准化 Skill 规范配合双向协同感知能将端到端完成率提升至 94.8%",
            "act": "批准 Q2 试点破局阶段技术预研立项并分配专项研发资源"
        }
    },
    "slides": [
        {
            "layout_type": "cover",
            "narrative_arc": "hook",
            "mission": "确立核心主张，建立架构评审共识与预期成效",
            "category": "ENTERPRISE STRATEGY & ARCHITECTURE 2026",
            "title": "新一代企业级 Agentic AI 业务与架构全景方案",
            "subtitle": "从单一认知对话到多智能体自主协同的工业化演进之路",
            "meta": "undoPPT Super Skill 联合出品 · 架构评审专供"
        },
        {
            "layout_type": "bento_cards",
            "narrative_arc": "conflict",
            "mission": "击穿听众对现有方案的侥幸心理，建立系统性重构的紧迫性",
            "transition": "【冲突】然而现存的两大传统方案，在真实生产环境下均已触碰天花板",
            "action_title": "痛点：传统被动方案与规则 RPA 难以支撑工业级自主闭环",
            "core_evidence": "传统方案人工介入成本高达 80%，而 Agentic 系统综合效率提升 400%+",
            "title": "传统 AI 方案 vs Agentic AI 核心维度对比",
            "subtitle": "打破单点工具局限，迈向具备长程规划与工具调用能力的自主智能体系统",
            "cards": [
                {
                    "tag": "TRADITIONAL LLM",
                    "title": "被动对话型方案",
                    "desc": "以单轮或短程问答为主，缺乏环境感知与外部工具执行能力，无法闭环复杂业务。",
                    "bullets": ["单向文本输出为主", "无状态上下文易丢失", "人工介入成本高达 80%"],
                    "highlight": False
                },
                {
                    "tag": "WORKFLOW RPA",
                    "title": "固定规则编排",
                    "desc": "严格依赖预设硬编码流程，面对不确定性与非结构化长尾场景极其脆弱。",
                    "bullets": ["维护成本高昂", "对突发异常容错率为零", "无法自主学习与演进"],
                    "highlight": False
                },
                {
                    "tag": "AGENTIC SYSTEM",
                    "title": "新一代自主协同集群",
                    "desc": "基于动态意图推理、多子智能体拓扑与沙箱工具链，实现全自主端到端闭环交付。",
                    "bullets": ["动态规划与自我反思", "毫秒级双向感知同步", "综合效率提升 400%+"],
                    "highlight": True
                }
            ]
        },
        {
            "layout_type": "architecture_stack",
            "narrative_arc": "breakthrough",
            "mission": "给出根本解法，证明平台具备高可用、分层解耦与工具沙箱控制力",
            "transition": "【突破】因此，我们必须构建‘交互-中枢-沙箱’三层闭环架构",
            "action_title": "方案：构建高可用、多租户、安全可信赖的智能体全生命周期中枢",
            "core_evidence": "三层架构严格解耦，沙箱隔离保障企业级安全合规",
            "title": "新一代企业级 Agentic AI 平台三层技术架构",
            "subtitle": "构建高可用、多租户、安全可信赖的智能体全生命周期运行时中枢",
            "layers": [
                {
                    "name": "业务交互与场景层",
                    "desc": "统一多模交互与接入",
                    "items": ["协同工作区", "企业微信/飞书", "OpenAPI 网关", "低代码控制台"]
                },
                {
                    "name": "智能体中枢调度层",
                    "desc": "意图与长程规划核心",
                    "items": ["意图研判探针", "模板解析解构引擎", "协同感知哨兵", "质量规约审计员"]
                },
                {
                    "name": "工具底座与沙箱层",
                    "desc": "安全受控执行环境",
                    "items": ["MCP 服务器集群", "Python 代码执行沙箱", "向量知识库", "模型网关"]
                }
            ]
        },
        {
            "layout_type": "metric_spotlight",
            "narrative_arc": "evidence",
            "mission": "用压倒性量化硬核指标击溃疑虑，提供坚不可摧的商业成效背书",
            "transition": "【实证】方案不仅理论自洽，更在全链路可观测指标上实现跨越式突破",
            "action_title": "成效：端到端任务自主完成率突破 94.8%，工时缩减 90%",
            "core_evidence": "94.8% 自主完成率，<8ms 毫秒级感知延迟，45s 极速综合交付",
            "title": "核心效能与业务价值度量指标",
            "subtitle": "全链路数据可观测性与工业级商业成效交付衡量",
            "metrics": [
                {
                    "label": "端到端自动化完成率",
                    "value": "94.8%",
                    "delta": "38.2% 同比提升",
                    "desc": "长程复杂任务中自主规划与工具调用的无人工干预达成比率。"
                },
                {
                    "label": "母版风格还原准确率",
                    "value": "99.2%",
                    "delta": "母版规范强穿透",
                    "desc": "企业专属字体、配色方案与网格母版的 100% 矢量级忠实复刻。"
                },
                {
                    "label": "协同修改感知延迟",
                    "value": "<8ms",
                    "delta": "SHA-256 毫秒级",
                    "desc": "用户本地手动调整文件后，智能体无感捕获并对齐意图的速度。"
                },
                {
                    "label": "单次综合交付耗时",
                    "value": "45s",
                    "delta": "缩减 90% 工时",
                    "desc": "从原始需求录入到 PPTX 与单文件 HTML 双格式产出的全流程耗时。"
                }
            ]
        },
        {
            "layout_type": "timeline",
            "narrative_arc": "progression",
            "mission": "给出低风险渐进式落地路径，打消听众对迁移风险的顾虑",
            "transition": "【落地】为确保业务平滑过渡，推行‘试点-建设-推广-生态’四步走路线",
            "action_title": "路径：分阶段稳步推进智能体在核心业务线的全域渗透",
            "core_evidence": "Q1 试点验证，Q2 平台就绪，Q3 规模推广，Q4 自主进化闭环",
            "title": "企业落地推行路线与关键里程碑",
            "subtitle": "分阶段稳步推进智能体在核心业务线的全场景渗透与规模化应用",
            "steps": [
                {
                    "time": "2026 Q1 · 试点破局",
                    "title": "场景原型验证",
                    "items": ["核心业务场景 POC", "模板解析标准库搭建", "研发环境私有化联调"]
                },
                {
                    "time": "2026 Q2 · 平台建设",
                    "title": "中枢能力就绪",
                    "items": ["多智能体调度集群上线", "MCP 核心工具链集成", "灰度放量 30% 核心团队"]
                },
                {
                    "time": "2026 Q3 · 规模推广",
                    "title": "业务全域覆盖",
                    "items": ["全公司级统一规范推广", "知识库实时双向同步", "效能分析仪表板运行"]
                },
                {
                    "time": "2026 Q4 · 生态赋能",
                    "title": "自主进化闭环",
                    "items": ["智能体自学习演进机制", "开放生态开发者支持", "商业回报全面兑现"]
                }
            ]
        },
        {
            "layout_type": "summary",
            "narrative_arc": "call_to_action",
            "mission": "发起明确行动号召，锁定立项决策与资源分配动作",
            "transition": "【号召】万事俱备，建议立即启动第一阶段试点立项与研发协同",
            "action_title": "决议：恪守认知动力学与母版穿透准则，启动 Q1 试点立项",
            "core_evidence": "信息充分性与认知契约已就绪，建议立即批准团队编制与算力配额",
            "title": "战略实施建议与收官结论",
            "subtitle": "以信息充分性为牵引，坚守安全合规与人机并肩双向协同原则",
            "points": [
                {
                    "title": "恪守认知动力学契约准则",
                    "desc": "在方案设计前坚决完成深度需求探针与认知差分析，杜绝信息贫血时仓促决策。"
                },
                {
                    "title": "推行母版规范强穿透机制",
                    "desc": "以统一 Design Tokens 统领全局，保障全生命周期在跨团队、跨工具间视觉与语义一致性。"
                },
                {
                    "title": "坚持极简无摩擦的双模交付",
                    "desc": "PPTX 原生矢量对象保障可二次编辑，单文件 HTML 解决大屏与无依赖跨平台极速分发。"
                },
                {
                    "title": "构建 Always-in-Sync 协同飞轮",
                    "desc": "依托毫秒级指纹与语义 AST 感知，随时理解并尊重人类专家的每一步手动调整，保持同频。"
                }
            ]
        }
    ]
}


def cmd_undo(args):
    """Deconstruct template command."""
    print(f"[*] Starting Template Deconstruction on: {args.template}")
    tokens = extract_template_tokens(args.template, extract_assets=True)
    out_file = args.out or ".undoppt/design_tokens.json"
    save_tokens(tokens, out_file)
    print(f"[✓] Design tokens successfully extracted and saved to: {out_file}")
    print(f"    - Theme Mode: {tokens.get('theme_mode', 'light').upper()}")
    print(f"    - Palette:    Primary={tokens['palette'].get('primary')}, Background={tokens['palette'].get('background')}")
    print(f"    - Typography: Title={tokens['typography']['title']['font']}, Body={tokens['typography']['body']['font']}")
    print(f"    - Layouts parsed: {tokens.get('master_layouts_count', 0)}")
    if tokens.get("master_slots"):
        active_slots = [k for k, v in tokens["master_slots"].items() if v]
        print(f"    - Master Slots detected: {', '.join(active_slots)}")
    if tokens.get("extracted_assets"):
        print(f"    - Visual Assets extracted: {len(tokens['extracted_assets'])} media items")


def cmd_build(args):
    """Build presentation command."""
    with open(args.blueprint, "r", encoding="utf-8") as f:
        blueprint = json.load(f)

    tokens_path = args.tokens or "presets/modern_bento.json"
    with open(tokens_path, "r", encoding="utf-8") as f:
        tokens = json.load(f)

    out_dir = args.out or "output"
    os.makedirs(out_dir, exist_ok=True)
    watcher = SyncWatcher()

    if args.format in ("pptx", "all"):
        pptx_out = os.path.join(out_dir, "presentation.pptx")
        build_presentation(blueprint, tokens, pptx_out)
        watcher.record_baseline(pptx_out)
        print(f"[✓] PPTX generated successfully: {pptx_out}")

    if args.format in ("html", "all"):
        html_out = os.path.join(out_dir, "presentation.html")
        build_standalone_html(blueprint, tokens, html_out)
        watcher.record_baseline(html_out)
        print(f"[✓] Standalone HTML generated successfully: {html_out}")


def cmd_plan(args):
    """Autonomous Cognitive Planner: transform natural language prompt into audited blueprint."""
    print(f"[*] Planning presentation for prompt: {args.prompt}")
    doc_path = getattr(args, "input_doc", None)
    if doc_path:
        print(f"    Grounded document: {doc_path}")
    planner = CognitivePlanner()
    blueprint = planner.plan(prompt=args.prompt, context=args.context, doc_path=doc_path)

    out_file = args.out or ".undoppt/blueprint.json"
    os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, ensure_ascii=False, indent=2)

    print(f"[✓] Blueprint planned and saved to: {out_file}")
    print(f"    - Core Thesis: {blueprint['contract']['core_thesis']}")
    print(f"    - Slides:      {len(blueprint['slides'])} slides synthesized")
    print(f"    - Audit Score: {blueprint['audit_summary']['score']} / 100 ({blueprint['audit_summary']['grade']})")
    if blueprint.get("grounded_sources", {}).get("extracted_numbers_count"):
        print(f"    - Grounded:    {blueprint['grounded_sources']['extracted_numbers_count']} quantitative facts extracted")
    if blueprint.get("audit_summary", {}).get("refinements_applied"):
        print(f"    - Refinements: {len(blueprint['audit_summary']['refinements_applied'])} auto-patches applied")


def cmd_generate(args):
    """End-to-end one-shot generation: prompt -> plan -> audit -> dual build."""
    print("================================================================")
    print("  undoPPT Super Skill - End-to-End Autonomous Generation (v2.6)")
    print("================================================================")
    print(f"[*] Prompt: {args.prompt}")
    doc_path = getattr(args, "input_doc", None)
    if doc_path:
        print(f"[*] Input Grounding Document: {doc_path}")

    # 1. Deconstruct or pick tokens
    tokens = {}
    if getattr(args, "template", None) and os.path.exists(args.template):
        print(f"[1/4] Deconstructing template: {args.template}...")
        tokens = extract_template_tokens(args.template, extract_assets=True)
        os.makedirs(".undoppt", exist_ok=True)
        save_tokens(tokens, ".undoppt/design_tokens.json")
    else:
        tokens_path = getattr(args, "tokens", None) or "presets/modern_bento.json"
        print(f"[1/4] Loading design tokens: {tokens_path}...")
        with open(tokens_path, "r", encoding="utf-8") as f:
            tokens = json.load(f)

    # 2. Plan Blueprint
    print("[2/4] Running Cognitive Planner & 10-Dimension Narrative Synthesis...")
    planner = CognitivePlanner(auditor=ContentAuditor(tokens=tokens))
    blueprint = planner.plan(
        prompt=args.prompt,
        context=getattr(args, "context", None),
        doc_path=doc_path
    )
    bp_path = os.path.join(args.out or "output", "blueprint.json")
    os.makedirs(os.path.dirname(os.path.abspath(bp_path)), exist_ok=True)
    with open(bp_path, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, ensure_ascii=False, indent=2)
    print(f"      Composite Score: {blueprint['audit_summary']['score']}/100 | Grade: {blueprint['audit_summary']['grade']}")

    # 3. Build Presentations
    out_dir = args.out or "output"
    os.makedirs(out_dir, exist_ok=True)
    watcher = SyncWatcher()

    if args.format in ("pptx", "all"):
        pptx_out = os.path.join(out_dir, "presentation.pptx")
        print("[3/4] Rendering Native Vector PPTX (with Speaker Notes injected)...")
        build_presentation(blueprint, tokens, pptx_out)
        watcher.record_baseline(pptx_out)

    if args.format in ("html", "all"):
        html_out = os.path.join(out_dir, "presentation.html")
        print("[4/4] Compiling Standalone HTML (with Cognitive Inspector Drawer)...")
        build_standalone_html(blueprint, tokens, html_out)
        watcher.record_baseline(html_out)

    print("\n[SUCCESS] Autonomous Delivery Complete!")
    print(f"  • Blueprint:       {os.path.abspath(bp_path)}")
    if args.format in ("pptx", "all"):
        print(f"  • PowerPoint PPTX: {os.path.abspath(os.path.join(out_dir, 'presentation.pptx'))}")
    if args.format in ("html", "all"):
        print(f"  • Standalone HTML: {os.path.abspath(os.path.join(out_dir, 'presentation.html'))}")
    print("================================================================")


def cmd_audit(args):
    """Audit presentation blueprint for cognitive quality and content architecture."""
    with open(args.blueprint, "r", encoding="utf-8") as f:
        blueprint = json.load(f)

    tokens = {}
    tokens_path = args.tokens or "presets/modern_bento.json"
    if os.path.exists(tokens_path):
        with open(tokens_path, "r", encoding="utf-8") as f:
            tokens = json.load(f)

    auditor = ContentAuditor(tokens=tokens)
    res = auditor.audit(blueprint)

    print("================================================================")
    print("  undoPPT Cognitive Quality & Content Architecture Audit (v2.6) ")
    print("================================================================")
    print(f"  • Composite Score:  {res['score']} / 100")
    print(f"    - Structural:     {res.get('structural_score', res['score'])} / 100")
    print(f"    - Semantic:       {res.get('semantic_score', res['score'])} / 100")
    if "semantic_subscores" in res:
        subs = res["semantic_subscores"]
        print(f"      · Causal Cohesion:    {subs.get('causal_cohesion', 0)} / 100")
        print(f"      · Thesis Alignment:   {subs.get('thesis_alignment', 0)} / 100")
        print(f"      · Evidence Weight:    {subs.get('evidence_weight', 0)} / 100")
        print(f"      · Skepticism Defense: {subs.get('skepticism_defense', 0)} / 100")
    print(f"  • Quality Grade:    {res['grade']}")
    print(f"  • Total Slides:     {res['total_slides']}")
    print(f"  • Result:           {'[PASS] High-Impact Presentation' if res['passed'] else '[WARN] Cognitive Optimization Needed'}")
    print("----------------------------------------------------------------")
    if not res["findings"]:
        print("  ✓ Exemplary content architecture! All 10 cognitive metrics satisfied.")
    else:
        print("  Findings & Actionable Recommendations:")
        for f in res["findings"]:
            prefix = "[!]" if f["level"] == "warning" else "[i]"
            print(f"    {prefix} ({f['code']}) {f['message']}")
    print("================================================================")


def cmd_sync(args):
    """Check sync status with user external modifications."""
    target = args.target or "output/presentation.pptx"
    watcher = SyncWatcher()
    res = watcher.check_sync(target)

    if not res.get("exists"):
        print(f"[!] Target file does not exist: {target}")
        sys.exit(1)

    if res.get("changed"):
        print(f"[⚡] Manual modifications DETECTED in: {target}")
        print(f"    Summary: {res.get('summary')}")
        if res.get("details"):
            for d in res["details"]:
                print(f"    - {d}")
    else:
        print(f"[✓] File is in SYNC with agent baseline: {target}")


def cmd_demo(args):
    """Run full demonstration pipeline."""
    print("================================================================")
    print("  undoPPT Super Skill - End-to-End Demo Generation Pipeline    ")
    print("================================================================")

    # 1. Load preset tokens
    tokens_path = "presets/modern_bento.json"
    with open(tokens_path, "r", encoding="utf-8") as f:
        tokens = json.load(f)

    # 2. Save blueprint & tokens into .undoppt cache
    os.makedirs(".undoppt", exist_ok=True)
    with open(".undoppt/blueprint.json", "w", encoding="utf-8") as f:
        json.dump(DEMO_BLUEPRINT, f, ensure_ascii=False, indent=2)
    with open(".undoppt/design_tokens.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)

    # 3. Perform Cognitive Quality Audit
    print("[1/4] Auditing Cognitive Quality & Narrative Dynamics...")
    auditor = ContentAuditor(tokens=tokens)
    audit_res = auditor.audit(DEMO_BLUEPRINT)
    print(f"      Score: {audit_res['score']}/100 | Grade: {audit_res['grade']}")

    # 4. Generate both formats
    out_dir = "output"
    pptx_path = os.path.join(out_dir, "presentation.pptx")
    html_path = os.path.join(out_dir, "presentation.html")

    print("[2/4] Rendering Native Vector PPTX (with Speaker Notes injected)...")
    build_presentation(DEMO_BLUEPRINT, tokens, pptx_path)

    print("[3/4] Compiling Standalone HTML (with Cognitive Inspector Drawer)...")
    build_standalone_html(DEMO_BLUEPRINT, tokens, html_path)

    print("[4/4] Initializing Sync Watcher Fingerprints...")
    watcher = SyncWatcher()
    watcher.record_baseline(pptx_path)
    watcher.record_baseline(html_path)

    print("\n[SUCCESS] Delivery Complete!")
    print(f"  • PowerPoint PPTX: {os.path.abspath(pptx_path)}")
    print(f"  • Standalone HTML: {os.path.abspath(html_path)}")
    print(f"  • Sync Baseline:   .undoppt/sync_state.json")
    print("================================================================")


def main():
    parser = argparse.ArgumentParser(description="undoPPT Super Skill Engine CLI (v2.6.0)")
    subparsers = parser.add_subparsers(dest="command")

    # plan
    p_plan = subparsers.add_parser("plan", help="Autonomous Cognitive Planner (Prompt to Blueprint)")
    p_plan.add_argument("--prompt", required=True, help="User prompt / presentation goal")
    p_plan.add_argument("--input-doc", default=None, help="Path to document (.md, .txt) to ground plan in domain facts")
    p_plan.add_argument("--context", default=None, help="Optional background notes or constraints")
    p_plan.add_argument("--out", default=".undoppt/blueprint.json", help="Output blueprint JSON path")

    # generate
    p_gen = subparsers.add_parser("generate", help="One-shot autonomous generation (Prompt to Deliverables)")
    p_gen.add_argument("--prompt", required=True, help="User prompt / presentation goal")
    p_gen.add_argument("--input-doc", default=None, help="Path to document (.md, .txt) to ground plan in domain facts")
    p_gen.add_argument("--context", default=None, help="Optional background notes")
    p_gen.add_argument("--template", default=None, help="Optional template .pptx to deconstruct")
    p_gen.add_argument("--tokens", default="presets/modern_bento.json", help="Design tokens JSON path")
    p_gen.add_argument("--format", choices=["pptx", "html", "all"], default="all", help="Output format")
    p_gen.add_argument("--out", default="output", help="Output directory")

    # undo
    p_undo = subparsers.add_parser("undo", help="Deconstruct PPTX template")
    p_undo.add_argument("--template", required=True, help="Path to template .pptx")
    p_undo.add_argument("--out", default=".undoppt/design_tokens.json", help="Output tokens JSON path")

    # build
    p_build = subparsers.add_parser("build", help="Build presentation from blueprint")
    p_build.add_argument("--blueprint", required=True, help="Path to slides_blueprint.json")
    p_build.add_argument("--tokens", default="presets/modern_bento.json", help="Path to design_tokens.json")
    p_build.add_argument("--format", choices=["pptx", "html", "all"], default="all", help="Output format")
    p_build.add_argument("--out", default="output", help="Output directory")

    # audit
    p_audit = subparsers.add_parser("audit", help="Audit presentation blueprint for cognitive quality")
    p_audit.add_argument("--blueprint", required=True, help="Path to blueprint.json")
    p_audit.add_argument("--tokens", default="presets/modern_bento.json", help="Path to design_tokens.json")

    # sync
    p_sync = subparsers.add_parser("sync", help="Check for external user edits")
    p_sync.add_argument("--target", default="output/presentation.pptx", help="Target file path to check")

    # demo
    subparsers.add_parser("demo", help="Generate full showcase presentation")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "plan":
        cmd_plan(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "undo":
        cmd_undo(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "audit":
        cmd_audit(args)
    elif args.command == "sync":
        cmd_sync(args)
    elif args.command == "demo":
        cmd_demo(args)


if __name__ == "__main__":
    main()
