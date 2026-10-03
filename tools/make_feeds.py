#!/usr/bin/env python3
"""Write public/atom.xml, public/rss.xml and public/feed.json from ITEMS below.

Run:  python3 tools/make_feeds.py
To add news, add an item at the top of ITEMS (newest first) and re-run.
Each item can carry an image (shown as a thumbnail by feed readers and
search engines) and an optional video attachment.
"""
import json
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SITE = "https://nithin434.github.io"
P = f"{SITE}/public"
NAME, EMAIL = "Nithin Jambula", "nithinjambula89@gmail.com"
TAGLINE = "Robotics software engineer: software for robots, system architecture and AI agents"
CATEGORIES = ["Robotics", "AI Agents", "System Architecture", "Nithin Jambula"]

# date, id, title, summary, link, image (path under public/ or None), video (path under public/ or None)
ITEMS = [
    ("2026-10-03", "vulcan-test-video", "Video: a test run of Vulcan at VIT-AP",
     "A short clip from a test run of Vulcan, the self-driving electric campus vehicle built by students at VIT-AP University.",
     f"{P}/gallery.html#vulcan-ride", "assets/video/vulcan-ride-poster.jpg", "assets/video/vulcan-ride.mp4"),
    ("2026-04-17", "context-rag", "Context-Preserving RAG system for enterprise documents",
     "Source-backed answers from PDF, DOCX and text files. Combines vector and BM25 keyword search, routes each question to the best search strategy, and records which passages every answer used.",
     f"{P}/projects/rag.html", None, None),
    ("2026-04-01", "airc-2026", "Paper at IEEE AIRC 2026: neuro-symbolic API security testing",
     "A Neuro-Symbolic AI Framework for Adaptive and Explainable API Security Testing. 7th International Conference on Artificial Intelligence, Robotics, and Control. DOI 10.1109/AIRC69745.2026.11631384.",
     "https://doi.org/10.1109/AIRC69745.2026.11631384", None, None),
    ("2025-12-26", "apriltag-rover", "AprilTag docking rover (ROS 2)",
     "A ROS 2 rover that finds and docks with its station on its own using AprilTag pose estimation and a multi-stage mission state machine.",
     f"{P}/projects/rover.html", None, None),
    ("2025-12-01", "ananta-swe", "Software Engineer, Robotics & Autonomy at Ananta Technologies",
     "Behavior trees, AprilTag-guided robot positioning, a 50+ scenario MuJoCo/Webots test suite (35% faster validation) and 2 robots taken from simulation to production.",
     f"{P}/cv.html", None, None),
    ("2025-11-12", "isai-nlp-2025", "Paper at IEEE iSAI-NLP 2025: deepfake and counterfeit currency detection",
     "Securing Reality: AI-Driven Detection of Deepfakes and Counterfeit Currency. 20th iSAI-NLP. DOI 10.1109/ISAI-NLP66160.2025.11320726.",
     "https://doi.org/10.1109/ISAI-NLP66160.2025.11320726", None, None),
    ("2025-10-25", "patchpilot", "PatchPilot: multi-agent code review with LangGraph",
     "AI agents review GitHub pull requests for security, quality and logic. A LangGraph state graph routes each pull request, and ChromaDB memory lets reviews learn from past issues.",
     f"{P}/projects/patchpilot.html", None, None),
    ("2025-10-01", "16fps", "16fps: multi-agent video generation",
     "A multi-agent system that generates consistent videos over a minute long from text, using memory, tool use and self-review.",
     f"{P}/projects/16fps.html", None, None),
    ("2024-11-01", "echosight-vikas", "EchoSight named awardee at Vikas 2024; patent filed",
     "Navigation glasses for the visually impaired running YOLOv8 at 45+ FPS on a Raspberry Pi, with spoken directions.",
     f"{P}/projects/echosight.html", "assets/img/photos/echo.jpg", None),
    ("2024-06-01", "air-centre", "Student research engineer at AIR Centre, VIT-AP",
     "LLM agents with rule-based reasoning for API security testing (+34% vulnerabilities found, 70% less manual testing), and a real-time AI voice calling agent.",
     f"{P}/projects/neurosecapi.html", None, None),
    ("2023-01-01", "vulcan", "Vulcan self-driving EV: perception & navigation lead",
     "DeepLabV3+ segmentation, lane following, CARLA + SAC + DAgger, real-time on NVIDIA Jetson.",
     f"{P}/projects/vulcan.html", "assets/img/photos/car.jpg", None),
]

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".mp4": "video/mp4"}


def media(path):
    """(absolute url, mime type, size in bytes) for a file under public/."""
    f = PUB / path
    return f"{P}/{path}", MIME[f.suffix.lower()], f.stat().st_size


def stamp(d):
    return datetime.fromisoformat(d).replace(tzinfo=timezone.utc)


