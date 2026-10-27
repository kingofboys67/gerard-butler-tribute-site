#!/usr/bin/env python3
"""
Technical SEO hardening pass for the Gerard Butler site.

Fixes applied idempotently to every public page:
  1. De-duplicates conflicting twitter:* / og:* meta (each tag kept once)
  2. Rebuilds truncated / too-short meta descriptions from on-page copy
  3. Adds width/height (CLS) + loading=lazy/decoding=async to every <img>
  4. Promotes the LCP image to fetchpriority=high + <link rel=preload>
  5. Generates true 1200x630 Open Graph cards for poster-based pages
  6. Adds hreflang x-default, refreshes the visible "Last updated" date
  7. Adds a site-wide crawlable footer index (fixes orphan pages)

Run:  python3 scripts/seo_hardening.py
"""

import os
import re
import subprocess
from datetime import date

from PIL import Image, ImageEnhance, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.gerardbutlerofficial.com"
OG_DIR = os.path.join(ROOT, "img", "og")

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
IMG_RE = re.compile(r"<img\b[^>]*>", re.I | re.S)


# --------------------------------------------------------------------------- utils
def public_pages():
    return [
        f
        for f in sorted(os.listdir(ROOT))
        if f.endswith(".html") and f not in NON_PUBLIC
    ]


_size_cache = {}


def image_size(rel_path):
    """Return (w, h) for a local image referenced as /img/x.jpg, else None."""
    rel_path = rel_path.lstrip("/")
    if rel_path in _size_cache:
        return _size_cache[rel_path]
    fp = os.path.join(ROOT, rel_path)
    dims = None
    if os.path.isfile(fp):
        try:
            with Image.open(fp) as im:
                dims = im.size
        except Exception:  # noqa: BLE001 - avif etc. fall back to sips
            try:
                out = subprocess.run(
                    ["sips", "-g", "pixelWidth", "-g", "pixelHeight", fp],
                    capture_output=True,
                    text=True,
                    timeout=20,
                ).stdout
                w = re.search(r"pixelWidth:\s*(\d+)", out)
                h = re.search(r"pixelHeight:\s*(\d+)", out)
                if w and h:
                    dims = (int(w.group(1)), int(h.group(1)))
            except Exception:  # noqa: BLE001
                dims = None
    _size_cache[rel_path] = dims
    return dims


def visible_text(html):
    html = re.sub(r"(?is)<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", html)
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", html)).strip()


def shorten(text, limit=158):
    """Trim to <= limit chars on a word (ideally sentence) boundary."""
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    window = text[:limit]
    stop = max(window.rfind(". "), window.rfind("! "), window.rfind("? "))
    if stop > 90:
        return window[: stop + 1]
    cut = window[: window.rfind(" ")].rstrip(" ,;:-–—")
    return cut


# ----------------------------------------------------------------- descriptions
def source_copy(html):
    """Best available descriptive paragraph for building a meta description."""
    m = re.search(r"(?is)<strong>Overview:</strong>(.*?)</p>", html)
    if m and len(visible_text(m.group(1))) > 80:
        return visible_text(m.group(1))
    for p in re.findall(r"(?is)<p\b[^>]*>(.*?)</p>", html):
        txt = visible_text(p)
        if len(txt) > 120 and "cookie" not in txt.lower():
            return txt
    return ""


def build_description(html, title):
    current = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S
    )
    current = current.group(1).strip() if current else ""
    if 120 <= len(current) <= 160 and not current.endswith(("...", "..", "…")):
        return current
    body = source_copy(html)
    if body:
        desc = shorten(body, 157)
        if len(desc) >= 110:
            return desc
    base = shorten(current.replace("...", "").strip(), 157) if current else ""
    if len(base) >= 110:
        return base
    return shorten(
        "%s — biography, filmography, trailers, streaming guide, news and charity work "
        "from the Gerard Butler archive." % (title or "Gerard Butler"),
        157,
    )


# ------------------------------------------------------------ social meta cleanup
def dedupe_social_meta(html):
    """Keep only the first instance of each twitter:*/og:* meta property."""
    seen = set()

    def repl(m):
        key = (m.group(1).lower(), m.group(2).lower())
        if key in seen:
            return ""
        seen.add(key)
        return m.group(0)

    html = re.sub(
        r'[ \t]*<meta[^>]+(?:name|property)=["\'](twitter:[a-zA-Z:]+|og:[a-zA-Z:]+)["\'][^>]*>\n?',
        repl,
        html,
        flags=re.I,
    )
    # collapse the now-empty comment placeholders ("<!-- Open Graph / Facebook -->\n\n<!-- Twitter -->")
    html = re.sub(r"<!-- Open Graph / [^>]*-->\s*(?=<!-- Twitter -->|<!-- JSON-LD|<link)", "", html)
    return html


