# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-branch-and-bound/. The authors are listed in prov/AGSJXC.jsonl.

import random
from fractions import Fraction as F

import pytest

from interval_branch_and_bound import Interval, interval_branch_and_bound


def g(x):
    return (x[0] ** 2 - 2) ** 2 + x[0] - 4


def g_expanded(x):
    return x[0] ** 4 - 4 * x[0] ** 2 + x[0]


def inside(point, boxes):
    return any(all(lo <= p <= hi for p, (lo, hi) in zip(point, y)) for _, y in boxes)


def test_example_of_the_page() -> None:
    stats: dict[str, int] = {}
    lo, ub, xbest, boxes = interval_branch_and_bound(g, [(-3, 3)], F(1, 2), stats)
    assert (lo, ub, xbest) == (F(-93, 16), F(-87, 16), [F(-3, 2)])
    assert boxes == [(F(-93, 16), ((F(-15, 8), F(-3, 2)),)), (F(-11, 2), ((F(-3, 2), F(-9, 8)),))]
    assert stats == {"boxes": 8, "split": 6}


def test_expanded_form_is_looser() -> None:
    stats: dict[str, int] = {}
    lo, ub, _, boxes = interval_branch_and_bound(g_expanded, [(-3, 3)], F(1, 2), stats)
    assert lo == F(-87, 8) and ub == F(-87, 16)
    assert len(boxes) == 7 and stats == {"boxes": 20, "split": 13}


def test_small_eps_encloses_the_minimum() -> None:
    lo, ub, _, boxes = interval_branch_and_bound(g, [(-3, 3)], F(1, 1024))
    # The minimum is about -5.4441920 at x about -1.47299.
    assert lo <= F(-54441920, 10 ** 7) <= ub and ub - lo < F(1, 1000)
    assert inside([F(-147299, 100000)], boxes)


def test_interval_arithmetic() -> None:
    a = Interval(-1, 2)
    assert (a * a).lo == -2 and (a ** 2).lo == 0 and (a ** 2).hi == 4
    assert (a ** 3).lo == -1 and (a ** 3).hi == 8
    assert (3 - a).lo == 1 and (3 - a).hi == 4
    assert (Interval(-3, -2) ** 2).lo == 4
    with pytest.raises(ValueError):
        interval_branch_and_bound(g, [(0, 1)], 0)


def test_degenerate_box_and_constant() -> None:
    lo, ub, xbest, boxes = interval_branch_and_bound(g, [(1, 1)], F(1, 4))
    assert lo == ub == -2 and xbest == [1]
    lo, ub, _, boxes = interval_branch_and_bound(lambda x: 7 + 0 * x[0], [(-1, 1)], F(1, 2))
    assert lo == ub == 7


def test_two_global_minimizers() -> None:
    rng = random.Random(1979)
    for _ in range(300):
        a = F(rng.randint(-15, 15), 8)
        b = F(rng.randint(-15, 15), 8)
        c = F(rng.randint(-20, 20), 3)
        f = lambda x, a=a, b=b, c=c: (x[0] - a) ** 2 * (x[0] - b) ** 2 + c
        lo, ub, xbest, boxes = interval_branch_and_bound(f, [(-2, 2)], F(1, 8))
        assert lo <= c <= ub == f(xbest)
        assert inside([a], boxes) and inside([b], boxes)
        assert all(w <= ub for w, _ in boxes)


def test_two_dimensional_bowls() -> None:
    rng = random.Random(1980)
    for _ in range(150):
        a = F(rng.randint(-7, 7), 4)
        b = F(rng.randint(-7, 7), 4)
        c = rng.randint(-5, 5)
        f = lambda x, a=a, b=b, c=c: (x[0] - a) ** 2 + 2 * (x[1] - b) ** 2 + c + (x[0] - a) * (x[1] - b)
        lo, ub, xbest, boxes = interval_branch_and_bound(f, [(-2, 2), (-2, 2)], F(1, 4))
        assert lo <= c <= ub == f(xbest)
        assert inside([a, b], boxes)


def test_random_polynomials_against_grid() -> None:
    rng = random.Random(1966)
    for _ in range(150):
        coef = [F(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(rng.randint(1, 6))]

        def f(x, coef=coef):
            return sum((ck * x[0] ** k for k, ck in enumerate(coef)), F(0))

        lo, ub, xbest, boxes = interval_branch_and_bound(f, [(-2, 2)], F(1, 8))
        grid = [F(-2) + F(i, 50) for i in range(201)]
        values = [f([t]) for t in grid]
        assert lo <= min(values)
        assert ub == f(xbest) and -2 <= xbest[0] <= 2
        # A point outside every returned box lies in a discarded box, so its value is above the minimum.
        assert all(v > lo for t, v in zip(grid, values) if not inside([t], boxes))
        lo2, ub2, _, _ = interval_branch_and_bound(f, [(-2, 2)], F(1, 32))
        assert max(lo, lo2) <= min(ub, ub2, min(values))
