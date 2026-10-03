#!/usr/bin/env python3
"""Tell Bing, Yandex and other IndexNow search engines that pages changed.

Run after a push has deployed:  python3 tools/indexnow.py
It submits every URL in sitemap.xml. The key file 0157152cd4bd10f0d8dbbb7dedaa19a2.txt at the site
root proves you own the site; keep it published.
"""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = "0157152cd4bd10f0d8dbbb7dedaa19a2"
HOST = "nithin434.github.io"

urls = re.findall(r"<loc>(https://[^<]+)</loc>", (ROOT / "sitemap.xml").read_text())
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req) as r:
    print(f"IndexNow: submitted {len(urls)} URLs, HTTP {r.status}")
