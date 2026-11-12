# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-circle-algorithm/. The authors are listed in prov/MR2G6P.jsonl.

import random
from fractions import Fraction

from midpoint_circle_algorithm import circle_octant, midpoint_circle


def direct_rule(r: int) -> list[tuple[int, int]]:
    """The same midpoint rule, with F(x + 1, y - 1/2) evaluated directly in Fraction at each step."""
    x, y, out = 0, r, []
    while x <= y:
        out.append((x, y))
        f = (x + 1) ** 2 + (y - Fraction(1, 2)) ** 2 - r * r
        assert f != 0
        if f > 0:
            y -= 1
        x += 1
    return out


def connected8(pts: set[tuple[int, int]]) -> bool:
    start = next(iter(pts))
    seen, stack = {start}, [start]
    while stack:
        x, y = stack.pop()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = (x + dx, y + dy)
                if q in pts and q not in seen:
                    seen.add(q)
                    stack.append(q)
    return len(seen) == len(pts)


def test_examples() -> None:
    assert circle_octant(0) == [(0, 0)]
    assert midpoint_circle(0, 0, 0) == [(0, 0)]
    assert circle_octant(1) == [(0, 1)]
    assert circle_octant(3) == [(0, 3), (1, 3), (2, 2)]
    assert circle_octant(10) == [(0, 10), (1, 10), (2, 10), (3, 10), (4, 9), (5, 9), (6, 8), (7, 7)]
    sizes = {1: 4, 2: 12, 3: 16, 5: 28, 8: 44, 10: 56, 100: 564, 1000: 5656}
    for r, k in sizes.items():
        assert len(midpoint_circle(0, 0, r)) == k
    assert circle_octant(100)[-1] == (70, 71)


def test_center_offset() -> None:
    assert midpoint_circle(5, -3, 2) == sorted((5 + x, -3 + y) for x, y in midpoint_circle(0, 0, 2))


def test_same_rule_evaluated_directly() -> None:
    for r in range(0, 400):
        assert circle_octant(r) == direct_rule(r)


def test_nearest_pixel_in_each_column() -> None:
    rng = random.Random(1977)
    radii = list(range(0, 300)) + [rng.randint(300, 20000) for _ in range(200)]
    for r in radii:
        oct_ = circle_octant(r)
        assert [x for x, _ in oct_] == list(range(len(oct_)))
        for x, y in oct_:
            t = 4 * (r * r - x * x)
            assert (2 * y - 1) ** 2 < t < (2 * y + 1) ** 2 or (r == 0 and y == 0)
            # the residual |x^2 + y^2 - r^2| is also smallest among y - 1, y, y + 1
            res = [abs(x * x + v * v - r * r) for v in (y - 1, y, y + 1)]
            assert res[1] < res[0] and res[1] < res[2]
        # the octant stops at the diagonal
        x, y = oct_[-1]
        assert y - x in (0, 1)


def test_symmetry_and_connectivity() -> None:
    for r in range(1, 120):
        pts = set(midpoint_circle(0, 0, r))
        assert all((y, x) in pts and (-x, y) in pts and (x, -y) in pts for x, y in pts)
        assert connected8(pts)
        assert all(abs(x * x + y * y - r * r) <= r for x, y in pts)
