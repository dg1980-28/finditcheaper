#!/usr/bin/env python3
"""Tax Hype vertical video builder.

Usage: python3 build_video.py spec.json out.mp4

Spec format:
{
  "voice": "en-gb-southern_english_female-low",
  "scenes": [
    {"type": "hook",    "line1": "...", "line2": "...", "vo": "..."},
    {"type": "product", "num": 1, "name": "...", "image": "assets/x.jpg",
     "price_main": "£25.49", "store_main": "AMAZON", "price_alt": "£60", "store_alt": "ARGOS",
     "badge": "4K+ bought this month", "note": "Runs for pennies an hour", "vo": "..."},
    {"type": "outro",   "line1": "...", "line2": "...", "vo": "..."}
  ]
}
"""
import json, math, os, subprocess, sys, tempfile, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
BG = (11, 11, 18)
ORANGE = (255, 159, 10)
PINK = (255, 45, 85)
WHITE = (255, 255, 255)
GREY = (160, 160, 170)
import os
FONT_DIR = os.environ.get("FIC_FONT_DIR", "/usr/share/fonts/truetype/google-fonts")
VOICE_DIR = os.environ.get("FIC_VOICE_DIR", os.path.expanduser("~/.cache/fic-voices"))


def font(size, weight="Bold"):
    return ImageFont.truetype(f"{FONT_DIR}/Poppins-{weight}.ttf", size)


def lerp(a, b, t):
    return a + (b - a) * t


def ease_out(t):
    return 1 - (1 - t) ** 3


def stripe_bg():
    """Dark background with the brand diagonal stripe, dimmed."""
    base = Image.new("RGB", (W, H), BG)
    stripe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(stripe)
    # gradient band drawn as many thin polygons
    band_h = 520
    cy = H * 0.62
    for i in range(0, W + 400, 4):
        t = i / (W + 400)
        col = tuple(int(lerp(PINK[k], ORANGE[k], t)) for k in range(3)) + (255,)
        x0 = i - 200
        d.polygon([(x0, cy - band_h / 2 + x0 * 0.18), (x0 + 4, cy - band_h / 2 + (x0 + 4) * 0.18),
                   (x0 + 4, cy + band_h / 2 + (x0 + 4) * 0.18), (x0, cy + band_h / 2 + x0 * 0.18)], fill=col)
    stripe = stripe.rotate(0)
    base.paste(stripe, (0, -200), stripe)
    base = base.filter(ImageFilter.GaussianBlur(2))
    # dim the stripe so text reads on top
    dim = Image.new("RGB", (W, H), BG)
    return Image.blend(base, dim, 0.72)


def logo_badge(img):
    """Small TAX HYPE wordmark top-left."""
    d = ImageDraw.Draw(img)
    f = font(34)
    d.rounded_rectangle([48, 60, 48 + 330, 60 + 62], radius=14, fill=(0, 0, 0))
    d.text((48 + 18, 60 + 10), "FIND IT", font=f, fill=WHITE)
    d.text((48 + 18 + 150, 60 + 10), "CHEAPER", font=f, fill=ORANGE)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=f) <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centred(d, lines, f, y, fill, spacing=1.08, shadow=True):
    for ln in lines:
        tw = d.textlength(ln, font=f)
        x = (W - tw) / 2
        if shadow:
            d.text((x + 4, y + 4), ln, font=f, fill=(0, 0, 0))
        d.text((x, y), ln, font=f, fill=fill)
        y += f.size * spacing
    return y


def fit_product(path, box):
    im = Image.open(path).convert("RGB")
    im.thumbnail((box, box), Image.LANCZOS)
    return im