def sync_social_copy(html, desc, title):
    """Make og/twitter descriptions and titles agree with the canonical pair."""
    html = re.sub(
        r'(<meta[^>]+property=["\']og:description["\'][^>]+content=["\']).*?(["\'][^>]*>)',
        lambda m: m.group(1) + desc + m.group(2),
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'(<meta[^>]+name=["\']twitter:description["\'][^>]+content=["\']).*?(["\'][^>]*>)',
        lambda m: m.group(1) + desc + m.group(2),
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'(<meta[^>]+name=["\']twitter:title["\'][^>]+content=["\']).*?(["\'][^>]*>)',
        lambda m: m.group(1) + (title or "") + m.group(2),
        html,
        count=1,
        flags=re.I | re.S,
    )
    if "twitter:image:alt" not in html:
        html = re.sub(
            r'(<meta[^>]+name=["\']twitter:image["\'][^>]*>)',
            r'\1\n  <meta name="twitter:image:alt" content="'
            + (title or "").replace('"', "&quot;")
            + '">',
            html,
            count=1,
            flags=re.I,
        )
    return html


# ------------------------------------------------------------------- image attrs
def fix_image_tags(html, page):
    """Add intrinsic dimensions, lazy-loading and an LCP hint to <img> tags."""
    first = {"done": False}

    def repl(m):
        tag = m.group(0)
        src = re.search(r'src=["\']([^"\']+)["\']', tag)
        if not src:
            return tag
        ref = src.group(1)
        dims = None if ref.startswith("http") else image_size(ref)
        is_hero = not first["done"] and (
            page == "index.html" or "hero" in tag.lower() or "poster" in ref.lower()
        )
        first["done"] = True

        attrs = {}
        for key in ("width", "height", "loading", "decoding", "fetchpriority"):
            found = re.search(r'\b%s=["\']?([^"\' >]+)' % key, tag, re.I)
            if found:
                attrs[key] = found.group(1)

        additions = []
        if dims:
            w, h = dims
            if page == "index.html" and "hero" not in tag.lower() and w > 1400:
                w, h = int(w * 0.75), int(h * 0.75)
            if "width" not in attrs:
                additions.append('width="%d"' % w)
            if "height" not in attrs:
                additions.append('height="%d"' % h)
        if is_hero:
            if "fetchpriority" not in attrs:
                additions.append('fetchpriority="high"')
            if "loading" not in attrs:
                additions.append('loading="eager"')
        elif "loading" not in attrs:
            additions.append('loading="lazy"')
        if "decoding" not in attrs:
            additions.append('decoding="async"')

        if not additions:
            return tag
        return tag[:-1].rstrip() + " " + " ".join(additions) + ">"

    html = IMG_RE.sub(repl, html)

    if page == "index.html" and 'rel="preload" as="image"' not in html:
        m = re.search(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*fetchpriority="high"', html)
        if m:
            html = re.sub(
                r'(<link rel="preconnect" href="https://fonts.googleapis.com">)',
                '<link rel="preload" as="image" href="%s" fetchpriority="high">\n  \\1'
                % m.group(1),
                html,
                count=1,
            )
    return html


# --------------------------------------------------------------------- OG cards
def make_og_card(src_rel, out_name):
    """Compose a 1200x630 social card: blurred cover art + centred poster."""
    out = os.path.join(OG_DIR, out_name)
    if os.path.exists(out):
        return "/img/og/" + out_name
    src = os.path.join(ROOT, src_rel.lstrip("/"))
    if not os.path.isfile(src):
        return None
    try:
        poster = Image.open(src).convert("RGB")
    except Exception:  # noqa: BLE001
        return None

    W, H = 1200, 630
    scale = max(W / poster.width, H / poster.height)
    bg = poster.resize(
        (max(1, int(poster.width * scale)), max(1, int(poster.height * scale))), Image.LANCZOS
    )
    left, top = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((left, top, left + W, top + H))
    bg = bg.filter(ImageFilter.GaussianBlur(26))
    bg = ImageEnhance.Brightness(bg).enhance(0.42)
    bg = ImageEnhance.Color(bg).enhance(0.85)

    ph = H - 84
    pw = max(1, int(poster.width * ph / poster.height))
    bg.paste(poster.resize((pw, ph), Image.LANCZOS), ((W - pw) // 2, 42))

    os.makedirs(OG_DIR, exist_ok=True)
    bg.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return "/img/og/" + out_name


def fix_og_image(html, page):
    """Point og:image/twitter:image at a real 1200x630 asset with correct dims."""
    m = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.I
    )
    if not m:
        return html
    local = m.group(1).replace(BASE, "")
    if "/img/og/" in local or not local.startswith("/"):
        return html
    dims = image_size(local)
    if dims and 1.6 <= dims[0] / dims[1] <= 2.1:
        card = local
    else:
        card = make_og_card(local, page[:-5] + ".jpg")
    if not card:
        return html

    new_url = BASE + card
    for pattern in (
        r'(<meta[^>]+property=["\']og:image["\'][^>]+content=["\']).*?(["\'])',
        r'(<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']).*?(["\'])',
    ):
        html = re.sub(
            pattern,
            lambda mm: mm.group(1) + new_url + mm.group(2),
            html,
            count=1,
            flags=re.I,
        )
    for prop, val in (("og:image:width", "1200"), ("og:image:height", "630")):
        if prop in html:
            html = re.sub(
                r'(<meta[^>]+property=["\']%s["\'][^>]+content=["\']).*?(["\'])' % prop,
                lambda mm: mm.group(1) + val + mm.group(2),
                html,
                count=1,
                flags=re.I,
            )
    return html


# ------------------------------------------------------------- hreflang + footer
def add_hreflang(html):
    if 'hreflang="x-default"' in html:
        return html
    m = re.search(r'<link rel="canonical" href="([^"]+)">', html)
    if not m:
        return html
    return html.replace(
        m.group(0),
        m.group(0) + '\n  <link rel="alternate" hreflang="en" href="%s">'
        '\n  <link rel="alternate" hreflang="x-default" href="%s">' % (m.group(1), m.group(1)),
        1,
    )


FOOTER_SECTIONS = [
    ("Career & Archive", [
        ("about", "Biography"),
        ("career-early-years", "Early Career 1990–1999"),
        ("career-breakthrough", "Breakthrough Era 2000–2009"),
        ("career-franchise-producer", "Franchise & Producer Era"),
        ("award-mtv-best-fight", "MTV Best Fight Award"),
        ("award-taurus-stunt", "Taurus World Stunt Award"),
        ("award-golden-camera", "Golden Camera Award"),
    ]),
    ("Films & Video", [
        ("films", "All Films A–Z"),
        ("reels", "Video Reels"),
        ("gallery", "Photo Gallery"),
        ("news", "News & Updates"),
    ]),
    ("Popular Films", [
        ("movie-300", "300 (2006)"),
        ("movie-olympus-has-fallen", "Olympus Has Fallen"),
        ("movie-london-has-fallen", "London Has Fallen"),
        ("movie-angel-has-fallen", "Angel Has Fallen"),
        ("movie-greenland", "Greenland"),
        ("movie-law-abiding-citizen", "Law Abiding Citizen"),
        ("movie-den-of-thieves", "Den of Thieves"),
        ("movie-how-to-train-your-dragon", "How to Train Your Dragon"),
        ("movie-plane", "Plane (2023)"),
        ("movie-phantom-of-the-opera", "The Phantom of the Opera"),
    ]),
    ("Community", [
        ("charity", "Charity & Mary's Meals"),
        ("fanclub", "VIP Fan Club"),
        ("auctions", "Charity Auctions"),
        ("meet-greet", "Meet & Greet"),
        ("private-shows", "Private Screenings"),
        ("vip-treatment", "VIP Treatment"),
        ("verify", "Member Verification"),
    ]),
]


def footer_index_html():
    cols = []
    for heading, links in FOOTER_SECTIONS:
        items = "".join('<li><a href="%s">%s</a></li>' % (href, label) for href, label in links)
        cols.append('<div class="footer-col"><h3>%s</h3><ul>%s</ul></div>' % (heading, items))
    return (
        '\n      <nav class="footer-index" aria-label="Site index">'
        + "".join(cols)
        + "</nav>"
    )


def update_footer(html):
    if '<span class="last-updated-date">' in html:
        today = date.today()
        html = re.sub(
            r'<span class="last-updated-date">.*?</span>',
            '<span class="last-updated-date">Last updated: '
            '<time datetime="%s">%s</time></span>'
            % (today.isoformat(), today.strftime("%B %-d, %Y")),
            html,
            count=1,
            flags=re.S,
        )
    if "footer-index" not in html and '<div class="footer-copy">' in html:
        html = html.replace(
            '<div class="footer-copy">', footer_index_html() + '\n      <div class="footer-copy">', 1
        )
    return html


# ---------------------------------------------------------------------- pipeline
def main():
    changed = 0
    for page in public_pages():
        path = os.path.join(ROOT, page)
        original = open(path, encoding="utf-8").read()
        html = original

        title_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        title = visible_text(title_m.group(1)) if title_m else ""

        html = dedupe_social_meta(html)
        desc = build_description(html, title)
        desc_attr = desc.replace("&", "&amp;").replace('"', "&quot;")
        html = re.sub(
            r'(<meta[^>]+name=["\']description["\'][^>]+content=["\']).*?(["\'])',
            lambda m: m.group(1) + desc_attr + m.group(2),
            html,
            count=1,
            flags=re.I | re.S,
        )
        html = sync_social_copy(html, desc_attr, title)
        html = fix_og_image(html, page)
        html = fix_image_tags(html, page)
        html = add_hreflang(html)
        html = update_footer(html)

        if html != original:
            open(path, "w", encoding="utf-8").write(html)
            changed += 1
            print("updated %s" % page)
    print("\n%d/%d pages updated" % (changed, len(public_pages())))


if __name__ == "__main__":
    main()
