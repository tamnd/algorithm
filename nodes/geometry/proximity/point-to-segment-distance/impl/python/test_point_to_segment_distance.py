# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-to-segment-distance/. The authors are listed in prov/XQG3E1.jsonl.

import random
from fractions import Fraction

import pytest

from point_to_segment_distance import (
    point_to_segment_distance,
    point_to_segment_distance_squared,
    point_to_segment_distance_squared_nd,
)


def test_example() -> None:
    a, b = (1, 1), (7, 9)
    assert point_to_segment_distance_squared((8, 2), a, b) == (25, (4, 5))
    assert point_to_segment_distance_squared((2, 7), a, b) == (
        Fraction(196, 25),
        (Fraction(106, 25), Fraction(133, 25)),
    )
    assert point_to_segment_distance_squared((10, 12), a, b) == (18, (7, 9))
    assert point_to_segment_distance_squared((-2, 0), a, b) == (10, (1, 1))
    assert point_to_segment_distance((8, 2), a, b) == pytest.approx(5.0)


def test_line_versus_segment_pitfall() -> None:
    # The line distance is 4, the segment distance is sqrt(20).
    assert point_to_segment_distance_squared((3, 4), (0, 0), (1, 0))[0] == 20


def test_degenerate_segment() -> None:
    assert point_to_segment_distance_squared((4, 5), (1, 1), (1, 1)) == (25, (1, 1))
    assert point_to_segment_distance_squared((1, 1), (1, 1), (1, 1)) == (0, (1, 1))


def test_endpoints_and_on_segment() -> None:
    a, b = (0, 0), (6, 0)
    assert point_to_segment_distance_squared((0, 0), a, b)[0] == 0
    assert point_to_segment_distance_squared((6, 0), a, b)[0] == 0
    assert point_to_segment_distance_squared((3, 0), a, b)[0] == 0
    assert point_to_segment_distance_squared((0, 5), a, b) == (25, (0, 0))
    assert point_to_segment_distance_squared((6, -5), a, b) == (25, (6, 0))


def oracle(p, a, b) -> Fraction:
    """Minimum of g over [0, 1] by evaluating g at 0, 1 and the vertex of the parabola when inside."""

    def g(t: Fraction) -> Fraction:
        x = a[0] + t * (b[0] - a[0])
        y = a[1] + t * (b[1] - a[1])
        return (p[0] - x) ** 2 + (p[1] - y) ** 2

    cands = [g(Fraction(0)), g(Fraction(1))]
    ux, uy = b[0] - a[0], b[1] - a[1]
    dd = ux * ux + uy * uy
    if dd:
        t = Fraction((p[0] - a[0]) * ux + (p[1] - a[1]) * uy, dd)
        if 0 <= t <= 1:
            cands.append(g(t))
    return min(cands)


def test_random_against_oracle() -> None:
    rng = random.Random(9031)
    for _ in range(3000):
        r = rng.choice([2, 5, 30])
        a = (rng.randint(-r, r), rng.randint(-r, r))
        b = (rng.randint(-r, r), rng.randint(-r, r))
        p = (rng.randint(-r, r), rng.randint(-r, r))
        d2, c = point_to_segment_distance_squared(p, a, b)
        assert d2 == oracle(p, a, b)
        assert d2 == (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2
        # c lies on the closed segment.
        ux, uy = b[0] - a[0], b[1] - a[1]
        assert (c[0] - a[0]) * uy - (c[1] - a[1]) * ux == 0
        assert min(a[0], b[0]) <= c[0] <= max(a[0], b[0])
        assert min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
        # No sampled point of the segment is closer.
        for _ in range(4):
            t = Fraction(rng.randint(0, 12), 12)
            q = (a[0] + t * ux, a[1] + t * uy)
            assert (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 >= d2
        assert point_to_segment_distance_squared_nd(p, a, b) == d2


def test_three_dimensions() -> None:
    rng = random.Random(55)
    for _ in range(500):
        a = [rng.randint(-5, 5) for _ in range(3)]
        b = [rng.randint(-5, 5) for _ in range(3)]
        p = [rng.randint(-5, 5) for _ in range(3)]
        best = None
        for k in range(0, 61):
            t = Fraction(k, 60)
            q = [x + t * (y - x) for x, y in zip(a, b)]
            v = sum((x - y) ** 2 for x, y in zip(p, q))
            best = v if best is None or v < best else best
        got = point_to_segment_distance_squared_nd(p, a, b)
        assert got <= best
