# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-feedback-als/. The authors are listed in prov/84ZRE0.jsonl.

"""Weighted matrix factorization for implicit feedback (Hu, Koren and Volinsky 2008).

The input is a dict of counts r_ui > 0 for the observed (user, item) pairs.
Every other pair has r_ui = 0. The preference is p_ui = 1 if r_ui > 0, else 0,
and the confidence is c_ui = 1 + alpha r_ui. The objective sums over ALL m n
pairs:

    J(X, Y) = sum over u, i of c_ui (p_ui - x_u . y_i)^2
              + lam (sum_u |x_u|^2 + sum_i |y_i|^2).

With Y fixed, the best x_u solves (Y^T C^u Y + lam I) x = Y^T C^u p(u). The fast
solve writes Y^T C^u Y = Y^T Y + Y^T (C^u - I) Y. The matrix C^u - I is zero
outside the items of user u, so after one O(n r^2) computation of Y^T Y per
half step, user u costs O(n_u r^2 + r^3), where n_u is its number of items.
"""

import math
import random

Matrix = list[list[float]]
Counts = dict[tuple[int, int], float]


def cholesky_solve(a: Matrix, b: list[float]) -> list[float]:
    """Solve a x = b. Precondition: a is symmetric positive definite. Cost O(r^3)."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = a[j][j] - sum(low[j][k] ** 2 for k in range(j))
        if s <= 0.0:
            raise ValueError("matrix is not positive definite")
        low[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            t = a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            low[i][j] = t / low[j][j]
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def gram(y: Matrix, r: int) -> Matrix:
    """Y^T Y for the rows y_i of Y. Cost O(n r^2)."""
    g = [[0.0] * r for _ in range(r)]
    for v in y:
        for s in range(r):
            for t in range(r):
                g[s][t] += v[s] * v[t]
    return g


def fast_system(rows: dict[int, float], y: Matrix, g: Matrix, lam: float, alpha: float) -> tuple[Matrix, list[float]]:
    """The system (A, b) of one row from Y^T Y and the observed entries only.

    rows maps the index on the other side to the count r_ui > 0. Cost O(n_u r^2).
    """
    r = len(g)
    a = [[g[s][t] for t in range(r)] for s in range(r)]
    for s in range(r):
        a[s][s] += lam
    b = [0.0] * r
    for j, count in rows.items():
        c = 1.0 + alpha * count
        v = y[j]
        for s in range(r):
            b[s] += c * v[s]  # @line L10
            for t in range(r):
                a[s][t] += (c - 1.0) * v[s] * v[t]  # @line L9
    return a, b


def direct_system(rows: dict[int, float], y: Matrix, lam: float, alpha: float) -> tuple[Matrix, list[float]]:
    """The system (Y^T C^u Y + lam I, Y^T C^u p(u)) summed over all n entries. Cost O(n r^2)."""
    r = len(y[0])
    a = [[0.0] * r for _ in range(r)]
    b = [0.0] * r
    for j, v in enumerate(y):
        count = rows.get(j, 0.0)
        c = 1.0 + alpha * count
        p = 1.0 if count > 0 else 0.0
        for s in range(r):
            b[s] += c * p * v[s]
            for t in range(r):
                a[s][t] += c * v[s] * v[t]
    for s in range(r):
        a[s][s] += lam
    return a, b


def half_step(groups: dict[int, dict[int, float]], count: int, y: Matrix, lam: float, alpha: float) -> Matrix:
    """Solve the weighted ridge problem of each of count rows with the other side y fixed."""
    r = len(y[0])
    g = gram(y, r)  # @line L7
    out = []
    for k in range(count):  # @line L8
        a, b = fast_system(groups.get(k, {}), y, g, lam, alpha)
        out.append(cholesky_solve(a, b))  # @line L11
    return out  # @line L12


def objective(counts: Counts, x: Matrix, y: Matrix, lam: float, alpha: float) -> float:
    """J(X, Y) summed over all m n pairs. Cost O(m n r); for tests and small data."""
    total = 0.0
    for u, xu in enumerate(x):
        for i, yi in enumerate(y):
            count = counts.get((u, i), 0.0)
            c = 1.0 + alpha * count
            p = 1.0 if count > 0 else 0.0
            e = p - sum(a * b for a, b in zip(xu, yi))
            total += c * e * e
    total += lam * sum(a * a for row in x for a in row)
    total += lam * sum(a * a for row in y for a in row)
    return total


def group(counts: Counts) -> tuple[dict[int, dict[int, float]], dict[int, dict[int, float]]]:
    """(by_user, by_item): user -> {item: count} and item -> {user: count}."""
    bu: dict[int, dict[int, float]] = {}
    bi: dict[int, dict[int, float]] = {}
    for (u, i), v in counts.items():
        if v <= 0:
            raise ValueError("counts must be positive; leave unobserved pairs out")
        bu.setdefault(u, {})[i] = v
        bi.setdefault(i, {})[u] = v
    return bu, bi


def implicit_als(
    counts: Counts,
    m: int,
    n: int,
    r: int,
    lam: float,
    alpha: float,
    sweeps: int,
    seed: int = 1,
    y0: Matrix | None = None,
    track: bool = False,
) -> tuple[Matrix, Matrix, list[float]]:
    """Run sweeps of (user half step, item half step).

    Precondition: lam > 0, alpha >= 0, counts positive. Cost per sweep
    O(s r^2 + (m + n) r^3) for s observed pairs. Returns (X, Y, history);
    with track=True, history holds J at the start and after each half step,
    which costs O(m n r) each time.
    """
    if lam <= 0.0 or alpha < 0.0:
        raise ValueError("need lam > 0 and alpha >= 0")
    bu, bi = group(counts)  # @line L1
    rng = random.Random(seed)
    if y0 is None:
        y = [[rng.gauss(0.0, 0.1) for _ in range(r)] for _ in range(n)]  # @line L2
    else:
        y = [row[:] for row in y0]
    x = [[0.0] * r for _ in range(m)]
    history = [objective(counts, x, y, lam, alpha)] if track else []
    for _ in range(sweeps):  # @line L3
        x = half_step(bu, m, y, lam, alpha)  # @line L4
        if track:
            history.append(objective(counts, x, y, lam, alpha))
        y = half_step(bi, n, x, lam, alpha)  # @line L5
        if track:
            history.append(objective(counts, x, y, lam, alpha))
    return x, y, history  # @line L6


def recommend(rows: dict[int, float], xu: list[float], y: Matrix, k: int) -> list[int]:
    """The k items with the highest x_u . y_i among the items the user has not used. Cost O(n r + n log n)."""
    scored = [(-sum(a * b for a, b in zip(xu, yi)), i) for i, yi in enumerate(y) if i not in rows]
    scored.sort()
    return [i for _, i in scored[:k]]
