# Animation performance

Animation is cheap when it stays on the compositor and expensive when it
touches layout or paint. The compositor works even during long tasks on
the main thread — that is the whole trick.

## Animate only `transform` and `opacity`

- `transform` (translate/scale/rotate) and `opacity` are compositor
  properties: the browser can run them without re-layout or (usually)
  re-paint.
- Animating `width`, `height`, `top`, `left`, `margin`, `padding`,
  `box-shadow`, `filter`, `background` forces layout and/or paint per
  frame — jank above 60 fps, and INP damage alongside.
- **Same effect, cheap:** slide in → `transform: translateX(...)`;
  fade → `opacity`; expand smoothly → animate `transform: scale`
  inside a fixed-size clipped wrapper, or reflow once and time the easing.
- Cards that "raise" → transition `transform: translateY(-2px)`, keep the
  shadow static (or use a pseudo-element whose opacity fades).

## `will-change`

- Reserve a compositor layer *before* the animation starts and release it
  after. Overuse (`will-change: transform` on everything) burns memory and
  creates layers the page never animates — worse than nothing.
- Use on a moving element right before its animation, only while it moves
  and only on the property that moves. Prefer `will-change: transform`.

## `transition: all`

- Opts every animatable property into a transition; a parent-state change
  then triggers expensive property transitions you never intended (rule
  `PERF-TRANS-ALL`). List the properties:

```css
.card {
  transition: transform 200ms ease, opacity 200ms ease;
}
```

## Durations and easing

| Interaction | Duration |
|---|---|
| Micro-interaction (hover, button press) | 100–200 ms |
| Component transition (menu, dialog) | 200–300 ms |
| Page entrance | ≤ 500 ms |

- One easing curve family per product (e.g. `cubic-bezier(.2, .8, .2, 1)`
  for enters, a slightly snappier one for exits). Curves that read as
  "bouncy gimmick" are a design smell, not a performance problem — but the
  bouncier the curve, the more frames it needs. Keep it ≤ 300 ms of
  visible work per transition.

## Respect `prefers-reduced-motion`

```css
@media (prefers-reduced-motion: reduce) {
  .card, .menu { transition: none; }
  [data-motion] { animation: none; }
}
```

- And for JS-driven motion, check `matchMedia('(prefers-reduced-motion: reduce)')`
  and run the static path. Rule `A11Y-REDUCED-MOTION` flags projects with
  animations but no reduced-motion block.

## Scroll-driven animation

- CSS scroll-driven `animation-timeline: view()` gets the compositor; the
  JS `scroll` listener approach needs `passive: true`.
- If JS must observe scroll, use `IntersectionObserver` to toggle
  visibility classes — the observer fires on compositor ticks, a raw
  `scroll` listener without `passive` blocks scrolling.

## Detect in code

- Grep `transition:` for `all` and `transition-property: all`.
- Grep `@keyframes`/`transition/animation` for `width|height|top|left|margin`
  in the animated block.
- Grep `will-change` and count elements carrying it.
- Grep `addEventListener('scroll'`; check the options object for
  `{ passive: true }` (rule `PERF-SCROLL-LISTENER`).

## Measure it

- DevTools Performance: a scroll/drag recording; look for long
  "Update Layer Tree"/"Paint" tasks and a frame rate well below 60.
- "Frame rate" graph in Recording: at 60 Hz, ~16.7 ms per frame; a
  shimmer line at debugging is a hit on the animating element.
- Compare before/after with the SAME environment and a fixed interaction
  (aim for identical conditions so the delta is the change, not the lab).