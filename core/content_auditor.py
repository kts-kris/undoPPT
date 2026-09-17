"""content_auditor.py - Cognitive Quality & Content Architecture Auditor for undoPPT.

Audits presentation blueprints against the 10 Core Content Quality Metrics:
  1. Core Thesis clarity (Q1)
  2. Audience and Persona alignment (Q2)
  3. Knowledge baseline & Delta awareness (Q3)
  4. Understand-Believe-Act outcome closure (Q4)
  5. Narrative pacing and dramatic arc (Q5)
  6. Single slide mission responsibility (Q6)
  7. Information density budget enforcement (Q7)
  8. Progressive disclosure & Action title priority (Q8)
  9. Core evidence vs secondary footnote distinction (Q9)
  10. Inter-slide rhetorical transitions and causality (Q10)
"""

import json
import re
from typing import Any, Callable, Dict, List, Optional, Tuple

from core.semantic_auditor import SemanticAuditor


class ContentAuditor:
    """Audits blueprints and tokens against cognitive engineering and semantic standards."""

    PASSIVE_TITLE_KEYWORDS = [
        "简介", "背景", "概览", "介绍", "现状", "思考", "分析", "总结",
        "overview", "background", "introduction", "status", "architecture", "summary"
    ]

    BUZZWORD_PATTERNS = [
        (re.compile(r"不仅[是为能有].*?更[是为能有]", re.IGNORECASE), "不仅是...更是... (AI特征套话，建议直接陈述事实机制)"),
        (re.compile(r"(闭环|抓手|赋能|打法|颗粒度|底层逻辑|盘活|解构|破局)", re.IGNORECASE), "空洞管理黑话 (缺乏具体操作动词，建议改为'构建/降低/交付/量化')"),
        (re.compile(r"为什么.*凭什么.*怎么做", re.IGNORECASE), "口号式设问句式 (建议替换为明确的业务论断或行动结论)"),
        (re.compile(r"\d+大战场|\d+维路径", re.IGNORECASE), "虚夸式宏大叙事套话 (建议具体说明执行领域或交付模块)"),
    ]

    VALID_TRANSITIONS = {"fade", "push", "wipe", "none"}

    def __init__(self, tokens: Optional[Dict[str, Any]] = None, llm_judge_fn: Optional[Callable] = None):
        self.tokens = tokens or {}
        self.budget = self.tokens.get("content_budget", {
            "density_tier": "balanced",
            "max_cards": 4,
            "max_title_words": 20,
            "max_bullet_points": 4,
            "max_desc_words": 50
        })
        self.semantic_auditor = SemanticAuditor(llm_judge_fn=llm_judge_fn)

    def audit(self, blueprint_data: Any) -> Dict[str, Any]:
        """Perform comprehensive cognitive & semantic audit of a presentation blueprint.

        Supports both raw list of slides and wrapped dict {"contract": ..., "slides": [...]}.
        """
        contract = None
        slides = []

        if isinstance(blueprint_data, dict):
            contract = blueprint_data.get("contract")
            slides = blueprint_data.get("slides", [])
        elif isinstance(blueprint_data, list):
            slides = blueprint_data

        findings: List[Dict[str, Any]] = []
        struct_score = 100

        # --- 1. Audit Cognitive Contract (Q1 - Q4) ---
        contract_findings, contract_score_deduction = self._audit_contract(contract)
        findings.extend(contract_findings)
        struct_score -= contract_score_deduction

        # --- 2. Audit Narrative Flow & Pacing (Q5, Q10) ---
        flow_findings, flow_deduction = self._audit_narrative_flow(slides)
        findings.extend(flow_findings)
        struct_score -= flow_deduction

        # --- 3. Audit Slide-by-Slide Cognitive Quality (Q6 - Q9) ---
        slide_findings, slide_deduction = self._audit_slides(slides)
        findings.extend(slide_findings)
        struct_score -= slide_deduction

        # --- 3.5 Audit Enterprise Rules (v3.4: Decision Ask, Benchmark Rigor, Promotion STAR) ---
        scenario_type = None
        if isinstance(blueprint_data, dict):
            scenario_type = blueprint_data.get("scenario") or blueprint_data.get("scenario_type")
        ent_findings, ent_deduction = self._audit_enterprise_rules(slides, scenario_type, contract)
        findings.extend(ent_findings)
        struct_score -= ent_deduction

        struct_score = max(0, min(100, struct_score))

        # --- 4. Deep Semantic & Rhetorical Audit (v2.5.0) ---
        semantic_res = self.semantic_auditor.audit_semantics(contract, slides)
        findings.extend(semantic_res.get("findings", []))
        semantic_score = semantic_res.get("semantic_score", 100.0)

        # Composite score: 50% structural density & rules + 50% deep semantic cohesion & evidence
        final_score = round(max(0.0, min(100.0, struct_score * 0.5 + semantic_score * 0.5)), 1)

        # Overall assessment
        if final_score >= 85:
            grade = "A (Exemplary Cognitive Impact)"
        elif final_score >= 70:
            grade = "B (Solid Logic with Minor Noise)"
        elif final_score >= 50:
            grade = "C (Information Overload / Generic Flow)"
        else:
            grade = "D (Needs Cognitive Restructuring)"

        return {
            "score": final_score,
            "structural_score": struct_score,
            "semantic_score": semantic_score,
            "semantic_subscores": semantic_res.get("subscores", {}),
            "grade": grade,
            "total_slides": len(slides),
            "findings": findings,
            "passed": final_score >= 70
        }

    def _audit_contract(self, contract: Optional[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        findings = []
        deduction = 0

        if not contract:
            findings.append({
                "level": "warning",
                "code": "MISSING_COGNITIVE_CONTRACT",
                "message": "未绑定顶层《认知契约》(Cognitive Contract)。建议明确受众(Q2)、信息差(Q3)与行动目标(Q4)。"
            })
            return findings, 10

        # Check Q1: Core Thesis
        if not contract.get("core_thesis") and not contract.get("message"):
            findings.append({
                "level": "warning",
                "code": "UNCLEAR_THESIS",
                "message": "认知契约缺少核心主旨(core_thesis)，可能导致整篇推演失去重心(Q1)。"
            })
            deduction += 3

        # Check Q2: Audience
        if not contract.get("audience"):
            findings.append({
                "level": "warning",
                "code": "MISSING_AUDIENCE_PROFILE",
                "message": "未定义目标受众画像(audience)，无法验证内容是否匹配听众心智(Q2)。"
            })
            deduction += 3

        # Check Q3: Knowledge Delta
        delta = contract.get("knowledge_delta", {})
        if not delta.get("blindspots_and_pains"):
            findings.append({
                "level": "info",
                "code": "UNSPECIFIED_KNOWLEDGE_DELTA",
                "message": "未标注受众的认知盲区或核心痛点(Q3)，建议聚焦填补信息差。"
            })

        # Check Q4: Understand-Believe-Act
        outcomes = contract.get("target_outcomes", {})
        if not outcomes.get("act"):
            findings.append({
                "level": "warning",
                "code": "MISSING_ACTION_OUTCOME",
                "message": "认知契约中未定义受众看完后的具体动作(Act)(Q4)，缺乏决策推进力。"
            })
            deduction += 4

        return findings, deduction

    def _audit_narrative_flow(self, slides: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        findings = []
        deduction = 0

        if len(slides) < 2:
            return findings, deduction

        transitions_count = sum(1 for s in slides[1:] if s.get("transition"))
        if transitions_count == 0:
            findings.append({
                "level": "warning",
                "code": "DISCONNECTED_FLOW",
                "message": "页面之间缺少显式承上启下逻辑连词(transition)(Q10)。可能导致前后页沦为信息孤岛。"
            })
            deduction += 6
        elif transitions_count < (len(slides) - 1) * 0.5:
            findings.append({
                "level": "info",
                "code": "WEAK_TRANSITIONS",
                "message": f"仅有 {transitions_count}/{len(slides)-1} 页配置了转折连词，建议强化因果与冲突推进(Q10)。"
            })
            deduction += 2

        # Check narrative arc progression (Q5)
        arcs = [s.get("narrative_arc") for s in slides if s.get("narrative_arc")]
        if not arcs:
            findings.append({
                "level": "info",
                "code": "UNSPECIFIED_NARRATIVE_ARC",
                "message": "未标注叙事节奏阶段(narrative_arc: hook → conflict → breakthrough → evidence → call_to_action)(Q5)。"
            })

        return findings, deduction

    def _audit_slides(self, slides: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        findings = []
        deduction = 0

        for idx, slide in enumerate(slides):
            page_num = idx + 1
            title = slide.get("title", "")
            mission = slide.get("mission")
            layout = slide.get("layout_type", "unknown")

            # Q6: Single Responsibility / Mission
            if not mission and layout != "cover":
                findings.append({
                    "level": "info",
                    "code": f"MISSING_MISSION_P{page_num}",
                    "message": f"第 {page_num} 页未声明单页职责(mission)(Q6)，请明确该页的唯一核心使命。"
                })

            # Q8: Action Title check
            stripped_title = title.strip().lower()
            if any(stripped_title == kw or stripped_title.startswith(f"{kw}：") or stripped_title.startswith(f"{kw}:") for kw in self.PASSIVE_TITLE_KEYWORDS):
                findings.append({
                    "level": "warning",
                    "code": f"PASSIVE_TITLE_P{page_num}",
                    "message": f"第 {page_num} 页标题 '{title}' 属于中性被动命名。建议采用观点先行/行动结论式标题(Action Title)(Q8)。"
                })
                deduction += 2

            # Anti-Pattern & Buzzword check (v3.2)
            slide_text_corpus = " ".join([
                str(slide.get("title", "")),
                str(slide.get("action_title", "")),
                str(slide.get("subtitle", "")),
                str(slide.get("mission", "")),
                str(slide.get("transition", "")),
                str(slide.get("core_evidence", "")),
                json.dumps(slide, ensure_ascii=False)
            ])
            buzzword_found = False
            for pattern, desc in self.BUZZWORD_PATTERNS:
                m = pattern.search(slide_text_corpus)
                if m:
                    findings.append({
                        "level": "warning",
                        "code": f"BUZZWORD_DETECTED_P{page_num}",
                        "message": f"第 {page_num} 页检测到空洞 AI 套话/黑话：'{m.group()}'（{desc}）。请遵循场景避坑红线，替换为具体事实机制与量化动作。"
                    })
                    if not buzzword_found:
                        deduction += 2
                        buzzword_found = True

            # Transition effect validity check (v3.2)
            trans = slide.get("transition_effect")
            if trans and trans not in self.VALID_TRANSITIONS:
                findings.append({
                    "level": "warning",
                    "code": f"INVALID_TRANSITION_P{page_num}",
                    "message": f"第 {page_num} 页切页动效 '{trans}' 无效。支持：{', '.join(sorted(self.VALID_TRANSITIONS))}。"
                })

            # Q7: Information Density budget check
            if layout in ("bento_cards",):
                cards = slide.get("cards", [])
                max_cards = self.budget.get("max_cards", 4)
                if len(cards) > max_cards:
                    findings.append({
                        "level": "warning",
                        "code": f"DENSITY_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页卡片数量({len(cards)})超过当前设计预设上限({max_cards})，易引发认知过载(Q7)。"
                    })
                    deduction += 3
            elif layout in ("architecture_stack",):
                layers = slide.get("layers", [])
                max_layers = self.budget.get("max_layers", 4)
                if len(layers) > max_layers:
                    findings.append({
                        "level": "warning",
                        "code": f"LAYERS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页架构层级({len(layers)})过多，建议归纳提炼至 {max_layers} 层以内(Q7)。"
                    })
                    deduction += 3
            elif layout in ("matrix_2x2", "matrix"):
                quads = slide.get("quadrants", [])
                if isinstance(quads, list) and len(quads) > 4:
                    findings.append({
                        "level": "warning",
                        "code": f"MATRIX_QUADS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页 2x2 矩阵象限数({len(quads)})超出4个，请核查布局结构(Q7)。"
                    })
                    deduction += 2
            elif layout in ("maturity_ladder", "ladder"):
                levels = slide.get("levels", [])
                if len(levels) > 5:
                    findings.append({
                        "level": "warning",
                        "code": f"LADDER_LEVELS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页阶梯阶数({len(levels)})过多，建议精简至 4-5 级以内保障视觉呼吸感(Q7)。"
                    })
                    deduction += 3
            elif layout in ("horizons_curve", "horizons", "three_horizons"):
                horizons = slide.get("horizons", [])
                if len(horizons) > 3:
                    findings.append({
                        "level": "warning",
                        "code": f"HORIZONS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页地平线模型应遵循经典 H1/H2/H3 三层次，当前为 {len(horizons)} 层(Q7)。"
                    })
                    deduction += 2
            elif layout in ("cross_mapping", "dual_mapping"):
                rows = slide.get("mapping_rows") or slide.get("rows", [])
                if len(rows) > 5:
                    findings.append({
                        "level": "warning",
                        "code": f"MAPPING_ROWS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页映射行数({len(rows)})过多，建议精炼核心层级至 4-5 行以内(Q7)。"
                    })
                    deduction += 2
            elif layout in ("standard_table", "table"):
                rows = slide.get("rows", [])
                headers = slide.get("headers", [])
                if len(rows) > 8:
                    findings.append({
                        "level": "warning",
                        "code": f"TABLE_ROWS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页表格行数({len(rows)})过多，建议精简至 8 行以内或拆页呈现(Q7)。"
                    })
                    deduction += 2
                if len(headers) > 6:
                    findings.append({
                        "level": "warning",
                        "code": f"TABLE_COLS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页表格列数({len(headers)})过多，易导致阅读拥挤(Q7)。"
                    })
                    deduction += 2
            elif layout in ("content_columns", "columns"):
                cols = slide.get("columns", [])
                if len(cols) > 4:
                    findings.append({
                        "level": "warning",
                        "code": f"COLUMNS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页并列列数({len(cols)})超过 4 列上限，横向排版易受挤压(Q7)。"
                    })
                    deduction += 2
            elif layout in ("process_flow", "flow", "linear_flow"):
                steps = slide.get("steps", [])
                if len(steps) > 6:
                    findings.append({
                        "level": "warning",
                        "code": f"FLOW_STEPS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页流程节点({len(steps)})过多，建议阶段化或精简至 6 步以内(Q7)。"
                    })
                    deduction += 2
            elif layout in ("data_chart", "chart"):
                categories = slide.get("categories", [])
                if len(categories) > 8:
                    findings.append({
                        "level": "warning",
                        "code": f"CHART_CATEGORIES_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页图表类目数({len(categories)})过多，建议精简核心对比维度(Q7)。"
                    })
                    deduction += 2

        return findings, deduction

    def _audit_enterprise_rules(
        self,
        slides: List[Dict[str, Any]],
        scenario_type: Optional[str],
        contract: Optional[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Audit enterprise management rigor: Decision-Ready Ask, Objective Benchmarking, Promotion STAR."""
        findings = []
        deduction = 0

        if not slides:
            return findings, deduction

        stype = (scenario_type or "").lower()

        # Rule 1: DECISION_ASK_MISSING
        # Management-facing briefings require explicit decision ask (sign_off_items or options)
        leadership_scenarios = {
            "project_charter", "annual_strategy_okr", "team_headcount_review",
            "tech_rfc_review", "cross_team_alignment", "strategic_planning"
        }
        if stype in leadership_scenarios:
            has_decision_ask = False
            for slide in slides:
                if slide.get("options") or slide.get("sign_off_items"):
                    has_decision_ask = True
                    break
            if not has_decision_ask:
                findings.append({
                    "level": "warning",
                    "code": "DECISION_ASK_MISSING",
                    "message": "管理汇报收尾页未提供明确的【请领导决策事项】(sign_off_items 或 options 选项比选)。向上汇报绝不能以泛泛空话结尾，必须推动高管审批与资源决议。"
                })
                deduction += 4

        # Rule 2: BENCHMARK_UNBALANCED
        # Comparison tables must establish balanced trade-offs (costs, migration friction, or boundaries)
        for idx, slide in enumerate(slides):
            page_num = idx + 1
            layout = slide.get("layout_type", "")
            if layout in ("standard_table", "table"):
                title_corpus = f"{slide.get('title', '')} {slide.get('action_title', '')} {slide.get('mission', '')}".lower()
                is_comparison = any(kw in title_corpus for kw in ["对比", "选型", "竞品", "对标", "benchmark", "rfc"])
                if is_comparison:
                    headers = [str(h).lower() for h in slide.get("headers", [])]
                    rows = slide.get("rows", [])
                    all_text = " ".join([str(c) for r in rows for c in r]).lower() + " " + " ".join(headers)
                    has_tradeoffs = any(kw in all_text for kw in [
                        "成本", "摩擦", "门槛", "劣势", "缺点", "局限", "trade-off", "tradeoff",
                        "代价", "短板", "学习成本", "风险", "适用边界", "复杂度", "兼容性"
                    ])
                    if len(rows) >= 2 and not has_tradeoffs:
                        findings.append({
                            "level": "warning",
                            "code": f"BENCHMARK_UNBALANCED_P{page_num}",
                            "message": f"第 {page_num} 页外部对标/选型表格缺乏客观权衡维度(成本/迁移摩擦/适用边界/门槛)。严禁虚假全优对比，必须客观呈现妥协与代价。"
                        })
                        deduction += 3

        # Rule 3: PROMOTION_LAUNDRY_LIST
        # Promotion reviews must avoid laundry list duty dumps without metrics or STAR causality
        if stype in ("promotion_assessment", "career_portfolio"):
            for idx, slide in enumerate(slides):
                page_num = idx + 1
                layout = slide.get("layout_type", "")
                if layout in ("content_columns", "bento_cards"):
                    corpus = json.dumps(slide, ensure_ascii=False)
                    has_laundry = any(kw in corpus for kw in ["日常维护", "日常跟进", "参与了", "协助完成", "各种琐碎", "常规工作", "负责日常"])
                    has_quantified = bool(re.search(r'\d+(\.\d+)?(%|万|亿|倍|qps|ms|人|次|个|级)', corpus, re.IGNORECASE))
                    if has_laundry and not has_quantified:
                        findings.append({
                            "level": "warning",
                            "code": f"PROMOTION_LAUNDRY_LIST_P{page_num}",
                            "message": f"第 {page_num} 页述职内容呈现碎片化任务流水账，缺乏 STAR 框架因果归因与量化净增量成果。建议剥离大盘红利，突出个人核心贡献。"
                        })
                        deduction += 4

        return findings, deduction

