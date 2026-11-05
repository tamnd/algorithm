# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ford-fulkerson/. The authors are listed in prov/AM5BV8.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from ford_fulkerson import ford_fulkerson

S, A, B, C, D, T = range(6)
RUNNING = [(S, A, 10), (S, C, 10), (A, B, 4), (A, C, 2), (A, D, 8), (C, D, 9), (D, B, 6), (B, T, 10), (D, T, 10)]


def min_cut_brute(n, edges, s, t):
    """Oracle: the least capacity over all 2^(n-2) s-t cuts."""
    others = [v for v in range(n) if v not in (s, t)]
    best = None
    for k in range(len(others) + 1):
        for extra in combinations(others, k):
            side = {s, *extra}
            cap = sum(c for u, v, c in edges if u in side and v not in side)
            best = cap if best is None else min(best, cap)
    return best


def check(n, edges, s, t, value, flow, side):
    """The flow is feasible, has the value, and the side is a cut of that capacity."""
    exc = [0] * n
    for (u, v, c), f in zip(edges, flow):
        assert 0 <= f <= c
        exc[u] -= f
        exc[v] += f
    for v in range(n):
        if v not in (s, t):
            assert exc[v] == 0
    assert -exc[s] == value
    assert s in side and t not in side
    cut = set(side)
    assert sum(c for u, v, c in edges if u in cut and v not in cut) == value


def test_running_example() -> None:
    value, flow, side = ford_fulkerson(6, RUNNING, S, T)
    assert value == 19
    assert side == [S, C]
    check(6, RUNNING, S, T, value, flow, side)


def test_backward_edge_needed() -> None:
    edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
    value, flow, side = ford_fulkerson(4, edges, 0, 3)
    assert value == 2
    check(4, edges, 0, 3, value, flow, side)


def test_no_path_and_zero_capacity() -> None:
    assert ford_fulkerson(3, [(0, 1, 5), (2, 1, 5)], 0, 2) == (0, [0, 0], [0, 1])
    assert ford_fulkerson(3, [(0, 1, 5), (1, 2, 0)], 0, 2) == (0, [0, 0], [0, 1])
    assert ford_fulkerson(2, [], 0, 1) == (0, [], [0])


def test_antiparallel_parallel_and_loops() -> None:
    edges = [(0, 1, 3), (1, 2, 2), (2, 1, 1), (2, 3, 2), (0, 2, 1), (1, 1, 7), (0, 1, 2)]
    value, flow, side = ford_fulkerson(4, edges, 0, 3)
    assert value == 2
    check(4, edges, 0, 3, value, flow, side)
    edges = [(0, 1, 4), (1, 0, 4), (1, 2, 3), (2, 1, 5)]
    value, flow, side = ford_fulkerson(3, edges, 0, 2)
    assert value == 3
    check(3, edges, 0, 2, value, flow, side)


def test_exact_rational_capacities() -> None:
    edges = [(0, 1, Fraction(1, 3)), (0, 2, Fraction(1, 2)), (1, 3, Fraction(1, 2)), (2, 3, Fraction(1, 4)), (2, 1, 1)]
    value, flow, side = ford_fulkerson(4, edges, 0, 3)
    assert value == Fraction(3, 4)
    check(4, edges, 0, 3, value, flow, side)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        ford_fulkerson(2, [(0, 1, 1)], 0, 0)
    with pytest.raises(ValueError):
        ford_fulkerson(2, [(0, 1, -1)], 0, 1)


def test_large_capacities() -> None:
    big = 2**62
    edges = [(0, 1, big), (1, 2, big), (0, 2, 1)]
    assert ford_fulkerson(3, edges, 0, 2)[0] == big + 1


def test_random_against_brute_force_cut() -> None:
    rng = random.Random(4417)
    for _ in range(600):
        n = rng.randint(2, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 6)) for _ in range(rng.randint(0, 12))]
        s, t = rng.sample(range(n), 2)
        value, flow, side = ford_fulkerson(n, edges, s, t)
        assert value == min_cut_brute(n, edges, s, t)
        check(n, edges, s, t, value, flow, side)
