# Semantics and ARIA

ARIA is a patch, not a goal. The best accessibility is the native element
that already has the behavior, the keyboard, and the announced name built
in.

## Native semantics first

| Want | Native | ARIA attempt (last resort) |
|---|---|---|
| A clickable thing | `<button>` | `div role="button"` + `tabindex` + keydown (fragile) |
| A link | `<a href>` | `span` + click (no cursor, no middle-click, no a11y) |
| A checklist | `<input type="checkbox">` | `div role="checkbox"` + arrow keys (all yours to redo) |
| A list | `<ul>/<ol><li>` | `div` rows with roles (loses native list semantics & css) |
| A heading | `<h1>…<h6>` | `span tabindex` styled huge (fake, no outline) |
| A form field | `<input>` + `<label>` | `input` with `aria-label` (no visible label) |
| A menu | `<nav>` | `div role="navigation"` |

- **The classic error: `div` with an `onClick`** — rule
  `A11Y-DIV-CLICK`: no role, no tabindex, no keyboard, and in React exactly
  the thing a screen reader finds nothing. A `<button>` fixes it in one
  line and gets focus/hover/keyboard/press styles free.

## The ARIA that is actually fine

- **`aria-live`** for status regions: `aria-live="polite"` for a success
  toast or a "3 of 12 loaded" counter; `assertive` only for something the
  user must interrupt (rare). The *content* area that changes is the live
  region; use `aria-busy` + clear text, not a wall of numbers.
- **`aria-describedby`** to tie a field to its helper/error text
  (with `aria-invalid`, see `forms.md`).
- **`aria-current="page"`** on the active nav item.
- **`aria-expanded` / `aria-controls`** on disclosure buttons.
- **`role="alert"`** on error banners (implicit assertive live region).
- **`aria-label`** on icon-only buttons ("Cerrar" on a ghost X) — an
  icon button with no name fails 4.1.2 by itself.

## Rules

- **ARIA only where native fails.** `role="button"` on a working native
  `<button>` is noise; the ARIA problem is duplication, not absence.
- **Don't override native roles.** `role="main"` on a div next to `<main>`:
  same role twice. One of them is redundant.
- **Accessible names:** derived from *content* where possible (a text
  button names itself); `aria-label` overrides *everything* (including
  the button's own text) — the label must be the a11y text, not a
  decoration.
- **Headings without jumps:** `h1 → h3` breaking for *visual* reasons
  fails 1.3.1's structure; CSS can visually lower a heading —
  the landmark order is what the a11y tree reads. Fix by ordering
  semantically and restyling to taste.
- **`alt`: useful or empty.** Decorative images (icons, separator doodads)
  get `alt=""` — not "logo", not deleted. Meaningful images describe the
  message ("Gráfico: conversión mensual"). Repeated adjacent text makes it
  decorative.
- **`lang` on `<html>`** (rule `A11Y-LANG`): locale for SR pronunciation
  and `text-to-speech`.
- **Form groups** use `<fieldset><legend>` for radio/checkbox groups —
  the group question is the legend, not a per-option repetition.

## Detect it

- Grep `onClick` on `div`/`span` (rule `A11Y-DIV-CLICK`) — every hit is
  a top candidate for a semantic element.
- Grep `<img` without `alt` (rule `A11Y-IMG-ALT`); check decorative ones
  for `alt=""`.
- Grep `role=` and diff against native material duplication.
- Grep `aria-label` on buttons that already have visible text (double
  naming = the SR hears the label, not the text).
- Grep heading tags in each file: order jumps h? (rule
  `A11Y-HEADING-SKIP`, heuristic).

## Verify

- Screen-reader spot check (VoiceOver/NVDA if available): read a button,
  a checkbox group, a live error; "3 items, checkbox checked" beats
  "div, div, div".
- The a11y tree (Chrome "Accessibility" tab in devtools) shows what an
  SR sees — if the tree has a lacuna of unnamed interactive elements,
  that is the report.