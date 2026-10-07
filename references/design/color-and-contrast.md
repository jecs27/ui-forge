# Color and contrast

Color is a signal, not the signal. Contrast is a hard requirement; the
numbers below come from WCAG AA, so treat them as floors.

## Contrast ratios (WCAG AA — hard floors, not suggestions)

| Text | Minimum contrast |
|---|---|
| Normal text | **4.5:1** |
| Large text (≥ 24 px / ~18.66 px bold) | **3:1** |
| UI components & graphics (borders, icons, input edges, graph lines) | **3:1** |

- These are against the *background they sit on*, not an average.
- **Practical rule:** never place grey-on-grey; if you cannot hit the
  number, darken the text or lighten the page. Text is never "styling".
- Disabled elements are a documented exception (WCAG lets you degrade
  them) — but then the *clearability* of the disabled state must carry
  meaning without color (a real disabled unlike an enabled look-alike).

## Don't rely on color alone

- Form state (valid/invalid/warning), graph categories, and link-vs-text
  need **a second channel**: text, icon, shape, underline, bold, or a
  change in semantic tag. A green/red-only validator is a finding that
  fails WCAG and real-world color-blind usage.
- Detect: screenshots of the palette in grayscale; a green-only =
  invalid indicator vanishes.

## Palette roles, not raw hues

Build the palette from **roles**, and map them to tokens:

| Role | Meaning | Example token |
|---|---|---|
| Background | Page/base | `--color-bg` |
| Surface | Cards, panels | `--color-surface` |
| Text primary / secondary | Content hierarchy | `--color-text-strong` / `--color-text-muted` |
| Border | Edges, dividers | `--color-border` |
| Accent | The one action color | `--color-accent` |
| States | Hover/active/disabled/error/success/focus | per-state |

Raw hex/rgb scattered through components (`UX-MAGIC-COLOR`) is a
findings class by itself — the tokens give you one-line theme swapping and
meaningful names. **An existing token system is preserved** (see
`detect_design_tokens.md`).

## Saturation and accent discipline

- One accent is a brand; six accents is a party. The accent goes on the
  primary action, the selected state, and links; **everything else stays
  neutral** (see `visual-hierarchy.md`).
- Saturated color text on saturated backgrounds is both low-contrast and
  visually loud. Keep accent for fills/buttons; reserve saturated *text*
  for emphasis words only.

## Dark mode (summary — see `dark-mode-and-theming.md`)

- Contrast floors hold in both modes; dark themes usually need *brighter*
  text (e.g. 13–15 % luminance-ish background content) to pass the same
  4.5:1 that light text passed at 19–21 on white.

## Detect it

- Grep hex/rgb values repeated in CSS/TSX (rule `UX-MAGIC-COLOR`,
  heuristic): the same `#6b7280` in 6 files with no token is a finding.
- Contrast-check the three highest-use text colors vs their
  backgrounds with any calculator (Lighthouse a11y, or an on-page picker)
  — computed, not eyeballed.
- Grayscale-render the screens and look for state/meaning loss.

## Measure it

- A contrast calculator on the actual values (the number, 4.5:1 vs the
  pair).
- Lighthouse "Contrast" checks the rendered page, not the source.