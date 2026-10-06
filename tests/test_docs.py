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
        for doc in ("docs/en/cli_reference.md", "README.md", "README_zh.md", "SKILL.md"):
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
        doc = read("docs/en/audit_codes.md")
        missing = sorted(c for c in codes if c not in doc)
        self.assertEqual(missing, [], f"audit codes with no entry in docs/en/audit_codes.md: {missing}")

    def test_every_lint_and_render_code_is_in_the_cli_reference(self):
        src = read("core/layout_lint.py") + read("core/render_check.py")
        codes = set(re.findall(r'"code":\s*"([A-Z_]+)"', src))
        self.assertIn("LOW_CONTRAST", codes)
        doc = read("docs/en/cli_reference.md")
        missing = sorted(c for c in codes if c not in doc)
        self.assertEqual(missing, [], f"render-check / lint codes missing from the CLI reference: {missing}")


class TestVersionAndLinks(unittest.TestCase):

    def test_current_version_appears_where_users_look(self):
        for doc in ("README.md", "README_zh.md", "SKILL.md", "DESIGN_PHILOSOPHY.md", "DESIGN_PHILOSOPHY_zh.md",
                    "docs/en/architecture.md", "docs/en/cli_reference.md", "docs/en/blueprint_specification.md"):
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
