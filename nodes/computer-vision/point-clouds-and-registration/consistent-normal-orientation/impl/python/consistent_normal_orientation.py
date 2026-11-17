# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-normal-orientation/. The authors are listed in prov/4CA5PS.jsonl.
"""Consistent orientation of point cloud normals by propagation along a
minimum spanning tree (Hoppe, DeRose, Duchamp, McDonald and Stuetzle, 1992).

1. The Riemannian graph has the edges of the Euclidean minimum spanning tree
   (EMST) of the points and the edges of the k-nearest neighbor graph.
2. The edge (i, j) has the cost 1 - |n_i . n_j|: small when the two normals
   are close to parallel, whatever their signs.
3. A minimum spanning tree of this graph is taken, and rooted at the point of
   largest z, whose normal is turned to have n_z >= 0.
4. A depth-first traversal from the root flips each child normal that points
   against its parent's normal.

This is a heuristic: it is exact along the tree edges, but it can fail where
the tree crosses a thin part or a sharp edge.

The EMST is computed here by Prim's algorithm on the complete graph, O(n^2),
and the k nearest neighbors by a brute force scan.
"""

from __future__ import annotations

import heapq
import math
from typing import Dict, List, Sequence, Set, Tuple

Vec3 = Tuple[float, float, float]


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def emst_edges(points: Sequence[Sequence[float]]) -> List[Tuple[int, int]]:
    """The edges of a Euclidean minimum spanning tree, by dense Prim, O(n^2)."""
    n = len(points)
    if n == 0:
        return []
    inside = [False] * n
    best = [math.inf] * n
    parent = [-1] * n
    best[0] = 0.0
    edges = []
    for _ in range(n):
        u = min((i for i in range(n) if not inside[i]), key=lambda i: best[i])
        inside[u] = True
        if parent[u] >= 0:
            edges.append((parent[u], u))
        for v in range(n):
            if not inside[v]:
                d = math.dist(points[u], points[v])
                if d < best[v]:
                    best[v], parent[v] = d, u
    return edges


def riemannian_graph(points: Sequence[Sequence[float]], k: int) -> Dict[int, Set[int]]:
    """EMST edges plus the symmetric k-nearest neighbor edges."""
    n = len(points)
    adj: Dict[int, Set[int]] = {i: set() for i in range(n)}
    for i, j in emst_edges(points):
        adj[i].add(j)
        adj[j].add(i)
    for i in range(n):
        others = heapq.nsmallest(k, (j for j in range(n) if j != i),
                                 key=lambda j: math.dist(points[i], points[j]))
        for j in others:
            adj[i].add(j)
            adj[j].add(i)
    return adj


def orient_normals(points: Sequence[Sequence[float]], normals: Sequence[Sequence[float]],
                   k: int) -> List[Vec3]:
    """Return the normals with signs made consistent. The input normals are
    unit vectors with arbitrary signs."""
    n = len(points)
    if n == 0:
        return []
    adj = riemannian_graph(points, k)  # @line L1
    weight = lambda i, j: 1.0 - abs(_dot(normals[i], normals[j]))  # @line L2
    # Prim's algorithm on the Riemannian graph, rooted at the highest point.
    root = max(range(n), key=lambda i: (points[i][2], -i))  # @line L3
    inside = [False] * n
    children: List[List[int]] = [[] for _ in range(n)]
    heap = [(0.0, root, -1)]
    while heap:  # @line L4
        w, v, p = heapq.heappop(heap)
        if inside[v]:
            continue
        inside[v] = True
        if p >= 0:
            children[p].append(v)
        for u in adj[v]:
            if not inside[u]:
                heapq.heappush(heap, (weight(v, u), u, v))
    # The EMST edges make the graph connected, so every point is now inside.
    out: List[Vec3] = [tuple(m) for m in normals]  # type: ignore[misc]
    if out[root][2] < 0:  # @line L5
        out[root] = (-out[root][0], -out[root][1], -out[root][2])
    stack = [root]  # @line L6
    while stack:  # @line L7
        i = stack.pop()  # @line L8
        for j in children[i]:  # @line L9
            if _dot(out[i], out[j]) < 0:  # @line L10
                out[j] = (-out[j][0], -out[j][1], -out[j][2])
            stack.append(j)  # @line L11
    return out  # @line L12
