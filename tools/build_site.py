#!/usr/bin/env python3
"""Generate finditcheaper.co.uk from data/products.json.

Run from the repo root:  python3 tools/build_site.py
Writes index.html, products/<slug>/index.html, weeks/<date>/index.html, sitemap.xml.
"""
import json, os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data", "products.json")))
SITE = DATA["site"]


def esc(s):
    return html.escape(str(s), quote=True)


def gbp(v):
    return f"£{v:,.2f}".replace(".00", "") if float(v).is_integer() else f"£{v:,.2f}"


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def store_url(p):
    if p.get("asin"):
        return f"https://www.amazon.co.uk/dp/{p['asin']}?tag={SITE['amazon_tag']}"
    return p.get("url", "#")


CSS = """
:root{--bg:#0b0b12;--surface:#15151f;--line:#262633;--fg:#f4f3f7;--muted:#a3a2b0;--accent:#ff9f0a;--hot:#ff2d55;
--display:"Poppins","Segoe UI",system-ui,sans-serif;--body:"DM Sans","Segoe UI",system-ui,sans-serif;color-scheme:dark}
*{box-sizing:border-box}html{background:var(--bg)}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);line-height:1.5;padding-inline:16px;padding-block:0 56px}
a{color:var(--accent)}.wrap{max-width:720px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:18px 0;border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--fg);font-family:var(--display);font-weight:800;font-size:20px;letter-spacing:-.3px}
.brand img{width:34px;height:34px;border-radius:50%}
.brand span{color:var(--accent)}
.nav a{color:var(--muted);text-decoration:none;font-size:14px;margin-left:14px}.nav a:hover{color:var(--fg)}
h1{font-family:var(--display);font-weight:800;font-size:clamp(28px,6vw,40px);line-height:1.1;letter-spacing:-.5px;margin:28px 0 8px;text-wrap:balance}
h2{font-family:var(--display);font-weight:700;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:30px 0 12px}
.lede{color:var(--muted);font-size:17px;max-width:60ch;margin:0 0 8px}
.meta{color:var(--muted);font-size:13px}
.list{display:grid;gap:12px;margin-top:16px}
.item{display:grid;grid-template-columns:96px 1fr auto;gap:14px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:12px;min-width:0}
.item img{width:96px;height:96px;object-fit:contain;background:#fff;border-radius:10px}
.item .name{font-weight:600;font-size:16px;line-height:1.25}.item .name a{color:var(--fg);text-decoration:none}
.item .sub{color:var(--muted);font-size:13px;margin-top:3px}
.price{font-family:var(--display);font-weight:700;font-size:20px;color:var(--accent);font-variant-numeric:tabular-nums}
.btn{display:inline-flex;align-items:center;justify-content:center;white-space:nowrap;background:var(--accent);color:#141008;font-weight:700;font-family:var(--display);font-size:14px;padding:11px 16px;border-radius:999px;text-decoration:none}
.btn.alt{background:transparent;color:var(--fg);border:1px solid var(--line)}
.btn:hover{filter:brightness(1.08)}a:focus-visible{outline:3px solid var(--fg);outline-offset:2px}
.hero{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start;margin-top:20px}
.hero img{width:100%;max-width:100%;background:#fff;border-radius:18px;aspect-ratio:1;object-fit:contain}
.pill{display:inline-block;background:var(--hot);color:#fff;font-weight:600;font-size:13px;padding:5px 12px;border-radius:999px}
table{width:100%;border-collapse:collapse;margin-top:8px;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:12px 8px;border-bottom:1px solid var(--line);vertical-align:middle}
th{color:var(--muted);font-weight:500;font-size:13px}td.p{font-family:var(--display);font-weight:700;font-size:18px;white-space:nowrap}
td.p s{color:var(--muted);font-weight:400;font-size:13px;margin-left:6px;text-decoration-color:var(--hot)}
tr.best td.p{color:var(--accent)}.tag{font-size:12px;color:var(--muted)}
.tablewrap{overflow-x:auto}
footer{color:var(--muted);font-size:12px;line-height:1.5;margin-top:40px;border-top:1px solid var(--line);padding-top:18px}
@media(max-width:560px){.hero{grid-template-columns:1fr}.item{grid-template-columns:72px 1fr}.item img{width:72px;height:72px}.item .cta{grid-column:2}.nav a{margin-left:10px}}
"""


def page(title, body, desc, path_depth=0, canonical=""):
    rel = "../" * path_depth
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://{SITE['domain']}/{canonical}">
<link rel="icon" href="{rel}assets/logo.png">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="https://{SITE['domain']}/assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <a class="brand" href="{rel}"><img src="{rel}assets/logo.png" alt="" width="34" height="34">FIND IT <span>CHEAPER</span></a>
  <nav class="nav"><a href="{rel}weeks/">Past weeks</a><a href="{SITE['tiktok']}">TikTok</a></nav>
