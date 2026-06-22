# Chile News Morning Digest — Project Instructions

## What this project does

Every morning, crawl a set of Chilean news websites and produce a single-page HTML morning digest for Neal — an American living in Santiago. The digest covers what matters, explained in terms that make sense to someone who knows US politics but not Chilean politics.

## Output format

- **Language:** English only
- **Length:** One page maximum. Tight. No padding.
- **Format:** Self-contained HTML file — single file, no external dependencies except image URLs and hyperlinks
- **Filename:** `digest_YYMMDD.html` (e.g. `digest_260527.html`)
- **Save to:** this project folder

## Landing page (index.html) and archive

The site is served via GitHub Pages, which loads `index.html` at the root URL — without it the bare site URL 404s. After creating each morning's digest, run `python3 generate_index.py` in this folder. It produces two files:

- **`index.html`** — a verbatim copy of the newest `digest_YYMMDD.html`, with a small "↗ Browse the archive" link injected near the top. This is the stable bookmark URL (`https://neal-jpg.github.io/chile-news/`): it always opens straight onto today's full briefing, no click-through.
- **`archive.html`** — a newest-first list of every edition, linked from the digest's archive link.

The dated `digest_*.html` files are the permanent, canonical archive and are never modified by the script. Do not hand-edit `index.html` or `archive.html`; the script overwrites both.

## Design requirements

The HTML should look like a real editorial product — not a wall of text. Use:
- A clean serif or sans-serif editorial font (load from Google Fonts)
- A clear masthead with the date and "Chile Morning Digest"
- **Multi-column layout** for the main content area — two columns side by side, with the weather card spanning full width at the top. This keeps the digest compact and avoids excessive scrolling. Columns should collapse to a single column on mobile.
- Section headers with visual weight
- Featured images pulled from article URLs where available (use `<img>` with the source URL directly)
- A weather section styled like a simple weather card (full width, above the columns)
- Comfortable line spacing, max-width ~960px, centered, light background
- Mobile-friendly (single column below 600px)

Think: newspaper front page meets digital newsletter. Clean, readable, not cluttered.

## Sections (in order)

### 1. Weather
Pull the Santiago forecast for today. Include: high/low, conditions, and one sentence of practical context ("bring a jacket" level). Source: wttr.in/Santiago or a news site weather section.

### 2. Top Headlines (3–5 stories)
The most important Chilean news stories of the day. For each:
- **Headline** (bold)
- 2–3 sentence summary in plain English
- If the story requires Chilean political/historical context to understand, include a "→ Background" link — see **Context pages** below for how these work
- Pull a lead image from the article if one is available

### 3. Interesting / Offbeat (1–2 items)
Something surprising, human, cultural, or worth knowing. Not hard news. Keep it light.

### 4. Opinion / Editorial (1–2 items)
One or two notable opinion pieces or editorials from Chilean outlets. Summarize the argument in 2–3 sentences. Include the outlet and author. Note whether the publication leans left, right, or center.

## What to leave out

- **Sports** — entirely. No scores, no games, no transfers.
- PR wire stories and sponsored content
- Celebrity gossip unless it has genuine national relevance

## Context framing

Neal grew up in the US and understands American political concepts (partisanship, executive vs. legislative power, midterms, Supreme Court decisions, etc.). Use those as reference points when explaining Chilean politics.

Examples of how to frame context:
- "Chile's Senate, which functions similarly to the US Senate, voted to..."
- "The Chilean left, think Bernie Sanders–style economic policies, is pushing back on..."
- "This is roughly equivalent to a US Supreme Court ruling being overturned by Congress..."

Don't over-explain — just enough so the story lands.

## News sources

When crawling:
- Fetch the homepage and any section pages (política, nacional, economía, cultura, tendencias)
- Skip deporte/deportes sections entirely
- Prefer stories from the last 24 hours
- **The Clinic is important** — it is left-leaning and satirical and provides a different perspective from the other sources. If the homepage fetch is too large, try fetching specific section pages like `https://www.theclinic.cl/noticias/politica/` or `https://www.theclinic.cl/lo-ultimo/` directly.

