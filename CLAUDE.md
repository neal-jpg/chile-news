# Chile Morning — Project Instructions

## What this project does

Every morning, crawl a set of Chilean news websites and produce a single-page HTML briefing for Neal — an American living in Santiago. As of 2026-07, the briefing is a **three-tab app**: **News**, **Events**, and **Music**. It is styled to feel like a sister app to Neal's **Chile Property Tracker** (same dark/light design system, pill tabs, cards, blue accent) — the two may be merged one day, so keep the look consistent.

Everything is explained in terms that make sense to someone who knows US politics/culture but not Chilean.

## Output format

- **Language:** English only (proper nouns, song/album/column titles may stay in Spanish).
- **Length:** One tight page **per tab**. No padding.
- **Format:** Self-contained HTML file — single file, no external dependencies except image URLs and hyperlinks. **Do not load Google Fonts** — the design uses the system font stack, which keeps the file fully self-contained.
- **Filename:** `digest_YYMMDD.html` (e.g. `digest_260706.html`).
- **Save to:** this project folder.

## Landing page (index.html) and archive

Served via GitHub Pages, which loads `index.html` at the root URL. After creating each morning's digest, run `python3 generate_index.py` in this folder. It produces:

- **`index.html`** — a verbatim copy of the newest `digest_YYMMDD.html`, with a small "↗ Browse the archive" link injected after `</header>`. This is the stable bookmark (`https://neal-jpg.github.io/chile-news/`).
- **`archive.html`** — a newest-first list of every edition (theme-aware, matches the app shell).

The dated `digest_*.html` files are the permanent archive and are never modified by the script. Do not hand-edit `index.html` or `archive.html`. The script extracts each edition's archive title from the News tab's `<h2 class="lead-headline">`, so **always keep that class on the lead headline.**

## Design system (sister app to the Property Tracker)

Think clean mobile app, **not** a newspaper. Key properties:

- **Theme-aware light/dark** via CSS custom properties + `@media (prefers-color-scheme: dark)`. Never hard-code colors in markup — use the variables.
- **System font stack**, no web fonts.
- **Narrow single column**, `max-width: 520px`, centered.
- **Pill tabs** at the top for the three sections (`.tab` / `.tab--on`).
- **Cards** with `0.5px` borders, 12px radius, `var(--surface-2)` background.
- **Blue accent** (`--accent-text`), not the old gold.
- Editorial hierarchy is preserved inside cards: label → headline → short summary → source links. The lead News story is a larger hero card.

Emit the canonical CSS block (see **Canonical snippets**) verbatim so every run is visually identical.

## Tab structure

Three tabs, News shown by default (so it still works if JS fails). Emit this shell (see snippets for the switcher script):

```html
<header class="head">
  <span class="head__logo">◈</span>
  <span class="head__name">Chile Morning</span>
  <span class="head__date">DAY<br>Month D, YYYY · Santiago</span>
</header>
<nav class="tabs">
  <button class="tab tab--on" data-tab="news">News</button>
  <button class="tab" data-tab="events">Events</button>
  <button class="tab" data-tab="music">Music</button>
</nav>
<main>
  <section class="panel panel--on" data-panel="news"> … </section>
  <section class="panel" data-panel="events"> … </section>
  <section class="panel" data-panel="music"> … </section>
</main>
```

---

## TAB 1 — News

The News tab holds what this project has always produced. Section order inside the tab:

### Weather (top of News tab)
Santiago forecast for today: high/low in °C **and** °F, one-line condition, a **Las Condes air-quality chip**, and a longer practical note (auto-collapsed to its first sentence). Source: `https://wttr.in/Santiago?format=j1` (fetch may be proxy-blocked — fall back to a web search for "Santiago weather forecast [date]"). Markup:

```html
<div class="weather weather-body">
  <div class="weather__place">Santiago · Winter</div>
  <div class="weather__temps">5° → 18°C  /  41° → 64°F</div>
  <div class="weather__cond">One-line condition.</div>
  <div class="aqi-chip aqi-{band}">Las Condes air · {AQI} {category}</div>
  <p class="weather__note">Longer practical paragraph…</p>
</div>
```

