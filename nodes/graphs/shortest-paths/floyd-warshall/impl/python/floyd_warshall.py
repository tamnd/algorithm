# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-warshall/. The authors are listed in prov/HSBPN7.jsonl.

import math


def floyd_warshall(
    n: int, edges: list[tuple[int, int, float]]
) -> tuple[list[list[float]], list[list[int | None]]]:
    """All-pairs shortest-path weights and a next-hop matrix.

    The graph has the vertices 0 .. n-1 and the directed edges (u, v, w); parallel
    edges and self-loops are allowed, and weights may be negative. Returns (D, nxt).
    If no cycle of negative weight exists, D[i][j] is the distance from i to j
    (math.inf if there is no path) and nxt[i][j] is the vertex after i on a shortest
    path (None if i == j or there is no path). A negative cycle exists if and only if
    D[i][i] < 0 for some i; then D holds no distances. Time Θ(n^3), extra space Θ(n^2).
    """
    D = [[math.inf] * n for _ in range(n)]  # @line L1
    nxt: list[list[int | None]] = [[None] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
    for u, v, w in edges:  # @line L2
        if w < D[u][v]:
            D[u][v] = w
            nxt[u][v] = v
    for k in range(n):  # @line L3
        Dk = D[k]
        for i in range(n):  # @line L4
            dik = D[i][k]
            if dik == math.inf:
                continue
            Di = D[i]
            for j in range(n):  # @line L5
                if dik + Dk[j] < Di[j]:  # @line L6
                    Di[j] = dik + Dk[j]  # @line L7
                    nxt[i][j] = nxt[i][k]
    return D, nxt  # @line L8


def has_negative_cycle(D: list[list[float]]) -> bool:
    """True if and only if the graph that produced D has a cycle of negative weight."""
    return any(D[i][i] < 0 for i in range(len(D)))


def path(nxt: list[list[int | None]], i: int, j: int) -> list[int] | None:
    """The vertices of a shortest path from i to j, or None if j is unreachable.

    Valid only when the graph has no negative cycle.
    """
    if i != j and nxt[i][j] is None:
        return None
    p = [i]
    while i != j:
        i = nxt[i][j]  # type: ignore[assignment]
        p.append(i)
    return p
