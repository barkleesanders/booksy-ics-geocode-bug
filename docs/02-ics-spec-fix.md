# 02 - ICS spec fix (RFC 5545 + Apple extensions)

## Goal

Make calendar clients navigate to the **shop door pin** without re-geocoding a bare street string.

Booksy already publishes:

- lat `37.7797680906372`
- lon `-122.39454645283753`

Those values belong in the invite.

## RFC 5545 fields that matter

| Property | Role |
|----------|------|
| `LOCATION` | Free text on the event. If this is **only** `411A Brannan St…`, Maps **searches that string**. |
| `GEO` | `lat;lon` (semicolon). When present and trusted, directions can use the pin even if title text is ambiguous. |
| `DESCRIPTION` | Optional human context; does not replace GEO. |

### Bad (street-only, no GEO)

```ics
LOCATION:411A Brannan St\, San Francisco\, CA 94107
```

This matches `code/testdata/bad_invite.ics`. Validator **FAIL**.

### Good (titled LOCATION + GEO)

```ics
LOCATION:The Closer Shave - Your Barber Juan\n411 Brannan St Unit A\nSan Francisco\, CA 94107
GEO:37.779768;-122.394546
```

Prefer **Unit A** wording over bare `411A` in the address lines (bare `411A` geocodes badly in Google; Nominatim also fails Unit A).

## Apple: `X-APPLE-STRUCTURED-LOCATION`

Apple Calendar’s in-event map is powered by an Apple extension. Keep it **consistent** with `LOCATION` and `GEO` or Calendar may ignore the rich location.

Pattern:

```ics
X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-ADDRESS=411 Brannan St Unit A\, San Francisco\, CA 94107;X-APPLE-RADIUS=50;X-TITLE=The Closer Shave:geo:37.779768,-122.394546
```

Notes:

- `X-TITLE` = storefront name (**The Closer Shave**), not only the barber brand, unless that is the Maps listing name.
- `X-ADDRESS` should include **Unit A**.
- `geo:lat,lon` uses a **comma** (URI); `GEO` property uses a **semicolon**.
- Fold long lines per RFC 5545 (75 octets) with a leading space on continuations.

Full good sample: `code/testdata/good_invite.ics` (also emitted by `code/generate_good_ics.py`).

## EventKit / place_id (best case)

On Apple platforms, a durable binding is a MapKit / Maps **place** (what you get when a human picks a POI in Maps). Third-party ICS that only sets a street string never gets that binding.

Owner path to a real place: **Apple Business Connect** listing for The Closer Shave at Unit A (see [03-apple-maps.md](03-apple-maps.md)). Booksy should prefer emitting structured location tied to that place when available; until then, **GEO + titled LOCATION** is the minimum fleet fix.

## Implementation checklist for Booksy (product)

- [ ] Never emit LOCATION that is only `housenumber + street` for multi-tenant venues.
- [ ] First line of LOCATION = business / venue name from the shop profile.
- [ ] Always copy JSON-LD / profile `geo` into `GEO`.
- [ ] Emit matching `X-APPLE-STRUCTURED-LOCATION` for iOS/macOS Calendar.
- [ ] Prefer `Unit A` / suite fields over concatenating `411A` alone.
- [ ] Regression test: validator in this repo must PASS on production fixtures.

## Validation

```bash
python3 code/validate_ics.py path/to/invite.ics
```

Exit code **1** if LOCATION is street-only and GEO / structured geo is missing.
