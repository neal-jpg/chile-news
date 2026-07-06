#!/usr/bin/env python3
"""Build index.html and archive.html for the Chile Morning Digest GitHub Pages site.

The site is served via GitHub Pages, which loads index.html at the bare root URL.
So that a single bookmarked link (https://neal-jpg.github.io/chile-news/) always
opens straight onto the newest briefing, this script copies the latest
digest_YYMMDD.html verbatim into index.html, injecting a small "Browse the
archive" link near the top. The full back-catalogue lives on archive.html, which
lists every edition newest-first. The dated digest_*.html files are never
modified — they remain the permanent, canonical archive.

Run this after creating each morning's digest (the daily workflow does this
automatically).
"""

import glob
import os
import re
import html

HERE = os.path.dirname(os.path.abspath(__file__))


def date_from_filename(path):
    """digest_YYMMDD.html -> 'Tuesday, June 16, 2026' (reliable across layouts)."""
    m = re.search(r'digest_(\d{2})(\d{2})(\d{2})\.html', os.path.basename(path))
    if not m:
        return os.path.basename(path)
    yy, mm, dd = (int(x) for x in m.groups())
    import datetime
    return datetime.date(2000 + yy, mm, dd).strftime("%A, %B %-d, %Y")


def extract(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    head_m = re.search(r'<h2[^>]*class="lead-headline"[^>]*>\s*([^<]+)', text)
    date = date_from_filename(path)
    headline = head_m.group(1).strip() if head_m else "Morning briefing"
    return date, headline


# Small understated link injected into index.html so readers can reach the
# archive from the always-latest root page. Uses inline styles so it does not
# depend on whatever CSS classes a given digest happens to define. The colour
# references the digest's own --accent-text custom property so it stays
# theme-aware (blue in both light and dark), matching the app shell.
ARCHIVE_BAR = (
    '\n  <div style="max-width:520px;margin:0 auto;padding:10px 16px 0;'
    'text-align:right;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\','
    'Roboto,sans-serif;font-size:12px;font-weight:600;letter-spacing:0.02em;">'
    '<a href="archive.html" style="color:var(--accent-text,#185fa5);'
    'text-decoration:none;">↗ Browse the archive</a></div>'
)


def build_index(latest_file):
    """index.html = a verbatim copy of the latest digest + an archive link."""
    with open(os.path.join(HERE, latest_file), encoding="utf-8") as fh:
        content = fh.read()
    if "</header>" in content:
        content = content.replace("</header>", "</header>" + ARCHIVE_BAR, 1)
    else:  # no masthead to anchor to — drop the link in after <body>
        content = content.replace("<body>", "<body>" + ARCHIVE_BAR, 1)
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(content)
    return out


def build_archive(entries):
    """archive.html = newest-first list of every edition."""
    rows = "\n".join(
        f'''        <li>
          <a href="{fn}">
            <span class="arc-date">{html.escape(date)}</span>
            <span class="arc-head">{html.escape(headline)}</span>
          </a>
        </li>'''
        for fn, date, headline in entries
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chile Morning — Archive</title>
  <style>
    :root {{
      --surface-0: #f7f6f2; --surface-1: #efeee8; --surface-2: #ffffff;
      --text-primary: #20201e; --text-secondary: #5f5e5a; --text-muted: #8a8880;
      --border: #e2e0d8;
      --accent-bg: #e6f1fb; --accent-text: #185fa5; --accent-border: #85b7eb;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --surface-0: #1a1a19; --surface-1: #242422; --surface-2: #2f2f2c;
        --text-primary: #f2f1ec; --text-secondary: #b4b2a9; --text-muted: #888780;
        --border: #3a3a37;
        --accent-bg: #0c2f4d; --accent-text: #85b7eb; --accent-border: #185fa5;
      }}
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--surface-0); color: var(--text-primary);
      max-width: 520px; margin: 0 auto; padding-bottom: 40px;
      -webkit-font-smoothing: antialiased; line-height: 1.5;
    }}
    .head {{ display: flex; align-items: center; gap: 8px; padding: 16px 16px 10px; }}
    .head__logo {{ color: var(--accent-text); font-size: 18px; }}
    .head__name {{ font-weight: 600; font-size: 17px; letter-spacing: -0.01em; }}
    .head__sub {{ margin-left: auto; font-size: 12px; color: var(--text-muted); }}
    main {{ padding: 4px 16px 8px; }}
    .backlink {{ display: inline-block; margin: 4px 0 18px; font-size: 13px; font-weight: 600;
      color: var(--accent-text); text-decoration: none; }}
    .backlink:hover {{ text-decoration: underline; }}
    .sec {{ font-size: 11px; font-weight: 700; letter-spacing: 0.13em; text-transform: uppercase;
      color: var(--accent-text); margin: 8px 0 12px; padding-bottom: 7px; border-bottom: 1px solid var(--border); }}
    ul.archive {{ list-style: none; padding: 0; margin: 0; }}
    ul.archive li {{ margin-bottom: 10px; }}
    ul.archive a {{ display: flex; flex-direction: column; gap: 4px;
      background: var(--surface-2); border: 0.5px solid var(--border); border-radius: 12px;
      padding: 12px 14px; text-decoration: none; color: inherit; transition: border-color .15s ease; }}
    ul.archive a:hover {{ border-color: var(--accent-border); }}
    ul.archive a:hover .arc-head {{ color: var(--accent-text); }}
    .arc-date {{ font-size: 11px; font-weight: 600; letter-spacing: 0.03em; text-transform: uppercase; color: var(--text-muted); }}
    .arc-head {{ font-size: 14.5px; font-weight: 600; line-height: 1.35; }}
    footer {{ text-align: center; font-size: 11px; color: var(--text-muted); padding: 24px 16px 8px; }}
  </style>
</head>
<body>
  <header class="head">
    <span class="head__logo">◈</span>
    <span class="head__name">Chile Morning</span>
    <span class="head__sub">Archive · Santiago</span>
  </header>

  <main>
    <a class="backlink" href="index.html">&larr; Today's edition</a>
    <div class="sec">All Editions</div>
    <ul class="archive">
{rows}
    </ul>
  </main>

  <footer>Chile Morning &middot; Updated daily</footer>
</body>
</html>
"""
    out = os.path.join(HERE, "archive.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    return out


def main():
    files = sorted(glob.glob(os.path.join(HERE, "digest_*.html")), reverse=True)
    entries = []
    for f in files:
        date, headline = extract(f)
        entries.append((os.path.basename(f), date, headline))

    if not entries:
        print("No digests found.")
        return

    latest_file = entries[0][0]
    build_index(latest_file)
    build_archive(entries)
    print(f"Wrote index.html (mirrors {latest_file}) and archive.html "
          f"({len(entries)} editions).")


if __name__ == "__main__":
    main()
