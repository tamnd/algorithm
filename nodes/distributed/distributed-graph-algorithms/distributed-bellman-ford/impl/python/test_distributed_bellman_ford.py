# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-bellman-ford/. The authors are listed in prov/FVKNH6.jsonl.

import math
import random

from distributed_bellman_ford import (
    INF,
    async_bellman_ford,
    blowup_instance,
    count_to_infinity,
    dijkstra,
    sync_bellman_ford,
)

EXAMPLE = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]


def random_graph(n: int, p: float, rng: random.Random) -> list[tuple[int, int, int]]:
    edges = [(rng.randrange(v), v, rng.randrange(0, 10)) for v in range(1, n)]
    edges += [(u, v, rng.randrange(0, 10)) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
    return edges


def hop_bounded(n: int, edges: list[tuple[int, int, int]], s: int, r: int) -> list[float]:
    """The least weight of a walk from s with at most r edges."""
    d = [INF] * n
    d[s] = 0
    for _ in range(r):
        nd = list(d)
        for u, v, w in edges:
            nd[v] = min(nd[v], d[u] + w)
            nd[u] = min(nd[u], d[v] + w)
        d = nd
    return d


def test_example_trace() -> None:
    st = sync_bellman_ford(5, EXAMPLE, 0)
    assert st["history"] == [
        [0, INF, INF, INF, INF],
        [0, 4, 1, INF, INF],
        [0, 3, 1, 5, INF],
        [0, 3, 1, 4, 8],
        [0, 3, 1, 4, 7],
    ]
    assert st["parent"] == [None, 2, 0, 1, 3]
    assert st["messages"] == 4 * 2 * len(EXAMPLE)


def test_sync_matches_dijkstra_in_n_minus_1_rounds() -> None:
    rng = random.Random(1)
    for _ in range(150):
        n = rng.randrange(1, 25)
        g = random_graph(n, rng.random() * 0.4, rng)
        s = rng.randrange(n)
        st = sync_bellman_ford(n, g, s)
        assert st["dist"] == dijkstra(n, g, s)
        # after round r, each estimate is the r-hop distance
        for r, row in enumerate(st["history"]):
            assert row == hop_bounded(n, g, s, r)
        assert st["messages"] == max(n - 1, 0) * 2 * len(g)
        assert st["max_bits"] <= 2 + math.ceil(math.log2(10 * n + 1)) + 1
        # the parents form a shortest path tree
        for v in range(n):
            p = st["parent"][v]
            if v != s:
                w = min(wt for a, b, wt in g if {a, b} == {v, p})
                assert st["dist"][v] == st["dist"][p] + w


def test_path_needs_n_minus_1_rounds() -> None:
    n = 12
    path = [(i, i + 1, 1) for i in range(n - 1)]
    assert sync_bellman_ford(n, path, 0, rounds=n - 2)["dist"][n - 1] == INF
    assert sync_bellman_ford(n, path, 0)["dist"][n - 1] == n - 1


def test_async_correct_under_random_delays() -> None:
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randrange(1, 20)
        g = random_graph(n, rng.random() * 0.4, rng)
        delay = {}
        for u, v, _w in g:
            delay[(u, v)] = rng.uniform(0.1, 5)
            delay[(v, u)] = rng.uniform(0.1, 5)
        s = rng.randrange(n)
        assert async_bellman_ford(n, g, s, delay)["dist"] == dijkstra(n, g, s)


def test_async_exponential_blowup() -> None:
    for k in range(1, 10):
        n, g, delay = blowup_instance(k)
        st = async_bellman_ford(n, g, 0, delay)
        assert st["dist"] == dijkstra(n, g, 0)
        # v_k holds every value 2^k - 1, 2^k - 2, ..., 0 in turn
        assert st["seen"][k] == [INF] + list(range(2**k - 1, -1, -1))
        assert st["messages"] == 2 ** (k + 3) - 8
        # the synchronous version on the same graph: 2m(n - 1) messages
        assert sync_bellman_ford(n, g, 0)["messages"] == 2 * len(g) * (n - 1)


def test_count_to_infinity() -> None:
    for cap in range(3, 40):
        seq = count_to_infinity(cap)
        assert len(seq) - 1 == cap - 1  # cap - 1 rounds to reach "infinity"
        for r, (a, b) in enumerate(seq[1:-1], start=1):
            assert (max(a, b), min(a, b)) == (r + 2, r + 1)
    assert count_to_infinity(16)[:4] == [(1, 2), (3, 2), (3, 4), (5, 4)]
