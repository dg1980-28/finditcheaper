#!/usr/bin/env python3
"""Read Amazon UK Movers & Shakers, best seller lists and product pages, and write
the result as JSON for the morning site-growth run.

Usage: python3 tools/scrape_amazon.py <out.json> [--images DIR] [--max-products N] [--browser] [--budget-seconds S] [ASIN ...]

--browser reads product pages through headless Chromium (Playwright), which Amazon
robot-checks far less than plain requests from a runner.

Meant to run in GitHub Actions (the cloud sandbox cannot reach amazon.co.uk). The
workflow commits <out.json> and the images back to the repo so the sandbox can read
them. Prices are copied from the page exactly as shown; nothing is inferred.

Output shape:
  {"date": "...", "movers": {category: {"status": "ok|empty|robot|error", "items": [...]}},
   "bestsellers": {category: {...}}, "products": {asin: {...}}}
Each list item: rank, asin, name, price, percent (movers only), text (the item's
visible text, for checking by hand). Each product: title, price, was, savings_pct,
bought, availability, deal, deal_ends, sold_by, badge, rating, ratings, image,
image_saved, prices_seen (every price string in the price block, in order).
"""
import datetime, json, os, re, sys, time, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_image  # noqa: E402  (same folder)

BASE = "https://www.amazon.co.uk"
MOVERS = ["", "beauty", "kitchen", "drugstore", "home-garden", "electronics", "diy",
          "lighting", "sports", "pet-supplies"]
BESTSELLERS = ["beauty", "drugstore", "kitchen", "home-garden", "diy", "lighting",
               "electronics", "sports", "pet-supplies"]
DELAY = 1.5


BROWSER = {"page": None}


def is_robot(html):
    return ("Robot Check" in html or "api-services-support@amazon.com" in html
            or "Enter the characters you see below" in html
            or "Sorry, we just need to make sure you're not a robot" in html)


def start_browser():
    """Headless Chromium with a persistent session: Amazon serves product pages to a
    real browser far more reliably than to plain requests from a runner IP."""
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    args = ["--disable-blink-features=AutomationControlled"]
    try:  # full Chrome for Testing in new headless mode looks like a normal browser
        browser = pw.chromium.launch(headless=True, channel="chromium", args=args)
    except Exception:
        browser = pw.chromium.launch(headless=True, args=args)
    ctx = browser.new_context(
        user_agent=fetch_image.UA, locale="en-GB", timezone_id="Europe/London",
        viewport={"width": 1366, "height": 900},
        extra_http_headers={"Accept-Language": "en-GB,en;q=0.9"})
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page = ctx.new_page()
    page.goto(BASE + "/", wait_until="domcontentloaded", timeout=60000)
    time.sleep(2)
    for sel in ("#sp-cc-accept", "input#sp-cc-accept", "button:has-text('Accept')"):
        try:
            page.locator(sel).first.click(timeout=3000)
            break
        except Exception:
            pass
    time.sleep(1.5)
    BROWSER["page"] = page
    BROWSER["page_keep"] = page
    BROWSER["pw"] = pw
    return page


def browser_get(url, tries=2):
    page = BROWSER["page"]
    last = None
    for i in range(tries):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(2.5)
            html = page.content()
            if is_robot(html):
                last = "robot"
                if i + 1 < tries:
                    time.sleep(15)
                continue
            if "productTitle" not in html and "/dp/" in url:
                # sometimes a continue/interstitial page; one more try
                last = "no product title"
                time.sleep(5)
                continue
            return html, None
        except Exception as e:
            last = f"{type(e).__name__}: {e}"[:120]
            time.sleep(5)
    return None, last


def get(url, tries=3):
    if BROWSER["page"] is not None:
        return browser_get(url, tries)
    last = None
    for i in range(tries):
        try:
            data, _ = fetch_image.get(url, timeout=40)
            html = data.decode("utf-8", "replace")
            if is_robot(html):
                last = "robot"
                time.sleep(4 + 3 * i)
                continue
            return html, None
        except urllib.error.HTTPError as e:
            last = f"http {e.code}"
            if e.code in (404, 410):
                break
            time.sleep(4 + 3 * i)
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(3)
    return None, last


def text(html):
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = html.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'") \
               .replace("&nbsp;", " ").replace("&pound;", "£").replace("&#163;", "£")
    return re.sub(r"\s+", " ", html).strip()


def block(html, start_pat, length=6000):
    m = re.search(start_pat, html)
    if not m:
        return ""
    start = html.rfind("<", 0, m.start())
    return html[max(start, 0):m.start() + length]


