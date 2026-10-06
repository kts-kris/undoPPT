"""ingest.py - Pull data points out of source documents, keeping where each one came from (v3.7).

`extract_facts` reads Markdown / text / CSV and returns one record per figure:

    {"label": "营收", "value": "1.2亿", "context": "Q3 营收 1.2 亿，同比 +18%", "source": "notes.md:L7"}

The `source` string is what ends up in a slide's `source` field (`cli.py cite` does the linking), so a
reader can go from a number on a slide back to the exact line or cell it came from.
Excel files: export the sheet to CSV first.
"""

import csv
import os
import re
from typing import Any, Dict, List

from core.provenance import FIGURE_RE, find_figures

_LABEL_JUNK = re.compile(r"^[#>*\-\s|:：,，.。;；()（）\[\]\d]+")
_UNIT_IN_HEADER = re.compile(r"[(（]\s*([^)）]+?)\s*[)）]\s*$")


def _clean_label(text: str, maxlen: int = 24) -> str:
    text = _LABEL_JUNK.sub("", text)
    text = re.sub(r"\s+", " ", text).strip(" :：,，|-+＋")
    return text[-maxlen:] if len(text) > maxlen else text


def _from_text(path: str) -> List[Dict[str, Any]]:
    base = os.path.basename(path)
    facts: List[Dict[str, Any]] = []
    heading = ""
    with open(path, "r", encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            line = raw.rstrip("\n")
            if re.match(r"^\s*#{1,6}\s+", line):
                heading = re.sub(r"^\s*#{1,6}\s+", "", line).strip()
            prev_end = 0
            for m in FIGURE_RE.finditer(line):
                value = re.sub(r"\s+", "", m.group(0))
                label = _clean_label(line[prev_end:m.start()]) or _clean_label(line[:m.start()]) or heading
                prev_end = m.end()
                facts.append({
                    "label": label,
                    "value": value,
                    "context": line.strip()[:120],
                    "section": heading,
                    "source": f"{base}:L{n}",
                })
    return facts


def _from_csv(path: str) -> List[Dict[str, Any]]:
    base = os.path.basename(path)
    facts: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return facts
    header = rows[0]
    for r_idx, row in enumerate(rows[1:], 2):
        row_label = row[0].strip() if row else ""
        for c_idx, cell in enumerate(row):
            cell = cell.strip()
            if not cell or c_idx >= len(header):
                continue
            col = header[c_idx].strip()
            unit_match = _UNIT_IN_HEADER.search(col)
            value = ""
            if find_figures(cell):
                value = re.sub(r"\s+", "", cell)
            elif unit_match and re.fullmatch(r"-?\d[\d,]*(?:\.\d+)?", cell):
                value = cell.replace(",", "") + unit_match.group(1).strip()
            if value:
                facts.append({
                    "label": f"{row_label} · {_UNIT_IN_HEADER.sub('', col).strip()}" if row_label and c_idx else (row_label or col),
                    "value": value,
                    "context": ", ".join(c.strip() for c in row)[:120],
                    "section": "",
                    "source": f"{base}:第{r_idx}行·{col}",
                })
    return facts


def extract_facts(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls"):
        raise ValueError("Excel is not read directly: export the sheet to CSV first.")
    if ext == ".csv":
        return _from_csv(path)
    return _from_text(path)
