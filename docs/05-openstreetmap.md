# 05 - OpenStreetMap recipe (`shop=hairdresser`)

## Honesty first

**OSM alone does NOT fix Apple Calendar.** Apple Maps ≠ OSM / Nominatim.

Add the shop to OSM to fix open-data search and to help apps that use Nominatim. Still require:

- Booksy ICS `GEO` + titled `LOCATION`
- Apple Business Connect + Google Business Profile for proprietary Maps

Do **not** claim an OSM changeset fixed Calendar invites.

## Current OSM state (evidence, Sep 24, 2026 PT)

| Item | State |
|------|--------|
| Building 411 Brannan | way/`124903636`, centroid ≈ `37.7796851, -122.3944474` |
| Shop POI “The Closer Shave” / “Your Barber Juan” | **Missing** (Nominatim 0 hits) |
| iHeartMedia | Office at **340 Townsend** ≈ `37.7766503, -122.3964158` (~384 m SW) |
| iHeart at 411 | **Does not exist** in OSM |

Reverse of Booksy pin → unnamed building only.

## Recommended edit (one new node)

Create **one node** at the Booksy door coordinates (do **not** retag the multi-tenant building way as the shop):

```
lat=37.7797680906372
lon=-122.39454645283753
shop=hairdresser
name=The Closer Shave
alt_name=Your Barber Juan
addr:housenumber=411A
addr:street=Brannan Street
addr:unit=A
addr:city=San Francisco
addr:state=CA
addr:postcode=94107
addr:country=US
website=https://theclosershavesf.com/
source=survey;booksy;website
```

Optional if surveyed on site: `phone=…`, `opening_hours=…`.

### Practice notes

- Prefer `shop=hairdresser` for a barbershop (OSM wiki convention).
- One primary `name` = storefront; use `alt_name` for the Booksy barber brand. Avoid two nodes for the same chair.
- Do not move or “correct” the iHeart object at 340 Townsend.
- Changeset comment example: `Add The Closer Shave barbershop (411A Brannan St, SF); missing POI; coords from Booksy JSON-LD / site`

Editors: [iD](https://www.openstreetmap.org/edit) or JOSM. Follow the [OSM code of conduct](https://wiki.openstreetmap.org/wiki/Code_of_conduct) and only map what you can verify.

## Verification after merge

Nominatim may lag minutes to hours.

1. Search `The Closer Shave San Francisco` → hit within ~20 m of Booksy lat/lng.
2. Reverse of Booksy coords → building and/or new shop node nearby.
3. Explicitly re-test Apple Calendar with a **new** Booksy invite; if ICS still lacks GEO, Apple path remains broken regardless of OSM.

## Optional local check

```bash
python3 code/geocode_compare.py
```

Respects Nominatim 1 req/s policy.
