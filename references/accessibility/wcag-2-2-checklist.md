# WCAG 2.2 AA — checklist

The working list for this skill's a11y scoring: WCAG 2.2 **Level AA**
plus the handful of large-text/UI exceptions. Criterion numbers follow the
W3C spec (see `PROVENANCE.md`). This is a practical checklist — evidence
for each item is the point of the audit.

## Perceivable

**1.3.1 A/AA — Info and relationships:** semantic structure (headings,
lists, table headers with `scope`, form fields with labels). Divs-as-
elements fail this.

**1.4.3 AA — Contrast (minimum):** 4.5:1 text, 3:1 large (≥ 24 px or
≥ 18.66 px bold), 3:1 UI and graphics. See `color-and-contrast.md`.

**1.4.4 AA — Resize text:** content works at 200 % browser zoom / text
enlargement without clipping or overlap (reflow is a sibling criterion
1.4.10 — see below).

**1.4.10 AA — Reflow:** no *two-dimensional* scrolling at 320 px wide at
400 % zoom (one-dimensional scrolling for tables/images is allowed).

**1.4.11 AA — Non-text contrast:** 3:1 for UI component edges and
graphical objects (input borders, icon strokes, graph lines).

**1.4.12 AA — Text spacing:** overriding line/paragraph/letter spacing
via user CSS breaks nothing (no clipped text at +1.5 line / +0.16
letter spacing).

**1.4.13 AA — Content on hover/focus:** tooltips through hover *and*
focus, dismissable, non-hiding when the pointer moves over them.

## Operable

**2.1.1/2.1.2 A — Keyboard:** every function operable by keyboard; no
keyboard trap (modals, see `keyboard-and-focus.md`).

**2.4.3 AA — Focus order:** sensible traversal matching visual order.

**2.4.7 AA — Focus visible:** an indicator ≥ 3:1 contrast while moving
(rule `A11Y-OUTLINE-NONE`).

**2.5.8 AA — Target size (minimum):** targets ≥ **24 × 24 px**. (This
skill recommends **44 × 44** for main touch targets even though 24 is
the AA minimum — the AA number is a floor, not a goal.)

**2.3.3 AA — Animation from interactions:** no >5 s motion triggered by
interaction without an off switch; `prefers-reduced-motion` is the gate.

## Understandable

**3.1.1 A — Page language:** `lang` on `<html>` (rule `A11Y-LANG`).

**3.2.3/3.2.4 AA — Consistent navigation and identification:** the nav
order is the same across pages; a component named X is X everywhere.

**3.2.6 AA — Consistent help:** when help exists (search, help link),
it is in the same relative place on every page.

**3.3.1/3.3.2 — Error identification + labels:** errors identified in
text and field labels present (rule `A11Y-LABEL`).

**3.3.3/3.3.4 AA — Error suggestion + prevention:** errors suggest a fix;
sensitive actions (purchase, delete) have a confirmation/reversal step.

**3.3.7 AA — Redundant entry:** no re-asking information the user already
entered (same field twice across a flow).

**3.3.8 AA — Accessible authentication (minimum):** no cognitive test
(no "select every square with a bus") as the only path. At minimum a
non-cognitive alternative (copy a code, paste a link); 2FA codes count
as accessible.

**2.4.11 AA — Focus not obscured (minimum):** the focus indicator is
not *fully* hidden by a floating header/footer/notification when an
element receives focus.

**2.5.7 AA — Dragging movements:** any action performable by drag has a
one-tap / no-drag alternative (sortable lists, sliders get a text or
button method).

## Robust

**4.1.2 A — Name, role, value:** custom widgets expose role and state
(ARIA, see `semantics-and-aria.md`).

**4.1.3 AA — Status messages:** dynamic updates announced via live
regions (aria-live) — saved states, error banners, progress ending.

## The audit practice for this checklist

- **Automated scan first** (axe if installed, or Lighthouse a11y pass)
  — catches ARIA misuse, missing labels/alt, contrast where composable.
- **Then keyboard-only walk:** Tab through, operate every control,
  escape out of layered UI — a straight T-route through the critical
  flows.
- **Then the state check** from `components-and-states.md` (focus,
  hover, error, empty, success) on the components the scan couldn't see.
- **Then note measured vs estimated**: contrast is calculable in code;
  "focus not obscured" needs a real render.
- Report each criterion as **pass / fail / not-tested**, with evidence,
  never a blanket "accessible".