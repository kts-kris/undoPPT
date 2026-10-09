"""test_docs.py - the documentation must keep up with the code.

Between v3.5 and v3.8 four releases shipped with documentation that was incomplete or, in places, wrong:
new commands missing from the CLI reference, findings no document explained, whitepapers whose only change was
the version number. These tests make that kind of drift fail instead of go unnoticed.
"""

import glob
import os
import re
import unittest

from core import __version__

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def all_docs_text():
    paths = glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True)
    paths += [os.path.join(ROOT, p) for p in ("README.md", "README_zh.md", "SKILL.md", "CHANGELOG.md")]
    return "\n".join(open(p, encoding="utf-8").read() for p in paths)


class TestCommandsAreDocumented(unittest.TestCase):

    def test_every_cli_command_is_in_the_reference_the_readmes_and_the_skill(self):
        commands = re.findall(r'subparsers\.add_parser\("([a-z\-]+)"', read("cli.py"))
        self.assertGreaterEqual(len(commands), 11)
        for doc in ("docs/en/cli_reference.md", "docs/zh/cli_reference.md", "README.md", "README_zh.md", "SKILL.md"):
            text = read(doc)
            for cmd in commands:
                self.assertTrue(
                    f"cli.py {cmd}" in text or f'cli.py" {cmd}' in text or f"`{cmd}`" in text,
                    f"`{cmd}` is not documented in {doc}",
                )


class TestModulesAreDocumented(unittest.TestCase):

    def test_every_core_module_is_in_the_readmes_and_the_architecture_page(self):
        modules = [os.path.basename(p)[:-3] for p in glob.glob(os.path.join(ROOT, "core", "*.py"))
                   if not p.endswith("__init__.py")]
        self.assertGreaterEqual(len(modules), 15)
        for doc in ("README.md", "README_zh.md", "docs/en/architecture.md"):
            text = read(doc)
            for m in modules:
                self.assertIn(f"{m}.py", text, f"core/{m}.py is not described in {doc}")

    def test_every_test_file_is_listed_in_the_readmes_and_contributing(self):
        tests = [os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "tests", "test_*.py"))]
        for doc in ("README.md", "README_zh.md", "CONTRIBUTING.md"):
            text = read(doc)
            for t in tests:
                self.assertIn(t, text, f"tests/{t} is not listed in {doc}")


class TestFindingsAreExplained(unittest.TestCase):

    def test_every_audit_code_has_an_entry_in_audit_codes(self):
        src = read("core/content_auditor.py") + read("core/semantic_auditor.py")
        codes = set()
        for c in re.findall(r'"code":\s*f?"([A-Z][A-Z_]*[A-Z])(?:_P\{[a-z_]+\})?"', src):
            codes.add(c)
        self.assertGreaterEqual(len(codes), 40)
        for doc_path in ("docs/en/audit_codes.md", "docs/zh/audit_codes.md"):
            doc = read(doc_path)
            missing = sorted(c for c in codes if c not in doc)
            self.assertEqual(missing, [], f"audit codes with no entry in {doc_path}: {missing}")

    def test_every_lint_and_render_code_is_in_the_cli_reference(self):
        src = read("core/layout_lint.py") + read("core/render_check.py")
        codes = set(re.findall(r'"code":\s*"([A-Z_]+)"', src))
        self.assertIn("LOW_CONTRAST", codes)
        for doc_path in ("docs/en/cli_reference.md", "docs/zh/cli_reference.md"):
            doc = read(doc_path)
            missing = sorted(c for c in codes if c not in doc)
            self.assertEqual(missing, [], f"render-check / lint codes missing from {doc_path}: {missing}")


