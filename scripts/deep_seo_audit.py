#!/usr/bin/env python3
"""
Deep SEO / GEO / entity audit for the Gerard Butler site.

Checks (per public page): title/meta length, canonical, OG/Twitter conflicts,
JSON-LD validity + types, H1 count, image alt/CLS/lazy, broken internal links,
content depth. Site-wide: robots.txt groups, sitemap coverage, AI surface
files, orphan pages, heavy assets.

Usage:
  python3 scripts/deep_seo_audit.py           # human summary
  python3 scripts/deep_seo_audit.py --json    # machine readable
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.gerardbutlerofficial.com"

# Scratch / QA pages that must never be indexed
NON_PUBLIC = {
    "compare.html",
    "compare_greenland.html",
    "find_gallery.html",
    "find_grid.html",
    "find_others.html",
    "gallery_check.html",
    "perf.html",
    "test_heli.html",
    "test_images.html",
    "test_reels.html",
}

TAG_RE = re.compile(r"<[^>]+>")


def strip_visible_text(html):
    html = re.sub(r"(?is)<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", html)
    return re.sub(r"\s+", " ", unescape(TAG_RE.sub(" ", html))).strip()


def get_meta(html, pattern):
    m = re.search(pattern, html, re.I | re.S)
    return unescape(m.group(1)).strip() if m else None


def parse_json_ld(html):
    blocks = re.findall(
        r'(?is)<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html
    )
    out, errors, types = [], [], []
    for b in blocks:
        try:
            data = json.loads(b.strip())
        except Exception as exc:  # noqa: BLE001
            errors.append("invalid JSON-LD: %s" % exc)
            continue
        out.append(data)
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else []
        for node in nodes:
            if isinstance(node, dict) and node.get("@type"):
                t = node["@type"]
                types.extend(t if isinstance(t, list) else [t])
    return out, errors, types


def resolve_internal(target):
    """Map an internal href/URL to a file on disk, or None if external/anchor."""
    if not target:
        return None
    target = target.split("#")[0].split("?")[0].strip()
    if not target or target.startswith(("mailto:", "tel:", "javascript:", "sms:")):
        return None
    if target.startswith(("http://", "https://")):
        if not target.startswith(BASE):
            return None
        target = target[len(BASE):] or "/"
    rel = target.lstrip("/")
    rel = rel[2:] if rel.startswith("./") else rel
    if rel == "":
        return os.path.join(ROOT, "index.html")
    for c in (
        os.path.join(ROOT, rel),
        os.path.join(ROOT, rel + ".html"),
        os.path.join(ROOT, rel, "index.html"),
    ):
        if os.path.isfile(c):
            return c
    return os.path.join(ROOT, rel)  # missing


def audit_page(path):
    name = os.path.basename(path)
    html = open(path, encoding="utf-8", errors="ignore").read()
    url = BASE + "/" if name == "index.html" else "%s/%s" % (BASE, name[:-5])

    title = get_meta(html, r"<title[^>]*>(.*?)</title>")
    desc = get_meta(html, r'<meta[^>]+name="description"[^>]+content="([^"]*)"')
    if not desc:
        desc = get_meta(html, r'<meta[^>]+content="([^"]*)"[^>]+name="description"')
    canonical = get_meta(html, r'<link[^>]+rel="canonical"[^>]+href="([^"]*)"')

    og_titles = re.findall(r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"', html, re.I | re.S)
    og_imgs = re.findall(r'<meta[^>]+property="og:image"[^>]+content="([^"]*)"', html, re.I | re.S)
    tw_cards = re.findall(r'<meta[^>]+name="twitter:card"', html, re.I)
    tw_titles = re.findall(
        r'<meta[^>]+name="twitter:title"[^>]+content="([^"]*)"', html, re.I | re.S
    )

    h1_text = [
        re.sub(r"\s+", " ", TAG_RE.sub("", h)).strip()
        for h in re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", html)
    ]

    imgs = re.findall(r"(?is)<img\b[^>]*>", html)
    img_total = len(imgs)
    img_no_alt = sum(1 for i in imgs if not re.search(r'\balt=["\'][^"\']+["\']', i, re.I))
    img_no_dims = sum(
        1
        for i in imgs
        if not (re.search(r"\bwidth=", i, re.I) and re.search(r"\bheight=", i, re.I))
    )
    img_no_lazy = sum(
        1
        for i in imgs
        if not re.search(r'loading=["\']lazy["\']', i, re.I)
        and not re.search(r'fetchpriority=["\']high["\']', i, re.I)
    )

    hrefs = re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\']', html, re.I)
    internal = {
        h for h in hrefs if not h.startswith(("http", "mailto:", "tel:", "#", "javascript:"))
    }

    _ld, ld_errors, ld_types = parse_json_ld(html)
    words = len(strip_visible_text(html).split())

    issues = []
    if not title:
        issues.append("missing <title>")
    elif len(title) > 60:
        issues.append("title too long (%d chars)" % len(title))
    if not desc:
        issues.append("missing meta description")
    elif not 120 <= len(desc) <= 160:
        issues.append("meta description length %d (target 120-160)" % len(desc))
    if not canonical:
        issues.append("missing canonical")
    elif canonical.rstrip("/") != url.rstrip("/"):
        issues.append("canonical mismatch: %s" % canonical)
    if len(og_titles) > 1:
        issues.append("%d og:title tags (conflict)" % len(og_titles))
    if len(og_imgs) > 1:
        issues.append("%d og:image tags" % len(og_imgs))
    if len(tw_cards) > 1:
        issues.append("%d twitter:card tags (conflict)" % len(tw_cards))
    if len(set(tw_titles)) > 1:
        issues.append("conflicting twitter:title values")
    if len(h1_text) != 1:
        issues.append("%d <h1> tags" % len(h1_text))
    if img_no_alt:
        issues.append("%d/%d images without alt" % (img_no_alt, img_total))
    if img_no_dims:
        issues.append("%d/%d images without width/height" % (img_no_dims, img_total))
    if ld_errors:
        issues.extend(ld_errors)
    if words < 600:
        issues.append("thin content (%d words)" % words)

    return {
        "file": name,
        "url": url,
        "title": title,
        "title_len": len(title or ""),
        "desc_len": len(desc or ""),
        "canonical": canonical,
        "og_image": og_imgs[0] if og_imgs else None,
        "schema_types": sorted(set(ld_types)),
        "h1": h1_text,
        "words": words,
        "images": img_total,
        "img_no_lazy": img_no_lazy,
        "issues": issues,
        "internal_links": sorted(internal),
        "mtime": datetime.fromtimestamp(os.path.getmtime(path), timezone.utc).date().isoformat(),
    }


def audit_site(pages):
    titles = {}
    for p in pages:
        titles.setdefault(p["title"], []).append(p["file"])
    dup_titles = {t: v for t, v in titles.items() if len(v) > 1}

    broken, inbound = {}, {}
    for p in pages:
        for href in p["internal_links"]:
            target = resolve_internal(href)
            if not target:
                continue
            if not os.path.isfile(target):
                broken.setdefault(p["file"], []).append(href)
            else:
                inbound.setdefault(os.path.basename(target), set()).add(p["file"])

    orphans = [p["file"] for p in pages if p["file"] != "index.html" and p["file"] not in inbound]

    robots_issues = []
    robots_path = os.path.join(ROOT, "robots.txt")
    if not os.path.exists(robots_path):
        robots_issues.append("robots.txt missing")
    else:
        robots = open(robots_path, encoding="utf-8").read()
        if "Sitemap:" not in robots:
            robots_issues.append("no Sitemap: directive")
        group, disallow_groups, ai_agents = None, set(), []
        for line in robots.splitlines():
            line = line.split("#")[0].strip()
            if not line:
                continue
            key, _, val = line.partition(":")
            key, val = key.strip().lower(), val.strip()
            if key == "user-agent":
                group = val
                if val not in ("*",) and val not in ai_agents:
                    ai_agents.append(val)
            elif key == "disallow" and group:
                disallow_groups.add(group)
        if disallow_groups and "*" not in disallow_groups:
            robots_issues.append(
                "Disallow rules scoped to specific bots only: " + ", ".join(sorted(disallow_groups))
            )

    sitemap_locs = []
    sm_path = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(sm_path):
        sitemap_locs = re.findall(r"<loc>(.*?)</loc>", open(sm_path, encoding="utf-8").read())
    public = {p["url"].rstrip("/") for p in pages}
    sm_set = {u.rstrip("/") for u in sitemap_locs}

    ai_files = {}
    for f in ("llms.txt", "llms-full.txt", "ai-knowledge.json", "feed.xml"):
        fp = os.path.join(ROOT, f)
        ai_files[f] = os.path.getsize(fp) if os.path.exists(fp) else 0

    heavy = []
    for dirpath, _dirs, files in os.walk(ROOT):
        if "/.git" in dirpath or "/node_modules" in dirpath:
            continue
        for f in files:
            if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".avif", ".mp4", ".mov")):
                continue
            size = os.path.getsize(os.path.join(dirpath, f))
            if size > 500_000:
                heavy.append((os.path.relpath(os.path.join(dirpath, f), ROOT), size))
    heavy.sort(key=lambda x: -x[1])

    return {
        "duplicate_titles": dup_titles,
        "broken_links": broken,
        "orphan_pages": orphans,
        "robots_issues": robots_issues,
        "sitemap": {
            "urls": len(sitemap_locs),
            "missing_from_sitemap": sorted(u for u in public if u not in sm_set),
            "dead_entries": sorted(u for u in sm_set if u not in public),
        },
        "ai_surface": ai_files,
        "heavy_assets": heavy[:15],
    }


def main():
    pages = [
        audit_page(os.path.join(ROOT, f))
        for f in sorted(os.listdir(ROOT))
        if f.endswith(".html") and f not in NON_PUBLIC
    ]
    site = audit_site(pages)
    report = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pages_audited": len(pages),
        "total_issues": sum(len(p["issues"]) for p in pages),
        "pages": pages,
    }
    report.update(site)

    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
        return

    print("DEEP SEO AUDIT - %s" % report["generated"])
    print("Pages: %d | Issue findings: %d\n" % (len(pages), report["total_issues"]))
    for p in sorted(pages, key=lambda x: -len(x["issues"])):
        if not p["issues"]:
            continue
        print("%s  (%d words | schema: %s)" % (p["file"], p["words"], ", ".join(p["schema_types"]) or "none"))
        for i in p["issues"]:
            print("   - %s" % i)
        print()
    clean = [p["file"] for p in pages if not p["issues"]]
    print("Clean pages (%d): %s" % (len(clean), ", ".join(clean) or "none"))
    print("\nDuplicate titles: %s" % (json.dumps(site["duplicate_titles"], indent=2) if site["duplicate_titles"] else "none"))
    print("Broken internal links: %s" % (json.dumps(site["broken_links"], indent=2) if site["broken_links"] else "none"))
    print("Orphan pages: %s" % (site["orphan_pages"] or "none"))
    print("robots.txt: %s" % (site["robots_issues"] or "ok"))
    print("sitemap: %d urls" % site["sitemap"]["urls"])
    print("  missing: %s" % (site["sitemap"]["missing_from_sitemap"] or "none"))
    print("  dead entries: %s" % (site["sitemap"]["dead_entries"] or "none"))
    print("AI surface: %s" % site["ai_surface"])
    print("\nHeaviest assets:")
    for path, size in site["heavy_assets"][:10]:
        print("  %6.2f MB  %s" % (size / 1048576, path))


if __name__ == "__main__":
    main()
