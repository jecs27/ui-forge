# measure.md — measurement guide (opt-in only)

Measurement turns "estimado" into "medido". It is **always opt-in**:
nothing here runs without your approval, and nothing gets installed
without your approval and the exact command shown.

## 0. The honesty contract

- Without a measurement tool and user permission to run it, the skill
  labels findings **"estimado por análisis estático"** and says so out
  loud. It never invents numbers.
- Every measured number records its **environment**: tool + version,
  device profile, URL/path, run count. Comparisons are only fair against
  the same environment.
- "Improved" is only claimed when the same environment measured before
  and after shows it.

## 1. Inventory tools already present (read-only)

Check for tools the project already has, and use them before suggesting
anything new:

- `node_modules/.bin/` — is `lighthouse` there? `playwright`/`@playwright`?
  A bundler analyzer (vite analyzer, `next/bundle-analyzer` config)?
- A `test/`/`e2e/` setup with Playwright: it can record performance logs
  without extra installs.
- DevTools you can drive yourself: Performance, Network, Lighthouse tab.

"A tool the project already has" is not an installation: running it is a
read operation on the build output. State the exact command anyway and
confirm — then run it.

## 2. If a tool is missing — ask

Show the user:

- the exact command (e.g. `npx lighthouse <url> --preset=desktop`),
- that it downloads the tool,
- that it is a one-time install into your environment, not the project,
- offer the read-only alternative (DevTools/static estimates) and wait.

Default answer is **no**. Mark findings estimated and move on.

## 3. Protocol when measuring

1. **Environment lock.** Note: tool version, network profile (throttle
   CPU 4×, network Slow 4G for mobile per the 2026 Lighthouse defaults),
   viewport (mobile: 390×844 3× DPR; desktop: 1350×940 1×), URL or the
   served route.
2. **Three runs per condition.** Report the **median**, not the best
   (median of LCP/INP/CLS; the median of any field you record). A
   single run is a benchmark, not a measurement.
3. **Rows to record** (see `baseline.json` schema below): LCP, INP
   (or TBT as the lab proxy — label it TBT, never INP), CLS, total
   transfer weight, JS bytes (gzip), request count, DOM node count.
4. Also record **TTFB** and **FCP** (supporting, not CWV).

## 4. Lab vs field

| Source | What it is | Use for |
|---|---|---|
| Lighthouse / WebPageTest / Playwright perf log | Lab: one deterministic environment | Budget regressions, before/after of a fix |
| CrUX / your RUM | Field: real users by percentile (p75) | Confirming the lab estimate; the final verdict |

If the user has field data (CrUX URL, a RUM dashboard), use it instead of
guessing. Otherwise say "sin datos de campo" and mark the category
`estimado`.

## 5. Baseline JSON schema (`.ui-forge/baseline.json`)

```json
{
  "date": "2026-10-06",
  "skill_version": "0.1.0",
  "environment": { "tool": "lighthouse", "tool_version": "12.x", "profile": "mobile-throttled", "route": "/" },
  "runs": 3,
  "metrics": {
    "lcp_ms": 2400,
    "inp_ms": null,
    "tbt_ms": 180,
    "cls": 0.05,
    "ttfb_ms": 600,
    "fcp_ms": 1200,
    "js_gzip_kb": 210,
    "css_gzip_kb": 40,
    "images_kb": 900,
    "requests_total": 38,
    "dom_nodes": 2100
  },
  "measured": true
}
```

`measured: false` + all-null metrics is a valid honest state — write it
when nothing could be measured, so `compare` can tell the user there is
no baseline yet.

Every number must come from a real run in that environment. Nothing here
is permitted to be a guess.