# SEO & Entity Playbook — winning Gerard Butler search (and AI answers)

Companion to `SEO-REPORT.md`. That file covers the technical work already shipped.
This one is the plan for the goals that **cannot** be coded: the knowledge panel,
rankings for the bare name, and being the source AI engines recommend.

---

## 1. Reality check on "the official site in the knowledge panel"

Google does not let a website claim a knowledge panel for a living person. For people, the
panel is assembled from the Knowledge Graph, and the "official site" link comes from
**Wikidata P856** and the **Wikipedia infobox "Website" field**.

Measured today (Wikidata Q169982, 21 Sep 2026 revision):

```
P856 (official website) : https://gerardbutler.net      <-- a third-party community site, © 2001-2021
P2003 (Instagram)       : gerardbutler
P2013 (Facebook ID)     : GerardButler
P345  (IMDb)            : nm0124930
P2002 (X/Twitter)       : (none)
```

So the panel's official link is currently occupied by another domain. Yours cannot take that slot by
optimising harder; it takes one of these routes, in order of realism:

| Route | What it requires | Realistic outcome |
|---|---|---|
| **A. Get the P856 statement corrected/removed** | A Wikidata account and a policy-based argument that a third-party community site is not an "official website" (Wikidata: P856 = *"the website of the item's subject"*). Use `Wikidata:Requests for deletions` or the item's talk page. | Achievable, sourced, and often accepted. Removes the competitor's claim — but does **not** hand you the slot. |
| **B. Authorisation from Butler's team** | Written permission (manager/agency: Range Media Partners; publicist). Then: point his real channels at your domain, get the Wikipedia infobox updated with a citation, add Zoho/GSC brand verification. | The only route that ends with *your* domain as "official". Weeks-to-months; entirely relationship-driven. |
| **C. Become the entity's de-facto reference** | Be the site that press, Wikipedia editors and AI models cite for filmography/streaming facts. Your site then appears in the panel's "Profiles"/social area rather than the official link. | Realistic and worth doing — this is §3 and §4. |

**Do not** fake the signal (buy `sameAs` mentions, edit Wikidata to your own domain without
authorisation). That reliably results in reversion, a block, and a site-level trust penalty.

---

## 2. Technical prerequisites already met

- `Person` + `Organization` + `WebSite` + `FAQPage` + `BreadcrumbList` + `Movie` +
  `ImageGallery` + `ItemList` schema — all valid, all with stable `@id`s.
- `sameAs` → Wikipedia, Wikidata, IMDb, Instagram, Facebook, X.
- One canonical host (`www`, apex 308 → www), clean URLs, `hreflang` set, sitemap + robots correct.
- `llms.txt`, `llms-full.txt`, `ai-knowledge.json` for language models.

**Still to do by you (needs your accounts):**

1. **Google Search Console** — verify `gerardbutlerofficial.com` (DNS TXT is safest), submit
   `sitemap.xml`, then use *URL Inspection → Request indexing* on `/`, `/films`, `/about`,
   `/movie-300`, `/movie-greenland`, `/charity`, `/news`.
2. **Bing Webmaster Tools** — import from GSC, submit the same sitemap. Bing powers ChatGPT
   search and Copilot, so this matters as much as Google for your AI goal.
3. **Yandex Webmaster** + **Naver Search Advisor** (IndexNow already covers Seznam/Yandex ping).
4. Optional but cheap: verify the domain in **Cloudflare**/**Pinterest**/**Reddit** so brand
   mentions become linkable entity signals.

---

## 3. Getting recommended by AI engines (GEO — generative engine optimisation)

AI answers are assembled from sources the model already trusts. Page markup gets you *readable*;
corroboration gets you *cited*.

**Already in place:** `llms.txt`, `llms-full.txt`, `ai-knowledge.json`, robots.txt explicitly
allowing GPTBot / OAI-SearchBot / ClaudeBot / PerplexityBot / Google-Extended / Applebot-Extended /
CCBot / Amazonbot, Q&A blocks with `FAQPage`, factual tables, stable URLs.

**The monthly loop that actually moves citations:**

1. **Write one factual, citable page per query cluster.** The ones AI gets asked constantly:
   - "Gerard Butler full filmography in order" → `/films` (built)
   - "Where to watch Gerard Butler movies" → `/films` + per-film "where to watch"
   - "Gerard Butler net worth" / "height" / "wife" / "nationality" → one `/facts` page with
     sourced statements (mark clearly what is reported vs. confirmed)
   - "Is Gerard Butler in Greenland 2?" → film page with release/status
