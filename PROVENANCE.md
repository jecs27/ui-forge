# PROVENANCE

All prose in this skill is original writing or paraphrase written for this
repository. No text was copied from other skills, vendor documentation,
blog posts, or tool output.

## Standards referenced (public specifications, not copied text)

| Source | Where used | Link |
|---|---|---|
| WCAG 2.2 (W3C Recommendation) | `references/accessibility/wcag-2-2-checklist.md` — success criterion numbers, level AA, and the numeric thresholds that appear in the standard itself (24 px target size, contrast ratios) | https://www.w3.org/TR/WCAG22/ |
| Core Web Vitals (Google public metric definitions) | `references/performance/core-web-vitals.md` — metric names and good thresholds (LCP 2.5 s, INP 200 ms, CLS 0.1) | https://web.dev/articles/vitals |
| Web Content Accessibility Techniques (W3C WAI) | General a11y guidance patterns; criterion identifiers only | https://www.w3.org/WAI/WCAG22/quickref/ |
| HTML Living Standard (WHATWG) | Semantics of native elements (`button`, `a`, `label`), media attributes | https://html.spec.whatwg.org/ |
| CSS Transforms / Compositor guidance (MDN) | `references/performance/animation-performance.md` — which properties animate on the compositor | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transforms |

Numeric thresholds in this skill are one of three kinds, and each file
labels them:

1. **Standard-defined** — comes from WCAG or a published metric definition
   (contrast 4.5:1, target size 24 px, CLS 0.1).
2. **Budget** — a tunable project budget, not a standard. Default values in
   `scripts/budgets.default.json` are starting points (170 KB gzip JS is a
   convention used in performance work, not a rule from any spec).
3. **Heuristic** — a detection guess with no guarantee. Always marked
   `confidence: low` or `confidence: medium` and phrased as "suspicion to
   confirm".

## Ideas adapted (not text)

- The diagnose → score → fix → verify loop is a common pattern in audit
  tooling; the implementation here is written from scratch.
- Design "philosophies" in `references/philosophies/` are original
  syntheses of well-known visual styles (minimalist, brutalist, editorial),
  not descriptions lifted from any designer's published framework.
- Static rules in `scripts/scan_static.py` encode the checks described in
  this repository's own reference files. Each rule ID maps to a rule
  written here first.

## Third-party code

None. `scripts/scan_static.py` uses only the Python 3 standard library.
