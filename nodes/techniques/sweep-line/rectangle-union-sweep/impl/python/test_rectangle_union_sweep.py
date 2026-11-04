# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rectangle-union-sweep/. The authors are listed in prov/4TVWVM.jsonl.

import random

from rectangle_union_sweep import union_area


def brute(rects):
    """Sum the cells of the grid of all coordinates whose center lies in some rectangle."""
    xs = sorted({r[0] for r in rects} | {r[2] for r in rects})
    ys = sorted({r[1] for r in rects} | {r[3] for r in rects})
    total = 0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx, cy = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if any(r[0] <= cx <= r[2] and r[1] <= cy <= r[3] for r in rects):
                total += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return total


def test_example() -> None:
    assert union_area([(1, 1, 4, 3), (2, 2, 6, 5), (5, 0, 7, 2)]) == 20


def test_edges() -> None:
    assert union_area([]) == 0
    assert union_area([(0, 0, 3, 2)]) == 6
    assert union_area([(0, 0, 3, 2), (0, 0, 3, 2)]) == 6  # identical
    assert union_area([(0, 0, 10, 10), (2, 2, 3, 3)]) == 100  # nested
    assert union_area([(0, 0, 1, 1), (1, 0, 2, 1)]) == 2  # touching edge
    assert union_area([(0, 0, 0, 5), (1, 1, 1, 1)]) == 0  # degenerate
    assert union_area([(0, 4, 10, 5), (4, 0, 5, 10)]) == 19  # cross
    big = 10**12
    assert union_area([(0, 0, big, big), (big // 2, 0, 2 * big, big)]) == 2 * big * big
    assert abs(union_area([(0.0, 0.0, 0.5, 0.5), (0.25, 0.25, 1.0, 1.0)]) - 0.75) < 1e-12


def test_against_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(1500):
        rects = []
        for _ in range(rng.randrange(0, 8)):
            x1, y1 = rng.randrange(10), rng.randrange(10)
            rects.append((x1, y1, x1 + rng.randrange(0, 5), y1 + rng.randrange(0, 5)))
        got = union_area(rects)
        assert got == brute(rects)
        assert isinstance(got, int)
