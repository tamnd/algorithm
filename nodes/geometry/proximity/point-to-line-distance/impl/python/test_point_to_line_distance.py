# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-to-line-distance/. The authors are listed in prov/SVW2VD.jsonl.

import random
from fractions import Fraction

import pytest

from point_to_line_distance import (
    point_to_line_distance,
    point_to_line_distance_squared,
    point_to_line_distance_squared_nd,
    signed_area2,
)


def test_example() -> None:
    a, b = (1, 1), (7, 9)
    d2, f = point_to_line_distance_squared((8, 2), a, b)
    assert d2 == 25 and f == (4, 5)
    d2, f = point_to_line_distance_squared((2, 7), a, b)
    assert d2 == Fraction(196, 25) and f == (Fraction(106, 25), Fraction(133, 25))
    assert point_to_line_distance((2, 7), a, b) == pytest.approx(2.8)
    assert signed_area2((8, 2), a, b) < 0 < signed_area2((2, 7), a, b)


def test_line_form_agrees() -> None:
    # 4x - 3y - 1 = 0 is the line through (1, 1) and (7, 9).
    for p in [(8, 2), (2, 7), (0, 0), (-5, 3), (1, 1)]:
        v = 4 * p[0] - 3 * p[1] - 1
        assert point_to_line_distance_squared(p, (1, 1), (7, 9))[0] == Fraction(v * v, 25)


def test_degenerate_line() -> None:
    with pytest.raises(ValueError):
        point_to_line_distance_squared((1, 2), (3, 3), (3, 3))


def test_point_on_line_and_axis_lines() -> None:
    assert point_to_line_distance_squared((5, 5), (0, 0), (1, 1))[0] == 0
    assert point_to_line_distance_squared((3, 4), (0, 0), (1, 0)) == (16, (3, 0))
    assert point_to_line_distance_squared((3, 4), (0, -2), (0, 9)) == (9, (0, 4))


def test_large_coordinates_exact() -> None:
    # Distances that a float root cannot tell apart.
    a, b = (0, 0), (10**9, 0)
    d1 = point_to_line_distance_squared((5, 10**8), a, b)[0]
    d2 = point_to_line_distance_squared((5, 10**8 + 1), a, b)[0]
    assert d1 < d2 and d2 - d1 == 2 * 10**8 + 1


def test_random_against_foot_characterization() -> None:
    # The foot f is the unique point on the line with (p - f) orthogonal to the line.
    rng = random.Random(4101)
    for _ in range(2000):
        a = (rng.randint(-20, 20), rng.randint(-20, 20))
        b = (rng.randint(-20, 20), rng.randint(-20, 20))
        if a == b:
            continue
        p = (rng.randint(-20, 20), rng.randint(-20, 20))
        d2, f = point_to_line_distance_squared(p, a, b)
        ux, uy = b[0] - a[0], b[1] - a[1]
        assert (f[0] - a[0]) * uy - (f[1] - a[1]) * ux == 0
        assert (p[0] - f[0]) * ux + (p[1] - f[1]) * uy == 0
        assert d2 == (p[0] - f[0]) ** 2 + (p[1] - f[1]) ** 2
        assert d2 == point_to_line_distance_squared_nd(p, a, b)
        # No sampled point of the line is closer than the foot.
        for _ in range(5):
            t = Fraction(rng.randint(-40, 40), rng.randint(1, 9))
            q = (a[0] + t * ux, a[1] + t * uy)
            assert (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 >= d2


def test_three_dimensions() -> None:
    # Line along the z-axis: distance is the length in the xy-plane.
    assert point_to_line_distance_squared_nd((3, 4, 7), (0, 0, 0), (0, 0, 2)) == 25
    rng = random.Random(77)
    for _ in range(500):
        a = [rng.randint(-9, 9) for _ in range(3)]
        b = [rng.randint(-9, 9) for _ in range(3)]
        if a == b:
            continue
        p = [rng.randint(-9, 9) for _ in range(3)]
        u = [y - x for x, y in zip(a, b)]
        w = [y - x for x, y in zip(a, p)]
        cr = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        expect = Fraction(sum(x * x for x in cr), sum(x * x for x in u))
        assert point_to_line_distance_squared_nd(p, a, b) == expect
