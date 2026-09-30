# nithin434.github.io

Personal portfolio of **Nithin Jambula**: robotics software, agentic AI, architecture & infrastructure.
It's plain HTML and CSS with no build step. Live at <https://nithin434.github.io/>.

## Layout

```
./                              ← repo root = site root (GitHub Pages serves it as-is)
├── index.html                  home page, the only page at the root
├── 404.html                    not-found page (GitHub requires it at the root)
├── favicon.ico robots.txt sitemap.xml llms.txt CITATION.cff
│                               files crawlers / GitHub only look for at the root
├── .nojekyll                   serve files raw: no Jekyll, no README rendering
├── .well-known/                webfinger, did.json, security.txt
├── public/                     everything else
│   ├── projects.html gallery.html cv.html topics.html cite.html
│   ├── CV.pdf
│   ├── atom.xml rss.xml feed.json      feeds (update all three for news)
│   ├── humans.txt nithin-jambula.vcf manifest.json opensearch.xml browserconfig.xml
│   └── assets/
│       ├── css/                style.css (site), feed.css (styles feeds in the browser)
│       ├── docs/               other PDFs (CV-ml.pdf)
│       └── img/
│           ├── avatar/         pixel avatar, sizes, og-image.jpg (generated)
│           ├── photos/         800px web copies used on pages
│           │   └── originals/  full-size photos (source of truth)
│           ├── certs/          certificate images and issuer logos
│           ├── px/             small pixel icons (spare)
│           └── icons/          legacy app/tile icons
├── tools/
│   ├── resize_photos.py        originals/ → photos/ (800px)
│   └── make_pixel_art.py       regenerates avatar, favicon, og-image
└── .github/workflows/pages.yml deploys the root to GitHub Pages on push to main
```

## Adding a photo

1. Drop the full-size image in `public/assets/img/photos/originals/`.
2. `python3 tools/resize_photos.py` creates the web copy and prints its width and height.
3. In `public/gallery.html`, copy a `<figure>` block into the right section and edit the `src`, `alt` and caption.
4. Add an `<image:image>` line under the gallery entry in `sitemap.xml`.

## Adding news

Add a row to the News table in `index.html`. Add the same item to `public/atom.xml`, `public/rss.xml` and `public/feed.json`, newest first, and bump each feed's `updated` / `lastBuildDate`.

## Conventions

- Monochrome only. Icons come from [Font Awesome](https://fontawesome.com/) via cdnjs.
- Every page carries the same `#nav` block, the Umami script and a canonical URL. Copy them from an existing page.
- Use relative paths (`public/assets/...` from `index.html`; `assets/...` and `../` from pages in `public/`) so the site works on GitHub Pages, under any sub-path, or opened from disk.
  The exception is `404.html`: GitHub serves it at any depth, so it uses absolute `https://nithin434.github.io/...` URLs.
- Preview locally: `python3 -m http.server` in the repo root
