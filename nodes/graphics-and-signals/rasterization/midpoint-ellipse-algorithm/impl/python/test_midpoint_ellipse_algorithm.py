# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-ellipse-algorithm/. The authors are listed in prov/VKBD4R.jsonl.

import random
from fractions import Fraction
from math import isqrt

from midpoint_ellipse_algorithm import ellipse_quadrant, midpoint_ellipse

HALF = Fraction(1, 2)


def direct_rule(a: int, b: int) -> tuple[list[tuple[int, int]], list[int], int]:
    """The same two-region midpoint rule, with F and its gradient evaluated directly in Fraction.

    Returns the pixels, the region of each pixel (1, 2, or 3 for the run on the x-axis) and the number of ties.
    """

    def f(x: Fraction, y: Fraction) -> Fraction:
        return b * b * x * x + a * a * y * y - a * a * b * b

    x, y, ties = 0, b, 0
    pts, reg = [(x, y)], [1]
    # region 1 while the gradient (2 b^2 X, 2 a^2 Y) at the midpoint (x + 1, y - 1/2) has the larger y part
    while 2 * a * a * (y - HALF) > 2 * b * b * (x + 1):
        v = f(Fraction(x + 1), y - HALF)
        ties += v == 0
        if v >= 0:
            y -= 1
        x += 1
        pts.append((x, y))
        reg.append(1)
    while y > 0:
        v = f(x + HALF, Fraction(y - 1))
        ties += v == 0
        if v < 0:
            x += 1
        y -= 1
        pts.append((x, y))
        reg.append(2)
    while x < a:
        x += 1
        pts.append((x, 0))
        reg.append(3)
    return pts, reg, ties


def col_nearest(a: int, b: int, x: int) -> int:
    """The row of the pixel nearest to the ellipse in column x, 0 <= x <= a, a >= 1, ties to the inner pixel.

    It is the smallest y >= 0 with F(x, y + 1/2) >= 0, in exact integers.
    """
    n = 4 * b * b * (a * a - x * x)
    y = max(0, (isqrt(n // (a * a)) - 1) // 2 - 1)
    while a * a * (2 * y + 1) ** 2 < n:
        y += 1
    return y


def row_nearest(a: int, b: int, y: int) -> int:
    return col_nearest(b, a, y)


def labels(a: int, b: int, pts: list[tuple[int, int]]) -> list[int]:
    """The region of each pixel: the loop of line L3 runs while its test holds at the last pixel."""
    k = 0
    while a * a * (2 * pts[k][1] - 1) > 2 * b * b * (pts[k][0] + 1):
        k += 1
    m = k
    while pts[m][1] > 0:
        m += 1
    return [1] * (k + 1) + [2] * (m - k) + [3] * (len(pts) - m - 1)


def cases(seed: int, count: int, top: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    out = [(a, b) for a in range(1, 31) for b in range(1, 31)]
    out += [(rng.randint(1, top), rng.randint(1, top)) for _ in range(count)]
    out += [(rng.randint(50, top), rng.randint(1, 6)) for _ in range(50)]
    return out


def test_examples() -> None:
    assert ellipse_quadrant(8, 5) == [(0, 5), (1, 5), (2, 5), (3, 5), (4, 4), (5, 4), (6, 3), (7, 2), (8, 1), (8, 0)]
    # the switch comes one column early: (6, 4) where the nearest pixel in row 4 is (7, 4)
    assert ellipse_quadrant(8, 7) == [(0, 7), (1, 7), (2, 7), (3, 6), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (8, 1), (8, 0)]
    assert row_nearest(8, 7, 4) == 7 and col_nearest(8, 7, 6) == 5
    # for a = b = 4 the corner pixel (3, 3) of the midpoint circle is missing
    assert ellipse_quadrant(4, 4) == [(0, 4), (1, 4), (2, 3), (3, 2), (4, 1), (4, 0)]
    # a flat ellipse: region 1 reaches row 0 at x = 13, and line L12 adds the tip
    assert ellipse_quadrant(15, 1)[-4:] == [(12, 1), (13, 0), (14, 0), (15, 0)]
    assert ellipse_quadrant(0, 0) == [(0, 0)]
    assert ellipse_quadrant(0, 3) == [(0, 3), (0, 2), (0, 1), (0, 0)]
    assert ellipse_quadrant(3, 0) == [(0, 0), (1, 0), (2, 0), (3, 0)]
    sizes = {(8, 5): 36, (100, 50): 448, (1000, 500): 4472, (640, 480): 3200}
    for (a, b), k in sizes.items():
        assert len(midpoint_ellipse(0, 0, a, b)) == k
    assert midpoint_ellipse(4, -7, 6, 3) == sorted((4 + x, -7 + y) for x, y in midpoint_ellipse(0, 0, 6, 3))


def test_same_rule_evaluated_directly() -> None:
    small = [(a, b) for a in range(0, 31) for b in range(0, 31)]
    rng = random.Random(1984)
    for a, b in small + [(rng.randint(1, 150), rng.randint(1, 150)) for _ in range(500)]:
        pts, _, ties = direct_rule(a, b)
        assert ellipse_quadrant(a, b) == pts
        # the midpoint is never on the ellipse when a and b are integers, so the tie rule is never used
        assert ties == 0


def test_nearest_pixels_and_the_switch() -> None:
    for a, b in cases(1985, 500, 1500):
        pts = ellipse_quadrant(a, b)
        reg = labels(a, b, pts)
        if a + b <= 60:
            assert reg == direct_rule(a, b)[1]
        last1 = max(i for i, r in enumerate(reg) if r == 1)
        caught = False
        for i, ((x, y), r) in enumerate(zip(pts, reg)):
            if r == 1 and i < last1:
                assert y == col_nearest(a, b, x)
            elif r == 1:
                assert y == col_nearest(a, b, x) or x == row_nearest(a, b, y)
            elif r == 2:
                rx = row_nearest(a, b, y)
                assert x in (rx - 1, rx)
                assert not (caught and x != rx)
                caught = caught or x == rx
            else:
                assert y == 0 and col_nearest(a, b, x) == 0


def test_chain_symmetry_and_end() -> None:
    for a, b in cases(1986, 500, 1000):
        pts = ellipse_quadrant(a, b)
        assert pts[0] == (0, b) and pts[-1] == (a, 0)
        assert len(pts) <= a + b + 1
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            assert (x1 - x0, y0 - y1) in ((1, 0), (0, 1), (1, 1))
    for a in range(1, 30):
        for b in range(1, 30):
            s = set(midpoint_ellipse(0, 0, a, b))
            assert all((-x, y) in s and (x, -y) in s for x, y in s)
