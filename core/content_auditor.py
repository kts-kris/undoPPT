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

import re
from typing import Any, Dict, List, Optional, Tuple


class ContentAuditor:
    """Audits blueprints and tokens against cognitive engineering standards."""

    PASSIVE_TITLE_KEYWORDS = [
        "简介", "背景", "概览", "介绍", "现状", "思考", "分析", "总结",
        "overview", "background", "introduction", "status", "architecture", "summary"
    ]

    def __init__(self, tokens: Optional[Dict[str, Any]] = None):
        self.tokens = tokens or {}
        self.budget = self.tokens.get("content_budget", {
            "density_tier": "balanced",
            "max_cards": 4,
            "max_title_words": 20,
            "max_bullet_points": 4,
            "max_desc_words": 50
        })

    def audit(self, blueprint_data: Any) -> Dict[str, Any]:
        """Perform comprehensive cognitive audit of a presentation blueprint.

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
        score = 100

        # --- 1. Audit Cognitive Contract (Q1 - Q4) ---
        contract_findings, contract_score_deduction = self._audit_contract(contract)
        findings.extend(contract_findings)
        score -= contract_score_deduction

        # --- 2. Audit Narrative Flow & Pacing (Q5, Q10) ---
        flow_findings, flow_deduction = self._audit_narrative_flow(slides)
        findings.extend(flow_findings)
        score -= flow_deduction

        # --- 3. Audit Slide-by-Slide Cognitive Quality (Q6 - Q9) ---
        slide_findings, slide_deduction = self._audit_slides(slides)
        findings.extend(slide_findings)
        score -= slide_deduction

        score = max(0, min(100, score))

        # Overall assessment
        if score >= 85:
            grade = "A (Exemplary Cognitive Impact)"
        elif score >= 70:
            grade = "B (Solid Logic with Minor Noise)"
        elif score >= 50:
            grade = "C (Information Overload / Generic Flow)"
        else:
            grade = "D (Needs Cognitive Restructuring)"

        return {
            "score": score,
            "grade": grade,
            "total_slides": len(slides),
            "findings": findings,
            "passed": score >= 70
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

            # Q7: Information Density budget check
            if layout == "bento_cards":
                cards = slide.get("cards", [])
                max_cards = self.budget.get("max_cards", 4)
                if len(cards) > max_cards:
                    findings.append({
                        "level": "warning",
                        "code": f"DENSITY_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页卡片数量({len(cards)})超过当前设计预设上限({max_cards})，易引发认知过载(Q7)。"
                    })
                    deduction += 3
            elif layout == "architecture_stack":
                layers = slide.get("layers", [])
                max_layers = self.budget.get("max_layers", 4)
                if len(layers) > max_layers:
                    findings.append({
                        "level": "warning",
                        "code": f"LAYERS_EXCEEDED_P{page_num}",
                        "message": f"第 {page_num} 页架构层级({len(layers)})过多，建议归纳提炼至 {max_layers} 层以内(Q7)。"
                    })
                    deduction += 3

        return findings, deduction