def parse_list(html):
    items = []
    parts = re.split(r'id="gridItemRoot"', html)[1:]
    if not parts:
        parts = re.split(r'class="zg-grid-general-faceout"', html)[1:]
    for p in parts:
        p = p[:12000]
        asin = re.search(r"/dp/([A-Z0-9]{10})", p)
        if not asin:
            continue
        t = text(p)
        name = re.search(r'alt="([^"]{8,})"', p)
        price = re.search(r"£\s?([\d,]+\.\d\d)", t)
        pct = re.search(r"([+-]?[\d,]+)\s?%", t)
        rank = re.search(r"#(\d+)", t)
        bought = re.search(r"([\d,]+K?\+?) bought in past month", t)
        rating = re.search(r"(\d\.\d) out of 5 stars", t)
        img = re.search(r'src="(https://[^"]+/images/I/([A-Za-z0-9+%-]+)\.[^"]*\.jpg)"', p)
        items.append({
            "image": f"https://m.media-amazon.com/images/I/{img.group(2)}._SL800_.jpg" if img else None,
            "rank": int(rank.group(1)) if rank else None,
            "asin": asin.group(1),
            "name": (name.group(1) if name else "").replace("&amp;", "&").replace("&quot;", '"'),
            "price": float(price.group(1).replace(",", "")) if price else None,
            "percent": int(pct.group(1).replace(",", "").replace("+", "")) if pct else None,
            "bought": bought.group(1) if bought else None,
            "rating": float(rating.group(1)) if rating else None,
            "text": t[:300],
        })
    return items


def fetch_list(path):
    html, err = get(BASE + path)
    if html is None:
        return {"status": err or "error", "items": []}
    items = parse_list(html)
    if not items:
        t = text(html)
        return {"status": "empty", "items": [], "text": t[:400]}
    return {"status": "ok", "items": items}


def money(s):
    m = re.search(r"£\s?([\d,]+(?:\.\d\d)?)", s or "")
    return float(m.group(1).replace(",", "")) if m else None


