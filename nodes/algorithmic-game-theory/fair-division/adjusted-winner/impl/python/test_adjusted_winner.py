# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjusted-winner/. The authors are listed in prov/8XAEP1.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from adjusted_winner import adjusted_winner, points

F = Fraction


def random_points(rng: random.Random, m: int) -> list[int]:
    cuts = sorted(rng.randint(0, 100) for _ in range(m - 1))
    edges = [0] + cuts + [100]
    return [edges[g + 1] - edges[g] for g in range(m)]


def equitable_po_value(pa, pb) -> Fraction:
    """A second method: walk along the goods in decreasing order of pA/pB.

    A takes a prefix of this order and B the rest, with one good split. The
    points of A grow and the points of B fall along the walk, so the walk
    meets equality once. Every point of the walk is Pareto optimal, and two
    agents have only one equitable Pareto optimal value.
    """
    m = len(pa)
    order = sorted(range(m), key=lambda g: (pb[g] == 0, F(pa[g], pb[g]) if pb[g] else F(0)), reverse=True)
    for j, g in enumerate(order):
        ua = sum(F(pa[h]) for h in order[:j])
        ub = sum(F(pb[h]) for h in order[j + 1 :])
        # with a share f of good g for A: ua + f pa[g] = ub + (1 - f) pb[g]
        if pa[g] + pb[g] == 0:
            continue
        f = (ub + pb[g] - ua) / (pa[g] + pb[g])
        if 0 <= f <= 1:
            return ua + f * pa[g]
    raise AssertionError("no equitable point on the walk")


def dominated_on_grid(pa, pb, s, steps: int) -> bool:
    """Brute force: does a share vector on the grid Pareto dominate s?"""
    ta, tb = points(pa, pb, s)
    grid = [F(k, steps) for k in range(steps + 1)]
    for y in itertools.product(grid, repeat=len(pa)):
        ya, yb = points(pa, pb, list(y))
        if ya >= ta and yb >= tb and (ya > ta or yb > tb):
            return True
    return False


def check(pa, pb, s) -> None:
    m = len(pa)
    assert len(s) == m and all(0 <= x <= 1 for x in s)
    assert sum(1 for x in s if 0 < x < 1) <= 1  # at most one good is split
    ta, tb = points(pa, pb, s)
    assert ta == tb  # equitable
    # envy-free: each agent values its own share at least as much as the other share
    assert ta >= 100 - ta and tb >= 100 - tb
    # Pareto optimal: an exchange certificate. No good g held (in part) by A
    # and good h held (in part) by B have pA(g) pB(h) < pA(h) pB(g).
    for g in range(m):
        for h in range(m):
            if s[g] > 0 and s[h] < 1:
                assert F(pa[g]) * pb[h] >= F(pa[h]) * pb[g] or (pa[g] == 0 and pb[g] == 0)
    assert ta == equitable_po_value(pa, pb)


def test_example() -> None:
    pa, pb = [50, 20, 15, 15], [40, 30, 10, 20]
    s = adjusted_winner(pa, pb)
    assert s == [F(5, 6), 0, 1, 0]
    assert points(pa, pb, s) == (F(170, 3), F(170, 3))
    check(pa, pb, s)
    assert not dominated_on_grid(pa, pb, s, 6)


def test_no_transfer_needed() -> None:
    pa, pb = [40, 30, 20, 10], [10, 20, 30, 40]
    s = adjusted_winner(pa, pb)
    assert s == [1, 1, 0, 0] and points(pa, pb, s) == (70, 70)


def test_identical_points() -> None:
    pa = [25, 25, 50]
    s = adjusted_winner(pa, pa)
    assert points(pa, pa, s) == (50, 50)
    check(pa, pa, s)


def test_zero_points() -> None:
    pa, pb = [100, 0, 0], [0, 0, 100]
    s = adjusted_winner(pa, pb)
    assert points(pa, pb, s) == (100, 100)
    pa, pb = [0, 60, 40], [50, 50, 0]
    s = adjusted_winner(pa, pb)
    check(pa, pb, s)


def test_random_against_brute_force() -> None:
    rng = random.Random(77)
    for _ in range(40):
        m = rng.randint(1, 4)
        pa, pb = random_points(rng, m), random_points(rng, m)
        s = adjusted_winner(pa, pb)
        check(pa, pb, s)
        assert not dominated_on_grid(pa, pb, s, 4)


def test_random_more_goods() -> None:
    rng = random.Random(78)
    for _ in range(300):
        m = rng.randint(1, 7)
        pa, pb = random_points(rng, m), random_points(rng, m)
        check(pa, pb, adjusted_winner(pa, pb))


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        adjusted_winner([50, 50], [100])
    with pytest.raises(ValueError):
        adjusted_winner([50, 40], [50, 50])
    with pytest.raises(ValueError):
        adjusted_winner([150, -50], [50, 50])
