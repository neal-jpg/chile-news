#!/usr/bin/env python3
"""Build index.html for the Chile Morning Digest GitHub Pages site.

Scans every digest_YYMMDD.html in this folder, pulls the human-readable date
and the lead headline from each, and writes a styled landing page that links
to the latest digest plus an archive of all earlier ones. Run this after
creating each morning's digest (the daily workflow does this automatically).
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


def main():
    files = sorted(glob.glob(os.path.join(HERE, "digest_*.html")), reverse=True)
    entries = []
    for f in files:
        date, headline = extract(f)
        entries.append((os.path.basename(f), date, headline))

    if not entries:
        print("No digests found.")
        return

    latest_file, latest_date, latest_headline = entries[0]

    archive_rows = "\n".join(
        f'''        <li>
          <a href="{fn}">
            <span class="arc-date">{html.escape(date)}</span>
            <span class="arc-head">{html.escape(headline)}</span>
          </a>
        </li>'''
        for fn, date, headline in entries[1:]
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chile Morning Digest</title>
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
    .section-label {{
      font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700;
      letter-spacing: 0.15em; text-transform: uppercase; color: #b5802a;
      margin-bottom: 14px; padding-bottom: 8px; border-bottom: 2px solid #111;
    }}
    .latest {{
      display: block; background: #fffefb; border: 1px solid #c9c4ba;
      border-radius: 3px; padding: 26px 28px; text-decoration: none; color: inherit;
      transition: box-shadow .15s ease, transform .15s ease; margin-bottom: 40px;
    }}
    .latest:hover {{ box-shadow: 0 6px 20px rgba(0,0,0,.12); transform: translateY(-2px); }}
    .latest .l-date {{
      font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600;
      color: #6b6b6b; letter-spacing: 0.03em;
    }}
    .latest .l-head {{
      font-family: 'Playfair Display', Georgia, serif; font-size: clamp(22px, 3.4vw, 30px);
      font-weight: 700; line-height: 1.25; margin: 10px 0 12px;
    }}
    .latest .l-cta {{
      font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600; color: #b5802a;
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
    <div class="masthead-title">The Morning Briefing</div>
    <div class="masthead-sub">Santiago, Chile</div>
    <div class="masthead-rule"></div>
  </header>

  <div class="wrapper">
    <div class="section-label">Latest Edition</div>
    <a class="latest" href="{latest_file}">
      <div class="l-date">{html.escape(latest_date)}</div>
      <div class="l-head">{html.escape(latest_headline)}</div>
      <div class="l-cta">Read today's briefing &rarr;</div>
    </a>

    <div class="section-label">Archive</div>
    <ul class="archive">
{archive_rows}
    </ul>
  </div>

  <footer>Chile Morning Digest &middot; Updated daily</footer>
</body>
</html>
"""

    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"Wrote {out} — latest: {latest_file} ({len(entries)} editions)")


if __name__ == "__main__":
    main()
