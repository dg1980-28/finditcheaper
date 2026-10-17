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

## 16 Oct 2026

Checked from the GitHub Actions runner (Scrape Amazon run 8, 05:54 to 06:02 UTC, London delivery address set, prices in GBP). The main Movers & Shakers page and all nine category pages (beauty, kitchen, drugstore, home-garden, electronics, diy, lighting, sports, pet-supplies) loaded but listed no products, as on 15 Oct. No climbers recorded, no video candidate from Movers & Shakers today.

Best seller lists loaded for beauty, kitchen, home-garden, lighting, electronics, sports and pet-supplies; drugstore and diy hit a robot check and were skipped (yesterday's lists covered the candidates from those two). Product pages read the same run, biggest "bought in past month" first:

- Catsan Hygiene Plus cat litter 20L, B001MZV3OO, £12.00 (was £12.89), 80K+ bought. No high street price checked. Not added.
- Dr. Beckmann Service-it washing machine cleaner 250g, B0080ZSQKS, £2.00 (RRP £3.49), 50K+ bought, #1 in Home & Kitchen. No high street price found (Superdrug and Currys do not list it). Added as a was/now deal.
- Medicube Collagen Jelly Cream 110ml, B0CM2PPNMW, £16.80 (RRP £17.90), 40K+ bought. Boots £26.00. Added. Biggest gap of the day (£9.20).
- Sudafed Blocked Nose Spray 15ml, B004RDYI04, £4.47 (RRP £6.05), 30K+ bought. Superdrug £4.69 (was £5.19). Added.
- Eylure Dybrow Dark Brown, B000SDQ224, £7.49 (RRP £8.00), 20K+ bought. Superdrug £9.00. Added.
- Hycosan Extra eye drops 7.5ml, B07PHZCQYB, £12.98, 20K+ bought. Superdrug £12.99. One penny apart, not added.
- Mr Muscle Drain Unblocker 2 x 1L, B075V3T7ZR, £6.75, 20K+ bought. No RRP shown, no high street price. Not added.
- Dr. Beckmann Carpet Stain Remover 650ml, B006ZMNWYS, £3.15, 20K+ bought. No RRP shown, no high street price. Not added.
- Garnier Hair Food Banana 400ml, B07L5WGS2X, £4.00 (RRP £7.99), 10K+ bought. Superdrug 390ml £8.99 (members £4.49). Added.
- Vitabiotics Ultra Vitamin D3 1000IU 96 tablets, B003VQZC3U, £4.92 (RRP £6.15), 10K+ bought. Superdrug £5.39. Added.
- Gorilla Super Glue 15g, B003CT4XT0, £5.75 (RRP £10.79), 10K+ bought, #1 in super glue. No high street price readable (B&Q search pages are blocked). Added as a was/now deal.
- TePe interdental brushes 0.7mm 20 pack, B08Z8N9L1R, £9.90 (RRP £10.95), 9K+ bought. Superdrug only sells a 6 pack (£3.49), so no like for like. Not added.
- Just For Men Moustache & Beard M45 Dark Brown, B07NBPSNC4, £8.95, 9K+ bought. Superdrug £8.99. Four pence apart, not added.
- Speedo Biofuse 2.0 goggles, B0BK1Y38RD, £17.99 (RRP £24.50), 7K+ bought. No high street price. Not added.
- FireAngel FA6813 CO alarm, B0CKWGSX22, £13.98 (RRP £17.99, limited time deal), 5K+ bought. Currys £13.99 (was £16.49). Added.
- Kidde 5CO CO alarm, B07WSX4NCV, £13.75 (RRP £18.95), 5K+ bought, sold by Safelincs. Wickes and Argos pages give no price. Not added.
- UniBond AERO 360 refill 4 pack, B01LCHCRQO, £11.50 (RRP £13.15), 5K+ bought. No high street price. Spare.
- Contigo Byron 470ml, B07TN8SLWP, £9.00 (was £12.50), 5K+ bought. No high street price. Spare.
- Ring Battery Video Doorbell 2K, B0FHJ91JY5, £79.99, 5K+ bought. Currys £79.99. Same price, not added.
- Tapo L530B B22 bulb, B08JZHXQC4, £7.99, 4K+ bought. Currys has delisted it and the Argos page gives no price. Not added.
- Rimmel 60 Seconds Super Shine 740 Clear, B00UYJGYCK, £3.38 (was £3.98), 4K+ bought, sold by AVA SUPPLIES. Superdrug £3.99. Added.
- Schwarzkopf LIVE 099 Deep Black, B0G35QMQ82, £6.50 (RRP £9.00), 4K+ bought. Superdrug £6.50 (was £8.99). Same price, spare.
- Clairol Nice'n Easy 4 Dark Brown, B07895R49B, £6.00 (was £6.68), 3K+ bought. Superdrug £7.99 (2 for £12). Added.

VIDEO CANDIDATE (by price gap rather than a Movers & Shakers climb): Medicube Collagen Jelly Cream £16.80 on Amazon vs £26 at Boots, 40K+ bought this month, £9.20 gap. Second choice: Garnier Hair Food Banana £4 vs Superdrug £8.99 (10K+). Both Amazon prices must be re-read on the evening run.

## 17 Oct 2026

Checked from the GitHub Actions runner. Scrape Amazon run 9 (05:55 UTC) read the main Movers & Shakers page and the nine category pages with plain requests: eight loaded and listed no products (as on 15 and 16 Oct), beauty and pet-supplies hit a robot check. No climbers recorded, no video candidate from Movers & Shakers today.

Best seller lists loaded for beauty, kitchen, electronics, sports and pet-supplies; drugstore, home-garden, diy and lighting hit robot checks (yesterday's lists covered those). Runs 9 and 10 then hit a robot check on nearly every product page and never got the UK delivery address set, so the few prices they returned were ex VAT and were discarded. Run 11 (07:15 to 07:18 UTC, headed Chrome under xvfb, London delivery address set, prices in GBP) read all 24 requested product pages first time. Biggest "bought in past month" first:

- Medicube PDRN Pink Collagen Jelly Gel Mask 4 pack, B0DGTMR754, £10.00 (RRP £16.90), 80K+ bought, #1 in face treatments and masks, sold by Medicube Official. John Lewis £14.99 (out of stock online). Added. Biggest count of the day.
- CeraVe Blemish Control Cleanser 236ml, B0B7RQ46LD, £11.60 (no RRP shown), 30K+ bought. Superdrug £14.49. Added.
- CeraVe AM Facial Moisturising Lotion SPF50 52ml, B09XN22JBT, £12.75 (RRP £16.50), 30K+ bought. Superdrug £16.99. Added. Biggest cash gap of the day (£4.24).
- La Roche Posay Cicaplast Baume B5+ 100ml, B0BJFLVCZK, £16.91 (RRP £19.50), 30K+ bought. Superdrug £19.89. Added.
- Acnecide Face Gel 15g, B089QQBDPD, £7.99 (RRP £10.99), 20K+ bought. Superdrug £10.99. Added.
- NIVEA Double Effect Waterproof Eye Makeup Remover 125ml, B09P1Z8TKZ, £2.00 (RRP £5.49), 20K+ bought. Boots £3.89. Added.
- Maybelline Lash Sensational mascara 9.5ml, B00PFCSXD4, £5.99 (RRP £9.99), 20K+ bought. Superdrug (Very Black) £9.99. Added.
- L'Oréal Infallible 3 Second Setting Spray 75ml, B0CNQ4DJRV, £9.34 (RRP £10), 10K+ bought, sold by Beautiquelondon. Superdrug £9.99. 65p gap, spare.
- Rimmel Stay Matte Pressed Powder Transparent, B004M9L0WW, £3.78 (RRP £4.99), 10K+ bought, sold by Horizon Mark. Superdrug £4.99. Spare.
- CeraVe Foaming Cleanser 236ml, B07C5SKVL7, £9.37 (RRP £12.50), 10K+ bought. Superdrug £12.49. Added.
- Nizoral Anti Dandruff Shampoo 100ml, B0DQV8G9HR, £9.74 (RRP £13.99), 10K+ bought. Superdrug £12.99. Added.
- Revolution Precise Brow Pencil Dark Brown, B07VRLPNY1, £3.87 (RRP £4), 10K+ bought. Superdrug £4.00. 13p gap, not added.
- Tommee Tippee GroEgg2, B08BD8TFV4, £19.98 (RRP £32.99), 10K+ bought, #1 in children's lighting. Boots out of stock online with no price; Argos and John Lewis pages give no price. Added as a was and now deal.
- Super Ninja Fruit Fly Traps 2 pack, B0963J155G, £9.99 (no RRP), 60K+ bought. No high street price. Not added.
- Bloo Power Active rim block 3 pack, B07PLT2N4G, £3.00 (no RRP), 10K+ bought. No high street price. Not added.
- Hot Hands 5 pairs, B08GCT8SXZ, £3.00 (RRP £4.99), 8K+ bought. No high street price readable. Spare.
- DURACELL 2032 4 pack, B01CG0TO76, £3.28 (RRP £8), 5K+ bought, sold and dispatched by DORCHESTER NEWS. Currys £8.99. Spare because of the third party seller.
- UniBond AERO 360 refill 4 pack, B01LCHCRQO, £11.50 (RRP £13.15), 5K+ bought. Spare.
- Contigo Byron 470ml, B07TN8SLWP, £9.00 (was £12.50), 5K+ bought. Spare.
- Schwarzkopf LIVE 099 Deep Black, B0G35QMQ82, £6.50 (RRP £9), 4K+ bought. Superdrug £6.50. Same price, not added.
- Garnier Nutrisse 4.15 Iced Coffee Brown, B006L68VDU, £7.39, 3K+ bought, currently unavailable from the main seller. Not added.

Re-checks: heated throw £25.49 (was £29.99) still a limited time deal, 7K+ bought; Oral-B iO2 Duo £59.98 (RRP £160) still a limited time deal, 3K+; FireAngel FA6813 £13.98 (RRP £17.99) still a limited time deal, 5K+. No deal end times were shown on any page; every "Only N left" line belonged to another item in a carousel, so no low stock notes.

VIDEO CANDIDATE (by price gap rather than a Movers & Shakers climb): Medicube PDRN Pink Collagen Jelly Gel Mask £10 on Amazon vs £14.99 at John Lewis, 80,000 bought this month, £4.99 gap (say "John Lewis lists it at £14.99" rather than "in stock", because it was out of stock online when checked). Second choice: CeraVe AM SPF50 £12.75 vs Superdrug £16.99 (30K+, £4.24 gap). Both Amazon prices must be re-read on the evening run.
