# nithin434.github.io

Personal portfolio of **Nithin Jambula**: robotics software, agentic AI, architecture & infrastructure.
It's plain HTML and CSS with no build step. Live at <https://nithin434.github.io/>.

## Layout

```
public/                     ← everything here is published as-is
├── index.html              home: bio, summary, news, AIR Centre
├── projects.html           projects with photos + tool links
├── gallery.html            photos, awards, certificates
├── cv.html                 full CV in HTML
├── topics.html             keyword / tools index (SEO + cross-links)
├── cite.html               BibTeX + share links
├── CV.pdf                  main CV
├── atom.xml rss.xml feed.json      feeds (update all three for news)
├── sitemap.xml robots.txt llms.txt humans.txt CITATION.cff
├── nithin-jambula.vcf manifest.json opensearch.xml browserconfig.xml favicon.ico
├── .well-known/            webfinger, did.json, security.txt
└── assets/
    ├── css/                style.css (site), feed.css (styles feeds in the browser)
    ├── docs/               other PDFs (CV-ml.pdf)
    └── img/
        ├── avatar/         pixel avatar, sizes, og-image.jpg (generated)
        ├── photos/         800px web copies used on pages
        │   └── originals/  full-size photos (source of truth)
        ├── certs/          certificate images and issuer logos
        ├── px/             small pixel icons (spare)
        └── icons/          legacy app/tile icons
tools/
├── resize_photos.py        originals/ → photos/ (800px)
└── make_pixel_art.py       regenerates avatar, favicon, og-image
.github/workflows/pages.yml deploys public/ to GitHub Pages on push to main
```

## Adding a photo

1. Drop the full-size image in `public/assets/img/photos/originals/`.
2. `python3 tools/resize_photos.py` creates the web copy and prints its width and height.
3. In `gallery.html`, copy a `<figure>` block into the right section and edit the `src`, `alt` and caption.
4. Add an `<image:image>` line under the gallery entry in `sitemap.xml`.

## Adding news

Add a row to the News table in `index.html`. Add the same item to `atom.xml`, `rss.xml` and `feed.json`, newest first, and bump each feed's `updated` / `lastBuildDate`.

## Conventions

- Monochrome only. Icons come from [Font Awesome](https://fontawesome.com/) via cdnjs.
- Every page carries the same `#nav` block, the Umami script and a canonical URL. Copy them from an existing page.
- Use root-relative paths (`/assets/...`).
- Preview locally: `cd public && python3 -m http.server`
