# Navigation and information architecture

Navigation's job: the user always knows **where they are**, **how to get
back**, and **where the next thing is**.

## Rules

- **Location is visible.** The current section is highlighted in the nav;
  mobile users get a title/breadcrumb pattern, not "you are in a list".
- **≤ 7 primary items** (cognitive ceiling on nav breadth — convention,
  backed by how people keep bearing in working memory). More: group under
  a logical parent, not a "more…" junk drawer.
- **Breadcrumbs when depth exists** (3+ levels): a trail is how deep plus
  a way back. Only where the content has real depth — flat landing pages
  do not need them.
- **A search field where volume exists.** Searching is easier than
  navigating at scale. If search exists, it takes the same primary
  position on every page (see WCAG 3.2.6 "consistent help").
- **Mobile nav lives in thumb reach.** The primary actions reachable from
  the bottom or the menu region a thumb reaches; no hamburger hiding
  every action once. (Convention — a priority, not a law.)
- **Consistency across pages**: same order, same labels, same position
  for the same nav. A link named "Account" on one screen and "Tu perfil"
  on the next is an IA bug, not a copy variation (see `microcopy.md`).
- **Page titles / heading match the nav label and the route** — the ALT
  of orientation and the browser tab.

## Information architecture (the map)

- **One mental model, not several.** Sort the product's screens into the
  smallest number of *primary* sections that survive every future feature.
  If two ways of organizing conflict (are settings under "Account" or
  "More"?), pick one tree and stay in it.
- **Card-sort / tree-test** only when volume demands; a 10-screen app
  sorts by conversation, not study.
- **Less is the feature**: either hide low-use nav and reveal on search,
  or keep a visible "More" with *real* items. A nav with 20 items is an
  IA finding by itself.

## Detect it

- One rendered route: the current location is highlighted? Breadcrumb
  exists in depth? The nav order list from a glance — count primary
  items.
- Grep nav labels across pages for the same item with different text.
- Check mobile against a thumb-zone mock or an actual device: primary
  actions in reach?
- Compare page `<title>`, H1, nav label, and url slug for a route — all
  four should be the same idea.

## Verify

- Click 3 screens deep and back: location always visible, breadcrumb
  valid.
- Ask a fresh user (or a colleague) "where do you find X" on the real
  app; a wrong answer within 5 s is an IA signal worth a finding.