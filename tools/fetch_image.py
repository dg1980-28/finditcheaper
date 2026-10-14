#!/usr/bin/env python3
"""Fetch a product image and save it as a 600px square jpg for the site and the video.

Usage: python3 tools/fetch_image.py <slug> <source> [<source> ...]

Each source is either an Amazon ASIN (10 characters, e.g. B0DNG1YCQN) or a direct
image URL. Sources are tried in order; the first one that yields an image wins.
For an ASIN the Amazon UK product page is fetched and its hi-res main image read
from the page. Writes assets/products/<slug>.jpg and video/assets/<slug>.jpg.

Meant to run in GitHub Actions (the cloud sandbox cannot reach Amazon, Argos or
Boots), from the render workflow, when a spec names an image that is not in the
repo yet and carries an "image_sources" list.
"""
import io, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9",
           "Accept": "text/html,application/xhtml+xml,image/avif,image/webp,image/*,*/*;q=0.8"}


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def amazon_image_url(asin):
    html, _ = get(f"https://www.amazon.co.uk/dp/{asin}?th=1")
    html = html.decode("utf-8", "replace")
    if "Robot Check" in html or "api-services-support@amazon.com" in html:
        raise RuntimeError("Amazon returned a robot check")
    m = re.search(r'"hiRes":"(https://m\.media-amazon\.com/images/I/[^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'data-old-hires="(https://m\.media-amazon\.com/images/I/[^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'id="landingImage"[^>]*data-a-dynamic-image="([^"]+)"', html)
    if m:
        dyn = json.loads(m.group(1).replace("&quot;", '"'))
        best = max(dyn.items(), key=lambda kv: kv[1][0] * kv[1][1])[0]
        return re.sub(r"\._[^.]*_\.", "._SL800_.", best)
    m = re.search(r'(https://m\.media-amazon\.com/images/I/[A-Za-z0-9+%-]+)\._[^"]*?\.jpg', html)
    if m:
        return m.group(1) + "._SL800_.jpg"
    raise RuntimeError("no main image found on the Amazon page")


def square(data, size=600):
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.paste(im, (0, 0), im)
    im = bg.convert("RGB")
    # trim near-white borders so the product fills the square
    from PIL import ImageChops
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
    bbox = diff.convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    w, h = im.size
    side = int(max(w, h) * 1.12)
    canvas = Image.new("RGB", (side, side), (255, 255, 255))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2))
    return canvas.resize((size, size), Image.LANCZOS)


def main(slug, sources):
    last = None
    for src in sources:
        try:
            url = amazon_image_url(src) if re.fullmatch(r"[A-Z0-9]{10}", src) else src
            print(f"trying {url}")
            data, ctype = get(url)
            if len(data) < 5000:
                raise RuntimeError(f"too small ({len(data)} bytes, {ctype})")
            im = square(data)
            for out in (os.path.join(ROOT, "assets", "products", f"{slug}.jpg"),
                        os.path.join(ROOT, "video", "assets", f"{slug}.jpg")):
                os.makedirs(os.path.dirname(out), exist_ok=True)
                im.save(out, "JPEG", quality=90)
                print(f"wrote {out}")
            return 0
        except Exception as e:  # try the next source
            last = e
            print(f"  failed: {e}")
    print(f"no image fetched for {slug}: {last}")
    return 1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2:]))