**Sources to crawl:**
- https://www.emol.com/ — center-right, one of Chile's largest legacy papers
- https://www.latercera.com/ — center-right, major daily
- https://www.biobiochile.cl/ — center, strong regional/national coverage
- https://www.theclinic.cl/ — left-leaning, satirical/opinion-heavy; try section pages if homepage fails
- https://www.df.cl/ — business/financial news (Chile's equivalent of the WSJ)

## Weather source

`https://wttr.in/Santiago?format=j1` — returns JSON with current conditions and forecast.

Or use the weather widget from any connected news site.

## Scheduled run

This digest is intended to run every morning. Use the `schedule` skill to set up an automated daily run if not already configured.

## Context pages

When a story needs background that would take more than two sentences to explain inline, create a separate context page instead of linking to Wikipedia directly. Rules:

- **Filename:** `context_YYMMDD_slug.html` (e.g. `context_260527_acusacion-constitucional.html`) — saved in the same project folder
- **Format:** Self-contained single HTML file, same visual style as the digest (same fonts, same color palette, same masthead style but with a "Context" label)
- **Length:** Short — 200–400 words. Just enough for the concept to click. Plain English framed for an American reader.
- **Structure:** Brief definition → how it works in Chile → American analogy → why it matters for today's story
- If a deeper dive is useful, you may include a "Read more" link to a Wikipedia article or other external source at the bottom — but the page itself should be self-contained enough that the reader doesn't need to follow it.
- The "→ Background" link in the digest should point to this local context file (e.g. `context_260527_acusacion-constitucional.html`), not to Wikipedia directly.
- **Reuse:** If a context page was created on a previous day for the same topic (e.g. "What is a constitutional accusation"), link to that existing file rather than creating a duplicate.

## Source links

Every story — Top Headlines, Interesting/Offbeat, and Opinion/Editorial — must include a "Read more →" link to the original article URL. Link text should be the outlet name (e.g. "Read more → La Tercera" or "Read more → Emol"). Style it as a small, understated inline link below the summary, similar to the context link style. This applies even when a "→ Background" context link is also present.

## Notes

- Do not include a market/financial ticker in the digest
- If there's no notable opinion content that day, skip that section
- Images should have `alt` text
- The file should open cleanly in any browser with no broken dependencies

## Daily refinements (added 2026-06-21)

These extend the sections above.

### Weather card — air quality + collapse

The weather card's glance (always visible) is: location/season, temps (°C and °F), a one-line condition, and a **Las Condes air-quality chip**. The long practical paragraph stays in `.weather-note` and is auto-collapsed to its first sentence with a "More…" toggle (the expand script below includes the `['.weather-body', '.weather-note']` pair — no manual change needed).

Air quality:
- Fetch the current AQI for the **Las Condes** station. Primary: the World Air Quality Index feed (waqi.info) for Las Condes, which reports on the US AQI scale. Fallback: Chile's SINCA network (`sinca.mma.gob.cl`) Las Condes station, converting PM2.5 to US AQI. If Las Condes is unavailable, use the nearest eastern-Santiago station and relabel the chip (e.g. "Santiago E. air"); if no reading at all, omit the chip.
- Emit the chip **immediately after `.weather-condition` and before `.weather-note`**:
  `<div class="aqi-chip aqi-{band}">Las Condes air · {AQI} {category}</div>`
- US AQI band → class · category: 0–50 `aqi-good` · good; 51–100 `aqi-moderate` · moderate; 101–150 `aqi-sensitive` · unhealthy for sensitive groups; 151–200 `aqi-unhealthy` · unhealthy; 201–300 `aqi-very-unhealthy` · very unhealthy; 301+ `aqi-hazardous` · hazardous.

### Paywalled links

- Treat links to these outlets as paywalled: **El Mercurio** (elmercurio.com), **Diario Financiero** (df.cl) premium articles, **La Tercera Premium**. Maintain this list as new paywalls appear.
- When emitting a paywalled "Read more" link, append a marker inside the anchor:
  `Read more → {Outlet} <span class="paywall-tag">🔒 paywall</span>`
