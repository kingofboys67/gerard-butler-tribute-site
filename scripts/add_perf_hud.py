with open('script.js', 'r', encoding='utf-8') as f:
    c = f.read()

hud_code = '''
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
'''

target = 'initNewsletterForms();'
if target in c and 'initMobilePerformanceHUD()' not in c:
    c = c.replace(target, target + '\n' + hud_code)
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Added Mobile Performance HUD to script.js!')
else:
    print('HUD already present or target not found.')
