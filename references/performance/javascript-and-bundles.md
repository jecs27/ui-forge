# JavaScript and bundles

JavaScript is the main-thread tax: parse, execute, and long tasks all
steal time from INP. The budget is a convention, not a standard —
adjustable in `scripts/budgets.default.json` and `PROFILE.md`.

## Budgets (defaults)

- **≤ 170 KB gzip** of JS on mobile critical routes (initial load)
- **≤ 50 KB gzip** per secondary-route chunk
- No single chunk over the gzip budget after splitting
- These are starting points; a dashboard app and a marketing page do not
  deserve the same number. Set real ones in `PROFILE.md`.

## The main techniques

1. **Route splitting** — `import()` per route; never one bundle for the
   whole app.
2. **Interaction splitting** — `import()` inside the event that needs it:
   a PDF export, a chart, a code editor loads on first use, not at boot.
3. **Dead code** — tree-shaking requires ESM + named imports; delete
   unused exports; watch for barrel files that pull whole modules.
4. **Named imports** for libraries with forests:

```js
// bad: whole lodash packaged
import _ from 'lodash'
// good
import { debounce } from 'lodash-es'
```

5. **Heavy-library alternatives** (lighter for the same job): moment →
   Temporal / Intl / date-fns-lite; lodash → native; `swiper`/carousel
   libs → CSS scroll-snap; syntax highlighters → only load the subset;
   WYSIWYG → `<textarea>`/`contenteditable` until the job demands more.
6. **Duplicates** — two copies of React from indirect deps is a classic;
   the bundle analyzer reports it.
7. **Don't ship what the server provides** — SSR the initial HTML so the
   client bundle is interaction-only.

## Long tasks (> 50 ms)

- The interactive threshold; a long task freezes the page and directly
  inflates INP.
- **Split:** chunk parsing/serialization into slices of work;
  `scheduler.yield()` in loops that run long; `requestIdleCallback` for
  non-urgent post-load work (analytics hydration, prefetching the next
  route).
- **Move off-thread:** Web Workers for image processing, code parse,
  large data transforms. Workers swap main-thread stall for message
  latency on the result — prefer when the work is heavy and batched.

## Hydration

- Client-side render whole app on load = blank until JS = worst case.
- **Islands / partial hydration:** hydrate interactive islands, leave
  static HTML. **Progressive:** hydrate on interaction or idle.
- **Server Components** where the framework supports them — data and
  templates become HTML, JS ships only for interactivity.

## How to analyze the bundle

Do **not install** an analyzer without permission. Without one:

- `package.json`: count direct deps; eyeball known-heavy names carried
  whole (custom rule `PERF-HEAVY-IMPORT`).
- DevTools → Sources → heap/size of loaded modules (production build local).
- Build output: report per-chunk gzip sizes from the bundler's own log
  (Vite prints them; Next/Webpack via `--stats`).
- Grep for `import X from 'heavy'` vs `from 'heavy/submodule'`.

With the project's already-installed tooling (e.g. `vite-plugin-visualizer`,
`@next/bundle-analyzer` if present) — run it, it is part of the project,
and it is a read operation.

## Measure it

- gzip size of the served entry + chunks (Network tab, or build log).
- Lighthouse TBT and "Unused JavaScript" (estimated, not a true field
  number).
- Field INP from CrUX/RUM is the final word on whether the JS strategy
  is working.