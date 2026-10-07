# Typography

Typography carries most of the "quality" signal of a UI at nearly zero
cost. Rule of thumb: strong hierarchy, predictable scale, readable body.

## Rules

- **Body ≥ 16 px.** Below 16 px hurts reading and interacts badly with
  200 % zoom / text-size accessibility (project convention; the *minimum*
  a11y floor is text size at 200 % zoom in `screen-reader-and-motion.md`).
- **Line height 1.4–1.6 for body text** (convention); 1.15–1.3 for
  headings. Tighter than 1.4 in a paragraph is a reading-pain finding.
- **Measure 45–75 chars** (see `layout-and-spacing.md`).
- **Modular scale:** heading sizes step in a ratio (e.g. 1.25 major
  third: 16 20 25 31 39…). Sizes picked by eye (17.3 px, 24 px, 31 px,
  43 px in the same design) are a scale-inconsistency finding.
- **≤ 3 weights per family.** More than that is hierarchy-by-weight-
  noise; system or variable font handles the rest.
- **Hierarchy via size/weight, not decoration.** All-caps small-caps for
  labels is a common, subtle trick — fine — but decorative letter-spacing
  on body text ruins readability.
- **`text-wrap: balance`** on headings — one line for headings of 2 lines
  that look orphaned:

```css
h2 { text-wrap: balance; }
/* does not change meaning; pure polish, P3 */

p  { text-wrap: pretty; }
```

- **Tabular numerals for data** (`font-variant-numeric: tabular-nums`):
  digits in tables/timestamps align vertically instead of dancing.

## Fluid type with `clamp()`

```css
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}
/* min at small screens, scales with viewport, capped at large */
```

Small screens scale down, big screens scale up — without a single
breakpoint littered with headings. Line-height needs `1/1.15` in the same
declaration when the ratio would scale poorly.

## Detect it

- Grep `font-size` for values < 16 px on body selectors, and count
  distinct sizes on one screen > 10 (no scale).
- Grep `letter-spacing` on long text; `font-weight` counts per family.
- Grep `vw` used directly in font-size (unclamped) — scales past the
  measure.
- Check a data table for `tabular-nums`.

## Verify

- Change a size → re-check the rendered measure and hierarchy (squint
  test still passes).
- Zoom text-only to 200 %: body reflows, nothing overlaps or clips (see
  a11y reflow). If it clips, the combo line-height + size is wrong — fix
  the CSS, not the zoom.