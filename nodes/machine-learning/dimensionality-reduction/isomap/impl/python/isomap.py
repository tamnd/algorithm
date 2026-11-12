# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isomap/. The authors are listed in prov/HKAVDA.jsonl.

"""Isomap (Tenenbaum, de Silva and Langford, 2000).

Build a k-nearest-neighbor graph (or an epsilon graph) on the points, compute
shortest path distances with Dijkstra's algorithm from each vertex, and apply
classical MDS to the matrix of graph distances.
"""

import heapq
import math


def neighbor_graph(points, k=None, eps=None):
    """Adjacency lists {j: weight}. With k, join i and j if either is among the k
    nearest neighbors of the other. With eps, join i and j if their distance is at most eps."""
    n = len(points)
    adj = [dict() for _ in range(n)]
    for i in range(n):
        dist = sorted((math.dist(points[i], points[j]), j) for j in range(n) if j != i)
        chosen = dist[:k] if k is not None else [(d, j) for d, j in dist if d <= eps]
        for d, j in chosen:
            adj[i][j] = d
            adj[j][i] = d
    return adj


def dijkstra(adj, s):
    dist = [math.inf] * len(adj)
    dist[s] = 0.0
    heap = [(0.0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u].items():
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist


def jacobi_eigh(a, max_sweeps=100):
    """Eigenvalues in descending order and the matching eigenvectors (as lists)."""
    n = len(a)
    a = [[float(x) for x in row] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = sum(x * x for row in a for x in row) or 1.0
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off <= 1e-26 * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                th = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for row in a:
                    x, y = row[p], row[q]
                    row[p], row[q] = c * x - s * y, s * x + c * y
                a[p], a[q] = ([c * x - s * y for x, y in zip(a[p], a[q])],
                              [s * x + c * y for x, y in zip(a[p], a[q])])
                for row in v:
                    x, y = row[p], row[q]
                    row[p], row[q] = c * x - s * y, s * x + c * y
    order = sorted(range(n), key=lambda i: -a[i][i])
    return [a[i][i] for i in order], [[v[r][i] for r in range(n)] for i in order]


def geodesic_distances(points, k=None, eps=None):
    adj = neighbor_graph(points, k, eps)  # @line L1
    g = []
    for s in range(len(points)):  # @line L2
        g.append(dijkstra(adj, s))  # @line L3
    if any(math.isinf(x) for row in g for x in row):  # @line L4
        raise ValueError("the neighbor graph is not connected")
    return g


def isomap(points, m, k=None, eps=None):
    """Return (Y, eigenvalues): n points in R^m and the eigenvalues of B, descending."""
    g = geodesic_distances(points, k, eps)
    n = len(g)
    a = [[x * x for x in row] for row in g]
    r = [sum(row) / n for row in a]
    tot = sum(r) / n
    b = [[-(a[i][j] - r[i] - r[j] + tot) / 2 for j in range(n)] for i in range(n)]  # @line L5
    lam, vecs = jacobi_eigh(b)  # @line L6
    scale = [math.sqrt(max(lam[j], 0.0)) for j in range(m)]
    y = [tuple(scale[j] * vecs[j][i] for j in range(m)) for i in range(n)]  # @line L7
    return y, lam  # @line L8
