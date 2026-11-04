# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geohash/. The authors are listed in prov/CF8HNQ.jsonl.

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
_INDEX = {c: i for i, c in enumerate(BASE32)}


def geohash_encode(lat: float, lon: float, p: int) -> str:
    """Return the geohash of (lat, lon) with p base-32 characters.

    Precondition: -90 <= lat <= 90, -180 <= lon <= 180, p >= 0.
    The bits alternate between longitude (first) and latitude. A value equal
    to the midpoint of its interval goes to the upper half. Cost: Theta(p).
    All midpoints are dyadic fractions of 180 and 360, so they are exact in
    binary floating point for p up to 18.
    """
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0) or p < 0:
        raise ValueError("latitude, longitude or precision out of range")
    lat_lo, lat_hi = -90.0, 90.0  # @line L1
    lon_lo, lon_hi = -180.0, 180.0
    s: list[str] = []  # @line L2
    bits, ch, even = 0, 0, True
    while len(s) < p:  # @line L3
        if even:  # @line L4
            mid = (lon_lo + lon_hi) / 2
            if lon >= mid:
                ch, lon_lo = 2 * ch + 1, mid
            else:
                ch, lon_hi = 2 * ch, mid
        else:
            mid = (lat_lo + lat_hi) / 2  # @line L5
            if lat >= mid:
                ch, lat_lo = 2 * ch + 1, mid
            else:
                ch, lat_hi = 2 * ch, mid
        even = not even  # @line L6
        bits += 1
        if bits == 5:  # @line L7
            s.append(BASE32[ch])
            bits, ch = 0, 0
    return "".join(s)  # @line L8


def geohash_decode(h: str) -> tuple[float, float, float, float]:
    """Return the cell (lat_lo, lat_hi, lon_lo, lon_hi) of the geohash h.

    Raises ValueError on a character outside the alphabet. Cost: Theta(|h|).
    """
    lat_lo, lat_hi = -90.0, 90.0
    lon_lo, lon_hi = -180.0, 180.0
    even = True
    for c in h.lower():
        if c not in _INDEX:
            raise ValueError(f"not a geohash character: {c!r}")
        v = _INDEX[c]
        for k in range(4, -1, -1):
            bit = (v >> k) & 1
            if even:
                mid = (lon_lo + lon_hi) / 2
                if bit:
                    lon_lo = mid
                else:
                    lon_hi = mid
            else:
                mid = (lat_lo + lat_hi) / 2
                if bit:
                    lat_lo = mid
                else:
                    lat_hi = mid
            even = not even
    return lat_lo, lat_hi, lon_lo, lon_hi


def geohash_center(h: str) -> tuple[float, float]:
    """Return the center (lat, lon) of the cell of h."""
    a, b, c, d = geohash_decode(h)
    return (a + b) / 2, (c + d) / 2
