# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-gene-coexpression-network-analysis/. The authors are listed in prov/WN4DQ5.jsonl.
"""Weighted gene coexpression network analysis (Zhang and Horvath 2005).

expr is a list of rows, one row per gene and one column per sample. The
steps are: Pearson correlations r_ij; the soft-threshold adjacency
a_ij = |r_ij|^beta (unsigned) or ((1 + r_ij) / 2)^beta (signed); the
topological overlap

    TOM_ij = (l_ij + a_ij) / (min(k_i, k_j) + 1 - a_ij),
    l_ij = sum_{u != i, j} a_iu a_uj,   k_i = sum_{u != i} a_iu;

average-linkage clustering of 1 - TOM; a cut of the tree at a fixed height
(a static cut, not the Dynamic Tree Cut of the WGCNA package); and the
eigengene of each module, the first principal component of its standardized
genes. scale_free_fit gives the R^2 of log10 p(k) against log10 k over
equal-width bins of k, the fit used to choose beta.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

Matrix = List[List[float]]


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("need two vectors of the same length >= 2")
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        raise ValueError("a gene has no variation")
    return max(-1.0, min(1.0, sxy / math.sqrt(sxx * syy)))


def correlation_matrix(expr: Sequence[Sequence[float]]) -> Matrix:
    n = len(expr)
    r = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            r[i][j] = r[j][i] = pearson(expr[i], expr[j])  # @line L1
    return r


def adjacency(r: Sequence[Sequence[float]], beta: float, signed: bool = False) -> Matrix:
    """Soft-threshold adjacency; the diagonal is 1."""
    n = len(r)
    a = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                base = (1.0 + r[i][j]) / 2.0 if signed else abs(r[i][j])
                a[i][j] = base ** beta  # @line L2
    return a


def connectivity(a: Sequence[Sequence[float]]) -> List[float]:
    """k_i = sum over u != i of a_iu."""
    n = len(a)
    return [sum(a[i][u] for u in range(n) if u != i) for i in range(n)]


def topological_overlap(a: Sequence[Sequence[float]]) -> Matrix:
    """The topological overlap matrix of an adjacency with entries in [0, 1]."""
    n = len(a)
    k = connectivity(a)  # @line L3
    t = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            shared = sum(a[i][u] * a[u][j] for u in range(n) if u != i and u != j)
            t[i][j] = t[j][i] = (shared + a[i][j]) / (min(k[i], k[j]) + 1.0 - a[i][j])  # @line L4
    return t


def average_linkage(d: Sequence[Sequence[float]]) -> List[Tuple[int, int, float, Tuple[int, ...]]]:
    """Agglomerative clustering with average linkage (UPGMA) on the distance matrix d.

    Returns the n - 1 merges as (id_a, id_b, height, members). Leaves have
    ids 0..n-1 and the cluster made by merge t has id n + t. Ties go to the
    pair with the smallest ids. Distances are updated by the Lance-Williams
    rule d(k, a + b) = (n_a d(k, a) + n_b d(k, b)) / (n_a + n_b).
    """
    n = len(d)
    members: Dict[int, Tuple[int, ...]] = {i: (i,) for i in range(n)}
    dist: Dict[Tuple[int, int], float] = {}
    for i in range(n):
        for j in range(i + 1, n):
            dist[(i, j)] = d[i][j]
    merges = []
    next_id = n
    while len(members) > 1:
        (ia, ib), h = min(dist.items(), key=lambda kv: (kv[1], kv[0]))
        na, nb = len(members[ia]), len(members[ib])
        new = tuple(sorted(members[ia] + members[ib]))
        del members[ia], members[ib]
        for c in members:
            dac = dist.pop((min(c, ia), max(c, ia)))
            dbc = dist.pop((min(c, ib), max(c, ib)))
            dist[(c, next_id)] = (na * dac + nb * dbc) / (na + nb)
        del dist[(ia, ib)]
        members[next_id] = new
        merges.append((ia, ib, h, new))
        next_id += 1
    return merges


def cut_tree(merges, n: int, height: float, min_size: int = 1) -> List[int]:
    """Labels from a static cut: merges at height <= height are kept.

    Modules are numbered 1, 2, ... by decreasing size (ties by smallest
    gene); genes in clusters smaller than min_size get label 0.
    """
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for _, _, h, mem in merges:
        if h <= height:
            root = find(mem[0])
            for g in mem[1:]:
                parent[find(g)] = root
    groups: Dict[int, List[int]] = {}
    for g in range(n):
        groups.setdefault(find(g), []).append(g)
    big = sorted((grp for grp in groups.values() if len(grp) >= min_size), key=lambda grp: (-len(grp), grp[0]))
    labels = [0] * n
    for lab, grp in enumerate(big, start=1):
        for g in grp:
            labels[g] = lab
    return labels


def standardize(row: Sequence[float]) -> List[float]:
    n = len(row)
    m = sum(row) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in row) / (n - 1))
    if sd == 0:
        raise ValueError("a gene has no variation")
    return [(x - m) / sd for x in row]


def eigengene(expr: Sequence[Sequence[float]], iters: int = 1000, tol: float = 1e-13) -> List[float]:
    """The first right singular vector of the standardized module matrix (unit length).

    Found by power iteration on the samples-by-samples matrix X^T X. Its sign
    is set so that it has a nonnegative correlation with the mean of the
    standardized genes.
    """
    x = [standardize(row) for row in expr]
    m = len(x[0])
    c = [[sum(row[s] * row[t] for row in x) for t in range(m)] for s in range(m)]
    avg = [sum(row[s] for row in x) / len(x) for s in range(m)]
    v = [1.0 + 0.01 * s for s in range(m)]
    norm = math.sqrt(sum(t * t for t in v))
    v = [t / norm for t in v]
    for _ in range(iters):
        w = [sum(c[s][t] * v[t] for t in range(m)) for s in range(m)]
        norm = math.sqrt(sum(t * t for t in w))
        if norm == 0:
            break
        w = [t / norm for t in w]
        if w[0] * v[0] < 0:
            w = [-t for t in w]
        done = max(abs(a - b) for a, b in zip(w, v)) < tol
        v = w
        if done:
            break
    if sum(a * b for a, b in zip(v, avg)) < 0:
        v = [-t for t in v]
    return v


def scale_free_fit(k: Sequence[float], n_bins: int = 10) -> Tuple[float, float]:
    """(R^2, slope) of the least-squares line of log10 p(k) on log10 mean k, over the non-empty bins."""
    lo, hi = min(k), max(k)
    if hi <= lo or lo <= 0:
        raise ValueError("need positive connectivities that are not all equal")
    width = (hi - lo) / n_bins
    bins: Dict[int, List[float]] = {}
    for v in k:
        b = min(int((v - lo) / width), n_bins - 1)
        bins.setdefault(b, []).append(v)
    xs = [math.log10(sum(vs) / len(vs)) for _, vs in sorted(bins.items())]
    ys = [math.log10(len(vs) / len(k)) for _, vs in sorted(bins.items())]
    if len(xs) < 3:
        raise ValueError("need at least three non-empty bins")
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((a - mx) ** 2 for a in xs)
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    syy = sum((b - my) ** 2 for b in ys)
    slope = sxy / sxx
    r2 = sxy * sxy / (sxx * syy) if syy > 0 else 1.0
    return r2, slope


def wgcna(expr: Sequence[Sequence[float]], beta: float, height: float, min_size: int = 1,
          signed: bool = False):
    """Module labels and module eigengenes (a dict from label to eigengene; label 0 has none)."""
    r = correlation_matrix(expr)
    a = adjacency(r, beta, signed)
    t = topological_overlap(a)
    d = [[1.0 - v for v in row] for row in t]  # @line L5
    merges = average_linkage(d)  # @line L6
    labels = cut_tree(merges, len(expr), height, min_size)  # @line L7
    eig = {}
    for lab in sorted(set(labels) - {0}):
        eig[lab] = eigengene([expr[g] for g in range(len(expr)) if labels[g] == lab])  # @line L8
    return labels, eig  # @line L9
