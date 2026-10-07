#!/usr/bin/env python3
"""ui-forge static scanner.

Read-only. No third-party dependencies. Prints a JSON document to stdout.

Usage:
    python3 scan_static.py [path ...]

Scopes: directories or files. Defaults to the current directory.
Never writes to the project. Never reads .env* files, key files, or
binary files. Rules are line/tag heuristics; heuristic rules carry a
`confidence` of "low" or "medium" and are suspicions, not verdicts.
Rule IDs and severities map to the references/ in this skill.
"""

import json
import os
import re
import sys
import time

VERSION = "0.1.0"

# --- file selection -------------------------------------------------------

EXTENSIONS = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".js", ".ts", ".css", ".scss", ".less", ".md"}
SKIP_DIRS = {"node_modules", ".git", ".hg", ".svn", "dist", "build", ".next", ".nuxt", ".output", "target", "__pycache__", ".cache", "coverage", ".turbo"}
# Files we must not open at all, regardless of content.
SECRET_FILENAME_RE = re.compile(r"(^\.env(\.|$)|\.pem$|\.key$|^id_rsa|^id_ed25519|\.keychain$)")


def _is_binary(path):
    try:
        with open(path, "rb") as fh:
            return b"\x00" in fh.read(1024)
    except OSError:
        return True


def walk_files(paths):
    """Yield readable source files, skipping junk and secrets."""
    skip_count = {"binary": 0, "secret_name": 0}
    pending = [p for p in paths if os.path.exists(p)]
    while pending:
        p = pending.pop()
        if os.path.isdir(p):
            base = os.path.basename(p.rstrip("/\\"))
            if base in SKIP_DIRS:
                continue
            try:
                names = sorted(os.listdir(p))
            except OSError:
                continue
            for n in names:
                pending.append(os.path.join(p, n))
            continue
        if not os.path.isfile(p):
            continue
        if SECRET_FILENAME_RE.search(os.path.basename(p)):
            skip_count["secret_name"] += 1
            continue
        ext = os.path.splitext(p)[1].lower()
        if ext not in EXTENSIONS:
            continue
        if _is_binary(p):
            skip_count["binary"] += 1
            continue
        yield p
    # stash counters so main() can read them
    _walkers["skip"] = skip_count


_walkers = {"skip": {"binary": 0, "secret_name": 0}}

# --- helpers --------------------------------------------------------------

line_cache = {}


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def line_no(text, pos):
    return text.count("\n", 0, pos) + 1


def snippet(text, pos, width=90):
    start = max(0, pos)
    end = start + width
    s = text[start:end].split("\n")[0].strip()
    return s if s else ""


