# Find It Cheaper: daily runbook

Everything needed to produce one product video a day and keep finditcheaper.co.uk current, from a fresh session. Follow it top to bottom.

## What this is
- Brand: Find It Cheaper. Trending UK products and where they're cheapest. The owner stays anonymous; never put his name anywhere.
- Site: https://finditcheaper.co.uk (GitHub Pages from this repo, `dg1980-28/finditcheaper`, branch `main`; a push to main rebuilds and deploys in about a minute).
- TikTok: @taxhype2027 (display name changes to Find It Cheaper after 18 Oct 2026, username to @finditcheaperuk after 10 Nov 2026).
- YouTube: Find It Cheaper channel, logged in through Chrome on the owner's PC.
- Amazon Associates tag: `taxhype-21`. Link format `https://www.amazon.co.uk/dp/ASIN?tag=taxhype-21`.
- Owner's PC paths: videos go to `C:\Users\user\Downloads\`.

## 0. Setup (every fresh session)
```
git clone https://github.com/dg1980-28/finditcheaper.git && cd finditcheaper
bash tools/setup_video_env.sh      # piper voice, fonts, ffmpeg check
```
Commit as `Claude <noreply@anthropic.com>`.

## 1. Pick today's product
1. Read `video/research/*.md` for the current shortlist and what has already been posted. `data/products.json` lists every product already on the site, and each has `video` if it has been posted.
2. From the cloud sandbox, Amazon is unreachable (egress block, and robots.txt stops WebFetch). Read it from GitHub Actions instead: edit `video/research/scrape/request.json` (`asins` to read, `max_products`, `no_lists` to skip the list pages) and push it; the "Scrape Amazon" workflow (`tools/scrape_amazon.py`, headless Chromium with a London delivery address) commits `video/research/scrape/<date>.json` and 600px images under `video/research/scrape/images/` within about 10 to 20 minutes. Then `python3 tools/parse_scrape.py video/research/scrape/<date>.json` prints price, RRP or was, savings, bought count and deal end per ASIN. If a run reports `location_ok: false` the prices are ex VAT or USD; push the request again after a 15 minute pause rather than using them. If a run comes back with `robot` on nearly every product page (17 Oct: two runs in a row, even with pauses), add `"headed": true, "channel": "chrome", "no_lists": true` to the request: the workflow then runs the runner's Google Chrome as a visible window under xvfb, which Amazon served without a single robot check (24 product pages in 4 minutes) when both headless modes were blocked. Keep `no_lists` on for that rerun; the plain request list pages are what trips the robot checks first. Competitor prices: Superdrug and Currys product pages give prices through WebFetch (find the URL with a web search first); Argos, Boots and B&Q product pages do not.
   First check Amazon Movers & Shakers (`https://www.amazon.co.uk/gp/movers-and-shakers/` and the per-category pages, e.g. `/gp/movers-and-shakers/beauty/`). It lists the biggest 24 hour sales rank climbers with a percentage. It is often empty from the sandbox; if it loads in a browser tab with cookies accepted, anything up 500% or more with 1K+ bought is the day's video candidate, and the climbers go in the log. Then the signal for trending: Amazon UK best seller lists (`/gp/bestsellers/beauty/`, `kitchen`, `drugstore`, `electronics`, `home-garden`, `diy`, `lighting`) and the "N+ bought in past month" line on each product page. Movers & Shakers is usually empty for the UK. TikTok's Creative Center needs an ad login and TikTok search is not a trend radar; don't bother.
3. Weight towards beauty and household (highest Amazon commission and biggest counts). Avoid Amazon's own devices unless the deal is huge, because every retailer matches those prices.
4. The best videos have a price gap: Amazon vs Argos, Boots, Superdrug, Currys or B&Q. Check the competitor the same day. Boots and Superdrug block plain fetches; load the page in a browser tab (`https://www.boots.com/sitesearch?searchTerm=...`, `https://www.argos.co.uk/search/<words-with-dashes>/`) and read the text. Argos in-page fetch is bot-blocked; navigate to each search instead.
5. Re-check the Amazon price on the day. Deal prices (especially around Prime Day and Black Friday) move.

