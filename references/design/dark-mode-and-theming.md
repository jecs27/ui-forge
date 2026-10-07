# Dark mode and theming

Dark mode is a real render of the product on a different surface, not a
negative filter of the light theme.

## Theming foundation: semantic tokens

Theme switching only works if styles reference **semantic roles**, not
raw values:

```css
:root {
  --color-bg: #ffffff;        --color-bg: #0f1114;        /* light first, dark second */
  --color-surface: #f6f7f9;   --color-surface: #17191d;
  --color-text-strong: #101114; --color-text-strong: #e8eaed;
  --color-text-muted: #5b6168;  --color-text-muted: #9ba1aa;
  --color-border: #e2e4e8;      --color-border: #2a2d33;
  --color-accent: #2563eb;      --color-accent: #60a5fa;
  ...
}
```

- If styles interpolate `#fff` / `#000` or `#fafafa` everywhere, that is
  the `UX-MAGIC-COLOR` findings class plus "no theming story".
- Roles above are a floor; product-specific roles (warning/success) join
  the same token file.

## Dark mode rules

1. **`prefers-color-scheme: dark` handles the OS preference; also offer a
   manual toggle** and persist it (localStorage), because users override
   the OS. The toggle must not flash a wrong theme on reload — inline the
   saved choice in a tiny script before first paint (see below).
2. **Never pure black on pure white / vice versa.** Pure `#000` text on
   `#fff` strains; and pure `#fff` text on `#000` is equally glaring.
   Use off-whites/off-blacks (`#0f1114` + `#e8eaed` style).
3. **Elevation *up* done with lighter surfaces, not shadows.** In dark
   mode the card above its background is a *lighter* grey, not a bigger
   drop shadow (shadow on black is invisible anyway). `--color-surface`
   steps lighter for each elevation level.
4. **Same contrast floors** in both modes (4.5:1 normal / 3:1 large+UI).
   Dark-mode palettes commonly need brighter text-passing colors.
5. **Mirrors and images adapt:** screenshots/illustrations with white
   backdrops get their own dark variants or `filter` transparencies;
   logos with dark glyphs need a light-glyph variant.
6. **A11y:** `color-scheme: dark` on the html so form controls and
   scrollbars render dark; always `prefers-reduced-motion` — theming and
   motion are independent axes.

## Prevent theme flash (FOUC the theme)

```html
<script>
  // runs before paint; safe from the flash of wrong theme
  try {
    var t = localStorage.getItem('theme');
    if (t === 'dark' || (!t && matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    }
  } catch (e) {}
</script>
```

The CSS then keys off `.dark` (manual) and/or `@media (prefers-color-scheme)`.

## Detect it

- Grep raw `#ffffff`, `#000`, `#fff`… usage where a token should be
  (`UX-MAGIC-COLOR` catches the repetition).
- Grep `prefers-color-scheme` — absent anywhere = a finding for a product
  with any dark ambitions.
- Grep `box-shadow` usage: cards in dark mode that keep a visible heavy
  shadow are a "dark mode is light theme with swapped text" symptom.
- Check images: white-background PNG inside dark surfaces.

## Verify

- Toggle both ways: contrast passes on the same content, no clipped
  text, no pure-black flash on load, toggle persists reload, images look
  right.
- Automated contrast check of the *dark* palette, not just light.

---

## Theming the rest

- Token changes should be a single source: updating the palette flips
  the whole product. Any new view uses tokens, never a one-off value
  (rule 7 of "rules for generated code").
- If no token system exists, propose creating one (a single
  `tokens.css` / theme file) rather than threading per-component colors.