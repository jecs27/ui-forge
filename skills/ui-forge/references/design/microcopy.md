# Microcopy

Microcopy is UI text written to be understood in 300 ms and actionable in
the next 3 seconds. Empty states, errors, and buttons are the three
highest-leverage places.

## Rules

- **Actions are verb + object**: "Guardar borrador", "Descargar CSV",
  "Crear cuenta". Never just "Ok", "Abrir", or bare "Guardar" when the
  object is ambiguous. Confirm/cancel pairs are "Cancelar" / the specific
  verb.
- **Errors say what happened *and* how to fix it**, at the point of
  failure: "No pudimos conectar con tu cuenta de correo. Revisa la
  conexión e inténtalo". Not "Error", not "Falló la operación".
- **Empty states teach the next action**: "Aún no tienes contactos. Una
  barra lateral te permite añadir el primero" — not "Sin resultados".
  A header + one aimed button does the job.
- **One tone, one vocabulary** team-wide: "borrar/eliminar",
  "cuenta/perfil", "guardar/enviar" — pick once and stay in it (ties to
  WCAG 3.2.6 consistency).
- **No jargon, no internal names** the user never sees elsewhere: no
  "fila 12", "modo EDI", version numbers in UI copy. Product version
  indicators belong in settings footers.
- **States explain delay honestly**: a spinner past ~5 s should have had
  a timeout message ("Sigue cargando. Puede tardar más en redes lentas").
  Indefinite spinners without scope are an anti-pattern.
- **Sensitive copy** (deletion, cancellation, irreversible): confirm with
  the consequence spelled: "Se eliminarán 274 registros. Esto no se puede
  deshacer". A confirmation that doesn't say what it costs is a foot-gun
  (see `anti-patterns.md`).
- **Numbers and units** in the same field: "Envío gratis a partir de
  39 €", not "envío gratis*".

## Detect it

- Grep the UI strings: modal confirmations — each one says what will
  happen, not just "¿Seguro?".
- Grep button labels list — any bare imperative that didn't name the
  object?
- Grep `catch`/error paths returning generic "Ha ocurrido un error".
- List empty states per screen: do any say "no results" without a path
  forward?

## Verify

- Walk the three acts: a wrong action, an empty screen, a slow network —
  each gives a specific, actionable sentence.
- Ask "what do I do next" for every empty/error state; an answer of
  "I guess…?" is a fix finding.