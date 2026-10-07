# Responsive

Responsive is "the product works at every width", not "there are three
sizes." Order below: start mobile, let content break the layout, protect
touch and safe areas.

## Principles

- **Mobile-first** in code and in review order. A design that is an
  adapted desktop is a desktop design that shrank; a real mobile-first
  flow thinks about thumb, one-handed reading, and network from the
  start.
- **Breakpoints by content, not devices.** A 600 px layout is a *content
  collapse*, not an iPad. Use `min-width` media queries from the small
  base upward; adding max-width hacks per device is a smell.
- **Container queries for components** (`@container`): a card grid should
  reflow because its *container* narrowed (sidebar vs full width), not
  because the viewport did. Component-per-container is the modern rule
  where browser support allows (2026: universal).
- **Relative units** everywhere sizing follows the content: `rem` for
  type (`UX-FIXED-PX-FONT`), `%`, `fr`, `clamp()`, `min()`/`max()`.
- **`dvh` on mobile, not `vh`**: `100vh` includes the hidden URL bar —
  a fixed footer floats or the hero clips; `100dvh` tracks the visible
  viewport (`UX-VH-MOBILE`).
- **Safe areas**: `padding: env(safe-area-inset-*)` on bottom bars and
  inset stuff — notches and home bars are real on the devices that hit
  them.
- **Touch:** targets ≥ 44 px recommended, 24 px minimum (AA), and the
  primary actions within thumb reach (see `navigation-and-ia.md`).

## Tables

- Wide tables on narrow screens: decide — horizontally scrollable inside
  a `overflow-x: auto` container with a scroll cue, or a card-reflow of
  the first rows. Never a full-page horizontal scroll because a table
  overflowed the body.

## Testing widths

- Check 320, 375, 768, 1024, 1440 px as a floor set (convention). For a
  consumer app 320 is the real low end; 1440+ matters for readable
  measure on large screens.
- **Text bump** is a test: enlarge system text to 200 % and confirm
  content reflows (see WCAG 1.4.4 resize) — a hard px width on a font or
  layout that clips at 200 % is a real finding.

## Detect it

- Grep `100vh` (rule `UX-VH-MOBILE`).
- Grep fixed px widths on containers with no `min`/`max`/`clamp`
  (heuristic: they may be fine inside a grid, so confirm context).
- Grep `@media (min-width: 1024px)`-first CSS (order check) and
  device-name breakpoints (`width: 768px` comments about "iPad").
- Grep `position: fixed` elements that lack bottom safe-area padding.
- Render 320 px: horizontal overflow of body is `overflow-x` hidden
  hiding it (the classic sin — content bombs).
- Grep `grid-template-columns: repeat(3` without `repeat(auto-fit` /
  container queries on a component meant to resize.

## Verify

- Resize to the floor set: nothing overflows, breaks clip, or moves
  unpredictably; content reflows at text-size 200 %.
- On a real small device (or devtools mobile emulation): tab bar sits
  above the home indicator, tap targets are ≥ 44 px, no accidental
  double-tap.