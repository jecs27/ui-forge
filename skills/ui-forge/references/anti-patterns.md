# Anti-patterns

Patterns this skill **flags when found** and **never produces**. They are
the observable symptoms of the template-mentality that plagues generated
and rushed UIs. Each lists why it's bad and what to propose instead.

| # | Anti-pattern | Why it's bad | Replace with |
|---|---|---|---|
| 1 | Three identical cards, soft shadow + purple gradient, as the default layout answer | Removes information; a row of non-informative cards is white space with clothes on; brand-templated | Layout from content needs; vary card roles or pick a table/split layout |
| 2 | Hero: giant text + two buttons + generic illustration, no value proposal | The most expensive empty promise on the page; fails the "what do I believe now" test | Headline that states the outcome, one unmissable action, honest medium |
| 3 | Entrance animations everywhere with cumulative delays | Hides content up to seconds; varies with scroll state; punishes slow users; often skips reduce-motion | ≤ 400 ms total, content visible by default, reduced-motion gate |
| 4 | `transition: all` / `will-change` everywhere / huge shadows on scrolling lists | Paint and layount churn, jank on scroll, battery burn | Animate `transform`/`opacity` only; list shadows off |
| 5 | Modal-for-everything | Highest interruption cost there is; each modal asks the user to break focus for a question that had a cheaper home | Row action → inline confirm; info → popover/expand; batch → bulk bar |
| 6 | Toasts self-dismissing unreasonably fast (≈2 s) | The only chance to see a warning evaporates | ≥ 5 s with persistent-dismiss affordance, or an inline persistent message for action-required |
| 7 | Stack of classics: icon w/o label · grey-on-white · placeholder-as-label | Each is an independent a11y regression (announced? contrast? label?) | Added labels, AA contrast, real visible labels |
| 8 | Accidental horizontal scroll / broken `100vh` mobile / clipped text at zoom 200 % | The responsive contract failed; mobile is where the user is | Reflow test at 320 px & 200 % text; `dvh`; `overflow-x` audit |
| 9 | Infinite spinners, no timeout, no error path | Dead UI is a data-loss moment on real networks | Timeout copy + retry; skeleton for shapes |
| 10 | Automatic carousel hiding key content | Content behind a timer = content hidden from slow readers; gesture discovery fails | Pause on hover/interaction; static stack or manual nav |
| 11 | Reflex optimization: `memo`/`lazy` in every PR | Bureaucracy-sized diffs that complicate the render graph and typically buy nothing measurable | Optimize only a measured hot path |
| 12 | Purple/blue gradient as the default palette, gradient text | Brand-templated; hides hierarchy behind decoration | Color from existing tokens or content need; flat accent with contrast step |
| 13 | Identical card grids / nested cards as the only structure | Every item reads equal weight; no scan path | Vary card roles or switch to table/split/list per content |
| 14 | Center-everything layout with no visual hierarchy | No focal point; squint test shows noise | One focal point left/top per reading direction; supporting content muted |
| 15 | Kicker or icon-tile stack above every heading | Decorative prefix competes with the headline | Heading first; icon only when it disambiguates |
| 16 | Hero metric row ("10k+ users") / generic testimonials / split-hero template | Unverifiable claims; layout answers every brief the same way | Outcome headline + one action; proof only with source |
| 17 | Generic "Get Started / Learn More" CTAs, emoji as decoration, glowing edges / pulsing dots | Vague action; noise that fails contrast and motion rules | Verb + object CTA; status via text + color, motion gated by reduced-motion |

## Rules for the skill itself

- A proposed "fix" that is actually one of the above is inverted: the
  finding is to *delete or simplify* it, not restyle it.
- In generated code, the skill never issues a modal where an inline
  affordance works, never self-dismisses a toast below readable time,
  never animates because animation is "polished".
- When an audit finds several of these on one screen, the report says
  "template-derived" explicitly and the fix targets the *pattern*, not
  each instance.