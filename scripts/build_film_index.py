#!/usr/bin/env python3
"""
Builds the crawlable filmography index and per-film cross-links.

Why: ~20 film pages (incl. /movie-300) had no internal links pointing at them,
so they were orphaned for crawlers. This script:

  1. Parses every movie-*.html page for title, year, character, director, poster
  2. Appends a complete "Filmography A-Z" + "By release year" table to films.html
  3. Adds a "Continue the filmography" prev/next + back-to-index block to each film page
  4. Emits Film + CollectionPage JSON-LD for the index (ItemList of all films)

Idempotent: existing generated blocks are replaced, not duplicated.

Run:  python3 scripts/build_film_index.py
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.gerardbutlerofficial.com"
MARK_A = '<section class="section film-az" id="film-index">'
MARK_END = "</section>\n\n  </main>"
CROSS_MARK = "<!-- cross-links:generated -->"


def txt(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def parse_film(path):
    html = open(path, encoding="utf-8").read()
    title = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    year = re.search(r"//\s*(\d{4})\s*RELEASE", html)
    poster = re.search(r'<img[^>]+src="(img/[^"]+)"[^>]*>', html)

    def row(label):
        m = re.search(
            r"<td[^>]*>\s*%s\s*</td>\s*<td[^>]*>(.*?)</td>" % label, html, re.I | re.S
        )
        return txt(m.group(1)) if m else ""

    return {
        "file": os.path.basename(path),
        "slug": os.path.basename(path)[:-5],
        "title": txt(title.group(1)) if title else "",
        "year": year.group(1) if year else "",
        "character": row("Character Role"),
        "director": row("Director"),
        "poster": poster.group(1) if poster else "",
    }


def film_list():
    films = [
        parse_film(os.path.join(ROOT, f))
        for f in sorted(os.listdir(ROOT))
        if f.startswith("movie-") and f.endswith(".html")
    ]
    films = [f for f in films if f["title"] and f["year"]]
    films.sort(key=lambda f: (f["title"].lower(), f["year"]))
    return films


def index_section(films):
    az = []
    for f in films:
        role = f" — {f['character']}" if f["character"] else ""
        az.append(
            '<li><a href="%s">%s (%s)%s</a></li>' % (f["slug"], f["title"], f["year"], role)
        )

    rows = []
    for f in sorted(films, key=lambda x: (-int(x["year"]), x["title"])):
        rows.append(
            "<tr><td>%s</td><td><a href=\"%s\">%s</a></td><td>%s</td><td>%s</td></tr>"
            % (f["year"], f["slug"], f["title"], f["character"] or "—", f["director"] or "—")
        )

    return """
  %s
    <div class="section-head">
      <div class="eyebrow">// Complete film index</div>
      <h2 class="display-font">Gerard Butler Filmography A&ndash;Z</h2>
      <p class="section-intro">Every Gerard Butler feature film in this archive, from <em>300</em> and the
      <em>Has Fallen</em> series to <em>Greenland</em>, <em>Den of Thieves</em> and
      <em>How to Train Your Dragon</em>. Each entry links to the full film page with synopsis,
      character, director, trailer and streaming options.</p>
    </div>

    <h3 class="sub-head">By release year</h3>
    <div class="table-wrap">
      <table class="film-table">
        <thead><tr><th>Year</th><th>Film</th><th>Gerard Butler plays</th><th>Director</th></tr></thead>
        <tbody>
          %s
        </tbody>
      </table>
    </div>

    <h3 class="sub-head">Alphabetical index</h3>
    <ul class="az-index">
      %s
    </ul>
  </section>

  </main>""" % (MARK_A, "\n          ".join(rows), "\n      ".join(az))


def index_jsonld(films):
    items = []
    for i, f in enumerate(sorted(films, key=lambda x: (-int(x["year"]), x["title"])), 1):
        items.append(
            {
                "@type": "ListItem",
                "position": i,
                "url": "%s/%s" % (BASE, f["slug"]),
                "name": "%s (%s)" % (f["title"], f["year"]),
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Gerard Butler Filmography",
        "description": "Complete list of Gerard Butler feature films with release years, characters and directors.",
        "url": BASE + "/films#film-index",
        "numberOfItems": len(items),
        "itemListElement": items,
    }


def update_films_page(films):
    path = os.path.join(ROOT, "films.html")
    html = open(path, encoding="utf-8").read()

    # replace previous generated block (up to its own closing </section>)
    if MARK_A in html:
        start = html.find(MARK_A)
        end = html.find("</section>", html.find('class="section film-az"', start))
        if end != -1:
            html = html[:start] + html[end + len("</section>"):].lstrip("\n")

    # restore </main> if a previous build swallowed it
    if "</main>" not in html:
        for anchor in ('\n\n  <!-- FOOTER -->', "\n\n<!-- FOOTER -->", "<footer"):
            if anchor in html:
                html = html.replace(anchor, "\n\n  </main>" + anchor, 1)
                break

    if "</main>" not in html:
        print("films.html: no </main>, skipping")
        return
    html = html.replace("</main>", index_section(films).lstrip("\n"), 1)

    ld = (
        '\n  <script type="application/ld+json">\n'
        + json.dumps(index_jsonld(films), indent=2)
        + "\n  </script>\n</head>"
    )
    if '"@type": "ItemList"' not in html:
        html = html.replace("</head>", ld, 1)

    open(path, "w", encoding="utf-8").write(html)
    print("films.html: index rebuilt with %d films" % len(films))


def film_faq(f):
    qas = []
    if f["character"]:
        qas.append(
            (
                "Who does Gerard Butler play in %s?" % f["title"],
                "Gerard Butler plays %s in %s (%s)%s."
                % (
                    f["character"],
                    f["title"],
                    f["year"],
                    ", directed by %s" % f["director"] if f["director"] else "",
                ),
            )
        )
    qas.append(
        (
            "What year did %s come out?" % f["title"],
            "%s was released in %s and features Gerard Butler in the cast."
            % (f["title"], f["year"]),
        )
    )
    if f["director"]:
        qas.append(
            (
                "Who directed %s?" % f["title"],
                "%s was directed by %s and stars Gerard Butler." % (f["title"], f["director"]),
            )
        )
    return qas


def cross_link_block(f, prev_f, next_f, total):
    items = "".join(
        '<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in film_faq(f)
    )
    prev_link = (
        '<a class="film-step" href="%s">&larr; %s (%s)</a>'
        % (prev_f["slug"], prev_f["title"], prev_f["year"])
        if prev_f
        else "<span></span>"
    )
    next_link = (
        '<a class="film-step" href="%s">%s (%s) &rarr;</a>'
        % (next_f["slug"], next_f["title"], next_f["year"])
        if next_f
        else "<span></span>"
    )
    return """
  %s
  <section class="section film-extras">
    <h2 class="display-font">%s — quick answers</h2>
    <div class="faq-list">%s</div>
    <nav class="film-nav-prevnext" aria-label="Filmography navigation">
      %s
      <a class="film-step film-step-all" href="films#film-index">All %d films A&ndash;Z</a>
      %s
    </nav>
  </section>

  </main>""" % (CROSS_MARK, f["title"], items, prev_link, total, next_link)


def update_film_page(f, prev_f, next_f, total):
    path = os.path.join(ROOT, f["file"])
    html = open(path, encoding="utf-8").read()
    if CROSS_MARK in html:
        start = html.find(CROSS_MARK)
        end = html.find("</section>", html.find('class="section film-extras"', start))
        if end != -1:
            html = html[:start] + html[end + len("</section>"):].lstrip("\n")
    # repair pages where an earlier build swallowed the closing </main>
    if "</main>" not in html:
        for anchor in ('\n\n  <!-- FOOTER -->', "\n\n<!-- FOOTER -->"):
            if anchor in html:
                html = html.replace(anchor, "\n\n  </main>" + anchor, 1)
                break
    if "</main>" not in html:
        print("%s: could not restore </main>, skipping" % f["file"])
        return
    html = html.replace("</main>", cross_link_block(f, prev_f, next_f, total).lstrip("\n"), 1)

    ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "%s/%s#faq" % (BASE, f["slug"]),
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in film_faq(f)
        ],
    }
    if "#faq" not in html:
        html = html.replace(
            "</head>",
            '\n  <script type="application/ld+json">\n'
            + json.dumps(ld, indent=2)
            + "\n  </script>\n</head>",
            1,
        )
    open(path, "w", encoding="utf-8").write(html)


def main():
    films = film_list()
    if not films:
        print("no film pages found")
        return
    update_films_page(films)
    by_year = sorted(films, key=lambda x: (int(x["year"]), x["title"]))
    count = 0
    for f in films:
        i = by_year.index(f)
        prev_f = by_year[i - 1] if i > 0 else None
        next_f = by_year[i + 1] if i < len(by_year) - 1 else None
        update_film_page(f, prev_f, next_f, len(films))
        count += 1
    print("%d film pages cross-linked" % count)


if __name__ == "__main__":
    main()
