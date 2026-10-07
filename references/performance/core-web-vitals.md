# Core Web Vitals

The three user-facing loading and interaction metrics, plus two supporting
ones. Thresholds are the *good* (p75 in the field) boundaries published
with the metric definitions. Laboratory measurement estimates; the field
confirms.

## Thresholds

| Metric | Good | What it means |
|---|---|---|
| **LCP** — Largest Contentful Paint | **≤ 2.5 s** | Largest text/image visible renders |
| **INP** — Interaction to Next Paint | **≤ 200 ms** | Response to a tap/click/key press |
| **CLS** — Cumulative Layout Shift | **≤ 0.1** | Unexpected visible shifting while loading |
| TTFB — Time to First Byte | ≤ 0.8 s | Server responds with content |
| FCP — First Contentful Paint | ≤ 1.8 s | Any content paints |

LCP, INP, CLS are the Core Web Vitals; TTFB and FCP support them but are
not themselves CWVs.

## Each metric

### LCP (≤ 2.5 s)

- **Causes in code:** slow TTFB; render-blocking CSS/JS; the LCP image
  loaded like a ordinary image (no `fetchpriority="high"`, lazy-loaded,
  no preload); large unoptimized hero image; client-side rendering that
  paints an empty shell before content.
- **Detect in code:** find the predicted LCP element (hero image, `h1`
  with a big font, a full-width block). Check its load strategy:
  `loading="lazy"` on it? No `fetchpriority`? Preload present?
  Server-rendered or client-rendered?
- **Fix, by priority:** speed up TTFB → inline critical CSS / stream SSR →
  preload + `fetchpriority="high"` the LCP image → convert to a modern
  format with proper `sizes` → defer everything else.
- **Measure:** lab (Lighthouse on the critical route, throttled) estimates
  in a controlled run; CrUX / RUM field data confirms real users.
  Report the percentile, not a single sample.

### INP (≤ 200 ms)

- **Causes in code:** long main-thread tasks (> 50 ms) blocking the
  response after a tap; huge render triggered by one state update;
  synchronous layout reads forced by animations; heavy third-party
  scripts running on load; event handlers doing expensive work inline.
- **Detect in code:** search for long synchronous operations in click
  handlers; renders of large lists on every keystroke; `transition: all`
  triggering layout; work done inside `useEffect` on mount;
  `Date.now()`-throttled scroll handlers (below 50 fps).
- **Fix, by priority:** remove long tasks or split them; keep handlers
  cheap and defer heavy work; use `requestIdleCallback` /
  `scheduler.yield()` / Web Workers for parsing or encoding; virtualize
  big lists; avoid dispatching expensive renders on every input.
- **Measure:** lab proxies with Total Blocking Time (TBT) — not a real
  INP — then field data (CrUX) for the real number. Also record slow
  interactions with `event-paint`-style tracing in DevTools.

### CLS (≤ 0.1)

- **Causes in code:** images without `width`/`height` or `aspect-ratio`;
  webfonts swapping to wider glyphs without `size-adjust`; injected
  content above the fold (ads, banners) with no reserved space; DOM moved
  by a transition/animation; late-inserted layout-affecting HTML.
- **Detect in code:** any image/media tag missing dimensions; `@font-face`
  without `size-adjust`/`ascent-override`; elements whose height depends
  on JS or network (measured text, dynamic banners); CSS that animates
  `height`/`top`/`margin`.
- **Fix, by priority:** reserve space for every image and iframe (dimensions
  or `aspect-ratio`); define font fallback metrics; animate only
  `transform`/`opacity`; reserve slots for injected widgets.
- **Measure:** lab CLS is synthetic and often under-reads; field CLS on
  real devices is the truth. When animating, DevTools
  "Layout Shift Regions" shows what moved.

### TTFB (≤ 0.8 s)

- **Causes in code:** server-side work (DB, rendering) before the first
  byte; missing cache; cold serverless functions; redirect chains; no
  compression for the document.
- **Fix:** cache at CDN/edge, stream SSR, warm what you can, kill
  redirects, enable compression.
- **Measure:** DevTools Network, or `curl -w '%{time_starttransfer}'`.

### FCP (≤ 1.8 s)

- **Causes in code:** render-blocking CSS and JS; stylesheet `@import`;
  giant CSS bundle; no critical CSS.
- **Fix:** inline critical CSS, preload fonts, defer non-critical JS,
  avoid `@import`.
- **Measure:** Lighthouse.

## Lab vs field

- **Lab** (Lighthouse/WebPageTest/Playwright): controlled, repeatable,
  estimates a single deterministic run. Good for regression checks, bad
  as truth for LCP/CLS on real hardware.
- **Field** (CrUX, your own RUM): real devices, real network, reported by
  percentile (p75 is the convention). Confirms.
- Rule: lab "estimates", field "confirms". A report that has only lab
  numbers says so and never claims a measured pass.