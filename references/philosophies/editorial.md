# Editorial

The magazine / paper-of-record treatment: a large, composed, publication
rhythm. Type is the hero; images run like plates.

## Principles

- Layout as composition: strong grid, asymmetric but balanced spread,
  folio-style header/footer (running page label), pull-quotes.
- One clear hierarchy: the lead story (hero) vs the briefs (secondary
  tracks) — a whole page of equal-grade captions fails this direction.
- Text-first: the page reads in sequence; imagery supports, does not
  shout over.

## Structure

- 12-column-able asymmetric grid; a strong masthead/header; content
  blocks large enough to matter (no 1/12 slivers of content).
- Sections as "issues": clear page-progression, white space between
  spreads, not continuous strip.

## Visual treatment

- Photography editorial-cropped, duotone or black/white-flavored; big
  captions/labels above images (plate captions).
- Rulers (hairlines) as editorial dividers, not boxes; serif + sans
  pairing gives the "press" feel.
- No generic card shadows; layout holds itself with grid and spacing.

## Typography and palette

- Serif display (heading) + humanist sans (body) or a single serif
  family with a true italic — editorial's signature is the *mix*.
- Tight display leading, wide measure prose, generous line-height body.
- Palette: paper/slightly off-white, ink/near-black, one red-accent
  (classic broadsheet: the masthead color) kept scarce.

## Microinteractions

- Hover on story cards lifts a hair (transform) and underlines the
  headline — reading-affordance motion, not spectacle.
- Entrances modest: fade+rise ≤ 200 ms; a "folio" page-turn metaphor
  optional and cost-heavy (skip it).

## Dials (1–10)

- `variance`: 4–6 (asymmetric but grid-seated; wildness emerges in the
  spread, not the layout)
- `motion`: 1–3
- `density`: 3–6 (airy around spreads, packed within data blocks)

## Performance cost

- Moderate: 2 families (2–3 total weights), possibly a variable serif
  for display; big plate images need proper `srcset`. No animation
  dependencies.

## Works best when

- News, long-form, portfolio, cultural brand, internal "annual report"
  quality, or any product whose voice benefits from "publication".

## Avoid when

- A rapid MVP tool whose main job is data entry (the composed page fights
  the grid-density it needs).
- Mobile-first utilitarian flows (a crew needs a symmetrical stack, not a
  broadsheet).
- Brands wanting friendliness/digital-native (editorial can read
  formal-cold).