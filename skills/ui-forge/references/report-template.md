# Report template

Two layers. In chat: short, scannable, one decision per line. On request:
full detail per finding. Both are written in the user's language.

## In-chat report

```
## ui-forge — <scope>

Stack: <detected> · Modo: <audit|perf|a11y|design|fix> · Medición: <medido|estimado>

### Puntuación: <N>/100
| Categoría | Puntos | Límite principal |
|---|---|---|
| Rendimiento | 21/30 | Imágenes sin dimensiones + lazy en LCP (estimado) |
| Accesibilidad | 14/20 | Focus oculto al abrir el modal |
| ... | ... | ... |

### Top 5 por prioridad
| ID | Sev | Hallazgo | Evidencia | Impacto | Esfuerzo |
|---|---|---|---|---|---|
| A11Y-012 | P0 | Formulario inutilizable por teclado | src/pages/Login.tsx:58 | bloquea registro | M |
| PERF-004 | P1 | 400 KB JS en la ruta crítica | main.tsx:1 (imports) | LCP +1.2 s | L |
| ... | ... | ... |

### Ganancias rápidas (< 15 min)
- PERF-IMG-DIM: dimensiones en las 4 imágenes del hero → CLS estable (1 archivo)
- A11Y-OUTLINE-NONE: reemplazar outline:none por :focus-visible (1 bloque CSS)

### Riesgos y cosas que NO toqué
- El estilo de <archivo X> se sale del alcance; no lo toqué.
- Perf está marcado «estimado»: no hay herramientas de medición instaladas.

### ¿Qué hacemos?
1. Aplicar todo   2. Solo P0 y P1   3. Elegir IDs   4. Solo reporte
```

Rules for this section: tables for comparison, bold for the numbers that
matter, never art. Only one question block at the end (the same
4-choice list).

## Per-finding detail (on request, or attached when applied)

```
ID: PERF-004 · P1 · Rendimiento
Problema: <una línea>
Evidencia: <archivo:línea o métrica>
Por qué importa: <efecto en el usuario o la métrica, una línea>
Usuario: <qué dolor evita o qué tarea desbloquea, una línea>
Corrección: <diff mínimo, una unidad>
Verificación: <cómo comprobar que mejoró>
Riesgo: <bajo/medio/alto + por qué>
```

## Detail ordering

Deduction (score) order: P0 blockers first, then priority =
impact ÷ effort descending. Every finding carries an ID so the user can
pick from the "choose IDs" option.

## Persist

`.ui-forge/reports/YYYY-MM-DD-<scope>.md` holds the full report body;
chat shows the short form. Writing only after the user's answer in phase 8.