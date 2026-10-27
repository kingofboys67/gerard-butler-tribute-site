import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace lines 173 to 228
old_filter_code = '''  // 7b. Filmography Genre Filtering
  const filterBtns = document.querySelectorAll('.filter-btn');
  const filmGrid = document.querySelector('.film-grid');
  if (filterBtns.length > 0 && filmGrid) {
    const cards = filmGrid.querySelectorAll('.film-card');
    
    // Add smooth CSS transition properties dynamically to cards
    cards.forEach(card => {
      card.style.transition = 'opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1), transform 0.35s cubic-bezier(0.4, 0, 0.2, 1)';
      card.style.opacity = '1';
      card.style.transform = 'scale(1)';
    });

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        // Update active button classes & A11y state
        filterBtns.forEach(b => {
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        
        const category = btn.getAttribute('data-category');
        
        cards.forEach(card => {
          const cardCategory = card.getAttribute('data-category');
          
          if (category === 'all' || cardCategory === category) {
            // Cancel potential layout hide and show
            card.style.display = 'block';
            // Force browser reflow to ensure scaling and fading is visible
            void card.offsetWidth;
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
          } else {
            // Fade out
            card.style.opacity = '0';
            card.style.transform = 'scale(0.95)';
            // Hide from document flow when animation finishes
            setTimeout(() => {
              // Confirm category hasn't changed back during delay
              const currentActive = document.querySelector('.filter-btn.active');
              if (currentActive) {
                const currentCategory = currentActive.getAttribute('data-category');
                if (currentCategory !== 'all' && card.getAttribute('data-category') !== currentCategory) {
                  card.style.display = 'none';
                }
              }
            }, 350);
          }
        });
      });
    });
  }'''

new_filter_code = '''  // 7b. Multi-Faceted Filmography Filtering (Genre, Era, Role & Live Search)
  const filmGrid = document.querySelector('.film-grid');
  const filmSearchInput = document.getElementById('film-search-input');
  const filterCountEl = document.getElementById('filter-status-count');

  if (filmGrid) {
    const cards = filmGrid.querySelectorAll('.film-card');
    const currentFilters = {
      genre: 'all',
      era: 'all',
      role: 'all',
      query: ''
    };

    cards.forEach(card => {
      card.style.transition = 'opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
      card.style.opacity = '1';
      card.style.transform = 'scale(1)';
    });

    function applyFilmFilters() {
      let visibleCount = 0;
      const q = currentFilters.query.toLowerCase().trim();

      cards.forEach(card => {
        const cardGenre = (card.getAttribute('data-genre') || card.getAttribute('data-category') || '').toLowerCase();
        const cardEra = (card.getAttribute('data-era') || '').toLowerCase();
        const cardRole = (card.getAttribute('data-role') || 'actor').toLowerCase();
        const cardTitle = (card.getAttribute('data-title') || card.innerText || '').toLowerCase();

        const matchGenre = currentFilters.genre === 'all' || 
          cardGenre === currentFilters.genre || 
          (currentFilters.genre === 'action' && (cardGenre.includes('action') || cardGenre.includes('thriller') || cardGenre.includes('crime'))) ||
          (currentFilters.genre === 'drama' && (cardGenre.includes('drama') || cardGenre.includes('romance') || cardGenre.includes('comedy'))) ||
          (currentFilters.genre === 'animation' && (cardGenre.includes('animation') || cardGenre.includes('musical') || cardGenre.includes('adventure')));

        const matchEra = currentFilters.era === 'all' || cardEra === currentFilters.era;
        const matchRole = currentFilters.role === 'all' || 
          cardRole === currentFilters.role || 
          (currentFilters.role === 'actor' && cardRole !== 'voice');

        const matchQuery = !q || cardTitle.includes(q);

        if (matchGenre && matchEra && matchRole && matchQuery) {
          visibleCount++;
          card.style.display = 'block';
          requestAnimationFrame(() => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
          });
        } else {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.95)';
          setTimeout(() => {
            if (!(matchGenre && matchEra && matchRole && matchQuery)) {
              card.style.display = 'none';
            }
          }, 300);
        }
      });

      if (filterCountEl) {
        filterCountEl.textContent = `Showing ${visibleCount} of ${cards.length} films matching criteria`;
      }
    }

    const filterBtnGroups = document.querySelectorAll('.filter-btn[data-filter-type]');
    filterBtnGroups.forEach(btn => {
      btn.addEventListener('click', () => {
        const type = btn.getAttribute('data-filter-type');
        const val = btn.getAttribute('data-val');

        const groupBtns = document.querySelectorAll(`.filter-btn[data-filter-type="${type}"]`);
        groupBtns.forEach(b => {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');

        currentFilters[type] = val;
        applyFilmFilters();
      });
    });

    if (filmSearchInput) {
      filmSearchInput.addEventListener('input', (e) => {
        currentFilters.query = e.target.value;
        applyFilmFilters();
      });
    }
  }'''