2. **Test the answer, then close the gap.** Ask ChatGPT / Claude / Perplexity / Gemini
   *"What is Gerard Butler's full filmography?"* — note which URLs they cite. If they cite
   Wikipedia/IMDb/Rotten Tomatoes only, the fix is off-site (§4), not more on-page copy.
3. **Publish a date-stamped changelog** (`/news`) so "freshness" signals exist. AI crawlers
   weight recency heavily on living-person facts.
4. **Keep facts identical everywhere** — same birth date, same film titles, same character names
   on site, IMDb-style listings, social bios. Contradiction = no citation.
5. **Make citation easy:** every page has a one-line "Source: gerardbutlerofficial.com" pattern
   in the copy and a stable anchor (`#film-index`, `#faq`).

---

## 4. Off-page: the only thing that gets you to #1

On-page work is now saturated. Rankings for anything competitive move on links/mentions.
Target list, roughly in order of value per hour spent:

| Target | Why | How |
|---|---|---|
| **Reddit** r/movies, r/GerardButler, r/AskMovies | Reddit is disproportionately cited by Google AI Overviews and by LLMs | Answer film questions with genuine value; link only where it directly answers. No link-dropping. |
| **Wikipedia citations** | Highest-trust corroboration; also the panel's source | Add your filmography page as a citation only where it verifies something Wikipedia currently leaves unsourced (film dates, character names). Never add it as an "external link" — that gets removed. |
| **Fan-community crossover** | gerardbutler.net, GB fan forums, Tumblr | Offer a factual data partnership/link exchange; they have 20+ years of authority. |
| **Press/entertainment desks** | Digital Spy, ScreenRant, Collider, ComingSoon, JoBlo | Pitch a data story: "Gerard Butler's 32 films ranked by box office" or "every Mike Banning film in order". Journalists link to data sources. |
| **YouTube/TikTok creators** | Your `vid/` reels are original | Publish clips with descriptions crediting the site; video results + links compound. |
| **Wikidata (cautious)** | Entity graph | Only policy-valid edits with sources (e.g. P2002 X handle if he has one). Never your own domain. |

**Do not:** buy links, use PBNs, run "guest post" mills, or mass-submit to directories. A
A 50-page site with bought links is a manual-action magnet.

---

## 5. Content gaps that are worth more than another 200 words on 32 film pages

Current film pages are ~300 words. That's fine for a film detail page; not fine if you want to
rank for the head terms. Highest-leverage additions, in order:

1. **`/where-to-watch`** — one page, every film, streaming service by region, with
   `StreamingService`/`Offer` data. This is the single biggest commercial query cluster and no
   site owns it well today.
2. **`/facts`** — height, birth date/place, family, education, G-BASE, awards, notable quotes,
   each with a source line. Directly matches how AI answers are phrased.
3. **`/upcoming`** — Greenland 2: Migration, Empire City, Blue Zeus and any announced project,
   with status + dates updated monthly. "Is X coming out" queries are huge and volatile.
4. **Per-era editorial pages** — already exist (`career-early-years`, etc.); expand to 900–1,200
   words each with real analysis. These are the pages that earn links.
5. **Film pages** — add "production notes", "box office", "reception" per film (sourced), not
   more boilerplate FAQ.

---

## 6. 90-day plan

**Week 1** — GSC + Bing verification, sitemap submission, request indexing for the 8 key URLs.
Fix any coverage errors. Set up a rank tracker for 25 queries (film names + "where to watch").

**Weeks 2–4** — ship `/facts`, `/where-to-watch`, `/upcoming`. Internal-link them from home +
footer. Re-run `scripts/seo_build.py` and IndexNow.

**Weeks 5–8** — off-page: 10 Reddit answers, 5 journalist pitches (data story), 3 Wikipedia
citations where sourced, contact gerardbutler.net for a factual cross-link.

**Weeks 9–12** — measure: GSC impressions/clicks per cluster, AI citation checks (ask 5 engines
the same 10 questions monthly), Core Web Vitals field data. Double down on what moved.

**KPIs that matter:** indexed pages (target 50/50), GSC impressions for "gerard butler
filmography" cluster, #1–3 positions on film-level queries, AI citation count per month.
Not: "position 1 for Gerard Butler" — that slot belongs to Wikipedia/IMDb.

---

## 7. Maintenance

```bash
python3 scripts/seo_build.py          # regenerate everything + audit
python3 scripts/check_html.py         # structural check
python3 scripts/ping_indexnow.py      # push changes to Bing/Yandex/Seznam
```

Run after any content change, then commit + push (Vercel deploys automatically).
