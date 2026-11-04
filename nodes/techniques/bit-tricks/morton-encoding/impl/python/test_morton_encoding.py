# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morton-encoding/. The authors are listed in prov/JEHNP6.jsonl.

import random

from morton_encoding import (
    compact,
    morton_decode,
    morton_encode,
    morton_encode3,
    spread,
    spread3,
)


def interleave(coords: list[int], b: int) -> int:
    """Oracle: bit i of coordinate j goes to bit d*i + j, one bit at a time."""
    d = len(coords)
    z = 0
    for i in range(b):
        for j, c in enumerate(coords):
            z |= ((c >> i) & 1) << (d * i + j)
    return z


def test_example() -> None:
    assert spread(181) == 0x4511
    assert spread(90) == 0x1144
    assert morton_encode(181, 90) == 0x6799 == 26521
    assert morton_decode(0x6799) == (181, 90)


def test_grid_4x4() -> None:
    rows = [[morton_encode(x, y) for x in range(4)] for y in range(4)]
    assert rows == [[0, 1, 4, 5], [2, 3, 6, 7], [8, 9, 12, 13], [10, 11, 14, 15]]


def test_spread_exhaustive_16_bits() -> None:
    for x in range(1 << 16):
        s = spread(x)
        assert s == interleave([x, 0], 16)
        assert compact(s) == x


def test_extremes() -> None:
    top = (1 << 32) - 1
    assert morton_encode(top, top) == (1 << 64) - 1
    assert morton_encode(top, 0) == 0x5555555555555555
    assert morton_encode(0, top) == 0xAAAAAAAAAAAAAAAA
    assert morton_decode((1 << 64) - 1) == (top, top)


def test_random_against_oracle() -> None:
    rng = random.Random(20261104)
    for _ in range(20000):
        x = rng.getrandbits(32)
        y = rng.getrandbits(32)
        z = morton_encode(x, y)
        assert z == interleave([x, y], 32)
        assert morton_decode(z) == (x, y)
    for _ in range(20000):
        z = rng.getrandbits(64)
        x, y = morton_decode(z)
        assert morton_encode(x, y) == z


def test_axis_order() -> None:
    rng = random.Random(7)
    for _ in range(5000):
        x, x2, y = rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32)
        if x < x2:
            assert morton_encode(x, y) < morton_encode(x2, y)


def test_three_coordinates_exhaustive_per_axis() -> None:
    for x in range(1 << 10):
        assert spread3(x) == interleave([x, 0, 0], 10)
    rng = random.Random(3)
    for _ in range(20000):
        c = [rng.getrandbits(10) for _ in range(3)]
        assert morton_encode3(*c) == interleave(c, 10)
