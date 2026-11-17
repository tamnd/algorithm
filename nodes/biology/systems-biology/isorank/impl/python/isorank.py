# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isorank/. The authors are listed in prov/35D89N.jsonl.
"""IsoRank: pairwise network alignment by a PageRank-like fixed point.

A graph is a list of neighbor lists: adj[u] is the list of neighbors of node
u, nodes are 0 .. n-1, and every edge appears in both lists. E is an n x m
matrix of non-negative sequence similarity scores for the n nodes of the first
graph and the m nodes of the second.

The score matrix R solves R = alpha A R + (1 - alpha) E, where
A[(i, j), (u, v)] = 1 / (|N(u)| |N(v)|) when u is a neighbor of i and v is a
neighbor of j, and 0 otherwise. The code never builds A: one step costs
O(e m + n f) for graphs with e and f edges.

The method of Singh, Xu and Berger (2008) also has a multiple alignment step
and, in its case study, a maximum weight bipartite matching instead of the
greedy one. This file has the pairwise scores, the greedy matching and two
checks: an exact rational solve and a personalized PageRank on the product
graph, both for small graphs only. No random draws are made.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Sequence, Tuple

Matrix = List[List[float]]


def normalize(e: Sequence[Sequence[float]]) -> Matrix:
    """Scale E so that its entries add up to 1 (uniform if E is all zero)."""
    n, m = len(e), len(e[0])
    total = sum(sum(row) for row in e)
    if any(v < 0 for row in e for v in row):
        raise ValueError("sequence scores must be non-negative")
    if total == 0:
        return [[1.0 / (n * m)] * m for _ in range(n)]
    return [[v / total for v in row] for row in e]


def isorank_step(adj1, adj2, r: Matrix, e: Matrix, alpha: float) -> Matrix:
    """One step R' = alpha A R + (1 - alpha) E, in O(e m + n f) time."""
    n, m = len(adj1), len(adj2)
    d1 = [len(a) for a in adj1]
    d2 = [len(a) for a in adj2]
    # s[u][v] = R[u][v] / (d_u d_v); a pair with an isolated node sends nothing
    s = [[r[u][v] / (d1[u] * d2[v]) if d1[u] and d2[v] else 0.0 for v in range(m)] for u in range(n)]
    # p[i][v] = sum of s[u][v] over the neighbors u of i
    p = [[0.0] * m for _ in range(n)]
    for i in range(n):
        row = p[i]
        for u in adj1[i]:
            su = s[u]
            for v in range(m):
                row[v] += su[v]
    out = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            acc = 0.0
            for v in adj2[j]:
                acc += p[i][v]
            out[i][j] = alpha * acc + (1.0 - alpha) * e[i][j]  # @line L4
    return out


def isorank_scores(adj1, adj2, e, alpha: float = 0.6, tol: float = 1e-12, max_iter: int = 1000) -> Tuple[Matrix, int]:
    """Iterate from R = E until the 1-norm change is at most tol. Returns (R, steps)."""
    if not 0.0 <= alpha < 1.0:
        raise ValueError("alpha must be in [0, 1)")
    en = normalize(e)  # @line L1
    r = [row[:] for row in en]  # @line L2
    for step in range(1, max_iter + 1):  # @line L3
        nxt = isorank_step(adj1, adj2, r, en, alpha)
        delta = sum(abs(a - b) for ra, rb in zip(nxt, r) for a, b in zip(ra, rb))  # @line L5
        r = nxt
        if delta <= tol:  # @line L6
            return r, step
    return r, max_iter


def greedy_matching(r: Sequence[Sequence[float]]) -> List[Tuple[int, int]]:
    """Take pairs by decreasing score, skipping pairs with a used node. Ties go to the smaller (i, j)."""
    n, m = len(r), len(r[0])
    pairs = sorted(((i, j) for i in range(n) for j in range(m)), key=lambda q: (-r[q[0]][q[1]], q))
    used1, used2 = set(), set()
    out = []
    for i, j in pairs:  # @line L7
        if i not in used1 and j not in used2:
            out.append((i, j))
            used1.add(i)
            used2.add(j)
    return out


def isorank(adj1, adj2, e, alpha: float = 0.6, tol: float = 1e-12):
    """Lines L1 to L8: scores, then the greedy one-to-one alignment."""
    r, _ = isorank_scores(adj1, adj2, e, alpha, tol)
    return greedy_matching(r), r  # @line L8


def exact_scores(adj1, adj2, e, alpha) -> List[List[Fraction]]:
    """Solve (I - alpha A) R = (1 - alpha) E exactly in rationals (small graphs only)."""
    alpha = Fraction(alpha)
    n, m = len(adj1), len(adj2)
    total = sum(Fraction(v) for row in e for v in row)
    en = [[Fraction(v) / total for v in row] for row in e]
    size = n * m
    idx = lambda i, j: i * m + j
    mat = [[Fraction(0)] * (size + 1) for _ in range(size)]
    for i in range(n):
        for j in range(m):
            row = mat[idx(i, j)]
            row[idx(i, j)] += 1
            for u in adj1[i]:
                for v in adj2[j]:
                    row[idx(u, v)] -= alpha / (len(adj1[u]) * len(adj2[v]))
            row[size] = (1 - alpha) * en[i][j]
    for c in range(size):
        piv = next(k for k in range(c, size) if mat[k][c] != 0)
        mat[c], mat[piv] = mat[piv], mat[c]
        pv = mat[c][c]
        mat[c] = [v / pv for v in mat[c]]
        for k in range(size):
            if k != c and mat[k][c] != 0:
                f = mat[k][c]
                mat[k] = [a - f * b for a, b in zip(mat[k], mat[c])]
    return [[mat[idx(i, j)][size] for j in range(m)] for i in range(n)]


def product_graph(adj1, adj2):
    """Tensor product graph: (i, j) ~ (u, v) when i ~ u and j ~ v. Node (i, j) is i * m + j."""
    m = len(adj2)
    return [[u * m + v for u in adj1[i] for v in adj2[j]] for i in range(len(adj1)) for j in range(m)]


def personalized_pagerank(adj, teleport: Sequence[float], alpha: float, iters: int) -> List[float]:
    """Generic personalized PageRank x = alpha P x + (1 - alpha) t, with P the random walk on adj."""
    x = list(teleport)
    for _ in range(iters):
        nxt = [(1.0 - alpha) * t for t in teleport]
        for w, nbrs in enumerate(adj):
            if nbrs:
                share = alpha * x[w] / len(nbrs)
                for z in nbrs:
                    nxt[z] += share
        x = nxt
    return x
