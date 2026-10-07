# Forms

Forms are where users most often abandon a product, and where a11y errors
cluster. The rules below are the difference between a form that feels
broken and one that feels competent.

## Labels

- **Every field has a visible label, programmatically associated**
  (`<label for>` or wrapping). Placeholders are **never** labels: they
  vanish on typing, fail screen readers unless duplicated as a visible
  label, and strain working memory.
- Redundant labels inside a legend/grid can be hidden *with a real
  technique* (`.visually-hidden`) — the a11y name must stay.
- **Optional vs required:** when most fields are required, mark the
  *optional* ones "Optional" instead of asterisking every required field.
  No legend, no asterisk-only required marking, no color-only markers.

## Types, keyboard, and input

- Correct `type`: `email`, `tel`, `url`, `number`, `date`,
  `password`. `inputmode` for numeric keypads (`inputmode="numeric"`,
  `inputmode="decimal"`), `autocomplete` spelled out
  (`autocomplete="name"`, `"email"`, `"cc-number"`, `"one-time-code"`).
- Never disable autocomplete unless the data is genuinely sensitive
  (one-time codes, some banking) — and even then think twice; annoying
  autofill beats annoyed users.
- Keyboard: chain of fields is Tab-able in reading order; no element is
  unreachable by keyboard; a submit button "type=submit" that fires Enter.

## Validation and errors

- **Client or server validation, both communicate with the user.** Do not
  rely on the platform's default `:invalid` bubble alone.
- **Inline, near the field, in text** — and also the very first error
  field receives focus (`aria-invalid`, `aria-describedby="err-id"`).
- Validate **on blur / after submit**, not per keystroke, unless the case
  genuinely needs live checking (username slug).
- Error messages: what happened + how to fix ("La fecha debe ser
  posterior a hoy", not "Error").
- **The submit button stays enabled.** Blocking submits to "prevent
  double" without an explanation is a finding; prefer disabling only after
  the first attempt plus an inline "Enviando…" state and a known timeout
  microcopy ("Sigue sin responder. Inténtalo de nuevo").
- **Never lose the user's input on an error.** Re-render with values
  preserved (or stored in an undoable draft). Related WCAG 3.3.4—
  3.3.7 redundancy rules.

## Input affordances

- Error and success states that rely on color alone fail (see
  `color-and-contrast.md`): pair with text and/or an icon.
- Password fields: show/hide toggle that is itself an accessible button
  (44 px), not a trick; never `autocomplete` a password confirmation with
  `"current-password"` twice.
- Sensible defaults reduce effort: a rarely-changed country field is a
  default, not a required question.

## Detect it

- Grep `placeholder=` used as the only label; count and list.
- Grep `<input` without a `<label>` or `aria-label` (rule `A11Y-LABEL`).
- Grep `disabled` on submit buttons and form controls; note the reason.
- Grep for color-only validators (`:valid/:invalid` with just a border/background change).
- Grep `type="text"` where `email|tel|url|inputmode` applies.

## Verify

- Fill it wrong on purpose: does the error show inline with text, keep
  focus on the field, and preserve the input?
- Keyboard-only run: Tab through the whole form, submit with Enter,
  fix an error and resubmit.
- Screen-reader spot check: label announced, error in `aria-describedby`.
- Refresh mid-form: what is lost and does the copy say why?