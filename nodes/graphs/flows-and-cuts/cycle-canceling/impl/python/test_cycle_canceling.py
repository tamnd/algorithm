# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-canceling/. The authors are listed in prov/M028R9.jsonl.

import random
from itertools import product

import pytest

from cycle_canceling import cycle_canceling

S, A, B, C, D, T = range(6)
RUNNING = [
    (S, A, 10, 2), (S, C, 10, 2), (A, B, 4, 6), (A, C, 2, 3), (A, D, 8, 1),
    (C, D, 9, 2), (D, B, 6, 1), (B, T, 10, 1), (D, T, 10, 3),
]


def brute(n, edges, s, t):
    """Oracle: enumerate every integral flow; return (max value, least cost at that value)."""
    best = None
    for f in product(*[range(c + 1) for _, _, c, _ in edges]):
        exc = [0] * n
        for (u, v, _, _), x in zip(edges, f):
            exc[u] -= x
            exc[v] += x
        if any(exc[v] for v in range(n) if v not in (s, t)):
            continue
        key = (-(-exc[s]), sum(x * e[3] for x, e in zip(f, edges)))
        if best is None or key < best:
            best = key
    return -best[0], best[1]


def check(n, edges, s, t, value, cost, flow):
    exc = [0] * n
    for (u, v, c, _), f in zip(edges, flow):
        assert 0 <= f <= c
        exc[u] -= f
        exc[v] += f
    for v in range(n):
        if v not in (s, t):
            assert exc[v] == 0
    assert -exc[s] == value
    assert sum(f * e[3] for f, e in zip(flow, edges)) == cost


def test_running_example() -> None:
    log = []
    value, cost, flow = cycle_canceling(6, RUNNING, S, T, lambda c, d, w: log.append((c, d, w)))
    assert (value, cost) == (19, 126)
    assert flow == [10, 9, 3, 0, 7, 9, 6, 9, 10]
    assert log == [([D, B, T, D], 1, -1), ([A, D, T, B, A], 1, -3)]
    check(6, RUNNING, S, T, value, cost, flow)


def test_no_path_zero_capacity_and_empty() -> None:
    assert cycle_canceling(3, [(0, 1, 5, 1), (2, 1, 5, 1)], 0, 2) == (0, 0, [0, 0])
    assert cycle_canceling(3, [(0, 1, 5, 1), (1, 2, 0, -9)], 0, 2) == (0, 0, [0, 0])
    assert cycle_canceling(2, [], 0, 1) == (0, 0, [])


def test_negative_cycle_away_from_the_path() -> None:
    # a negative cycle not connected to s or t is still cancelled
    edges = [(0, 1, 2, 1), (2, 3, 3, -2), (3, 2, 5, 1)]
    value, cost, flow = cycle_canceling(4, edges, 0, 1)
    assert (value, cost, flow) == (2, 2 - 3, [2, 3, 3])


def test_negative_self_loop_is_filled() -> None:
    value, cost, flow = cycle_canceling(2, [(0, 1, 1, 0), (0, 0, 4, -1)], 0, 1)
    assert (value, cost, flow) == (1, -4, [1, 4])


def test_antiparallel_edges_keep_their_own_flow() -> None:
    edges = [(0, 1, 3, 1), (1, 2, 2, 4), (2, 1, 1, -5), (2, 3, 2, 1), (0, 2, 1, 1)]
    value, cost, flow = cycle_canceling(4, edges, 0, 3)
    assert (value, cost) == brute(4, edges, 0, 3)
    check(4, edges, 0, 3, value, cost, flow)
    assert flow[1] >= 1 and flow[2] == 1  # the cycle a b a has cost -1 and is used


def test_cheaper_long_path() -> None:
    edges = [(0, 3, 1, 10), (0, 1, 1, 1), (1, 2, 1, 1), (2, 3, 1, 1)]
    value, cost, flow = cycle_canceling(4, edges, 0, 3)
    assert (value, cost) == (2, 13)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        cycle_canceling(2, [(0, 1, 1, 0)], 0, 0)
    with pytest.raises(ValueError):
        cycle_canceling(2, [(0, 1, -1, 0)], 0, 1)
    with pytest.raises(TypeError):
        cycle_canceling(2, [(0, 1, 1.5, 0)], 0, 1)


def test_random_against_brute_force() -> None:
    rng = random.Random(2718)
    for _ in range(600):
        n = rng.randint(2, 5)
        m = rng.randint(0, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 3), rng.randint(-4, 6)) for _ in range(m)]
        s, t = rng.sample(range(n), 2)
        value, cost, flow = cycle_canceling(n, edges, s, t)
        assert (value, cost) == brute(n, edges, s, t)
        check(n, edges, s, t, value, cost, flow)
