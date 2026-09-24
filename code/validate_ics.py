#!/usr/bin/env python3
"""Validate booking-app ICS invites for geocode-safe LOCATION + GEO.

Fails (exit 1) when LOCATION looks like a bare street address and GEO is
missing. Warns when LOCATION has no shop/business name prefix.

Usage:
  python code/validate_ics.py code/testdata/*.ics
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Unfold RFC5545 line continuations (CRLF + space/tab).
_UNFOLD = re.compile(r"\r?\n[ \t]")

# Bare street-ish LOCATION: starts with house number, no leading business name.
_STREET_ONLY = re.compile(
    r"^\s*\d+[A-Za-z]?\s+[A-Za-z]",
    re.IGNORECASE,
)

# Common street tokens that appear in multi-tenant bare addresses.
_STREET_TOKENS = re.compile(
    r"\b(st|street|ave|avenue|rd|road|blvd|boulevard|ln|lane|dr|drive|way|ct|court)\b",
    re.IGNORECASE,
)


def unfold(raw: str) -> str:
    return _UNFOLD.sub("", raw.replace("\r\n", "\n"))


def parse_properties(text: str) -> Dict[str, List[str]]:
    """Map uppercase property name -> list of values (params stripped loosely)."""
    props: Dict[str, List[str]] = {}
    for line in unfold(text).split("\n"):
        line = line.strip("\r")
        if not line or line.startswith("BEGIN:") or line.startswith("END:"):
            continue
        if ":" not in line:
            continue
        name_part, value = line.split(":", 1)
        name = name_part.split(";", 1)[0].upper()
        props.setdefault(name, []).append(value)
    return props


def first(props: Dict[str, List[str]], key: str) -> Optional[str]:
    vals = props.get(key)
    return vals[0] if vals else None


def location_display(loc: str) -> str:
    """ICS escapes: \\n -> newline, \\, -> comma, etc."""
    return (
        loc.replace("\\n", "\n")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\\\", "\\")
    )


def is_street_only_location(loc: str) -> bool:
    """True if LOCATION looks like address text without a titled first line."""
    display = location_display(loc).strip()
    if not display:
        return True
    first_line = display.split("\n", 1)[0].strip()
    # Titled form: "Business Name" or "Business\nAddress"
    if _STREET_ONLY.match(first_line) and _STREET_TOKENS.search(first_line):
        return True
    # Single-line bare address with street token + house number somewhere
    if "\n" not in display and _STREET_ONLY.match(display):
        return True
    return False


def has_shop_name(loc: str) -> bool:
    display = location_display(loc).strip()
    if not display:
        return False
    first_line = display.split("\n", 1)[0].strip()
    # Shop name if first line does not start with a house number
    return not bool(_STREET_ONLY.match(first_line))


def has_geo(props: Dict[str, List[str]]) -> bool:
    geo = first(props, "GEO")
    if geo and re.match(r"^-?\d+(\.\d+)?;-?\d+(\.\d+)?$", geo.strip()):
        return True
    # Apple structured location often carries geo:lat,lon
    for key, vals in props.items():
        if key.startswith("X-APPLE-STRUCTURED-LOCATION"):
            for v in vals:
                if "geo:" in v.lower():
                    return True
        # Name may include params: X-APPLE-STRUCTURED-LOCATION;VALUE=URI;...
    # Also check raw keys that include params as part of name_part before split
    for k, vals in props.items():
        if "X-APPLE-STRUCTURED-LOCATION" in k:
            for v in vals:
                if re.search(r"geo:-?\d", v, re.I):
                    return True
    return False


def validate_file(path: Path) -> Tuple[bool, List[str], List[str]]:
    """Return (ok, errors, warnings)."""
    errors: List[str] = []
    warnings: List[str] = []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, [f"cannot read: {e}"], []

    if "BEGIN:VEVENT" not in raw:
        errors.append("no VEVENT found")
        return False, errors, warnings

    props = parse_properties(raw)
    loc = first(props, "LOCATION")
    if loc is None:
        errors.append("missing LOCATION")
        return False, errors, warnings

    street_only = is_street_only_location(loc)
    geo_ok = has_geo(props)

    if street_only and not geo_ok:
        errors.append(
            "LOCATION is street-only and GEO / X-APPLE-STRUCTURED-LOCATION "
            "geo pin is missing (Calendar will re-geocode the bare address)"
        )

    if not has_shop_name(loc):
        warnings.append(
            "LOCATION has no shop/business name on the first line "
            "(prefer 'Shop Name\\nUnit address' over bare street)"
        )

    if not geo_ok:
        warnings.append("no GEO property (and no geo: in X-APPLE-STRUCTURED-LOCATION)")

    ok = len(errors) == 0
    return ok, errors, warnings


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail if ICS LOCATION is street-only without GEO."
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="One or more .ics files",
    )
    args = parser.parse_args(argv)

    exit_code = 0
    for path in args.files:
        ok, errors, warnings = validate_file(path)
        status = "PASS" if ok else "FAIL"
        print(f"{status}  {path}")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN:  {w}")
        if not ok:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
