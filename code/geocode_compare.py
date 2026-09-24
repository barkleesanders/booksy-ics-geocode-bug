#!/usr/bin/env python3
"""Optional Nominatim forward-geocode comparison for the Closer Shave case.

Respects Nominatim usage policy: max 1 request/second, identifiable UA.
Does not invent coordinates; prints whatever Nominatim returns.

Usage:
  python code/geocode_compare.py
  python code/geocode_compare.py --query "411A Brannan St San Francisco"
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, List

USER_AGENT = "booksy-ics-geocode-bug/1.0 (research; github.com/barkleesanders)"
NOMINATIM = "https://nominatim.openstreetmap.org/search"
SLEEP_SEC = 1.1

# Reference pins from evidence (Booksy JSON-LD + GIS dump), for distance only.
REF = {
    "booksy_shop": (37.7797680906372, -122.39454645283753),
    "osm_building_411": (37.7796851, -122.3944474),  # way/124903636
    "iheart_340_townsend": (37.7766503, -122.3964158),
}

DEFAULT_QUERIES = [
    "The Closer Shave San Francisco",
    "Your Barber Juan San Francisco",
    "411 Brannan St San Francisco",
    "411A Brannan St San Francisco",
    "411 Brannan St Unit A San Francisco",
    "iHeartMedia San Francisco",
    "iHeartRadio San Francisco",
]


def haversine_m(a: tuple, b: tuple) -> float:
    import math

    lat1, lon1 = a
    lat2, lon2 = b
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))


def nominatim_search(query: str, limit: int = 3) -> List[Dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "format": "json",
            "addressdetails": 1,
            "limit": limit,
        }
    )
    url = f"{NOMINATIM}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def summarize_hit(hit: Dict[str, Any]) -> str:
    lat = float(hit["lat"])
    lon = float(hit["lon"])
    name = hit.get("display_name", "")[:90]
    d_shop = haversine_m((lat, lon), REF["booksy_shop"])
    d_ih = haversine_m((lat, lon), REF["iheart_340_townsend"])
    return (
        f"  -> {lat:.6f},{lon:.6f} | {d_shop:.0f}m to shop | "
        f"{d_ih:.0f}m to iHeart | {name}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare Nominatim queries (rate-limited)."
    )
    parser.add_argument("--query", action="append", help="Extra / only query")
    parser.add_argument(
        "--only-extra",
        action="store_true",
        help="Run only --query values, skip defaults",
    )
    args = parser.parse_args()

    queries = list(DEFAULT_QUERIES)
    if args.only_extra and args.query:
        queries = list(args.query)
    elif args.query:
        queries.extend(args.query)

    print("Reference pins (evidence, not Nominatim):")
    for k, (la, lo) in REF.items():
        print(f"  {k}: {la},{lo}")
    print()
    print("Nominatim forward searches (1 req/s):")
    print()

    for i, q in enumerate(queries):
        if i:
            time.sleep(SLEEP_SEC)
        print(f"QUERY: {q}")
        try:
            hits = nominatim_search(q)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            continue
        if not hits:
            print("  -> 0 hits")
        else:
            for h in hits:
                print(summarize_hit(h))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
