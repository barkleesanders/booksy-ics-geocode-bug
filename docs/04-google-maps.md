# 04 - Google Maps / Google Business Profile

Google’s public geocoder already demonstrates the bug: bare `411` / `411A Brannan St San Francisco` pins near **iHeart** (~15 m), while **The Closer Shave** and **Unit A** queries pin correctly.

This repo does **not** claim GBP is broken or already fixed. Investigation noted the name / Unit A path resolving to the shop.

## Owner: Google Business Profile

1. Sign in to [Google Business Profile](https://business.google.com/) for **The Closer Shave**.
2. Confirm primary name is the storefront customers expect.
3. Address: **411 Brannan St, Unit A** (or **Bldg A**), San Francisco, CA 94107. Prefer structured unit fields over a single `411A` line if the UI allows.
4. Map pin: entrance at / near Booksy coords `37.779768, -122.394546`. Reject any pin near 340 Townsend.
5. Categories: Barber shop / Hair salon.
6. Ensure “Your Barber Juan” does not create a second conflicting pin unless it is truly a separate premises.
7. After saves, verify:

```
The Closer Shave San Francisco
411 Brannan St Unit A San Francisco
```

both land on the shop. Separately confirm that bare

```
411A Brannan St San Francisco
```

still mis-pins for **non-owners** (geocoder quirk); that is why ICS must not rely on bare street alone.

## Customer: Suggest an edit

1. Open Google Maps.
2. Find the wrong result (e.g. directions to iHeart when searching the barbershop address) or the shop listing.
3. **Suggest an edit** / **Report a problem** on the place card.
4. Clarify: shop is **411 Brannan Unit A**; iHeart is **340 Townsend**, different business.

Paste-ready text: [REPORT_PACK.md](../REPORT_PACK.md).

## Why GBP alone does not fix Apple Calendar

Android / Google Calendar consumers benefit from a clean GBP. Apple Calendar invitees use Apple Maps. Booksy still must ship `GEO` + titled `LOCATION` in ICS for the Apple path.
