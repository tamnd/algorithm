# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnson/. The authors are listed in prov/GE9795.jsonl.

import random

from johnson import johnson

# CLRS Figure 23.6, vertices 1 .. 5 renamed 0 .. 4
CLRS = [(0, 1, 3), (0, 2, 8), (0, 4, -4), (1, 3, 1), (1, 4, 7), (2, 1, 4), (3, 0, 2), (3, 2, -5), (4, 3, 6)]


def floyd_warshall(n: int, edges: list[tuple[int, int, int]]) -> list[list[float | None]] | None:
    inf = float("inf")
    d = [[0.0 if i == j else inf for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    if any(d[i][i] < 0 for i in range(n)):
        return None
    return [[None if x == inf else x for x in row] for row in d]


def test_clrs_example() -> None:
    assert johnson(5, CLRS) == [
        [0, 1, -3, 2, -4],
        [3, 0, -4, 1, -1],
        [7, 4, 0, 5, 3],
        [2, -1, -5, 0, -2],
        [8, 5, 1, 6, 0],
    ]


def test_negative_cycle() -> None:
    assert johnson(3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)]) is None
    assert johnson(1, [(0, 0, -1)]) is None  # a negative self-loop


def test_unreachable_and_empty() -> None:
    assert johnson(0, []) == []
    assert johnson(1, []) == [[0]]
    assert johnson(3, [(0, 1, -2)]) == [[0, -2, None], [None, 0, None], [None, None, 0]]


def test_zero_cycle_and_parallel_arcs() -> None:
    d = johnson(3, [(0, 1, 2), (1, 0, -2), (1, 2, 5), (1, 2, 1)])
    assert d == [[0, 2, 3], [-2, 0, 1], [None, None, 0]]


def test_random_against_floyd_warshall() -> None:
    rng = random.Random(1977)
    for _ in range(600):
        n = rng.randint(1, 7)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-4, 9)) for _ in range(rng.randint(0, 3 * n))]
        assert johnson(n, edges) == floyd_warshall(n, edges)
