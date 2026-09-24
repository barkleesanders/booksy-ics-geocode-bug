# 07 - Repro matrix (shop vs iHeart)

All coordinates below are from the Sep 24, 2026 PT investigation (Booksy JSON-LD + GIS dump). Do not invent new pins.

## Reference pins

| Label | lat, lon | Notes |
|-------|----------|-------|
| Booksy shop (JSON-LD) | `37.7797680906372, -122.39454645283753` | Your Barber Juan / door |
| OSM building 411 Brannan | `37.7796851, -122.3944474` | way/`124903636`, ~13 m from Booksy |
| iHeartMedia OSM | `37.7766503, -122.3964158` | 340 Townsend, ~384 m SW |
| Google bare-411 primary | `37.7765346, -122.3965119` | ~15 m from iHeart, ~399 m from shop |

## Query matrix

| Query | Expected / observed | Dist → shop | Dist → iHeart | Named hit |
|-------|---------------------|-------------|---------------|-----------|
| The Closer Shave San Francisco | **Shop** | ~13 m | ~379 m | The Closer Shave @ 411 Brannan St Bldg a |
| 411 Brannan St Unit A San Francisco | **Shop** | ~13 m | ~379 m | The Closer Shave |
| **411 Brannan St San Francisco** | **Wrong** | ~399 m | ~15 m | iHeart cluster |
| **411A Brannan St San Francisco** | **Wrong** | ~399 m | ~15 m | same wrong cluster |
| iHeartRadio San Francisco | iHeart | ~393 m | ~27 m | 340 Townsend |
| iHeartMedia San Francisco | iHeart | ~393 m | ~27 m | 340 Townsend |
| Your Barber Juan San Francisco | Weak / incomplete in scrape | - | - | do not rely on this alone |
| Nominatim: The Closer Shave SF | **0 hits** (no OSM POI) | - | - | missing shop node |
| Nominatim: 411A Brannan SF | Bad / street-level | - | - | not Unit A |
| Nominatim reverse of Google wrong pin | iHeartMedia @ 340 Townsend | - | - | smoking gun |

## How to re-run

### Google Maps (browser)

Paste each query into Google Maps. Compare the primary pin to the reference table.

### Nominatim (script)

```bash
python3 code/geocode_compare.py
```

Rate-limited to ~1 request/second with an identifiable User-Agent.

### Apple Maps

Use Maps on a Mac/iPhone (web `maps.apple.com` from headless fetch often returns a JS shell only). Search the same strings. Calendar path: accept a Booksy invite and tap LOCATION.

### ICS fixtures in this repo

```bash
python3 code/validate_ics.py code/testdata/bad_invite.ics   # expect FAIL
python3 code/validate_ics.py code/testdata/good_invite.ics  # expect PASS
```

## Pass/fail for a real Booksy invite

On device, after the next booking:

- [ ] `LOCATION` starts with shop name and includes Unit A
- [ ] `GEO` within ~20 m of `37.779768, -122.394546`
- [ ] Optional `X-APPLE-STRUCTURED-LOCATION` matches title/address/geo
- [ ] Get Directions opens The Closer Shave / 411 Unit A, **not** iHeart / 340 Townsend
- [ ] Driving ETA matches Brannan, not Townsend

If GEO + title are correct but Maps still opens iHeart, remaining issue is Apple POI database → Business Connect, not more street text.
