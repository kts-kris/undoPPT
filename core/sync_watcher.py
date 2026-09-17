"""sync_watcher.py - Millisecond Fingerprinting & Semantic AST Diff Watcher.

Monitors output deliverables (PPTX and HTML) for user external modifications.
When called at the beginning of each turn:
  1. Fast Fingerprint (SHA-256 + mtime) Check (<10ms).
  2. If modified: Runs semantic AST diff on slides, shapes, and texts.
  3. Generates human-friendly proactive modification summaries for the agent.
  4. Updates the local sync state cache in .undoppt/sync_state.json.
"""

import hashlib
import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

from pptx import Presentation


def compute_file_hash(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def extract_pptx_snapshot(pptx_path: str) -> Dict[str, Any]:
    """Extract a lightweight AST snapshot of slides, titles, and text contents."""
    if not os.path.exists(pptx_path):
        return {}

    prs = Presentation(pptx_path)
    slides_data = []

    for idx, slide in enumerate(prs.slides):
        texts = []
        titles = []
        shape_count = len(slide.shapes)

        for shape in slide.shapes:
            if shape.has_text_frame:
                frame_text = " ".join([p.text.strip() for p in shape.text_frame.paragraphs if p.text.strip()])
                if frame_text:
                    texts.append(frame_text)
                    # Infer title
                    if len(shape.text_frame.paragraphs) > 0:
                        first_p = shape.text_frame.paragraphs[0]
                        if first_p.runs and any(r.font.size and r.font.size.pt >= 24 for r in first_p.runs):
                            titles.append(frame_text)

        slide_title = titles[0] if titles else (texts[0] if texts else f"幻灯片 {idx+1}")
        slides_data.append({
            "slide_index": idx + 1,
            "title": slide_title,
            "shape_count": shape_count,
            "texts": texts
        })

    return {
        "slide_count": len(prs.slides),
        "slides": slides_data
    }


def diff_pptx_snapshots(old_snap: Dict[str, Any], new_snap: Dict[str, Any]) -> List[str]:
    """Generate human-readable modification descriptions by comparing two PPTX snapshots."""
    changes = []
    old_slides = old_snap.get("slides", [])
    new_slides = new_snap.get("slides", [])

    old_count = old_snap.get("slide_count", 0)
    new_count = new_snap.get("slide_count", 0)

    if old_count != new_count:
        changes.append(f"幻灯片总页数从 {old_count} 页变更为 {new_count} 页")

    # Compare matching slide indices
    min_len = min(len(old_slides), len(new_slides))
    for i in range(min_len):
        s_old = old_slides[i]
        s_new = new_slides[i]
        page_num = i + 1

        # Check title changes
        if s_old.get("title") != s_new.get("title"):
            changes.append(
                f"第 {page_num} 页标题被微调：由「{s_old.get('title')[:25]}」修改为「{s_new.get('title')[:25]}」"
            )

        # Check shape count change
        old_shapes = s_old.get("shape_count", 0)
        new_shapes = s_new.get("shape_count", 0)
        if old_shapes != new_shapes:
            diff_num = abs(new_shapes - old_shapes)
            action = "增加" if new_shapes > old_shapes else "删减"
            changes.append(f"第 {page_num} 页版面元素发生微调（{action}了 {diff_num} 个模块/形状）")

        # Check text content modifications
        old_text_set = set(s_old.get("texts", []))
        new_text_set = set(s_new.get("texts", []))
        added_texts = new_text_set - old_text_set
        removed_texts = old_text_set - new_text_set

        if added_texts or removed_texts:
            if added_texts and not any("标题" in c for c in changes if f"第 {page_num} 页" in c):
                sample = list(added_texts)[0][:30]
                changes.append(f"第 {page_num} 页文案内容更新（新增或修改了关键描述：「{sample}...」）")

    return changes


def analyze_intent_diff(old_data: Any, new_data: Any) -> Dict[str, Any]:
    """Semantic Intent Reflection Engine (EPIC-06).

    Analyzes fine-grained modifications between two versions of slides (blueprint or PPTX AST)
    and infers the underlying strategic intent of the human expert.
    """
    import re

    def _extract_slides(data: Any) -> List[Dict[str, Any]]:
        if isinstance(data, dict):
            return data.get("slides", [])
        elif isinstance(data, list):
            return data
        return []

    old_slides = _extract_slides(old_data)
    new_slides = _extract_slides(new_data)

    modifications = []
    intent_breakdown = []

    # 1. Slide count evolution
    if len(old_slides) != len(new_slides):
        if len(new_slides) < len(old_slides):
            diff_count = len(old_slides) - len(new_slides)
            modifications.append(f"幻灯片总页数精简了 {diff_count} 页")
            intent_breakdown.append({
                "dimension": "叙事篇幅与节奏",
                "observation": f"删减了 {diff_count} 页内容",
                "deduction": "人类意图：极度压缩沟通成本，聚焦核心冲突与破局点，做认知减法。"
            })
        else:
            diff_count = len(new_slides) - len(old_slides)
            modifications.append(f"幻灯片总页数扩充了 {diff_count} 页")
            intent_breakdown.append({
                "dimension": "叙事篇幅与节奏",
                "observation": f"新增了 {diff_count} 页论据/支撑内容",
                "deduction": "人类意图：强化逻辑链条的完整性与防御纵深，提供更详尽的实证闭环。"
            })

    # 2. Per-slide granular analysis
    min_len = min(len(old_slides), len(new_slides))
    aggressive_metrics_count = 0
    conservative_metrics_count = 0
    streamlined_shapes_count = 0
    expanded_shapes_count = 0

    for i in range(min_len):
        s_old = old_slides[i]
        s_new = new_slides[i]
        page = i + 1

        # Title analysis
        old_title = str(s_old.get("action_title") or s_old.get("title", ""))
        new_title = str(s_new.get("action_title") or s_new.get("title", ""))
        if old_title and new_title and old_title != new_title:
            modifications.append(f"第 {page} 页标题调整：「{old_title[:20]}」➔「{new_title[:20]}」")
            bold_kw = ["下一代", "突破", "全面", "极致", "颠覆", "自主", "自研", "自适应", "领先", "壁垒"]
            safe_kw = ["稳健", "平滑", "保底", "敏捷", "渐进", "可行", "合规", "成本"]
            if any(k in new_title for k in bold_kw) and not any(k in old_title for k in bold_kw):
                intent_breakdown.append({
                    "dimension": "战略语态",
                    "observation": f"第 {page} 页标题引入强攻坚词汇「{new_title}」",
                    "deduction": "人类意图：拔高汇报站位与攻坚破局感，向决策层展示技术自主性与代际领导力。"
                })
            elif any(k in new_title for k in safe_kw) and not any(k in old_title for k in safe_kw):
                intent_breakdown.append({
                    "dimension": "战略语态",
                    "observation": f"第 {page} 页标题倾向务实落地词汇「{new_title}」",
                    "deduction": "人类意图：缓解决策层对激进变迁的风险顾虑，强调平滑演进与安全着陆。"
                })

        # Metric changes
        old_texts = " ".join([str(t) for t in s_old.get("texts", [])] + [str(m.get("value", "")) for m in s_old.get("metrics", []) if isinstance(m, dict)])
        new_texts = " ".join([str(t) for t in s_new.get("texts", [])] + [str(m.get("value", "")) for m in s_new.get("metrics", []) if isinstance(m, dict)])

        old_pcts = [float(p) for p in re.findall(r"([0-9]+(?:\.[0-9]+)?)\s*%", old_texts)]
        new_pcts = [float(p) for p in re.findall(r"([0-9]+(?:\.[0-9]+)?)\s*%", new_texts)]
        if old_pcts and new_pcts:
            if max(new_pcts) > max(old_pcts):
                aggressive_metrics_count += 1
                modifications.append(f"第 {page} 页量化指标拔高（最高百分比由 {max(old_pcts)}% 提升至 {max(new_pcts)}%）")
            elif max(new_pcts) < max(old_pcts):
                conservative_metrics_count += 1
                modifications.append(f"第 {page} 页量化指标回调（最高百分比由 {max(old_pcts)}% 调整为 {max(new_pcts)}%）")

        # Check shape / card count changes
        old_cards = len(s_old.get("cards", [])) or len(s_old.get("layers", [])) or s_old.get("shape_count", 0)
        new_cards = len(s_new.get("cards", [])) or len(s_new.get("layers", [])) or s_new.get("shape_count", 0)
        if old_cards and new_cards:
            if new_cards < old_cards:
                streamlined_shapes_count += (old_cards - new_cards)
            elif new_cards > old_cards:
                expanded_shapes_count += (new_cards - old_cards)

    if aggressive_metrics_count > 0:
        intent_breakdown.append({
            "dimension": "指标激进化",
            "observation": f"在 {aggressive_metrics_count} 处关键指标上调了量化承诺",
            "deduction": "人类意图：主动加压拉大与竞品/现状的代际差距，塑造极具说服力的必赢心智。"
        })
    elif conservative_metrics_count > 0:
        intent_breakdown.append({
            "dimension": "指标务实化",
            "observation": f"在 {conservative_metrics_count} 处关键指标回调至更严谨区间",
            "deduction": "人类意图：恪守真实性底线，规避汇报被质疑数据虚标的合规风险。"
        })

    if streamlined_shapes_count > 0:
        intent_breakdown.append({
            "dimension": "模块删繁就简",
            "observation": f"累计删减了 {streamlined_shapes_count} 个版面卡片/架构层级",
            "deduction": "人类意图：剥离冗余次要分支，凸显绝对主干与核心护城河。"
        })
    elif expanded_shapes_count > 0:
        intent_breakdown.append({
            "dimension": "维度补充拓展",
            "observation": f"累计补充了 {expanded_shapes_count} 个架构模块或对比维度",
            "deduction": "人类意图：补齐盲区，增强技术闭环与评委答辩防守覆盖面。"
        })

    # Synthesize strategic intent statement
    if not intent_breakdown:
        strategic_intent = "人类专家在本地进行了版面与排版细节的微调优化，整体战略主旨与推演逻辑保持稳定同频。"
        suggested_posture = "保持当前战略主线，在后续轮次中无缝承接人类专家的微调细节。"
    else:
        deductions_summary = "；".join([item["deduction"].replace("人类意图：", "") for item in intent_breakdown])
        strategic_intent = f"检测到人类专家深层战略意图调整：{deductions_summary}"
        if aggressive_metrics_count > 0 or any("攻坚" in item.get("deduction", "") for item in intent_breakdown):
            suggested_posture = "激进化配合：后续生成中进一步强化硬核壁垒与突破性论证，同步提升口播应对的自信度。"
        elif conservative_metrics_count > 0 or any("务实" in item.get("deduction", "") for item in intent_breakdown):
            suggested_posture = "严谨化配合：后续生成中加强落地步骤、容灾兜底与回滚机制的实证细节。"
        else:
            suggested_posture = "紧密对齐：吸纳人类专家的结构调整，在后续演练中保持聚焦。"

    return {
        "detected_modifications": modifications,
        "strategic_intent": strategic_intent,
        "intent_breakdown": intent_breakdown,
        "suggested_agent_posture": suggested_posture
    }


class SyncWatcher:
    """Proactive File Change & Intent Synchronization Watcher."""

    def __init__(self, state_file: str = ".undoppt/sync_state.json"):
        self.state_file = state_file
        os.makedirs(os.path.dirname(os.path.abspath(state_file)), exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_state(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def record_baseline(self, filepath: str):
        """Record the initial state of a delivered file."""
        if not os.path.exists(filepath):
            return

        f_hash = compute_file_hash(filepath)
        mtime = os.path.getmtime(filepath)
        snapshot = extract_pptx_snapshot(filepath) if filepath.endswith(".pptx") else {}

        self.state[filepath] = {
            "hash": f_hash,
            "mtime": mtime,
            "snapshot": snapshot,
            "last_synced": time.time()
        }
        self._save_state()

    def analyze_intent_diff(self, old_data: Any, new_data: Any) -> Dict[str, Any]:
        """Expose analyze_intent_diff via SyncWatcher instance."""
        return analyze_intent_diff(old_data, new_data)

    def check_sync(self, filepath: str) -> Dict[str, Any]:
        """Check whether the user has externally modified the file, and return diff summary."""
        if not os.path.exists(filepath):
            return {"exists": False, "changed": False, "message": "File does not exist."}

        curr_hash = compute_file_hash(filepath)
        curr_mtime = os.path.getmtime(filepath)
        prev_data = self.state.get(filepath)

        if not prev_data:
            # First time seeing this file, record baseline
            self.record_baseline(filepath)
            return {"exists": True, "changed": False, "message": "Initial baseline established."}

        # Fast Fingerprint Check
        if prev_data.get("hash") == curr_hash:
            return {"exists": True, "changed": False, "message": "In sync. No modifications detected."}

        # User modified the file! Run semantic diff
        new_snapshot = extract_pptx_snapshot(filepath) if filepath.endswith(".pptx") else {}
        old_snapshot = prev_data.get("snapshot", {})

        diff_details = diff_pptx_snapshots(old_snapshot, new_snapshot) if old_snapshot and new_snapshot else ["文件二进制内容已在本地被更新。"]
        intent_reflection = self.analyze_intent_diff(old_snapshot, new_snapshot)

        # Update sync state to the new modified version
        self.state[filepath] = {
            "hash": curr_hash,
            "mtime": curr_mtime,
            "snapshot": new_snapshot,
            "last_synced": time.time()
        }
        self._save_state()

        summary_text = "；".join(diff_details) if diff_details else "检测到用户在本地微调了文件。"
        return {
            "exists": True,
            "changed": True,
            "summary": summary_text,
            "details": diff_details,
            "intent_reflection": intent_reflection
        }
