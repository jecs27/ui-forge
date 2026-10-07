# Motion and feedback

Motion is a tool with two jobs: **orient** (where the change happened)
and **confirm** (the action registered). It fails when it decorates, and
fails hard when it hides content.

## The 11 rules

1. **Feedback < 100 ms perceived, or the interaction feels dead.**
   Instant visual acknowledgment of a press (a 100 ms scale/opacity
   press-state) is nearly free and kills "did it register?" doubt.
2. **Every click/tap gets an answer:** a state change, a press effect,
   an optimistic update, or at minimum a loading signal with a timeout
   message. A click with zero response is a finding.
3. **Motion has purpose.** Slide-and-fade to *relate* an element to its
   origin (a menu from its button), crossfade to *replace*, rearrage to
   *reorder*. Random bounce across the whole page is decoration.
4. **One easing family, one duration grammar** (see
   `animation-performance.md` for numbers). Motion variety (springy
   here, linear there) reads as broken.
5. **Easing < 300 ms** for component transitions, **entrances ≤ 500 ms**,
   and never a cumulative stagger that hides content — timed entrance
   delays that keep content below the fold for 2 s is a P1
   (`anti-patterns.md`: "animations as hiding").
6. **No animation without `prefers-reduced-motion` handling** (rule
   `A11Y-REDUCED-MOTION`; WCAG 2.3.3 requires an off switch for >5 s
   motion; the media query is the modern gate).
7. **`prefers-reduced-motion: reduce` → static, immediate, still-focusable**
   state, same information, no second-class layout. Hiding content via
   animation-only ("slideUp with no static fallback") is a data-loss bug
   in that mode.
8. **Direction signals.** Back-navigation slides content the way the user
   came from; forward, away. Wrong direction = the browser back gesture
   feels broken (convention on mobile web).
9. **Motion is not a status alarm.** Real errors are persistent inline
   messages, not a shake-and-forget "(shake animation)" — shake conveys
   "something's wrong-whatever", and only recent-dismissed non-critical
   events may toast.
10. **A spinner is not feedback for a tap.** Show what is changing
    (skeleton of the target region) or the exact data being waited on.
11. **Entrance-first-page marketing:** the jump is the moment whether the
    page loads with content vs animating onto a skeleton. Keep the LCP
    out of entrance animations (see CWV LCP timing).

## Detect it

- Grep for `transition: all`, `animation:`, `@keyframes` and count
  properties used (layout props → `animation-performance.md`).
- Grep for delays: `animation-delay`/`transition-delay` stacks; a
  staggered entrance (`.item { animation-delay: calc(var(--i) * 100ms) }`)
  over 10 items — 1 s of hidden content = finding.
- Look for click handlers with zero visual state change (no press state,
  no loading switch).
- Grep `prefers-reduced-motion` absence while `animation:` exists
  (scanner `A11Y-REDUCED-MOTION`).

## Verify

- Turn on `prefers-reduced-motion: reduce` in the OS/devtools and
  repeat the flows: every action still completes, nothing is hidden,
  nothing loops.
- Record the first load: is the LCP part of an entrance animation? What
  is FCP vs LCP?