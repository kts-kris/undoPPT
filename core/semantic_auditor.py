"""semantic_auditor.py - Semantic Cognitive & Rhetorical Cohesion Auditor (v2.5.0).

Audits presentations against deep semantic metrics:
  1. Semantic Causal Cohesion (Q10 rhetorical transition taxonomy)
  2. Thesis Centrifugal Alignment (Q1 thesis drift detection)
  3. Quantitative Smoking Gun Evidence Weighting (Q9 hard evidence vs slogans)
  4. Audience Skepticism Defense (Q2-Q4 pain confrontation & closure)
  5. Optional Pluggable LLM-as-a-Judge evaluation hook.
"""

import re
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class SemanticAuditor:
    """Evaluates semantic rigor, logical coherence, and empirical evidence weighting."""

    # Rhetorical transition taxonomy
    TRANSITION_TAXONOMY = {
        "contrast": [
            "然而", "但是", "但", "相反", "反之", "不过", "偏偏", "现实是", "痛点", "冲突", "容易混淆", "常犯错误", "难点",
            "however", "but", "yet", "nevertheless", "in contrast", "conversely", "misconception"
        ],
        "causality": [
            "因此", "所以", "导致", "造成", "因而", "鉴于此", "由此可见", "故而", "必然", "由于",
            "therefore", "thus", "consequently", "as a result", "hence", "accordingly"
        ],
        "breakthrough": [
            "破局", "解法", "突破", "应对", "重构", "打穿", "重塑", "策略", "方案", "立足", "掌握方法", "记忆诀窍", "核心要点", "核心解法",
            "solution", "breakthrough", "transform", "reframe", "overcome", "solve", "technique"
        ],
        "progression": [
            "进而", "进一步", "随后", "不仅如此", "在此基础上", "递进", "同时", "随之", "由浅入深", "循序渐进", "拓展延伸", "由此及彼", "深入解析", "分步拆解",
            "furthermore", "moreover", "next", "in addition", "subsequently", "beyond", "step by step"
        ],
        "evidence": [
            "实证", "验证", "数据表明", "测算", "落地成效", "实践表明", "核验", "硬核", "实例印证", "案例分析", "范例", "示例", "例句", "课堂反馈", "实践证明",
            "evidence", "proven", "data shows", "metrics", "empirically", "verified", "case study", "example"
        ],
        "action": [
            "决议", "建议", "号召", "当场", "启动", "批准", "行动", "实施", "拍板", "落地", "学以致用", "演练实践", "实战巩固", "作业布置", "实践练习", "巩固提升",
            "call to action", "decision", "action", "approve", "mandate", "execute", "practice", "exercise"
        ]
    }

    # Number / evidence patterns: percentages, multipliers, ratios, units (ms, s, 万, 亿, etc.)
    EVIDENCE_PATTERN = re.compile(
        r"(\d+(?:\.\d+)?%|\b\d+x\b|\d+:\d+(?::\d+)?|[<>]?\s*\d+(?:\.\d+)?\s*(?:ms|s|h|min|万|亿|千|元|k|m|b|倍|个|家|天|月|年|分|条|点|道|字|篇))",
        re.IGNORECASE
    )

    # Pedagogical / qualitative evidence pattern for education and training
    QUALITATIVE_EVIDENCE_PATTERN = re.compile(
        r"(例|示例|例题|案例|课标|法则|诀窍|规范|步骤|示范|练习|掌握|考点|对比|解析|真题|图解|经典)",
        re.IGNORECASE
    )

    STOP_WORDS = {
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个",
        "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好",
        "自己", "这", "全面", "推进", "进行", "关于", "基于", "以及", "通过", "实现",
        "the", "a", "an", "and", "or", "to", "in", "for", "of", "with", "by", "on"
    }

    def __init__(self, llm_judge_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
        """Initialize SemanticAuditor with optional LLM judge hook."""
        self.llm_judge_fn = llm_judge_fn

    def audit_semantics(self, contract: Optional[Dict[str, Any]], slides: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audit blueprint against the 4 semantic dimensions and optional LLM judge."""
        findings: List[Dict[str, Any]] = []

        # 1. Rhetorical Causal Cohesion
        cohesion_score, cohesion_findings = self._audit_causal_cohesion(slides)
        findings.extend(cohesion_findings)

        # 2. Thesis Centrifugal Alignment
        alignment_score, alignment_findings = self._audit_thesis_alignment(contract, slides)
        findings.extend(alignment_findings)

        # 3. Quantitative Smoking Gun Evidence Weight
        evidence_score, evidence_findings = self._audit_evidence_weight(slides, contract=contract)
        findings.extend(evidence_findings)

        # 4. Audience Skepticism Defense
        skepticism_score, skepticism_findings = self._audit_audience_skepticism(contract, slides)
        findings.extend(skepticism_findings)

        # Weighted aggregate offline semantic score
        # Cohesion (25%), Alignment (25%), Evidence (30%), Skepticism (20%)
        composite_score = round(
            cohesion_score * 0.25 +
            alignment_score * 0.25 +
            evidence_score * 0.30 +
            skepticism_score * 0.20,
            1
        )

        llm_critique = None
        if self.llm_judge_fn:
            try:
                llm_critique = self.llm_judge_fn({
                    "contract": contract,
                    "slides": slides,
                    "heuristic_score": composite_score
                })
                if isinstance(llm_critique, dict) and "adjusted_score" in llm_critique:
                    composite_score = float(llm_critique["adjusted_score"])
            except Exception as e:
                findings.append({
                    "level": "info",
                    "code": "LLM_JUDGE_BYPASS",
                    "message": f"LLM 裁判评估未完成，已自动回退到规则本体审计: {str(e)}"
                })

        return {
            "semantic_score": composite_score,
            "subscores": {
                "causal_cohesion": cohesion_score,
                "thesis_alignment": alignment_score,
                "evidence_weight": evidence_score,
                "skepticism_defense": skepticism_score
            },
            "findings": findings,
            "llm_critique": llm_critique
        }

    def _audit_causal_cohesion(self, slides: List[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
        """Audit inter-slide rhetorical transitions and causal progression."""
        findings = []
        if len(slides) <= 1:
            return 100.0, findings

        score = 100.0
        covered_types: Set[str] = set()
        empty_transitions = 0

        for idx in range(1, len(slides)):
            slide = slides[idx]
            page = idx + 1
            transition = slide.get("transition", "")
            narrative_arc = slide.get("narrative_arc", "")

            if not transition.strip():
                empty_transitions += 1
                findings.append({
                    "level": "warning",
                    "code": f"MISSING_TRANSITION_P{page}",
                    "message": f"第 {page} 页缺少逻辑转折词(transition)，前后页缺乏显式因果咬合关系。"
                })
                score -= 10
                continue

            # Classify transition against taxonomy
            matched_taxonomies = []
            trans_lower = transition.lower()
            for cat, keywords in self.TRANSITION_TAXONOMY.items():
                if any(kw in trans_lower for kw in keywords):
                    matched_taxonomies.append(cat)
                    covered_types.add(cat)

            if not matched_taxonomies:
                findings.append({
                    "level": "info",
                    "code": f"GENERIC_TRANSITION_P{page}",
                    "message": f"第 {page} 页转折连词 '{transition}' 语意较弱，未匹配标准因果/冲突/突破本体修辞。"
                })
                score -= 3

            # Check if transition matches narrative arc phase
            if narrative_arc == "conflict" and "contrast" not in matched_taxonomies:
                findings.append({
                    "level": "info",
                    "code": f"ARC_TRANSITION_MISMATCH_P{page}",
                    "message": f"第 {page} 页处于冲突阶段(conflict)，建议转折语中强化对立冲突感(如‘然而’、‘矛盾在于’)。"
                })
                score -= 2

        # Bonus for taxonomy variety
        if len(covered_types) >= 3:
            score += 5
        elif len(covered_types) <= 1 and len(slides) > 3:
            findings.append({
                "level": "info",
                "code": "MONOTONOUS_RHETORIC",
                "message": "整套方案转折语态单一，建议交替使用因果推进、冲突对立与破局重构修辞。"
            })
            score -= 5

        score = max(0.0, min(100.0, score))
        return score, findings

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful semantic tokens from Chinese and English text."""
        if not text:
            return set()
        # Find alphanumeric words
        en_words = set(re.findall(r'[a-zA-Z]{3,}', text.lower()))
        # Find Chinese segments: 2 to 4 char sequences
        clean_cn = re.sub(r'[^一-龥]', ' ', text)
        cn_tokens = set()
        for token in clean_cn.split():
            if len(token) >= 2:
                cn_tokens.add(token)
                # n-grams for longer phrases
                if len(token) > 2:
                    for i in range(len(token) - 1):
                        cn_tokens.add(token[i:i+2])
        raw_set = en_words.union(cn_tokens)
        return {w for w in raw_set if w not in self.STOP_WORDS and len(w) > 1}

    def _audit_thesis_alignment(self, contract: Optional[Dict[str, Any]], slides: List[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
        """Audit whether each slide stays centrifugally aligned to the core thesis."""
        findings = []
        if not contract or not contract.get("core_thesis"):
            return 70.0, [{
                "level": "warning",
                "code": "NO_CORE_THESIS",
                "message": "缺少明确的主旨(core_thesis)，无法进行离心漂移检测。"
            }]

        thesis = contract.get("core_thesis", "")
        thesis_keywords = self._extract_keywords(thesis)
        if not thesis_keywords:
            return 85.0, findings

        score = 100.0
        drifted_slides = 0

        for idx, slide in enumerate(slides):
            page = idx + 1
            # Skip cover
            if slide.get("layout_type") == "cover":
                continue

            # Gather slide text elements
            slide_content = " ".join([
                str(slide.get("title", "")),
                str(slide.get("action_title", "")),
                str(slide.get("subtitle", "")),
                str(slide.get("mission", "")),
                str(slide.get("core_evidence", ""))
            ])
            slide_keywords = self._extract_keywords(slide_content)

            overlap = thesis_keywords.intersection(slide_keywords)
            if not overlap:
                drifted_slides += 1
                findings.append({
                    "level": "warning",
                    "code": f"THESIS_DRIFT_P{page}",
                    "message": f"第 {page} 页核心词汇与顶层主旨 '{thesis[:20]}...' 语义关联度不足，存在离心偏题风险。"
                })
                score -= 8

        if drifted_slides == 0:
            score += 5

        score = max(0.0, min(100.0, score))
        return score, findings

    def _audit_evidence_weight(self, slides: List[Dict[str, Any]], contract: Optional[Dict[str, Any]] = None) -> Tuple[float, List[Dict[str, Any]]]:
        """Audit whether claims are backed by hard, quantified smoking gun evidence or grounded pedagogical examples."""
        findings = []
        score = 100.0
        total_evidence_points = 0
        pages_with_evidence = 0
        scenario = (contract.get("scenario") or contract.get("genre") or "").lower() if contract else ""
        is_education_or_general = scenario in ("education_training", "general_informative")

        for idx, slide in enumerate(slides):
            page = idx + 1
            if slide.get("layout_type") == "cover":
                continue

            # Aggregate all text in slide
            raw_dump = ""
            for k, v in slide.items():
                if isinstance(v, (str, int, float)):
                    raw_dump += f" {v}"
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            raw_dump += " " + " ".join(str(val) for val in item.values())
                        else:
                            raw_dump += f" {item}"

            num_matches = self.EVIDENCE_PATTERN.findall(raw_dump)
            qual_matches = self.QUALITATIVE_EVIDENCE_PATTERN.findall(raw_dump) if is_education_or_general else []
            count = len(num_matches) + len(qual_matches)
            total_evidence_points += count

            if (len(num_matches) > 0) or (is_education_or_general and len(qual_matches) > 0):
                pages_with_evidence += 1

            # Specifically check core_evidence field
            core_evidence = slide.get("core_evidence", "")
            if not core_evidence:
                findings.append({
                    "level": "info",
                    "code": f"MISSING_CORE_EVIDENCE_P{page}",
                    "message": f"第 {page} 页未定义核心实证(core_evidence)，论证说服力易受削弱。"
                })
                score -= 3
            else:
                has_quant = bool(self.EVIDENCE_PATTERN.search(core_evidence))
                has_qual = bool(self.QUALITATIVE_EVIDENCE_PATTERN.search(core_evidence))
                if not has_quant and not (is_education_or_general and has_qual):
                    findings.append({
                        "level": "info",
                        "code": f"UNQUANTIFIED_EVIDENCE_P{page}",
                        "message": f"第 {page} 页核心实证 '{core_evidence[:24]}...' 缺乏具体量化数据或代表性范例支撑。"
                    })
                    score -= 2

        content_pages = max(1, len(slides) - 1)
        evidence_ratio = pages_with_evidence / content_pages
        min_ratio = 0.35 if is_education_or_general else 0.50

        if evidence_ratio < min_ratio:
            findings.append({
                "level": "warning",
                "code": "EVIDENCE_POVERTY",
                "message": f"仅有 {pages_with_evidence}/{content_pages} 页具备充分实证/范例支撑，建议强化论据厚度。"
            })
            score -= 10 if is_education_or_general else 15
        elif evidence_ratio >= 0.8:
            score += 5

        score = max(0.0, min(100.0, score))
        return score, findings

    def _audit_audience_skepticism(self, contract: Optional[Dict[str, Any]], slides: List[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
        """Audit if audience skepticism, pains, and targeted actions are systematically defended."""
        findings = []
        if not contract:
            return 60.0, [{
                "level": "warning",
                "code": "MISSING_CONTRACT",
                "message": "缺少认知契约，无法核验受众疑虑对抗度。"
            }]

        score = 100.0
        delta = contract.get("knowledge_delta", {})
        pains = delta.get("blindspots_and_pains", [])
        outcomes = contract.get("target_outcomes", {})
        act_goal = outcomes.get("act", "")

        # Check pain points coverage
        if pains:
            pains_str = " ".join(pains)
            pain_keywords = self._extract_keywords(pains_str)
            all_slides_content = " ".join([
                f"{s.get('title', '')} {s.get('action_title', '')} {s.get('mission', '')} {s.get('core_evidence', '')}"
                for s in slides
            ])
            covered = pain_keywords.intersection(self._extract_keywords(all_slides_content))
            coverage_rate = len(covered) / max(1, len(pain_keywords))
            if coverage_rate < 0.2:
                findings.append({
                    "level": "warning",
                    "code": "PAINS_IGNORED",
                    "message": "方案未正面触碰认知契约中声明的受众痛点与盲区，可能面临‘不解渴’的质疑。"
                })
                score -= 12

        # Check call to action resolution
        if act_goal:
            last_slide = slides[-1] if slides else {}
            last_dump_parts = [str(last_slide.get(k, '')) for k in ("title", "action_title", "points", "cards", "steps", "columns", "quadrants", "layers", "mission", "subtitle")]
            last_text = " ".join(last_dump_parts)
            act_keywords = self._extract_keywords(act_goal)
            overlap = act_keywords.intersection(self._extract_keywords(last_text))
            if not overlap:
                findings.append({
                    "level": "warning",
                    "code": "ACT_OUTCOME_UNRESOLVED",
                    "message": f"收尾页未能与目标行动决策 '{act_goal[:20]}...' 形成强闭环。"
                })
                score -= 10

        score = max(0.0, min(100.0, score))
        return score, findings
