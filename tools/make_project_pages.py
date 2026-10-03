#!/usr/bin/env python3
"""Generate one page per project in public/projects/<id>.html.

Source of truth is public/projects.html: each <div class="proj" id="..."> block
(title, links, photo, description, tools) becomes its own page with its own
title, description, heading and structured data, so search engines can rank
every project on its own. Also links each project title on projects.html to
its page. Re-run after editing projects.html, then run tools/seo_sync.py.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public/projects.html"
OUT = ROOT / "public/projects"
SITE = "https://nithin434.github.io"
OG_DEFAULT = f"{SITE}/public/assets/img/avatar/og-image.jpg"
UMAMI = '<script defer src="https://umami-ip.vercel.app/script.js" data-website-id="e11be2c5-c4ed-4f96-a3ac-426074b5b96f"></script>'
NAV = [("../../", "fa-house", "home"), ("../projects.html", "fa-robot", "projects"), ("../gallery.html", "fa-images", "gallery"),
       ("../cv.html", "fa-id-card", "cv"), ("../topics.html", "fa-tags", "topics"), ("../CV.pdf", "fa-file-pdf", "cv.pdf"),
       ("../atom.xml", "fa-rss", "atom")]


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def deeper(fragment):
    """Rewrite relative href/src from public/ to public/projects/."""
    return re.sub(r'(href|src)="(?!https?:|mailto:|#|\.\./\.\./)([^"]+)"', r'\1="../\2"', fragment)


def summary(desc, limit=158):
    out = ""
    for sentence in re.split(r"(?<=[.!?])\s+", desc):
        if len(out) + len(sentence) + 1 > limit:
            break
        out = (out + " " + sentence).strip()
    return out or desc[:limit].rsplit(" ", 1)[0] + "…"


def parse():
    s = SRC.read_text()
    projects, section = [], ""
    for m in re.finditer(r'<h2>.*?</i>\s*(.*?)</h2>|<div class="proj" id="([^"]+)">(.*?)\n</div>', s, flags=re.S):
        if m.group(1) is not None:
            section = text(m.group(1))
            continue
        pid, body = m.group(2), m.group(3)
        h3 = re.search(r"<h3>(.*?)</h3>", body, flags=re.S).group(1)
        small = re.search(r"<small>\((.*?)\)</small>", h3, flags=re.S)
        name = text(re.sub(r"<small>.*?</small>", "", h3, flags=re.S))
        name = re.sub(r"^<a [^>]*>|</a>$", "", name)
        img = re.search(r'<img class="photo" src="([^"]+)" width="(\d+)" height="(\d+)"[^>]*alt="([^"]*)"', body)
        paras = re.findall(r"<p>(.*?)</p>", body, flags=re.S)
        tools = re.search(r'<p class="tools">(.*?)</p>', body, flags=re.S)
        links = re.findall(r'<a href="(https?://[^"]+)">([^<]+)</a>', small.group(1)) if small else []
        projects.append({
            "id": pid, "name": name, "section": section,
            "meta_html": small.group(1) if small else "",
            "desc_html": paras[0].strip() if paras else "",
            "desc": text(paras[0]) if paras else "",
            "tools_html": tools.group(1).strip() if tools else "",
            "tools": [t.strip() for t in text(tools.group(1)).split("·")] if tools else [],
            "img": img.groups() if img else None,
            "repo": next((u for u, t in links if "github.com" in u), None),
            "links": links,
        })
    return projects


def page(p, all_projects):
    url = f"{SITE}/public/projects/{p['id']}.html"
    title = f"{p['name']} — Nithin Jambula"
    desc = summary(p["desc"])
    og_image = f"{SITE}/public/{p['img'][0]}" if p["img"] else OG_DEFAULT
    keywords = ", ".join([p["name"], "Nithin Jambula", p["section"]] + p["tools"])
    ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode" if p["repo"] else "CreativeWork",
        "@id": url, "name": p["name"], "description": p["desc"], "url": url,
        "author": {"@type": "Person", "@id": f"{SITE}/#person", "name": "Nithin Jambula", "url": f"{SITE}/"},
        "keywords": ", ".join(p["tools"]), "genre": p["section"],
        "isPartOf": {"@type": "CollectionPage", "url": f"{SITE}/public/projects.html", "name": "Projects — Nithin Jambula"},
        "inLanguage": "en", "license": "https://creativecommons.org/licenses/by/4.0/",
    }
    if p["repo"]:
        ld["codeRepository"] = p["repo"]
    if p["img"]:
        ld["image"] = og_image
    sameas = [u for u, _ in p["links"] if u != p["repo"]] + ([p["repo"]] if p["repo"] else [])
    if sameas:
        ld["sameAs"] = sameas
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Projects", "item": f"{SITE}/public/projects.html"},
        {"@type": "ListItem", "position": 3, "name": p["name"], "item": url}]}
    related = [q for q in all_projects if q["section"] == p["section"] and q["id"] != p["id"]]
    nav = " | ".join(f'<a href="{h}"><i class="fa-solid {i}" aria-hidden="true"></i> {t}</a>' for h, i, t in NAV)
    e = lambda t: html.escape(t, quote=True)
    photo = ""
    if p["img"]:
        src, w, h, alt = p["img"]
        photo = f'<p><img class="photo-full" src="../{src}" width="{w}" height="{h}" alt="{alt}"></p>\n'
    rel_html = "".join(f'  <li><a href="{q["id"]}.html">{html.escape(q["name"])}</a></li>\n' for q in related)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(keywords)}">
<meta name="author" content="Nithin Jambula">
<link rel="canonical" href="{url}">
<link rel="icon" href="../../favicon.ico" sizes="any">
<meta property="og:type" content="article">
<meta property="og:image" content="{og_image}">
<script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(crumbs, ensure_ascii=False)}
</script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">
<link rel="stylesheet" href="../assets/css/style.css">
{UMAMI}
</head>
<body>
<div id="page">

<div id="nav">
  [ {nav} ]
</div>

<p class="meta crumbs"><a href="../../">home</a> / <a href="../projects.html">projects</a> / {html.escape(p["name"])}</p>
<h1>{html.escape(p["name"])}<span class="cursor">_</span></h1>
<p class="meta">{html.escape(p["section"])}{" · " + deeper(p["meta_html"]) if p["meta_html"] else ""} · by <a href="../../">Nithin Jambula</a></p>

{photo}<p>{deeper(p["desc_html"])}</p>

<h2>Built with</h2>
<p class="tools">{deeper(p["tools_html"])}</p>

<h2>More {html.escape(p["section"].lower())}</h2>
<ul>
{rel_html}  <li><a href="../projects.html">all projects →</a></li>
</ul>

<div id="footer"></div>

</div>
</body>
</html>
'''


def link_titles(projects):
    """Make each project title on projects.html link to its own page."""
    s = SRC.read_text()
    for p in projects:
        block = re.search(rf'<div class="proj" id="{re.escape(p["id"])}">.*?<h3>', s, flags=re.S)
        start = block.end()
        if s.startswith('<a href="projects/', start):
            continue
        end = s.index(" <small>", start) if " <small>" in s[start:s.index("</h3>", start)] else s.index("</h3>", start)
        s = s[:start] + f'<a href="projects/{p["id"]}.html">' + s[start:end] + "</a>" + s[end:]
    SRC.write_text(s)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    projects = parse()
    for p in projects:
        (OUT / f"{p['id']}.html").write_text(page(p, projects))
    link_titles(projects)
    print(f"{len(projects)} project pages written to public/projects/")
