# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-matrix/. The authors are listed in prov/QTKKXV.jsonl.

from fractions import Fraction
from typing import Sequence


class Laplacian:
    """The Laplacian L = D - W of an undirected weighted graph on 0..n-1.

    Stored sparsely: deg[u] is the weighted degree D[u][u], and adj[u] is a
    list of (v, w) pairs, one for each edge {u, v} of weight w. Parallel edges
    are allowed; their weights add up in L. Self-loops are rejected, because
    they do not change D - W.
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.deg: list[float] = [0] * n
        self.adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, w: float = 1) -> None:
        if u == v:
            raise ValueError("a self-loop does not change the Laplacian")
        if w <= 0:
            raise ValueError("weights must be positive")
        self.deg[u] += w  # @line L1
        self.deg[v] += w
        self.adj[u].append((v, w))  # @line L2
        self.adj[v].append((u, w))  # @line L3

    def multiply(self, x: Sequence[float]) -> list[float]:
        """Return y = L x in Theta(n + m) time."""
        y = [0] * self.n
        for u in range(self.n):  # @line L4
            y[u] = self.deg[u] * x[u]  # @line L5
            for v, w in self.adj[u]:  # @line L6
                y[u] -= w * x[v]  # @line L7
        return y  # @line L8

    def quadratic_form(self, x: Sequence[float]) -> float:
        """Return x^T L x, the sum of w (x_u - x_v)^2 over the edges."""
        s = 0  # @line L9
        for u in range(self.n):  # @line L10
            for v, w in self.adj[u]:  # @line L11
                if u < v:
                    s += w * (x[u] - x[v]) ** 2  # @line L12
        return s  # @line L13

    def entry(self, u: int, v: int) -> float:
        """L[u][v] in O(1 + d(u)) time."""
        if u == v:
            return self.deg[u]
        return -sum(w for t, w in self.adj[u] if t == v)

    def dense(self) -> list[list[float]]:
        a = [[0] * self.n for _ in range(self.n)]
        for u in range(self.n):
            a[u][u] = self.deg[u]
            for v, w in self.adj[u]:
                a[u][v] -= w
        return a


def _eliminate(a: list[list[Fraction]]) -> tuple[int, Fraction]:
    """Gaussian elimination over the rationals; return (rank, determinant)."""
    a = [row[:] for row in a]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank, det = 0, Fraction(1)
    for c in range(cols):
        piv = next((r for r in range(rank, rows) if a[r][c] != 0), None)
        if piv is None:
            det = Fraction(0)
            continue
        if piv != rank:
            a[rank], a[piv] = a[piv], a[rank]
            det = -det
        det *= a[rank][c]
        for r in range(rank + 1, rows):
            f = a[r][c] / a[rank][c]
            if f:
                for k in range(c, cols):
                    a[r][k] -= f * a[rank][k]
        rank += 1
    return rank, det


def components(lap: Laplacian) -> int:
    """The number of connected components, n - rank(L)."""
    if lap.n == 0:
        return 0
    m = [[Fraction(x) for x in row] for row in lap.dense()]
    return lap.n - _eliminate(m)[0]


def spanning_tree_count(lap: Laplacian) -> Fraction:
    """Matrix-tree theorem: the determinant of L with row and column 0 removed.
    For weights this is the sum over spanning trees of the product of weights."""
    if lap.n <= 1:
        return Fraction(1)
    m = [[Fraction(x) for x in row[1:]] for row in lap.dense()[1:]]
    return _eliminate(m)[1]
