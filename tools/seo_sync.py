#!/usr/bin/env python3
"""Keep SEO tags, footers and sitemap.xml consistent across every page.

Run from anywhere:  python3 tools/seo_sync.py
Safe to re-run: it only adds tags a page is missing, replaces the footer
between the FOOTER markers, and rewrites sitemap.xml from PAGES below.
When you add a page, add it to PAGES and re-run.
"""
import html
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://nithin434.github.io"
OG_IMAGE = f"{SITE}/public/assets/img/avatar/og-image.jpg"
TODAY = date.today().isoformat()

# path, sitemap priority, changefreq, breadcrumb name, images [(url path, caption)]
PAGES = [
    ("index.html", "1.0", "monthly", "Home", [("public/assets/img/avatar/avatar-512.png", "Pixel-art avatar of Nithin Jambula")]),
    ("public/projects.html", "0.9", "monthly", "Projects", [
        ("public/assets/img/photos/car.jpg", "Vulcan self-driving campus EV"),
        ("public/assets/img/photos/echo.jpg", "EchoSight navigation glasses for the visually impaired"),
    ]),
    ("public/cv.html", "0.9", "monthly", "CV", []),
    ("public/gallery.html", "0.8", "monthly", "Gallery", [
        ("public/assets/img/photos/car.jpg", "Vulcan self-driving campus EV"),
        ("public/assets/img/photos/vlan.jpg", "Vulcan at VLaunchpad 2025"),
        ("public/assets/img/photos/echo.jpg", "EchoSight prototype"),
        ("public/assets/img/photos/vikas.jpg", "Vikas 2024 Innovation Challenge"),
        ("public/assets/img/certs/stanford.png", "Machine Learning Specialization, Stanford and DeepLearning.AI"),
        ("public/assets/img/certs/IBM_DLF.png", "Deep Learning Fundamentals, IBM"),
        ("public/assets/img/certs/IBM_P.png", "Machine Learning with Python, IBM"),
        ("public/assets/img/certs/IBM_S.png", "Machine Learning Specialist Advanced, IBM"),
        ("public/assets/img/certs/oyo.png", "Object Detection Bootcamp, Google"),
    ]),
    ("public/topics.html", "0.7", "monthly", "Topics", []),
    ("public/cite.html", "0.6", "yearly", "Cite", []),
]
PDFS = [("public/CV.pdf", "0.8", "monthly")]

# Profiles and publications linked from every footer (backlinks).
PROFILES = [
    ("https://github.com/nithin434", "GitHub"),
    ("https://linkedin.com/in/nithin-jambula", "LinkedIn"),
    ("https://doi.org/10.1109/AIRC69745.2026.11631384", "IEEE AIRC 2026"),
    ("https://doi.org/10.1109/ISAI-NLP66160.2025.11320726", "IEEE iSAI-NLP 2025"),
    ("https://pypi.org/project/apk2abb/", "PyPI"),
    ("https://air.vitap.ac.in/", "AIR Centre, VIT-AP"),
    ("https://vitap.ac.in/", "VIT-AP University"),
]
SITE_LINKS = [
    ("index.html", "home"), ("public/projects.html", "projects"), ("public/gallery.html", "gallery"),
    ("public/cv.html", "cv"), ("public/topics.html", "topics"), ("public/cite.html", "cite"),
    ("public/CV.pdf", "cv.pdf"), ("public/atom.xml", "atom"), ("public/rss.xml", "rss"),
    ("public/feed.json", "json feed"), ("sitemap.xml", "sitemap"), ("llms.txt", "llms.txt"),
]
FOOTER_START, FOOTER_END = "<!-- FOOTER:start -->", "<!-- FOOTER:end -->"


def rel(from_page, target):
    """Relative link from one page to a repo-root path."""
    if from_page.startswith("public/"):
        if target == "index.html":
            return "../"
        return target[len("public/"):] if target.startswith("public/") else "../" + target
    return "./" if target == "index.html" else target


def page_url(path):
    return f"{SITE}/" if path == "index.html" else f"{SITE}/{path}"


def footer(page):
    profiles = " ·\n  ".join(f'<a href="{u}" rel="me noopener">{t}</a>' if "nithin" in u else f'<a href="{u}">{t}</a>'
                              for u, t in PROFILES)
    links = " · ".join(f'<a href="{rel(page, p)}">{t}</a>' for p, t in SITE_LINKS)
    return (f'{FOOTER_START}\n<div id="footer">\n  {profiles}<br>\n  {links}<br>\n'
            f'  © 2023–{date.today().year} Nithin Jambula · '
            f'<a href="mailto:nithinjambula89@gmail.com">nithinjambula89@gmail.com</a> · '
            f'text under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>\n</div>\n{FOOTER_END}')


