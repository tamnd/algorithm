# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pettie-ramachandran-mst/. The authors are listed in prov/BJQNXT.jsonl.

"""A structural model of the Pettie-Ramachandran optimal MST algorithm.

The recursion, the partition into small pieces with corrupted edges, the
contraction, the dense step and the two Borůvka steps follow the algorithm.
Three parts are replaced by simple stand-ins, which do not change the output:

* The optimal decision trees for the pieces are replaced by Kruskal's
  algorithm on each piece. A decision tree computes the same forest.
* The soft heap is replaced by a binary heap. The caller may pass a function
  `corrupt` that raises the key of an edge when it enters the heap, which
  models the corruption of a soft heap. With no function, nothing is
  corrupted.
* The linear-time dense MSF algorithm is replaced by Kruskal's algorithm.

So this code shows the structure and is checked for correctness; it does not
have the optimal running time.
"""

import heapq
import math
from typing import Callable

Edge = tuple[int, int, float, int]  # (u, v, w, index in the input)


def _kruskal(n: int, edges: list[Edge]) -> list[Edge]:
    """Minimum spanning forest for the key (w, index)."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []
    for e in sorted(edges, key=lambda e: (e[2], e[3])):
        a, b = find(e[0]), find(e[1])
        if a != b:
            parent[a] = b
            out.append(e)
    return out


def _contract(n: int, forest: list[Edge]) -> tuple[int, list[int]]:
    """Label the components of (0..n-1, forest) by 0..c-1."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v, _, _ in forest:
        parent[find(u)] = find(v)
    label: dict[int, int] = {}
    lab = []
    for x in range(n):
        lab.append(label.setdefault(find(x), len(label)))
    return len(label), lab


def _relabel(lab: list[int], edges: list[Edge]) -> list[Edge]:
    """Map edges through the labels and drop the self-loops."""
    return [(lab[u], lab[v], w, i) for u, v, w, i in edges if lab[u] != lab[v]]


def _partition(n: int, edges: list[Edge], r: int, corrupt) -> tuple[list[list[int]], set[int], list[Edge]]:
    """Grow pieces of at most r vertices with a heap that may corrupt keys.

    Returns the pieces, the set C of corrupted edge indices, and the link
    edges by which a piece stopped at an earlier piece.
    """
    adj: list[list[Edge]] = [[] for _ in range(n)]
    for e in edges:
        adj[e[0]].append(e)
        if e[1] != e[0]:
            adj[e[1]].append(e)
    dead = [False] * n
    bad: set[int] = set()
    pieces: list[list[int]] = []
    links: list[Edge] = []
    for v in range(n):
        if dead[v]:
            continue
        inside = {v}
        heap: list = []
        raised: set[int] = set()

        def insert(x: int) -> None:
            for e in adj[x]:
                y = e[1] if e[0] == x else e[0]
                if e[3] in bad or y in inside:
                    continue
                bump = corrupt(e[3]) if corrupt else 0
                if bump > 0:
                    raised.add(e[3])
                heapq.heappush(heap, ((e[2] + bump, e[3]), x, y, e))

        insert(v)
        while heap and len(inside) < r:
            _, x, y, e = heapq.heappop(heap)
            if e[3] in raised:
                bad.add(e[3])
                continue
            if y in inside:
                continue
            if dead[y]:
                links.append(e)
                break
            inside.add(y)
            insert(y)
        bad |= {item[3][3] for item in heap if item[3][3] in raised}
        for x in inside:
            dead[x] = True
        pieces.append(sorted(inside))
    return pieces, bad, links


def _boruvka_step(n: int, edges: list[Edge]) -> list[Edge]:
    """One Borůvka step: the least edge at each vertex, for the key (w, index)."""
    best: dict[int, Edge] = {}
    for e in edges:
        for x in (e[0], e[1]):
            if x not in best or (e[2], e[3]) < (best[x][2], best[x][3]):
                best[x] = e
    return list({e[3]: e for e in best.values()}.values())


def _optimal_msf(n: int, edges: list[Edge], r: int | None, corrupt) -> set[int]:
    edges = [e for e in edges if e[0] != e[1]]
    if not edges:  # @line L1
        return set()
    rr = r if r is not None else max(2, math.ceil(math.log2(max(2.0, math.log2(max(2.0, math.log2(max(2, n))))))))  # @line L2
    pieces, bad, links = _partition(n, edges, rr, corrupt)  # @line L3
    piece_of = [0] * n
    for k, p in enumerate(pieces):
        for x in p:
            piece_of[x] = k
    inner: list[list[Edge]] = [[] for _ in pieces]
    for e in edges:
        if e[3] not in bad and piece_of[e[0]] == piece_of[e[1]]:
            inner[piece_of[e[0]]].append(e)
    forest = list(links)  # @line L4
    for p, es in zip(pieces, inner):
        local = {x: j for j, x in enumerate(p)}
        sub = [(local[u], local[v], w, i) for u, v, w, i in es]
        back = {e[3]: e for e in es}
        forest += [back[e[3]] for e in _kruskal(len(p), sub)]
    na, lab = _contract(n, forest)
    ga = _relabel(lab, [e for e in edges if e[3] not in bad])  # @line L5
    fa_ids = {e[3] for e in _kruskal(na, ga)}  # @line L6
    gb = [e for e in edges if e[3] in fa_ids or e[3] in bad] + forest  # @line L7
    gb = list({e[3]: e for e in gb}.values())
    fb: set[int] = set()  # @line L8
    nc, cur = n, gb
    for _ in range(2):
        step = _boruvka_step(nc, cur)
        if not step:
            break
        fb |= {e[3] for e in step}
        nc, lab2 = _contract(nc, step)
        cur = _relabel(lab2, cur)
    rest = _optimal_msf(nc, cur, r, corrupt)  # @line L9
    return fb | rest  # @line L10


def pettie_ramachandran_mst(
    n: int,
    edges: list[tuple[int, int, float]],
    r: int | None = None,
    corrupt: Callable[[int], float] | None = None,
) -> list[int]:
    """Return the indices of the edges of a minimum spanning forest, in increasing order.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge of weight w. Weights may be negative and may tie; ties are broken by
    the edge index, so the result is the unique minimum forest for the order
    (w, index). The graph may be disconnected, and parallel edges and
    self-loops are allowed. r is the largest piece size, by default
    max(2, ceil(log2 log2 log2 n)). corrupt(i) returns how much to raise the
    key of edge i when it enters the partition heap; 0 means no corruption.

    Cost: with the stand-ins of this module, O(m log m) time per level of the
    recursion and O(n + m) extra space per level, where m = len(edges).
    """
    es = [(u, v, w, i) for i, (u, v, w) in enumerate(edges)]
    return sorted(_optimal_msf(n, es, r, corrupt))
