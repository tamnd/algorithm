# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-nearest-neighbor-clustering/. The authors are listed in prov/6JJNPV.jsonl.
"""Clustering of cells on a shared nearest neighbor graph with the Louvain method.

The steps are those of PhenoGraph (Levine et al. 2015) and of the Seurat
pipeline: the k nearest neighbors of each cell in PCA space, edge weights from
the overlap of the neighbor sets (the Jaccard index), and communities of
high modularity found by the Louvain method of Blondel et al. (2008).

Choices of this version:
- The neighbor set of cell i is i with its k nearest neighbors, as in Seurat.
  PhenoGraph leaves i out. With i in the set, every edge of the k-nearest-
  neighbor graph gets a positive weight.
- Neighbor search is brute force and the Louvain method visits the vertices in
  index order and breaks ties by the smaller community label, so the output
  is deterministic. Real tools use approximate neighbor search and a random
  vertex order.
- There is no pruning of small weights and no Leiden refinement.

A graph is a list of dicts: adj[i][j] is the weight of the pair (i, j), and
adj[i][j] == adj[j][i]. Sums run over ordered pairs, so a self-loop weight
adj[c][c] after aggregation is the total weight of the ordered pairs inside c.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from rq3lin import knn, pca_fit, pca_project

Graph = List[Dict[int, float]]
EPS = 1e-12


def snn_graph(points: Sequence[Sequence[float]], k: int) -> Graph:
    """Shared nearest neighbor graph: Jaccard weights on the edges of the k-NN graph."""
    n = len(points)
    nbrs = knn(points, k)  # @line L2
    sets = [set(nbrs[i]) | {i} for i in range(n)]
    adj: Graph = [dict() for _ in range(n)]
    for i in range(n):
        for j in nbrs[i]:  # @line L3
            if j in adj[i]:
                continue
            w = len(sets[i] & sets[j]) / len(sets[i] | sets[j])  # @line L4
            adj[i][j] = w
            adj[j][i] = w
    return adj


def degrees(adj: Graph) -> List[float]:
    return [sum(row.values()) for row in adj]


def modularity(adj: Graph, labels: Sequence[int], resolution: float = 1.0) -> float:
    """Q = (1 / 2m) sum over ordered pairs (i, j) in one community of (A_ij - gamma k_i k_j / 2m)."""
    k = degrees(adj)
    two_m = sum(k)
    if two_m == 0:
        return 0.0
    inside = sum(w for i, row in enumerate(adj) for j, w in row.items() if labels[i] == labels[j])
    tot: Dict[int, float] = {}
    for i, c in enumerate(labels):
        tot[c] = tot.get(c, 0.0) + k[i]
    return inside / two_m - resolution * sum(t * t for t in tot.values()) / (two_m * two_m)


def local_moving(adj: Graph, resolution: float = 1.0) -> Tuple[List[int], int]:
    """Phase 1 of Louvain: move single vertices while the modularity grows.

    Returns (community of each vertex, number of moves).
    """
    n = len(adj)
    k = degrees(adj)
    two_m = sum(k)
    comm = list(range(n))  # @line L5
    tot = k[:]
    moves = 0
    changed = True
    while changed:  # @line L8
        changed = False
        for i in range(n):  # @line L6
            c0 = comm[i]
            links: Dict[int, float] = {}
            for j, w in adj[i].items():
                if j != i:
                    links[comm[j]] = links.get(comm[j], 0.0) + w
            tot[c0] -= k[i]
            best = c0
            best_gain = links.get(c0, 0.0) - resolution * k[i] * tot[c0] / two_m
            for c in sorted(links):
                gain = links[c] - resolution * k[i] * tot[c] / two_m  # @line L7
                if gain > best_gain + EPS:
                    best, best_gain = c, gain
            tot[best] += k[i]
            comm[i] = best
            if best != c0:
                moves += 1
                changed = True
    return comm, moves


def relabel(comm: Sequence[int]) -> List[int]:
    """Labels 0, 1, 2, ... in the order of first appearance."""
    seen: Dict[int, int] = {}
    return [seen.setdefault(c, len(seen)) for c in comm]


def aggregate(adj: Graph, comm: Sequence[int]) -> Graph:
    """One vertex per community; the weight of (C, D) is the sum of the weights of the ordered pairs from C to D."""
    r = max(comm) + 1
    out: Graph = [dict() for _ in range(r)]
    for i, row in enumerate(adj):
        for j, w in row.items():
            a, b = comm[i], comm[j]
            out[a][b] = out[a].get(b, 0.0) + w  # @line L9
    return out


def louvain(adj: Graph, resolution: float = 1.0) -> Tuple[List[int], List[List[int]]]:
    """Louvain method: local moving and aggregation until no vertex moves.

    Returns (labels of the input vertices, labels after each level).
    """
    labels = list(range(len(adj)))
    levels = []
    g = adj
    if sum(degrees(adj)) == 0:
        return labels, levels
    while True:
        comm, moves = local_moving(g, resolution)
        if moves == 0:  # @line L10
            break
        comm = relabel(comm)
        labels = [comm[c] for c in labels]
        levels.append(labels[:])
        g = aggregate(g, comm)
    return labels, levels  # @line L11


def snn_cluster(X: Sequence[Sequence[float]], k: int = 10, n_pcs: Optional[int] = None,
                resolution: float = 1.0) -> List[int]:
    """Cluster the rows of X (cells by features): optional PCA, SNN graph, Louvain."""
    pts = X
    if n_pcs is not None:
        mu, axes, _ = pca_fit(X, n_pcs)
        pts = pca_project(X, mu, axes)  # @line L1
    return louvain(snn_graph(pts, k), resolution)[0]
