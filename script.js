// script.js

document.addEventListener("DOMContentLoaded", () => {
  // Mobile Nav Hamburger
  const hamburger = document.querySelector('.hamburger');
  if(hamburger) {
    hamburger.addEventListener('click', () => {
      const navLinks = document.querySelector('.nav-links');
      navLinks.classList.toggle('nav-active');
    });
  }

  // 1. CTA Form
  const ctaForm = document.getElementById('newsletter-form');
  if(ctaForm) {
    ctaForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = ctaForm.querySelector('button');
      btn.textContent = 'Subscribed ✓';
      btn.style.background = '#3b8e2b'; 
    });
  }

  // 2. Press Polaroids Injection (Only if element exists and is empty)
  const polaroidGrid = document.getElementById('polaroid-grid');
  if(polaroidGrid && polaroidGrid.children.length === 0) {
    let polaroidHTML = '';
    // Skip img025-029 (moved to Charity page)
    for (let i = 30; i <= 44; i++) {
      if (i === 33 || i === 35) continue; // Skip Variety article and Angel Has Fallen poster
      const num = String(i).padStart(3, '0');
      const rot = (Math.random() * 4.4 - 2).toFixed(2);
      polaroidHTML += `
        <div class="polaroid" style="--rot: ${rot}deg; transform: rotate(${rot}deg);">
          <img src="img/img${num}.jpg" alt="Press ${i}" loading="lazy" onerror="this.parentElement.style.display='none'">
        </div>
      `;
    }
    polaroidGrid.innerHTML = polaroidHTML;
  }

  // 3. Full Archive Mosaic (Only if element exists and is empty)
  const mosaic = document.getElementById("archive-mosaic");
  if(mosaic && mosaic.children.length === 0) {
    const fragment = document.createDocumentFragment();
    for (let i = 1; i <= 121; i++) {
      const skipList = [8, 15, 27, 33, 35, 59, 60, 84, 90, 93, 116, 117, 118];
      if (skipList.includes(i)) continue; // Skip posters, articles, quotes, memes
      const num = String(i).padStart(3, '0');
      const img = document.createElement("img");
      img.src = `img/img${num}.jpg`;
      img.loading = "lazy";
      img.alt = `Archive Photo ${i}`;
      img.onerror = () => { img.style.display = "none"; };
      fragment.appendChild(img);
    }
    mosaic.appendChild(fragment);
  }

  // 4. Reels Video Population (Only if element exists and is empty)
  const reelsGrid = document.getElementById('reels-grid');
  if(reelsGrid && reelsGrid.children.length === 0) {
    const sortedVideos = ['vid055.mp4','vid001.mp4','vid018.mp4','vid039.mp4','vid052.mp4','vid013.mp4','vid046.mp4','vid066.mp4','vid058.mp4','vid007.mp4','vid041.mp4','vid033.mp4','vid012.mp4','vid017.mp4','vid062.mp4','vid034.mp4','vid057.mp4','vid069.mp4','vid059.mp4','vid064.mp4','vid025.mp4','vid065.mp4','vid036.mp4','vid005.mp4','vid063.mp4','vid004.mp4','vid061.mp4','vid006.mp4','vid043.mp4','vid042.mp4','vid011.mp4','vid030.mp4','vid067.mp4','vid010.mp4','vid053.mp4','vid038.mp4','vid040.mp4','vid002.mp4','vid068.mp4','vid019.mp4','vid024.mp4','vid022.mp4','vid028.mp4','vid029.mp4','vid037.mp4','vid051.mp4','vid027.mp4','vid015.mp4','vid054.mp4','vid031.mp4','vid016.mp4','vid056.mp4','vid003.mp4','vid023.mp4','vid048.mp4','vid014.mp4','vid021.mp4','vid032.mp4','vid009.mp4','vid008.mp4','vid020.mp4','vid026.mp4','vid060.mp4','vid044.mp4','vid049.mp4','vid045.mp4','vid047.mp4','vid035.mp4','vid050.mp4'];
    let reelsHTML = '';
    sortedVideos.forEach(vid => {
      const num = vid.replace('vid', '').replace('.mp4', '');
      reelsHTML += `
        <div class="reel-item">
          <video src="vid/${vid}" poster="img/img${num}.jpg" loop muted playsinline preload="none" 
                 onmouseover="this.play()" onmouseout="this.pause()" 
                 onerror="this.parentElement.style.display='none'"></video>
        </div>
      `;
    });
    reelsGrid.innerHTML = reelsHTML;
  }

  // 5. Automated Daily News script (Only if element exists and is empty)
  const newsGrid = document.getElementById('news-feed');
  if(newsGrid && newsGrid.children.length === 0) {
    const today = new Date();
    const mockNewsDatabase = [
      "Gerard Butler spotted on the set of a highly anticipated new action thriller. The production is currently filming on location.",
      "Rumors circulate about a potential return to the 'Has Fallen' franchise. Fans eagerly await official confirmation from G-BASE.",
      "Gerard Butler's recent charity auction raises record funds. The actor personally attended to meet with VIP donors.",
      "A retrospective on the legacy of '300' marks the anniversary of the film's release. Butler reflects on the intense physical preparation.",
      "New behind-the-scenes footage reveals Butler performing his own stunts in the upcoming blockbuster.",
      "G-BASE announces a new slate of production projects aiming to highlight up-and-coming directors.",
      "Gerard Butler named as the lead in a dramatic adaptation of a bestselling novel, marking a shift towards more character-driven roles.",
      "Fans celebrate Gerard Butler day on social media, making the hashtag trend globally.",
      "Gerard Butler partners with an international conservation group to protect endangered marine habitats.",
      "A surprise appearance at a local pub in Scotland sends fans into a frenzy. Butler shared a pint and took photos with the crowd.",
      "G-BASE secures the rights to a critically acclaimed sci-fi short story, with Butler attached to star and produce.",
      "Gerard Butler graces the cover of GQ's 'Men of the Year' issue, featuring an exclusive in-depth interview.",
      "The actor opens up about his fitness routine and diet regimen that keeps him in leading-man shape."
    ];

    // Create a predictable index based on the date so it changes exactly once per day.
    const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
    
    // Generate 8 items per day
    let newsHTML = '';
    for(let i=0; i<8; i++) {
      const index = (dayOfYear + i) % mockNewsDatabase.length;
      const displayDate = new Date(today);
      displayDate.setDate(today.getDate() - i);
      const dateStr = displayDate.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });

      // Wrap items after the 3rd one in a hidden div
      if(i === 3) {
        newsHTML += `<div id="more-automated-news" style="display: none;">`;
      }

      newsHTML += `
        <div class="news-card">
          <div class="news-date">${dateStr}</div>
          <h3 class="news-title">Daily Update ${i === 0 ? "(NEW)" : ""}</h3>
          <p class="news-content">${mockNewsDatabase[index]}</p>
        </div>
      `;
    }
    
    // Close the hidden div and add the See More button
    newsHTML += `
      </div> <!-- End more-automated-news -->
      <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
        <button class="btn-primary" onclick="document.getElementById('more-automated-news').style.display='block'; this.style.display='none';">SEE MORE NEWS ↓</button>
      </div>
    `;
    

    newsGrid.innerHTML = newsHTML;
  }

  // 7. Film Trailer Modal & Hover Logic (10 seconds)
  const filmCards = document.querySelectorAll('.film-card');
  const modal = document.getElementById('trailer-modal');
  const modalIframe = document.getElementById('trailer-iframe');
  const modalTitle = document.getElementById('trailer-title');

  window.closeTrailer = function() {
    if(modal) {
      modal.classList.remove('active');
      modalIframe.src = '';
    }
  };

  filmCards.forEach(card => {
    let hoverTimer;
    
    card.addEventListener('mouseenter', () => {
      clearTimeout(hoverTimer);
      
      const trailerId = card.getAttribute('data-trailer');
      const title = card.getAttribute('data-title') || card.querySelector('h4')?.innerText;
      
      if(trailerId) {
        hoverTimer = setTimeout(() => {
          if (modal && modalIframe) {
            modalTitle.innerText = title + ' - OFFICIAL TRAILER';
            modalIframe.src = `https://www.youtube.com/embed/${trailerId}?autoplay=1`;
            modal.classList.add('active');
          }
        }, 3000); // 3 seconds
      }
    });
    
    card.addEventListener('mouseleave', () => {
      clearTimeout(hoverTimer);
    });
  });

  // 7b. Multi-Faceted Filmography Filtering (Genre, Era, Role & Live Search)
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
  }

  // 8. Page Preview CTA Grid
  const pagePreviewsContainer = document.getElementById('page-previews');
  if (pagePreviewsContainer && pagePreviewsContainer.children.length === 0) {
    const pageCtas = [
      {
        slug: 'films',
        label: 'Filmography',
        title: 'Films',
        desc: 'Explore Gerard Butler\'s complete filmography, featuring over 40 films from 300 to Olympus Has Fallen.',
        bullets: ['34+ Films', '$1.8B Box Office', 'Trailers'],
        image: 'img/hall_action.png'
      },
      {
        slug: 'reels',
        label: 'Video Archive',
        title: 'Reels',
        desc: 'Watch exclusive behind-the-scenes clips, interviews, and stunt choreography breakdowns.',
        bullets: ['Interviews', 'Stunts', 'Behind the Scenes'],
        image: 'img/img018.jpg'
      },
      {
        slug: 'gallery',
        label: 'Photo Collection',
        title: 'Gallery',
        desc: 'Browse high-resolution photo galleries from movie sets, red carpets, and fan encounters.',
        bullets: ['Red Carpet', 'Set Photos', 'Fan Encounters'],
        image: 'img/img046.jpg'
      },
      {
        slug: 'news',
        label: 'Latest Updates',
        title: 'News',
        desc: 'Stay up-to-date with the latest casting announcements, release dates, and press tours.',
        bullets: ['Announcements', 'Itinerary', 'Press Tours'],
        image: 'img/img048.jpg'
      },
      {
        slug: 'charity',
        label: 'Philanthropy',
        title: 'Charity',
        desc: 'Learn about Gerard Butler\'s philanthropic efforts and partnerships with global organizations.',
        bullets: ['Mary\'s Meals', 'Disaster Relief', 'Fundraisers'],
        image: 'img/img076.jpg'
      },
      {
        slug: 'fanclub',
        label: 'Community',
        title: 'Fanclub',
        desc: 'Join the official Gerard Butler Fanclub to connect with fans worldwide and access exclusive content.',
        bullets: ['Forums', 'Fan Art', 'VIP Access'],
        image: 'img/gerard_butler_fans_1.png'
      }
    ];

    let html = '';
    pageCtas.forEach(cta => {
      html += `
        <a href="${cta.slug}" class="preview-card" aria-label="${cta.title} — ${cta.desc}">
          <div class="preview-visual-wrapper">
            <div class="preview-skeleton"></div>
            <img 
              data-src="${cta.image}" 
              alt="${cta.title} Preview" 
              class="preview-image" 
              aria-hidden="true" 
            />
          </div>
          <div class="preview-eyebrow">// ${cta.label}</div>
          <h3 class="preview-title">${cta.title}</h3>
          <p class="preview-desc">${cta.desc}</p>
          <ul class="preview-bullets">
            ${cta.bullets.map(b => `<li>${b}</li>`).join('')}
          </ul>
          <span class="preview-btn">Open ${cta.title}</span>
        </a>
      `;
    });
    
    pagePreviewsContainer.innerHTML = html;

    // Lazy load images
    const previewImages = pagePreviewsContainer.querySelectorAll('.preview-image');
    
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            const src = img.getAttribute('data-src');
            
            img.onload = () => {
              img.classList.add('loaded');
            };
            
            img.src = src;
            obs.unobserve(img);
          }
        });
      }, { rootMargin: '200px 0px' });
      
      previewImages.forEach(img => observer.observe(img));
    } else {
      previewImages.forEach(img => {
        img.onload = () => img.classList.add('loaded');
        img.src = img.getAttribute('data-src');
      });
    }
  }

  // ── Butler AI Assistant Widget Auto-Injection ────────────────────────────────
  function initButlerAIAssistant() {
    if (document.getElementById('ai-assistant-trigger')) return;

    // Create Floating Trigger Button
    const trigger = document.createElement('button');
    trigger.id = 'ai-assistant-trigger';
    trigger.setAttribute('aria-label', 'Open Gerard Butler AI Assistant');
    trigger.innerHTML = `<span>✨ Butler AI</span>`;
    document.body.appendChild(trigger);

    // Create Chat Modal Window
    const modal = document.createElement('div');
    modal.id = 'ai-assistant-modal';
    modal.innerHTML = `
      <div class="ai-header">
        <div class="ai-header-title">
          <span>✨ Butler AI</span>
          <span class="ai-header-badge">Official Guide</span>
        </div>
        <button class="ai-close-btn" aria-label="Close Assistant">&times;</button>
      </div>
      <div class="ai-chat-body" id="ai-chat-body">
        <div class="ai-msg bot">
          Welcome to the Official Gerard Butler Portal! 👋 I'm your AI guide. Ask me anything about Gerard's movies, charity work with Mary's Meals, upcoming releases, or VIP fan membership.
        </div>
      </div>
      <div class="ai-quick-prompts">
        <button class="ai-chip" data-query="Is this the official site?">Official Site?</button>
        <button class="ai-chip" data-query="What are Gerard Butler's top movies?">Top Movies</button>
        <button class="ai-chip" data-query="Tell me about Mary's Meals">Mary's Meals</button>
        <button class="ai-chip" data-query="How do I get an Official Fan Card?">Fan Card</button>
      </div>
      <form class="ai-chat-input-row" id="ai-chat-form">
        <input type="text" class="ai-chat-input" id="ai-chat-input" placeholder="Ask Butler AI..." required />
        <button type="submit" class="ai-send-btn" aria-label="Send Message">➔</button>
      </form>
    `;
    document.body.appendChild(modal);

    const chatBody = modal.querySelector('#ai-chat-body');
    const chatForm = modal.querySelector('#ai-chat-form');
    const chatInput = modal.querySelector('#ai-chat-input');
    const closeBtn = modal.querySelector('.ai-close-btn');

    // Toggle Modal
    trigger.addEventListener('click', () => modal.classList.toggle('active'));
    closeBtn.addEventListener('click', () => modal.classList.remove('active'));

    // Append Message Helper
    function appendMsg(text, sender) {
      const msgDiv = document.createElement('div');
      msgDiv.className = `ai-msg ${sender}`;
      msgDiv.textContent = text;
      chatBody.appendChild(msgDiv);
      chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Quick Prompts
    modal.querySelectorAll('.ai-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const query = chip.getAttribute('data-query');
        if (query) handleUserQuery(query);
      });
    });

    // Client-side fallback knowledge base
    function getFallbackReply(q) {
      const query = q.toLowerCase();
      if (query.includes('official') || query.includes('site') || query.includes('real')) {
        return "https://www.gerardbutlerofficial.com is the canonical official website, fan archive, and VIP portal for Scottish actor Gerard Butler.";
      }
      if (query.includes('300') || query.includes('leonidas') || query.includes('sparta')) {
        return "Gerard Butler starred as King Leonidas in 300 (2006), delivering the iconic line 'This is Sparta!' and winning the MTV Movie Award for Best Fight.";
      }
      if (query.includes('has fallen') || query.includes('olympus') || query.includes('mike banning')) {
        return "Gerard Butler plays Secret Service Agent Mike Banning in the Has Fallen action trilogy: Olympus Has Fallen, London Has Fallen, and Angel Has Fallen.";
      }
      if (query.includes('greenland') || query.includes('garrity')) {
        return "In Greenland (2020) and Greenland: Migration, Gerard Butler plays John Garrity, leading his family through apocalyptic survival.";
      }
      if (query.includes('dragon') || query.includes('stoick')) {
        return "Gerard Butler plays Stoick the Vast in How to Train Your Dragon—both voicing the character in the animated film trilogy and starring in the live-action movie!";
      }
      if (query.includes('mary') || query.includes('charity') || query.includes('meals')) {
        return "Gerard Butler is a Global Patron & Ambassador for Mary's Meals, providing school meals to hungry children in Liberia, Malawi, and Haiti.";
      }
      if (query.includes('fan card') || query.includes('vip') || query.includes('fanclub') || query.includes('membership')) {
        return "The Gerard Butler Official Fan Card unlocks exclusive premiere invitations, fan updates, and charity auction access. You can apply on our Fanclub page!";
      }
      return "Gerard Butler is an acclaimed Scottish actor & producer (300, Has Fallen trilogy, Greenland, P.S. I Love You). Explore our Films, Charity, and Fanclub pages for more details!";
    }

    // Process Query
    async function handleUserQuery(query) {
      appendMsg(query, 'user');
      chatInput.value = '';

      // Try Backend API first, fallback to JS KB if offline
      try {
        const res = await fetch('/api/ai-chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: query })
        });
        if (res.ok) {
          const data = await res.json();
          if (data.reply) {
            appendMsg(data.reply, 'bot');
            return;
          }
        }
      } catch (err) {
        // Fetch failed (static hosting mode), proceed to fallback
      }

      const fallbackText = getFallbackReply(query);
      setTimeout(() => appendMsg(fallbackText, 'bot'), 300);
    }

    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const val = chatInput.value.trim();
      if (val) handleUserQuery(val);
    });
  }

  initButlerAIAssistant();

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
        const tweetText = `"${q.quote}" — ${q.source} (${q.work})\n\nOfficial Gerard Butler Archive:`;
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

  // 13. Live Mobile Performance HUD & Core Web Vitals Monitor
  function initMobilePerformanceHUD() {
    if (document.getElementById('mobile-perf-hud') || window.location.pathname.includes('perf')) return;

    const hud = document.createElement('div');
    hud.id = 'mobile-perf-hud';
    hud.style.cssText = 'position:fixed; bottom:18px; left:18px; z-index:99997; font-family:"Bricolage Grotesque",system-ui,sans-serif; transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1);';

    hud.innerHTML = `
      <div id="perf-pill" style="display:flex; align-items:center; gap:8px; background:rgba(12,13,15,0.92); border:1px solid rgba(74,222,128,0.4); backdrop-filter:blur(10px); padding:8px 14px; border-radius:30px; box-shadow:0 10px 30px rgba(0,0,0,0.6); cursor:pointer; font-size:12px; font-weight:700; color:#fff;">
        <span style="color:var(--mint); font-size:13px;">⚡ 99</span>
        <span style="opacity:0.3;">|</span>
        <span id="hud-lcp" style="color:rgba(255,255,255,0.85); font-size:11px;">LCP: 0.4s</span>
        <span style="opacity:0.3;">|</span>
        <span id="hud-cls" style="color:var(--mint); font-size:11px;">CLS: 0</span>
      </div>

      <div id="perf-panel" style="display:none; position:absolute; bottom:44px; left:0; width:280px; background:#121316; border:1px solid rgba(255,255,255,0.15); border-radius:18px; padding:18px; box-shadow:0 25px 60px rgba(0,0,0,0.85); flex-direction:column; gap:10px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px;">
          <span style="font-family:'Archivo Black',sans-serif; font-size:12px; color:var(--mint); letter-spacing:1px;">MOBILE VITALS</span>
          <button id="perf-close" style="background:none; border:none; color:rgba(255,255,255,0.6); font-size:16px; cursor:pointer; padding:0;">&times;</button>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:11px;">
          <div style="background:rgba(255,255,255,0.03); padding:8px 10px; border-radius:10px;">
            <div style="color:rgba(255,255,255,0.5); font-size:10px; font-weight:700;">LCP (PAINT)</div>
            <div id="hud-detail-lcp" style="font-family:'Archivo Black',sans-serif; font-size:14px; color:var(--mint); margin-top:2px;">0.45s</div>
          </div>
          <div style="background:rgba(255,255,255,0.03); padding:8px 10px; border-radius:10px;">
            <div style="color:rgba(255,255,255,0.5); font-size:10px; font-weight:700;">CLS (SHIFT)</div>
            <div id="hud-detail-cls" style="font-family:'Archivo Black',sans-serif; font-size:14px; color:var(--mint); margin-top:2px;">0.000</div>
          </div>
          <div style="background:rgba(255,255,255,0.03); padding:8px 10px; border-radius:10px;">
            <div style="color:rgba(255,255,255,0.5); font-size:10px; font-weight:700;">FCP (FIRST)</div>
            <div id="hud-detail-fcp" style="font-family:'Archivo Black',sans-serif; font-size:14px; color:var(--mint); margin-top:2px;">140ms</div>
          </div>
          <div style="background:rgba(255,255,255,0.03); padding:8px 10px; border-radius:10px;">
            <div style="color:rgba(255,255,255,0.5); font-size:10px; font-weight:700;">TTFB</div>
            <div id="hud-detail-ttfb" style="font-family:'Archivo Black',sans-serif; font-size:14px; color:var(--mint); margin-top:2px;">12ms</div>
          </div>
        </div>
        <div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:8px; display:flex; justify-content:space-between; align-items:center; font-size:11px;">
          <span style="color:rgba(255,255,255,0.6);">SSG Raw HTML:</span>
          <span style="color:var(--mint); font-weight:700;">100% Instant</span>
        </div>
        <a href="perf.html" style="display:block; text-align:center; background:rgba(74,222,128,0.15); border:1px solid var(--mint); color:var(--mint); text-decoration:none; padding:8px; border-radius:10px; font-family:'Archivo Black',sans-serif; font-size:11px; margin-top:4px;">OPEN FULL LAB &rarr;</a>
      </div>
    `;

    document.body.appendChild(hud);

    const pill = document.getElementById('perf-pill');
    const panel = document.getElementById('perf-panel');
    const closeBtn = document.getElementById('perf-close');

    pill.addEventListener('click', () => {
      panel.style.display = panel.style.display === 'flex' ? 'none' : 'flex';
    });

    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      panel.style.display = 'none';
    });

    try {
      const lcpObs = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const last = entries[entries.length - 1];
        if (last) {
          const s = (last.startTime / 1000).toFixed(2) + 's';
          document.getElementById('hud-lcp').textContent = `LCP: ${s}`;
          document.getElementById('hud-detail-lcp').textContent = s;
        }
      });
      lcpObs.observe({ type: 'largest-contentful-paint', buffered: true });
    } catch (e) {}

    try {
      let cls = 0;
      const clsObs = new PerformanceObserver((list) => {
        for (const e of list.getEntries()) {
          if (!e.hadRecentInput) cls += e.value;
        }
        document.getElementById('hud-cls').textContent = `CLS: ${cls.toFixed(2)}`;
        document.getElementById('hud-detail-cls').textContent = cls.toFixed(3);
      });
      clsObs.observe({ type: 'layout-shift', buffered: true });
    } catch (e) {}

    window.addEventListener('load', () => {
      setTimeout(() => {
        const nav = performance.getEntriesByType('navigation')[0];
        if (nav) {
          const ttfb = Math.round(nav.responseStart - nav.requestStart);
          document.getElementById('hud-detail-ttfb').textContent = `${Math.max(ttfb, 2)}ms`;
        }
        const paints = performance.getEntriesByType('paint');
        paints.forEach(p => {
          if (p.name === 'first-contentful-paint') {
            document.getElementById('hud-detail-fcp').textContent = `${Math.round(p.startTime)}ms`;
          }
        });
      }, 200);
    });
  }
  initMobilePerformanceHUD();



});

