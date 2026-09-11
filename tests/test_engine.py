"""test_engine.py - Automated Unit & Regression Tests for undoPPT Engine.
"""

import json
import os
import shutil
import tempfile
import unittest

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


if __name__ == "__main__":
    unittest.main()
