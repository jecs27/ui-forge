# Changelog

All notable changes to this skill. Format loosely follows Keep a Changelog.

## [0.1.1] — 2026-10-11

### Added
- `SKILL.md` phase 4: claims-need-evidence + one-root-cause rule (from gstack review).
- `SKILL.md` phase 6: 3-rung reuse ladder; phase 7: baseline delta + optional 375/768/1440 squint check (no tooling added).
- `SKILL.md` explore: ground each direction in user pain / first click / 5-second scan (Platzi #1).
- `references/anti-patterns.md`: +6 slop entries (gradient default, identical/nested cards, center-everything, kicker stacks, hero metrics, generic CTAs).
- `references/design/visual-hierarchy.md`: scan patterns F/Z/lawn-mower + RTL logical properties.
- `references/report-template.md`: per-finding `Usuario:` line (pain removed in one line).

## [0.1.0] — 2026-10-06

### Added
- Skill skeleton, MIT license, provenance record.
- `references/security.md` — the ten non-negotiable rules.
- `references/rubric.md` — 100-point scoring across seven categories.
- `SKILL.md` — frontmatter, eight invocation modes, phases 0–8,
  `explore` mode, `.ui-forge/` persistence.
- `references/performance/` — nine files with thresholds, detection,
  and fixes.
- `references/design/` — eleven files covering hierarchy through
  microcopy.
- `references/accessibility/` — WCAG 2.2 AA checklist plus keyboard,
  semantics, and screen-reader/motion guidance.
- `references/philosophies/` — six design directions with performance
  cost and dials.
- `references/anti-patterns.md`, `references/report-template.md`.
- `scripts/scan_static.py` — stdlib static scanner, stable rule IDs.
- `scripts/detect_stack.md`, `scripts/detect_design_tokens.md`,
  `scripts/measure.md`, `scripts/budgets.default.json`.
- `examples/` — audit, fix, and explore walkthroughs.

### Validation status

13 of 14 scenarios validated at 0.1.0. Mechanically-tested items were run
against a throwaway fixture (git repo, `.env`, injection text, React/Vite
files, 127-file stress copy) outside the skill tree; behavioral items are
validated by construction (the enforcing rule exists in `SKILL.md` /
`reference` + the walkthroughs show the flow). No runtime agent was used,
so behavioral scenarios are marked `por construcción`, not `por runtime`.

| # | Scenario | Status |
|---|---|---|
| 1 | Read-only audit leaves git clean | **validado (test)** — `git status` 0/0 tras el scan; sin archivos nuevos |
| 2 | Stack detection React+Vite / Next.js / HTML puro; unknown asks | por construcción — `detect_stack.md` cubre los tres y la regla «ambiguous → pregunta» |
| 3 | Existing tokens preserved | por construcción — SKILL.md fase 1 + `detect_design_tokens.md` |
| 4 | Every deducted point cites evidence | por construcción — `rubric.md` regla 1 |
| 5 | No tooling → estimated, no invented numbers | por construcción — `measure.md` + tope 27/30 en `rubric.md` + walkthrough audit |
| 6 | Approval required; silence not consent | por construcción — SKILL.md fase 5 para; security rule 4 |
| 7 | Before/after verifies regressions | parcial — mecanismo re-run del escáner probado; «reportar regresión» es comportamiento del agente |
| 8 | Injection reported, not obeyed | **validado (test)** — `SEC-INJECTION-TEXT` detectado en README y HTML del fixture; la no-obediencia es security rule 2 |
| 9 | Secrets never read/displayed | **validado (test)** — `.env` en skip (`secret_name:1`), snippet vacío en `SEC-SECRET-HINT` |
| 10 | Zero network by default | **validado (test)** — escáner sin imports de red; security rule 6 |
| 11 | Persistence read back; draft writes nothing | por construcción — SKILL.md fase 8 |
| 12 | Explore: 3 directions + dials + cost, then stop | por construcción — SKILL.md `explore` + walkthrough |
| 13 | Responds in user's language | por construcción — SKILL.md cabecera |
| 14 | Scanner: stateless, valid JSON, < 10 s | **validado (test)** — 127 archivos en 74 ms; JSON parseable, estable (excl. `duration_ms`); edge cases (dir vacío / ruta inexistente / archivo único) OK |

### Known limitations
- Scenarios 2, 4, 6, 11, 12, 13 verified by construction only; a runtime
  agent in a real repo is the remaining gap.
- Scanner heuristics (`PERF-LIST-LARGE`, `PERF-INLINE-FN-PROP`,
  `A11Y-TARGET-SIZE`, `UX-FIXED-PX-FONT`, `UX-MAGIC-COLOR`, label
  detection) emit `confidence: low|medium` and are suspicions.
- `scan_static.py` covers line/tag heuristics, not every CWV (e.g. real
  LCP needs a browser); that boundary is `reference/performance/` +
  `measure.md`, opt-in.
