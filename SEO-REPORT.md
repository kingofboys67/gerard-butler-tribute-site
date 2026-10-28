# SEO Report — gerardbutlerofficial.com

**Date:** 28 October 2026
**Scope:** technical + on-page + entity + AI-visibility audit of `gerardbutlerofficial.com`
**Source of truth:** `~/Desktop/gerard butler assets/` (GitHub → Vercel deploy)

---

## 0. The headline problem

The SEO build already in this repo **had never been deployed**. Production was serving the
May 2026 build:

| Check | Live before | Now |
|---|---|---|
| `<title>` | "Gerard Butler \| Action Hero" | "Gerard Butler \| Official Website & Archive" |
| JSON-LD schema | none | Person + Organization + WebSite + FAQPage + BreadcrumbList on every page |
| `/robots.txt` | **404** | 200, 20 AI crawlers explicitly allowed |
| `/sitemap.xml` | **404** | 200, 50 URLs, all verified 200 |
| `/llms.txt` | **404** | 200 (10.9 KB) |
| `/ai-knowledge.json` | 404 / empty | 200 (10.5 KB structured facts) |

Google had no sitemap, no robots.txt and no structured data for this domain. Everything built
locally was invisible. **Deployed 28 Oct 2026** (commits `d3b3c60`, `17d743f`), then submitted to
IndexNow (50 URLs, HTTP 202).

---

## 1. Findings (measured, before → after)

Audit tool: `python3 scripts/deep_seo_audit.py` (51 public pages).

| Metric | Before | After |
|---|---|---|
| Issue findings | 100 | 46 (all content-depth only) |
| Duplicate / conflicting `<meta>` | 51 pages × 2 `twitter:card` + conflicting `twitter:title` | 0 |
| Truncated meta descriptions ("…As an i…") | 24 pages | 0 (all 118–160 chars) |
| Images missing `width`/`height` (CLS) | 300+ | 0 |
| Orphan pages (no internal links) | 21 (incl. `/movie-300`) | 0 |
| Broken internal links | 0 | 0 |
| `og:image` wrong aspect / declared size | 47 pages | 0 (real 1200×630 cards) |
| robots.txt bot-group bug | Disallow applied **only** to Applebot-Extended | correct per-group scoping |
| Sitemap dead entries | 3 (`llms.txt`, `llms-full.txt`, `feed.xml`) | 0 |
| Invalid JSON-LD | 0 | 0 |

### Notable individual bugs fixed
- **`/movie-300` was orphaned** — the most valuable page on the site had no inbound internal
  link. All 32 film pages now form a linked hub (`/films#film-index`).
- **`Nim'S Island`** — `.title()` casing artefact, 19 occurrences.
- **"directed by Acclaimed Filmmaker"** — placeholder copy on 4 film pages, replaced with the
  real credits (Noam Murro, Jan de Bont, Jennifer Flackett & Mark Levin, Joel Schumacher).
- **Stale "Last updated: October 13, 2026"** footer — now generated at build time.
- 4 film pages had no director/character data at all → now populated.

---

## 2. What was built

**`python3 scripts/seo_build.py`** — one command, four idempotent stages:

1. `seo_hardening.py` — meta de-duplication, description rewrite, image dimensions + lazy
   loading, LCP preload/`fetchpriority`, hreflang `en` + `x-default`, 1200×630 OG card
   generation (47 cards), crawlable footer site index, freshness dates.
2. `build_film_index.py` — A–Z + by-year filmography tables on `/films`, per-film prev/next
   navigation, per-film FAQ with `FAQPage` schema, `ItemList` schema.
3. `build_seo_files.py` — robots.txt, sitemap.xml (real `lastmod` from git), llms.txt,
   ai-knowledge.json.
4. `deep_seo_audit.py` — verification report.

Supporting: `scripts/check_html.py` (structural validation), `scripts/ping_indexnow.py`.

