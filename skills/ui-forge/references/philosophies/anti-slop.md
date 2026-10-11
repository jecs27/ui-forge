# Anti-slop

Not a visual style — a *veto*. Use as a filter over the other five:
whatever the direction, it must not devolve into the sludge every
template generates. This file names the sludge.

## The sludge list

1. **Three identical cards with soft shadow + purple gradient** as the
   answer to every content question. A row of uniform cards says "we had
   a template", not "we had ideas". If cards, vary the fact they
   represent (a summary card ≠ a people card ≠ a log card).
2. **Hero = giant text + two buttons + a generic illustration**, no
   proposal of value. The hero says *the thing the user needs to
   believe*; if the words could apply to any SaaS, it is filler.
3. **Entrance animations on everything with cumulative delay** — the
   opposite of polish. Stagger > 1 visible second of hidden/revealed
   content fails the user (see `motion-and-feedback.md`).
4. **`transition: all`, `will-change` everywhere, enormous shadows on
   scroll lists** — paint budgets vaporized for an effect nobody asked
   for (scanner `PERF-TRANS-ALL`, `PERF-ANIM-LAYOUT`).
5. **Modal for everything** — a confirm modal for a row-action that
   needs no confirmation, an info modal for a paragraph that fits in a
   tooltip. Modals interrupt; use them only when there's a reason to
   pause the page.
6. **Toasts that self-dismiss before reading** (~2 s) and a missing
   error/empty identity. A toast is a high-street billboard; billboards
   don't flash-by in 1.5 s.
7. **Icon without label + light-grey-on-white text + placeholder-as-label.**
   Three classics in one row; each fails a different a11y rule
   (`semantics-and-aria.md`, `color-and-contrast.md`, `forms.md`).
8. **Accidental horizontal scroll; `100vh` broken on mobile; text
   clipped at font-size bump.** Responsive is a test, not a hope
   (scanner `UX-VH-MOBILE`, see `responsive.md`).
9. **Infinite spinners with no timeout or error path.** Network makes
   "it'll load" a lie daily (see `microcopy.md`: honest wait copy).
10. **Automatic carousels hiding key content** — content behind a
    timer is content hidden from the user who was reading.
11. **Premature optimization as busywork:** blanket `memo`/`lazy`/`memo`
    recommendation without measurement, "optimized" code slower than the
    boring version (`react-and-frameworks.md`).

## How anti-slop applies in an audit

- Every proposed direction must print a one-line "slop check": which
  item in the list it *doesn't* do and why.
- If a proposed fix _is_ one of these by reflex ("add a modal here",
  "three stat cards"), the finding is to remove it, not restyle it.
- The scanner's low-confidence heuristics exist to catch these patterns in
  the wild (e.g. repeated `transition: all`), and the report treats them
  as symptoms of a template, never as intentional choices.