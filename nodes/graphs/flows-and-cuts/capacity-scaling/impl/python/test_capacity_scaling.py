# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/capacity-scaling/. The authors are listed in prov/H1FND5.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from capacity_scaling import capacity_scaling

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
    value, flow, side = capacity_scaling(6, RUNNING, S, T)
    assert value == 19
    assert side == [S, C]
    check(6, RUNNING, S, T, value, flow, side)


def test_backward_edge_needed() -> None:
    edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
    value, flow, side = capacity_scaling(4, edges, 0, 3)
    assert value == 2
    check(4, edges, 0, 3, value, flow, side)


def test_no_path_and_zero_capacity() -> None:
    assert capacity_scaling(3, [(0, 1, 5), (2, 1, 5)], 0, 2) == (0, [0, 0], [0, 1])
    assert capacity_scaling(3, [(0, 1, 5), (1, 2, 0)], 0, 2) == (0, [0, 0], [0, 1])
    assert capacity_scaling(2, [], 0, 1) == (0, [], [0])


def test_antiparallel_parallel_and_loops() -> None:
    edges = [(0, 1, 3), (1, 2, 2), (2, 1, 1), (2, 3, 2), (0, 2, 1), (1, 1, 7), (0, 1, 2)]
    value, flow, side = capacity_scaling(4, edges, 0, 3)
    assert value == 2
    check(4, edges, 0, 3, value, flow, side)
    edges = [(0, 1, 4), (1, 0, 4), (1, 2, 3), (2, 1, 5)]
    value, flow, side = capacity_scaling(3, edges, 0, 2)
    assert value == 3
    check(3, edges, 0, 2, value, flow, side)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        capacity_scaling(2, [(0, 1, 1)], 0, 0)
    with pytest.raises(ValueError):
        capacity_scaling(2, [(0, 1, -1)], 0, 1)


def test_large_capacities() -> None:
    big = 2**62
    edges = [(0, 1, big), (1, 2, big), (0, 2, 1)]
    assert capacity_scaling(3, edges, 0, 2)[0] == big + 1


def test_random_against_brute_force_cut() -> None:
    rng = random.Random(4417)
    for _ in range(600):
        n = rng.randint(2, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 6)) for _ in range(rng.randint(0, 12))]
        s, t = rng.sample(range(n), 2)
        value, flow, side = capacity_scaling(n, edges, s, t)
        assert value == min_cut_brute(n, edges, s, t)
        check(n, edges, s, t, value, flow, side)


def test_bad_case_for_plain_ford_fulkerson() -> None:
    x = 10**15
    edges = [(0, 1, x), (0, 2, x), (1, 2, 1), (1, 3, x), (2, 3, x)]
    value, flow, side = capacity_scaling(4, edges, 0, 3)
    assert value == 2 * x
    assert flow[2] == 0  # the shortest paths never use the middle edge


def test_long_path_no_recursion_limit() -> None:
    n = 5000
    edges = [(i, i + 1, 3) for i in range(n - 1)]
    assert capacity_scaling(n, edges, 0, n - 1)[0] == 3


def test_non_integer_capacities_rejected() -> None:
    with pytest.raises(TypeError):
        capacity_scaling(2, [(0, 1, 1.5)], 0, 1)
    with pytest.raises(TypeError):
        capacity_scaling(2, [(0, 1, Fraction(1, 2))], 0, 1)


def test_phases_of_running_example() -> None:
    log = []
    value, flow, side = capacity_scaling(6, RUNNING, S, T, lambda d, p, a: log.append((d, p, a)))
    assert value == 19
    assert log == [
        (8, [S, A, D, T], 8),
        (4, [S, C, D, B, T], 6),
        (2, [S, A, B, T], 2),
        (2, [S, C, D, T], 2),
        (1, [S, C, D, A, B, T], 1),
    ]


def test_each_amount_at_least_delta_and_at_most_2m_per_phase() -> None:
    rng = random.Random(5150)
    for _ in range(500):
        n = rng.randint(2, 7)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 40)) for _ in range(rng.randint(0, 14))]
        s, t = rng.sample(range(n), 2)
        log = []
        value, flow, side = capacity_scaling(n, edges, s, t, lambda d, p, a: log.append((d, a)))
        assert value == min_cut_brute(n, edges, s, t)
        check(n, edges, s, t, value, flow, side)
        per_phase = {}
        for d, a in log:
            assert a >= d
            per_phase[d] = per_phase.get(d, 0) + 1
        for d, k in per_phase.items():
            assert k <= 2 * max(1, len(edges))
