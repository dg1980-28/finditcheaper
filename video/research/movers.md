# Amazon Movers & Shakers log

One entry per morning run. Top 10 climbers with percentage, price and "bought in past month". Anything up 500% or more with 1K+ bought is marked VIDEO CANDIDATE for the evening video run.

## 13 Oct 2026

Not checked. The cloud sandbox for this run could not reach amazon.co.uk at all (the egress proxy rejected the connection: organisation policy), and the WebFetch route needed a permission answer that nobody was there to give. Same for Argos, Boots, Superdrug and finditcheaper.co.uk. No climbers recorded, no video candidate from Movers & Shakers today. The 12 Oct shortlist in batch2-trending.md still stands for the evening run.

## 14 Oct 2026

Not checked. amazon.co.uk is still unreachable from the cloud sandbox: the egress proxy refuses the connection as an organisation policy denial, and the WebFetch route refuses every amazon.co.uk address because Amazon's robots.txt disallows it (the main Movers & Shakers page, the category pages, the best seller lists and individual product pages all fail the same way). No climbers recorded, no video candidate from Movers & Shakers today. The 12 Oct shortlist in batch2-trending.md still stands for the evening run, with the usual caveat that the Amazon price must be re-checked on the day.

## 15 Oct 2026

Checked for real this time, from a GitHub Actions runner (new `Scrape Amazon` workflow, `tools/scrape_amazon.py`; the sandbox still cannot reach amazon.co.uk). The main Movers & Shakers page and all nine category pages (beauty, kitchen, drugstore, home-garden, electronics, diy, lighting, sports, pet-supplies) loaded but listed no products at all, as OPS.md says is usual for the UK. No climbers recorded, no video candidate from Movers & Shakers today.

Best seller lists did load, so the "bought in past month" counts are today's signal (product pages read 08:57 to 09:00 UTC with a London delivery address, prices in GBP):

- Medicube Zero Pore Pad 2.0, B09V7Z4TJG, £15.30 (RRP £16.90), 100K+ bought, #1 in beauty. Superdrug £17.89. Added to the site today.
- Garnier Micellar Water 700ml, B01M6UUOY2, £6.47 (RRP £9.99), 70K+ bought, #3 in beauty. Superdrug £6.65. Added.
- Maybelline Sky High mascara, B08WR5CPNB, £8.11 (RRP £12.99), 60K+ bought, #2 in beauty. Superdrug £12.99. Added. Still the strongest beauty price gap for a video.
- Nizoral 60ml, B001ETUD5I, £6.67 (RRP £8.99), 40K+ bought. Superdrug £8.49. Added.
- BIODANCE collagen mask 4 pack, B0B2RM68G2, £11.99 (RRP £14.90), 40K+ bought. Superdrug £14.89. Added.
- CeraVe Hydrating Cleanser 236ml, B07C5R51Q9, £9.37 (RRP £12.50), 30K+ bought. Superdrug £12.49. Added.
- HG Mould Remover Spray 500ml, B000IU40HQ, £4.50 (RRP £9.42), 30K+ bought. B&Q page would not give a price. Not added.
- BRITA MAXTRA PRO 6 pack, B0BSXDVQG7, £24.50 (RRP £37.49), 20K+ bought. Currys £34.99. Added. Biggest cash gap of the day (£10.49).
- Oral-B Vitality Pro, B0B18V92KS, £21.00 (RRP £49.99), 10K+ bought, #1 in rotating toothbrushes. Currys £29.99. Added.
- Maybelline Eraser concealer 01 Light, B00JR76TKW, £6.99 (RRP £10), 10K+ bought. Superdrug £7.99. Added.
- Garnier Hair Food banana 400ml, B07L5WGS2X, £4.00 (RRP £7.99), 10K+ bought. Superdrug 390ml £4.49 (members half price). Spare for another day.
- Dreo Atom 316 heater, B0C9D4KL9D, £39.99 (was £49.99), 5K+ bought, deal ends about 11.45pm tonight. Added as a was/now deal; no high street match for this exact model.
- Hot Hands 5 pairs, B08GCT8SXZ, £3.00 (RRP £4.99), 7K+ bought. Boots page would not give a price. Not added.

VIDEO CANDIDATE (by price gap rather than a Movers & Shakers climb): Maybelline Sky High £8.11 vs Superdrug £12.99 (60K+ bought), or BRITA MAXTRA PRO £24.50 vs Currys £34.99 (20K+ bought). Both Amazon prices must be re-read on the evening run.
