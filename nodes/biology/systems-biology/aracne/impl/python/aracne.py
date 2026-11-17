# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aracne/. The authors are listed in prov/VF2D8H.jsonl.
"""ARACNE: mutual information network with data processing inequality pruning.

The expression data is a list of m genes, and each gene is a list of n
samples (floats). Genes are numbered 0 .. m-1 in the code (the page numbers
them from 1). An edge is a pair (i, j) with i < j.

The original method of Margolin et al. (2006) estimates mutual information
with a Gaussian kernel estimator on rank (copula) transformed data, and picks
the threshold I0 from a permutation null. This file uses a plug-in estimate on
equal-frequency bins of the ranks, and takes I0 as a parameter. The pruning
step (lines L4 to L8 of the page) is the same as in the paper.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Set, Tuple

Edge = Tuple[int, int]


def ranks(xs: Sequence[float]) -> List[int]:
    """Rank of each value, 0 .. n-1. Ties are broken by position (stable)."""
    order = sorted(range(len(xs)), key=lambda s: xs[s])
    r = [0] * len(xs)
    for pos, s in enumerate(order):
        r[s] = pos
    return r


def equal_frequency_bins(xs: Sequence[float], b: int) -> List[int]:
    """Bin index 0 .. b-1 of each value: rank r goes to bin floor(r b / n)."""
    n = len(xs)
    return [r * b // n for r in ranks(xs)]


def mutual_information_binned(x: Sequence[float], y: Sequence[float], b: int) -> float:
    """Plug-in mutual information, in nats, of two samples on b x b rank bins."""
    if len(x) != len(y) or len(x) == 0:
        raise ValueError("x and y must have the same positive length")
    return mi_from_bins(equal_frequency_bins(x, b), equal_frequency_bins(y, b), b)


def mi_from_bins(bx: Sequence[int], by: Sequence[int], b: int) -> float:
    """Plug-in mutual information, in nats, of two binned samples; O(n + b^2) time."""
    n = len(bx)
    joint: Dict[Tuple[int, int], int] = {}
    cx = [0] * b
    cy = [0] * b
    for s in range(n):
        joint[(bx[s], by[s])] = joint.get((bx[s], by[s]), 0) + 1
        cx[bx[s]] += 1
        cy[by[s]] += 1
    mi = 0.0
    for (u, v), c in joint.items():
        mi += c / n * math.log(c * n / (cx[u] * cy[v]))
    return mi


def gaussian_mutual_information(rho: float) -> float:
    """Mutual information, in nats, of two jointly normal variables with correlation rho."""
    return -0.5 * math.log(1.0 - rho * rho)


def mi_matrix(data: Sequence[Sequence[float]], b: int) -> List[List[float]]:
    """Symmetric m x m matrix of binned mutual information (diagonal 0)."""
    m = len(data)
    bins = [equal_frequency_bins(gene, b) for gene in data]  # one sort per gene
    mi = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            v = mi_from_bins(bins[i], bins[j], b)  # @line L2
            mi[i][j] = mi[j][i] = v
    return mi


def aracne_prune(mi: Sequence[Sequence[float]], threshold: float, tolerance: float = 0.0) -> Set[Edge]:
    """Lines L3 to L8: threshold the matrix, then apply the DPI to every triangle.

    An edge e of a triangle whose three edges all pass the threshold is removed
    when I(e) < (1 - tolerance) * I(f) for both other edges f of the triangle.
    All removals are decided on the thresholded graph and applied at the end,
    so the result does not depend on the order of the genes.
    """
    m = len(mi)
    if not 0.0 <= tolerance < 1.0:
        raise ValueError("tolerance must be in [0, 1)")
    keep = 1.0 - tolerance
    adj: List[Set[int]] = [set() for _ in range(m)]
    edges: Set[Edge] = set()
    for i in range(m):
        for j in range(i + 1, m):
            if mi[i][j] > threshold:  # @line L3
                edges.add((i, j))
                adj[i].add(j)
                adj[j].add(i)
    removed: Set[Edge] = set()  # @line L4
    for i, j in sorted(edges):
        for k in sorted(adj[i] & adj[j]):
            if k <= j:
                continue  # @line L5
            # the triangle i < j < k, visited once
            tri = ((i, j), (i, k), (j, k))  # @line L6
            for e in tri:
                others = [f for f in tri if f != e]
                ie = mi[e[0]][e[1]]
                if all(ie < keep * mi[f[0]][f[1]] for f in others):  # @line L7
                    removed.add(e)
    return edges - removed  # @line L8


def aracne(data: Sequence[Sequence[float]], threshold: float, tolerance: float = 0.0, b: int = 4) -> Set[Edge]:
    """Lines L1 to L8: estimate all pairwise MI values, then prune."""
    for gene in data:  # @line L1
        if len(gene) != len(data[0]):
            raise ValueError("every gene needs the same number of samples")
    return aracne_prune(mi_matrix(data, b), threshold, tolerance)


def tree_correlations(m: int, parent: Sequence[int], r: Sequence[float]) -> List[List[float]]:
    """Exact correlations of a Gaussian tree model.

    Gene 0 is the root, parent[c] < c is the parent of gene c >= 1, and r[c] is
    the correlation of gene c with its parent. The correlation of two genes is
    the product of r over the edges of the path between them.
    """
    path_to_root = []
    for c in range(m):
        p = [c]
        while p[-1] != 0:
            p.append(parent[p[-1]])
        path_to_root.append(p)
    rho = [[1.0] * m for _ in range(m)]
    for a in range(m):
        for b2 in range(a + 1, m):
            pa, pb = path_to_root[a], set(path_to_root[b2])
            lca = next(v for v in pa if v in pb)
            prod = 1.0
            for v in pa:
                if v == lca:
                    break
                prod *= r[v]
            for v in path_to_root[b2]:
                if v == lca:
                    break
                prod *= r[v]
            rho[a][b2] = rho[b2][a] = prod
    return rho


def simulate_tree(rng, m: int, parent: Sequence[int], r: Sequence[float], n: int) -> List[List[float]]:
    """n samples of the Gaussian tree model, gene by gene in index order per sample.

    Each sample draws gene 0 then genes 1 .. m-1 with rng.gauss(0, 1):
    x_c = r[c] x_parent + sqrt(1 - r[c]^2) z.
    """
    data = [[0.0] * n for _ in range(m)]
    for s in range(n):
        data[0][s] = rng.gauss(0.0, 1.0)
        for c in range(1, m):
            data[c][s] = r[c] * data[parent[c]][s] + math.sqrt(1.0 - r[c] * r[c]) * rng.gauss(0.0, 1.0)
    return data
