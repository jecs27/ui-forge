# Dense data

The terminal for information: every pixel carries signal, sorting beats
search, and the page reads like a cockpit. This is a *tool* direction,
not a *magazine* direction.

## Principles

- Information density is the value: multiple trains of data run in
  parallel on one screen; whitespace is a cost, not an ornament.
- Scanning beats reading: columnar layouts, compact type, highlight the
  *change* not the base value.
- Power user first: keyboard, sorting, bulk ops, dense-but-visible
  affordances.

## Structure

- Tight multi-column grids; tables and data-grids as first-class
  citizens; fixed table headers; hierarchical rows with disclosure.
- Density choice explicit: a density slider (comfortable ↔ compact) is a
  feature of this direction, not an afterthought.
- Panels/layout: dockable panes, collapsible rails — hard edges, no
  breathing-room hero.

## Visual treatment

- Hairline borders, small type, tabular numerals, strong zebra for row
  tracking. Elevation only to separate *modes* (diagram vs panel), not
  decoration.
- Color = data ink: highlight anomalies, deltas, selections; neutral
  everything else. Status as combination of text + color (never color
  alone).

## Typography and palette

- Compact sans or a UI-font at 12–14 body-ish for dense text; monospace
  for identifiers/numbers (great practice anyway for the data itself).
- Tabular figures (`font-variant-numeric: tabular-nums`) in every
  numeric column so digits align.
- Greys for grid lines, near-black text, one accent + signal colors
  (success/warn/error) constrained to the data stream.

## Microinteractions

- Snappy: 100–150 ms; hover-row highlight, press feedback on bulk
  control; sorting is instant (client-side).
- Enter-table state muscles: row selection state group with checkboxes +
  `aria-selected` on rows (a11y locked to this direction).

## Dials (1–10)

- `variance`: 3–5 (the pages vary, the visual language doesn't)
- `motion`: 1–2 (fast, purposeful; nothing decorative)
- `density`: 8–10 (the whole point; respect touch ≥ 44 px on targets
  even in dense mode — density applies to data, never below the a11y
  floor)

## Performance cost

- Low-moderate: big grids want virtualization or pagination (the
  direction *demands* real perf, no lazy-80-infinite loops); client-side
  sort on 10k rows needs a real index. Ships on one font family.

## Works best when

- Dashboards, CRMs, ops consoles, financial/analytics products, admin
  backends, any "I live here all day" tool.

## Avoid when

- Consumer broadcast/retail marketing (density antagonizes the emotional
  funnel).
- First-time consumer onboarding (a cockpit confuses a tourist).
- Any product whose job is reading long prose (see `editorial`).