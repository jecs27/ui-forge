# Explore walkthrough — a realistic `explore` session

`explore` is for choosing a direction **before** building. It presents 3
directions with dials and performance cost, then stops.

## Setup

- A product: "catálogo de cursos en línea, audiencia de UX designers,
  proyecto nuevo (empty folder), sin sistema de diseño yet."
- `detect_design_tokens.md` → absent (no theme exists). So explore may
  cover palette too, but the skill still *limits* — palette + typography
  (see below) — kept minimal.

## The 3 directions

```
Direcciones para «catálogo de cursos» (proyecto nuevo, sin tokens):

1. Minimalista (cursos como contenido, no como tarjetas plantilla)
   · Estructura: lista de cursos en una columna legible, sin grid de
     cards uniformes; el título es el héroe.
   · Tratamiento visual: flat, un acento, aire y alineación por rejilla.
   · Interacción: 120ms presa+hover en fila; nada decorativo.
   · Funciona mejor cuando: el catálogo ES contenido y la calma es la marca.
   Dials: variance 2 · motion 2 · density 3
   Costo: ≤1 fuente woff2 (variable) · sin dependencias JS · ≈60 KB crítico

2. Editorial (cursos como publicaciones)
   · Estructura: portada-asimetría, destacado central + briefs laterales.
   · Tratamiento visual: serif display + sans, hairlines, fotografía
     de gran formato con srcset.
   · Interacción: hover subraya el título y eleva 2px (transform only).
   · Funciona mejor cuando: categoría premium quiere autoridad de revista.
   Dials: variance 5 · motion 2 · density 4
   Costo: 2 familias (2–3 pesos) · imágenes grandes necesitan AVIF+srcset ·
          ~120 KB crítico estimado

3. Dense data (cursos como inventario manejable)
   · Estructura: tabla/lista densa, filtros y ordenación por columna.
   · Tratamiento visual: hairlines, tabular-nums, zebra sutil, estatus
     con texto+color (nunca solo color).
   · Interacción: sort instantáneo en cliente, filas con checkbox+
     aria-selected; 120ms feedback.
   · Funciona mejor cuando: el usuario administra mucho volumen y quiere
     poder de control.
   Dials: variance 3 · motion 1 · density 9
   Costo: una fuente compacta · la tabla pide virtualización en catálogos
          reales (100+ filas) · bajo en assets, real en ingeniería.
```

Then **stops**:

```
¿Cuál es la base estructural? (número, orden, «todas» con cuál base,
o «decide tú»)
```

## Accept patterns (the skill's rules)

```
Usuario: "2"             → solo dirección 2.
Usuario: "3, 1"          → 3 es la base estructural, 1 define el mood.
Usuario: "todas"         → skill pregunta cuál es la base antes de
                           combinar; nunca junta dos elevaciones distintas
                           en un componente.
Usuario: "decide tú"     → skill elige 2 (la mejor relación contenido/
                           costo para cursos) y justifica en una línea.
```

## What this walkthrough demonstrates

- 3 directions, max 4 bullets each (scenario 12).
- Dials declared (`variance`, `motion`, `density`), perf cost stated per
  direction, and an explicit **stop** — no building.
- Anti-slop applied: direction 1 explicitly avoids the "3 identical
  cards" plank, direction 3 meets touch-target floors even at density 9.