def atom():
    out = ['<?xml version="1.0" encoding="utf-8"?>',
           '<?xml-stylesheet type="text/css" href="assets/css/feed.css"?>',
           '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xml:lang="en">',
           f"  <title>{NAME}</title>", f"  <subtitle>{escape(TAGLINE)}</subtitle>",
           f"  <id>{SITE}/</id>",
           f'  <link rel="self" type="application/atom+xml" href="{P}/atom.xml"/>',
           f'  <link rel="alternate" type="text/html" href="{SITE}/"/>',
           f"  <updated>{ITEMS[0][0]}T00:00:00Z</updated>",
           f"  <author><name>{NAME}</name><email>{EMAIL}</email><uri>{SITE}/</uri></author>",
           f"  <icon>{P}/assets/img/avatar/avatar-32.png</icon>",
           f"  <logo>{P}/assets/img/avatar/me-800.jpg</logo>",
           "  <rights>CC BY 4.0</rights>"]
    out += [f'  <category term="{escape(c)}"/>' for c in CATEGORIES]
    for d, i, title, summary, link, image, video in ITEMS:
        out += ["  <entry>", f"    <title>{escape(title)}</title>",
                f"    <id>tag:nithin434.github.io,{d}:{i}</id>",
                f'    <link rel="alternate" type="text/html" href="{escape(link)}"/>',
                f"    <updated>{d}T00:00:00Z</updated>", f"    <published>{d}T00:00:00Z</published>",
                f"    <summary>{escape(summary)}</summary>"]
        for m in (image, video):
            if m:
                url, mime, size = media(m)
                out.append(f'    <link rel="enclosure" type="{mime}" length="{size}" href="{url}"/>')
        if image:
            out.append(f'    <media:thumbnail url="{media(image)[0]}"/>')
        out.append("  </entry>")
    out.append("</feed>\n")
    (PUB / "atom.xml").write_text("\n".join(out))


def rss():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">',
           "<channel>", f"  <title>{NAME}</title>", f"  <link>{SITE}/</link>",
           f"  <description>{escape(TAGLINE)}</description>", "  <language>en</language>",
           f'  <atom:link href="{P}/rss.xml" rel="self" type="application/rss+xml"/>',
           f"  <lastBuildDate>{format_datetime(stamp(ITEMS[0][0]))}</lastBuildDate>",
           f"  <managingEditor>{EMAIL} ({NAME})</managingEditor>",
           f"  <image><url>{P}/assets/img/avatar/me.jpg</url><title>{NAME}</title><link>{SITE}/</link></image>"]
    out += [f"  <category>{escape(c)}</category>" for c in CATEGORIES]
    for d, i, title, summary, link, image, video in ITEMS:
        out += ["  <item>", f"    <title>{escape(title)}</title>", f"    <link>{escape(link)}</link>",
                f'    <guid isPermaLink="false">tag:nithin434.github.io,{d}:{i}</guid>',
                f"    <pubDate>{format_datetime(stamp(d))}</pubDate>",
                f"    <description>{escape(summary)}</description>"]
        enc = video or image          # RSS allows one enclosure per item
        if enc:
            url, mime, size = media(enc)
            out.append(f'    <enclosure url="{url}" length="{size}" type="{mime}"/>')
        if image:
            url, mime, _ = media(image)
            out.append(f'    <media:content url="{url}" medium="image" type="{mime}"/>')
            out.append(f'    <media:thumbnail url="{url}"/>')
        out.append("  </item>")
    out.append("</channel>\n</rss>\n")
    (PUB / "rss.xml").write_text("\n".join(out))


def json_feed():
    items = []
    for d, i, title, summary, link, image, video in ITEMS:
        it = {"id": f"tag:nithin434.github.io,{d}:{i}", "url": link, "title": title,
              "content_text": summary, "date_published": f"{d}T00:00:00Z", "tags": CATEGORIES[:3]}
        if image:
            it["image"] = media(image)[0]
        if video:
            url, mime, size = media(video)
            it["attachments"] = [{"url": url, "mime_type": mime, "size_in_bytes": size, "title": title}]
        items.append(it)
    feed = {"version": "https://jsonfeed.org/version/1.1", "title": NAME, "home_page_url": f"{SITE}/",
            "feed_url": f"{P}/feed.json", "description": TAGLINE,
            "icon": f"{P}/assets/img/avatar/me-800.jpg", "favicon": f"{P}/assets/img/avatar/avatar-32.png",
            "authors": [{"name": NAME, "url": f"{SITE}/", "avatar": f"{P}/assets/img/avatar/me.jpg"}],
            "language": "en", "items": items}
    (PUB / "feed.json").write_text(json.dumps(feed, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    atom(); rss(); json_feed()
    print(f"atom.xml, rss.xml, feed.json written ({len(ITEMS)} items)")
