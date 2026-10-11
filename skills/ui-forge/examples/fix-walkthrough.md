# Fix walkthrough — a realistic application phase

Continues the audit from `audit-walkthrough.md`. The user answered
"aplica solo los P0 y P1 y el de 100dvh". The skill now does Phase 6–8.

## Phase 6 — apply, one finding at a time

Tree status first: `git status` is clean (`git stash` check was 0
entries) → proceed on a branch `ui-forge/2026-10-06-src-pages`, then one
diff per finding.

### Flow with the first finding (A11Y-003)

```
ID: A11Y-003 · P0 · Accesibilidad
Problema: el botón "Agregar" es un div onClick sin rol ni teclado.
Evidencia: src/pages/Home.tsx:41
Por qué importa: inaccesible con teclado; un screen reader no lo lee.
Corrección: cambiar <div onClick={add} className="cta">Agregar</div>
            por <button onClick={add} className="cta">Agregar</button>
            (y .cta gana cursor:pointer y :focus-visible via la clase,
            sin tocar otras reglas).
Verificación: Tab hasta el botón, Enter dispara add(); el a11y tree
              nombra "Agregar, button".
Riesgo: bajo — el CSS .cta ya estilaba el div; solo cambia el elemento
        base de estilo (block vs inline), se verifica en el render local.
```

Better diff shown, then applied. The same one-at-a-time pattern for:
`PERF-002` (remove lazy, add fetchpriority on the hero img),
`A11Y-007` (focus mgmt in the modal — this one gets a `:focus-visible`
CSS addition and a focus trap on the `<dialog>`), and `UX-004`
(`100vh` → `100dvh`).

No refactor touches outside that list. The bundle-split finding (PERF-009)
was explicitly not in scope — untouched, noted as skipped.

Sample applied patches:

```diff
-<div onClick={add} className="cta">Agregar</div>
+<button onClick={add} className="cta" type="button">Agregar</button>
```

```css
.login { height: 100dvh; }   /* era 100vh */
```

## Phase 7 — verify before/after

- Re-run scanner on scope: `A11Y-003`, `A11Y-007`, `PERF-002`, `UX-004`
  gone; no new findings introduced in scope.
- Tests: `npm test -- --run` (the project's own script) → 3 pass.
- Linter/typecheck (`npm run lint`, `tsc --noEmit`) → clean, verified.
- **Regressions reported honestly:** after the modal focus change the
  trigger button's focus stays visible (no regression found). If it had
  regressed, the report would say so and offer the revert of that
  specific finding.
- No measurement tool → "mejoras verificadas por escáner + inspección;
  impacto en LCP estimado, sin número inventado".

## Phase 8 — persistence

Ask "¿guardo la línea base y el reporte?" — wait for "sí". Then write
`baseline.json` (measured:false + a note of which findings resolved),
`decisions.md` (one line per applied finding, date), and
`reports/2026-10-06-src-pages-fix.md`; **read each back** before
confirming. Suggest `.ui-forge/reports/` gets gitignored.

## What this walkthrough demonstrates

- Approval before any write; one finding at a time with minimal diffs
  (scenarios 6, 7).
- Regression honesty: report when a change hurts, offer its revert (7).
- Tests/lint/typecheck actually run and reported with real results (7).
- Reversibility: branch name + clean-tree check; no force, no reset.