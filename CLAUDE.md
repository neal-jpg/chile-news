# Chile News Morning Digest — Project Instructions

## What this project does

Every morning, crawl a set of Chilean news websites and produce a single-page HTML morning digest for Neal — an American living in Santiago. The digest covers what matters, explained in terms that make sense to someone who knows US politics but not Chilean politics.

## Output format

- **Language:** English only
- **Length:** One page maximum. Tight. No padding.
- **Format:** Self-contained HTML file — single file, no external dependencies except image URLs and hyperlinks
- **Filename:** `digest_YYMMDD.html` (e.g. `digest_260527.html`)
- **Save to:** this project folder

## Landing page (index.html)

The site is served via GitHub Pages, which loads `index.html` at the root URL — without it the bare site URL 404s. After creating each morning's digest, regenerate the landing page by running `python3 generate_index.py` in this folder. It scans all `digest_*.html` files, links the newest as the featured edition, and lists the rest as an archive. Do not hand-edit `index.html`; the script overwrites it.

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
