# Visual hierarchy

Hierarchy is the reader's eye path: what reads first, second, last. It
should match the product goal of the screen, not the sexiest element.

## Rules

- **One focal point per view.** One element is clearly the most important;
  everything else supports it. If two things fight (a giant headline *and*
  a pulsing button), neither wins.
- **Size, weight, and color are signals.** A single level of change — one
  bigger bolder headline — reads as hierarchy. Changing size **and** color
  **and** weight together reads as shouting.
- **One primary action per screen.** Even on dashboard/settings, one
  action is the "do this next" default. Secondary actions reduce to
  lower visual weight in the same position each time.
- **Proximity groups.** Things closer together are "one group"; related
  controls sit nearer each other than to unrelated ones. This is cheaper
  and clearer than drawing boxes around every group.
- **Contrast is the lever, not color.** Dark text on light, not dark on
  mid-grey. Reduce secondary text to a *reduced* contrast step, never to
  unreadable (see `color-and-contrast.md` for the numeric floor).
- **Whitespace implies importance.** More space around an element makes it
  read as more important; a cluttered top section floods the viewport with
  equal-weight noise.

## Scan patterns and reading direction

- **Design for scanning, not reading.** Users scan in F (text-heavy),
  Z (sparse landing), or lawn-mower (list/grid) paths before they read.
  Put the value proposition and primary action on that path; details off it.
- **Order follows the locale.** Latin scripts read top-down, left-right;
  RTL locales (Arabic, Hebrew) mirror the path. Never hardcode
  `left/right` order in a fix — use logical properties (`inline-start`)
  or the project's RTL setup, and flag an `ml-/mr-` chain as a finding.
- **Hierarchy check in code:** the first scannable block (hero/header)
  must hold the H1 + primary action; a nav, badge row, or kicker stack
  above them pushes the focal point off the scan path.

## The squint test

Look at the rendered screen, squint until details blur. The thing you can
still see as "a shape" is the focal point. If you see three shapes pulling
attention, hierarchy failed. Run it on a real render, not a spec — this is
a heuristic that works because the eye is the measurement device.

Mal → bien:

```text
BAD:  H1 HUGE GIGANTIC / button PRIMARY glowing / sidebar image big /
      nav item bold — everything shouts, nothing leads.

GOOD: Strong H1 lead, one glowing primary button, muted nav,
      supporting content at contrast step below.
```

## Detect it (in code and render)

- **In code:** how many elements carry the "important" signals — check
  font sizes, weights, accent colors, and the number of primary-style
  buttons per view. More than one element in the top size class = a
  hint of a fight.
- **In render:** the squint test; also a `filter: blur(8px)` screenshot —
  blur removes text and forces shape salience.
- **In real usage:** what does a new user click first? If it is not the
  intended action, the hierarchy lied.

## Measure / verify the change

- Fix on the rendered page, re-run the squint test.
- If an analytics event exists for the conversion action, compare click
  rate before/after; hierarchy is legible in that number.