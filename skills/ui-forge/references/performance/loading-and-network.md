# Loading and network

How the page assembles: critical resources, connection hints, caching,
compression, and avoiding request waterfalls.

## Critical resources and hints

- **Critical =** what the first render needs: HTML, critical CSS, the LCP
  image when big enough to matter. Everything else is deferred.
- **`<link rel="preload" as="style">`** for the critical stylesheet when
  it is not inlined. Use sparingly; a `preload` adds a priority claim.
- **`<link rel="modulepreload">`** for the modules the entry route imports
  synchronously; the module loader fetches them ahead of use.
- **`fetchpriority="high"`** on the LCP image; `fetchpriority="low"` on
  low-value resources (below-fold images, off-screen widgets) so they
  stop competing.
- **`<link rel="preconnect">`** to the origin(s) your critical scripts
  and CSS come from (warm DNS + TLS early). One or two, not ten.
- **`<link rel="dns-prefetch">`** as the lighter fallback for origins the
  user may visit *later* (auth, checkout). It guesses; do not rely on it
  for the critical path.

Mal → bien:

```html
<!-- bad: browser discovers the hero image late, no hints -->
<img src="/hero.jpg">
<script src="https://cdn.x.com/app.js"></script>

<!-- good -->
<link rel="preconnect" href="https://cdn.x.com">
<img src="/hero.jpg" fetchpriority="high" width="1600" height="900">
<script src="https://cdn.x.com/app.js" defer></script>
```

## Caching and transport

- **`Cache-Control`:** long `max-age` (or `immutable`) for hashed
  asset URLs; `no-cache` (revalidate) for HTML; never re-download what
  did not change. Fingerprinted names (`app.a1b2c3.js`) make this safe.
- **Compression:** Brotli preferred, gzip fallback, over HTTP/2 or 3.
  Enable for HTML/CSS/JS/SVG/JSON; not for images and video (already
  compressed).
- **HTTP/2–3:** connection reuse kills most connections-per-host problems;
  that is *why* bundlers merge files. Do not hand-split files to "avoid
  HTTP/1.1 head-of-line" on a modern server.

## Request waterfalls

A waterfall: resource B cannot start until A returns, and so on. Chain
>2–3 deep on a critical route is a smell.

- **Detect:** Network tab sorted by "Start time"; look for straight
  diagonal lines of dependent requests.
- **Fix:** parallelize independent fetches (`Promise.all`) instead of
  nesting; server-render or preload the next-needed data; chunk routes so
  a click fetches one file, not a chain.
- **Prefetch by intent:** `router.prefetch()` on hover/`IntersectionObserver`
  for the *next* screen, not everything.

## Loading states

- **Skeleton vs spinner:** skeleton reserved-space placeholders preserve
  layout (no CLS) and show structure; a spinner says nothing about
  shape. Use skeletons for data views, spinners only for tiny inline
  actions.
- **Progressive loading:** render what is ready (`Suspense`
  streaming), fill the rest as data arrives. Default route in its shell
  beats a blank page with one spinner.
- **`Suspense`:** wrap async sections so the rest of the page is
  interactive while they resolve; an entire-app suspense boundary is the
  same as a spinner wall — avoid.

## How to detect it (code)

- Grep `<link rel=` for preload/preconnect; check the LCP image for
  `fetchpriority`.
- Grep CSS for `@import` (serial, render-blocking) — replace with
  `<link>` or bundler imports.
- Check `index.html` scripts: any classic `<script src>` without
  `defer`/`async` blocks rendering.
- Look for Promise chains in data fetching that serialize requests that
  are independent.

## How to measure it

- DevTools Network: waterfall shape, per-resource timing, transfer size
  vs size.
- `curl -sI <url>` for caching headers and `server` compression.
- WebPageTest filmstrip shows what the user actually sees; compare with
  the Network waterfall to find what the LCP waits on.