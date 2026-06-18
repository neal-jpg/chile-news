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
# depend on whatever CSS classes a given digest happens to define.
ARCHIVE_BAR = (
    '\n  <div style="max-width:980px;margin:0 auto;padding:14px 18px 0;'
    'text-align:right;font-family:\'Inter\',sans-serif;font-size:12px;'
    'font-weight:600;letter-spacing:0.03em;">'
    '<a href="archive.html" style="color:#b5802a;text-decoration:none;">'
    '↗ Browse the archive</a></div>'
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
  <title>Chile Morning Digest — Archive</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Source Serif 4', Georgia, serif;
      background: #ddd9d1; color: #1a1a1a;
      font-size: 17px; line-height: 1.7;
    }}
    header {{ background: #111; padding: 22px 24px 18px; text-align: center; }}
    .eyebrow {{
      font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 700;
      letter-spacing: 0.2em; text-transform: uppercase; color: #b5802a; margin-bottom: 6px;
    }}
    .masthead-title {{
      font-family: 'Playfair Display', Georgia, serif; font-size: clamp(28px, 5vw, 44px);
      font-weight: 700; color: #fffefb; letter-spacing: 0.01em;
    }}
    .masthead-sub {{
      font-family: 'Inter', sans-serif; font-size: 12px; color: #888;
      margin-top: 6px; letter-spacing: 0.05em;
    }}
    .masthead-rule {{ width: 40px; height: 2px; background: #b5802a; margin: 12px auto 0; }}
    .wrapper {{ max-width: 980px; margin: 0 auto; padding: 32px 24px 56px; }}
    .backlink {{
      display: inline-block; margin-bottom: 26px;
      font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600;
      color: #b5802a; text-decoration: none; letter-spacing: 0.03em;
    }}
    .backlink:hover {{ text-decoration: underline; }}
    .section-label {{
      font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700;
      letter-spacing: 0.15em; text-transform: uppercase; color: #b5802a;
      margin-bottom: 14px; padding-bottom: 8px; border-bottom: 2px solid #111;
    }}
    ul.archive {{ list-style: none; }}
    ul.archive li {{ border-bottom: 1px solid #c9c4ba; }}
    ul.archive a {{
      display: flex; flex-direction: column; gap: 3px; padding: 14px 4px;
      text-decoration: none; color: inherit; transition: padding-left .15s ease, color .15s ease;
    }}
    ul.archive a:hover {{ padding-left: 10px; }}
    ul.archive a:hover .arc-head {{ color: #b5802a; }}
    .arc-date {{ font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; color: #6b6b6b; }}
    .arc-head {{ font-size: 17px; line-height: 1.4; }}
    footer {{
      text-align: center; font-family: 'Inter', sans-serif; font-size: 11px;
      color: #8a8579; padding: 24px; letter-spacing: 0.04em;
    }}
  </style>
</head>
<body>
  <header>
    <div class="eyebrow">Chile Morning Digest</div>
    <div class="masthead-title">Archive</div>
    <div class="masthead-sub">Santiago, Chile</div>
    <div class="masthead-rule"></div>
  </header>

  <div class="wrapper">
    <a class="backlink" href="index.html">&larr; Today's edition</a>
    <div class="section-label">All Editions</div>
    <ul class="archive">
{rows}
    </ul>
  </div>

  <footer>Chile Morning Digest &middot; Updated daily</footer>
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
