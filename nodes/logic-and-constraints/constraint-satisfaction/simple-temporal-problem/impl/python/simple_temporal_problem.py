# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simple-temporal-problem/. The authors are listed in prov/CNEAFW.jsonl.

"""The simple temporal problem by shortest paths.

Time points are 0 .. n-1. A constraint (i, j, a, b) means a <= X_j - X_i <= b,
with a = -inf or b = inf for a missing side. In the distance graph it gives
the edge i -> j with weight b and the edge j -> i with weight -a.

minimal_network(n, constraints) runs Floyd-Warshall. It returns None when the
graph has a negative cycle (the STP is inconsistent), and otherwise the matrix
d with d[i][j] the shortest distance from i to j. The tightest constraint on
X_j - X_i that follows from the STP is then -d[j][i] <= X_j - X_i <= d[i][j].

solve(n, constraints) runs Bellman-Ford from a virtual source and returns a
solution (a list of times) or None. Weights may be int or Fraction.
"""

import math
from fractions import Fraction

INF = math.inf
Number = int | Fraction | float


def _edges(constraints: list[tuple]) -> list[tuple[int, int, Number]]:
    edges = []
    for i, j, a, b in constraints:
        if b != INF:
            edges.append((i, j, b))  # X_j - X_i <= b
        if a != -INF:
            edges.append((j, i, -a))  # X_i - X_j <= -a
    return edges


def minimal_network(n: int, constraints: list[tuple]) -> list[list[Number]] | None:
    d: list[list[Number]] = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in _edges(constraints):
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    if any(d[i][i] < 0 for i in range(n)):
        return None
    return d


def solve(n: int, constraints: list[tuple]) -> list[Number] | None:
    """A solution by Bellman-Ford, or None if the distance graph has a negative cycle."""
    edges = _edges(constraints)
    dist: list[Number] = [0] * n  # a virtual source with weight-0 edges to all points
    # A shortest path from the source uses at most n - 1 edges after the first,
    # so without a negative cycle round n changes nothing.
    for _ in range(n + 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            return dist
    return None  # still changing after n rounds: a negative cycle


def satisfies(times: list[Number], constraints: list[tuple]) -> bool:
    return all(a <= times[j] - times[i] <= b for i, j, a, b in constraints)
