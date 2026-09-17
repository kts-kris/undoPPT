"""test_engine.py - Automated Unit & Regression Tests for undoPPT Engine.
"""

import json
import os
import shutil
import tempfile
import unittest

from pptx import Presentation

from core.cognitive_planner import CognitivePlanner
from core.content_auditor import ContentAuditor
from core.html_builder import build_standalone_html
from core.pptx_builder import build_presentation
from core.sync_watcher import SyncWatcher, compute_file_hash, analyze_intent_diff
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
                "layout_type": "matrix_2x2",
                "title": "象限决策矩阵",
                "quadrants": [
                    {"name": "生态协作", "strategy": "联合研发", "items": ["外部模型"]},
                    {"name": "平台主导", "strategy": "标准制定", "items": ["行业规范"]},
                    {"name": "差异聚焦", "strategy": "局部深耕", "items": ["定制算法"]},
                    {"name": "核心整合", "strategy": "全链穿透", "items": ["自研资产"], "highlight": True}
                ],
                "principles": ["原则1", "原则2"]
            },
            {
                "layout_type": "maturity_ladder",
                "title": "四级能力阶梯",
                "levels": [
                    {"level": "L1", "name": "访问", "mechanism": "开通", "metric": "覆盖率"},
                    {"level": "L2", "name": "使用", "mechanism": "考评", "metric": "活跃度"},
                    {"level": "L3", "name": "常态", "mechanism": "模板", "metric": "复用率"},
                    {"level": "L4", "name": "结果", "mechanism": "账本", "metric": "净收益", "highlight": True}
                ],
                "safety_line": "全流程安全合规"
            },
            {
                "layout_type": "horizons_curve",
                "title": "三道地平线治理",
                "summary_card": "分池独立考核",
                "horizons": [
                    {"id": "H1", "title": "核心效率", "focus": ["问答", "审核"], "governance": "标准化", "metric": "现金节省"},
                    {"id": "H2", "title": "成长重构", "focus": ["排产", "预测"], "governance": "敏捷", "metric": "北极星改善"},
                    {"id": "H3", "title": "新兴模式", "focus": ["数据服务"], "governance": "孵化", "metric": "PMF验证"}
                ]
            },
            {
                "layout_type": "cross_mapping",
                "title": "四层穿透映射",
                "rows": [
                    {"tier": "01 决策", "source_role": "顶层定调", "target_role": "集团战略委"},
                    {"tier": "02 统筹", "source_role": "协同中枢", "target_role": "业务技术中枢"}
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

    def test_cognitive_planner_generation(self):
        """Test CognitivePlanner synthesizes an audited blueprint from a prompt."""
        planner = CognitivePlanner()
        bp = planner.plan("智能制造数字化战略规划")
        self.assertIn("contract", bp)
        self.assertIn("core_thesis", bp["contract"])
        self.assertGreaterEqual(len(bp["slides"]), 5)
        self.assertGreaterEqual(bp["audit_summary"]["score"], 70)

        # Test dual build of the planner output
        out_pptx = os.path.join(self.test_dir, "planner_test.pptx")
        out_html = os.path.join(self.test_dir, "planner_test.html")
        build_presentation(bp, self.sample_tokens, out_pptx)
        build_standalone_html(bp, self.sample_tokens, out_html)
        self.assertTrue(os.path.exists(out_pptx))
        self.assertTrue(os.path.exists(out_html))

    def test_semantic_auditor_metrics(self):
        """Test SemanticAuditor evaluates causal cohesion, thesis alignment, and evidence."""
        from core.semantic_auditor import SemanticAuditor
        auditor = SemanticAuditor()
        contract = {
            "core_thesis": "从应用规模表象全面迈向以经营结果为导向的企业级AI系统性重构与闭环",
            "knowledge_delta": {"blindspots_and_pains": ["400+智能体闲置", "数据断点"]},
            "target_outcomes": {"act": "当场决议批准成立四层协同组织"}
        }
        slides = [
            {"layout_type": "cover", "title": "企业级AI战略规划", "narrative_arc": "hook"},
            {
                "layout_type": "bento_cards",
                "narrative_arc": "conflict",
                "transition": "【冲突】然而 400+ 智能体中长尾闲置高达 80%",
                "action_title": "痛点：400+智能体闲置，数据断点严重",
                "core_evidence": "长尾闲置占比高达 80%，投入产出比脱节",
                "title": "现状分析与冲突痛点"
            },
            {
                "layout_type": "summary",
                "narrative_arc": "call_to_action",
                "transition": "【决议】因此当场决议批准成立四层协同组织，重构 4:3:3 投资结构",
                "action_title": "决议：当场决议批准成立四层协同组织",
                "core_evidence": "重构 4:3:3 投资结构，预计回收期缩减至 12个月",
                "title": "收官决议",
                "points": [{"title": "批准成立四层协同组织", "desc": "全面闭环"}]
            }
        ]
        res = auditor.audit_semantics(contract, slides)
        self.assertIn("semantic_score", res)
        self.assertGreaterEqual(res["semantic_score"], 80.0)
        self.assertIn("causal_cohesion", res["subscores"])
        self.assertIn("thesis_alignment", res["subscores"])
        self.assertIn("evidence_weight", res["subscores"])
        self.assertIn("skepticism_defense", res["subscores"])

    def test_document_context_ingestion(self):
        """Test DocumentContextIngestor extracts numbers, pains, actions, and entities."""
        from core.cognitive_planner import DocumentContextIngestor
        ingestor = DocumentContextIngestor()
        doc_content = """
        # 某制造集团智能化转型复盘
        痛点：当前存在 418个智能体，但真正高频使用的仅 71个，长尾闲置高达 80%。
        现状：传统投资结构为 7:2:1，导致底层数据治理严重滞后。
        建议：当场决议将投资结构重构为 4:3:3，并在 18个月内完成三大旗舰战役打穿。
        """
        data = ingestor.ingest(doc_content)
        self.assertIn("418个", data["numbers"])
        self.assertIn("80%", data["numbers"])
        self.assertIn("4:3:3", data["numbers"])
        self.assertIn("某制造集团", data["entity_mentions"])
        self.assertGreaterEqual(len(data["extracted_pains"]), 1)
        self.assertGreaterEqual(len(data["extracted_actions"]), 1)

    def test_grounded_planner_with_document_and_refinement(self):
        """Test CognitivePlanner grounds blueprint in document context and performs self-refinement."""
        planner = CognitivePlanner()
        sample_doc = os.path.join(self.test_dir, "sample_doc.md")
        with open(sample_doc, "w", encoding="utf-8") as f:
            f.write("某制造集团数字化战略：418个智能体中 80% 闲置。决议重构 4:3:3 预算，立项制造与供应链战役。")

        bp = planner.plan("我要编写某制造集团的AI战略", doc_path=sample_doc, auto_refine=True)
        self.assertTrue(bp["grounded_sources"]["has_doc"])
        self.assertGreaterEqual(bp["grounded_sources"]["extracted_numbers_count"], 1)
        self.assertGreaterEqual(bp["audit_summary"]["score"], 85)
        self.assertIn(bp["version"], ("3.1.0", "3.4.0"))

    def test_undo_engine_master_slots_and_theme_mode(self):
        """Test undo_engine extracts master slots geometry and theme mode."""
        out_pptx = os.path.join(self.test_dir, "slots_test.pptx")
        build_presentation(self.sample_blueprint, self.sample_tokens, out_pptx)

        tokens = extract_template_tokens(out_pptx, extract_assets=True, assets_dir=os.path.join(self.test_dir, "assets"))
        self.assertIn("master_slots", tokens)
        self.assertIn("theme_mode", tokens)
        self.assertIn(tokens["theme_mode"], ["light", "dark"])
        self.assertGreater(tokens["master_layouts_count"], 0)
        self.assertIn("slots", tokens["layouts"][0])

    def test_career_resume_planner(self):
        """Test CognitivePlanner synthesizes and audits a personal resume / career portfolio deck."""
        planner = CognitivePlanner()
        bp = planner.plan("帮我生成一份资深全栈架构师的个人简历")
        self.assertEqual(bp["scenario"], "career_portfolio")
        self.assertIn("架构", bp["contract"]["core_thesis"])
        self.assertIn("架构师", bp["slides"][0]["title"])
        self.assertGreaterEqual(bp["audit_summary"]["score"], 85)

        # Verify layout mix for career portfolio
        layouts = [s["layout_type"] for s in bp["slides"]]
        self.assertIn("cover", layouts)
        self.assertIn("bento_cards", layouts)
        self.assertIn("content_columns", layouts)
        self.assertIn("metric_spotlight", layouts)
        self.assertIn("timeline", layouts)
        self.assertIn("summary", layouts)

        # Verify dual build works for resume blueprint
        out_pptx = os.path.join(self.test_dir, "resume_test.pptx")
        out_html = os.path.join(self.test_dir, "resume_test.html")
        build_presentation(bp, self.sample_tokens, out_pptx)
        build_standalone_html(bp, self.sample_tokens, out_html)
        self.assertTrue(os.path.exists(out_pptx))
        self.assertTrue(os.path.exists(out_html))

    def test_all_15_layouts_render(self):
        """Test PPTX and HTML builders render all 15 layout primitives cleanly."""
        all_15_blueprint = [
            {"layout_type": "cover", "title": "P1 封面", "subtitle": "全图元演练", "category": "TEST"},
            {"layout_type": "architecture_stack", "title": "P2 架构栈", "layers": [{"name": "层1", "items": ["组件A"]}]},
            {"layout_type": "bento_cards", "title": "P3 Bento卡片", "cards": [{"title": "卡片1", "desc": "说明"}]},
            {"layout_type": "metric_spotlight", "title": "P4 指标", "metrics": [{"label": "达成率", "value": "99%"}]},
            {"layout_type": "timeline", "title": "P5 时间轴", "steps": [{"time": "2026", "title": "节点", "items": ["完成"]}]},
            {"layout_type": "matrix_2x2", "title": "P6 矩阵", "quadrants": [{"name": "象限A", "desc": "描述"}], "axes": {"x": "X", "y": "Y"}},
            {"layout_type": "maturity_ladder", "title": "P7 阶梯", "levels": [{"step": "L1", "name": "起步", "target": "标"}]},
            {"layout_type": "horizons_curve", "title": "P8 地平线", "horizons": [{"horizon": "H1", "name": "基准", "focus": "核心"}]},
            {"layout_type": "cross_mapping", "title": "P9 映射", "rows": [{"tier": "01", "source_role": "A", "target_role": "B"}]},
            {"layout_type": "summary", "title": "P10 总结", "points": [{"title": "要点", "desc": "建议"}]},
            {"layout_type": "standard_table", "title": "P11 表格", "headers": ["A", "B", "C"], "rows": [["1", "2", "3"], ["4", "5", "6"]]},
            {"layout_type": "data_chart", "title": "P12 图表", "chart_type": "column_clustered", "categories": ["Q1", "Q2"], "series": [{"name": "收入", "values": [10, 20]}]},
            {"layout_type": "content_columns", "title": "P13 并列栏", "columns": [{"title": "栏1", "points": ["点1", "点2"]}]},
            {"layout_type": "keynote_quote", "title": "P14 金句", "quote_text": "博观而约取，厚积而薄发", "author": "苏轼", "key_takeaway": "深度思考"},
            {"layout_type": "process_flow", "title": "P15 流程", "steps": [{"step": "01", "name": "立项", "desc": "确立契约"}, {"step": "02", "name": "构建", "desc": "交付产物"}]}
        ]
        out_pptx = os.path.join(self.test_dir, "all_15.pptx")
        out_html = os.path.join(self.test_dir, "all_15.html")
        build_presentation(all_15_blueprint, self.sample_tokens, out_pptx)
        build_standalone_html(all_15_blueprint, self.sample_tokens, out_html)

        self.assertTrue(os.path.exists(out_pptx))
        self.assertTrue(os.path.exists(out_html))

        prs = Presentation(out_pptx)
        self.assertEqual(len(prs.slides), 15)

        # Verify table shape exists on slide 11 (index 10)
        table_slide = prs.slides[10]
        has_table = any(s.has_table for s in table_slide.shapes)
        self.assertTrue(has_table, "Slide 11 should contain a native PowerPoint table shape")

        # Verify chart shape exists on slide 12 (index 11)
        chart_slide = prs.slides[11]
        has_chart = any(s.has_chart for s in chart_slide.shapes)
        self.assertTrue(has_chart, "Slide 12 should contain a native PowerPoint chart shape")

    def test_education_training_planner(self):
        """Test CognitivePlanner synthesizes an education/pedagogical presentation with zero tech jargon."""
        planner = CognitivePlanner()
        bp = planner.plan("小学语文识字教学公开课")
        self.assertEqual(bp["scenario"], "education_training")
        self.assertIn("教学", bp["contract"]["core_thesis"])
        self.assertGreaterEqual(bp["audit_summary"]["score"], 70)

        # Verify that tech jargon is NOT present
        bp_json_str = json.dumps(bp, ensure_ascii=False)
        self.assertNotIn("CTO", bp_json_str)
        self.assertNotIn("微服务", bp_json_str)
        self.assertNotIn("高并发", bp_json_str)
        self.assertNotIn("全栈架构师", bp_json_str)

        # Verify build succeeds
        out_pptx = os.path.join(self.test_dir, "edu_test.pptx")
        out_html = os.path.join(self.test_dir, "edu_test.html")
        build_presentation(bp, self.sample_tokens, out_pptx)
        build_standalone_html(bp, self.sample_tokens, out_html)
        self.assertTrue(os.path.exists(out_pptx))
        self.assertTrue(os.path.exists(out_html))

    def test_anti_buzzword_and_scenario_redlines(self):
        """Test ContentAuditor intercepts prohibited AI buzzwords and invalid transitions."""
        auditor = ContentAuditor()
        bad_bp = {
            "slides": [
                {
                    "layout_type": "bento_cards",
                    "action_title": "不仅是技术创新，更是战略打法与闭环",
                    "mission": "说明为什么凭什么怎么做",
                    "cards": [{"title": "抓手", "desc": "赋能业务底层逻辑，盘活颗粒度"}]
                }
            ]
        }
        res = auditor.audit(bad_bp)
        codes = [f["code"] for f in res["findings"]]
        self.assertTrue(any("BUZZWORD_DETECTED" in c for c in codes), "Should detect buzzwords")

    def test_slide_transitions_and_motion(self):
        """Test slide transitions are properly injected in PPTX and step mode is in HTML."""
        bp = {
            "presentation_config": {
                "transition_effect": "fade"
            },
            "slides": [
                {
                    "layout_type": "bento_cards",
                    "title": "测试过渡",
                    "transition_effect": "push",
                    "cards": [{"title": "卡片1", "desc": "内容1"}, {"title": "卡片2", "desc": "内容2"}]
                }
            ]
        }
        out_pptx = os.path.join(self.test_dir, "trans_test.pptx")
        out_html = os.path.join(self.test_dir, "trans_test.html")
        build_presentation(bp, self.sample_tokens, out_pptx)
        build_standalone_html(bp, self.sample_tokens, out_html)

        self.assertTrue(os.path.exists(out_pptx))
        self.assertTrue(os.path.exists(out_html))

        # Check PPTX contains transition in slide XML
        prs = Presentation(out_pptx)
        slide_elm = prs.slides[0]._element
        has_trans = any(child.tag.endswith("transition") for child in slide_elm)
        self.assertTrue(has_trans, "Slide should contain a transition element in OOXML")

        # Check HTML contains step-btn and staged classes
        with open(out_html, "r", encoding="utf-8") as f:
            html_text = f.read()
        self.assertIn("step-btn", html_text)
        self.assertIn("staged-hidden", html_text)

    def test_pptx_ooxml_timing_sequence(self):
        """Test standard ECMA-376 OOXML <p:timing> generation in PPTX (EPIC-01 & EPIC-02)."""
        bp = {
            "presentation_config": {
                "transition_effect": "fade",
                "motion_pace": "staged"
            },
            "slides": [
                {"layout_type": "cover", "title": "Cover Slide"},
                {
                    "layout_type": "bento_cards",
                    "title": "Bento Analysis",
                    "narrative_arc": "conflict",
                    "cards": [
                        {"title": "方案 A", "desc": "痛点说明"},
                        {"title": "方案 B", "desc": "瓶颈说明"}
                    ]
                },
                {
                    "layout_type": "architecture_stack",
                    "title": "Tech Architecture",
                    "narrative_arc": "breakthrough",
                    "layers": [
                        {"name": "网关层", "items": ["API 网关"]},
                        {"name": "业务层", "items": ["调度引擎"]}
                    ]
                }
            ]
        }
        out_pptx = os.path.join(self.test_dir, "timing_test.pptx")
        build_presentation(bp, self.sample_tokens, out_pptx)
        self.assertTrue(os.path.exists(out_pptx))

        prs = Presentation(out_pptx)
        self.assertEqual(len(prs.slides), 3)

        # Slide 0 (cover) should not have timing sequence
        slide0_tags = [c.tag.split("}")[-1] for c in prs.slides[0]._element]
        self.assertNotIn("timing", slide0_tags)

        # Slide 1 and Slide 2 should have valid OOXML timing node
        slide1_tags = [c.tag.split("}")[-1] for c in prs.slides[1]._element]
        self.assertIn("timing", slide1_tags)
        slide2_tags = [c.tag.split("}")[-1] for c in prs.slides[2]._element]
        self.assertIn("timing", slide2_tags)

        # Test instant motion_pace disables timing
        bp_instant = dict(bp)
        bp_instant["presentation_config"] = {"motion_pace": "instant"}
        out_instant = os.path.join(self.test_dir, "instant_test.pptx")
        build_presentation(bp_instant, self.sample_tokens, out_instant)
        prs_instant = Presentation(out_instant)
        slide1_instant_tags = [c.tag.split("}")[-1] for c in prs_instant.slides[1]._element]
        self.assertNotIn("timing", slide1_instant_tags)

    def test_html_presenter_hud_and_sandbox(self):
        """Test Live Presenter HUD (P key) and Active Decision Sandbox in HTML (EPIC-04 & EPIC-05)."""
        bp = {
            "contract": {
                "core_thesis": "架构驱动业务百倍增长",
                "audience": {"role": "技术评委会", "stance": "严苛审视SLA与成本"}
            },
            "slides": [
                {
                    "layout_type": "architecture_stack",
                    "title": "分布式微服务架构",
                    "mission": "证明系统高可用",
                    "transition": "【承接】由此可见基础设施稳固，接下来看性能数据",
                    "layers": [{"name": "路由层", "items": ["Envoy", "Traefik"]}]
                },
                {
                    "layout_type": "metric_spotlight",
                    "title": "核心效能大字报",
                    "mission": "用实测数据证明吞吐达标",
                    "transition": "【号召】建议立即启动立项",
                    "core_evidence": "P99 < 5ms, 99.999% 可用性",
                    "metrics": [
                        {"label": "可用性", "value": "99.99%", "delta": "+0.8%"},
                        {"label": "QPS", "value": "50000", "delta": "+40%"}
                    ],
                    "sandbox": {
                        "enabled": True,
                        "scenarios": {
                            "conservative": {"metrics": [{"value": "99.9%"}, {"value": "35000"}]},
                            "aggressive": {"metrics": [{"value": "99.999%"}, {"value": "80000"}]}
                        }
                    },
                    "hud_notes": {
                        "objection_defense": [
                            {"skepticism": "如何保障极端断网下的数据一致性？", "counter": "依靠 Raft 共识协议与本地事务回滚日志"}
                        ]
                    }
                }
            ]
        }
        out_html = os.path.join(self.test_dir, "hud_sandbox_test.html")
        build_standalone_html(bp, self.sample_tokens, out_html)
        self.assertTrue(os.path.exists(out_html))

        with open(out_html, "r", encoding="utf-8") as f:
            html_text = f.read()

        # Presenter HUD markup & shortcut checks
        self.assertIn("presenter-hud", html_text)
        self.assertIn("hud-btn", html_text)
        self.assertIn("架构驱动业务百倍增长", html_text)
        self.assertIn("技术评委会", html_text)
        self.assertIn("如何保障极端断网下的数据一致性？", html_text)
        self.assertIn("Raft 共识协议", html_text)

        # Active Decision Sandbox checks
        self.assertIn("scenario-sandbox", html_text)
        self.assertIn("data-conservative-val=\"99.9%\"", html_text)
        self.assertIn("data-aggressive-val=\"99.999%\"", html_text)

        # Architecture drilldown modal check
        self.assertIn("arch-drilldown-modal", html_text)
        self.assertIn("architecture-item", html_text)

    def test_sync_watcher_intent_reflection(self):
        """Test SyncWatcher semantic intent reflection engine (EPIC-06)."""
        old_blueprint = {
            "slides": [
                {"title": "旧方案架构体系", "cards": [{"title": "C1"}, {"title": "C2"}, {"title": "C3"}]},
                {"title": "性能初测", "metrics": [{"label": "SLA", "value": "95.0%"}]}
            ]
        }
        new_blueprint = {
            "slides": [
                {"title": "下一代自研突破架构", "cards": [{"title": "C1"}]},
                {"title": "极致性能承诺", "metrics": [{"label": "SLA", "value": "99.99%"}]}
            ]
        }

        res = analyze_intent_diff(old_blueprint, new_blueprint)
        self.assertIn("strategic_intent", res)
        self.assertIn("suggested_agent_posture", res)
        self.assertTrue(len(res["detected_modifications"]) >= 2)
        self.assertTrue(len(res["intent_breakdown"]) >= 2)
        self.assertIn("激进化", res["suggested_agent_posture"])

    def test_enterprise_12_scenarios_cognitive_planning(self):
        """Test CognitivePlanner accurately classifies, contracts, and synthesizes all 12 enterprise operational scenarios."""
        planner = CognitivePlanner()

        test_cases = [
            ("project_charter", "strategic_planning", "某重点创新业务立项答辩与投资评审"),
            ("annual_strategy_okr", "strategic_planning", "集团年度战略规划与 OKR 拆解大图"),
            ("qbr_business_review", "general_informative", "核心业务季度经营复盘 QBR 分析"),
            ("cross_team_alignment", "general_informative", "跨部门业务拉通与协同交付对齐"),
            ("team_headcount_review", "general_informative", "团队编制规划与财务人头预算答辩"),
            ("tech_rfc_review", "tech_architecture", "核心系统高可用架构选型 RFC 评审答辩"),
            ("post_mortem_review", "tech_architecture", "线上生产事故复盘与系统防呆治理"),
            ("product_launch_gtm", "product_pitch", "新产品上市策略与 GTM 全渠道推进计划"),
            ("enterprise_rfp_pitch", "product_pitch", "政企数字化大客户解决方案竞标答辩 RFP"),
            ("promotion_assessment", "career_portfolio", "资深技术专家职级晋升述职答辩"),
            ("internal_tech_talk", "education_training", "高并发微服务工程方法论内部技术培训"),
            ("all_hands_rally", "education_training", "公司年度战略誓师与全员动员大会")
        ]

        for expected_scenario, expected_archetype, prompt in test_cases:
            bp = planner.plan(prompt, auto_refine=True)
            self.assertEqual(bp["scenario"], expected_scenario, f"Failed for prompt: {prompt}")
            self.assertEqual(bp["archetype"], expected_archetype, f"Failed archetype for prompt: {prompt}")
            self.assertIn("contract", bp)
            self.assertIn("core_thesis", bp["contract"])
            self.assertEqual(len(bp["slides"]), 6, f"Expected 6 slides for scenario {expected_scenario}")
            self.assertGreaterEqual(bp["audit_summary"]["score"], 85, f"Low audit score for {expected_scenario}")

    def test_decision_ready_ask_dual_rendering(self):
        """Test Decision-Ready Ask options, recommendations, and sign-off checklists in PPTX and HTML."""
        bp = {
            "version": "3.4.0",
            "scenario": "project_charter",
            "archetype": "strategic_planning",
            "slides": [
                {
                    "layout_type": "cover",
                    "title": "项目立项答辩",
                    "subtitle": "投资决策与推进建议"
                },
                {
                    "layout_type": "summary",
                    "narrative_arc": "call_to_action",
                    "action_title": "决策决议：推荐全面启动方案 B 实施改造，明确三项资源审批",
                    "title": "方案比选与请领导决策事项",
                    "subtitle": "三大路径权衡、推荐结论与审批决议清单",
                    "options": [
                        {"name": "方案A: 维持现状打补丁", "pros": "零前期资本追加", "cons": "瓶颈恶化不可持续", "cost": "0 元", "risk": "高", "recommended": False},
                        {"name": "方案B: 试点立项演进 (推荐)", "pros": "投产比 1:4.5，周期可控", "cons": "需短期调配专班", "cost": "首期预算", "risk": "低", "recommended": True},
                        {"name": "方案C: 全新颠覆重构", "pros": "理论天花板最高", "cons": "周期长达18个月", "cost": "数百万追加", "risk": "极高", "recommended": False}
                    ],
                    "recommendation": "综合 ROI 与交付确定性，推荐采纳方案 B：试点立项演进，验证核心产出后再行释放后续资源。",
                    "sign_off_items": [
                        "1. 批准《方案实施立项申请》并划拨首期专用预算",
                        "2. 协调核心业务团队各指派 1 名专职研发骨干组建联合专班",
                        "3. 锁定 Q3 关键里程碑交付节点并建立双周调度机制"
                    ]
                }
            ]
        }

        # Test PPTX build
        out_pptx = os.path.join(self.test_dir, "decision_ask_test.pptx")
        build_presentation(bp, self.sample_tokens, out_pptx)
        self.assertTrue(os.path.exists(out_pptx))
        self.assertGreater(os.path.getsize(out_pptx), 1000)

        # Test HTML build
        out_html = os.path.join(self.test_dir, "decision_ask_test.html")
        build_standalone_html(bp, self.sample_tokens, out_html)
        self.assertTrue(os.path.exists(out_html))
        with open(out_html, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Check Decision Ask visual indicators in HTML
        self.assertIn("★ 推荐决策 RECOMMENDED", html_content)
        self.assertIn("💡 决策建议", html_content)
        self.assertIn("请领导决策与审批清单 (Sign-off Items)", html_content)
        self.assertIn('type="checkbox"', html_content)
        self.assertIn("批准《方案实施立项申请》并划拨首期专用预算", html_content)

    def test_enterprise_rigor_audit_rules(self):
        """Test ContentAuditor enforces DECISION_ASK_MISSING, BENCHMARK_UNBALANCED, and PROMOTION_LAUNDRY_LIST."""
        auditor = ContentAuditor()

        # 1. Test DECISION_ASK_MISSING in leadership deck
        bp_missing_ask = {
            "scenario": "project_charter",
            "slides": [
                {"layout_type": "cover", "title": "项目立项答辩"},
                {"layout_type": "summary", "title": "结论与总结", "action_title": "行动：持续推进项目后续落地", "mission": "总结全篇", "transition": "【总结】综上所述", "points": [{"title": "要点1", "desc": "描述1"}]}
            ]
        }
        res1 = auditor.audit(bp_missing_ask)
        codes1 = [f["code"] for f in res1["findings"]]
        self.assertIn("DECISION_ASK_MISSING", codes1)

        # 2. Test BENCHMARK_UNBALANCED in comparison table
        bp_unbalanced_table = {
            "scenario": "tech_rfc_review",
            "slides": [
                {"layout_type": "cover", "title": "技术架构选型"},
                {
                    "layout_type": "standard_table",
                    "title": "主流架构方案充分对标",
                    "action_title": "选型：我方方案全维度远超所有竞品方案",
                    "mission": "架构方案选型对标",
                    "transition": "【对标】与竞品进行全方位对比",
                    "headers": ["评估维度", "竞品A", "我方方案", "结论"],
                    "rows": [
                        ["性能表现", "差", "优", "我方胜出"],
                        ["可用性", "低", "高", "我方胜出"],
                        ["扩展性", "弱", "强", "我方胜出"]
                    ]
                },
                {"layout_type": "summary", "title": "审批事项", "options": [{"name": "B", "recommended": True}], "sign_off_items": ["批准立项"]}
            ]
        }
        res2 = auditor.audit(bp_unbalanced_table)
        codes2 = [f["code"] for f in res2["findings"]]
        self.assertTrue(any(c.startswith("BENCHMARK_UNBALANCED") for c in codes2))

        # 3. Test PROMOTION_LAUNDRY_LIST in career review
        bp_laundry_promo = {
            "scenario": "promotion_assessment",
            "slides": [
                {"layout_type": "cover", "title": "个人晋升述职"},
                {
                    "layout_type": "content_columns",
                    "title": "日常工作回顾",
                    "action_title": "工作：认真负责完成各项日常跟进与维护",
                    "mission": "阐明工作职责",
                    "transition": "【工作】在过去一年中完成各项日常",
                    "columns": [
                        {"tag": "任务", "title": "日常维护与跟进", "points": ["负责日常系统维护", "参与了需求评审", "协助完成各种琐碎测试"]}
                    ]
                }
            ]
        }
        res3 = auditor.audit(bp_laundry_promo)
        codes3 = [f["code"] for f in res3["findings"]]
        self.assertTrue(any(c.startswith("PROMOTION_LAUNDRY_LIST") for c in codes3))


if __name__ == "__main__":
    unittest.main()


