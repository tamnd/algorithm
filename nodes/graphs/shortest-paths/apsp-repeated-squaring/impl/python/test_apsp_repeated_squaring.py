# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apsp-repeated-squaring/. The authors are listed in prov/TRREJZ.jsonl.

import math
import random

from apsp_repeated_squaring import apsp_repeated_squaring

INF = math.inf
EDGES = [(0, 1, 3), (0, 2, 8), (1, 3, 1), (1, 2, 4), (2, 1, -2), (3, 0, 2), (3, 2, 2)]


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


def oracle(n, edges):
    """Distance matrix from n Bellman-Ford runs, or None if any negative cycle exists."""
    rows = [bellman_ford(n, edges, s) for s in range(n)]
    return None if any(r is None for r in rows) else rows


def test_example() -> None:
    assert apsp_repeated_squaring(4, EDGES) == [
        [0, 3, 6, 4],
        [3, 0, 3, 1],
        [1, -2, 0, -1],
        [2, 0, 2, 0],
    ]


def test_negative_cycle_of_two_edges() -> None:
    # squaring only until k >= n - 1 = 1 would miss this cycle
    assert apsp_repeated_squaring(2, [(0, 1, 1), (1, 0, -2)]) is None


def test_negative_cycle_not_reachable_from_everyone() -> None:
    # 0 -> 1 only; the cycle 1 -> 2 -> 1 has weight -1 and 3 is isolated
    assert apsp_repeated_squaring(4, [(0, 1, 4), (1, 2, -3), (2, 1, 2)]) is None


def test_negative_self_loop() -> None:
    assert apsp_repeated_squaring(1, [(0, 0, -1)]) is None
    assert apsp_repeated_squaring(1, [(0, 0, 5)]) == [[0]]


def test_unreachable_and_trivial() -> None:
    assert apsp_repeated_squaring(0, []) == []
    assert apsp_repeated_squaring(3, [(0, 1, -7)]) == [[0, -7, INF], [INF, 0, INF], [INF, INF, 0]]


def test_zero_cycle_and_parallel_edges() -> None:
    edges = [(0, 1, 2), (0, 1, 1), (1, 2, -3), (2, 0, 2)]
    assert apsp_repeated_squaring(3, edges) == [[0, 1, -2], [-1, 0, -3], [2, 3, 0]]


def test_long_path_needs_all_squarings() -> None:
    n = 9
    edges = [(i, i + 1, -1) for i in range(n - 1)]
    D = apsp_repeated_squaring(n, edges)
    assert D is not None
    assert D[0][n - 1] == -(n - 1)
    assert D[n - 1][0] == INF


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1976)
    for _ in range(600):
        n = rng.randint(1, 8)
        m = rng.randint(0, 3 * n)
        low = rng.choice([0, -2, -5])
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, 9)) for _ in range(m)]
        assert apsp_repeated_squaring(n, edges) == oracle(n, edges)
