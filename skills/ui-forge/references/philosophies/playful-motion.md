# Playful motion

The product that feels alive: character through timing, bounce, and
responsive personality — while never hiding the content or the facts
behind the motion.

## Principles

- Motion is a voice: springs that over-shoot, button presses that squish,
  easter eggs that reward exploration. Everything moving *answers* a
  user action; nothing animates for its own sake.
- Errors still land fast and clear — humor in states, not in obstruction.
- Personality scales with trust: playful is charming on a sticker/light
  app and derailing on a bank transfer.

## Structure

- Ordinary layout (grid, columns, hierarchy as normal) — the play lives
  in the *behavior layer*, not the sitemap. Structure stays shared.
- Cards can tilt on hover; scroll can deform; but the base IA is
  pedestrian-grade so users never get lost.

## Visual treatment

- Rounded geometry, soft color pairs, emoji-safe iconography, gradient
  accents kept on small elements (a gradient button magnetizes attention
  — reserve for ONE).
- Shadows with personality (soft, colored `drop-shadow` on tiny elements) —
  cost-budgeted, never on lists that scroll (see performance rule).

## Typography and palette

- A chunky rounded sans (or a variable one) for display, casual color
  choirs (lavender/peach/mint trios), generous type scale.
- Keep body text legible ≥ 16 px and single-accent discipline even in a
  colorful direction.

## Microinteractions

- Springs for the set-piece moments: 150–400 ms with visible overshoot
  (avoid > 500 ms gestures — slow = unresponsive feel).
- Staggered entrances OK **under one rule**: total delay ≤ 400 ms and
  content LCP never delayed by the animation (rule from
  `animation-performance.md`).
- Press squish, celebrate-on-success (a checkbox that "pops"), error
  places a friendly inline message + shake-free fix guidance.
- EVERY animation has a `prefers-reduced-motion` static twin —
  non-negotiable in a moving direction.

## Dials (1–10)

- `variance`: 5–7 (set-piece moments vary, system is stable)
- `motion`: 8–9 (this is the signature)
- `density`: 3–5

## Performance cost

- Highest of the set: springs = JS or careful `transition-timing-function`
  work; tinted shadows and gradients add paint; supersets of animation
  mean a tested reduce-motion path and disciplined layers. Estimate 1–2
  extra JS deps only when the project's own stack lacks the tools;
  CSS-only variants exist.

## Works best when

- Consumer social, education apps, gamified onboarding, e-learning,
  wellness, kids/brand-casual products, or a category winning on delight.

## Avoid when

- Money, legal, healthcare, infrastructure, enterprise ops (play there
  reads as error).
- An elderly/accessibility-sensitive primary audience without extreme
  restraint.
- Anything where the demo is a screen-capture on a slow machine — the
  motion is the pitch and it must stay crisp.