# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-linear-method/. The authors are listed in prov/XKTFZV.jsonl.

"""SLIM, the sparse linear method for top-N recommendation (Ning and Karypis 2011).

A is the m x n user-item matrix (0/1 or counts). SLIM learns an n x n matrix W
with W >= 0 and diag(W) = 0 that minimizes

    1/2 |A - A W|_F^2 + beta/2 |W|_F^2 + lam |W|_1.

The problem splits into one elastic net per column j,

    min over w >= 0 with w_j = 0 of  1/2 |a_j - A w|^2 + beta/2 |w|^2 + lam sum_k w_k,

solved here by cyclic coordinate descent. The coordinate step for w_k is the
exact minimizer over w_k >= 0 with the other coordinates fixed:

    w_k = max(0, a_k . e + |a_k|^2 w_k - lam) / (|a_k|^2 + beta),

where e = a_j - A w is the current residual. The score of item i for user u
is a_u . w_i, the i-th entry of a_u^T W.
"""

Matrix = list[list[float]]


def column(a: Matrix, k: int) -> list[float]:
    return [row[k] for row in a]


def dot(x: list[float], y: list[float]) -> float:
    return sum(p * q for p, q in zip(x, y))


def column_objective(a: Matrix, j: int, w: list[float], beta: float, lam: float) -> float:
    """1/2 |a_j - A w|^2 + beta/2 |w|^2 + lam |w|_1. Cost O(m n)."""
    m, n = len(a), len(a[0])
    total = 0.0
    for u in range(m):
        e = a[u][j] - sum(a[u][k] * w[k] for k in range(n))
        total += 0.5 * e * e
    return total + 0.5 * beta * dot(w, w) + lam * sum(abs(v) for v in w)


def slim_column(
    a: Matrix, j: int, beta: float, lam: float, tol: float = 1e-12, max_sweeps: int = 10000
) -> list[float]:
    """Solve the elastic net of column j by cyclic coordinate descent.

    Precondition: beta > 0 and lam >= 0. Stops when no coordinate moves by
    more than tol in a sweep. Cost O(m n) per sweep with dense columns.
    """
    if beta <= 0.0 or lam < 0.0:
        raise ValueError("need beta > 0 and lam >= 0")
    m, n = len(a), len(a[0])
    cols = [column(a, k) for k in range(n)]
    norms = [dot(c, c) for c in cols]
    w = [0.0] * n  # @line L2
    e = cols[j][:]
    for _ in range(max_sweeps):  # @line L3
        moved = 0.0
        for k in range(n):  # @line L4
            if k == j or norms[k] == 0.0:
                continue
            rho = dot(cols[k], e) + norms[k] * w[k]  # @line L5
            new = max(0.0, rho - lam) / (norms[k] + beta)  # @line L6
            d = new - w[k]
            if d != 0.0:
                for u in range(m):  # @line L7
                    e[u] -= cols[k][u] * d
                w[k] = new
                moved = max(moved, abs(d))
        if moved <= tol:
            break
    return w  # @line L8


def slim(a: Matrix, beta: float, lam: float, tol: float = 1e-12) -> Matrix:
    """The n x n matrix W, one column per item. Cost O(T m n^2) for T sweeps per column."""
    n = len(a[0])
    cols = [slim_column(a, j, beta, lam, tol) for j in range(n)]  # @line L1
    return [[cols[j][k] for j in range(n)] for k in range(n)]  # @line L9


def scores(a: Matrix, w: Matrix, u: int) -> list[float]:
    """The row a_u^T W. Cost O(n^2)."""
    n = len(w)
    return [sum(a[u][k] * w[k][i] for k in range(n)) for i in range(n)]


def recommend(a: Matrix, w: Matrix, u: int, k: int) -> list[int]:
    """The k items with the highest score that user u has not used. Cost O(n^2)."""
    s = scores(a, w, u)  # @line L10
    cand = sorted((-s[i], i) for i in range(len(s)) if a[u][i] == 0)
    return [i for _, i in cand[:k]]


def kkt_violation(a: Matrix, j: int, w: list[float], beta: float, lam: float) -> float:
    """The largest violation of the KKT conditions of column j.

    With g_k = -a_k . (a_j - A w) + beta w_k, the conditions are, for k != j:
    g_k + lam = 0 if w_k > 0, and g_k + lam >= 0 if w_k = 0; also w >= 0 and
    w_j = 0. Cost O(m n).
    """
    m, n = len(a), len(a[0])
    e = [a[u][j] - sum(a[u][k] * w[k] for k in range(n)) for u in range(m)]
    worst = abs(w[j])
    for k in range(n):
        if k == j:
            continue
        worst = max(worst, -w[k])
        g = -sum(a[u][k] * e[u] for u in range(m)) + beta * w[k]
        if w[k] > 0.0:
            worst = max(worst, abs(g + lam))
        else:
            worst = max(worst, -(g + lam))
    return worst
