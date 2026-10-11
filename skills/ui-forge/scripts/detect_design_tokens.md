# detect_design_tokens.md — how to find existing design tokens (prose guide)

Run during Phase 1. The goal is one binary answer: **does a design token
system exist?** If it does, this skill never overwrites it, only uses it
and references it by source path.

## Where tokens hide (in order of likelihood)

1. **CSS custom properties** — a `:root { --color-*, --space-*, ... }`
   block or a `tokens.css` / `design-tokens.css`. The single most common
   home.
2. **Framework config** — Tailwind: `tailwind.config.*` (theme.extend,
   colors, spacing); shadcn/ui: `components.json` + CSS vars in the
   global stylesheet; MUI/Chakra/Radix: their `theme` object files.
3. **Token files** — `tokens/`, `design-tokens/`, `*.tokens.json`,
   Style Dictionary `properties/`, W3C-design-tokens JSON (`$type` keys).
4. **Component-library theming API** — a `ThemeProvider`, a `theme.ts`
   exporting a palette object.

## Classify

| Class | Definition | What to do |
|---|---|---|
| `clear` | A named token source exists and the components reference it (`.css` uses `var(--…)`; TSX uses `theme.colors.…`) | Preserve it. All fixes must use these tokens. Record the source path in `PROFILE.md`. |
| `ambiguous` | Tokens exist but components mostly hard-code values, or there are two candidate token systems | Declare both, ask the user which is canonical, then treat the canonical one as `clear`. |
| `absent` | No token file, values hard-coded (`#hex` / px scattered) | Record "absent". Proposed fixes may suggest creating tokens — but creating them is a separate approved finding, not a silent side-effect. |

## Evidence to record (for `PROFILE.md`)

- Source path(s) of the token file(s).
- The naming convention (`--color-`, `--space-`, camelCase, kebab).
- Coverage: which roles exist (color roles matter most — `bg`, `surface`,
  `text`, `border`, `accent`, states).
- Any **duplicate** token systems that will confuse new code.

## Rules

- Never rewrite token values as part of an a11y/contrast fix without
  explicit approval — changing `--color-text-strong` affects every
  consumer, not just the flagged component. Prefer a component-level
  override or ask.
- The scanner's `UX-MAGIC-COLOR` flag is the *signal*; this guide is the
  *conclusion*. `UX-MAGIC-COLOR` fires only when tokens seem absent —
  confirm here before proposing to mint tokens.
- If `ambiguous`, the single question to the user is: "¿cuál es el
  sistema canónico de tokens?"