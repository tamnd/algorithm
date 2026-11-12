# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-clustering/. The authors are listed in prov/FGDG1R.jsonl.

"""Spectral clustering as in von Luxburg (2007).

The input is a symmetric similarity matrix W with non-negative entries and a zero
diagonal. Three variants are given: unnormalized spectral clustering (L = D - W),
the Shi and Malik variant (generalized eigenvectors of L u = lambda D u, the
eigenvectors of L_rw), and the Ng, Jordan and Weiss variant (eigenvectors of L_sym
with rows scaled to norm 1). The eigenvectors come from a cyclic Jacobi solver,
and the final step is Lloyd's k-means with k-means++ seeding.
"""

import math
import random
from typing import Optional, Sequence

Matrix = list


def sq_dist(x: Sequence[float], y: Sequence[float]) -> float:
    return sum((a - b) * (a - b) for a, b in zip(x, y))


# ------------------------------------------------------------ similarity graphs


def epsilon_graph(points: Sequence[Sequence[float]], eps: float) -> Matrix:
    """Unweighted graph: i and j are joined when their distance is at most eps."""
    n = len(points)
    return [[1.0 if i != j and sq_dist(points[i], points[j]) <= eps * eps else 0.0
             for j in range(n)] for i in range(n)]


def knn_graph(points: Sequence[Sequence[float]], k: int, mutual: bool = False) -> Matrix:
    """Unweighted k-nearest-neighbor graph, made symmetric by 'or' (or by 'and' if mutual)."""
    n = len(points)
    near = []
    for i in range(n):
        order = sorted((sq_dist(points[i], points[j]), j) for j in range(n) if j != i)
        near.append({j for _, j in order[:k]})
    W = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                a, b = j in near[i], i in near[j]
                if (a and b) if mutual else (a or b):
                    W[i][j] = 1.0
    return W


def gaussian_graph(points: Sequence[Sequence[float]], sigma: float) -> Matrix:
    """Fully connected graph with w_ij = exp(-|x_i - x_j|^2 / (2 sigma^2))."""
    n = len(points)
    return [[0.0 if i == j else math.exp(-sq_dist(points[i], points[j]) / (2 * sigma * sigma))
             for j in range(n)] for i in range(n)]


# ------------------------------------------------------------ Laplacians


def degrees(W: Matrix) -> list:
    return [sum(row) for row in W]


def laplacian(W: Matrix, kind: str = "unnormalized") -> Matrix:
    """L = D - W, L_sym = I - D^(-1/2) W D^(-1/2), or L_rw = I - D^(-1) W."""
    n = len(W)
    d = degrees(W)
    if kind == "unnormalized":
        return [[(d[i] if i == j else 0) - W[i][j] for j in range(n)] for i in range(n)]
    if any(x <= 0 for x in d):
        raise ValueError("a normalized Laplacian needs every degree to be positive")
    if kind == "sym":
        return [[(1.0 if i == j else 0.0) - W[i][j] / math.sqrt(d[i] * d[j])
                 for j in range(n)] for i in range(n)]
    if kind == "rw":
        return [[(1 if i == j else 0) - W[i][j] / d[i] for j in range(n)] for i in range(n)]
    raise ValueError(kind)


# ------------------------------------------------------------ eigenvectors


def jacobi_eigh(A: Matrix, tol: float = 1e-13, max_sweeps: int = 100):
    """Eigenvalues (ascending) and eigenvectors (as columns of V) of a symmetric matrix."""
    n = len(A)
    a = [[float(x) for x in row] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = max(1.0, max((abs(x) for row in a for x in row), default=0.0))
    for _ in range(max_sweeps):
        off = sum(a[p][q] * a[p][q] for p in range(n) for q in range(p + 1, n))
        if off <= (tol * scale) ** 2:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for r in range(n):  # A <- A J
                    arp, arq = a[r][p], a[r][q]
                    a[r][p], a[r][q] = c * arp - s * arq, s * arp + c * arq
                for r in range(n):  # A <- J^T A
                    apr, aqr = a[p][r], a[q][r]
                    a[p][r], a[q][r] = c * apr - s * aqr, s * apr + c * aqr
                for r in range(n):  # V <- V J
                    vrp, vrq = V[r][p], V[r][q]
                    V[r][p], V[r][q] = c * vrp - s * vrq, s * vrp + c * vrq
    order = sorted(range(n), key=lambda i: a[i][i])
    vals = [a[i][i] for i in order]
    vecs = [[V[r][i] for i in order] for r in range(n)]
    return vals, vecs


# ------------------------------------------------------------ k-means on the rows


def k_means(Y: Sequence[Sequence[float]], k: int, rng: random.Random, iters: int = 100) -> list:
    """Lloyd's algorithm with k-means++ seeding. Returns a label in 0..k-1 for each row."""
    n = len(Y)
    centers = [list(Y[rng.randrange(n)])]
    while len(centers) < k:
        w = [min(sq_dist(y, c) for c in centers) for y in Y]
        total = sum(w)
        if total <= 0:
            centers.append(list(Y[rng.randrange(n)]))
            continue
        x, acc = rng.random() * total, 0.0
        for i in range(n):
            acc += w[i]
            if acc >= x and w[i] > 0:
                break
        centers.append(list(Y[i]))
    labels = [-1] * n
    for _ in range(iters):
        new = [min(range(k), key=lambda j: sq_dist(y, centers[j])) for y in Y]
        if new == labels:
            break
        labels = new
        for j in range(k):
            members = [Y[i] for i in range(n) if labels[i] == j]
            if members:
                centers[j] = [sum(col) / len(members) for col in zip(*members)]
    return labels


# ------------------------------------------------------------ the algorithm


def spectral_embedding(W: Matrix, k: int, method: str = "njw") -> list:
    """The n x k matrix whose rows are clustered by k-means (lines L1 to L8)."""
    n = len(W)
    d = degrees(W)  # @line L1
    if method == "unnormalized":
        M = laplacian(W, "unnormalized")  # @line L2
    elif method in ("shi-malik", "njw"):
        M = laplacian(W, "sym")  # @line L3
    else:
        raise ValueError(method)
    _, vecs = jacobi_eigh(M)  # @line L4
    U = [[vecs[i][j] for j in range(k)] for i in range(n)]  # @line L5
    if method == "shi-malik":
        U = [[x / math.sqrt(d[i]) for x in U[i]] for i in range(n)]  # @line L6
    if method == "njw":
        U = [[x / (math.sqrt(sum(v * v for v in row)) or 1.0) for x in row] for row in U]  # @line L7
    return U  # @line L8


def spectral_clustering(W: Matrix, k: int, method: str = "njw",
                        rng: Optional[random.Random] = None) -> list:
    """Return a cluster label in 0..k-1 for each vertex."""
    rng = rng if rng is not None else random.Random(0)
    Y = spectral_embedding(W, k, method)
    return k_means(Y, k, rng)  # @line L9


def as_partition(labels: Sequence[int]) -> set:
    """The partition of the indices that a labeling defines (labels do not matter)."""
    groups: dict = {}
    for i, c in enumerate(labels):
        groups.setdefault(c, []).append(i)
    return {frozenset(g) for g in groups.values()}  # @line L10
