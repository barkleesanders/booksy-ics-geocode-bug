# Report pack (copy-paste)

Ready-to-send text for Booksy, the merchant, Apple Maps, and Google Maps.  
Facts only. No claim that listings are already fixed. No secrets.

Shop: **The Closer Shave** / **Your Barber Juan** (Booksy `1710466`)  
Address: **411 Brannan St Unit A** (also written **411A Brannan St**), San Francisco, CA 94107  
Booksy JSON-LD pin: **37.7797680906372, -122.39454645283753**  
Wrong POI: **iHeartMedia / iHeartRadio, 340 Townsend St** (~400 m away)  
OSM building at 411: way/**124903636**

---

## 1) Booksy support (email)

**To:** info.us@booksy.com  
**Subject:** Calendar invites geocode to iHeartMedia (340 Townsend) instead of 411A Brannan Unit A

Hi Booksy Support,

Booksy business: Your Barber Juan (id 1710466), at The Closer Shave, 411A Brannan St / 411 Brannan St Unit A, San Francisco, CA 94107.

When customers accept the Booksy calendar invite in Apple Calendar and tap Get Directions, Maps sends them to iHeartMedia / iHeartRadio at 340 Townsend Street, about 400 meters from our door.

Booksy’s public JSON-LD already has the correct coordinates: 37.7797680906372, -122.39454645283753. The invite path appears to emit a bare street LOCATION without GEO / X-APPLE-STRUCTURED-LOCATION, so Apple Maps re-geocodes “411A Brannan” and prefers a famous nearby POI.

Public geocode checks (2026-09-24 PT):

- Google: “411 Brannan St San Francisco” and “411A Brannan St San Francisco” primary-pin near 37.77653,-122.39651 (~15 m from iHeart, ~399 m from shop).
- Nominatim reverse of that pin: “iHeartMedia San Francisco, 340 Townsend Street”.
- “The Closer Shave” / “411 Brannan St Unit A” resolve to the shop.
- OSM has building way/124903636 at 411 Brannan with no shop POI; iHeart in OSM is only at 340 Townsend.

Please update ICS generation to:

1. Put the venue/shop name on the first line of LOCATION, then Unit A address (prefer “Unit A” over bare “411A” alone).
2. Always emit GEO from the business profile / JSON-LD pin.
3. Emit matching X-APPLE-STRUCTURED-LOCATION (X-TITLE, X-ADDRESS, geo URI) for Apple Calendar.
4. Apply the same rule fleet-wide for multi-tenant and unit-letter addresses.

We can share sample bad/good .ics files and a small validator. Thank you.

[Your name]

---

## 2) Juan / Closer Shave merchant checklist

Use in Biz chat or as an internal checklist. Not a claim that work is done.

**Calendar wrong-pin checklist**

- [ ] Message Booksy Biz chat: invites send clients to iHeart @ 340 Townsend; ask for GEO + shop name in ICS (see short chat blurb in docs/06-booksy-report.md).
- [ ] Email info.us@booksy.com with section (1) above.
- [ ] Apple Business Connect: claim **The Closer Shave**, address **411 Brannan St Unit A**, pin on entrance near 37.779768, -122.394546 (not Townsend).
- [ ] Google Business Profile: confirm Unit A / Bldg A and pin on the shop (name search already looked correct in our checks; still verify).
- [ ] Optional: add OSM node `shop=hairdresser` `name=The Closer Shave` at Booksy coords (helps Nominatim; does **not** fix Apple Calendar alone).
- [ ] After Booksy confirms ICS change: book a test, export/inspect .ics for LOCATION + GEO, tap Get Directions on iPhone, confirm pin is 411 Unit A not 340 Townsend.
- [ ] Do not tell clients “Maps is fixed” until that device test passes.

**Biz chat one-liner**

Calendar pin wrong: clients navigate to iHeart at 340 Townsend instead of 411 Brannan Unit A. Booksy web JSON-LD already has 37.779768,-122.394546. Please add GEO + shop name to ICS / Apple structured location. Emailing details to info.us@booksy.com.

---

## 3) Apple Maps feedback (“Report a Problem”)

Paste into Apple Maps → place card → Report a Problem (adjust to the nearest form fields).

The Closer Shave / Your Barber Juan is at 411 Brannan St Unit A, San Francisco, CA 94107 (about 37.779768, -122.394546). It is not at 340 Townsend.

iHeartMedia / iHeartRadio is a different business at 340 Townsend Street. Apple Calendar invites that only contain the street “411A Brannan St” are opening directions near iHeart (~400 m away) instead of the barbershop.

Please bind the barbershop place to Unit A at 411 Brannan and keep iHeart at Townsend. Thank you.

---

## 4) Google suggest-edit text

Paste into Google Maps → Suggest an edit / Report a problem.

The Closer Shave (Your Barber Juan) is at 411 Brannan St Unit A, San Francisco, CA 94107. Correct door coordinates are approximately 37.779768, -122.394546.

Bare searches for “411 Brannan St San Francisco” or “411A Brannan St San Francisco” have been resolving near iHeartMedia at 340 Townsend Street (~400 m away). iHeart is not a tenant at 411 Brannan.

Please keep The Closer Shave / Unit A pinned at 411 Brannan, and keep iHeartMedia at 340 Townsend. Searches that include “Unit A” or “The Closer Shave” already look correct; the bare street form is what breaks calendar-style address-only queries.

---

## Fleet note (optional add-on to Booksy)

If you operate other Booksy locations in shared buildings, assume the same failure mode whenever LOCATION is street-only without GEO. Prefer venue name + unit + GEO on every invite.
