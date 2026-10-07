# detect_stack.md — how to detect the stack (prose guide, not executable)

The agent follows this during Phase 1. Read files; never install, never
run a build. Classify each dimension as `clear` / `ambiguous` / `absent`.

## What to read, in order

1. `package.json` (if it exists) — the single highest-signal file in a
   JS project.
2. Lockfiles: `pnpm-lock.yaml` / `yarn.lock` / `package-lock.json` /
   `bun.lockb` → package manager.
3. Config files: `.next/`, `next.config.*`, `nuxt.config.*`, `astro.config.*`,
   `svelte.config.*`, `vite.config.*`, `remix.config.*`, `webpack.config.*`
   → framework/bundler. Presence of the *directory* `.next/` alone is a
   strong Next signal, but never rely only on it.
4. `index.html` at root → SPA/bundler entry. `server/`, `api/` routes,
   `prerender`, `ssr` flags → architecture.
5. `tailwind.config.*`, `theme/`, `tokens/`, `*.css` with `:root` →
   styling approach (handled in `detect_design_tokens.md`).
6. `.babelrc`/`tsconfig` paths, `src/` layout, `components/` vs `pages/`
   vs `app/`.

## Dimensions and how to classify

| Dimension | Evidence | `clear` if | `ambiguous` if | `absent` if |
|---|---|---|---|---|
| Framework | `package.json` deps (`react`, `next`, `vue`, `svelte`, `astro`, `preact`) + config file | dependency AND its config file exist | only the dependency, no config | no framework deps at all |
| Bundler | `vite`, `webpack`, `esbuild`, `rollup`, or the framework's built-in | a dedicated config or the dependency name | framework's built-in bundler, no explicit one | no build step observed (plain HTML/CSS/JS) |
| Styling | `tailwindcss`, `styled-components`, `emotion`, CSS modules, plain `*.css`, SCSS | one clear mechanism | two mechanisms coexisting without a stated boundary | no CSS at all (unexpected) |
| Package manager | lockfile name | exactly one lockfile | lockfiles conflict or `package.json` has no lock | no lockfile |
| Architecture | `getServerSideProps`/SSR imports, `vercel.json`, static export, `app/` dir, `window` guards | explicit SSR/SSG config or runtime check | mixed (SSR + SPA components) | nothing — assume SPA/static |
| Component library | `@mui`, `antd`, `radix`, `shadcn` (components.json), `chakra`, custom `components/` | one library used across files | library present but rarely used | fully hand-rolled |
| i18n | `next-intl`, `react-i18next`, `i18n` config, `locale` dirs | an i18n config or library | scattered `t()` calls, no config | none observed |
| Tests | `*.test.*`, `*.spec.*`, vitest/jest/playwright config | config + test files | tests exist oddly placed | none |

## Rules

- **`clear`** → record it, move on, never re-derive.
- **`ambiguous`** → record both candidates and **ask the user once**
  before assuming. Example: both Vite and Webpack configs present because
  of a library scaffold — say what you found and ask which is the real
  build.
- **`absent`** → record "no evidence" and proceed; if the code is clearly
  plain HTML/CSS/JS, that is a legitimate stack, not a gap.

## Output

Write the detected stack into the audit announcement (3–5 lines) and
into `.ui-forge/PROFILE.md` at persist time. Do not invent versions; say
what the files show. If uncertain about a version's implications, note it
and keep vendor-agnostic.