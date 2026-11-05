# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mpm-algorithm/. The authors are listed in prov/QQPNK1.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from mpm_algorithm import mpm

# s, a, b, c, d, t = 0 .. 5
EXAMPLE = [(0, 1, 10), (0, 2, 10), (1, 2, 2), (1, 3, 4), (1, 4, 8), (2, 4, 9), (4, 3, 6), (3, 5, 10), (4, 5, 10)]


def cut_capacity(edges, side):
    return sum(c for u, v, c in edges if u in side and v not in side)


def brute_min_cut(n, edges, s, t):
    """Independent oracle: the least capacity over all s-t cuts."""
    others = [v for v in range(n) if v not in (s, t)]
    best = None
    for r in range(len(others) + 1):
        for extra in itertools.combinations(others, r):
            c = cut_capacity(edges, {s, *extra})
            best = c if best is None else min(best, c)
    return best


def check(n, edges, s, t, value, flow, side):
    net = [0] * n
    for (u, v, c), x in zip(edges, flow):
        assert 0 <= x <= c
        net[u] -= x
        net[v] += x
    for v in range(n):
        if v not in (s, t):
            assert net[v] == 0
    assert net[t] == value == -net[s]
    assert s in side and t not in side
    assert cut_capacity(edges, side) == value


def test_example() -> None:
    value, flow, side = mpm(6, EXAMPLE, 0, 5)
    assert value == 19
    assert side == {0, 2}
    check(6, EXAMPLE, 0, 5, value, flow, side)


def test_zero_capacity_and_no_path() -> None:
    edges = [(0, 1, 0), (1, 2, 5)]
    assert mpm(3, edges, 0, 2) == (0, [0, 0], {0})
    edges = [(0, 1, 4), (2, 3, 4)]
    value, flow, side = mpm(4, edges, 0, 3)
    assert (value, side) == (0, {0, 1})
    with pytest.raises(ValueError):
        mpm(2, [], 0, 0)
    with pytest.raises(ValueError):
        mpm(2, [(0, 1, -1)], 0, 1)


def test_antiparallel_parallel_and_loops() -> None:
    edges = [(0, 1, 3), (1, 0, 2), (0, 1, 1), (1, 2, 3), (2, 1, 7), (1, 1, 5)]
    value, flow, side = mpm(3, edges, 0, 2)
    assert value == 3
    check(3, edges, 0, 2, value, flow, side)


def test_real_capacities() -> None:
    edges = [(0, 1, Fraction(1, 3)), (0, 2, Fraction(1, 2)), (1, 2, Fraction(1, 7)), (1, 3, Fraction(1, 5)), (2, 3, Fraction(2, 3))]
    value, flow, side = mpm(4, edges, 0, 3)
    assert value == brute_min_cut(4, edges, 0, 3) == Fraction(5, 6)
    check(4, edges, 0, 3, value, flow, side)


def test_random_against_brute_force() -> None:
    rng = random.Random(31)
    for _ in range(800):
        n = rng.randint(2, 7)
        s, t = rng.sample(range(n), 2)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 6)) for _ in range(rng.randint(0, 3 * n))]
        value, flow, side = mpm(n, edges, s, t)
        assert value == brute_min_cut(n, edges, s, t)
        check(n, edges, s, t, value, flow, side)
