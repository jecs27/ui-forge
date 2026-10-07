# Rendering and CSS

How the page paints and re-paints. The two enemies are layout work on the
main thread and a DOM so big the simplest selector is slow.

## Layout thrashing

Alternating *read* and *write* of layout forces synchronous reflow after
each read (`el.offsetHeight` inside a loop mutating styles). The browser
cannot batch — it recalculates layout on every read.

```js
// bad: read, write interleaved → reflow per iteration
for (const el of items) {
  const w = el.offsetWidth      // read (forces layout)
  el.style.width = w / 2 + 'px' // write (invalidates)
}
```

- Batch reads first, writes second.
- Where a list must expand/collapse, animate `transform`/`opacity`, not
  `width`/`height`.
- `content-visibility: auto` with `contain-intrinsic-size` tells the
  browser the off-screen section's reserved size, so it can skip its
  layout entirely:

```css
section.long {
  content-visibility: auto;
  contain-intrinsic-size: auto 480px; /* approximates the section's size */
}
```

## DOM size

- **> 1 500 nodes: warn. > 3 000 nodes: a real problem.** A bigger DOM
  makes every style recalc and selector match costlier.
- Detect via DevTools Performance memory timeline, or Lighthouse
  "Avoid an excessive DOM size" (which lists node counts).
- Fix: fewer wrapper divs, `<ul>` instead of divs per row, virtualization
  for long lists, split mega-forms, lazy content in tabs.

## Expensive selectors and CSS

- **Cheap selectors:** class last or only; avoid `*` and universal
  descendant rules on hot paths. Real impact only shows with a big DOM —
  don't micro-optimize selectors on a 300-node app.
- **`@import` in CSS** is serial and render-blocking — replace with
  `<link>` or bundler imports (rule `PERF-CSS-IMPORT`).
- **Critical CSS:** inline the first-paint styles; the rest loads
  non-blocking. Generates a second stylesheet a device never needs to
  parse at FCP.
- **`contain`** to isolate heavy regions (a map, a large table) so their
  layout does not invalidate everything else: `contain: layout paint`.

## Long lists

- **> 100 visible-ish elements** that all render: virtualize
  (render the window) or paginate. Native `<dialog>`, tabs, or
  `content-visibility` cover simpler cases without a dependency.
- Infinite scroll + virtualization is the standard stack-heavy pattern;
  ask whether the product is a timeline or a finite list before adding it.

## Expensive paint properties

- `box-shadow`, `filter` (blur, drop-shadow), `backdrop-filter` are
  paint-hungry. On elements that animate or scroll, they turn a cheap
  frame into a blur pass on every frame.
- Prefer solid borders/borders + low-count shadows; keep filters off
  animated elements (covered in `animation-performance.md`).

## Detect in code

- Grep `.offsetHeight/offsetWidth/scrollTop` next to style writes (layout
  thrash, heuristic).
- Grep `@import` in `.css` files (rule `PERF-CSS-IMPORT`).
- Grep `transition: all` and `transition-property: all`
  (`PERF-TRANS-ALL`), and animated `width|height|top|left|margin`
  (`PERF-ANIM-LAYOUT`).
- Count DOM in multi-page apps from one rendered critical route
  (DevTools cons 'document.body.querySelectorAll('*').length` — a read).

## Measure it

- Lighthouse "Avoid an excessive DOM size" and "largest contentful paint"
  labs; DevTools Performance for a scroll/render recording to see long
  Raster/Paint/Update Layout tasks.
- Search for forced reflows: Performance recording tagged with a red
  "Forced reflow" warning over a script marker.