Air quality — fetch current AQI for the **Las Condes** station (waqi.info primary, SINCA `sinca.mma.gob.cl` fallback, US AQI scale). If Las Condes is unavailable use the nearest eastern-Santiago station and relabel the chip; if no reading, omit the chip. US AQI band → class · category: 0–50 `aqi-good` · good; 51–100 `aqi-moderate` · moderate; 101–150 `aqi-sensitive` · unhealthy for sensitive groups; 151–200 `aqi-unhealthy` · unhealthy; 201–300 `aqi-very-unhealthy` · very unhealthy; 301+ `aqi-hazardous` · hazardous.

### Top Headlines (3–5 stories)
Most important Chilean news of the day. Lead story uses `.lead-story` / `.lead-headline`; the rest use `.story-card` / `.card-headline`. Each: a `.label` (topic), headline, 2–3 sentence summary in `.story-body`, source links, and a `.context-link` when background is needed. Pull a lead image where available (`<img class="card-img" alt="…">` at the top of the card).

### Interesting / Offbeat (1–2 items)
`.offbeat-card` with `.offbeat-headline` / `.offbeat-body`. Surprising, human, cultural. Not hard news.

### Opinion / Editorial (1–2 items)
`.opinion-card` with `.opinion-headline` / `.opinion-outlet` / `.opinion-body`. Summarize the argument in 2–3 sentences; name the outlet, author, and lean. **Aim for one left- and one right-leaning piece** (best-effort — say so plainly if one side has nothing notable). Prefer free columnists (The Clinic / El Mostrador / El Desconcierto on the left; El Líbero / Ex-Ante / La Tercera free columns on the right).

### News framing
Neal knows US political concepts. Use them as reference points ("Chile's Senate, like the US Senate…"; "think Bernie Sanders–style…"; "roughly a US Supreme Court ruling overturned by Congress"). Don't over-explain.

### News sources
- https://www.emol.com/ — center-right legacy paper
- https://www.latercera.com/ — center-right daily
- https://www.biobiochile.cl/ — center, strong national coverage
- https://www.theclinic.cl/ — left-leaning, satirical (try `/noticias/politica/` or `/lo-ultimo/` if homepage fails)
- https://www.df.cl/ — business/financial

Fetch homepages + section pages (política, nacional, economía, cultura). **Skip sports entirely.** Prefer the last 24 hours. NOTE: direct fetches are frequently proxy-blocked (403) — use **WebSearch** with dated queries as the reliable path, then link the real article URLs.

### What to leave out of News
Sports (entirely), PR wire/sponsored content, celebrity gossip without national relevance. No market/financial ticker.

---

## TAB 2 — Events

