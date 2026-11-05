# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thorup-undirected-sssp/. The authors are listed in prov/J10R6J.jsonl.

"""Thorup's SSSP for undirected graphs with positive integer weights.

The component hierarchy and the bucketed visiting order follow Thorup (1999).
To stay short, this version finds the least tentative distance in a component
with a lazy binary heap per hierarchy node instead of Thorup's split-findmin
structure and bucket arrays, so it runs in O(m r log n) time for r levels, not
O(m). The order in which it settles vertices is one that Thorup's rule allows.
"""

import heapq
import math


def _find(parent: list[int], x: int) -> int:
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def thorup_undirected_sssp(n: int, edges: list[tuple[int, int, int]], s: int, trace: list | None = None) -> list[int | None]:
    """Distances from s in an undirected graph with positive integer weights.

    Vertices are 0 .. n-1; edges lists (u, v, w), each usable both ways. Returns
    dist with None for vertices not reachable from s. Raises ValueError on a
    weight that is not a positive integer (a negative edge u-v would give the
    negative closed walk u, v, u). If trace is a list, each call
    (level, lowest vertex of the component, bound) is appended to it.
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    big = 1
    for u, v, w in edges:
        if not isinstance(w, int) or isinstance(w, bool) or w < 1:
            raise ValueError(f"weight {w!r} is not a positive integer")
        adj[u].append((v, w))
        adj[v].append((u, w))
        big = max(big, w)
    # @line L1
    r = big.bit_length()  # every weight is < 2^r
    # anc[i][v] = id of the level-i component of v; level i joins edges of weight < 2^i
    uf = list(range(n))
    by_weight = sorted(edges, key=lambda e: e[2])
    anc: list[list[int]] = []
    j = 0
    for i in range(r + 1):
        while j < len(by_weight) and by_weight[j][2] < (1 << i):
            a, b = _find(uf, by_weight[j][0]), _find(uf, by_weight[j][1])
            if a != b:
                uf[a] = b
            j += 1
        anc.append([_find(uf, v) for v in range(n)])
    heaps = [dict() for _ in range(r + 1)]  # heaps[i][component id] = list of (D, v)
    dist = [math.inf] * n
    done = [False] * n

    def push(v: int) -> None:
        for i in range(r + 1):
            heapq.heappush(heaps[i].setdefault(anc[i][v], []), (dist[v], v))

    def lowest(i: int, comp: int):
        h = heaps[i].get(comp, [])
        while h and (done[h[0][1]] or h[0][0] != dist[h[0][1]]):
            heapq.heappop(h)
        return h[0] if h else None

    def visit(i: int, comp: int, hi: float) -> None:
        if trace is not None:
            trace.append((i, min(v for v in range(n) if anc[i][v] == comp), hi))
        # @line L5
        if i == 0:
            # @line L6
            v = comp
            done[v] = True
            for x, w in adj[v]:
                # @line L7
                if not done[x] and dist[v] + w < dist[x]:
                    dist[x] = dist[v] + w
                    push(x)
            return
        while True:
            # @line L8
            top = lowest(i, comp)
            if top is None or top[0] >= hi:
                return
            # @line L9
            d, v = top
            b = d >> (i - 1)
            # @line L10
            visit(i - 1, anc[i - 1][v], (b + 1) << (i - 1))

    # @line L2
    dist[s] = 0
    push(s)
    # @line L3
    visit(r, anc[r][s], math.inf)
    # @line L4
    return [None if d == math.inf else d for d in dist]
