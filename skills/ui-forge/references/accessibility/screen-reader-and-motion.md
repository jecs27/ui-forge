# Screen readers and motion

Two populations served by the same care: users who listen to the page and
users who cannot take motion. Both get their respect from *structure* and
*native behavior*, not from cleverness.

## Screen readers

- **Visually hidden text done right** (still in the a11y tree):

```css
.visually-hidden {
  position: absolute;
  width: 1px; height: 1px;
  margin: -1px; padding: 0;
  overflow: hidden; clip-path: inset(50%);
  border: 0; white-space: nowrap;
}
```

  Use for: a readable link name when the visible one is ambiguous
  ("Leer más … sobre el balance Q3", with the full name hidden), an
  `h1` visibly replaced by a logo, form labels that are icons. Never
  `display: none` (removes from a11y tree) when you meant "visually
  hidden".

- **Status announcements:** use `aria-live` regions (see
  `semantics-and-aria.md`) for async ends ("Guardado"), form-message
  changes, and cart updates. A *visually* noticeable spinner is not
  sufficient — say what is loading.

- **Tables:** real `<caption>` or `aria-label`, `<th scope>` — the SR
  reads headers. A div-grid that "looks" like a table gives the SR a
  list of divs.

- **Controls that are only visual** (a current-page dot with no label, a
  colored legend with no text) get hidden *decorative* treatment and a
  real text name.

## Motion (the interaction axis)

- **`prefers-reduced-motion: reduce`** is the modern gate (rule
  `A11Y-REDUCED-MOTION`): anyone with this OS setting gets a static,
  immediate version. Every animated element on the page needs one.
- **Autoplay without out:** video autoplay needs `muted` (+ `playsinline`)
  or sound off and a control to start; anything with sound autoplaying is
  an instant fail (rule `A11Y-AUTOPLAY`). Respect reduce-motion for
  autoplay video too — pause autoplay entirely in that mode.
- **No blinking > 3×/s** (WCAG 2.2.2, plus a *seizure* danger above 3 Hz
  — flashing never worth it; remove strobes outright, not "until AA
  passes").
- **Scroll-triggered reveals** should not hide content if JS/motion is
  off — content visible by default, animation only adds motion on top.

## Zoom and reflow 200 %/400 %

- Reflow at 400 % (320 px wide): no two-way scroll except intentional
  data-grid scrobble; text wraps, fields stack, no clipped overlays.
- Text at 200 %: measures saturate (a fixed-device measure that caps
  text at 800 px still reflows — the cap slows reading, then reflow
  still happens).
- `position: fixed` overlays that never size under zoom are a classic
  reflow breaker.

## Detect it

- Grep `aria-live` (work, but are they *polite* and containing real
  text?), `aria-label` on icons.
- Grep `display: none` where an element should be *visually* hidden —
  differ, `display:none` kills helper text.
- Grep `prefers-reduced-motion` presence/absence (rule) vs any
  `animation:`/`transition:` in the file.
- Grep `autoplay` in video tags for missing `muted` (rule).
- Grep blinking: `animation` with a > 333 ms step? (3 Hz ceiling).

## Verify

- Text-only render at 400 % zoom / 320 px; walk the fields and
  confirm nothing needs horizontal scroll.
- With reduce-motion ON, every animated element lands in its final state
  instantly and no content loops.
- Turn on a screen reader briefly: 3 representative controls announce
  sensibly.