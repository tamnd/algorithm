# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wu-line-algorithm/. The authors are listed in prov/ZEVX63.jsonl.

import math
import random
from fractions import Fraction

from wu_line_algorithm import wu_line, wu_line_any, wu_line_exact


def as_map(pts: list[tuple[int, int, Fraction]]) -> dict[tuple[int, int], Fraction]:
    m: dict[tuple[int, int], Fraction] = {}
    for x, y, a in pts:
        assert (x, y) not in m
        if a:
            m[(x, y)] = a
    return m


def tent(x0: int, y0: int, x1: int, y1: int) -> dict[tuple[int, int], Fraction]:
    """Brute force: each pixel (x, j) of an inner column gets max(0, 1 - |j - Y(x)|), the endpoints get 1."""
    m = {(x0, y0): Fraction(1), (x1, y1): Fraction(1)}
    for x in range(x0 + 1, x1):
        exact_y = y0 + Fraction((y1 - y0) * (x - x0), x1 - x0)
        for j in range(math.floor(exact_y) - 2, math.floor(exact_y) + 3):  # the tent is 0 farther away
            a = 1 - abs(j - exact_y)
            if a > 0:
                m[(x, j)] = a
    return m


def first_octant(rng: random.Random) -> tuple[int, int, int, int]:
    x0, y0 = rng.randint(-50, 50), rng.randint(-50, 50)
    dx = rng.randint(1, 60)
    return x0, y0, x0 + dx, y0 + rng.randint(0, dx)


def test_example() -> None:
    m = as_map(wu_line(0, 0, 5, 2, w=8))
    want = {(0, 0): 256, (5, 2): 256, (1, 0): 154, (1, 1): 102, (2, 0): 52, (2, 1): 204,
            (3, 1): 206, (3, 2): 50, (4, 1): 104, (4, 2): 152}
    assert m == {p: Fraction(v, 256) for p, v in want.items()}
    exact = as_map(wu_line_exact(0, 0, 5, 2))
    assert exact == tent(0, 0, 5, 2)
    assert exact[(1, 0)] == Fraction(3, 5) and exact[(2, 1)] == Fraction(4, 5)


def test_edges() -> None:
    assert wu_line_any(2, 3, 2, 3) == [(2, 3, Fraction(1))]
    assert as_map(wu_line(0, 0, 1, 0)) == {(0, 0): 1, (1, 0): 1}
    assert as_map(wu_line(0, 0, 4, 0)) == {(i, 0): 1 for i in range(5)}
    assert as_map(wu_line(0, 0, 4, 4)) == {(i, i): 1 for i in range(5)}
    assert as_map(wu_line_any(0, 0, 0, -3)) == {(0, -i): 1 for i in range(4)}


def test_exact_form_equals_tent() -> None:
    rng = random.Random(1991)
    for _ in range(500):
        x0, y0, x1, y1 = first_octant(rng)
        assert as_map(wu_line_exact(x0, y0, x1, y1)) == tent(x0, y0, x1, y1)


def test_fixed_point_error_bound() -> None:
    rng = random.Random(5)
    for _ in range(500):
        x0, y0, x1, y1 = first_octant(rng)
        w = rng.randint(4, 20)
        got = as_map(wu_line(x0, y0, x1, y1, w))
        ref = tent(x0, y0, x1, y1)
        for p in set(got) | set(ref):
            i = p[0] - x0
            assert abs(got.get(p, 0) - ref.get(p, 0)) <= Fraction(i, 2 ** (w + 1))


def test_fixed_point_invariant_and_column_sums() -> None:
    rng = random.Random(11)
    for _ in range(500):
        x0, y0, x1, y1 = first_octant(rng)
        w = rng.randint(1, 16)
        d = math.floor(Fraction((y1 - y0) * 2**w, x1 - x0) + Fraction(1, 2))
        pts = wu_line(x0, y0, x1, y1, w)
        for k in range(2, len(pts), 2):
            (x, y, a), (_, y2, b) = pts[k], pts[k + 1]
            assert y2 == y + 1 and a + b == 1
            assert y + b == y0 + Fraction((x - x0) * d, 2**w)


def tent_any(x0: int, y0: int, x1: int, y1: int) -> dict[tuple[int, int], Fraction]:
    """Brute force tent weights for any direction: step the major axis, weight the minor axis."""
    m = {(x0, y0): Fraction(1), (x1, y1): Fraction(1)}
    steep = abs(y1 - y0) > abs(x1 - x0)
    a0, b0, a1, b1 = (y0, x0, y1, x1) if steep else (x0, y0, x1, y1)
    lo, hi = min(a0, a1), max(a0, a1)
    for a in range(lo + 1, hi):
        exact_b = b0 + Fraction((b1 - b0) * (a - a0), a1 - a0)
        for j in range(math.floor(exact_b) - 2, math.floor(exact_b) + 3):
            v = 1 - abs(j - exact_b)
            if v > 0:
                m[(j, a) if steep else (a, j)] = v
    return m


def test_all_octants() -> None:
    rng = random.Random(8)
    for _ in range(500):
        x0, y0, x1, y1 = (rng.randint(-30, 30) for _ in range(4))
        if (x0, y0) != (x1, y1):
            assert as_map(wu_line_any(x0, y0, x1, y1, exact=True)) == tent_any(x0, y0, x1, y1)
