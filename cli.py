#!/usr/bin/env python3
"""cli.py - Unified Command Line Interface for undoPPT Super Skill Engine.

Usage:
  python3 cli.py undo --template <template.pptx> [--out <tokens.json>]
  python3 cli.py build --blueprint <blueprint.json> [--tokens <tokens.json>] [--format pptx|html|all] [--out <dir>]
  python3 cli.py sync [--target <file.pptx>]
  python3 cli.py demo
"""

import argparse
import json
import os
import sys

from core.html_builder import build_standalone_html
from core.pptx_builder import build_presentation
from core.sync_watcher import SyncWatcher
from core.undo_engine import extract_template_tokens, save_tokens


DEMO_BLUEPRINT = [
    {
        "layout_type": "cover",
        "category": "ENTERPRISE STRATEGY & ARCHITECTURE 2026",
        "title": "新一代企业级 Agentic AI 业务与架构全景方案",
        "subtitle": "从单一认知对话到多智能体自主协同的工业化演进之路",
        "meta": "undoPPT Super Skill 联合出品 · 架构评审专供"
    },
    {
        "layout_type": "bento_cards",
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
        "title": "战略实施建议与收官结论",
        "subtitle": "以信息充分性为牵引，坚守安全合规与人机并肩双向协同原则",
        "points": [
            {
                "title": "恪守信息充分性第一准则",
                "desc": "在方案设计前坚决完成深度需求探针与企业内部素材注水，杜绝信息贫血时仓促决策。"
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


def cmd_undo(args):
    """Deconstruct template command."""
    print(f"[*] Starting Template Deconstruction on: {args.template}")
    tokens = extract_template_tokens(args.template)
    out_file = args.out or ".undoppt/design_tokens.json"
    save_tokens(tokens, out_file)
    print(f"[✓] Design tokens successfully extracted and saved to: {out_file}")
    print(f"    - Palette: Primary={tokens['palette'].get('primary')}, Background={tokens['palette'].get('background')}")
    print(f"    - Typography: Title={tokens['typography']['title']['font']}, Body={tokens['typography']['body']['font']}")
    print(f"    - Layouts parsed: {tokens.get('master_layouts_count', 0)}")


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

    # 3. Generate both formats
    out_dir = "output"
    pptx_path = os.path.join(out_dir, "presentation.pptx")
    html_path = os.path.join(out_dir, "presentation.html")

    print("[1/3] Rendering Native Vector PPTX (100% editable shapes)...")
    build_presentation(DEMO_BLUEPRINT, tokens, pptx_path)

    print("[2/3] Compiling Standalone Zero-Dependency HTML...")
    build_standalone_html(DEMO_BLUEPRINT, tokens, html_path)

    print("[3/3] Initializing Sync Watcher Fingerprints...")
    watcher = SyncWatcher()
    watcher.record_baseline(pptx_path)
    watcher.record_baseline(html_path)

    print("\n[SUCCESS] Delivery Complete!")
    print(f"  • PowerPoint PPTX: {os.path.abspath(pptx_path)}")
    print(f"  • Standalone HTML: {os.path.abspath(html_path)}")
    print(f"  • Sync Baseline:   .undoppt/sync_state.json")
    print("================================================================")


def main():
    parser = argparse.ArgumentParser(description="undoPPT Super Skill Engine CLI")
    subparsers = parser.add_subparsers(dest="command")

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

    # sync
    p_sync = subparsers.add_parser("sync", help="Check for external user edits")
    p_sync.add_argument("--target", default="output/presentation.pptx", help="Target file path to check")

    # demo
    subparsers.add_parser("demo", help="Generate full showcase presentation")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "undo":
        cmd_undo(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "sync":
        cmd_sync(args)
    elif args.command == "demo":
        cmd_demo(args)


if __name__ == "__main__":
    main()