def parse_product(asin, html):
    d = {"asin": asin}
    m = re.search(r'id="productTitle"[^>]*>(.*?)</span>', html, re.S)
    d["title"] = text(m.group(1)) if m else None
    core = block(html, r'id="corePriceDisplay_desktop_feature_div"|id="corePrice_feature_div"|id="corePrice_desktop"', 12000)
    if not core:
        core = block(html, r'id="apex_desktop"', 15000)
    seen = re.findall(r'class="a-offscreen">\s*(£[\d,]+\.?\d*)', core)
    d["prices_seen"] = seen
    m = re.search(r'(?:priceToPay|apexPriceToPay|a-price-whole)[^£]*?class="a-offscreen">\s*(£[\d,]+\.?\d*)', core, re.S)
    if m:
        d["price"] = money(m.group(1))
    elif seen:
        d["price"] = money(seen[0])
    else:
        m = re.search(r'id="priceblock_(?:deal|our|sale)price"[^>]*>\s*(£[\d,.]+)', html)
        d["price"] = money(m.group(1)) if m else None
    m = re.search(r'a-text-price[^>]*>\s*<span class="a-offscreen">\s*(£[\d,]+\.?\d*)', core)
    d["was"] = money(m.group(1)) if m else None
    m = re.search(r'savingsPercentage[^>]*>\s*-?(\d+)%', core)
    d["savings_pct"] = int(m.group(1)) if m else None
    ct = text(core)
    d["price_text"] = ct[:300]
    full = text(html)
    m = re.search(r"([\d,]+K?\+?) bought in past month", full)
    d["bought"] = m.group(1) if m else None
    av = block(html, r'id="availability"', 1500)
    d["availability"] = text(av)[:120] if av else None
    m = re.search(r"Only (\d+) left in stock", full)
    d["low_stock"] = int(m.group(1)) if m else None
    deal = block(html, r'id="dealBadge[^"]*"|class="dealBadge[^"]*"', 1500)
    d["deal"] = text(deal)[:80] if deal else None
    ends = re.findall(r"((?:Deal e|E)nds in[^.]{0,60}|Ends [A-Z][a-z]+ \d+ [A-Z][a-z]+[^.]{0,30})", full)
    d["deal_ends"] = ends[:3]
    sellers = re.findall(r'offer-display-feature-text-message">\s*(?:<[^>]+>\s*)*([^<]{2,60})', html)
    d["sold_by"] = [text(s) for s in sellers][:3]
    bd = block(html, r'id="zeitgeistBadge_feature_div"', 1500)
    d["badge"] = text(bd)[:100] if bd else None
    m = re.search(r"(\d\.\d) out of 5 stars", full)
    d["rating"] = float(m.group(1)) if m else None
    m = re.search(r'id="acrCustomerReviewText"[^>]*>\s*([\d,]+)', html)
    d["ratings"] = int(m.group(1).replace(",", "")) if m else None
    m = re.search(r"Best Sellers Rank[^#]{0,40}(#[\d,]+ in [^(]{3,60})", full)
    d["rank"] = m.group(1).strip() if m else None
    m = re.search(r'"hiRes":"(https://m\.media-amazon\.com/images/I/[^"]+)"', html) \
        or re.search(r'data-old-hires="(https://m\.media-amazon\.com/images/I/[^"]+)"', html)
    d["image"] = m.group(1) if m else None
    d["checked"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return d


def fetch_product(asin, images):
    html, err = get(f"{BASE}/dp/{asin}?th=1&psc=1")
    if html is None and BROWSER["page"] is not None:
        BROWSER["page"] = None  # try once without the browser, then put it back
        html, err = get(f"{BASE}/dp/{asin}?th=1&psc=1")
        BROWSER["page"] = BROWSER.get("page_keep")
    if html is None:
        return {"asin": asin, "status": err or "error"}
    d = parse_product(asin, html)
    d["status"] = "ok"
    if images and d.get("image"):
        try:
            data, _ = fetch_image.get(d["image"])
            os.makedirs(images, exist_ok=True)
            out = os.path.join(images, f"{asin}.jpg")
            fetch_image.square(data).save(out, "JPEG", quality=90)
            d["image_saved"] = out
        except Exception as e:
            d["image_saved"] = None
            d["image_error"] = str(e)
    return d


def main(argv):
    out = argv[0]
    images, max_products, extra, use_browser, budget = None, 60, [], False, 1500
    i = 1
    while i < len(argv):
        if argv[i] == "--images":
            images = argv[i + 1]; i += 2
        elif argv[i] == "--browser":
            use_browser = True; i += 1
        elif argv[i] == "--budget-seconds":
            budget = int(argv[i + 1]); i += 2
        elif argv[i] == "--max-products":
            max_products = int(argv[i + 1]); i += 2
        else:
            extra.append(argv[i]); i += 1
    res = {"date": datetime.date.today().isoformat(), "movers": {}, "bestsellers": {}, "products": {}}
    for c in MOVERS:
        res["movers"][c or "all"] = fetch_list(f"/gp/movers-and-shakers/{c}/" if c else "/gp/movers-and-shakers/")
        print("movers", c or "all", res["movers"][c or "all"]["status"], len(res["movers"][c or "all"]["items"]))
        time.sleep(DELAY)
    for c in BESTSELLERS:
        res["bestsellers"][c] = fetch_list(f"/gp/bestsellers/{c}/")
        print("bestsellers", c, res["bestsellers"][c]["status"], len(res["bestsellers"][c]["items"]))
        time.sleep(DELAY)
    # product pages: the ASINs given on the command line first (existing products),
    # then movers climbers, then best sellers round-robin by category
    queue = list(extra)
    for c in MOVERS:
        for it in res["movers"][c or "all"]["items"][:10]:
            queue.append(it["asin"])
    cols = [[it["asin"] for it in res["bestsellers"][c]["items"][:12]] for c in BESTSELLERS]
    for row in range(12):
        for col in cols:
            if row < len(col):
                queue.append(col[row])
    seen = set()
    todo = [a for a in queue if not (a in seen or seen.add(a))][:max_products]
    if use_browser:
        try:
            start_browser()
            print("browser started")
        except Exception as e:
            print("browser failed to start, falling back to plain requests:", e)
    def save():
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w") as f:
            json.dump(res, f, indent=1, ensure_ascii=False)
    save()
    t0 = time.time()
    for a in todo:
        if time.time() - t0 > budget:
            print("time budget used up, stopping product pages", flush=True)
            res["stopped_early"] = True
            break
        res["products"][a] = fetch_product(a, images)
        p = res["products"][a]
        print("product", a, p.get("status"), p.get("price"), p.get("was"), p.get("bought"), (p.get("title") or "")[:50], flush=True)
        save()  # keep what we have if the job is cut short
        time.sleep(DELAY)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
