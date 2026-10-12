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
2. Signal for trending: Amazon UK best seller lists (`/gp/bestsellers/beauty/`, `kitchen`, `drugstore`, `electronics`, `home-garden`, `diy`, `lighting`) and the "N+ bought in past month" line on each product page. Movers & Shakers is usually empty for the UK. TikTok's Creative Center needs an ad login and TikTok search is not a trend radar; don't bother.
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

```
python3 tools/build_video.py video/specs/vNN-slug.json videos/vNN-slug.mp4
```
Pull four frames with ffmpeg and look at them before shipping (text clipping, price overlap). Commit the mp4 to `videos/` and push: it must be on the site for the YouTube upload trick to work.

## 4. Captions
Write `video/research/vNN-caption.md`:
- TikTok (max 2 lines of text then tags): hook sentence, prices, "Link on finditcheaper.co.uk. Contains affiliate links." Hashtags: 5 or 6, product-specific plus `#amazonfindsuk #ukdeals #finditcheaper`.
- YouTube title: "<Product>: £X on Amazon vs £Y at <Store>". Description: 3 sentences, the product page URL, "Prices checked <date>. As an Amazon Associate, Find It Cheaper earns from qualifying purchases."

## 5. Deliver and upload
1. Copy the mp4 to the owner's Downloads as `finditcheaper-vNN-<slug>.mp4` (`device_commit_files` from `/mnt/user-data/outputs/`, or `device_bash` copy). If the PC isn't reachable, send the file in chat instead and say so.
2. YouTube (hands-off): in the Chrome tab group open `https://studio.youtube.com`, click Create > Upload videos, then in the page run JS that fetches `https://finditcheaper.co.uk/videos/vNN-slug.mp4`, builds a `File`, sets it on the `input[type=file]` via `DataTransfer` and dispatches `change`. Fill title and description, Not made for kids, add the "Altered content: No" answer, leave visibility on Private and stop. The owner clicks Public and Publish; never click those.
3. TikTok: the web upload page blocks fetch from other domains and the file picker can't be driven. Leave `https://www.tiktok.com/tiktokstudio/upload` open in Chrome, tell the owner the file name, and once he has picked it, type the caption, then each hashtag separately with a one second wait (autocomplete swallows them otherwise), tick "Promotional content" > "Your brand"/"Others' brand" as fits, and let him press Post. Caption edits on a posted video can only be done in the phone app, once a day, within 7 days.
4. Message the owner (SendUserMessage) with: product, prices, what's uploaded, the exact two clicks he has left.

## 6. Rules
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