- If the same story is also covered by a **free** outlet, list the free link first (primary); keep the paywalled link too, marked.
- We cannot read behind paywalls — only the public preview. Route around them; never attempt to bypass a paywall.

### Opinion balance (best-effort)

- Aim for **at least one left-leaning and one right-leaning** opinion daily, each tagged with its lean in `.opinion-outlet` (e.g. "… · Left-Leaning", "… · Center-Right").
- Prefer **free** columnists so they're readable. Free options span the spectrum, e.g. The Clinic / El Mostrador / El Desconcierto (left); El Líbero / Ex-Ante / La Tercera free columns (right).
- If the sharpest take is paywalled, find a free piece making a similar — or the opposing — argument so the viewpoint still appears.
- **Best-effort, not forced:** if one side genuinely has nothing notable, say so plainly (e.g. "No standout conservative column today") rather than padding with a weak piece.

### Share buttons

Every story gets a "Share" control that sends the full text (headline, summary, source links, context link, attribution) via the native share sheet, with a clipboard fallback. **Do not hand-add Share buttons** — the canonical share script below injects one into every `.story-links` automatically. Just include the script and the `.share-btn`/`.toast` CSS.

### Canonical interactive snippets — emit verbatim in every digest

Include all three blocks below, unchanged, so each run produces identical, working code.

**1) CSS** — add inside the `<style>` block:

```css
/* AIR QUALITY CHIP */
.aqi-chip { display:inline-flex; align-items:center; gap:6px; font-family:'Inter',sans-serif; font-size:12px; font-weight:600; letter-spacing:0.02em; padding:5px 11px; border-radius:6px; margin-top:8px; }
.aqi-good           { background:#e6f4ea; color:#1e6b3a; }
.aqi-moderate       { background:#fbeecb; color:#856518; }
.aqi-sensitive      { background:#fbe3cf; color:#9a541b; }
.aqi-unhealthy      { background:#f8dada; color:#9a2b2b; }
.aqi-very-unhealthy { background:#ece0f3; color:#5d2c7c; }
.aqi-hazardous      { background:#ecd9d9; color:#6d1f1f; }
/* PAYWALL TAG */
.paywall-tag { font-family:'Inter',sans-serif; font-size:10px; font-weight:700; letter-spacing:0.04em; color:#8a7a52; }
/* SHARE BUTTON + TOAST */
.share-btn { font-family:'Inter',sans-serif; font-size:12px; font-weight:600; letter-spacing:0.02em; color:#b5802a; background:none; border:none; padding:0; cursor:pointer; }
.share-btn:hover { text-decoration:underline; }
.toast { position:fixed; left:50%; bottom:24px; transform:translateX(-50%); background:#111; color:#fff; font-family:'Inter',sans-serif; font-size:13px; padding:10px 16px; border-radius:6px; opacity:0; pointer-events:none; transition:opacity .25s ease; z-index:1000; }
.toast.show { opacity:0.96; }
```

**2) Expand-toggle script** — place before `</body>`. The `['.weather-body', '.weather-note']` pair (first entry) is what collapses the weather note:

```html
<script>
(function(){
  [
    ['.weather-body', '.weather-note'],
    ['.lead-body', '.story-body'],
    ['.card-body', '.story-body'],
    ['.offbeat-card', '.offbeat-body'],
    ['.opinion-card', '.opinion-body']
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

**3) Share script** — place after the expand script, before `</body>`:

```html
<script>
(function(){
  function storyOf(el){
    return el.closest('.lead-story, .story-card, .offbeat-card, .opinion-card');
  }
  function textOf(story, sel){
    var n = story.querySelector(sel);
    return n ? n.textContent.replace(/\s+/g,' ').trim() : '';
  }
  function buildShareText(story, links){
    var headline = textOf(story, '.lead-headline, .card-headline, .offbeat-headline, .opinion-headline');
    var summary  = textOf(story, '.story-body, .offbeat-body, .opinion-body');
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
    lines.push('', '— via Chile Morning Digest · https://neal-jpg.github.io/chile-news/');
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