Forward-looking "what's on around Santiago," **today → ~2 weeks out**, deduped day to day. Each item: a `.tags` row, `.event-headline`, a 2–3 sentence `.event-body` (what/where/when + one line on why it's worth it), and source links. Use `.event-card` / `.event-body-wrap`.

### Interests (tag each item)
- **Kids** — *top priority.* Tag with `<span class="tag tag--kids">Kids</span>` so it stands out.
- Coffee, Outdoors, Cinema (special screenings / cycles, not the multiplex), Food, Beer/Wine — tag with `<span class="tag tag--int">🏷 Label</span>` (use a fitting emoji).

### Selection rules
- Forward-looking only; drop events that have already happened.
- Exclude nightlife/DJ club events, sports, and pure commercial promos.
- **Best-effort & honest:** if a category (e.g. beer/wine) has nothing on this fortnight, say so in a `.note` line rather than padding. It's fine for a slow week to lean on genuine ongoing/seasonal attractions.
- Lead each Events tab with a `.banner` one-liner setting context (e.g. school-holiday status).

### Event sources (via WebSearch — direct fetch usually blocked)
- Papers' culture/agenda desks: La Tercera *Finde/Culto*, Emol *Tendencias*, BioBioChile *Artes y Cultura*, The Clinic, El Desconcierto *Tendencias*.
- Listings/venues: GAM (gam.cl), Centro Cultural La Moneda / Cineteca Nacional (cclm.cl), Centro Arte Alameda, MIM (Museo Interactivo Mirador), Teleférico/Parquemet, municipal cultural agendas (Providencia, Las Condes, Santiago, Ñuñoa).
- Food/beer/coffee/wine festivals when in season (e.g. Ñam, Bierfest, Expo Café, Vendimia) — verify dates are upcoming, not past.
- Don't limit yourself to these if you find something well-known and worthwhile.

---

## TAB 3 — Music

Deepen Neal's connection to the **Chilean music scene**. Focus on **album/EP/single releases, charts, interviews, reissues, awards, and scene news** — **NOT live shows** (he has no time for gigs right now). Windowed to "recent & notable (last ~2 weeks)." Each item: a `.tags` genre row, `.music-headline` (Artist — *Title*), a 2–3 sentence `.music-body` (what it is, why notable, "for fans of…"), and source links. Use `.music-card` / `.music-body-wrap`. Cover art image optional (`<img class="card-img">`).

### Genres (tag each item with `<span class="tag tag--genre">Genre</span>`)
Rock, Indie, Dreampop, Hip Hop, Electronic (composition/producers — **not DJ sets**), Metal (heavy & thrash — **not death metal**), Jazz, Blues, Folk/Folklórico, Classical.

### Selection rules
- Prioritize Chilean (or Chile-relevant) artists across the genres above.
- **Reggaeton/urbano is mostly not Neal's vibe** — cover it only briefly, as a one-item chart-context snapshot (tag `tag--int` "📊 Charts"), noting the releases you feature sit outside the mainstream chart.
- No live-show listings. If a "quiet fortnight," feature fewer items honestly rather than padding — but there is almost always at least a release or interview worth surfacing.
- Aim for genre spread across the tab.

### Music sources (via WebSearch — direct fetch usually blocked)
Most important: **MusicaPopular.cl, Rockaxis, POTQ Magazine, Soloartistaschilenas.cl, Disonantes.cl**, and **Bandcamp (Chile)** for digging. Also useful: Super 45, El Mostrador *Jengibre*, La Tercera *Culto*, Spotify/kworb Chile charts for the snapshot. Don't limit yourself to these.

---

## Context pages (News)

When a News story needs background longer than two sentences, create a separate context page instead of linking to Wikipedia:

- **Filename:** `context_YYMMDD_slug.html` in this folder.
- **Format:** self-contained single HTML file, same design system as the digest, with a "Context" label. 200–400 words. Plain English framed for an American reader.
- **Structure:** brief definition → how it works in Chile → American analogy → why it matters today.
- Optional "Read more" external link at the bottom, but the page must stand alone.
- The `.context-link` in the digest points to this local file, never to Wikipedia directly.
- **Reuse:** if a context page for the same concept already exists (check `context_*.html`), link to it instead of creating a duplicate.

## Source links (all tabs)

Every item — News, Events, Music — gets a "Read more →" link to the original URL inside `.story-links`, styled small/understated. Link text is the outlet name (e.g. "Read more → La Tercera"). `target="_blank"` marks it as an external source (the share script relies on this).

## Paywalled links

Treat as paywalled: **El Mercurio** (elmercurio.com), **Diario Financiero** (df.cl) premium, **La Tercera Premium**. Maintain this list. When emitting a paywalled link, append inside the anchor: `Read more → {Outlet} <span class="paywall-tag">🔒 paywall</span>`. If a free outlet also covers the story, list the free link first. Never attempt to bypass a paywall — only the public preview.

## Share buttons

Every item gets a "Share" control (native share sheet + clipboard fallback). **Do not hand-add them** — the canonical share script injects one into every `.story-links`. Just include the script and the `.share-btn`/`.toast` CSS (both in the canonical block).

## Notes

- Images need `alt` text; the file must open cleanly in any browser with no broken dependencies.
- This digest runs every morning (automated). Compute the date in America/Santiago time.

---

## Canonical snippets — emit verbatim in every digest

Include all four blocks unchanged so every run produces identical, working code.

**1) CSS** — the entire `<style>` block:

