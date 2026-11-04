# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geohash/. The authors are listed in prov/CF8HNQ.jsonl.

import random
from fractions import Fraction

import pytest

from geohash import BASE32, geohash_center, geohash_decode, geohash_encode


def oracle(lat: float, lon: float, p: int) -> str:
    """Independent encoder: exact integer cell indices, then interleave."""
    nbits = 5 * p
    lon_bits = (nbits + 1) // 2
    lat_bits = nbits // 2
    xi = int((Fraction(lon) + 180) / 360 * 2**lon_bits)
    yi = int((Fraction(lat) + 90) / 180 * 2**lat_bits)
    xi = min(xi, 2**lon_bits - 1)
    yi = min(yi, 2**lat_bits - 1)
    out = []
    for k in range(nbits):
        if k % 2 == 0:
            out.append((xi >> (lon_bits - 1 - k // 2)) & 1)
        else:
            out.append((yi >> (lat_bits - 1 - k // 2)) & 1)
    chars = []
    for c in range(p):
        v = 0
        for b in out[5 * c : 5 * c + 5]:
            v = 2 * v + b
        chars.append(BASE32[v])
    return "".join(chars)


def test_page_example() -> None:
    assert geohash_encode(57.64911, 10.40744, 11) == "u4pruydqqvj"
    assert geohash_encode(57.64911, 10.40744, 2) == "u4"
    assert geohash_decode("u4") == (56.25, 61.875, 0.0, 11.25)


def test_boundary_example() -> None:
    assert geohash_encode(0.0001, 10.0, 6) == "s0p058"
    assert geohash_encode(-0.0001, 10.0, 6) == "kpzpgx"


def test_edges() -> None:
    assert geohash_encode(10.0, 20.0, 0) == ""
    assert geohash_encode(90.0, 180.0, 4) == "zzzz"
    assert geohash_encode(-90.0, -180.0, 4) == "0000"
    assert geohash_encode(0.0, 0.0, 1) == "s"
    with pytest.raises(ValueError):
        geohash_encode(91.0, 0.0, 3)
    with pytest.raises(ValueError):
        geohash_decode("ab")  # 'a' is not in the alphabet


def test_cell_sizes() -> None:
    lat_lo, lat_hi, lon_lo, lon_hi = geohash_decode("u09tunq")
    assert lat_hi - lat_lo == 180 / 2**17
    assert lon_hi - lon_lo == 360 / 2**18


def test_random_against_oracle() -> None:
    rng = random.Random(4096)
    for _ in range(2000):
        lat = rng.uniform(-90, 90)
        lon = rng.uniform(-180, 180)
        if rng.random() < 0.2:  # land on grid lines on purpose
            lat = round(lat / 11.25) * 11.25
            lon = round(lon / 22.5) * 22.5
        p = rng.randint(0, 12)
        h = geohash_encode(lat, lon, p)
        assert h == oracle(lat, lon, p)
        # the point lies in its cell, and shorter hashes are prefixes
        a, b, c, d = geohash_decode(h)
        assert a <= lat <= b and c <= lon <= d
        for q in range(p + 1):
            assert geohash_encode(lat, lon, q) == h[:q]
        if p:
            clat, clon = geohash_center(h)
            assert geohash_encode(clat, clon, p) == h
