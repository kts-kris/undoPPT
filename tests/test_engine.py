"""test_engine.py - Automated Unit & Regression Tests for undoPPT Engine.
"""

import json
import os
import shutil
import tempfile
import unittest

from pptx import Presentation

from core.content_auditor import ContentAuditor
from core.html_builder import build_standalone_html
from core.pptx_builder import build_presentation
from core.sync_watcher import SyncWatcher, compute_file_hash
from core.undo_engine import extract_template_tokens, save_tokens
from core.vision_extractor import create_tokens_from_style_spec


class TestUndoPPTEngine(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sample_blueprint = [
            {
                "layout_type": "cover",
                "title": "测试封面标题",
                "subtitle": "测试副标题描述",
                "category": "TEST CATEGORY"
            },
            {
                "layout_type": "architecture_stack",
                "title": "架构测试层级",
                "subtitle": "层级化服务架构",
                "layers": [
                    {"name": "网关接入层", "items": ["API 网关", "认证中枢"]},
                    {"name": "核心计算层", "items": ["调度算法", "推理引擎"]}
                ]
            },
            {
                "layout_type": "bento_cards",
                "title": "多维对比分析",
                "cards": [
                    {"tag": "ITEM 1", "title": "方案 A", "desc": "描述 A", "bullets": ["要点 1", "要点 2"]},
                    {"tag": "ITEM 2", "title": "方案 B", "desc": "描述 B", "bullets": ["要点 3", "要点 4"]}
                ]
            },
            {
                "layout_type": "metric_spotlight",
                "title": "指标测试板",
                "metrics": [
                    {"label": "可用性", "value": "99.99%", "delta": "+0.5%", "desc": "全网平均"},
                    {"label": "延迟", "value": "<10ms", "desc": "端到端中位数"}
                ]
            },
            {
                "layout_type": "timeline",
                "title": "里程碑测试",
                "steps": [
                    {"time": "阶段 1", "title": "概念验证", "items": ["环境准备", "冒烟测试"]},
                    {"time": "阶段 2", "title": "上线试跑", "items": ["灰度发布", "全量推广"]}
                ]
            },
            {
                "layout_type": "summary",
                "title": "收官总结",
                "points": [
                    {"title": "结论 1", "desc": "这是第一个核心建议"},
                    {"title": "结论 2", "desc": "这是第二个核心建议"}
                ]
            }
        ]
        self.sample_tokens = create_tokens_from_style_spec()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_pptx_builder_generation(self):
        """Test PPTX builder produces a valid presentation with all 6 layouts."""
        out_pptx = os.path.join(self.test_dir, "test.pptx")
        res = build_presentation(self.sample_blueprint, self.sample_tokens, out_pptx)
        self.assertTrue(os.path.exists(res))
        self.assertGreater(os.path.getsize(res), 1000)

    def test_html_builder_generation(self):
        """Test HTML builder produces a standalone, self-contained HTML."""
        out_html = os.path.join(self.test_dir, "test.html")
        res = build_standalone_html(self.sample_blueprint, self.sample_tokens, out_html)
        self.assertTrue(os.path.exists(res))
        with open(res, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("测试封面标题", content)
            self.assertIn("架构测试层级", content)

    def test_undo_engine_deconstruction(self):
        """Test undo_engine can deconstruct a generated PPTX and extract tokens."""
        out_pptx = os.path.join(self.test_dir, "source.pptx")
        build_presentation(self.sample_blueprint, self.sample_tokens, out_pptx)

        tokens = extract_template_tokens(out_pptx)
        self.assertIn("canvas", tokens)
        self.assertIn("palette", tokens)
        self.assertIn("typography", tokens)
        self.assertEqual(tokens["canvas"]["aspect_ratio"], "16:9")

    def test_sync_watcher_change_detection(self):
        """Test sync_watcher detects file changes and generates diff summary."""
        state_file = os.path.join(self.test_dir, "sync_state.json")
        watcher = SyncWatcher(state_file=state_file)

        target_file = os.path.join(self.test_dir, "sync_test.pptx")
        build_presentation(self.sample_blueprint, self.sample_tokens, target_file)

        # 1. Initial baseline
        res1 = watcher.check_sync(target_file)
        self.assertFalse(res1["changed"])

        # 2. Simulate modification
        with open(target_file, "ab") as f:
            f.write(b"modified")

        # 3. Detect modification
        res2 = watcher.check_sync(target_file)
        self.assertTrue(res2["changed"])

    def test_content_auditor(self):
        """Test ContentAuditor evaluates cognitive metrics, contract, and budgets."""
        auditor = ContentAuditor(tokens=self.sample_tokens)
        structured_blueprint = {
            "contract": {
                "core_thesis": "全面推进智能体架构演进",
                "audience": {"role": "CTO", "stance": "严谨"},
                "knowledge_delta": {"blindspots_and_pains": ["成本过高"]},
                "target_outcomes": {"act": "批准预算"}
            },
            "slides": [
                {
                    "layout_type": "cover",
                    "narrative_arc": "hook",
                    "mission": "立论确立",
                    "title": "方案全景",
                    "subtitle": "副标题"
                },
                {
                    "layout_type": "bento_cards",
                    "narrative_arc": "conflict",
                    "mission": "指出核心矛盾",
                    "transition": "【冲突】然而现有系统已达极限",
                    "action_title": "痛点：传统方案维护成本过高",
                    "core_evidence": "成本节省 40%",
                    "cards": [
                        {"tag": "A", "title": "方案 A", "desc": "描述", "bullets": ["要点"]}
                    ]
                }
            ]
        }
        res = auditor.audit(structured_blueprint)
        self.assertTrue(res["passed"])
        self.assertGreaterEqual(res["score"], 80)
        self.assertIn("A", res["grade"])

    def test_cognitive_notes_pptx(self):
        """Test PPTX builder embeds mission and transition into speaker notes."""
        out_pptx = os.path.join(self.test_dir, "notes_test.pptx")
        bp = {
            "contract": {"core_thesis": "主旨论点", "target_outcomes": {"act": "立项"}},
            "slides": [
                {
                    "layout_type": "cover",
                    "narrative_arc": "hook",
                    "mission": "开门见山",
                    "title": "测试主旨",
                    "subtitle": "副标"
                },
                {
                    "layout_type": "summary",
                    "narrative_arc": "call_to_action",
                    "mission": "推动立即决策",
                    "transition": "【因此】建议启动执行",
                    "core_evidence": "实证数据充分",
                    "title": "决议建议",
                    "points": [{"title": "要点", "desc": "说明"}]
                }
            ]
        }
        build_presentation(bp, self.sample_tokens, out_pptx)
        prs = Presentation(out_pptx)
        self.assertEqual(len(prs.slides), 2)
        # Check slide 1 notes
        notes1 = prs.slides[0].notes_slide.notes_text_frame.text
        self.assertIn("【认知契约 / Cognitive Contract】", notes1)
        self.assertIn("【单页使命 / Mission】开门见山", notes1)

        # Check slide 2 notes
        notes2 = prs.slides[1].notes_slide.notes_text_frame.text
        self.assertIn("【承上启下 / Transition】", notes2)
        self.assertIn("推动立即决策", notes2)

    def test_cognitive_html_drawer(self):
        """Test HTML builder includes cognitive inspector drawer and attributes."""
        out_html = os.path.join(self.test_dir, "drawer_test.html")
        bp = [
            {
                "layout_type": "cover",
                "narrative_arc": "hook",
                "mission": "确立核心目标",
                "core_evidence": "行业领先指标",
                "title": "认知测试封面"
            }
        ]
        build_standalone_html(bp, self.sample_tokens, out_html)
        with open(out_html, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("cognitive-drawer", content)
            self.assertIn("data-mission=\"确立核心目标\"", content)
            self.assertIn("Notes (N)", content)


if __name__ == "__main__":
    unittest.main()