```css
:root {
  --surface-0: #f7f6f2; --surface-1: #efeee8; --surface-2: #ffffff;
  --text-primary: #20201e; --text-secondary: #5f5e5a; --text-muted: #8a8880;
  --border: #e2e0d8;
  --accent-bg: #e6f1fb; --accent-text: #185fa5; --accent-border: #85b7eb;
  --success-bg: #eaf3de; --success-text: #3b6d11;
  --warning-bg: #faeeda; --warning-text: #854f0b;
  --danger-bg: #f8dada; --danger-text: #9a2b2b;
  --gray-bg: #f1efe8;
  --line: #378add;
}
@media (prefers-color-scheme: dark) {
  :root {
    --surface-0: #1a1a19; --surface-1: #242422; --surface-2: #2f2f2c;
    --text-primary: #f2f1ec; --text-secondary: #b4b2a9; --text-muted: #888780;
    --border: #3a3a37;
    --accent-bg: #0c2f4d; --accent-text: #85b7eb; --accent-border: #185fa5;
    --success-bg: #1b3007; --success-text: #97c459;
    --warning-bg: #3a2905; --warning-text: #ef9f27;
    --danger-bg: #3a1414; --danger-text: #e58a8a;
    --gray-bg: #2c2c29;
    --line: #5aa0e6;
  }
}
* { box-sizing: border-box; }
html, body { margin: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--surface-0); color: var(--text-primary);
  max-width: 520px; margin: 0 auto; padding-bottom: 40px;
  -webkit-font-smoothing: antialiased;
  line-height: 1.5;
}
a { color: var(--accent-text); }
.head { display: flex; align-items: center; gap: 8px; padding: 16px 16px 10px; }
.head__logo { color: var(--accent-text); font-size: 18px; }
.head__name { font-weight: 600; font-size: 17px; letter-spacing: -0.01em; }
.head__date { margin-left: auto; font-size: 12px; color: var(--text-muted); text-align: right; }
.tabs { display: flex; gap: 6px; padding: 0 16px 12px; overflow-x: auto; -webkit-overflow-scrolling: touch; }
.tabs::-webkit-scrollbar { display: none; }
.tab { flex: 0 0 auto; font-family: inherit; font-size: 13px; padding: 7px 15px; border-radius: 999px; white-space: nowrap;
  border: 0.5px solid var(--border); color: var(--text-secondary); background: transparent; cursor: pointer; }
.tab--on { background: var(--accent-bg); color: var(--accent-text); border-color: var(--accent-border); font-weight: 600; }
main { padding: 4px 16px 8px; }
.panel { display: none; }
.panel--on { display: block; }
.banner { display: flex; align-items: flex-start; gap: 7px; font-size: 12.5px; color: var(--text-secondary);
  background: var(--gray-bg); border-radius: 8px; padding: 9px 11px; margin: 6px 0 14px; line-height: 1.45; }
.banner b { color: var(--text-primary); font-weight: 600; }
.sec { font-size: 11px; font-weight: 700; letter-spacing: 0.13em; text-transform: uppercase;
  color: var(--accent-text); margin: 26px 0 12px; padding-bottom: 7px; border-bottom: 1px solid var(--border); }
.sec:first-of-type { margin-top: 8px; }
.weather { background: var(--accent-bg); border: 0.5px solid var(--accent-border); border-radius: 12px;
  padding: 13px 15px; margin: 4px 0 16px; }
.weather__place { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent-text); }
.weather__temps { font-size: 19px; font-weight: 600; margin: 5px 0 3px; color: var(--text-primary); }
.weather__cond { font-size: 13px; color: var(--text-secondary); }
.weather__note { font-size: 12.5px; color: var(--text-secondary); line-height: 1.55; margin: 9px 0 0; }
.aqi-chip { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 600;
  letter-spacing: 0.02em; padding: 4px 10px; border-radius: 6px; margin-top: 9px; }
.aqi-good           { background: var(--success-bg); color: var(--success-text); }
.aqi-moderate       { background: var(--warning-bg); color: var(--warning-text); }
.aqi-sensitive      { background: var(--warning-bg); color: var(--warning-text); }
.aqi-unhealthy      { background: var(--danger-bg); color: var(--danger-text); }
.aqi-very-unhealthy { background: var(--danger-bg); color: var(--danger-text); }
.aqi-hazardous      { background: var(--danger-bg); color: var(--danger-text); }
.lead-story, .story-card, .offbeat-card, .opinion-card, .event-card, .music-card {
  background: var(--surface-2); border: 0.5px solid var(--border); border-radius: 12px;
  overflow: hidden; margin-bottom: 12px; }
.opinion-card { border-left: 3px solid var(--accent-border); }
.card-img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; background: var(--surface-1); }
.lead-body, .card-body, .offbeat-body-wrap, .opinion-body-wrap, .event-body-wrap, .music-body-wrap {
  padding: 13px 15px 12px; }
.label { font-size: 10px; font-weight: 700; letter-spacing: 0.11em; text-transform: uppercase;
  color: var(--accent-text); margin-bottom: 6px; }
.lead-headline { font-size: 20px; font-weight: 600; line-height: 1.28; margin: 0 0 9px; color: var(--text-primary); }
.card-headline, .offbeat-headline, .event-headline, .music-headline {
  font-size: 15.5px; font-weight: 600; line-height: 1.32; margin: 0 0 8px; color: var(--text-primary); }
.opinion-headline { font-size: 15px; font-weight: 600; font-style: italic; line-height: 1.32; margin: 0 0 5px; color: var(--text-primary); }
.story-body, .offbeat-body, .opinion-body, .event-body, .music-body {
  font-size: 13.5px; line-height: 1.62; color: var(--text-secondary); margin: 0 0 9px; }
.story-body:last-of-type, .offbeat-body:last-of-type, .opinion-body:last-of-type,
.event-body:last-of-type, .music-body:last-of-type { margin-bottom: 0; }
.opinion-outlet { font-size: 10.5px; font-weight: 600; letter-spacing: 0.03em; text-transform: uppercase;
  color: var(--text-muted); margin-bottom: 9px; }
.tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 9px; }
.tag { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 3px; }
.tag--kids   { background: var(--success-bg); color: var(--success-text); }
.tag--genre  { background: var(--accent-bg); color: var(--accent-text); }
.tag--int    { background: var(--gray-bg); color: var(--text-secondary); }
.story-links { display: flex; flex-wrap: wrap; align-items: center; gap: 5px 13px;
  margin-top: 11px; padding-top: 10px; border-top: 0.5px solid var(--border); font-size: 12px; }
.story-links a { color: var(--text-muted); text-decoration: none; }
.story-links a:hover { color: var(--accent-text); text-decoration: underline; }
.context-link { color: var(--accent-text) !important; font-weight: 600; }
.paywall-tag { font-size: 10px; font-weight: 700; letter-spacing: 0.04em; color: var(--text-muted); }
.expand-btn { font-family: inherit; font-size: 12px; font-weight: 600; color: var(--accent-text);
  background: none; border: none; padding: 4px 0 0; cursor: pointer; display: inline-block; }
.expand-btn:hover { text-decoration: underline; }
.share-btn { font-family: inherit; font-size: 12px; font-weight: 600; color: var(--accent-text);
  background: none; border: none; padding: 0; cursor: pointer; }
.share-btn:hover { text-decoration: underline; }
.toast { position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%); background: var(--text-primary);
  color: var(--surface-0); font-size: 13px; padding: 10px 16px; border-radius: 8px; opacity: 0;
  pointer-events: none; transition: opacity .25s ease; z-index: 1000; }
.toast.show { opacity: 0.97; }
.note { font-size: 12px; color: var(--text-muted); font-style: italic; margin: 4px 0 2px; }
footer { text-align: center; font-size: 11px; color: var(--text-muted); padding: 24px 16px 8px; }
footer a { color: var(--accent-text); text-decoration: none; }
```

