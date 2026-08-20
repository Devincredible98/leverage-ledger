#!/usr/bin/env python3
"""
The Leverage Ledger — daily newsletter generator.
Topic: millennials/Gen Z escaping the 9-5 grind and building income outside
broke-industry jobs (trading, YouTube automation, ecommerce, AI B2B, SMM,
digital products, reselling, car detailing, lawn care, etc).

Output:
  - newsletter.md  (human-readable)
  - feed.xml       (RSS 2.0 — beehiiv RSS->newsletter pulls this)

No API POST (beehiiv posts endpoint is Enterprise-only). RSS automation sends it.
"""
import datetime, hashlib, os, random

PUB_ID = "pub_194ae4d5-4830-443e-89e8-f8ad39535219"
SITE = "https://leverage-ledger.netlify.app"
TITLE = "The Leverage Ledger"

# Content banks — rotating, so each issue feels distinct
ANGLES = [
    ("Trading Options & Futures", "A 25-year-old quit a $17/hr warehouse job after learning to sell options premium on a paper account for 6 months. The edge wasn't a 'secret indicator' — it was risk rules: 1-2% per trade, no trades 15 min around news, and logging every loss. Start on paper. The market will still be there when you're ready."),
    ("YouTube Automation", "Faceless YouTube channels are printing without a face on camera: compilation, finance explainers, and 'day in the life of a remote worker' loops. The leverage is the system — script, voiceover (AI), render, schedule. One person runs 3 channels. Watch time pays; sponsors pay more."),
    ("Ecommerce & Reselling", "Reselling isn't just thrift flips. The real leverage is arbitrage at scale: sourcing via reselling apps, relisting with better photos, and bundling. A college student did $4k/mo flipping returned Amazon stock bought at liquidation. The grind job paid less."),
    ("AI Automation B2B", "Local businesses are drowning in manual work — booking, follow-ups, invoicing. Sell them a simple AI workflow (not a 'platform'). Pitch: 'I'll save you 10 hours/week.' Charge $500-1500/mo. No code degree needed; just know which tool connects to what."),
    ("Social Media Management", "Every restaurant, gym, and realtor needs a feed but has no time. Manage 5 local accounts at $400-750/mo each = a full-time salary, remotely, in sweatpants. The skill is consistency + showing the owner real numbers."),
    ("Digital Products", "Courses, ebooks, PDFs, Notion templates — build once, sell forever. A $19 PDF on 'how to start reselling' out-earns a shift when it sells while you sleep. Leverage = productized knowledge."),
    ("Car Detailing & Lawn Care", "The 'unsexy' trades print. Mobile detailing at $150-400 a pop, 4 cars a weekend = more than a fast-food manager. Lawn care on a route = recurring. Real skills, real cash, no boss watching the clock."),
]

HOOKS = [
    "You were not built to scan boxes at 4am so a DSP can hit quota.",
    "The 40-hour week was a deal. You can renegotiate — by building leverage.",
    "Uber Eats pays per mile. Ownership pays per system.",
    "A shitty job application is a bet on someone else's calendar. Build your own.",
    "The grind isn't noble when it's rented time. Own the asset.",
]

def build_issue():
    today = datetime.date.today()
    # pick 3 distinct angles
    picks = random.sample(ANGLES, 3)
    hook = random.choice(HOOKS)
    # today's 'play' — one concrete first step
    play = picks[0][1].split(". ")[0] + "."

    md = []
    md.append(f"# {TITLE} — {today.strftime('%B %d, %Y')}\n")
    md.append(f"> {hook}\n")
    md.append("## Today's Reality Check")
    md.append("The system sells you time for a wage. Leverage buys it back. Here are three ways people your age are building income outside the broke-industry loop — no degree, no permission slip required.\n")
    for i, (name, body) in enumerate(picks, 1):
        md.append(f"### {i}. {name}")
        md.append(body + "\n")
    md.append("## Today's Play")
    md.append(f"Pick ONE of the above. Spend 30 minutes today researching the first step — not consuming, *doing*. Momentum beats motivation.\n")
    md.append("---\n*The Leverage Ledger — income without the 9-5. Unsubscribe anytime.*")
    return today, "\n".join(md), picks, hook

def to_html(md_text):
    # minimal markdown->html (paragraphs, headings, blockquote, hr)
    lines = md_text.split("\n")
    html, in_p = [], False
    def close_p():
        nonlocal in_p
        if in_p:
            html.append("</p>"); in_p = False
    for ln in lines:
        s = ln.strip()
        if not s:
            close_p(); continue
        if s.startswith("# "):
            close_p(); html.append(f"<h1>{s[2:]}</h1>")
        elif s.startswith("## "):
            close_p(); html.append(f"<h2>{s[3:]}</h2>")
        elif s.startswith("### "):
            close_p(); html.append(f"<h3>{s[4:]}</h3>")
        elif s.startswith("> "):
            close_p(); html.append(f"<blockquote>{s[2:]}</blockquote>")
        elif s.startswith("---"):
            close_p(); html.append("<hr>")
        elif s.startswith("*") and s.endswith("*"):
            close_p(); html.append(f"<p><em>{s[1:-1]}</em></p>")
        else:
            if not in_p:
                html.append("<p>"); in_p = True
            html.append(s + " ")
    close_p()
    return "\n".join(html)

def main():
    today, md, picks, hook = build_issue()
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "newsletter.md"), "w") as f:
        f.write(md)
    html = to_html(md)
    guid = hashlib.md5(today.isoformat().encode()).hexdigest()
    item_url = f"{SITE}/issue-{today.isoformat()}"
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{TITLE}</title>
    <link>{SITE}</link>
    <description>Daily plays for escaping the 9-5 and building income outside broke-industry jobs — trading, YouTube, ecommerce, AI B2B, SMM, digital products, reselling, detailing, and more.</description>
    <language>en-us</language>
    <lastBuildDate>{today.strftime('%a, %d %b %Y 09:00:00 -0500')}</lastBuildDate>
    <item>
      <title>{TITLE} — {today.strftime('%B %d, %Y')}</title>
      <link>{item_url}</link>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{today.strftime('%a, %d %b %Y 09:00:00 -0500')}</pubDate>
      <description><![CDATA[{html}]]></description>
    </item>
  </channel>
</rss>"""
    with open(os.path.join(base, "feed.xml"), "w") as f:
        f.write(feed)
    print(f"Generated issue for {today.isoformat()}")
    print(f"  angles: {[p[0] for p in picks]}")
    print(f"  newsletter.md + feed.xml written")

if __name__ == "__main__":
    main()
