# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dinic/. The authors are listed in prov/K5ZN3K.jsonl.

import math
import random
from fractions import Fraction
from itertools import combinations

import pytest

from dinic import dinic

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
    value, flow, side = dinic(6, RUNNING, S, T)
    assert value == 19
    assert side == [S, C]
    check(6, RUNNING, S, T, value, flow, side)


def test_backward_edge_needed() -> None:
    edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
    value, flow, side = dinic(4, edges, 0, 3)
    assert value == 2
    check(4, edges, 0, 3, value, flow, side)


def test_no_path_and_zero_capacity() -> None:
    assert dinic(3, [(0, 1, 5), (2, 1, 5)], 0, 2) == (0, [0, 0], [0, 1])
    assert dinic(3, [(0, 1, 5), (1, 2, 0)], 0, 2) == (0, [0, 0], [0, 1])
    assert dinic(2, [], 0, 1) == (0, [], [0])


def test_antiparallel_parallel_and_loops() -> None:
    edges = [(0, 1, 3), (1, 2, 2), (2, 1, 1), (2, 3, 2), (0, 2, 1), (1, 1, 7), (0, 1, 2)]
    value, flow, side = dinic(4, edges, 0, 3)
    assert value == 2
    check(4, edges, 0, 3, value, flow, side)
    edges = [(0, 1, 4), (1, 0, 4), (1, 2, 3), (2, 1, 5)]
    value, flow, side = dinic(3, edges, 0, 2)
    assert value == 3
    check(3, edges, 0, 2, value, flow, side)


def test_exact_rational_capacities() -> None:
    edges = [(0, 1, Fraction(1, 3)), (0, 2, Fraction(1, 2)), (1, 3, Fraction(1, 2)), (2, 3, Fraction(1, 4)), (2, 1, 1)]
    value, flow, side = dinic(4, edges, 0, 3)
    assert value == Fraction(3, 4)
    check(4, edges, 0, 3, value, flow, side)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        dinic(2, [(0, 1, 1)], 0, 0)
    with pytest.raises(ValueError):
        dinic(2, [(0, 1, -1)], 0, 1)


def test_large_capacities() -> None:
    big = 2**62
    edges = [(0, 1, big), (1, 2, big), (0, 2, 1)]
    assert dinic(3, edges, 0, 2)[0] == big + 1


def test_random_against_brute_force_cut() -> None:
    rng = random.Random(4417)
    for _ in range(600):
        n = rng.randint(2, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 6)) for _ in range(rng.randint(0, 12))]
        s, t = rng.sample(range(n), 2)
        value, flow, side = dinic(n, edges, s, t)
        assert value == min_cut_brute(n, edges, s, t)
        check(n, edges, s, t, value, flow, side)


def test_bad_case_for_plain_ford_fulkerson() -> None:
    x = 10**15
    edges = [(0, 1, x), (0, 2, x), (1, 2, 1), (1, 3, x), (2, 3, x)]
    value, flow, side = dinic(4, edges, 0, 3)
    assert value == 2 * x
    assert flow[2] == 0  # the shortest paths never use the middle edge


def test_irrational_like_float_capacities() -> None:
    r = (math.sqrt(5) - 1) / 2
    edges = [(0, 1, 1.0), (0, 2, r), (1, 2, 1.0), (2, 1, r * r), (1, 3, r), (2, 3, 1.0)]
    value, flow, side = dinic(4, edges, 0, 3)
    assert math.isclose(value, min_cut_brute(4, edges, 0, 3), rel_tol=1e-12)
    assert 0 in side and 3 not in side


def test_random_floats() -> None:
    rng = random.Random(77)
    for _ in range(500):
        n = rng.randint(2, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.random() * 5) for _ in range(rng.randint(0, 12))]
        s, t = rng.sample(range(n), 2)
        value, flow, side = dinic(n, edges, s, t)
        assert math.isclose(value, min_cut_brute(n, edges, s, t), rel_tol=1e-9, abs_tol=1e-9)
        cut = set(side)
        assert math.isclose(value, sum(c for u, v, c in edges if u in cut and v not in cut), rel_tol=1e-9, abs_tol=1e-9)


def test_phases_of_running_example() -> None:
    log = []
    value, flow, side = dinic(6, RUNNING, S, T, lambda p, path, d: log.append((p, path, d)))
    assert value == 19
    assert log == [
        (1, [S, A, B, T], 4),
        (1, [S, A, D, T], 6),
        (1, [S, C, D, T], 4),
        (2, [S, C, D, B, T], 5),
    ]


def test_blocking_is_not_maximum_needs_second_phase() -> None:
    s, x1, x2, y1, y2, t = range(6)
    edges = [(s, x1, 1), (s, x2, 1), (x1, y1, 1), (x1, y2, 1), (x2, y1, 1), (y1, t, 1), (y2, t, 1)]
    log = []
    value, flow, side = dinic(6, edges, s, t, lambda p, path, d: log.append((p, path, d)))
    assert value == 2
    assert log == [(1, [s, x1, y1, t], 1), (2, [s, x2, y1, x1, y2, t], 1)]


def test_long_path_no_recursion_limit() -> None:
    n = 5000
    edges = [(i, i + 1, 3) for i in range(n - 1)]
    assert dinic(n, edges, 0, n - 1)[0] == 3