## 2. Add the product to the site
Edit `data/products.json`:
- `products.<slug>`: `name`, `short`, `image` (file in `assets/products/`, 600px square jpg, from the Amazon listing's SL800 image), `blurb` (2 to 3 plain sentences, British English, no dashes), `badge` ("40K+ bought this month"), `checked` (ISO date), `prices` (list of `{store, price, was?, asin|url, product?, note?}`). Cheapest row is highlighted automatically.
- Copy the image to `video/assets/<slug>.jpg` as well for the video.
- Optionally add a `weeks[]` entry for a roundup; single-product videos don't need one.
Then `python3 tools/build_site.py`, commit, push. Check `https://finditcheaper.co.uk/products/<slug>/` loads after the deploy.

## 3. Render the video
Write `video/specs/vNN-<slug>.json` using `video/specs/v03-medicube.json` as the template:
- `hook`: two lines, the number first ("40,000 people bought this on Amazon this month") then the price angle.
- Two `product` scenes: the product with `store_main`/`price_main` and `store_alt`/`price_alt` (WAS price, then the competitor). `badge` is the social proof, `note` one short fact.
- `outro`: "Link on the site" / "finditcheaper.co.uk", `small` = "Prices checked D Mon YYYY. Contains affiliate links."
- `vo` lines are what piper reads. Write numbers as words ("sixteen ninety"), spell out initialisms with spaces ("P D R N"). Keep total length 25 to 35 seconds; `pad` 0.4.
- Claims must match what was checked. Never say "same thing" about a different model; say "vs Silentnight at Argos".

Rendering happens in GitHub Actions (`.github/workflows/render.yml`), because the ElevenLabs API is blocked from the cloud sandbox but not from GitHub. Commit and push the spec; the "Render video" workflow renders `videos/vNN-slug.mp4` with the ElevenLabs voice (repo secret `ELEVENLABS_API_KEY`, voice name in repo variable `ELEVENLABS_VOICE`, default Lily) and commits the mp4 back within about 3 minutes. Poll `https://api.github.com/repos/dg1980-28/finditcheaper/actions/runs?per_page=3` until the run is complete, then `git pull`. If the workflow fails or the secret isn't set yet, render locally with the offline voice instead:
```
bash tools/setup_video_env.sh
python3 tools/build_video.py video/specs/vNN-slug.json videos/vNN-slug.mp4
```
Either way, pull four frames with ffmpeg and look at them before shipping (text clipping, price overlap), and make sure the mp4 is pushed to `videos/`: it must be on the site for the YouTube upload trick to work.

## 4. Captions
Write `video/research/vNN-caption.md`:
- TikTok (max 2 lines of text then tags): hook sentence, prices, "Link on finditcheaper.co.uk. Contains affiliate links." Hashtags: 5 or 6, product-specific plus `#amazonfindsuk #ukdeals #finditcheaper`.
- YouTube title: "<Product>: £X on Amazon vs £Y at <Store>". Description: 3 sentences, the product page URL, "Prices checked <date>. As an Amazon Associate, Find It Cheaper earns from qualifying purchases."

## 5. Deliver and upload
1. Copy the mp4 to the owner's Downloads as `finditcheaper-vNN-<slug>.mp4` (`device_commit_files` from `/mnt/user-data/outputs/`, or `device_bash` copy). If the PC isn't reachable, send the file in chat instead and say so.
2. YouTube (hands-off): in the Chrome tab group open `https://studio.youtube.com`, click Create > Upload videos, then in the page run JS that fetches `https://finditcheaper.co.uk/videos/vNN-slug.mp4`, builds a `File`, puts it in a `DataTransfer` and dispatches `dragenter`, `dragover` and `drop` DragEvents carrying it on the `ytcp-uploads-dialog` element (the dialog has no `input[type=file]` any more; the drop started the upload first time on 23 Oct). Fill title and description, Not made for kids, add the "Altered content: No" answer, leave visibility on Private and stop. The owner clicks Public and Publish; never click those.
3. TikTok: the web upload page blocks fetch from other domains and the file picker can't be driven. Leave `https://www.tiktok.com/tiktokstudio/upload` open in Chrome, tell the owner the file name, and once he has picked it, type the caption, then each hashtag separately with a one second wait (autocomplete swallows them otherwise), tick "Promotional content" > "Your brand"/"Others' brand" as fits, and let him press Post. Caption edits on a posted video can only be done in the phone app, once a day, within 7 days.
4. Message the owner (SendUserMessage) with: product, prices, what's uploaded, the exact two clicks he has left.

## 6. Rules
- Urgency is allowed when it's true, and it helps: "limited time deal", "was £160 last week", "5,000 bought this month", "only 3 left" when Amazon shows that, "clocks go back Sunday". Lead with the number. Never invent scarcity or a fake countdown; UK law (DMCC Act 2024) bans fake urgency and Amazon closes Associate accounts for it. If Amazon shows a deal end time, put "ends <day>" on screen and in the caption.
- Prices in GBP, British English, no dashes in any text or captions.
- One video a day, posted 6 to 9pm UK. Don't stack two in a day.
- Never fabricate a competitor price. If no competitor was found, do a "was/now" deal angle and say so.
- Affiliate disclosure on every post and every page.
- Don't change DNS, GitHub Pages settings, TikTok account settings, or click Publish/Post. Those are the owner's.
- If something can't be verified (out of stock, price changed, site deploy failed), say exactly that in the message and leave the step undone rather than guessing.

## Growth backlog (not daily)
- Awin application once ~20 product pages exist (Argos, Currys, Boots, B&Q links).
- Cross-post Shorts to Instagram Reels (@finditcheaperuk) once the account exists.
- Weekly roundup video on Sundays from the week's five products.
- "Deals today" page on the site listing every product currently on a Limited Time Deal.
