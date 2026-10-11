# ui-forge

A local, deterministic skill that **audits a UI, scores it, proposes
fixes with real code, applies them only with explicit approval, and
verifies before/after**.

It covers **performance, accessibility, visual hierarchy, interaction,
consistency, responsive behavior, and microcopy** in one workflow — it
diagnoses and fixes, it does not just hand out style opinions.

- **Local and deterministic:** all knowledge ships in `references/`.
  Nothing is fetched from the internet, ever.
- **Read-only until you say so.** No installs, no network, no secrets,
  no destructive commands.
- Answers in the language you write in; its files are in English.

## Install

```bash
npx skills add jecs27/ui-forge
```

Claude Code, Codex, OpenCode, manual copy: see [INSTALL.md](INSTALL.md).

Then reload your agent. `/ui-forge` is now available.

No dependencies, no setup: the only executable is
`scripts/scan_static.py`, which uses the Python 3 standard library and
only reads.

## How it works — the audit loop

Every mode runs a subset of these phases, defined in `SKILL.md`:

| Phase | What happens | Writes to project? |
|---|---|---|
| 0 · Memory | Reads `.ui-forge/PROFILE.md` if present (stack, budgets, tokens, decisions) | no |
| 1 · Discovery | Detects stack and design tokens; sets scope (critical routes on big projects) | no |
| 2 · Static analysis | Runs `scan_static.py`, reads critical files by hand, consults only the relevant `references/` | no |
| 3 · Measurement | Optional, opt-in: Lighthouse/Playwright only if already installed or approved; otherwise marked **estimated** | no |
| 4 · Scoring | 100-point rubric across 7 categories, every deduction citing evidence | no |
| 5 · Report | Prioritized findings (impact ÷ effort, P0 first) → **stops and waits for your decision** | no |
| 6 · Apply | One approved finding at a time, minimal diffs, on a clean tree or a `ui-forge/<date>-<scope>` branch | **yes — only what you approved** |
| 7 · Verify | Re-runs scanner/measurement, reports improvements **and regressions**, runs the project's tests/lint/typecheck | no |
| 8 · Persist | Asks before writing `.ui-forge/` state; reads each file back to confirm; draft mode writes nothing | **yes — after asking** |

## Modes

| Command | Runs | Effect |
|---|---|---|
| `/ui-forge audit [path]` | Phases 0–8 | Full read-only audit with scoring |
| `/ui-forge perf [path]` | perf category | Performance only |
| `/ui-forge a11y [path]` | a11y category | Accessibility only (WCAG 2.2 AA) |
| `/ui-forge design [path]` | design categories | Hierarchy, layout, states, consistency |
| `/ui-forge fix [path]` | Phases 0–8 | Audit, then apply approved findings |
| `/ui-forge explore [request]` | — | **3 design directions** with dials and performance cost, then stops |
| `/ui-forge compare` | — | Current metrics vs saved `.ui-forge/baseline.json` |
| `/ui-forge report` | Phase 8 | Write/update `.ui-forge/reports/` |

No mode given → inferred. Real ambiguity → exactly one question and
proceed.

## Scoring

100 points, seven categories (full rubric in `references/rubric.md`):

| Category | Pts | Category | Pts |
|---|---:|---|---:|
| Performance | 30 | Consistency & system | 10 |
| Accessibility | 20 | Responsive | 5 |
| Hierarchy & layout | 15 | Content & microcopy | 5 |
| Interaction & states | 15 | **Total** | **100** |

- Severities: **P0** blocker · **P1** high · **P2** medium · **P3** polish.
- Every deducted point cites `file:line` or a metric — never a vibe.
- **Measured vs estimated** is always labeled. Without measurement tools,
  the performance category caps at 27/30 and nothing is invented.

## State and outputs

Everything the skill persists lives in the audited project:

```
.ui-forge/
├── PROFILE.md       stack, budgets, tokens (with source path),
│                    critical routes, exclusions, chosen philosophy
├── baseline.json    metrics (measured or estimated), date, environment
├── decisions.md     one line per decision: what, why, date
└── reports/         YYYY-MM-DD-<scope>.md
```

- Draft mode ("just show me", "it's a test") writes nothing.
- Existing token systems are preserved, never overwritten.
- The skill suggests gitignoring `.ui-forge/reports/`.

## Layout

```
skills/ui-forge/
  SKILL.md            orchestration: modes, phases 0–8, explore, persistence
  references/         knowledge, loaded only when a phase needs it
  performance/        Core Web Vitals, loading, images, fonts, bundles,
                      rendering, frameworks, animation, third-party
  design/             hierarchy, layout, type, color, states, forms,
                      nav, motion, responsive, dark mode, microcopy
  accessibility/      WCAG 2.2 AA checklist, keyboard/focus,
                      semantics/ARIA, screen readers & motion
  philosophies/       design directions for `explore`
  security.md         the ten non-negotiable rules
  rubric.md           the scoring system
  report-template.md  the two-layer report format
  anti-patterns.md    what the skill flags and never produces
scripts/
  scan_static.py      stdlib read-only scanner (27 rules, JSON to stdout)
  detect_stack.md     prose guide to detect the stack
  detect_design_tokens.md  prose guide; existing tokens are preserved
  measure.md          opt-in measurement protocol
  budgets.default.json     tunable budget defaults
examples/
  audit-walkthrough.md     full read-only audit session
  fix-walkthrough.md       approved-fix + verification session
  explore-walkthrough.md   3-direction explore session
```

## Validation status

13 of 14 acceptance scenarios are validated for 0.1.0 (mechanically-tested
ones ran against a throwaway fixture; behavioral ones are verified by
construction). The honest per-scenario table is in
`skills/ui-forge/CHANGELOG.md`.

## License

MIT — see `LICENSE`. All prose is original or rewritten for this skill;
inspired standards (WCAG 2.2, Core Web Vitals) are attributed in
`skills/ui-forge/PROVENANCE.md`.