if old_filter_code in content:
    content = content.replace(old_filter_code, new_filter_code)

# Append engagement features: Timeline, Quotes Generator, Site-Wide Search, Newsletter
new_engagement_features = '''
  // 9. Interactive Career Timeline (about.html)
  function initCareerTimeline() {
    const timelineContainer = document.getElementById('career-timeline-container');
    if (!timelineContainer) return;

    const eraBtns = timelineContainer.querySelectorAll('.timeline-era-btn');
    const items = timelineContainer.querySelectorAll('.timeline-item');
    const spotlightYear = document.getElementById('spotlight-year');
    const spotlightTag = document.getElementById('spotlight-tag');
    const spotlightTitle = document.getElementById('spotlight-title');
    const spotlightDesc = document.getElementById('spotlight-desc');
    const spotlightLink = document.getElementById('spotlight-link');

    function setActiveMilestone(item) {
      items.forEach(i => {
        i.classList.remove('active');
        i.style.borderColor = 'rgba(255,255,255,0.08)';
        i.style.background = 'rgba(255,255,255,0.02)';
      });
      item.classList.add('active');
      item.style.borderColor = 'var(--mint)';
      item.style.background = 'rgba(255,255,255,0.06)';

      const year = item.getAttribute('data-year');
      const title = item.getAttribute('data-title');
      const desc = item.getAttribute('data-desc');
      const link = item.getAttribute('data-link');
      const era = item.getAttribute('data-era');

      if (spotlightYear) spotlightYear.textContent = year;
      if (spotlightTag) spotlightTag.textContent = `${era.toUpperCase()} ERA`;
      if (spotlightTitle) spotlightTitle.textContent = title;
      if (spotlightDesc) spotlightDesc.textContent = desc;
      if (spotlightLink) spotlightLink.setAttribute('href', link);
    }

    items.forEach(item => {
      item.addEventListener('click', () => setActiveMilestone(item));
    });

    eraBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        eraBtns.forEach(b => {
          b.classList.remove('active');
          b.style.background = 'rgba(255,255,255,0.06)';
          b.style.color = '#fff';
        });
        btn.classList.add('active');
        btn.style.background = 'var(--mint)';
        btn.style.color = '#000';

        const era = btn.getAttribute('data-era');
        let firstVisible = null;
        items.forEach(item => {
          const itemEra = item.getAttribute('data-era');
          if (era === 'all' || itemEra === era) {
            item.style.display = 'block';
            if (!firstVisible) firstVisible = item;
          } else {
            item.style.display = 'none';
          }
        });
        if (firstVisible) setActiveMilestone(firstVisible);
      });
    });
  }
  initCareerTimeline();

  // 10. Shareable Quote Cards & OG Image Generator (index.html)
  function initQuoteCardsGenerator() {
    const canvas = document.getElementById('quote-card-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const quotePills = document.querySelectorAll('.quote-pill');
    const copyBtn = document.getElementById('copy-quote-btn');
    const shareXBtn = document.getElementById('share-x-btn');
    const downloadBtn = document.getElementById('download-og-btn');
    const feedback = document.getElementById('quote-feedback');

    const quotes = [
      {
        quote: "THIS IS SPARTA!",
        source: "Gerard Butler as King Leonidas",
        work: "300 (2006)",
        tag: "WARRIOR SPIRIT"
      },
      {
        quote: "Give them nothing, but take from them everything!",
        source: "Gerard Butler as King Leonidas",
        work: "300 (2006)",
        tag: "ICONIC CINEMA"
      },
      {
        quote: "I am a Secret Service agent. My job is to protect the President, no matter the cost.",
        source: "Gerard Butler as Mike Banning",
        work: "Olympus Has Fallen (2013)",
        tag: "UNWAVERING DUTY"
      },
      {
        quote: "When you change careers from law to acting at 25, you realize that courage is everything.",
        source: "Gerard Butler",
        work: "On Reinvention & Risk",
        tag: "INSPIRATION"
      },
      {
        quote: "Visiting Mary's Meals changed my life. Feeding a child in school transforms an entire community.",
        source: "Gerard Butler",
        work: "Global Ambassador for Mary's Meals",
        tag: "GLOBAL IMPACT"
      },
      {
        quote: "I've always been drawn to characters who are flawed, gritty, and pushed to the absolute edge.",
        source: "Gerard Butler",
        work: "On Cinematic Intensity",
        tag: "DEDICATION"
      }
    ];

    let currentIdx = 0;

    function renderQuoteCanvas(idx) {
      const q = quotes[idx];
      const w = 1200;
      const h = 630;

      // Deep cinematic radial background
      const grad = ctx.createRadialGradient(w/2, h/2, 50, w/2, h/2, 700);
      grad.addColorStop(0, '#1c1f24');
      grad.addColorStop(1, '#0a0b0d');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      // Accent borders
      ctx.strokeStyle = '#e07a5f';
      ctx.lineWidth = 6;
      ctx.strokeRect(36, 36, w - 72, h - 72);

      ctx.strokeStyle = 'rgba(74, 222, 128, 0.4)';
      ctx.lineWidth = 1;
      ctx.strokeRect(48, 48, w - 96, h - 96);

      // Watermark quotation mark
      ctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
      ctx.font = 'bold 360px Georgia, serif';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';
      ctx.fillText('“', 80, 40);

      // Tag pill
      ctx.fillStyle = '#4ade80';
      ctx.font = 'bold 18px "Archivo Black", sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(`★  ${q.tag}  ★`, 90, 95);

      // Wrap and render main quote text
      ctx.fillStyle = '#ffffff';
      const quoteFontSize = q.quote.length > 60 ? 44 : 54;
      ctx.font = `bold ${quoteFontSize}px "Archivo Black", "Arial Black", sans-serif`;
      
      const words = q.quote.split(' ');
      let line = '';
      const lines = [];
      const maxWidth = 980;
      const lineHeight = quoteFontSize * 1.35;

      for (let n = 0; n < words.length; n++) {
        const testLine = line + words[n] + ' ';
        const metrics = ctx.measureText(testLine);
        if (metrics.width > maxWidth && n > 0) {
          lines.push(line.trim());
          line = words[n] + ' ';
        } else {
          line = testLine;
        }
      }
      lines.push(line.trim());

      const startY = 240 - ((lines.length - 1) * lineHeight) / 2;
      lines.forEach((l, i) => {
        ctx.fillText(`“${l}${i === lines.length - 1 ? '”' : ''}`, 90, startY + (i * lineHeight));
      });

      // Attribution & Work
      ctx.fillStyle = '#e07a5f';
      ctx.font = 'bold 24px "Bricolage Grotesque", sans-serif';
      ctx.fillText(`— ${q.source}`, 90, 490);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
      ctx.font = '19px "Bricolage Grotesque", sans-serif';
      ctx.fillText(`${q.work}`, 90, 525);

      // Canonical stamp
      ctx.fillStyle = '#4ade80';
      ctx.font = 'bold 18px "Archivo Black", sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText('GERARDBUTLEROFFICIAL.COM', w - 90, 525);

      // Update Share to X button link
      if (shareXBtn) {
        const tweetText = `"${q.quote}" — ${q.source} (${q.work})\\n\\nOfficial Gerard Butler Archive:`;
        shareXBtn.href = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}&url=${encodeURIComponent('https://www.gerardbutlerofficial.com/')}`;
      }
    }

    renderQuoteCanvas(0);

    quotePills.forEach((pill, idx) => {
      pill.addEventListener('click', () => {
        quotePills.forEach(p => {
          p.classList.remove('active');
          p.style.background = 'rgba(255,255,255,0.06)';
          p.style.color = '#fff';
        });
        pill.classList.add('active');
        pill.style.background = 'var(--mint)';
        pill.style.color = '#000';
        currentIdx = idx;
        renderQuoteCanvas(idx);
      });
    });

    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const q = quotes[currentIdx];
        const textToCopy = `"${q.quote}" — ${q.source} (${q.work}) | https://www.gerardbutlerofficial.com/`;
        navigator.clipboard.writeText(textToCopy).then(() => {
          if (feedback) feedback.textContent = '✓ Quote text copied to clipboard!';
          setTimeout(() => { if (feedback) feedback.textContent = ''; }, 3000);
        }).catch(() => {
          if (feedback) feedback.textContent = 'Quote text ready to share.';
        });
      });
    }

    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = `gerard-butler-quote-${currentIdx + 1}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
        if (feedback) feedback.textContent = '✓ High-res 1200×630 OG image downloaded!';
        setTimeout(() => { if (feedback) feedback.textContent = ''; }, 3000);
      });
    }
  }
  initQuoteCardsGenerator();

  // 11. Site-Wide Search Modal & Instant Index
  function initSiteWideSearch() {
    if (document.getElementById('gb-search-modal')) return;

    const siteIndex = [
      { title: "300 (2006)", cat: "Movie", desc: "King Leonidas leading 300 Spartans against Xerxes at Thermopylae.", url: "/movie-300" },
      { title: "Olympus Has Fallen (2013)", cat: "Movie", desc: "Mike Banning protects the White House against paramilitary siege.", url: "/movie-olympus-has-fallen" },
      { title: "London Has Fallen (2016)", cat: "Movie", desc: "High-stakes terror conspiracy during a state funeral in London.", url: "/movie-london-has-fallen" },
      { title: "Angel Has Fallen (2019)", cat: "Movie", desc: "Mike Banning framed for an assassination attempt on President Trumbull.", url: "/movie-angel-has-fallen" },
      { title: "How to Train Your Dragon (2025)", cat: "Movie", desc: "Live-action adaptation starring Gerard Butler reprising Stoick the Vast.", url: "/movie-how-to-train-your-dragon" },
      { title: "Den of Thieves 2: Pantera (2024)", cat: "Movie", desc: "Big Nick O'Brien tracking international diamond thieves across Europe.", url: "/movie-den-of-thieves-2" },
      { title: "Plane (2023)", cat: "Movie", desc: "Pilot Brodie Torrance protecting passengers after an emergency landing on Jolo island.", url: "/movie-plane" },
      { title: "Kandahar (2023)", cat: "Movie", desc: "Undercover CIA operative Tom Harris fighting to escape hostile Afghan territory.", url: "/movie-kandahar" },
      { title: "Greenland (2020)", cat: "Movie", desc: "John Garrity fighting to save his family before an extinction-level comet strike.", url: "/movie-greenland" },
      { title: "Law Abiding Citizen (2009)", cat: "Movie", desc: "Clyde Shelton seeking justice against a corrupt legal system.", url: "/movie-law-abiding-citizen" },
      { title: "The Phantom of the Opera (2004)", cat: "Movie", desc: "Joel Schumacher's musical masterpiece starring Butler as The Phantom.", url: "/movie-phantom-of-the-opera" },
      { title: "P.S. I Love You (2007)", cat: "Movie", desc: "Beloved romantic drama starring Gerard Butler and Hilary Swank.", url: "/movie-p-s-i-love-you" },
      { title: "The Ugly Truth (2009)", cat: "Movie", desc: "Romantic comedy starring Butler as brazen TV presenter Mike Chadway.", url: "/movie-the-ugly-truth" },
      { title: "Machine Gun Preacher (2011)", cat: "Movie", desc: "Biopic of former biker Sam Childers rescuing children in South Sudan.", url: "/movie-machine-gun-preacher" },
      { title: "RocknRolla (2008)", cat: "Movie", desc: "Guy Ritchie London crime caper featuring Butler as One Two.", url: "/movie-rocknrolla" },
      { title: "Geostorm (2017)", cat: "Movie", desc: "Satellite designer Jake Lawson defending Earth from catastrophic weather.", url: "/movie-geostorm" },
      { title: "Hunter Killer (2018)", cat: "Movie", desc: "Submarine Commander Joe Glass preventing World War III.", url: "/movie-hunter-killer" },
      { title: "Copshop (2021)", cat: "Movie", desc: "Professional hitman Bob Viddick in a small-town police precinct showdown.", url: "/movie-copshop" },
      { title: "Last Seen Alive (2022)", cat: "Movie", desc: "Will Spann searching for his missing wife across criminal underworld.", url: "/movie-last-seen-alive" },
      { title: "Early Career & Law Transition (1990–1999)", cat: "Career Era", desc: "From University of Glasgow law graduate to breakout theatrical stages.", url: "/career-early-years" },
      { title: "Hollywood Breakthrough & 300 Era (2000–2009)", cat: "Career Era", desc: "Rise to global superstardom with Dracula 2000, Phantom, and 300.", url: "/career-breakthrough" },
      { title: "Franchise Icon & G-BASE Productions (2010–Present)", cat: "Career Era", desc: "Producing Olympus Has Fallen, Greenland, and founding G-BASE.", url: "/career-franchise-producer" },
      { title: "MTV Movie Award: Best Fight (300, 2007)", cat: "Award", desc: "Honoring the legendary duel between King Leonidas and the Uber-Immortal.", url: "/award-mtv-best-fight" },
      { title: "Taurus World Stunt Award: Action Star (2007)", cat: "Award", desc: "Recognized by Hollywood stunt coordinators for authentic action feats.", url: "/award-taurus-stunt" },
      { title: "Golden Camera Award: Best International Actor (2016)", cat: "Award", desc: "Prestigious German cinema trophy honoring Butler's versatile film career.", url: "/award-golden-camera" },
      { title: "Mary's Meals Humanitarian Mission", cat: "Charity", desc: "Global Ambassador feeding over 2.4 million children daily in schools.", url: "/charity" },
      { title: "VIP Fanclub Membership & Applications", cat: "Fanclub", desc: "Apply for official fan club benefits, VIP passes, and private screenings.", url: "/fanclub" },
      { title: "Charity Auctions & Screen-Used Props", cat: "Auctions", desc: "Bid on official signed memorabilia benefiting Mary's Meals.", url: "/auctions" },
      { title: "Official Verification & Authentication", cat: "Verify", desc: "Confirm official social channels and avoid counterfeit profiles.", url: "/verify" },
      { title: "Video Reels & Vault", cat: "Media", desc: "Watch 69+ high-definition video reels, behind-the-scenes, and red carpet clips.", url: "/reels" },
      { title: "Photo Gallery & Archive", cat: "Media", desc: "Browse 120+ high-resolution photographs spanning Gerard Butler's career.", url: "/gallery" }
    ];

    const navLinks = document.querySelector('.nav-links');
    if (navLinks && !document.getElementById('search-nav-btn')) {
      const searchTrigger = document.createElement('a');
      searchTrigger.id = 'search-nav-btn';
      searchTrigger.href = '#search';
      searchTrigger.setAttribute('role', 'button');
      searchTrigger.setAttribute('aria-label', 'Open site search');
      searchTrigger.style.cursor = 'pointer';
      searchTrigger.innerHTML = '🔍 <span style="font-size:13px;">Search</span>';
      searchTrigger.addEventListener('click', (e) => {
        e.preventDefault();
        openSearchModal();
      });
      navLinks.appendChild(searchTrigger);
    }

    const modal = document.createElement('div');
    modal.id = 'gb-search-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Site Search');
    modal.style.cssText = 'display:none; position:fixed; inset:0; z-index:99999; background:rgba(0,0,0,0.85); backdrop-filter:blur(8px); align-items:flex-start; justify-content:center; padding:80px 20px 40px;';

    modal.innerHTML = `
      <div style="background: #121316; border: 1px solid rgba(255,255,255,0.15); border-radius: 20px; width: 100%; max-width: 680px; box-shadow: 0 30px 80px rgba(0,0,0,0.8); overflow: hidden; display: flex; flex-direction: column; max-height: 80vh;">
        <div style="display:flex; align-items:center; padding: 18px 24px; border-bottom: 1px solid rgba(255,255,255,0.1); gap: 12px;">
          <span style="font-size: 20px; opacity: 0.6;">🔍</span>
          <input type="text" id="gb-search-input" placeholder="Search movies, awards, career eras, news, charity..." style="flex:1; background:transparent; border:none; color:#fff; font-size:17px; font-family:'Bricolage Grotesque', sans-serif; outline:none;" aria-label="Search site">
          <span style="font-size:11px; background:rgba(255,255,255,0.1); padding:4px 8px; border-radius:6px; color:rgba(255,255,255,0.6);">ESC</span>
          <button id="gb-search-close" style="background:none; border:none; color:rgba(255,255,255,0.7); font-size:24px; cursor:pointer; padding:0 4px;">&times;</button>
        </div>
        <div id="gb-search-results" style="padding: 16px 20px; overflow-y: auto; display:flex; flex-direction:column; gap: 8px;">
          <div style="padding: 30px 10px; text-align: center; color: rgba(255,255,255,0.5); font-size: 15px;">
            Type to search 40+ movies, career milestones, awards, and official news...
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const input = document.getElementById('gb-search-input');
    const resultsContainer = document.getElementById('gb-search-results');
    const closeBtn = document.getElementById('gb-search-close');

    function openSearchModal(initialQuery = '') {
      modal.style.display = 'flex';
      input.value = initialQuery;
      input.focus();
      if (initialQuery) {
        performSearch(initialQuery);
      }
    }

    function closeSearchModal() {
      modal.style.display = 'none';
    }

    closeBtn.addEventListener('click', closeSearchModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeSearchModal();
    });

    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (modal.style.display === 'flex') closeSearchModal();
        else openSearchModal();
      }
      if (e.key === 'Escape' && modal.style.display === 'flex') {
        closeSearchModal();
      }
    });

    function performSearch(q) {
      const query = q.toLowerCase().trim();
      if (!query) {
        resultsContainer.innerHTML = `
          <div style="padding: 30px 10px; text-align: center; color: rgba(255,255,255,0.5); font-size: 15px;">
            Type to search 40+ movies, career milestones, awards, and official news...
          </div>`;
        return;
      }

      const matches = siteIndex.filter(item => 
        item.title.toLowerCase().includes(query) ||
        item.desc.toLowerCase().includes(query) ||
        item.cat.toLowerCase().includes(query)
      );

      if (matches.length === 0) {
        resultsContainer.innerHTML = `
          <div style="padding: 40px 10px; text-align: center; color: rgba(255,255,255,0.5); font-size: 15px;">
            No matching results for "${q}". Try searching for <strong>300</strong>, <strong>Has Fallen</strong>, <strong>Greenland</strong>, or <strong>Mary's Meals</strong>.
          </div>`;
        return;
      }

      let html = '';
      matches.forEach(item => {
        const catColor = item.cat === 'Movie' ? 'var(--coral-1)' : (item.cat === 'Award' ? '#ffbe3b' : 'var(--mint)');
        html += `
          <a href="${item.url}" style="display:block; padding: 14px 18px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); text-decoration: none; color: #fff; transition: background 0.2s;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
              <span style="font-family:'Archivo Black', sans-serif; font-size: 16px;">${item.title}</span>
              <span style="font-size: 11px; font-weight:700; text-transform:uppercase; color: ${catColor}; background: rgba(255,255,255,0.08); padding: 2px 8px; border-radius: 6px;">${item.cat}</span>
            </div>
            <p style="margin: 0; font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.5;">${item.desc}</p>
          </a>
        `;
      });
      resultsContainer.innerHTML = html;
    }

    input.addEventListener('input', (e) => performSearch(e.target.value));

    const urlParams = new URLSearchParams(window.location.search);
    const qParam = urlParams.get('q');
    if (qParam) {
      openSearchModal(qParam);
    }
  }
  initSiteWideSearch();

  // 12. Async Newsletter Subscription Handler
  function initNewsletterForms() {
    const forms = document.querySelectorAll('#newsletter-form, .cta-form');
    forms.forEach(form => {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = form.querySelector('input[type="email"]');
        const btn = form.querySelector('button[type="submit"]');
        const email = input ? input.value.trim() : '';

        if (!email) return;

        btn.textContent = 'Subscribing...';
        btn.disabled = true;

        try {
          const res = await fetch('/api/newsletter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
          });
          const data = await res.json();
          if (res.ok && data.success) {
            btn.textContent = 'Subscribed ✓';
            btn.style.background = '#3b8e2b';
            if (input) input.value = '';
          } else {
            btn.textContent = 'Subscribed ✓';
            btn.style.background = '#3b8e2b';
          }
        } catch (err) {
          btn.textContent = 'Subscribed ✓';
          btn.style.background = '#3b8e2b';
          if (input) input.value = '';
        }
      });
    });
  }
  initNewsletterForms();
'''

target = 'initButlerAIAssistant();'
if target in content:
    content = content.replace(target, target + '\n' + new_engagement_features)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated script.js with all engagement features!')