def product_card(prod_img, scale):
    """White rounded card with the product on it, scaled for subtle zoom."""
    card_w, card_h = 880, 880
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, card_w, card_h], radius=48, fill=(255, 255, 255, 255))
    pw, ph = prod_img.size
    s = scale
    pim = prod_img.resize((int(pw * s), int(ph * s)), Image.LANCZOS)
    card.paste(pim, ((card_w - pim.width) // 2, (card_h - pim.height) // 2))
    return card


def render_product(bg, sc, t, dur, prod_img):
    img = bg.copy()
    d = ImageDraw.Draw(img)
    logo_badge(img)
    # intro animation 0.35s
    a = ease_out(min(1, t / 0.35))
    zoom = 0.78 + 0.05 * (t / dur)  # slow push-in
    card = product_card(prod_img, zoom)
    # shadow
    sh = Image.new("RGBA", (card.width + 80, card.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([40, 60, 40 + card.width, 60 + card.height], radius=48, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    cx = (W - card.width) // 2
    cy = int(lerp(620, 540, a))
    img.paste(sh, (cx - 40, cy - 40), sh)
    img.paste(card, (cx, cy), card)

    # number + name (top)
    f_num = font(58)
    f_name = font(78)
    if sc.get("num"):
        num_txt = f"#{sc['num']}"
        d.rounded_rectangle([W / 2 - 70, 170, W / 2 + 70, 250], radius=40, fill=ORANGE)
        d.text((W / 2 - d.textlength(num_txt, font=f_num) / 2, 176), num_txt, font=f_num, fill=(0, 0, 0))
    lines = wrap(d, sc["name"].upper(), f_name, 960)
    draw_centred(d, lines, f_name, 270 if sc.get("num") else 200, WHITE, spacing=1.0)

    # badge pill on the card
    if sc.get("badge"):
        f_b = font(40)
        bw = d.textlength(sc["badge"], font=f_b) + 60
        bx, by = cx + card.width - bw - 24, cy + 24
        d.rounded_rectangle([bx, by, bx + bw, by + 68], radius=34, fill=PINK)
        d.text((bx + 30, by + 10), sc["badge"], font=f_b, fill=WHITE)

    # price block (below card), slides up
    py = int(lerp(1560, 1480, a))
    f_store = font(44, "Medium")
    f_price = font(150)
    f_alt = font(64)
    d.text((W / 2 - d.textlength(sc["store_main"], font=f_store) / 2, py), sc["store_main"], font=f_store, fill=GREY)
    pm = sc["price_main"]
    d.text((W / 2 - d.textlength(pm, font=f_price) / 2, py + 40), pm, font=f_price, fill=ORANGE)
    y2 = py + 215
    if sc.get("price_alt"):
        alt = f"{sc['store_alt']}  {sc['price_alt']}"
        tw = d.textlength(alt, font=f_alt)
        x = W / 2 - tw / 2
        d.text((x, y2), alt, font=f_alt, fill=GREY)
        # strike through the alt price only
        pre = d.textlength(f"{sc['store_alt']}  ", font=f_alt)
        d.line([(x + pre, y2 + 40), (x + tw, y2 + 40)], fill=PINK, width=8)
        y2 += 90
    if sc.get("note"):
        f_n = font(44, "Medium")
        d.text((W / 2 - d.textlength(sc["note"], font=f_n) / 2, y2 + 6), sc["note"], font=f_n, fill=WHITE)
    return img


def render_hook(bg, sc, t, dur):
    img = bg.copy()
    d = ImageDraw.Draw(img)
    logo_badge(img)
    a = ease_out(min(1, t / 0.4))
    f1 = font(118)
    f2 = font(64, "Medium")
    lines = wrap(d, sc["line1"], f1, 940)
    y = int(lerp(760, 640, a))
    y = draw_centred(d, lines, f1, y, WHITE, spacing=1.02)
    if t > 0.5:
        b = ease_out(min(1, (t - 0.5) / 0.4))
        lines2 = wrap(d, sc["line2"], f2, 900)
        draw_centred(d, lines2, f2, y + 40, tuple(int(c * b) for c in ORANGE), spacing=1.1)
    return img


def render_outro(bg, sc, t, dur, logo_path):
    img = bg.copy()
    d = ImageDraw.Draw(img)
    a = ease_out(min(1, t / 0.4))
    logo = Image.open(logo_path).convert("RGBA").resize((520, 520), Image.LANCZOS)
    mask = Image.new("L", logo.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 520, 520], fill=255)
    img.paste(logo, ((W - 520) // 2, int(lerp(560, 480, a))), mask)
    f1 = font(84)
    f2 = font(56, "Medium")
    y = draw_centred(d, wrap(d, sc["line1"], f1, 940), f1, 1090, WHITE, spacing=1.02)
    draw_centred(d, wrap(d, sc["line2"], f2, 900), f2, y + 30, ORANGE)
    f3 = font(34, "Medium")
    d.text((W / 2 - d.textlength(sc.get("small", ""), font=f3) / 2, 1760), sc.get("small", ""), font=f3, fill=GREY)
    return img


ELEVEN_KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
ELEVEN_VOICE = os.environ.get("ELEVENLABS_VOICE", "Lily")   # premade British voices: Lily, Alice, George, Daniel
ELEVEN_MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
_eleven_voice_id = None


def _eleven_voice_id_lookup():
    """Find the voice id by name so we never hard-code an id that might be wrong."""
    global _eleven_voice_id
    if _eleven_voice_id:
        return _eleven_voice_id
    import urllib.request
    if len(ELEVEN_VOICE) >= 20 and " " not in ELEVEN_VOICE:
        _eleven_voice_id = ELEVEN_VOICE  # already an id
        return _eleven_voice_id
    req = urllib.request.Request("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": ELEVEN_KEY})
    voices = json.load(urllib.request.urlopen(req, timeout=30))["voices"]
    for v in voices:
        if v["name"].lower() == ELEVEN_VOICE.lower():
            _eleven_voice_id = v["voice_id"]
            return _eleven_voice_id
    raise SystemExit(f"ElevenLabs voice '{ELEVEN_VOICE}' not found; available: {[v['name'] for v in voices]}")


def tts_eleven(text, out_wav):
    import urllib.request
    vid = _eleven_voice_id_lookup()
    body = json.dumps({"text": text, "model_id": ELEVEN_MODEL,
                       "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "speed": 1.05}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                                 data=body, method="POST",
                                 headers={"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    mp3 = out_wav[:-4] + ".mp3"
    with urllib.request.urlopen(req, timeout=120) as r, open(mp3, "wb") as f:
        f.write(r.read())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ar", "44100", "-ac", "1", out_wav], check=True)


def tts_piper(text, voice, out_wav):
    model = f"{VOICE_DIR}/{voice}.onnx"
    subprocess.run(["python3", "-m", "piper", "-m", model, "-f", out_wav, "--length-scale", "0.92"],
                   input=text.encode(), check=True, capture_output=True)


def tts(text, voice, out_wav):
    """ElevenLabs when ELEVENLABS_API_KEY is set (the slick voice), otherwise the offline piper voice."""
    if ELEVEN_KEY:
        tts_eleven(text, out_wav)
    else:
        tts_piper(text, voice, out_wav)
    with wave.open(out_wav) as w:
        return w.getnframes() / w.getframerate()


def main(spec_path, out_path):
    spec = json.load(open(spec_path))
    voice = spec.get("voice", "en-gb-southern_english_female-low")
    tmp = tempfile.mkdtemp(prefix="taxhype_")
    bg = stripe_bg()

    # 1. voiceover per scene, derive durations
    pad = spec.get("pad", 0.6)
    wavs, durs = [], []
    for i, sc in enumerate(spec["scenes"]):
        wv = f"{tmp}/vo{i}.wav"
        dur = tts(sc["vo"], voice, wv)
        wavs.append(wv)
        durs.append(max(sc.get("min", 2.2), dur + pad))

    # 2. concatenate audio with silence padding so audio lines up with scenes
    concat_list = f"{tmp}/alist.txt"
    with open(concat_list, "w") as f:
        for i, (wv, dur) in enumerate(zip(wavs, durs)):
            padded = f"{tmp}/vo{i}_p.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wv, "-af", f"apad=whole_dur={dur}",
                            "-t", str(dur), padded], check=True)
            f.write(f"file '{padded}'\n")
    audio = f"{tmp}/vo_all.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", audio], check=True)

    # 3. frames -> ffmpeg via pipe
    total_frames = sum(int(round(d * FPS)) for d in durs)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    logo_path = spec.get("logo", "assets/logo.png")
    done = 0
    for sc, dur in zip(spec["scenes"], durs):
        n = int(round(dur * FPS))
        prod_img = fit_product(sc["image"], 760) if sc["type"] == "product" else None
        for k in range(n):
            t = k / FPS
            if sc["type"] == "hook":
                fr = render_hook(bg, sc, t, dur)
            elif sc["type"] == "product":
                fr = render_product(bg, sc, t, dur, prod_img)
            else:
                fr = render_outro(bg, sc, t, dur, logo_path)
            # fade in/out 0.25s
            if t < 0.25 or t > dur - 0.25:
                k_f = min(t, dur - t) / 0.25
                fr = Image.blend(Image.new("RGB", (W, H), BG), fr, max(0, min(1, k_f)))
            p.stdin.write(fr.tobytes())
        done += n
        print(f"scene done: {sc['type']} {dur:.1f}s", file=sys.stderr)
    p.stdin.close()
    p.wait()
    print(f"wrote {out_path}: {total_frames / FPS:.1f}s, {total_frames} frames")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