</header>
{body}
<footer>Prices were correct when checked and change often, so check the retailer before you buy. As an Amazon Associate, {SITE['name']} earns from qualifying purchases. Some buttons are affiliate links; you pay the same price either way.</footer>
</div>
</body>
</html>
"""


def best_price(prod):
    return min(prod["prices"], key=lambda p: p["price"])


def item_row(slug, prod, depth):
    rel = "../" * depth
    best = best_price(prod)
    return f"""<div class="item">
  <img src="{rel}assets/products/{prod['image']}" alt="{esc(prod['short'])}" loading="lazy" width="96" height="96">
  <div><div class="name"><a href="{rel}products/{slug}/">{esc(prod['name'])}</a></div>
  <div class="sub">{esc(prod.get('badge',''))} · cheapest at {esc(best['store'])}</div>
  <div class="price">{gbp(best['price'])}</div></div>
  <a class="btn cta" href="{rel}products/{slug}/">Compare</a>
</div>"""


def build_week(week, depth):
    rows = "\n".join(item_row(s, DATA["products"][s], depth) for s in week["products"])
    vid = f'<p class="meta">Checked {nice_date(week["date"])}. <a href="{week["video"]}">Watch the video on TikTok</a>.</p>' if week.get("video") else ""
    return f"<h1>{esc(week['title'])}</h1>{vid}<div class=\"list\">{rows}</div>"


def product_page(slug, prod):
    best = best_price(prod)
    rows = []
    for p in sorted(prod["prices"], key=lambda p: p["price"]):
        is_best = p is best
        label = esc(p["store"])
        sub = f'<div class="tag">{esc(p["product"])}</div>' if p.get("product") else ""
        was = f'<s>{gbp(p["was"])}</s>' if p.get("was") else ""
        note = f'<div class="tag">{esc(p["note"])}</div>' if p.get("note") else ""
        rows.append(f'<tr class="{"best" if is_best else ""}"><td>{label}{sub}</td><td class="p">{gbp(p["price"])}{was}{note}</td><td><a class="btn{"" if is_best else " alt"}" href="{store_url(p)}" rel="sponsored nofollow">Go to {label}</a></td></tr>')
    table = "\n".join(rows)
    body = f"""
<h1>{esc(prod['name'])}</h1>
<p class="meta">Prices checked {nice_date(prod['checked'])}</p>
<div class="hero">
  <img src="../../assets/products/{prod['image']}" alt="{esc(prod['name'])}" width="600" height="600">
  <div>
    <span class="pill">{esc(prod.get('badge',''))}</span>
    <p class="lede">{esc(prod['blurb'])}</p>
    <p><strong>Cheapest right now: {esc(best['store'])}, {gbp(best['price'])}</strong></p>
  </div>
</div>
<h2>Price comparison</h2>
<div class="tablewrap"><table><thead><tr><th>Retailer</th><th>Price</th><th></th></tr></thead><tbody>{table}</tbody></table></div>
"""
    title = f"{prod['short']}: cheapest price in the UK"
    desc = f"{prod['name']} compared at {', '.join(sorted(set(p['store'] for p in prod['prices'])))}. Cheapest is {best['store']} at {gbp(best['price'])}, checked {nice_date(prod['checked'])}."
    return page(title, body, desc, 2, f"products/{slug}/")


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(content)


def main():
    weeks = sorted(DATA["weeks"], key=lambda w: w["date"], reverse=True)
    latest = weeks[0]
    urls = [""]
    # home
    intro = f'<p class="lede">{esc(SITE["tagline"])}</p>'
    write("index.html", page(f"{SITE['name']}: what the UK is buying this week", intro + build_week(latest, 0), SITE["tagline"], 0, ""))
    # weeks
    for w in weeks:
        write(f"weeks/{w['date']}/index.html", page(f"{w['title']} ({nice_date(w['date'])})", build_week(w, 2), f"The products from the {nice_date(w['date'])} video, with prices compared.", 2, f"weeks/{w['date']}/"))
        urls.append(f"weeks/{w['date']}/")
    archive = "".join(f'<div class="item" style="grid-template-columns:1fr auto"><div><div class="name"><a href="{w["date"]}/">{esc(w["title"])}</a></div><div class="sub">{nice_date(w["date"])} · {len(w["products"])} products</div></div><a class="btn alt" href="{w["date"]}/">Open</a></div>' for w in weeks)
    write("weeks/index.html", page("Past weeks", f"<h1>Past weeks</h1><div class=\"list\">{archive}</div>", "Every weekly roundup from Find It Cheaper.", 1, "weeks/"))
    urls.append("weeks/")
    # products
    for slug, prod in DATA["products"].items():
        write(f"products/{slug}/index.html", product_page(slug, prod))
        urls.append(f"products/{slug}/")
    # sitemap, robots, CNAME, 404
    sm = "\n".join(f"<url><loc>https://{SITE['domain']}/{u}</loc></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: https://{SITE['domain']}/sitemap.xml\n")
    write("CNAME", SITE["domain"] + "\n")
    write("404.html", page("Page not found", "<h1>Page not found</h1><p class=\"lede\">That one's gone. <a href=\"/\">Back to this week's products.</a></p>", "Page not found", 0, "404.html"))
    print(f"built {len(urls)} pages")


if __name__ == "__main__":
    main()
