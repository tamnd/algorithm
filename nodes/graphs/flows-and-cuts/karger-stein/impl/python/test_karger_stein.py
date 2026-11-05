# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karger-stein/. The authors are listed in prov/QPM3H8.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from karger_stein import karger_stein, recursive_contract

# a, b, c, d, e, f = 0 .. 5 and g, h = 6, 7: two 4-cliques of weight 2, abcg and defh, joined by cd and be
EXAMPLE = (
    [(a, b, 2) for a, b in itertools.combinations([0, 1, 2, 6], 2)]
    + [(a, b, 2) for a, b in itertools.combinations([3, 4, 5, 7], 2)]
    + [(2, 3, 1), (1, 4, 1)]
)


def cut_value(edges, side):
    return sum(c for u, v, c in edges if (u in side) != (v in side))


def brute(n, edges):
    """Independent oracle: the least cut over all nonempty proper subsets holding vertex 0."""
    best = None
    for r in range(n - 1):
        for extra in itertools.combinations(range(1, n), r):
            c = cut_value(edges, {0, *extra})
            best = c if best is None else min(best, c)
    return best


def check(n, edges, value, side):
    assert 0 < len(side) < n
    assert cut_value(edges, side) == value


def test_example() -> None:
    value, side = karger_stein(8, EXAMPLE, rng=random.Random(1))
    assert value == 2
    assert side in ({0, 1, 2, 6}, {3, 4, 5, 7})


def test_one_run_succeeds_often() -> None:
    rng = random.Random(7)
    w = [[0] * 8 for _ in range(8)]
    for u, v, c in EXAMPLE:
        w[u][v] += c
        w[v][u] += c
    groups = [frozenset([v]) for v in range(8)]
    wins = sum(recursive_contract(w, groups, rng)[0] == 2 for _ in range(2000))
    # the proof guarantees 2 / (D + 2) = 1/2 for this graph, whose recursion depth D is 2
    assert wins / 2000 > 0.5


def test_small_and_degenerate() -> None:
    assert karger_stein(2, [(0, 1, 3), (1, 0, 4)]) == (7, {0})
    assert karger_stein(2, []) == (0, {0})
    with pytest.raises(ValueError):
        karger_stein(1, [])
    with pytest.raises(ValueError):
        karger_stein(3, [(0, 1, -1)])


def test_disconnected_zero_weight_and_loops() -> None:
    edges = [(i, i + 1, 3) for i in range(5)] + [(i, i + 1, 3) for i in range(6, 11)] + [(5, 6, 0), (0, 0, 9)]
    value, side = karger_stein(12, edges, rng=random.Random(3))
    assert value == 0
    check(12, edges, value, side)


def test_cycle_and_real_weights() -> None:
    cycle = [(i, (i + 1) % 10, 1) for i in range(10)]
    assert karger_stein(10, cycle, rng=random.Random(5))[0] == 2
    rng = random.Random(11)
    edges = [(u, v, Fraction(rng.randint(1, 9), rng.randint(1, 9))) for u, v in itertools.combinations(range(8), 2)]
    value, side = karger_stein(8, edges, runs=30, rng=rng)
    assert value == brute(8, edges)
    check(8, edges, value, side)
    floats = [(u, v, c * 0.5) for u, v, c in cycle]
    assert karger_stein(10, floats, rng=rng)[0] == 1.0


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(2, 10)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 4)) for _ in range(rng.randint(0, 3 * n))]
        value, side = karger_stein(n, edges, runs=25, rng=rng)
        check(n, edges, value, side)
        assert value == brute(n, edges)