def find_block(text, start):
    """Given a position at '{', return (open_pos, close_pos) of the brace block."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return start, i
    return start, len(text) - 1


# --- regexes --------------------------------------------------------------

RE_IMG = re.compile(r"<img\b[^>]*>", re.I | re.S)
RE_ALT = re.compile(r"\balt\s*=")
RE_DIM = re.compile(r"\b(width|height|aspect-ratio)\s*=")
RE_LAZY = re.compile(r"\bloading\s*=\s*[\"']lazy[\"']")
RE_HEROISH = re.compile(r"(hero|banner|cover|header|main|portada|principal)", re.I)
RE_SCRIPT_SRC = re.compile(r"<script\b(?P<tag>[^>]*\bsrc\s*=[^>]*?)>", re.I | re.S)
RE_DEFER = re.compile(r"\bdefer\b|\basync\b|\btype\s*=\s*[\"']?module[\"']?", re.I)
RE_PICTURE = re.compile(r"<picture\b[^>]*>.*?</picture>", re.I | re.S)
RE_PX_SRC = re.compile(r"\bsrc\s*=\s*[\"'][^\"']*\.(png|jpe?g)[\"']", re.I)
RE_MORDERN = re.compile(r"\.(webp|avif)\b")
RE_HTML_TAG = re.compile(r"<html\b[^>]*>", re.I)
RE_LANG_ATTR = re.compile(r"\blang\s*=", re.I)
RE_FONT_FACE = re.compile(r"@font-face\s*\{", re.I)
RE_FONT_DISPLAY = re.compile(r"font-display\s*:", re.I)
RE_CSS_IMPORT = re.compile(r"^\s*@import\b", re.M)
RE_TRANS_ALL = re.compile(r"transition(-property)?\s*:\s*[^;}]*\ball\b", re.I)
RE_LAYOUT_PROP = re.compile(r"\b(width|height|top|left|margin|padding)\s*:", re.I)
RE_KEYFRAMES = re.compile(r"@keyframes\b[^{]*\{", re.I)
RE_TRANS_LAYOUT = re.compile(
    r"transition(-property)?\s*:\s*[^;}]*\b(width|height|top|left|margin|padding)\b", re.I
)
RE_SCROLL = re.compile(r"addEventListener\s*\(\s*[\"'](scroll|touchmove)[\"']", re.I)
RE_PASSIVE = re.compile(r"\bpassive\s*:")
RE_MAP = re.compile(r"\.map\s*\(")
RE_KEY_INDEX = re.compile(r"\bkey\s*=\s*\{\s*index\s*\}")
RE_INLINE_HANDLER = re.compile(r"\bon[A-Z]\w*\s*=\s*\{?\s*[({]")
RE_STYLE_OBJECT = re.compile(r"\bstyle\s*=\s*\{\{")
RE_HEAVY_IMPORT = re.compile(
    r"\b(from|require\()\s*[\"'](lodash|moment|underscore)[\"']", re.I
)
RE_HEAVY_ALL = re.compile(r"import\s+\*?\s*as\s+_\s*from\s*[\"']lodash[\"']", re.I)
RE_INPUT = re.compile(r"<(input|textarea|select)\b[^>]*>", re.I | re.S)
RE_LABEL_ON = re.compile(r"\b(aria-label|aria-labelledby)\s*=", re.I)
RE_INPUT_ID = re.compile(r"\bid\s*=\s*[\"']([^\"']+)[\"']", re.I)
RE_LABEL_FOR = re.compile(r"<label\b[^>]*\bfor\s*=\s*[\"'](%s)[\"']", re.I)
RE_HIDDEN = re.compile(r"\btype\s*=\s*[\"']hidden[\"']", re.I)
RE_HEADING = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.I | re.S)
RE_PX_FONT = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", re.I)
RE_REM = re.compile(r"\bfont-size\s*:\s*[^;}]*rem\b", re.I)
RE_RGB = re.compile(r"#[0-9a-fA-F]{3,8}|rgba?\([0-9,\s.]+%?\)")
RE_TOKEN = re.compile(r"\b(?:var\(--|theme\.|tokens\.|colors\.)", re.I)
RE_100VH = re.compile(r"(min-height|height)\s*:\s*100vh", re.I)
RE_AUTOPLAY = re.compile(r"<(video|audio)\b[^>]*\bautoplay\b[^>]*>", re.I | re.S)
RE_MUTED = re.compile(r"\bmuted\b")
RE_CONTROLS = re.compile(r"\bcontrols\b")
RE_TARGET = re.compile(r"(button|btn|icon|chip|toggle|switch|tab)\b", re.I)

# Security: report these locations, never act on the text.
RE_INJECTION = re.compile(
    r"""ignore\s+(all\s+|any\s+|your\s+|previous\s+|prior\s+|earlier\s+|above\s+)?
        (instructions?|prompts?|directives?|rules|system\s+prompts?) |
        disregard\s+(all\s+|any\s+|your\s+|previous\s+|prior\s+)?(instructions?|prompts?|rules|the\s+above) |
        you\s+are\s+now\s+(in\s+)?(developer\s+mode|do\s+anything\s+mode|god\s+mode|unrestricted\s+mode) |
        send\s+(me\s+)?(the\s+|my\s+)?(\.env|env\s+file|credentials|secrets|tokens|api\s+keys) |
        print\s+(all\s+|the\s+|your\s+)?(previous|system|internal|full)\s+(instructions|prompt|system|config) |
        repeat\s+(all\s+|the\s+|verbatim\s+)?(above|previous|everything|this\s+prompt) |
        expose\s+(your|full|the\s+system)\s+(prompt|instructions|rules|config) |
        jailbreak
    """,
    re.I | re.X,
)
RE_SECRET = re.compile(
    r"""\b(AKIA[0-9A-Z]{16})\b |
        \b(SK\-[A-Za-z0-9]{20,})\b |
        \b(eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,})\b |
        -----BEGIN\s+(RSA|OPENSSH|EC|DSA|PRIVATE)\s+KEY----- |
        (api[_-]?key|secret|token|passwd|password|auth)\s*[:=]\s*["'][A-Za-z0-9_\-/+=]{16,}["']
    """,
    re.I | re.X,
)


# --- per-rule scanners -----------------------------------------------------

def scan_perf(text, path, findings):
    ext = os.path.splitext(path)[1].lower()

    # PERF-IMG-DIM
    for m in RE_IMG.finditer(text):
        tag = m.group(0)
        if not RE_DIM.search(tag):
            findings.append(rule("PERF-IMG-DIM", "P2", path, line_no(text, m.start()),
                                 snippet(text, m.start()),
                                 "Añade width+height (o aspect-ratio) para evitar CLS."))

    # PERF-IMG-LAZY-LCP (heuristic: heroish lazy img)
    imgs = list(RE_IMG.finditer(text))
    for idx, m in enumerate(imgs):
        if not RE_LAZY.search(m.group(0)):
            continue
        if idx < 3 or RE_HEROISH.search(m.group(0)):
            findings.append(rule("PERF-IMG-LAZY-LCP", "P1", path, line_no(text, m.start()),
                                 snippet(text, m.start()),
                                 "La imagen probable de héroe no debe ser lazy ni competir por LCP.",
                                 "medium"))

    # PERF-IMG-FORMAT (heuristic: raster img outside <picture>, no modern source)
    picture_spans = [m.span() for m in RE_PICTURE.finditer(text)]
    for m in RE_IMG.finditer(text):
        if RE_PX_SRC.search(m.group(0)):
            start = m.start()
            if any(a <= start < b for a, b in picture_spans):
                continue
            findings.append(rule("PERF-IMG-FORMAT", "P2", path, line_no(text, start),
                                 snippet(text, start),
                                 "Raster sin alternativa WebP/AVIF (srcset/picture)", "medium"))

    # if the file is CSS-ish
    if ext in {".css", ".scss", ".less"}:
        # PERF-FONT-DISPLAY: every @font-face needs font-display
        fm_start = 0
        for m in RE_FONT_FACE.finditer(text):
            body = m.end() - 1
            _, close = find_block(text, body)
            block = text[body:close + 1]
            if not RE_FONT_DISPLAY.search(block):
                findings.append(rule("PERF-FONT-DISPLAY", "P2", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "Añade font-display: swap|optional para evitar FOIT."))

        if ext == ".css":
            for m in RE_CSS_IMPORT.finditer(text):
                findings.append(rule("PERF-CSS-IMPORT", "P1", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "@import es serial y bloquea el render; usa <link> o el bundler."))

        for m in RE_TRANS_ALL.finditer(text):
            findings.append(rule("PERF-TRANS-ALL", "P2", path, line_no(text, m.start()),
                                 snippet(text, m.start()),
                                 "Lista las propiedades que transicionas; evita `all`."))

        for m in RE_TRANS_LAYOUT.finditer(text):
            findings.append(rule("PERF-ANIM-LAYOUT", "P2", path, line_no(text, m.start()),
                                 snippet(text, m.start()),
                                 "Animando propiedades de layout; usa transform/opacity.", "medium"))

        for m in RE_KEYFRAMES.finditer(text):
            _, close = find_block(text, m.end() - 1)
            body = text[m.end() - 1:close + 1]
            if RE_LAYOUT_PROP.search(body):
                findings.append(rule("PERF-ANIM-LAYOUT", "P2", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "@keyframes anima una propiedad de layout; usa transform/opacity.",
                                     "medium"))

    if ext in {".html", ".htm"}:
        for m in RE_SCRIPT_SRC.finditer(text):
            if not RE_DEFER.search(m.group("tag")):
                findings.append(rule("PERF-SCRIPT-BLOCK", "P1", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "script clásico sin defer/async/type=module bloquea el render."))

        for m in RE_SCROLL.finditer(text):
            if not RE_PASSIVE.search(text, m.end(), min(m.end() + 200, len(text))):
                findings.append(rule("PERF-SCROLL-LISTENER", "P2", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "Listener de scroll sin {passive:true}; añádelo (o usa IO).", "medium"))

    # PERF-LIST-LARGE / PERF-INLINE-FN-PROP (React-ish heuristics)
    if ext in {".jsx", ".tsx", ".vue", ".svelte", ".js", ".ts"}:
        for m in RE_MAP.finditer(text):
            segment = text[m.start():m.start() + 600]
            if RE_KEY_INDEX.search(segment):
                findings.append(rule("PERF-LIST-LARGE", "P2", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     ".map con key={index} dentro de colecciones grandes: virtualiza o usa id estable.",
                                     "low"))
            if RE_INLINE_HANDLER.search(segment) or RE_STYLE_OBJECT.search(segment):
                findings.append(rule("PERF-INLINE-FN-PROP", "P3", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "Handlers/objetos inline en listas: cada render recrea las props.",
                                     "low"))

    if ext in {".js", ".ts", ".jsx", ".tsx"}:
        for m in RE_HEAVY_IMPORT.finditer(text):
            findings.append(rule("PERF-HEAVY-IMPORT", "P2", path, line_no(text, m.start()),
                                 snippet(text, m.start()),
                                 "Importación completa de librería pesada; usa submódulos/named imports.",
                                 "medium"))


def scan_a11y(text, path, findings):
    ext = os.path.splitext(path)[1].lower()

    # A11Y-DIV-CLICK
    if ext in {".jsx", ".tsx", ".vue", ".svelte", ".js", ".ts"}:
        for m in re.finditer(r"<(div|span)\b(?P<tag>[^>]*\bonClick\s*=)[^>]*>", text, re.I | re.S):
            tag = m.group("tag") + text[m.end() - 1]
            if not re.search(r"\b(role|tabIndex|onKeyDown|onKeyUp)\s*=", tag, re.I):
                findings.append(rule("A11Y-DIV-CLICK", "P1", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "Elemento con onClick sin rol ni teclado; úsalo como <button>."))

    # A11Y-IMG-ALT (html and jsx/tsx)
    if ext in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}:
        for m in RE_IMG.finditer(text):
            tag = m.group(0)
            if not RE_ALT.search(tag):
                findings.append(rule("A11Y-IMG-ALT", "P1", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "img sin alt. Informativa → describe; decorativa → alt=\"\"."))

    # A11Y-OUTLINE-NONE (CSS)
    if ext in {".css", ".scss", ".less"}:
        for m in re.finditer(r"\boutline\s*:\s*(?:none|0)\b", text, re.I):
            tail = text[m.end():m.end() + 600]
            if not re.search(r":focus-visible", tail + text[max(0, m.start() - 1200):m.start()]):
                findings.append(rule("A11Y-OUTLINE-NONE", "P1", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "outline removido sin reemplazo :focus-visible."))

    # A11Y-LABEL (heuristic: wrapping <label> case can be missed)
    if ext in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}:
        for m in RE_INPUT.finditer(text):
            tag = m.group(0)
            if RE_HIDDEN.search(tag) or RE_LABEL_ON.search(tag):
                continue
            idm = RE_INPUT_ID.search(tag)
            labelled = False
            if idm:
                ahead = text[max(0, m.start() - 2500):m.start()]
                labelled = re.search(r"<label\b[^>]*\bfor\s*=\s*[\"']" + re.escape(idm.group(1)) + r"[\"']", ahead, re.I | re.S)
            if not labelled:
                findings.append(rule("A11Y-LABEL", "P1", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "input sin label asociado ni aria-label; se pierde el nombre accesible.",
                                     "medium"))

    # A11Y-LANG
    if ext in {".html", ".htm"}:
        for m in RE_HTML_TAG.finditer(text):
            if not RE_LANG_ATTR.search(m.group(0)):
                findings.append(rule("A11Y-LANG", "P2", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "<html> sin lang; los lectores no saben en qué idioma leer."))

    # A11Y-AUTOPLAY
    if ext in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}:
        for m in RE_AUTOPLAY.finditer(text):
            tag = m.group(0)
            if not (RE_MUTED.search(tag) or RE_CONTROLS.search(tag)):
                findings.append(rule("A11Y-AUTOPLAY", "P1", path, line_no(text, m.start()),
                                     snippet(text, m.start()),
                                     "autoplay sin muted ni control; peligro a11y, ruido y datos."))

    # A11Y-TARGET-SIZE (CSS, heuristic)
    if ext in {".css", ".scss", ".less"}:
        for selector, body, sel_pos in css_rules(text):
            if not RE_TARGET.search(selector):
                continue
            for m in re.finditer(r"\b(width|height)\s*:\s*(\d+(?:\.\d+)?)px", body, re.I):
                if float(m.group(2)) < 24:
                    findings.append(rule("A11Y-TARGET-SIZE", "P2", path, line_no(text, sel_pos),
                                         snippet(text, sel_pos),
                                         "Objetivo < 24 px (mínimo AA); 44 px recomendado.",
                                         "low"))

    # A11Y-REDUCED-MOTION: project-level, reported once
    if ext in {".css", ".scss", ".less"}:
        has_anim = re.search(r"(animation|transition)\s*:", text)
        has_reduce = re.search(r"prefers-reduced-motion", text, re.I)
        if has_anim and not has_reduce and not _motion_flagged.get(path):
            findings.append(rule("A11Y-REDUCED-MOTION", "P2", path, line_no(text, has_anim.start()),
                                 snippet(text, has_anim.start()),
                                 "Hay animaciones/transiciones sin bloque prefers-reduced-motion.",
                                 "medium"))
            _motion_flagged[path] = True

    # A11Y-HEADING-SKIP (heuristic)
    if ext in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".md"}:
        prev = 0
        for m in RE_HEADING.finditer(text):
            level = int(m.group(1))
            if prev and level > prev + 1:
                findings.append(rule("A11Y-HEADING-SKIP", "P2", path, line_no(text, m.start()),
                                     snippet(text, m.start(), 120),
                                     f"h{prev} → h{level}: se salta un nivel.", "medium"))
            prev = level


_motion_flagged = {}


def css_rules(text):
    """Yield (selector, body, selector_pos) for top-level CSS rules."""
    out = []
    pos = 0
    while True:
        brace = text.find("{", pos)
        if brace == -1:
            return out
        selector = text[pos:brace]
        close = text.find("}", brace)
        if close == -1:
            return out
        out.append((selector, text[brace + 1:close], brace - len(selector) + len(selector.lstrip())))
        pos = close + 1


def scan_ux(text, path, findings):
    ext = os.path.splitext(path)[1].lower()
    if ext not in {".css", ".scss", ".less", ".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}:
        return

    # UX-FIXED-PX-FONT (heuristic once per file when rem isn't the system)
    px = list(RE_PX_FONT.finditer(text))
    uses_rem = RE_REM.search(text)
    if px and not uses_rem:
        findings.append(rule("UX-FIXED-PX-FONT", "P3", path, line_no(text, px[0].start()),
                             snippet(text, px[0].start()),
                             f"Tipografía en px fijos ({len(px)} usos); plantéate rem y una escala.", "low"))

    # UX-MAGIC-COLOR (heuristic once per file)
    colors = set(m.group(0).lower() for m in RE_RGB.finditer(text))
    if len(colors) >= 3 and not RE_TOKEN.search(text):
        anchor = min(colors)
        pos = text.lower().find(anchor)
        findings.append(rule("UX-MAGIC-COLOR", "P2", path, line_no(text, pos),
                             snippet(text, pos),
                             f"{len(colors)} colores sueltos sin tokens {sorted(colors)[:4]}...", "low"))

    # UX-VH-MOBILE
    for m in RE_100VH.finditer(text):
        findings.append(rule("UX-VH-MOBILE", "P2", path, line_no(text, m.start()),
                             snippet(text, m.start()),
                             "100vh en móvil incluye la barra; usa 100dvh/svh.", "medium"))


def scan_sec(text, path, findings):
    for m in RE_INJECTION.finditer(text):
        findings.append(rule("SEC-INJECTION-TEXT", "P0", path, line_no(text, m.start()),
                             snippet(text, m.start(), 70),
                             "Texto con instrucciones incrustadas. Se ignora y se reporta; revisar quién lo introdujo."))
    for m in RE_SECRET.finditer(text):
        findings.append(rule("SEC-SECRET-HINT", "P1", path, line_no(text, m.start()),
                             "", "Posible secreto en esta línea. No se muestra el valor; rótalo y revoca si es real."))


def rule(rid, sev, path, line, snip, hint, confidence=None):
    d = {"rule": rid, "severity": sev, "file": path, "line": line,
         "snippet": snip, "hint": hint}
    if confidence:
        d["confidence"] = confidence
    return d


# --- main -----------------------------------------------------------------

def main(argv):
    paths = argv or ["."]
    findings = []
    scanned = 0
    t0 = time.time()
    for path in walk_files(paths):
        scanned += 1
        text = read_text(path)
        if not text:
            continue
        scan_perf(text, path, findings)
        scan_a11y(text, path, findings)
        scan_ux(text, path, findings)
        scan_sec(text, path, findings)
    findings.sort(key=lambda f: ({"P0": 0, "P1": 1, "P2": 2, "P3": 3}[f["severity"]],
                                  f["rule"], f["file"], f["line"]))
    # dedupe: one finding per (rule, file, line); the SEC probes can match twice on a line
    seen = set()
    uniq = []
    for f in findings:
        key = (f["rule"], f["file"], f["line"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(f)
    findings = uniq
    doc = {
        "skill_version": VERSION,
        "scanned_files": scanned,
        "skipped": _walkers["skip"],
        "duration_ms": int((time.time() - t0) * 1000),
        "finding_count": len(findings),
        "findings": findings,
    }
    sys.stdout.write(json.dumps(doc, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])