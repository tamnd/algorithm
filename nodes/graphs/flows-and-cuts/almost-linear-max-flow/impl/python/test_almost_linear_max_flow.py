# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/almost-linear-max-flow/. The authors are listed in prov/8Q450K.jsonl.

import random
from itertools import product

import pytest

from almost_linear_max_flow import almost_linear_max_flow

S, A, B, C, D, T = range(6)
RUNNING = [
    (S, A, 10), (S, C, 10), (A, B, 4), (A, C, 2), (A, D, 8),
    (C, D, 9), (D, B, 6), (B, T, 10), (D, T, 10),
]


def min_cut_brute(n, edges, s, t):
    """Oracle: the least capacity of a set containing s and not t."""
    others = [v for v in range(n) if v not in (s, t)]
    best = None
    for bits in product((0, 1), repeat=len(others)):
        side = {s} | {v for v, b in zip(others, bits) if b}
        cap = sum(c for u, v, c in edges if u in side and v not in side)
        best = cap if best is None else min(best, cap)
    return best


def check_flow(n, edges, s, t, value, flow):
    assert len(flow) == len(edges)
    exc = [0] * n
    for (u, v, c), f in zip(edges, flow):
        assert isinstance(f, int) and 0 <= f <= c
        exc[u] -= f
        exc[v] += f
    for v in range(n):
        if v not in (s, t):
            assert exc[v] == 0
    assert exc[t] == value == -exc[s]


def test_running_example():
    log = []
    value, flow = almost_linear_max_flow(6, RUNNING, S, T, on_step=lambda k, g: log.append((k, g)))
    assert value == 19
    check_flow(6, RUNNING, S, T, value, flow)
    # F_lo = -21 and the optimal cost is -19, so a gap below 3 means within 1 of optimal.
    gaps = [g for k, g in log if k > 0]
    assert gaps[0] == pytest.approx(21.0)
    assert gaps[-1] < 2.01
    assert log[-1] == (-1, 0)  # the finish needed no augmenting path


def test_finish_alone_is_exact():
    log = []
    value, flow = almost_linear_max_flow(6, RUNNING, S, T, max_steps=0, on_step=lambda k, g: log.append((k, g)))
    assert value == 19
    check_flow(6, RUNNING, S, T, value, flow)
    assert log[-1][0] == -1 and log[-1][1] > 0


def test_zero_capacity_and_antiparallel():
    edges = RUNNING + [(A, S, 3), (C, A, 0), (T, D, 5)]
    value, flow = almost_linear_max_flow(6, edges, S, T)
    assert value == 19
    check_flow(6, edges, S, T, value, flow)
    edges = [(0, 1, 3), (1, 0, 2), (1, 2, 3), (2, 1, 4)]
    assert almost_linear_max_flow(3, edges, 0, 2) == (3, [3, 0, 3, 0])


def test_no_path_and_degenerate():
    assert almost_linear_max_flow(4, [(0, 1, 5), (3, 1, 5)], 0, 3) == (0, [0, 0])
    assert almost_linear_max_flow(2, [], 0, 1) == (0, [])
    assert almost_linear_max_flow(2, [(0, 1, 0)], 0, 1) == (0, [0])
    assert almost_linear_max_flow(2, [(0, 0, 4), (0, 1, 2), (0, 1, 5)], 0, 1) == (7, [0, 2, 5])
    assert almost_linear_max_flow(3, [(1, 0, 4), (1, 2, 4)], 0, 2) == (0, [0, 0])


def test_bad_input():
    with pytest.raises(TypeError):
        almost_linear_max_flow(2, [(0, 1, 1.5)], 0, 1)
    with pytest.raises(TypeError):
        almost_linear_max_flow(2, [(0, 1, -1)], 0, 1)
    with pytest.raises(ValueError):
        almost_linear_max_flow(2, [(0, 1, 1)], 1, 1)


def test_random_against_brute_force():
    rng = random.Random(2022)
    for _ in range(500):
        n = rng.randint(2, 6)
        m = rng.randint(0, 10)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(m)]
        s, t = rng.sample(range(n), 2)
        value, flow = almost_linear_max_flow(n, edges, s, t)
        assert value == min_cut_brute(n, edges, s, t)
        check_flow(n, edges, s, t, value, flow)


def test_random_short_runs_still_exact():
    rng = random.Random(11)
    for _ in range(100):
        n = rng.randint(2, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 20)) for _ in range(rng.randint(1, 12))]
        k = rng.randint(0, 5)
        value, flow = almost_linear_max_flow(n, edges, 0, n - 1, max_steps=k)
        assert value == min_cut_brute(n, edges, 0, n - 1)
        check_flow(n, edges, 0, n - 1, value, flow)
