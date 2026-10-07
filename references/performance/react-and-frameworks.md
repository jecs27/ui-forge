# React and frameworks

Framework-specific performance: the common causes of slow UIs in modern
component frameworks, in order of how often they actually matter.

## React

The rule for optimization: **measure first, then optimize.** `memo` added
by habit is worse than no `memo` — it costs a shallow-compare on every
render and bribes you to stop thinking about the real render graph.

### Re-render check

- **What actually re-renders on an interaction.** DevTools → React
  Profiler shows which components re-rendered and why. A pure click that
  re-renders half the tree is the problem; `memo` on one leaf is a
  symptom-side fix.
- **State placed too high in the tree**: a `count` in a context/provider
  at the root re-renders every consumer. Hoist it to the component that
  needs it.
- **Context that changes often** (a loading flag updating per request):
  split contexts, or keep the volatile state local.

### Curated fixes (only after seeing the render graph)

- **`useMemo`/`useCallback`/`memo`** — for *expensive* computations or
  children that re-render because a parent repasses a new function/object
  each render. Prove it with the profiler before adding.
- **`key` stability**: `key={index}` on a sortable/filterable list
  remounts rows and loses state; use a stable id. Do not *add* `key={index}`
  to appease a lint rule on a static list — it is harmless and pointless.
- **`useTransition`/`useDeferredValue`**: a slow filter input can defer
  the expensive re-render of the list, keeping the field responsive.
- **`lazy` + `Suspense`** for route-level and heavy-interaction components.
- **No derived state in effects**: `useEffect(() => setX(compute(y)), [y])`
  causes a double render and a flash; compute during render instead.
- **Data that the server can hand over** (initial list, post content):
  render it in the SSR/SSG HTML instead of fetching + `useEffect` on
  mount — that is a whole empty-frame-and-spinner cycle.

## Next.js / Remix / Astro / SvelteKit / Vue+Nuxt

The equivalent rules per framework — short form:

- **Next:** server components by default for data/static content; client
  components only where interactive; `<Image>` for the LCP image (built-in
  sizing and priority); route groups to shape JS per route; streaming
  `Suspense` to push HTML before data resolves.
- **Remix:** loader data renders server-side by default (no client fetch);
  mutations in actions; the fetch cache is a non-issue — respect it.
- **Astro:** islands by philosophy — a full-client Vue/React component is
  opt-in; keep interactive islands small and static the rest.
- **SvelteKit:** `{...}` re-render hygiene is automatic; the lever is
  *which data loads on the server* vs the client. Svelte stores update
  subscribers; keep heavy stores local.
- **Vue/Nuxt:** reactivity is granular — the cost pattern is different;
  big risks are a bloated `app.js` from eager global registration and
  watchers doing long synchronous work. `defineAsyncComponent` for heavy
  pieces, route-level prefetching mindful of budgets.

Shared rule across all: **images via the framework's own component**
(`<Image>`/`<img>` with `nuxt-img`) — infrastructure the framework
maintains, instead of hand-rolling `srcset`.

## Data fetching

- **Cache and deduplicate** identical requests (React Query/SWR if the
  project already uses one; otherwise framework-level caching) so a
  screen's refetch is not a wall of spinners.
- **Optimistic updates** where the operation is reversible-ish and fast:
  reflect the intent immediately, reconcile on failure. Good for toggles,
  votes, small edits. Not for money/security finalities.
- **Prefetch on intent**: hover/visibility of a route prefetches its
  data; the click then is instant instead of a wait.

## Detect in code

- Grep `memo(`, `useMemo`, `useCallback` — count how many have a comment
  or measurement justifying them (most won't; that is a finding, P3).
- Grep `useEffect` that ends in a `setState`/`fetch` on mount — candidate
  for server-side data.
- Grep `key={index}` in `.map` over dynamic lists.
- Grep top-level `createContext` with a state that updates on a timer or
  per-request.

## Measure it

- React DevTools Profiler: sessions per interaction, render count, which
  components.
- React DevTools "Highlight updates when components render" for a visual
  of the render graph.
- Lighthouse TBT + field INP from RUM are the user-visible verdict.