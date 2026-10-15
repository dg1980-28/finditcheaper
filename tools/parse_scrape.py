#!/usr/bin/env python3
"""Read the price block out of the page text saved by scrape_amazon.py.

Usage: python3 tools/parse_scrape.py video/research/scrape/<date>.json [ASIN ...]

Prints one line per product: price, RRP or was price, savings, bought count, deal
badge, deal end, stock line. Amazon's visible text goes
"N+ bought in past month £8.11 with 37 percent savings -37% £ 8 . 11 ... RRP: £12.99",
so the numbers are read from that run of text and nothing is computed.
"""
import json, re, sys


def parse_text(t):
    d = {}
    head = t[:60000]
    m = re.search(r"([\d,]+K?\+?) bought in past month", head)
    d["bought"] = m.group(1) if m else None
    start = m.end() if m else 0
    seg = head[start:start + 1500]
    m = re.search(r"£(\d[\d,]*\.\d\d) with (\d+) percent savings", seg)
    if m:
        d["price"] = float(m.group(1).replace(",", ""))
        d["savings_pct"] = int(m.group(2))
    else:
        m = re.search(r"£ ?(\d[\d,]*) \. (\d\d)", seg) or re.search(r"£(\d[\d,]*\.\d\d)", seg)
        if m:
            d["price"] = float((m.group(1) + "." + m.group(2)).replace(",", "")) if m.lastindex == 2 else float(m.group(1).replace(",", ""))
        else:
            d["price"] = None
        d["savings_pct"] = None
    m = re.search(r"(RRP|Was|List Price|Typical price):? ?£(\d[\d,]*\.\d\d)", seg)
    d["was"] = float(m.group(2).replace(",", "")) if m else None
    d["was_kind"] = m.group(1) if m else None
    d["deal"] = "Limited time deal" if "Limited time deal" in seg else ("Deal" if re.search(r"\bDeal\b", seg[:300]) else None)
    m = re.search(r"Ends in (\d+) hours? (\d+) minutes?", head)
    d["deal_ends"] = f"{m.group(1)}h {m.group(2)}m" if m else None
    m = re.search(r"Only (\d+) left in stock", head)
    d["low_stock"] = int(m.group(1)) if m else None
    for s in ("Currently unavailable", "Temporarily out of stock", "In stock"):
        if s in head:
            d["stock"] = s
            break
    else:
        d["stock"] = None
    m = re.search(r"Sold by:? ([A-Za-z0-9+&' .-]{2,40}?)(?: Returns| This| Dispatch| Payment| Gift| <|$)", head)
    d["sold_by"] = m.group(1).strip() if m else None
    m = re.search(r"#(\d[\d,]*) in ([A-Za-z &]+?) \(", head)
    d["rank"] = f"#{m.group(1)} in {m.group(2)}" if m else None
    m = re.search(r"(#1 Best Seller|Amazon's Choice|Overall Pick)", head)
    d["badge"] = m.group(1) if m else None
    return d


def main(path, asins):
    data = json.load(open(path))
    out = {}
    for a, p in data["products"].items():
        if asins and a not in asins:
            continue
        if p.get("status") != "ok" or not p.get("page_text"):
            print(a, p.get("status"))
            continue
        r = parse_text(p["page_text"])
        r["title"] = p.get("title")
        r["checked"] = p.get("checked")
        out[a] = r
        print(a, r["price"], r["was"], r["was_kind"], r["savings_pct"], r["bought"], r["deal"], r["deal_ends"], r["low_stock"], r["stock"], r["sold_by"], "|", (r["title"] or "")[:50])
    return out


if __name__ == "__main__":
    main(sys.argv[1], set(sys.argv[2:]))
