# 06 - Booksy report templates

Use Biz chat (merchant) and email **info.us@booksy.com** (or current US support address on booksy.com). Keep tone factual. No secrets.

Copy-paste variants also live in [REPORT_PACK.md](../REPORT_PACK.md).

---

## A) This shop: Your Barber Juan / The Closer Shave

**Subject:** Calendar invites geocode to iHeartMedia (340 Townsend) instead of 411A Brannan Unit A

Hi Booksy Support,

Booksy business: Your Barber Juan (id 1710466), location The Closer Shave, 411A Brannan St / 411 Brannan St Unit A, San Francisco, CA 94107.

Problem: Apple Calendar invites from Booksy send customers’ Get Directions to iHeartMedia / iHeartRadio at 340 Townsend St (~400 m away), not to our door.

Evidence:

1. Booksy’s own JSON-LD already has the correct pin: 37.7797680906372, -122.39454645283753.
2. Google geocodes bare “411 Brannan St San Francisco” and “411A Brannan St San Francisco” to ~37.77653,-122.39651 (~15 m from iHeart, ~399 m from us). Nominatim reverse of that pin is “iHeartMedia San Francisco, 340 Townsend Street”.
3. Queries with our business name or “Unit A” resolve correctly to The Closer Shave.
4. OSM building way/124903636 is at 411 Brannan; there is no iHeart tenant at 411. iHeart in OSM is only at 340 Townsend.

Likely cause: ICS LOCATION is a bare street string without GEO / X-APPLE-STRUCTURED-LOCATION, so Apple Maps re-geocodes 411A and prefers a famous nearby POI.

Please fix invites to:

- LOCATION first line = shop/venue name (The Closer Shave / Your Barber Juan), then Unit A address (prefer “Unit A” over bare “411A” alone).
- Always emit GEO from the profile pin (same as JSON-LD).
- Emit matching X-APPLE-STRUCTURED-LOCATION with X-TITLE and geo: URI for Apple Calendar.

Public write-up / validator: (attach or link this repo after publish under github.com/barkleesanders/…).

Thank you,
[Merchant / Barklee Sanders]

---

## B) Fleet / other multi-tenant shops

**Subject:** Fleet risk: bare street LOCATION in ICS breaks multi-tenant / unit addresses in Apple Calendar

Hi Booksy Support,

We hit a systematic geocode failure: ICS LOCATION set to a bare multi-tenant street (example: 411A Brannan St, San Francisco) without GEO causes Apple/Google to re-geocode to a famous nearby POI (example: iHeartMedia at 340 Townsend, ~400 m from the real shop).

Booksy already stores correct coordinates in business JSON-LD; they are not making it into calendar invites.

Please treat this as a product bug for all shops that have:

- unit / suite / “A” style addresses
- shared buildings with stronger nearby brands

Recommended product rule:

1. Never emit street-only LOCATION for booking ICS.
2. Always copy profile/JSON-LD geo → GEO.
3. Always include venue name on LOCATION line 1.
4. Emit X-APPLE-STRUCTURED-LOCATION for iOS/macOS.
5. Prefer structured unit fields (“Unit A”) in address text.
6. Add a regression test (street-only without GEO = fail).

Reference case: Your Barber Juan / The Closer Shave, Booksy 1710466, pin 37.7797680906372,-122.39454645283753; OSM building way/124903636; wrong POI iHeart @ 340 Townsend.

Happy to share sample bad/good ICS and a small Python validator.

Thanks,
[Name]

---

## Merchant Biz chat (short)

Calendar pin wrong: customers navigate to iHeart at 340 Townsend instead of 411 Brannan Unit A. Booksy web JSON-LD already has the right coords (37.779768,-122.394546). Please add GEO + shop name to ICS LOCATION / Apple structured location. Details in email to info.us@booksy.com.