**2) Tab switcher script** — before `</body>`:

```html
<script>
(function(){
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  var panels = Array.prototype.slice.call(document.querySelectorAll('.panel'));
  function show(name){
    tabs.forEach(function(t){ t.classList.toggle('tab--on', t.getAttribute('data-tab') === name); });
    panels.forEach(function(p){ p.classList.toggle('panel--on', p.getAttribute('data-panel') === name); });
  }
  tabs.forEach(function(t){
    t.addEventListener('click', function(){
      var name = t.getAttribute('data-tab');
      show(name);
      if (history.replaceState) history.replaceState(null, '', '#' + name);
    });
  });
  var hash = (location.hash || '').replace('#','');
  if (hash && document.querySelector('[data-panel="' + hash + '"]')) show(hash);
})();
</script>
```

**3) Expand-toggle script** — after the tab script. Collapses the weather note and the first paragraph of each News card to one sentence with a "More…" toggle:

```html
<script>
(function(){
  [
    ['.weather-body', '.weather__note'],
    ['.lead-body', '.story-body'],
    ['.card-body', '.story-body'],
    ['.offbeat-body-wrap', '.offbeat-body'],
    ['.opinion-body-wrap', '.opinion-body']
  ].forEach(function(pair){
    document.querySelectorAll(pair[0]).forEach(function(container){
      var paras = Array.from(container.querySelectorAll(pair[1]));
      if (!paras.length) return;
      var first = paras[0];
      var m = first.innerHTML.match(/^([\s\S]*?[.!?])(\s+)(?=[A-ZÀ-Ü<])/);
      if (!m && paras.length < 2) return;
      if (m) {
        first.innerHTML = m[1] +
          '<span class="xmore" hidden>' + first.innerHTML.slice(m[1].length) + '</span>';
      }
      paras.slice(1).forEach(function(p){ p.hidden = true; });
      var btn = document.createElement('button');
      btn.className = 'expand-btn';
      btn.textContent = 'More…';
      btn.setAttribute('data-open', '0');
      btn.addEventListener('click', function(){
        var open = btn.getAttribute('data-open') === '1';
        var xmore = first.querySelector('.xmore');
        if (xmore) xmore.hidden = open;
        paras.slice(1).forEach(function(p){ p.hidden = open; });
        btn.textContent = open ? 'More…' : 'Less';
        btn.setAttribute('data-open', open ? '0' : '1');
      });
      first.after(btn);
    });
  });
})();
</script>
```

