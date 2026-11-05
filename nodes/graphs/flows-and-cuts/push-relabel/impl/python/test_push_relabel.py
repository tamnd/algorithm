# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/push-relabel/. The authors are listed in prov/56SN6Q.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from push_relabel import push_relabel

# s, a, b, c, d, t = 0 .. 5
EXAMPLE = [(0, 1, 10), (0, 2, 10), (1, 2, 2), (1, 3, 4), (1, 4, 8),
           (2, 4, 9), (4, 3, 6), (3, 5, 10), (4, 5, 10)]


def min_cut_brute(n, edges, s, t):
    """Independent oracle: the least capacity of a set S with s in S, t not in S."""
    others = [v for v in range(n) if v not in (s, t)]
    best = None
    for r in range(len(others) + 1):
        for extra in itertools.combinations(others, r):
            side = {s, *extra}
            c = sum(w for u, v, w in edges if u in side and v not in side)
            best = c if best is None else min(best, c)
    return best


def check(n, edges, s, t, value, flow, side):
    assert all(0 <= f <= c for f, (_, _, c) in zip(flow, edges))
    bal = [0] * n
    for f, (u, v, _) in zip(flow, edges):
        bal[u] -= f
        bal[v] += f
    assert all(bal[v] == 0 for v in range(n) if v not in (s, t))
    assert bal[t] == value and -bal[s] == value
    assert s in side and t not in side
    assert value == sum(c for u, v, c in edges if u in side and v not in side)


def test_example() -> None:
    value, flow, side = push_relabel(6, EXAMPLE, 0, 5)
    assert value == 19 and side == {0, 2}
    check(6, EXAMPLE, 0, 5, value, flow, side)


def test_small_example_and_stuck_excess() -> None:
    edges = [(0, 1, 3), (0, 2, 2), (1, 2, 1), (1, 3, 2), (2, 3, 3)]
    assert push_relabel(4, edges, 0, 3)[0] == 5
    value, flow, side = push_relabel(3, [(0, 1, 5), (1, 2, 2)], 0, 2)
    assert (value, flow, side) == (2, [2, 2], {0, 1})


def test_zero_capacity_and_no_path() -> None:
    assert push_relabel(3, [(0, 1, 5), (1, 2, 0), (0, 2, 0)], 0, 2) == (0, [0, 0, 0], {0, 1})
    assert push_relabel(4, [(0, 1, 3), (2, 3, 3)], 0, 3) == (0, [0, 0], {0, 1})
    assert push_relabel(2, [], 0, 1) == (0, [], {0})


def test_antiparallel_parallel_loops() -> None:
    edges = [(0, 1, 3), (1, 0, 2), (1, 2, 4), (0, 1, 2), (1, 1, 7), (2, 1, 1), (2, 0, 6)]
    value, flow, side = push_relabel(3, edges, 0, 2)
    assert value == 4
    check(3, edges, 0, 2, value, flow, side)


def test_real_capacities() -> None:
    edges = [(0, 1, Fraction(1, 2)), (0, 2, Fraction(1, 3)), (1, 2, Fraction(1, 7)),
             (1, 3, Fraction(2, 5)), (2, 3, Fraction(3, 4))]
    value, flow, side = push_relabel(4, edges, 0, 3)
    assert value == min_cut_brute(4, edges, 0, 3) == Fraction(5, 6)
    check(4, edges, 0, 3, value, flow, side)


def test_errors() -> None:
    with pytest.raises(ValueError):
        push_relabel(2, [(0, 1, 1)], 1, 1)
    with pytest.raises(ValueError):
        push_relabel(2, [(0, 1, -1)], 0, 1)


def test_random_against_brute_force() -> None:
    rng = random.Random(99)
    for _ in range(700):
        n = rng.randint(2, 7)
        m = rng.randint(0, 18)
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice([0, 1, 2, 3, 5, 9, 30]))
                 for _ in range(m)]
        s, t = rng.sample(range(n), 2)
        value, flow, side = push_relabel(n, edges, s, t)
        assert value == min_cut_brute(n, edges, s, t)
        check(n, edges, s, t, value, flow, side)
