# Third-party scripts

Analytics, chat, maps, pixels, and "one small widget" — the category that
turns a 100 KB app page into a 2 MB one and adds seconds to LCP/CLS.
Nothing here is a verdict against using them; it is a verdict about
*loading* them at boot.

## The cost model

- A third-party script costs: bytes, main-thread parse/execute time,
  network contention on the critical path, and a private HTTP waterfall
  you cannot fix. **Detect:** an ad or tag manager whose `async` script
  still delays the LCP because the browser races it against your fonts.

## Loading rules (in priority order)

1. **Measure the cost before approving.** Turn the script off for one
   recorded session; compare LCP/CLS/INP. If the delta is invisible and
   the vendor is optional, drop it.
2. **`defer` or `async`.** Never a render-blocking classic script
   (rule `PERF-SCRIPT-BLOCK`). `defer` preserves order, `async` does not;
   for independent embeds `async` is fine.
3. **Load after interaction** — a chat widget, a video player library, a
   heavy visualizer: the `<script>` is inserted at `pointerdown`/focus on
   the affordance, or at the first `IntersectionObserver` entry.
4. **Facade pattern:** render a cheap static image/button that *looks*
   like the embedded map/video/chat; hydrate the real component only when
   the user taps it. Common for maps and videos; a facade costs ~1 asset
   instead of the vendor's whole payload.
5. **`fetchpriority="low"`** on third-party scripts whose timing is not
   urgent, so they never beat your own critical resources.
6. **Cap the list.** Default budget: ≤ 5 tracked third-party scripts
   (in `budgets.default.json`). Each above the cap is a finding with the
   vendor named and its bytes measured.
7. **Self-host only when the license allows.** Same asset served from your
   origin removes the third-party waterfall but assigns you its
   maintenance and its privacy obligations — do not self-host just to
   make the number look better.

## Consent and privacy as a performance lever

- Consent-managed tags are usually *not* loaded until the user accepts —
  turn this into a win: the pre-consent page has the third-party category
  dark by default, which is faster and more private simultaneously.
  No CMP reaches into a page that lacks the capability anyway.
- CSP: third-party scripts need their own site allow-list; a tightened
  CSP both hardens the page and documents exactly what you load.

## Detect in code

- Grep `<script src=` in HTML; tag classic scripts without `defer`/
  `async`/`type="module"` (`PERF-SCRIPT-BLOCK`).
- Inventory `<script>`-loaded vendor code, tag managers, chat, maps,
  pixels: count them, estimate bytes from their own known sizes (mark
  estimated if not measured).
- Grep for embeds (`<iframe src="...maps...">`, `chat`, `intercom`,
  `grecaptcha`) that mount at boot rather than on intent.

## Measure it

- Network tab: bytes/requests by third-party origin vs your origin; the
  time the critical path waits on a vendor request (waterfall).
- Lighthouse "Third-party summaries" (when run with permission) tabulates
  impact per script.
- A/B of page without vendor vs with — the honest number for "is this
  worth our users' seconds".