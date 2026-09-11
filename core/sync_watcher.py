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
            "details": diff_details
        }