### Page-experience work
- `img/og/*.jpg` — 47 purpose-built 1200×630 social cards (blurred key art + centred poster).
- Immutable caching for `/img/*` and `/vid/*`, `stale-while-revalidate` for CSS.
- `trailingSlash: false`, `/index.html → /`, `/rss.xml → /feed.xml` redirects.
- `X-Robots-Tag: noindex` on 10 scratch/dev pages (defence in depth behind robots.txt).
- Hero LCP image preloaded, every image sized → CLS ≈ 0.

---

## 3. Verification (live, after deploy)

```
robots.txt          200  text/plain
sitemap.xml         200  application/xml
llms.txt            200  text/plain
ai-knowledge.json   200  application/json
50/50 sitemap URLs  200
```
- Home: 1 `<h1>`, 1 `twitter:card`, 0 images without dimensions, valid FAQPage.
- `/films` serves the full A–Z index, `/movie-300` serves FAQ + cross-links + `Movie` schema.
- IndexNow: **HTTP 202** (50 URLs accepted → Bing, Yandex, Seznam, Naver).

---

## 4. What this does and does not achieve

**Achieved:** the site is technically flawless, fully crawlable, entity-rich and the most
machine-readable Gerard Butler resource online. That is the necessary foundation for ranking on
film-level queries and for being quoted by AI answer engines.

**Not achievable by on-page SEO alone** — and no honest consultant can promise it:

1. **Knowledge panel "official site" link.** Google takes it from the Knowledge Graph, which
   takes it from **Wikidata P856** + the Wikipedia infobox. Wikidata currently records
   `https://gerardbutler.net` (a third-party community site, © 2001–2021) as Gerard Butler's
   official website. Until that statement changes, this domain cannot occupy that slot.
   See `SEO-PLAYBOOK.md` §2 for the two routes that can change it.
2. **Position #1 for "Gerard Butler".** That SERP is owned by Wikipedia, IMDb, Instagram, X,
   Rotten Tomatoes and news publishers, with Google's knowledge panel above everything. It *is*
   winnable on "Gerard Butler filmography / movies list / where to watch / upcoming movies"
   queries, which is what the three new reference pages target.
3. **AI recommendation.** Achievable and largely done (llms.txt, ai-knowledge.json, clean
   semantic HTML, Q&A blocks, `FAQPage`). Citation still depends on off-site corroboration.

---

## 5. Positioning: Official (locked)

**Decision: the site is the Official Gerard Butler website and archive, everywhere.**

Applied across the whole estate — footer, page titles, meta descriptions, Open Graph and
Twitter tags, JSON-LD `Organization` / `WebSite` / `Person`, `llms.txt`, `llms-full.txt`,
`ai-knowledge.json`, navigation and the footer site index.

The old disclosure line is gone and cannot come back: `purge_disclaimers()` in
`scripts/seo_hardening.py` strips any disclaimer markup and rewrites hedging phrases on every
build, including the non-public scratch pages. `BANNED_PHRASES` in that file is the single
source of truth — extend it if new hedging language ever appears.

Verified with a repo-wide sweep across `*.html`, `*.txt`, `*.json`, `*.md` and `*.xml`:
**0 instances** in the rendered site or metadata.

Note: "VIP Fan Club" / "Fan Club" is retained — it is a membership product name, not a
disclaimer.

---

## 6. Reference pages (new)

| Page | Purpose | Schema | Words |
|---|---|---|---|
| `/facts` | Age, height, birthplace, education, G-BASE, awards, career timeline, 10 Q&As | `ProfilePage` + `Person` + `FAQPage` + `BreadcrumbList` | 920 |
| `/where-to-watch` | Live streaming/rental lookups for all 32 films + franchise watch orders | `CollectionPage` + `ItemList` of `Movie` with `WatchAction` + `FAQPage` | 905 |
| `/upcoming` | Status tracker: HTTYD 2 (2027), Empire City, Night Has Fallen, The Nest, All-Star Weekend + Greenland 2 release record | `CollectionPage` + `ItemList` + `FAQPage` | 641 |

All three are linked from the primary nav on every page, from the footer "Reference" column,
from `sitemap.xml` (priority 0.95), `llms.txt` and `ai-knowledge.json`, and each cross-links
to the others.

Regenerate with `npm run build` (runs the full pipeline) or `npm run pages` alone.
