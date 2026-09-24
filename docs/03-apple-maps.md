# 03 - Apple Maps (owner + customer)

Apple Calendar Get Directions uses **Apple Maps**, not OpenStreetMap. Fixing OSM does not fix Apple Calendar.

This doc does **not** claim the Apple listing is already corrected.

## Owner: Apple Business Connect

1. Go to [Apple Business Connect](https://businessconnect.apple.com/) and sign in with the business Apple ID.
2. Claim or create **The Closer Shave** (primary storefront name customers see on the door).
3. Set address to **411 Brannan St, Unit A** (or **Bldg A**), San Francisco, CA 94107. Avoid emitting only `411A` with no unit field if the form supports unit/suite.
4. Place the map pin on the **shop entrance** (align with Booksy pin ≈ `37.779768, -122.394546`). Do not accept a pin that snaps to 340 Townsend.
5. Categories: barber / hair salon as appropriate.
6. Hours, phone, website (`https://theclosershavesf.com/` if that is the live site), photos.
7. If “Your Barber Juan” is a separate consumer-facing brand, decide one primary Maps name; use alternate name fields rather than two conflicting pins at the same chair.
8. After publish, wait for indexing; then search Apple Maps for **The Closer Shave San Francisco** and confirm the pin is at 411 Unit A, not Townsend.

Ask Booksy (see [06-booksy-report.md](06-booksy-report.md)) to pull the Connect place into ICS structured location when their pipeline supports place IDs.

## Customer: Report a Problem (soft signal)

If Maps opens iHeart from a Calendar event or from a search for the shop address:

1. Open Apple Maps on iPhone/Mac.
2. Search **The Closer Shave** or the wrong pin you were sent to.
3. Tap the place card → **Report a Problem** (wording varies by OS version).
4. Choose the closest option (wrong location, place does not exist here, etc.).
5. State clearly: the barbershop is at **411 Brannan St Unit A**; **iHeartMedia is at 340 Townsend** and is a different business ~400 m away; Calendar invites with bare `411A Brannan` are routing to iHeart.

Paste-ready text is in [REPORT_PACK.md](../REPORT_PACK.md).

## What success looks like

- Searching the shop name opens a pin at 411 Unit A.
- Calendar events that include GEO + titled LOCATION open that pin (or an unlabeled pin within ~20 m of Booksy coords).
- Events that still only have bare street LOCATION may keep failing until Booksy ships GEO; Business Connect alone does not rewrite old ICS text.

## Honesty

Until Connect shows a verified listing and a real invite is re-tested on a Mac/iPhone, treat Apple POI state as **unknown / unverified** in this repo.
