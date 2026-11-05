# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successive-shortest-path/. The authors are listed in prov/13QZ7V.jsonl.

import itertools
import math
import random

import pytest

from successive_shortest_path import successive_shortest_path as ssp

# s, a, b, t = 0, 1, 2, 3; edges (u, v, capacity, cost)
EXAMPLE = [(0, 1, 3, 1), (0, 2, 2, 4), (1, 2, 2, 1), (1, 3, 2, 5), (2, 3, 3, 1)]


def brute(n, edges, s, t):
    """Independent oracle: the least cost of an integral s-t flow of each value.

    Self-loops are ignored by the algorithm, so they carry 0 here as well.
    """
    best = {}
    for x in itertools.product(*[range(e[2] + 1 if e[0] != e[1] else 1) for e in edges]):
        bal = [0] * n
        for (u, v, _, _), f in zip(edges, x):
            bal[u] -= f
            bal[v] += f
        if all(bal[v] == 0 for v in range(n) if v not in (s, t)):
            c = sum(f * e[3] for e, f in zip(edges, x))
            k = bal[t]
            if k >= 0 and (k not in best or c < best[k]):
                best[k] = c
    return best


def check(n, edges, s, t, value, cost, flow):
    assert all(0 <= f <= e[2] for f, e in zip(flow, edges))
    bal = [0] * n
    for (u, v, _, _), f in zip(edges, flow):
        bal[u] -= f
        bal[v] += f
    assert all(bal[v] == 0 for v in range(n) if v not in (s, t))
    assert bal[t] == value
    assert cost == sum(f * e[3] for f, e in zip(flow, edges))


def test_example_each_value() -> None:
    expected = {0: 0, 1: 3, 2: 6, 3: 11, 4: 17, 5: 25}
    for d, c in expected.items():
        value, cost, flow = ssp(4, EXAMPLE, 0, 3, d)
        assert (value, cost) == (d, c)
        check(4, EXAMPLE, 0, 3, value, cost, flow)
    assert ssp(4, EXAMPLE, 0, 3) == (5, 25, [3, 2, 1, 2, 3])
    assert ssp(4, EXAMPLE, 0, 3, 9)[:2] == (5, 25)


def test_zero_capacity_and_no_path() -> None:
    assert ssp(2, [(0, 1, 0, -100)], 0, 1) == (0, 0, [0])
    assert ssp(4, [(0, 1, 3, 1), (2, 3, 3, 1)], 0, 3) == (0, 0, [0, 0])
    assert ssp(2, [], 0, 1) == (0, 0, [])


def test_negative_costs_and_antiparallel() -> None:
    edges = [(0, 1, 2, -3), (1, 0, 2, 5), (1, 2, 3, 1), (0, 2, 1, 0), (1, 1, 4, -9)]
    value, cost, flow = ssp(3, edges, 0, 2)
    assert (value, cost) == (3, -4)
    check(3, edges, 0, 2, value, cost, flow)
    assert flow[1] == 0 and flow[4] == 0


def test_negative_cycle_rejected() -> None:
    with pytest.raises(ValueError):
        ssp(3, [(1, 2, 1, -2), (2, 1, 1, 1), (0, 1, 1, 0)], 0, 1)
    # a negative cycle of capacity 0 does not count
    assert ssp(3, [(1, 2, 0, -2), (2, 1, 1, 1), (0, 1, 1, 0)], 0, 1)[:2] == (1, 0)


def test_errors() -> None:
    with pytest.raises(ValueError):
        ssp(2, [(0, 1, 1, 1)], 1, 1)
    with pytest.raises(ValueError):
        ssp(2, [(0, 1, -1, 1)], 0, 1)


def has_negative_cycle(n, edges):
    dist = [0] * n
    for _ in range(n):
        for u, v, c, w in edges:
            if c > 0 and u != v and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return any(c > 0 and u != v and dist[u] + w < dist[v] for u, v, c, w in edges)


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    tested = 0
    while tested < 600:
        n = rng.randint(2, 5)
        m = rng.randint(0, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 3), rng.randint(-3, 6))
                 for _ in range(m)]
        if has_negative_cycle(n, edges):
            continue
        s, t = rng.sample(range(n), 2)
        best = brute(n, edges, s, t)
        top = max(best)
        for d in range(top + 1):
            value, cost, flow = ssp(n, edges, s, t, d)
            assert value == d and cost == best[d]
            check(n, edges, s, t, value, cost, flow)
        value, cost, _ = ssp(n, edges, s, t)
        assert (value, cost) == (top, best[top])
        tested += 1
