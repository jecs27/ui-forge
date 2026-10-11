# Images and media

Images are usually the largest bytes on a page and the most common cause
of CLS. Get format, dimensions, and load time right.

## Formats

- **AVIF** first, **WebP** fallback, JPEG/PNG as last resort. SVG for
  logos and icons.
- Serve via `<picture>` so old browsers fall back:

```html
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" width="1600" height="900" alt="aurora sobre el lago">
</picture>
```

## Sizing (`srcset` + `sizes`)

- `srcset` gives the browser candidates; `sizes` tells it the rendered
  width so it picks the right one:

```html
<img src="cat-800.jpg"
     srcset="cat-400.jpg 400w, cat-800.jpg 800w, cat-1200.jpg 1200w"
     sizes="(max-width: 600px) 100vw, 50vw"
     width="800" height="600" alt="gato dormido">
```

- **Always set `width` and `height`** (or CSS `aspect-ratio`). Without
  them the image reserves zero space and the page jumps when it loads —
  a direct CLS source.
- `sizes` must match the real layout, or the browser downloads a bigger
  image than needed.

## Loading attributes

- `loading="lazy"` on **below-the-fold** images only.
- **Never** lazy-load the LCP image; give it `fetchpriority="high"`.
- `decoding="async"` on images that are not the LCP (lets the browser
  continue rendering while decoding).
- Hidden/off-screen (carousel slides, tabs) → `loading="lazy"` is correct;
  they are below the initial viewport.

```html
<img src="hero.jpg" fetchpriority="high" width="1600" height="900" alt="portada">
<img src="thumb.jpg" loading="lazy" decoding="async" width="400" height="300" alt="miniatura">
```

## CSS backgrounds vs `<img>`

- Use `<img>` when the image is content (adds `alt`, supports lazy/
  priority, reserves space). Use CSS background only for decorative
  textures or when the image is behind other content. A background image
  that is content is inaccessible — no `alt`, no semantics.
- Retina: `background-image: image-set(url('x.avif') 1x, url('x.avif') 2x)`.

## Optimize the actual bytes

- Recompress: real transparency lossless, otherwise compressed WebP/AVIF.
- Remove embedded metadata; some formats strip it automatically.
- Generators: `cwebp`, `avifenc`, ImageMagick, or a build-time plugin —
  always check the project's own toolchain before proposing one.
- Icons: a single SVG sprite, or an icon component library that
  tree-shakes — not 40 separate requests.

## Video

- `preload="metadata"` unless the video is center-stage autoplay;
  `poster` so the first frame is not blank; `playsinline` + `muted` for
  autoplay; no autoplay sound without a control the user can find.
- Don't stream before the user scrolls it into view.
- A `video` pretending to be the hero should preload only its poster, not
  the full file.

## Detect in code

- Grep `<img` for tags missing `width`/`height`/`aspect-ratio` per tag
  (scanner rule `PERF-IMG-DIM`).
- Grep `loading="lazy"` and check the one in the hero (rule
  `PERF-IMG-LAZY-LCP`).
- Look for `.png`/`.jpg` refs on hero/large elements with no WebP/AVIF
  `source` (rule `PERF-IMG-FORMAT`, heuristic — only large images count).
- No `srcset` and a single `src` on a responsive-sized image.

## Measure it

- Network tab: transfer size and time of each image; the LCP image's load
  time.
- Lighthouse: "Properly size images" and "Serve images in next-gen
  formats" give concrete resizable/downloadable wins.
- Compare the requested bytes (`?w=` unset) vs the actual rendered size —
  that delta is pure waste.