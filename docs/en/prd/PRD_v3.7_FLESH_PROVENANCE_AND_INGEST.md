# undoPPT v3.7.0 Product Requirements Document (PRD)
## Flesh: Every Number Says Where It Came From

> English | [简体中文](../../PRD_v3.7_FLESH_PROVENANCE_AND_INGEST.md)

> **Later changes**: in §6, the "Keynote" verification planned for v3.8 was not achieved; see the [v3.8 PRD](PRD_v3.8_SKIN_AND_POISE.md). The page footer introduced here (R5) is shown in Chinese in the output (`来源：`, `待核`, `估算`, `示例数据`).

---

## 1. Document Metadata

* **Product**: undoPPT (presentation deconstruction and reconstruction agent)
* **Version**: v3.7.0
* **Written**: 2026-10-06
* **Status**: Released / in production
* **Core goals**:
  1. Make **every number in the blueprint able to name its source**; numbers without one are plainly marked "to verify" on the output;
  2. Provide a **traceable data channel** from document to blueprint: `ingest` extracts, `cite` fills back;
  3. Provide a **delivery gate**: `build --final` refuses to build while unverified numbers remain;
  4. Make the demo **obey the product's own rules**, as a model rather than a counter-example;
  5. 100% backward compatible: `source` / `status` are optional and do not change existing blueprints.

---

## 2. Background and Problem Analysis

Flesh (content) is the substance of a deck. v3.6 solved "generating on insufficient information" and "content that cannot carry the layout", but not a more dangerous class of problem: **numbers that look like evidence but cannot be checked**.

Measured before v3.7:

| # | Symptom | Root cause |
|---|---|---|
| 1 | Numbers such as "35% cost saving" and "94.8% completion" in planner output are all invented by templates, yet look no different from real data on the page | The blueprint has no source field; neither renderer nor auditor cares where a number came from |
| 2 | Users supplied documents, yet numbers were still copied by the agent by hand, with no way to notice mistakes | No traceable channel from document to blueprint |
| 3 | The demo itself triggered 8 audit findings (4 clichés, 3 unquantified, 1 thesis drift) and ended on four bullet points with no decision loop | The demo was written before the rules existed and never checked by them |
| 4 | The cliché warning said only "don't use 'closed loop'", not what to write instead | The rule is an after-the-fact alarm, not guidance usable while drafting |

---

## 3. Requirements

### 3.1 Data provenance model (`core/provenance.py`)
- **R1 Fields**: `source` (string or list) and `status` (`verified` / `estimate` / `illustrative` / `todo`), writable on a page or on a nested item. A page-level value covers the whole page; an item-level value covers only that item and takes precedence.
- **R2 What counts as a number**: percentages, multiples, money, durations, numbers with units of measure, and headcounts like "5 heads". Years, quarters (Q3), priorities (P0), levels (L4) and structural counts ("3 pillars") are not numbers.
- **R3 To verify**: a number covered by no `source`, and any number with `status: todo`, is to be verified. `illustrative` does not count as to-verify but must be labelled.
- **R4** Native chart data counts as a set of numbers and needs a `source`.

### 3.2 Markers on the output
- **R5** PPTX and HTML: the footer shows `来源：…` (with the prefix "estimate · / sample data ·" when `status` is `estimate` / `illustrative`); a page with to-verify numbers shows an amber `待核 N 项` badge at the top right.
- **R6** Speaker notes and the HTML cognitive drawer (`N` key) list sources, estimates, sample data and to-verify numbers.
- **R7** Footer and badge are added after layout fitting and **must not move the content blocks**.

### 3.3 Data channel
- **R8 `cli.py ingest`**: from `.md` / `.txt` extract numbers with source `file:L<line>`; from `.csv`, source `file:row N·column`, using the unit in the header's brackets (`value(10k CNY)` + `1200` → `1200 10k CNY`). Excel is explicitly rejected with a hint to export CSV.
- **R9 `cli.py cite`**: fill sources back into the blueprint by numeric value. **Conservative rule**: a page-level `source` covers every number on the page, so it is written only when **all** the page's unsourced numbers match; a partial match writes only `source_candidates` and the numbers stay to-verify. `cite` never writes `status` (a match proves only that the number appears in the document, not that it is used for the same claim).
- **R10 `build --final`**: while to-verify numbers remain, exit code 1 and refuse to build; when it passes, the to-verify badge is hidden. A plain `build` keeps the badge, for drafts.

### 3.4 Audit
- **R11** `UNSOURCED_FIGURES_P<n>` and `EVIDENCE_TODO_P<n>` (2 points each, at most 10 in total); `EVIDENCE_ESTIMATE_P<n>` and `EVIDENCE_ILLUSTRATIVE_P<n>` are notices only. The audit result carries number statistics and the `audit` command prints a one-line summary.
- **R12 Cliché replacement suggestions**: nine cliché terms each carry a concrete rewrite (the `suggestion` field, also put in the message).

### 3.5 Demo
- **R13** The demo ends on a decision-loop page: three options (exactly one recommended), the reason, an approval list.
- **R14** The demo contains no banned words, and all its core evidence is quantified; invented numbers are uniformly marked `illustrative`. Target: an audit with no warnings.

### 3.6 Rendering fixes
- **R15** The font-size floor raises only runs under 12pt and leaves titles alone; short labels (≤16 characters) may not wrap because of enlargement (v3.5's whole-box proportional enlargement produced orphan characters).
- **R16** On the decision page the approval list box ends at 7.0 in, clear of the footer.

---

## 4. Acceptance Criteria

| Criterion | Result |
|---|---|
| All tests pass | 105 (68 existing + 37 new) |
| Demo audit | 100/100, no warnings (v3.6: 8); only `illustrative` notices |
| Demo numbers | 64, all marked as sample data, 0 to verify |
| Demo ending | 3 options, 1 recommended, reason, 3 approval items |
| Real PowerPoint render: demo | 8 pages, 0 static lint findings; footer visible, decision-page list box clear of the footer, level names on one line |
| PPTX for the 12 enterprise scenarios | 0 static lint findings; PowerPoint blank bands: 0 pages over limit |
| `cite` partial match | Writes no `source`, only `source_candidates`; unmatched numbers stay to-verify |
| `build --final` | With to-verify numbers: exit code 1 and no file; with all sourced: exit code 0 and no badge |
| Footer/badge do not move content | Two PPTX files with and without a footer have identical vertical positions for content shapes |
| End to end | `ingest` → `cite` → `build --final` passes on a sample document |

---

## 5. Out of Scope and Known Limits

- Number detection is pattern-based: it misses numbers written in words such as "三成" ("30%"), and may count unit-bearing numbers that are not claims.
- `cite` matches only numeric value strings and understands no semantics; `verified` must be decided by a person.
- Excel is not read directly; export CSV first.
- The planner still invents numbers (it is the fallback author); v3.7 makes them **visible as to-verify** rather than preventing them from being written.

---

## 6. Follow-up Roadmap

| Version | Theme | Highlights |
|---|---|---|
| v3.8.0 | Skin polish and poise | Type hierarchy and contrast rules; trial with real corporate templates; three narrative animations verified in PowerPoint / Keynote |
