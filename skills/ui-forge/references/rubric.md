# Rubric — scoring

Total: **100 points**, seven categories. Score each category from its
starting budget down, deducting per finding, then sum.

| Category | Points | What it covers |
|---|---:|---|
| Performance | 30 | Core Web Vitals, weight, bundles, rendering, images, fonts, third-party scripts |
| Accessibility | 20 | WCAG 2.2 AA, keyboard, focus, semantics, contrast |
| Hierarchy and layout | 15 | Focal point, spacing scale, typography, grid, readability |
| Interaction and states | 15 | All component states, feedback, forms, errors, empty states |
| Consistency and system | 10 | Tokens, reuse, coherence across screens |
| Responsive | 5 | Behavior at 320–1440 px, touch, safe areas |
| Content and microcopy | 5 | Clarity, useful errors, empty states |

## Severity levels

| Level | Meaning | Examples |
|---|---|---|
| **P0 — Blocker** | The product cannot be used, or accessibility fails critically | Form unusable by keyboard; LCP > 4 s; contrast so low text is unreadable |
| **P1 — High** | Clearly degrades the experience or blows a budget noticeably | 400 KB of unused JS on the critical route; no focus indicator; 32 px touch targets |
| **P2 — Medium** | Visible improvement, no urgency | Spacing scale inconsistent between two screens; missing `empty` state |
| **P3 — Polish** | Fine detail | `text-wrap: balance` missing on an `h1`; tabular numerals off in a data table |

## Scoring rules

1. **Every deducted point cites evidence.** `file:line`, a measured
   metric, or a scanner finding ID. A deduction with no evidence is not
   scored — drop the finding instead.
2. **Distinguish measured from estimated.** A number from a real
   measurement (Lighthouse, WebPageTest, bundler stats, the scanner's
   objective counts) is *measured*. Anything reasoned from static code
   inspection is *estimated*. Estimated findings deduct **at most half**
   what the same finding would deduct if measured, and the report labels
   them `estimado`.
3. **Never 100/100 without real measurement.** With no measurement tool
   available at all, the performance category caps at **27/30** (i.e. the
   total caps at 97 before any deduction) and every performance finding
   carries the `estimado` label. State this cap in the report header.
4. **Show category subtotals and the total**, plus one sentence naming
   the category that limits the score the most.
5. **No double-counting.** One root cause is one deduction. If a missing
   token causes both "magic color" and "inconsistent", deduct once under
   the root cause and mention the symptom.
6. **Findings outside the agreed scope are not scored.** Score only the
   files and routes named in the audit scope.

## Deduction guidance

The exact deduction is a judgment call, but stay inside these bands so
scores are comparable between audits.

| Severity | Typical deduction |
|---|---|
| P0 | 8–15 points in its category; if the category would go below 0, floor at 0 |
| P1 | 4–8 points |
| P2 | 2–4 points |
| P3 | 1 point |

If a category's findings exceed its budget, floor that category at 0 and
say so ("rendimiento: 0/30, supera el presupuesto de la categoría").

## Worked micro-example

Scope: one landing page. Performance category starts at 30.

- `PERF-IMG-DIM` on 4 images below the fold → estimated, P2 → −3
- No measurement tooling available → cap applied, labeled `estimado`
- LCP image is lazy → estimated P1 → −6

Performance = 30 − 3 − 6 = **21/30**, labeled *estimado por análisis
estático*.

Report line:

```
| Rendimiento | 21/30 | Imágenes sin dimensiones; lazy en LCP (estimado) |
```

## What limits the score

After scoring, write one sentence naming the single category with the
largest loss and why. This is the headline recommendation: fixing that
category first yields the biggest point gain.
