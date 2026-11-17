# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mst-pseudotime/. The authors are listed in prov/MJ06W1.jsonl.
"""Pseudotime from a minimum spanning tree of cells or of cluster centers.

Two versions:

- On cells, the idea of Monocle 1 (Trapnell et al. 2014): a minimum spanning
  tree over the cells in a reduced space, its longest path as the backbone of
  the process, and for each cell the distance along the tree from a root cell
  at one end of the backbone. Monocle 1 then orders the cells with a PQ tree
  and an independent component analysis space; this version uses the tree
  distance and any coordinates it is given.
- On clusters, the idea of TSCAN (Ji and Ji 2016): a minimum spanning tree
  over the cluster centers, the path of clusters from a root cluster to the
  farthest cluster, and each cell of a cluster on the path projected onto the
  nearest path edge at its cluster. Cells of clusters off the path get None.

The tree is found by Prim's algorithm on the complete graph with Euclidean
weights, in O(n^2) time. Ties are broken by the smaller index.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

Edge = Tuple[int, int, float]


def dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def prim_mst(points: Sequence[Sequence[float]]) -> List[Edge]:
    """The edges (parent, child, weight) of a minimum spanning tree of the complete Euclidean graph."""
    n = len(points)
    if n == 0:
        return []
    inside = [False] * n
    best = [math.inf] * n
    parent = [-1] * n
    best[0] = 0.0
    edges = []
    for _ in range(n):
        u = min((v for v in range(n) if not inside[v]), key=lambda v: (best[v], v))
        inside[u] = True
        if parent[u] >= 0:
            edges.append((parent[u], u, best[u]))
        for v in range(n):
            if not inside[v]:
                w = dist(points[u], points[v])  # @line L1
                if w < best[v]:
                    best[v], parent[v] = w, u  # @line L2
    return edges


def adjacency(n: int, edges: Sequence[Edge]) -> List[List[Tuple[int, float]]]:
    adj: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    return adj


def tree_distances(adj, source: int) -> Tuple[List[float], List[int]]:
    """Distances along the tree from source, and the parent of each vertex on its path to source."""
    n = len(adj)
    d = [math.inf] * n
    par = [-1] * n
    d[source] = 0.0
    stack = [source]
    while stack:
        u = stack.pop()
        for v, w in adj[u]:
            if d[v] == math.inf:
                d[v] = d[u] + w
                par[v] = u
                stack.append(v)
    return d, par


def farthest(d: Sequence[float]) -> int:
    return max(range(len(d)), key=lambda v: (d[v], -v))


def diameter_path(adj, start: int = 0) -> List[int]:
    """A longest path of the tree, by two farthest-vertex searches."""
    a = farthest(tree_distances(adj, start)[0])  # @line L3
    d, par = tree_distances(adj, a)
    b = farthest(d)
    path = [b]
    while path[-1] != a:
        path.append(par[path[-1]])
    return path[::-1]


def cell_pseudotime(points: Sequence[Sequence[float]], root: Optional[int] = None) -> Dict[str, object]:
    """Pseudotime of each cell as the tree distance from the root.

    With root=None the root is the first end of the backbone. Returns a dict
    with 'tree', 'backbone', 'root', 'pseudotime' and 'branch_points'.
    """
    n = len(points)
    if n < 2:
        raise ValueError("need at least two cells")
    edges = prim_mst(points)
    adj = adjacency(n, edges)
    backbone = diameter_path(adj)
    if root is None:
        root = backbone[0]  # @line L4
    if not 0 <= root < n:
        raise ValueError("root out of range")
    tau = tree_distances(adj, root)[0]  # @line L5
    branch = [v for v in range(n) if len(adj[v]) >= 3]  # @line L6
    return {"tree": edges, "backbone": backbone, "root": root, "pseudotime": tau, "branch_points": branch}


def cluster_pseudotime(points: Sequence[Sequence[float]], labels: Sequence[int],
                       root_cluster: int) -> Dict[str, object]:
    """TSCAN-style pseudotime: an MST on the cluster centers and projection onto the main path."""
    ids = sorted(set(labels))
    if root_cluster not in ids:
        raise ValueError("unknown root cluster")
    pos = {c: i for i, c in enumerate(ids)}
    dim = len(points[0])
    centers = []
    for c in ids:
        members = [p for p, l in zip(points, labels) if l == c]
        centers.append([sum(p[a] for p in members) / len(members) for a in range(dim)])  # @line L7
    adj = adjacency(len(ids), prim_mst(centers))
    d, par = tree_distances(adj, pos[root_cluster])
    end = farthest(d)
    path = [end]
    while path[-1] != pos[root_cluster]:
        path.append(par[path[-1]])
    path = path[::-1]
    offset = [0.0]
    for a, b in zip(path, path[1:]):
        offset.append(offset[-1] + dist(centers[a], centers[b]))
    where = {c: i for i, c in enumerate(path)}
    tau: List[Optional[float]] = []
    for p, l in zip(points, labels):
        i = where.get(pos[l])
        if i is None:
            tau.append(None)
            continue
        best = None
        for j in (i - 1, i):  # the path edges (j, j + 1) at this cluster
            if 0 <= j < len(path) - 1:
                a, b = centers[path[j]], centers[path[j + 1]]
                L = offset[j + 1] - offset[j]
                s = sum((x - y) * (z - y) for x, y, z in zip(p, a, b)) / L
                s = min(max(s, 0.0), L)
                foot = [y + s / L * (z - y) for y, z in zip(a, b)]
                cand = (dist(p, foot), offset[j] + s)
                if best is None or cand < best:
                    best = cand
        tau.append(best[1] if best is not None else 0.0)  # @line L8
    return {"centers": centers, "path": [ids[i] for i in path], "pseudotime": tau}
