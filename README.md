# Booksy ICS geocode bug: bare street LOCATION → wrong POI (iHeart @ 340 Townsend)

**Public evidence + fix docs + ICS validators** for Barklee Sanders (`barkleesanders`).

When Booksy (and similar booking apps) put a **bare multi-tenant street** into an Apple Calendar ICS `LOCATION` (e.g. `411A Brannan St`) **without `GEO` / structured place binding,** Apple/Google re-geocode that string and can land on a **famous nearby POI** instead of the shop door.

Concrete case: **Your Barber Juan / The Closer Shave** at **411A Brannan St, San Francisco** vs **iHeartMedia / iHeartRadio** at **340 Townsend St** (~400 m away).

> This repo documents the bug and ships sample ICS + a validator.  
> It does **not** claim Apple Maps or Google listings are already fixed.  
> OSM alone does **not** fix Apple Calendar (Apple Maps ≠ OSM).

Evidence: Booksy JSON-LD, Nominatim/OSM Overpass, and Google Maps public geocode comparisons checked **Thu Sep 24, 2026 ~1:05-1:10 PM PT**.

---

## TL;DR

| Fact | Value |
|------|--------|
| Booksy JSON-LD shop pin | `37.7797680906372, -122.39454645283753` |
| OSM building at 411 Brannan | way/`124903636` ≈ `37.7796851, -122.3944474` (~13 m from Booksy) |
| iHeart in OSM / Google | **340 Townsend** ≈ `37.7766503, -122.3964158` (~384 m SW) |
| Google bare `411` / `411A Brannan St SF` | primary pin ~`37.77653, -122.39651` (**~15 m from iHeart**, **~399 m from shop**) |
| Nominatim reverse of that wrong pin | **iHeartMedia San Francisco, 340 Townsend Street** |
| Shop in OSM? | **No** “The Closer Shave” / “Your Barber Juan” node (building only) |

**Root cause:** address-only ICS → Calendar/Maps search the street string → unit `411A` mishandled → ranked POI search prefers iHeart cluster.

**What actually fixes Apple Calendar for invitees:**

1. **Booksy** must emit `GEO` + titled `LOCATION` (+ ideally `X-APPLE-STRUCTURED-LOCATION`).
2. **Owner** must claim **Apple Business Connect** + keep **Google Business Profile** aligned (Unit A / Bldg A).
3. Optional OSM `shop=hairdresser` helps open data / Nominatim; **does not** replace (1)+(2) for Apple.

---

## Repro (customer experience)

1. Book via Booksy with Your Barber Juan (business id `1710466`).
2. Accept the calendar invite into Apple Calendar.
3. Tap the event location → Get Directions / open in Maps.
4. Observe pin / ETA near **340 Townsend (iHeart)**, not **411 Brannan Unit A**.

Queries that demonstrate geocoder behavior (see [docs/07-repro-matrix.md](docs/07-repro-matrix.md)):

| Query | Typical result |
|-------|----------------|
| `411 Brannan St San Francisco` | Wrong: iHeart cluster |
| `411A Brannan St San Francisco` | Wrong: same |
| `411 Brannan St Unit A San Francisco` | Correct: The Closer Shave |
| `The Closer Shave San Francisco` | Correct: shop |
| `iHeartMedia San Francisco` | Correct: 340 Townsend |

---

## Fix matrix

| Actor | Action | Fixes Apple Calendar invites? |
|-------|--------|-------------------------------|
| Booksy | `LOCATION` = shop name + Unit A address; always emit `GEO` from JSON-LD pin; emit `X-APPLE-STRUCTURED-LOCATION` | **Yes** (primary) |
| Merchant | Apple Business Connect listing at Unit A door | **Yes** for Maps POI search |
| Merchant | Google Business Profile Unit A / Bldg A (often already OK) | Helps Google Maps / Android |
| Anyone | OSM `shop=hairdresser` node at Booksy coords | Helps Nominatim/OSM apps; **not** Apple |
| Customer | Apple Maps “Report a Problem” / Google “Suggest an edit” | Soft signal only |

Copy-paste emails: [REPORT_PACK.md](REPORT_PACK.md). Booksy + merchant templates: [docs/06-booksy-report.md](docs/06-booksy-report.md).

---

## Repo layout

```
README.md
REPORT_PACK.md
LICENSE
docs/01-root-cause.md
docs/02-ics-spec-fix.md
docs/03-apple-maps.md
docs/04-google-maps.md
docs/05-openstreetmap.md
docs/06-booksy-report.md
docs/07-repro-matrix.md
code/validate_ics.py
code/generate_good_ics.py
code/geocode_compare.py
code/testdata/bad_invite.ics
code/testdata/good_invite.ics
SUMMARY.txt
```

---

## Tools

Validate ICS files (exit **non-zero** on street-only LOCATION without GEO):

```bash
python3 code/validate_ics.py code/testdata/*.ics
```

Generate a good sample invite:

```bash
python3 code/generate_good_ics.py
python3 code/generate_good_ics.py --out /tmp/good.ics
```

Optional Nominatim compare (1 req/s, identifiable UA):

```bash
python3 code/geocode_compare.py
```

### Expected validator behavior

| File | Result |
|------|--------|
| `code/testdata/bad_invite.ics` | **FAIL** (street-only LOCATION, no GEO) |
| `code/testdata/good_invite.ics` | **PASS** (titled LOCATION + GEO + Apple structured location) |

---

## Honesty / non-claims

- We did **not** fix Apple or Google listings by publishing this repo.
- We did **not** obtain a live Booksy `.ics` dump from a Mac in the investigation window (machines offline). Theory matches public geocode + ICS field behavior; confirm on next invite.
- OSM edit (if performed later) does **not** fix Apple Calendar by itself.
- No secrets, tokens, or private calendar data are included.

## License

MIT. See [LICENSE](LICENSE).
