# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-shortest-path-algorithm/. The authors are listed in prov/758800.jsonl.

import math
import random

from generic_shortest_path_algorithm import generic_sssp

INF = math.inf
# s=0, a=1, b=2, c=3, z=4
EXAMPLE = [(0, 2, 4), (2, 3, 1), (0, 1, 1), (1, 3, 6), (1, 2, 2), (4, 0, 1)]


def bellman_ford(n, edges, s):
    """Independent oracle: distances from s, or None if a negative cycle is reachable."""
    d = [INF] * n
    d[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    if any(d[u] + w < d[v] for u, v, w in edges):
        return None
    return d


def test_example_in_two_orders() -> None:
    d, parent, steps = generic_sssp(5, EXAMPLE, 0)
    assert d == [0, 1, 3, 4, INF] and parent == [None, 0, 1, 2, None]
    assert steps == 5
    # always taking the last tense edge happens to need only four relaxations
    d2, _, steps2 = generic_sssp(5, EXAMPLE, 0, choose=lambda t: t[-1])
    assert d2 == d and steps2 == 4


def test_negative_cycle() -> None:
    edges = [(0, 1, 1), (1, 2, -2), (2, 1, 1), (2, 3, 0)]
    assert generic_sssp(4, edges, 0) is None
    assert generic_sssp(1, [(0, 0, -1)], 0) is None


def test_negative_cycle_not_reachable_and_unreachable_vertex() -> None:
    edges = [(0, 1, -3), (2, 3, -1), (3, 2, -1)]
    d, parent, _ = generic_sssp(4, edges, 0)
    assert d == [0, -3, INF, INF] and parent == [None, 0, None, None]


def exponential_instance(k):
    """Chain v_0 .. v_k with a heavy edge v_i -> v_(i+1) of weight 2^(k-1-i) and a light
    detour v_i -> u_i -> v_(i+1) of weight 0, plus an order of relaxations that makes
    the label of v_k take all 2^k values 2^k - 1, ..., 0."""
    v = list(range(k + 1))
    u = [k + 1 + i for i in range(k)]
    edges, idx = [], {}
    for i in range(k):
        for a, b, w in ((v[i], v[i + 1], 2 ** (k - 1 - i)), (v[i], u[i], 0), (u[i], v[i + 1], 0)):
            idx[a, b] = len(edges)
            edges.append((a, b, w))
    order = []

    def run(i):
        # called right after the label of v_i dropped
        if i == k:
            return
        order.append(idx[v[i], v[i + 1]])
        run(i + 1)
        order.append(idx[v[i], u[i]])
        order.append(idx[u[i], v[i + 1]])
        run(i + 1)

    run(0)
    return 2 * k + 1, edges, order


def test_bad_order_takes_exponentially_many_steps() -> None:
    for k in range(1, 8):
        n, edges, order = exponential_instance(k)
        it = iter(order)
        seen = []

        def choose(tense):
            e = next(it)
            assert e in tense
            if edges[e][1] == k:
                seen.append(None)
            return e

        d, _, steps = generic_sssp(n, edges, 0, choose=choose)
        assert d[k] == 0
        assert len(seen) == 2**k  # the label of v_k dropped 2^k times
        assert steps >= 2**k


def test_random_orders_against_bellman_ford() -> None:
    rng = random.Random(1956)
    rules = [None, lambda t: t[-1], lambda t: rng.choice(t)]
    for _ in range(600):
        n = rng.randint(1, 7)
        low = rng.choice([0, -2, -5])
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, 9)) for _ in range(rng.randint(0, 3 * n))]
        s = rng.randrange(n)
        want = bellman_ford(n, edges, s)
        got = generic_sssp(n, edges, s, choose=rng.choice(rules))
        if want is None:
            assert got is None
        else:
            assert got is not None and got[0] == want
            for x in range(n):
                if x != s and want[x] < INF:
                    p = got[1][x]
                    assert any(a == p and b == x and want[p] + w == want[x] for a, b, w in edges)
