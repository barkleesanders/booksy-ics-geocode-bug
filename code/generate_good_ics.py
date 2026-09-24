#!/usr/bin/env python3
"""Emit a geocode-safe sample ICS for The Closer Shave / Your Barber Juan.

Coords are Booksy's published JSON-LD pin (not invented):
  37.7797680906372, -122.39454645283753

Usage:
  python code/generate_good_ics.py > /tmp/closer-shave.ics
  python code/generate_good_ics.py --out code/testdata/good_invite.ics
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Evidence: Booksy HairSalon JSON-LD for business 1710466
SHOP_LAT = 37.7797680906372
SHOP_LON = -122.39454645283753
SHOP_TITLE = "The Closer Shave"
SHOP_BARBER = "Your Barber Juan"
SHOP_ADDRESS = "411 Brannan St Unit A, San Francisco, CA 94107"
SHOP_LOCATION_MULTILINE = (
    f"{SHOP_TITLE} - {SHOP_BARBER}\\n"
    "411 Brannan St Unit A\\n"
    "San Francisco\\, CA 94107"
)


def ics_escape_text(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")


def fold_line(line: str, limit: int = 75) -> str:
    """RFC5545 line folding at 75 octets (approx chars for ASCII)."""
    if len(line) <= limit:
        return line
    parts = [line[:limit]]
    rest = line[limit:]
    while rest:
        parts.append(" " + rest[: limit - 1])
        rest = rest[limit - 1 :]
    return "\r\n".join(parts)


def build_vevent(
    uid: str,
    dtstart: datetime,
    duration_min: int = 45,
    summary: str = "Haircut with Your Barber Juan",
) -> str:
    dtend = dtstart + timedelta(minutes=duration_min)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fmt = "%Y%m%dT%H%M%SZ"
    geo = f"{SHOP_LAT:.6f};{SHOP_LON:.6f}"
    geo_uri = f"geo:{SHOP_LAT:.6f},{SHOP_LON:.6f}"
    x_addr = ics_escape_text(SHOP_ADDRESS)
    x_title = ics_escape_text(SHOP_TITLE)

    structured = (
        "X-APPLE-STRUCTURED-LOCATION;VALUE=URI;"
        f"X-ADDRESS={x_addr};"
        "X-APPLE-RADIUS=50;"
        f"X-TITLE={x_title}:{geo_uri}"
    )

    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{stamp}",
        f"DTSTART:{dtstart.strftime(fmt)}",
        f"DTEND:{dtend.strftime(fmt)}",
        f"SUMMARY:{ics_escape_text(summary)}",
        (
            "DESCRIPTION:Appointment at The Closer Shave (Your Barber Juan)\\n"
            + ics_escape_text(SHOP_ADDRESS)
        ),
        f"LOCATION:{SHOP_LOCATION_MULTILINE}",
        f"GEO:{geo}",
        structured,
        "STATUS:CONFIRMED",
        "SEQUENCE:0",
        "END:VEVENT",
    ]
    return "\r\n".join(fold_line(L) for L in lines)


def build_calendar(vevent: str) -> str:
    head = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Booksy-ICS-Geocode-Bug/Demo//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:REQUEST",
    ]
    tail = ["END:VCALENDAR"]
    body = "\r\n".join(head) + "\r\n" + vevent + "\r\n" + "\r\n".join(tail) + "\r\n"
    return body


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate good sample ICS")
    parser.add_argument(
        "--out",
        type=Path,
        help="Write to file instead of stdout",
    )
    parser.add_argument(
        "--start",
        default="2026-09-24T21:15:00Z",
        help="UTC start time ISO8601 (default: sample slot)",
    )
    args = parser.parse_args()

    start = datetime.fromisoformat(args.start.replace("Z", "+00:00"))
    vevent = build_vevent(
        uid="booksy-example-good-closer-shave@example.com",
        dtstart=start,
    )
    ics = build_calendar(vevent)

    if args.out:
        args.out.write_text(ics, encoding="utf-8")
        print(f"wrote {args.out}", flush=True)
    else:
        # stdout: use LF for terminal readability; file write keeps CRLF
        print(ics.replace("\r\n", "\n"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