class TestVersionAndLinks(unittest.TestCase):

    def test_current_version_appears_where_users_look(self):
        for doc in ("README.md", "README_zh.md", "SKILL.md", "DESIGN_PHILOSOPHY.md", "DESIGN_PHILOSOPHY_zh.md",
                    "docs/en/architecture.md", "docs/en/cli_reference.md", "docs/en/blueprint_specification.md",
                    "docs/zh/architecture.md", "docs/zh/cli_reference.md", "docs/zh/blueprint_specification.md"):
            self.assertIn(__version__, read(doc), f"{doc} does not mention {__version__}")

    def test_changelog_has_an_entry_for_the_current_version(self):
        self.assertIn(f"## [{__version__}]", read("CHANGELOG.md"))

    def test_skill_copies_are_identical(self):
        self.assertEqual(read("SKILL.md"), read(".agents/skills/undo-ppt/SKILL.md"))

    def test_every_relative_markdown_link_resolves(self):
        pages = glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True)
        pages += [os.path.join(ROOT, p) for p in ("README.md", "README_zh.md", "SKILL.md", "CONTRIBUTING.md",
                                                  "CHANGELOG.md", "DESIGN_PHILOSOPHY.md", "DESIGN_PHILOSOPHY_zh.md")]
        broken = []
        for page in pages:
            text = open(page, encoding="utf-8").read()
            for m in re.finditer(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", text):
                target = m.group(1)
                if target.startswith("http"):
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(page), target))):
                    broken.append((os.path.relpath(page, ROOT), target))
        self.assertEqual(broken, [])

    def test_every_document_is_reachable_from_a_readme(self):
        readmes = read("README.md") + read("README_zh.md")
        for path in glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True):
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            self.assertIn(rel, readmes, f"{rel} is not linked from either README")


KEY_DOCS = ("cli_reference", "audit_codes", "design_system", "blueprint_specification", "architecture",
            "agent_integration", "scenario_anti_patterns", "scenario_outlines")


class TestBilingualParity(unittest.TestCase):
    """The key reference docs exist in English and Chinese and stay in step.

    Not a translation check (a test cannot judge that): it catches a document that exists in one language only,
    a section added to one side, a code block that was not carried over, and facts missing from the Chinese side.
    """

    def test_every_key_doc_exists_in_both_languages_and_links_to_the_other(self):
        for name in KEY_DOCS:
            en, zh = f"docs/en/{name}.md", f"docs/zh/{name}.md"
            self.assertTrue(os.path.exists(os.path.join(ROOT, en)), en)
            self.assertTrue(os.path.exists(os.path.join(ROOT, zh)), zh)
            self.assertIn(f"[简体中文](../zh/{name}.md)", read(en), f"{en} has no link to its Chinese version")
            self.assertIn(f"[English](../en/{name}.md)", read(zh), f"{zh} has no link to its English version")

    def test_no_orphan_document_in_either_language_folder(self):
        for lang, other in (("en", "zh"), ("zh", "en")):
            names = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(ROOT, "docs", lang, "*.md"))}
            self.assertEqual(names - set(KEY_DOCS), set(), f"docs/{lang} has a document that is not in KEY_DOCS")
            self.assertEqual(names, set(KEY_DOCS), f"docs/{lang} is missing documents")

    def test_both_versions_have_the_same_section_structure(self):
        for name in KEY_DOCS:
            en, zh = read(f"docs/en/{name}.md"), read(f"docs/zh/{name}.md")
            h2_en, h2_zh = len(re.findall(r"^## ", en, re.M)), len(re.findall(r"^## ", zh, re.M))
            h3_en, h3_zh = len(re.findall(r"^### ", en, re.M)), len(re.findall(r"^### ", zh, re.M))
            fences_en, fences_zh = en.count("```"), zh.count("```")
            self.assertEqual((h2_en, h3_en, fences_en), (h2_zh, h3_zh, fences_zh),
                             f"{name}: sections (##, ###) and code fences differ between languages")

    def test_chinese_docs_carry_the_same_facts(self):
        facts = {
            "cli_reference": ["probe", "ingest", "cite", "render-check", "--final", "--motion", "reveal", "contrast", "build"],
            "scenario_anti_patterns": [f"S{i:02d}" for i in range(1, 13)],
            "blueprint_specification": ["options", "sign_off_items", "recommendation", "presentation_config", "source", "status"],
            "architecture": ["layout_fit", "layout_lint", "render_check", "contract_probe", "blueprint_compat", "provenance",
                             "ingest", "motion", "contrast", "design_check", "theme_reader", "vision_extractor"],
            "design_system": ["check_tokens", "repair_tokens", "font_ea", "theme_source", "design_notes"],
        }
        for name, needles in facts.items():
            for lang in ("en", "zh"):
                text = read(f"docs/{lang}/{name}.md")
                for needle in needles:
                    self.assertIn(needle, text, f"docs/{lang}/{name}.md does not mention {needle}")

    def test_every_chinese_doc_is_linked_from_the_chinese_readme_and_english_from_the_english_one(self):
        for name in KEY_DOCS:
            self.assertIn(f"docs/zh/{name}.md", read("README_zh.md"), f"README_zh.md does not link docs/zh/{name}.md")
            self.assertIn(f"docs/en/{name}.md", read("README.md"), f"README.md does not link docs/en/{name}.md")

    def test_chinese_docs_link_only_to_chinese_docs(self):
        for name in KEY_DOCS:
            for target in re.findall(r"\]\(([^)#\s]+\.md)", read(f"docs/zh/{name}.md")):
                if target.startswith("http") or target.startswith("../en/"):
                    continue  # the language switch at the top
                self.assertNotIn("/en/", target, f"docs/zh/{name}.md links to an English document: {target}")


