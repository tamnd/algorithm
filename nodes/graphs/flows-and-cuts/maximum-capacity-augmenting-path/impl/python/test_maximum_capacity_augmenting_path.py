# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-capacity-augmenting-path/. The authors are listed in prov/QFY05A.jsonl.

import itertools
import random

import pytest

from maximum_capacity_augmenting_path import maximum_capacity_augmenting_path as mcap

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


def check_flow(n, edges, s, t, value, flow, side):
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
    value, flow, side = mcap(6, EXAMPLE, 0, 5)
    assert value == 19 and side == {0, 2}
    check_flow(6, EXAMPLE, 0, 5, value, flow, side)


def test_zero_capacity_and_no_path() -> None:
    edges = [(0, 1, 5), (1, 2, 0), (0, 2, 0)]
    assert mcap(3, edges, 0, 2) == (0, [0, 0, 0], {0, 1})
    assert mcap(4, [(0, 1, 3), (2, 3, 3)], 0, 3) == (0, [0, 0], {0, 1})
    assert mcap(2, [], 0, 1) == (0, [], {0})


def test_antiparallel_parallel_and_loops() -> None:
    edges = [(0, 1, 3), (1, 0, 2), (1, 2, 4), (0, 1, 2), (1, 1, 7), (2, 1, 1)]
    value, flow, side = mcap(3, edges, 0, 2)
    assert value == 4
    check_flow(3, edges, 0, 2, value, flow, side)
    assert flow[4] == 0


def test_backward_edge_is_needed() -> None:
    edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
    assert mcap(4, edges, 0, 3)[0] == 2


def test_errors() -> None:
    with pytest.raises(ValueError):
        mcap(2, [(0, 1, 1)], 0, 0)
    with pytest.raises(ValueError):
        mcap(2, [(0, 1, -1)], 0, 1)


def test_large_values() -> None:
    big = 2 ** 62
    value, _, _ = mcap(3, [(0, 1, big), (1, 2, big), (0, 2, 5)], 0, 2)
    assert value == big + 5


def test_random_against_brute_force() -> None:
    rng = random.Random(4711)
    for _ in range(600):
        n = rng.randint(2, 7)
        m = rng.randint(0, 16)
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice([0, 1, 2, 3, 5, 8, 20]))
                 for _ in range(m)]
        s, t = rng.sample(range(n), 2)
        value, flow, side = mcap(n, edges, s, t)
        assert value == min_cut_brute(n, edges, s, t)
        check_flow(n, edges, s, t, value, flow, side)
