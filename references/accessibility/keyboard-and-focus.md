# Keyboard and focus

Keyboard access is the non-negotiable core of a11y, and focus is its
visible contract: a user must never lose track of *where they are*.

## Tab order

- **Logical order** (reading, then interactive controls in the visual
  order they appear). Big DOM order mismatches → fixes = reorder in HTML,
  not `tabindex` hacks.
- **`tabindex="-1"`** to make something focusable *by script* only
  (e.g. moving focus to an error after a submit) — never "0" on
  non-interactive elements just to make them reachable.

## The focus indicator

- **`:focus-visible`** (keyboard-and-autocomplete-only) gives the crisp
  keyboard ring without the mouse-click outline:
  - **Never `outline: none` without a real replacement** (`A11Y-OUTLINE-NONE`).
  - Replacement must be ≥ 3:1 against the surroundings, not a 1 px
    `box-shadow` the same color as the surface.
- Common cheap pattern:

```css
:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
```

- **Focus-visible vs focus:** `:focus-visible` for keyboard-origin focus;
  do not remove `:focus` entirely for mouse (some platforms read
  different). Verified: the Safari/Chrome/FF behavior differs slightly —
  test the ring in at least two browsers by Tab-ing.

## Modals and overlays

- **Open →** move focus to the dialog (or its close button for `alertdialog`).
- **Inside →** trap: Tab cycles within the dialog, never escapes to the
  page behind (`keydown` handler on the dialog checks Tab).
- **Close →** focus returns to the element that opened it (the trigger).
- Anything modal-by-*design* but implemented as a floating div that breaks
  the above is a failure of 2.1.2 (no trap) and 2.4.3 (focus order).
  Native `<dialog>` + `showModal()` gives focus behavior for free.

## Skip links and landmarks

- **Skip-to-content link** first focusable element on every page target
  `#main` (much cheaper than demanding only `main` in tests).
- `nav`, `main`, `header`, `footer`, complementary regions → screen
  readers jump straight; don't only rely on them, but for pages:
  <nav> before <main> and one <h1> at the top of main.

## Shortcuts that don't fight

- Custom keyboard shortcuts must *not* swallow standard keys the way a
  screen reader needs them (letters are risky globally; scope keybindings
  to a focused editor region and state them).
- Arrow navigation in a calendar/table: mouseless nav is valuable, but the
  arrow grid must come with the semantics (roving `tabindex`) so screen
  readers announce it — a raw `onKeyDown` that moves a cursor div fails 4.1.2.

## Detect it

- Tab through the critical route with keyboard only; record each item
  that is unreachable or traps focus.
- Grep `outline: none` / `outline: 0` in CSS (rule `A11Y-OUTLINE-NONE`);
  each needs a matching replacement.
- Grep `<dialog>` usage: are focus trap/return implemented, or was a div
  made to *look* modal?
- Grep `tabIndex={"0"}` on `<div>` carriers — probably should be a real
  element.

## Verify

- Redo the Tab-walk after a fix; focus ring visible ≥ 3:1 on each stop.
- Close a modal with Esc → focus visibly back on the opener button.