class TestPrdBilingualParity(unittest.TestCase):
    """Every PRD has an English counterpart in docs/en/prd/ with the same structure, linked both ways."""

    PRDS = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "docs", "PRD_*.md")))

    def test_there_are_prds_to_check(self):
        self.assertGreaterEqual(len(self.PRDS), 7)

    def test_every_prd_has_an_english_version_that_links_back(self):
        for name in self.PRDS:
            en = f"docs/en/prd/{name}"
            self.assertTrue(os.path.exists(os.path.join(ROOT, en)), en)
            self.assertIn(f"](en/prd/{name})", read(f"docs/{name}"), f"docs/{name} has no link to its English version")
            self.assertIn(f"[简体中文](../../{name})", read(en), f"{en} has no link to its Chinese version")

    def test_no_english_prd_without_a_chinese_original(self):
        names = {os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "docs", "en", "prd", "*.md"))}
        self.assertEqual(names, set(self.PRDS))

    def test_prd_versions_have_the_same_structure(self):
        for name in self.PRDS:
            zh, en = read(f"docs/{name}"), read(f"docs/en/prd/{name}")
            shape = lambda t: (len(re.findall(r"^## ", t, re.M)), len(re.findall(r"^### ", t, re.M)),
                               len(re.findall(r"^#### ", t, re.M)), t.count("```"), len(re.findall(r"^> \*\*", t, re.M)))
            self.assertEqual(shape(zh), shape(en), f"{name}: headings, code fences or correction notes differ")

    def test_english_prds_link_only_inside_english_docs_or_up_to_the_originals(self):
        for name in self.PRDS:
            for target in re.findall(r"\]\(([^)#\s]+\.md)", read(f"docs/en/prd/{name}")):
                if target.startswith("http"):
                    continue
                self.assertFalse(target.startswith("../zh/") or target.startswith("../../zh/"),
                                 f"docs/en/prd/{name} links to a Chinese guide: {target}")


class TestNoKnownStaleClaims(unittest.TestCase):
    """Claims that were once true and are not. Each corresponds to a defect found in v3.5-v3.8."""

    def test_nothing_promises_click_to_advance_animation_in_keynote_or_wps(self):
        for doc in ("README.md", "README_zh.md", "SKILL.md", "DESIGN_PHILOSOPHY.md", "DESIGN_PHILOSOPHY_zh.md"):
            text = read(doc)
            self.assertNotRegex(text, r"genuine step-by-step click-to-advance animations in PowerPoint, Keynote")
            self.assertNotIn("原生单击步进进入效果", text)
            self.assertNotIn("<p:timing>` 原生时序步进", text)

    def test_undo_is_not_described_as_luminance_based(self):
        self.assertNotIn("Computes canvas and shape luminance", read("README.md"))
        self.assertNotIn("Computes canvas luminance", read("DESIGN_PHILOSOPHY.md"))
        self.assertNotIn("智能检测背景与形状亮度", read("README_zh.md"))

    def test_architecture_states_the_real_audit_weighting(self):
        self.assertNotIn("structural score (40%)", read("docs/en/architecture.md"))

    def test_the_testing_claim_is_not_wider_than_what_was_run(self):
        self.assertNotIn("15 test suites pass cleanly across Python 3.10", read("README.md"))


if __name__ == "__main__":
    unittest.main()
