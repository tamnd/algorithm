# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stoer-wagner/. The authors are listed in prov/M60CT8.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from stoer_wagner import stoer_wagner

# a, b, c, d, e, f = 0 .. 5: triangles abc and def with weight 2, joined by cd and be
EXAMPLE = [(0, 1, 2), (0, 2, 2), (1, 2, 2), (3, 4, 2), (3, 5, 2), (4, 5, 2), (2, 3, 1), (1, 4, 1)]


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
    value, side = stoer_wagner(6, EXAMPLE)
    assert value == 2
    assert side in ({0, 1, 2}, {3, 4, 5})
    check(6, EXAMPLE, value, side)


def test_two_vertices_and_parallel_edges() -> None:
    assert stoer_wagner(2, [(0, 1, 3), (1, 0, 4)]) == (7, {1})
    assert stoer_wagner(2, []) == (0, {1})


def test_disconnected_zero_weight_and_loops() -> None:
    value, side = stoer_wagner(4, [(0, 1, 5), (2, 3, 5), (1, 2, 0), (0, 0, 9)])
    assert value == 0
    check(4, [(0, 1, 5), (2, 3, 5), (1, 2, 0)], value, side)


def test_cycle_and_real_weights() -> None:
    cycle = [(i, (i + 1) % 6, 1) for i in range(6)]
    assert stoer_wagner(6, cycle)[0] == 2
    edges = [(0, 1, Fraction(1, 2)), (1, 2, Fraction(1, 3)), (2, 0, Fraction(1, 7)), (2, 3, Fraction(2, 5))]
    value, side = stoer_wagner(4, edges)
    assert value == brute(4, edges) == Fraction(2, 5)
    check(4, edges, value, side)


def test_errors() -> None:
    with pytest.raises(ValueError):
        stoer_wagner(1, [])
    with pytest.raises(ValueError):
        stoer_wagner(2, [(0, 1, -1)])


def test_random_against_brute_force() -> None:
    rng = random.Random(31337)
    for _ in range(800):
        n = rng.randint(2, 8)
        m = rng.randint(0, 20)
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice([0, 1, 1, 2, 3, 7]))
                 for _ in range(m)]
        value, side = stoer_wagner(n, edges)
        assert value == brute(n, edges)
        check(n, edges, value, side)
