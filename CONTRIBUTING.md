# Contributing to undoPPT

Thank you for your interest in contributing to **undoPPT**! We welcome contributions from developers, researchers, and AI practitioners across the global open-source community.

---

## 1. Development Setup

### Prerequisites
- **Python 3.10+** (Tested on Python 3.10, 3.11, 3.12, 3.13, and 3.14).
- Standard package manager (`pip`).

### Clone and Install
```bash
# Clone the repository
git clone https://github.com/kts-kris/undoPPT.git
cd undoPPT

# Create a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Running Tests

Before committing any changes or opening a pull request, ensure all tests pass:

```bash
pip install -r requirements-dev.txt        # pytest, plus pypdfium2 and pillow for real renders
python3 -m pytest tests -q
```
Tests that need a macOS PowerPoint are skipped unless you opt in: `UNDOPPT_TEST_POWERPOINT=1 python3 -m pytest tests -q`.

### Writing Tests
Tests are split by what they protect:

| File | Covers |
| :--- | :--- |
| `tests/test_engine.py` | planner, auditors, builders, sync watcher, templates |
| `tests/test_layout.py` | content-adaptive layout, layout lint, offline HTML, renderer coverage (v3.5) |
| `tests/test_contract.py` | readiness probe, evidence budget, blueprint compatibility, text fidelity, scenario outlines (v3.6) |
| `tests/test_flesh.py` | provenance, `ingest` / `cite`, `build --final`, the decision-ready demo (v3.7) |
| `tests/test_motion_design.py` | narrative animations, contrast, real-theme extraction, template robustness (v3.8) |
| `tests/test_docs.py` | the documentation covers every command, module, audit code and test file, links resolve, no known stale claim returns |

When introducing a feature or fixing a bug, add assertions covering what a reader of the result would see, not just the data. Several shipped defects were invisible to tests that only inspected the file: an animation tree PowerPoint ignored, a template whose colours were never read, blueprint text silently dropped by a renderer. Prefer a test that fails if you reintroduce the bug (run it once against the broken code), and verify visual changes with `cli.py render-check --render`.

---

## 3. Engineering Standards

To maintain the reliability and modularity of `undoPPT`:

1. **Decoupled Architecture**: Maintain the strict boundary between soft cognitive reasoning (AI Agent / Cognitive Planner) and deterministic physical layout (Builders & Auditors). Never leak physical coordinate calculations into semantic prompts.
2. **Zero Domain Hardcoding**: Avoid hardcoding company names, proprietary internal tools, or domain-specific assumptions. Use generic scenario archetypes and dynamic fact extraction.
3. **Dual-Format Parity**: Any new layout primitive must be implemented with full visual and functional parity across **both** `core/pptx_builder.py` (native vector PowerPoint shapes/charts) and `core/html_builder.py` (responsive HTML with Tailwind).
4. **Speaker Notes & Cognitive Drawer**: Every slide must continue to embed slide missions, transitions, and talking points into PowerPoint Speaker Notes and the HTML Cognitive Inspector drawer (`N` key).
5. **Pythonic Quality**: Follow PEP 8 guidelines. Keep functions modular and maintain docstrings.
6. **Nothing Silently Dropped**: Every field a blueprint can carry must reach the slide. If a renderer reads a different field name than the specification documents, add the mapping to `core/blueprint_compat.py` (a test asserts every planner-emitted string reaches both PPTX and HTML).
7. **No Invented Numbers**: Do not add sample figures to presets, demos or planner templates without `status: "illustrative"` (or a `source`). The demo shows the rule.
8. **Verify in a Real Viewer**: Run `python3 cli.py render-check --pptx ... --html ... --render` for any change to layout, colour, fonts or animation. The layout lint, the contrast check and the animation validator are necessary, not sufficient.

---

## 4. How to Add a New Layout Primitive

To introduce a 16th layout primitive:
1. **Schema Definition**: Define the primitive's name and required attributes in `docs/en/blueprint_specification.md`.
2. **PPTX Implementation**: Add a rendering method `_render_<primitive_name>(slide, slide_data, tokens)` in `core/pptx_builder.py`. Use native vector shapes and avoid bitmap conversion.
3. **HTML Implementation**: Add a rendering method `_render_<primitive_name>(slide_data, tokens)` in `core/html_builder.py` with responsive CSS.
4. **Auditor & Content Budget**: Add density boundary rules (e.g. maximum items, text length limits) in `core/content_auditor.py` and ensure default tokens in `presets/` accommodate the primitive.
5. **Test Coverage**: Add a test slide with the new layout primitive into `test_all_15_layouts_render` in `tests/test_engine.py`; if the planner can emit it, `tests/test_contract.py::TestRendererCoverage` already checks that both builders know the name. Add its minimum body length to `ContentAuditor.MIN_BODY_CHARS`.
6. **Layout & Motion**: Decide whether it belongs in `FIT_LAYOUTS` (`core/layout_fit.py`) and which narrative animation it gets (`AUTO_BY_LAYOUT` in `core/motion.py`). Run `cli.py render-check --render` on a deck that uses it.
7. **Documentation**: Update `docs/en/blueprint_specification.md`, `README.md`, `README_zh.md` and `CHANGELOG.md`.

---

## 5. Submitting Pull Requests

1. **Fork** the repository and create your branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. **Commit** your changes following the [Conventional Commits](https://www.conventionalcommits.org/) specification:
   - `feat:` for new capabilities or layout primitives;
   - `fix:` for bug fixes;
   - `docs:` for documentation updates;
   - `refactor:` for code refactoring without functional changes;
   - `test:` for test additions or improvements.
3. **Run the test suite** and verify clean execution:
   ```bash
   python3 -m unittest discover -s tests -v
   ```
4. **Push** to your fork and submit a Pull Request to `main`.
5. Clearly describe the problem solved or feature added in the PR description, including test evidence.

---

## 6. License & Contributor Agreement

By contributing to `undoPPT`, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