**4) Share script** — after the expand script, before `</body>`. Injects a "Share" button into every `.story-links` across all three tabs:

```html
<script>
(function(){
  function storyOf(el){
    return el.closest('.lead-story, .story-card, .offbeat-card, .opinion-card, .event-card, .music-card');
  }
  function textOf(story, sel){
    var n = story.querySelector(sel);
    return n ? n.textContent.replace(/\s+/g,' ').trim() : '';
  }
  function buildShareText(story, links){
    var headline = textOf(story, '.lead-headline, .card-headline, .offbeat-headline, .opinion-headline, .event-headline, .music-headline');
    var summary  = textOf(story, '.story-body, .offbeat-body, .opinion-body, .event-body, .music-body');
    var anchors  = Array.from(links.querySelectorAll('a'));
    var sources  = anchors.filter(function(a){ return a.getAttribute('target') === '_blank'; });
    var context  = anchors.filter(function(a){ return a.getAttribute('target') !== '_blank'; });
    var lines = [headline, '', summary];
    if (sources.length){
      lines.push('', 'Read more:');
      sources.forEach(function(a){
        var name = a.textContent.replace(/^\s*Read more\s*→\s*/i,'').replace(/\s+/g,' ').trim();
        lines.push('• ' + name + ': ' + a.href);
      });
    }
    if (context.length){
      var c = context[0];
      var title = c.textContent.replace(/^\s*→\s*Background:\s*/i,'').replace(/^\s*→\s*/,'').replace(/\s+/g,' ').trim();
      lines.push('', 'Background: ' + title + ' ' + c.href);
    }
    lines.push('', '— via Chile Morning · https://neal-jpg.github.io/chile-news/');
    return lines.join('\n');
  }
  var toast;
  function showToast(msg){
    if (!toast){ toast = document.createElement('div'); toast.className = 'toast'; document.body.appendChild(toast); }
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(function(){ toast.classList.remove('show'); }, 1800);
  }
  document.querySelectorAll('.story-links').forEach(function(links){
    var story = storyOf(links);
    if (!story) return;
    var btn = document.createElement('button');
    btn.className = 'share-btn';
    btn.type = 'button';
    btn.textContent = 'Share';
    btn.addEventListener('click', function(){
      var text = buildShareText(story, links);
      if (navigator.share){
        navigator.share({ text: text }).catch(function(){});
      } else if (navigator.clipboard){
        navigator.clipboard.writeText(text).then(function(){ showToast('Copied to clipboard'); })
          .catch(function(){ showToast('Copy failed'); });
      } else {
        showToast('Sharing not supported');
      }
    });
    links.appendChild(btn);
  });
})();
</script>
```