def meta(s, pattern):
    m = re.search(pattern, s)
    return html.unescape(m.group(1)) if m else ""


def sync_page(path, crumb):
    p = ROOT / path
    s = p.read_text()
    title = meta(s, r"<title>(.*?)</title>")
    desc = meta(s, r'<meta name="description" content="([^"]*)"')
    url = page_url(path)
    icon_prefix = "" if path == "index.html" else "../"
    asset = "public/" if path == "index.html" else ""
    esc = lambda t: html.escape(t, quote=True)

    wanted = [
        ("name=\"robots\"", '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">'),
        ("theme-color", '<meta name="theme-color" content="#000000">'),
        ("og:type", f'<meta property="og:type" content="{"profile" if path in ("index.html", "public/cv.html") else "website"}">'),
        ("og:site_name", '<meta property="og:site_name" content="Nithin Jambula">'),
        ("og:title", f'<meta property="og:title" content="{esc(title)}">'),
        ("og:description", f'<meta property="og:description" content="{esc(desc)}">'),
        ("og:url", f'<meta property="og:url" content="{url}">'),
        ("og:image\"", f'<meta property="og:image" content="{OG_IMAGE}">'),
        ("og:locale", '<meta property="og:locale" content="en_US">'),
        ("twitter:card", '<meta name="twitter:card" content="summary_large_image">'),
        ("twitter:title", f'<meta name="twitter:title" content="{esc(title)}">'),
        ("twitter:description", f'<meta name="twitter:description" content="{esc(desc)}">'),
        ("twitter:image", f'<meta name="twitter:image" content="{OG_IMAGE}">'),
        ("apple-touch-icon", f'<link rel="apple-touch-icon" href="{asset}assets/img/avatar/avatar-180.png">'),
        ("rel=\"manifest\"", f'<link rel="manifest" href="{asset}manifest.json">'),
        ("application/atom+xml", f'<link rel="alternate" type="application/atom+xml" title="Nithin Jambula (Atom)" href="{asset}atom.xml">'),
        ("application/rss+xml", f'<link rel="alternate" type="application/rss+xml" title="Nithin Jambula (RSS)" href="{asset}rss.xml">'),
        ("rel=\"sitemap\"", f'<link rel="sitemap" type="application/xml" title="Sitemap" href="{icon_prefix}sitemap.xml">'),
        ("rel=\"author\"", f'<link rel="author" href="{asset}humans.txt">'),
        ('rel="me" href="https://github.com', '<link rel="me" href="https://github.com/nithin434">'),
        ('rel="me" href="https://linkedin.com', '<link rel="me" href="https://linkedin.com/in/nithin-jambula">'),
    ]
    missing = [tag for key, tag in wanted if key not in s]
    if crumb != "Home" and "BreadcrumbList" not in s:
        missing.append(
            '<script type="application/ld+json">\n'
            '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [\n'
            f'  {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/"}},\n'
            f'  {{"@type": "ListItem", "position": 2, "name": "{crumb}", "item": "{url}"}}\n]}}\n</script>')
    if missing:
        anchor = s.index('<link rel="stylesheet"')
        s = s[:anchor] + "\n".join(missing) + "\n" + s[anchor:]

    # Replace the footer (first run: the old <div id="footer">...</div>).
    new_footer = footer(path)
    if FOOTER_START in s:
        s = re.sub(re.escape(FOOTER_START) + r".*?" + re.escape(FOOTER_END), lambda _: new_footer, s, flags=re.S)
    else:
        s = re.sub(r'<div id="footer">.*?</div>', lambda _: new_footer, s, count=1, flags=re.S)
    p.write_text(s)
    return len(missing)


def write_sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for path, prio, freq, _, images in PAGES:
        out += ["  <url>", f"    <loc>{page_url(path)}</loc>", f"    <lastmod>{TODAY}</lastmod>",
                f"    <changefreq>{freq}</changefreq>", f"    <priority>{prio}</priority>"]
        for img, cap in images:
            out.append(f"    <image:image><image:loc>{SITE}/{img}</image:loc>"
                       f"<image:title>{html.escape(cap)}</image:title></image:image>")
        out.append("  </url>")
    for path, prio, freq in PDFS:
        out += ["  <url>", f"    <loc>{SITE}/{path}</loc>", f"    <lastmod>{TODAY}</lastmod>",
                f"    <changefreq>{freq}</changefreq>", f"    <priority>{prio}</priority>", "  </url>"]
    out.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(out))


if __name__ == "__main__":
    for path, _, _, crumb, _ in PAGES:
        print(f"{path}: added {sync_page(path, crumb)} tags, footer synced")
    write_sitemap()
    print("sitemap.xml written")
