# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prim-dijkstra-tradeoff/. The authors are listed in prov/93CM0J.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Point = tuple[int, int]
Number = Union[int, Fraction]


def l1(p: Point, q: Point) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def prim_dijkstra_tradeoff(points: Sequence[Point], c: Number, source: int = 0) -> tuple[list[int], list[int]]:
    """Alpert, Hu, Huang, Kahng and Karger's Prim-Dijkstra tree with parameter 0 <= c <= 1.

    Grows a spanning tree from the source. Each step adds the point v and tree
    point u that minimize c * d(u) + dist(u, v), where d(u) is the length of the
    tree path from the source to u. c = 0 gives Prim's minimum spanning tree and
    c = 1 gives a shortest path tree. Returns (parent, d); parent[source] = -1.
    Ties go to the smaller index of v, then of u. Runs in O(n^2) time.
    """
    if not 0 <= c <= 1:
        raise ValueError("c must lie in [0, 1]")
    n = len(points)
    parent = [-1] * n
    d = [0] * n
    if n == 0:
        return parent, d
    in_tree = [False] * n
    in_tree[source] = True
    key: list[Number] = [l1(points[source], p) for p in points]  # @line L1
    best_u = [source] * n
    for _ in range(n - 1):  # @line L2
        v = min((i for i in range(n) if not in_tree[i]), key=lambda i: (key[i], i))  # @line L3
        u = best_u[v]
        in_tree[v] = True
        parent[v] = u
        d[v] = d[u] + l1(points[u], points[v])  # @line L4
        for w in range(n):  # @line L5
            if not in_tree[w]:
                k = c * d[v] + l1(points[v], points[w])
                if k < key[w]:  # @line L6
                    key[w] = k
                    best_u[w] = v
    return parent, d  # @line L7


def tree_cost(points: Sequence[Point], parent: Sequence[int]) -> int:
    return sum(l1(points[v], points[u]) for v, u in enumerate(parent) if u >= 0)
