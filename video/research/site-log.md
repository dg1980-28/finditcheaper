# Site log

One dated entry per morning site-growth run: products added, re-check changes, video candidates, anything that failed.

## 13 Oct 2026

- Products added: none. The cloud sandbox for this run could not reach amazon.co.uk, argos.co.uk, boots.com, superdrug.com or finditcheaper.co.uk (egress proxy rejected every connection: organisation policy), and the WebFetch route needed a permission answer with nobody present. No price can be verified that way, so nothing was added rather than guessing.
- Re-checks: none possible for the same reason. All five existing products still show 11 and 12 Oct prices; four of them (heated throw, Lumie, Kärcher, Shark) are now older than 3 days and need re-checking at the next run that has Amazon access.
- Video candidates: none from Movers & Shakers (not checked, see movers.md). The 12 Oct shortlist in batch2-trending.md still stands; Oral-B iO2 Duo vs Argos is the strongest gap on paper, but the £59.98 price must be re-checked before anything is posted.
- Built: "Deals today" page at /deals.html (every product whose Amazon row has a was price above the current price, biggest saving first, with checked date and note), nav link in the header, sitemap entry. Header now wraps on phones instead of breaking the logo onto two lines. Commit 65f14f2, pushed to main.
- Deploy check: could not fetch the live site from the sandbox (same block), so the 200 checks on / and /deals.html were not done. The "Build and deploy site" workflow run 13 for 65f14f2 completed with success at 06:06 UTC, which is the usual sign the site is live.
- Next run needs Amazon and Argos access to do steps 1 to 3 at all. If the cloud sandbox stays blocked, the task should require David's computer so it can use Chrome there.
