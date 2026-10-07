# Layout and spacing

Spacing is the design system people feel first: rhythm, alignment, and
density. It should come from a scale, not from vibes.

## Spacing scale

- **One base unit, powers / multiples of it.** Base 4 px or 8 px are the
  common conventions (this is a project convention, not a standard).
  `2 4 8 12 16 24 32 48 64` is a working 4 px-derived set. A project
  that tolerates `3px` here, `7px` there, and `18px` there has no scale —
  that is a finding, and the fix is to pick a base and normalize.
- **Rhythm: consistent vertical (margin) and horizontal (writing) flow.**
  Consistent spacing *is* the relative hierarchy (see visual-hierarchy);
  inconsistent spacing breaks reading rhythm faster than inconsistent
  size.
- **Grid alignment:** elements align to the same left/gutter edges; an
  off-by-one offset is visible in 50 ms. Use tokens for gaps rather than
  per-component numbers.

## Letter/line widths

- **Reading measure: 45–75 characters per line** for running text
  (project convention, derived from typographic practice; the a11y
  reflow rule only touches zoom, not measure). Wider lines are harder to
  track; narrower feel choppy. `ch` is the unit: text at
  `max-width: 65ch`.
- **Page content width:** caps at ~1200–1440 px, but that is a
  convention; a data dashboard may legitimately run wider with short cell
  text.

## Density matches the product

- **Density dial:** a CRM spreadsheet dense and scan-navigable; a
  consumer landing page airy and emotive; the *same* product must not
  mix both without system-level reason.
- **Tactile targets** (44 px recommended / 24 px WCAG minimum) live in
  `accessibility/` — spacing must not squeeze below them.
- **Avoid the reflex 3-card template.** "Three cards with soft shadow"
  is the default answer to every layout question and the fastest way to
  serialize a design (see `anti-patterns.md`). Ask what the content
  needs before picking cards.

## Responsive relation

- Density and grid should degrade with the container, not with a magic
  breakpoint list — `repeat(auto-fit, minmax(...))` and *container
  queries* (see `responsive.md`) keep blocks coherent across widths.

## Detect it

- Grep CSS for spacing values (`padding`, `margin`, `gap`) and count
  distinct values in one page: value count >> 8 → no scale.
- Look for direct px widths on containers in responsive layouts (should
  be relative or clamped).
- Eyeball alignment in a rendered screenshot: elements whose edges should
  line up but don't by a few px.

## Measure/verify

- Track the spacing-token usage ratio: assignments to tokens vs raw
  values. Moving a page from 30 raw values to 8 tokens is the metric.
- The squint test also verifies rhythm: blurred screenshot shows whether
  groups, gaps, and alignment still read as intentional.