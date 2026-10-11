# Fonts

Web fonts cost two things: bytes and a flash/flicker on swap. The goal is
to load little, and swap predictably.

## Rules

- **`font-display: swap`** (or `optional`) on every `@font-face`.
  `block` (default in some browsers) holds invisible text up to 3 s;
  `swap` shows the fallback immediately and swaps when ready; `optional`
  gives up fast if network is slow — ideal for self-hosted UI faces.
- **woff2 only** for the wire (browsers all support it since 2018).
  woff/ttf are for legacy compatibility — ship woff2 and be done.
- **Subset:** load only the glyph ranges the UI uses (latin, latin-ext,
  cyrillic...). A full CJK font is megabytes; subset to the running text.
- **Preload only the critical face** — the one the LCP text uses. Other
  faces load with the stylesheet to avoid preload overload.
- **Variable font over multiple static weights** when the design uses 3+
  weights: one file, seamless intermediate weights. Static specimens are
  fine for 1–2 weights.
- **Budget (project convention, not a standard): ≤ 2 families and ≤ 4
  loaded weights**, adjustable in `budgets.default.json`. Over it → question
  whether a weight is real hierarchy or habit.

## CLS: font swap shifts text

- The fallback renders, then the real font lands and reflows. Fix with
  metric overrides on the `@font-face`:

```css
@font-face {
  font-family: 'Noto Sans';
  src: url('/fonts/noto-sans.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
  size-adjust: 100%;          /* tune to match fallback metrics */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

- `size-adjust` aligns cap height; the overrides align the baseline. Tune
  numerically against the fallback; this is project-specific work, not a
  copy-paste — verify with before/after CLS.
- Alternatively `font-display: optional`: after the failed quick load,
  the fallback sticks and nothing reflows. Good for non-critical text.

## Loading strategy

```html
<link rel="preload" href="/fonts/display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/fonts.css">
```

- `crossorigin` is mandatory on the preload of a font (fonts are loaded
  with CORS).
- Server render the critical CSS inline or with a preload; non-critical
  faces can join the stylesheet. Third-party font services:
  `preconnect` to their origin before the stylesheet.

## Detect in code

- Grep `@font-face` and each block: missing `font-display` (scanner rule
  `PERF-FONT-DISPLAY`), missing `src` woff2 upgrade path, full alphabet
  subsets that are overkill.
- Count families × weights loaded (budget comparison).
- Grep `font-family` in CSS for the fallback stack: a good stack lists
  generic families last (`ui-sans-serif, system-ui, sans-serif`), a bad
  one names only the webfont.

## Measure it

- Network tab: bytes per font, load time, whether it delays FCP/LCP.
- DevTools → Rendering → "Paint flashing" to see the late repaint when
  the font swaps.
- Compare CLS with fonts disabled vs enabled to isolate swap-induced
  shift.
- PageWeight or the network summary for total font bytes.