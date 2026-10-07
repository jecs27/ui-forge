# Components and states

Every interactive component is really a set of states. A component whose
list of states is untracked is a component that will ship half-baked and
will need to be revisited at the worst moment.

## The state checklist

A component owns as many of these as its role suggests:

`default · hover · focus-visible · active · disabled · loading ·
empty · error · success · selected · skeleton`

For a **form field**: default, focus, filled, error, disabled, help-text —
skipping the error state visually until the user hits submit is a finding.
For a **cards grid**: default, hover (if interactive), selected (if part
of selection), skeleton (first paint), empty (no results).

Rule: every state is either **implemented** or **listed as pending** in
the report. "It inherits the default" counts as implemented only when the
design genuinely wants that (some minimal styles do — state it).

## Buttons

- **Just three tiers** — primary / secondary / tertiary — as tokens.
  A page with five button styles is a design-system leak.
- **Labels are verbs + object**, not vague ("Save", "Publish draft",
  "Download CSV") — never "Click here" or "Ok".
- **Touch target:** 44 px recommended, 24 px WCAG minimum
  (`A11Y-TARGET-SIZE`). A 32 px icon button fails the recommendation but
  passes AA — the report says so.
- **Focus visible** on every interactive element (`:focus-visible`, see
  `keyboard-and-focus.md`).
- **Disabled** state must be visually distinguishable from enabled *and*
  still legible; add a tooltip/explanation when a "disabled" actually
  means "why can't I click this".

## Behaviors per common component (short)

**Tables:** real `<table>` headers with `scope`; row hover without a
reflow (transform highlight); empty state; long-celled truncate vs
scroll decision; tabular numerals.

**Modals/dialogs:** `<dialog>`; focus trapped and returned; Esc closes;
dismissable by backdrop click with a visible close control; content is
scrollable to the last row with focus visible.

**Menus (dropdown/context):** keyboard nav (arrows, type-ahead);
`role="menu"` semantics; closes on Esc and click-outside; no focus loss.

**Tabs:** `role="tablist"` + `aria-selected`; arrow-key switching;
panel refocus rules; lazy panels below the fold.

**Toasts:** focus moves or announced (`aria-live="polite"`) for messages
that carry an action; duration long enough to read (≥ 5 s is the common
floor — convention); never toast-toast when it is really an inline
error the user must act on.

**Tooltips:** appear on hover *and* focus; not the *only* place a label
lives (a tooltip that substitutes for a visible label is an a11y +
discoverability finding); disappears when pointer/tab moves away.

## Detect it

- Inspect each interactive component in code for the state list above;
  grep the component file for `disabled`, `aria-selected`, `:hover`,
  `:focus-visible`, skeleton/empty branches. Missing ones are they
  unhandled or intentionally defaulted?
- Grep button styles: count distinct background/border combos used as
  buttons (5+ → no system).
- Grep `title=` / tooltip-only labels on inputs and controls.

## Verify

- Walk the states manually on a real render (or the nearest dev server):
  hover each, focus each, submit empty, submit wrong, submit success,
  network-off. The report answer is "states 8/11 implemented, empty +
  error on the grid pending" — not "looks fine to me".
- Automated a11y scan (axe/AC-axe if installed) catches focus/contrast
  — but states are a design-audit task, not an automated one.