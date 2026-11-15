# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alternating-least-squares/. The authors are listed in prov/S7Y3XE.jsonl.

"""Alternating least squares for the factorization R ~ P Q^T.

The objective is

    J(P, Q) = sum over (u, i) in K of (r_ui - p_u . q_i)^2
              + lam (sum_u c_u |p_u|^2 + sum_i c_i |q_i|^2)

with c_u = c_i = 1 (plain ridge penalty) or, with weighted=True, c_u the
number of ratings of user u and c_i the number of ratings of item i (the
ALS-WR weighting of Zhou et al. 2008). With Q fixed, J splits into one
ridge regression for each user, solved exactly by

    (sum over i in I_u of q_i q_i^T + lam c_u I) p_u = sum over i in I_u of r_ui q_i,

and the same holds for the items with P fixed. A user with no rating
gets p_u = 0.
"""

import math
import random


def cholesky_solve(a, b):
    """Solve a x = b for a symmetric positive definite matrix a."""
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


def normal_equations(rows, fixed, lam, weighted, r):
    """The ridge system (A, b) of one user (or item).

    rows maps the other side's index to the rating; fixed holds the
    fixed factor vectors.
    """
    c = len(rows) if weighted else 1
    a = [[0.0] * r for _ in range(r)]
    b = [0.0] * r
    for j, v in rows.items():
        y = fixed[j]
        for s in range(r):
            b[s] += v * y[s]
            for t in range(r):
                a[s][t] += y[s] * y[t]  # @line L8
    for s in range(r):
        a[s][s] += lam * c
    return a, b


def half_step(groups, count, fixed, lam, weighted, r):
    """Solve the ridge problem of each of count rows with the other side fixed."""
    out = []
    for k in range(count):  # @line L6
        rows = groups.get(k)
        if not rows:  # @line L7
            out.append([0.0] * r)
            continue
        a, b = normal_equations(rows, fixed, lam, weighted, r)
        out.append(cholesky_solve(a, b))  # @line L9
    return out  # @line L10


def objective(train, p, q, lam, weighted=False):
    nu, ni = {}, {}
    for u, i in train:
        nu[u] = nu.get(u, 0) + 1
        ni[i] = ni.get(i, 0) + 1
    total = 0.0
    for (u, i), v in train.items():
        e = v - sum(a * b for a, b in zip(p[u], q[i]))
        total += e * e
    for u, pu in enumerate(p):
        c = nu.get(u, 0) if weighted else 1
        total += lam * c * sum(a * a for a in pu)
    for i, qi in enumerate(q):
        c = ni.get(i, 0) if weighted else 1
        total += lam * c * sum(a * a for a in qi)
    return total


def group(train):
    """(by_user, by_item): user -> {item: r} and item -> {user: r}."""
    bu, bi = {}, {}
    for (u, i), v in train.items():
        bu.setdefault(u, {})[i] = v
        bi.setdefault(i, {})[u] = v
    return bu, bi


def als(train, m, n, r, lam, sweeps, seed=1, weighted=False, q0=None):
    """Run sweeps of (user half step, item half step).

    Returns (P, Q, history), where history holds J at the start and after
    each half step. Q starts from q0 if given, else from small random values.
    """
    if lam <= 0.0:
        raise ValueError("lam must be positive")
    rng = random.Random(seed)
    if q0 is None:
        q = [[rng.gauss(0.0, 0.1) for _ in range(r)] for _ in range(n)]  # @line L1
    else:
        q = [row[:] for row in q0]
    p = [[0.0] * r for _ in range(m)]
    bu, bi = group(train)
    history = [objective(train, p, q, lam, weighted)]
    for _ in range(sweeps):  # @line L2
        p = half_step(bu, m, q, lam, weighted, r)  # @line L3
        history.append(objective(train, p, q, lam, weighted))
        q = half_step(bi, n, p, lam, weighted, r)  # @line L4
        history.append(objective(train, p, q, lam, weighted))
    return p, q, history  # @line L5
