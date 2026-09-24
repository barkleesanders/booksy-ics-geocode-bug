# 01 - Root cause

## Symptom

Apple Calendar events created from Booksy invites for **Your Barber Juan** (Booksy business `1710466`, working out of **The Closer Shave** at **411A Brannan St / 411 Brannan St Unit A, San Francisco, CA 94107**) open Get Directions near **iHeartMedia / iHeartRadio at 340 Townsend St**, not at the barbershop door.

Distance between the two pins is about **384-399 m**.

## What Booksy already knows

Booksy’s public business page publishes correct door coordinates in JSON-LD (`HairSalon`):

```json
{
  "name": "Your Barber Juan",
  "address": {
    "streetAddress": "411A Brannan St, San Francisco, 94107"
  },
  "geo": {
    "latitude": 37.7797680906372,
    "longitude": -122.39454645283753
  }
}
```

So the platform **has** a good pin for web/SEO. The calendar path is consistent with emitting **address text without that pin** (and without a Maps place binding).

## What geocoders do with bare `411` / `411A Brannan`

| Source | Bare street query | Result |
|--------|-------------------|--------|
| Google Maps (public search) | `411 Brannan St San Francisco` | ~`37.7765346, -122.3965119` (~15 m from iHeart, ~399 m from shop) |
| Google Maps | `411A Brannan St San Francisco` | Same wrong cluster |
| Google Maps | `411 Brannan St Unit A…` or `The Closer Shave…` | Correct shop (~13 m from Booksy pin) |
| Nominatim reverse of Google’s wrong pin | - | **iHeartMedia San Francisco, 340 Townsend Street** |
| Nominatim forward `411 Brannan…` | - | OSM building centroid ≈ Booksy |
| Nominatim forward `411A Brannan…` | - | Fails / street segments, not Unit A |
| Nominatim `The Closer Shave` / `Your Barber Juan` | - | **0 hits** (shop not in OSM) |

Smoking gun: the coordinate Google returns for bare `411(A) Brannan` **reverse-geocodes in OSM/Nominatim to iHeart at 340 Townsend**. iHeart is **not** a 411 Brannan tenant in public records or OSM.

## Multi-tenant address shape

| Entity | Address form | Role |
|--------|--------------|------|
| The Closer Shave LLC | `411 Brannan Street A` / `411A` / `Unit A` / `Bldg A` | Barbershop storefront |
| Your Barber Juan | `411A Brannan St` | Barber in that space (Booksy listing) |
| Other suites | e.g. Ste B, shared campus listings | Same building, different tenants |
| iHeartMedia | **340 Townsend St** | Famous POI ~3-4 blocks SW - **not** at 411 |

Unit letter matters. Geocoders that strip or mishandle `A` / `Unit A` lose the shop identity and fall back to ranked nearby brands.

## ICS → Calendar → Maps path

1. Invite carries `LOCATION:411A Brannan St…` (or similar) and **no** `GEO`.
2. Apple Calendar shows that text; Get Directions hands the string to **Apple Maps**.
3. Maps runs a place search / geocode on the street string (not “footprint of building 411”).
4. Awkward `411A` + weak/missing shop POI + strong iHeart brand nearby → wrong pin.
5. Every invitee’s device re-resolves independently, so the failure can be fleet-wide.

Apple Calendar uses **Apple Maps**, not OpenStreetMap. Adding an OSM node helps Nominatim and OSM-based apps; it does **not** by itself change Apple’s geocoder.

## Root cause (one sentence)

**Shared / awkward unit address without a durable Maps place title + without ICS `GEO` / structured location pinned to the shop door → Calendar/Maps prefer a more famous nearby POI when resolving LOCATION for directions.**

## What is *not* the root cause

- OSM claiming iHeart is at 411 (it does not; iHeart OSM is only at 340 Townsend).
- Booksy lacking door coords entirely (JSON-LD has them; ICS path is the gap).
- Customer “user error” for accepting a normal booking invite.

## Evidence paths (investigation)

Facts above are copied from the Sep 24, 2026 PT investigation:

- Booksy JSON-LD geo pin
- OSM building way/`124903636`
- Nominatim reverse of Booksy pin → unnamed building
- Nominatim reverse of Google bare-411 pin → iHeartMedia @ 340 Townsend
- Google Maps geocode comparison table

See also [07-repro-matrix.md](07-repro-matrix.md).
