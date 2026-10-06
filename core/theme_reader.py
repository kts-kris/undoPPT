"""theme_reader.py - Read a real PPTX theme: colour scheme, master background, fonts (v3.8).

Until v3.7 `undo` looked only for explicit RGB fills and font names on *slides*. A real template keeps its
colours in `ppt/theme/theme1.xml` (referenced by name: accent1, bg2...) and its fonts in the theme font scheme;
its slides are empty placeholders. So `undo` found nothing and returned defaults: three different Office
themes, one of them dark, all came back as the same light blue theme.

This module reads what the template actually defines:
  - the colour scheme (dk1, lt1, dk2, lt2, accent1..6)
  - the master's colour map (which of those the master calls background / text)
  - the master background, resolving scheme colours and lumMod / lumOff / tint / shade
  - major / minor Latin fonts and the East Asian fonts for Chinese / Japanese
"""

import colorsys
import re
import zipfile
from typing import Any, Dict, Optional
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
SCHEME_KEYS = ("dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink")


def _hex(value: str) -> str:
    return "#" + value.lstrip("#").upper()


def _apply_modifiers(hex_color: str, node: ET.Element) -> str:
    """Apply lumMod / lumOff / tint / shade children of a colour element (in document order)."""
    r, g, b = (int(hex_color.lstrip("#")[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    for child in node:
        tag = child.tag.split("}")[1]
        val = int(child.get("val", "0")) / 100000.0
        if tag == "lumMod":
            l = max(0.0, min(1.0, l * val))
        elif tag == "lumOff":
            l = max(0.0, min(1.0, l + val))
        elif tag == "tint":
            l = max(0.0, min(1.0, l + (1 - l) * (1 - val)))
        elif tag == "shade":
            l = max(0.0, min(1.0, l * val))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))


def _resolve_color(node: ET.Element, scheme: Dict[str, str], clr_map: Dict[str, str]) -> Optional[str]:
    """Resolve an <a:srgbClr> / <a:schemeClr> / <a:sysClr> element to #RRGGBB."""
    tag = node.tag.split("}")[1]
    if tag == "srgbClr":
        return _apply_modifiers(_hex(node.get("val")), node)
    if tag == "sysClr":
        return _apply_modifiers(_hex(node.get("lastClr", "000000")), node)
    if tag == "schemeClr":
        name = node.get("val")
        name = clr_map.get(name, name)  # bg1 -> lt1 or dk1, tx1 -> dk1 or lt1 ...
        base = scheme.get(name)
        return _apply_modifiers(base, node) if base else None
    return None


def _part_for_master(z: zipfile.ZipFile) -> Dict[str, str]:
    names = set(z.namelist())
    master = "ppt/slideMasters/slideMaster1.xml"
    theme = "ppt/theme/theme1.xml"
    rels = "ppt/slideMasters/_rels/slideMaster1.xml.rels"
    if rels in names:
        for m in re.finditer(r'Type="[^"]*/theme"[^>]*Target="([^"]+)"|Target="([^"]+)"[^>]*Type="[^"]*/theme"', z.read(rels).decode("utf-8")):
            target = m.group(1) or m.group(2)
            theme = "ppt/" + target.replace("../", "")
            break
    return {"master": master, "theme": theme}


def read_theme(pptx_path: str) -> Optional[Dict[str, Any]]:
    """Return the template's real theme, or None when the file has no readable theme."""
    try:
        z = zipfile.ZipFile(pptx_path)
    except (zipfile.BadZipFile, FileNotFoundError):
        return None
    with z:
        parts = _part_for_master(z)
        names = set(z.namelist())
        if parts["theme"] not in names or parts["master"] not in names:
            return None
        theme = ET.fromstring(z.read(parts["theme"]))
        master = ET.fromstring(z.read(parts["master"]))

    scheme: Dict[str, str] = {}
    clr_scheme = theme.find(".//a:clrScheme", NS)
    if clr_scheme is None:
        return None
    for key in SCHEME_KEYS:
        el = clr_scheme.find(f"a:{key}", NS)
        if el is None or len(el) == 0:
            continue
        child = el[0]
        value = child.get("val") if child.tag.endswith("srgbClr") else child.get("lastClr")
        if value:
            scheme[key] = _hex(value)
    if "dk1" not in scheme or "lt1" not in scheme:
        return None

    clr_map_el = master.find(".//p:clrMap", NS)
    clr_map = dict(clr_map_el.attrib) if clr_map_el is not None else {"bg1": "lt1", "tx1": "dk1", "bg2": "lt2", "tx2": "dk2"}

    background = None
    bg = master.find(".//p:bg", NS)
    if bg is not None:
        for el in bg.iter():
            if el.tag.split("}")[1] in ("srgbClr", "schemeClr", "sysClr"):
                background = _resolve_color(el, scheme, clr_map)
                break
    if background is None:
        background = scheme.get(clr_map.get("bg1", "lt1"))

    font_scheme = theme.find(".//a:fontScheme", NS)
    fonts: Dict[str, Optional[str]] = {"major": None, "minor": None, "east_asian": None}
    if font_scheme is not None:
        for key, tag in (("major", "majorFont"), ("minor", "minorFont")):
            el = font_scheme.find(f"a:{tag}/a:latin", NS)
            if el is not None and el.get("typeface") and not el.get("typeface").startswith("+"):
                fonts[key] = el.get("typeface")
        for tag in ("minorFont", "majorFont"):
            for script in ("Hans", "Hant", "Jpan"):
                el = font_scheme.find(f"a:{tag}/a:font[@script='{script}']", NS)
                if el is not None and el.get("typeface"):
                    fonts["east_asian"] = fonts["east_asian"] or el.get("typeface")
            ea = font_scheme.find(f"a:{tag}/a:ea", NS)
            if ea is not None and ea.get("typeface"):
                fonts["east_asian"] = ea.get("typeface")

    return {
        "scheme_name": clr_scheme.get("name", ""),
        "colors": scheme,
        "clr_map": clr_map,
        "background": background,
        "text": scheme.get(clr_map.get("tx1", "dk1")),
        "text_secondary": scheme.get(clr_map.get("tx2", "dk2")),
        "fonts": fonts,
    }
