# Audit walkthrough — a realistic session

Shows a full read-only audit from invocation to the report and the
approval stop. No file is modified; the only writes happen in Phase 8
after an explicit answer.

## Setup

- Project: a React + Vite landing route `src/pages/Home.tsx`, CSS in
  `src/index.css`, package.json present, `next` absent. No Lighthouse in
  the project, no network allowed.
- User: `/ui-forge audit src/pages`

## Phase 0 — project memory

`.ui-forge/PROFILE.md` does not exist (first audit) → nothing to apply,
no questions. The best posts of `decisions.md` get written later.

## Phase 1 — discovery

```
Stack: React 18 + Vite · estilos: CSS plano (sin Tailwind) · SPA ·
sin librería de componentes · alcance: src/pages (3 archivos)
Tokens: ausentes (colores en hex sueltos; verify with detect_design_tokens.md:
ambiguous → ask once).
Presupuestos: budgets.default.json (JS gzip ≤170 KB, 44px targets, AA 4.5:1)
```

One question asked (the only ambiguity): "No encuentro un sistema de
tokens; ¿lo confirmas o hay un theme que se me escapa?" → "Confirmo, no
hay." → `absent` recorded.

## Phase 2–3 — static analysis, no measurement

- `python3 scripts/scan_static.py src/pages` → 14 findings.
- Manual read of `Home.tsx` confirms hero img is lazy; `track.ts` has a
  scroll listener without `passive`.
- No Lighthouse installed → measurement is **opt-in, declined** → all
  performance findings labeled `estimado por análisis estático`.

## Phase 4–5 — scoring and report

```
## ui-forge — src/pages (landing)

Stack: React18+Vite · Modo: audit · Medición: estimada (sin herramientas)

### Puntuación: 61/100
| Categoría | Puntos | Límite principal |
|---|---|---|
| Rendimiento | 15/30* | Lazy en LCP + JS 240KB (sin medir → etiquetado estimado) |
| Accesibilidad | 12/20 | Div onClick + input sin label + focus oculto |
| Jerarquía | 11/15 | Hero sin propuesta de valor; 3 cards plantilla |
| Interacción | 12/15 | Falta estado empty en la lista |
| Consistencia | 7/10 | 6 colores sueltos en 3 archivos |
| Responsive | 3/5 | 100vh en móvil |
| Microcopy | 4/5 | Footer botón "Ok" sin verbo |
* Cap aplicado sin medición: rendimiento máx 27/30

### Top 5 por prioridad
| ID | Sev | Hallazgo | Evidencia | Impacto | Esfuerzo |
|---|---|---|---|---|---|
| A11Y-003 | P0 | Botón "Agregar" es un div onClick | Home.tsx:41 | inaccesible con teclado | S |
| PERF-002 | P1 | Imagen hero en loading="lazy" | Home.tsx:9 | LCP +1s (estimado) | S |
| A11Y-007 | P1 | Focus oculto al abrir modal | Modal.tsx:15 | perder la pista de foco | M |
| UX-004 | P2 | 100vh en login móvil | login.css:12 | barra del navegador tapada | S |
| PERF-009 | P2 | 240 KB JS en ruta crítica | main.tsx:1 | parseo +TBT (estimado) | L |

### Ganancias rápidas (< 15 min)
- A11Y-003 → cambiar el div a <button> (1 línea + CSS)
- UX-004 → height: 100dvh (1 línea)
- PERF-002 → quitar loading="lazy" y añadir fetchpriority="high" (1 línea)

### Riesgos y cosas que NO toqué
- El bundle a 240 KB: sin medición real, el split es una propuesta, no una
  certeza; habría que medir con scanner del bundler (permiso).
- El modal de share: su comportamiento de foco estaba fuera de alcance;
  lo dejé fuera, anotado para una segunda pasada.

### ¿Qué hacemos?
1. Aplicar todo   2. Solo P0 y P1   3. Elegir IDs   4. Solo reporte
```

Then it **stops**. The user's silence is not consent — Phase 6 starts only
on an explicit "aplica solo los P0" or similar.

## Phase 8 — persistence (only after "guardar")

`decisions.md`, `baseline.json` (measured: false + nulls, honest) and
`reports/2026-10-06-src-pages.md` written; each file **read back** before
confirming; `.gitignore` suggestion offered for `reports/`.

## What this walkthrough demonstrates

- Zero writes until an explicit answer (scenario 6).
- Everything measured is labeled "estimado"; nothing invented (5).
- P0 first ordering; impact ÷ effort inside the band (1, 2, 4, 7, 9).
- The scanner:
  `A11Y-DIV-CLICK`, `PERF-IMG-LAZY-LCP`, `UX-VH-MOBILE`,
  `SEC-*` none here because no injection text present.