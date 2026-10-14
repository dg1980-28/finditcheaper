# Site log

One dated entry per morning site-growth run: products added, re-check changes, video candidates, anything that failed.

## 13 Oct 2026

- Products added: none. The cloud sandbox for this run could not reach amazon.co.uk, argos.co.uk, boots.com, superdrug.com or finditcheaper.co.uk (egress proxy rejected every connection: organisation policy), and the WebFetch route needed a permission answer with nobody present. No price can be verified that way, so nothing was added rather than guessing.
- Re-checks: none possible for the same reason. All five existing products still show 11 and 12 Oct prices; four of them (heated throw, Lumie, Kärcher, Shark) are now older than 3 days and need re-checking at the next run that has Amazon access.
- Video candidates: none from Movers & Shakers (not checked, see movers.md). The 12 Oct shortlist in batch2-trending.md still stands; Oral-B iO2 Duo vs Argos is the strongest gap on paper, but the £59.98 price must be re-checked before anything is posted.
- Built: "Deals today" page at /deals.html (every product whose Amazon row has a was price above the current price, biggest saving first, with checked date and note), nav link in the header, sitemap entry. Header now wraps on phones instead of breaking the logo onto two lines. Commit 65f14f2, pushed to main.
- Deploy check: could not fetch the live site from the sandbox (same block), so the 200 checks on / and /deals.html were not done. The "Build and deploy site" workflow run 13 for 65f14f2 completed with success at 06:06 UTC, which is the usual sign the site is live.
- Next run needs Amazon and Argos access to do steps 1 to 3 at all. If the cloud sandbox stays blocked, the task should require David's computer so it can use Chrome there.

## 14 Oct 2026

- Products added: none. amazon.co.uk is blocked two ways from this cloud run: the sandbox egress proxy refuses the connection (organisation policy, same as 13 Oct) and WebFetch refuses every amazon.co.uk address because Amazon's robots.txt disallows it. So no Amazon price, was price, "bought in past month" count or SL800 image could be read for any product, and nothing was added rather than guessing. The same applies to m.media-amazon.com, so images could not be saved either.
- Re-checks: no Amazon prices could be re-checked, so the five existing products keep their 11 and 12 Oct Amazon prices and "checked" dates (all now older than 3 days apart from Medicube, which turns 3 days old today). Partial good news: argos.co.uk does work through WebFetch when the address comes from a web search result. The Argos search page for Lumie still lists the Lumie Sunrise Alarm Clock at £49.00 today, matching the Argos row on the site. The Kärcher and Shark Argos pages loaded without prices (the search results and product prices load after the page, so the fetch only saw the menu), and the Silentnight heated throw product page returned an error. Argos prices were not changed on the site because the matching Amazon price could not be confirmed on the same day.
- Video candidates: none from Movers & Shakers (not reachable, see movers.md).
- Deals page: already built on 13 Oct. Confirmed tools/build_site.py generates deals.html (Amazon rows with a was price above the current price, biggest saving first, with checked date and note), the header nav link and the sitemap entry. Running the build today changed nothing.
- Deploy check: finditcheaper.co.uk and dg1980-28.github.io are both blocked from the sandbox and not indexed by the search tool, so the 200 checks were not done directly. The GitHub API shows the "Build and deploy site" workflow for yesterday's commit afd1f4d completed with success at 06:07 UTC on 13 Oct.
- What would unblock this: the task needs either a run that requires David's computer (Chrome there can open Amazon, Argos, Boots and Superdrug with cookies accepted), or amazon.co.uk and m.media-amazon.com allowed on the organisation's egress list. Amazon's robots.txt means WebFetch will never be the route for Amazon pages. Argos via WebFetch is usable for competitor checks once Amazon prices are available.
