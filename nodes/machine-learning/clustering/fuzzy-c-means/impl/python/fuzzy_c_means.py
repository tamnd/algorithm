# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fuzzy-c-means/. The authors are listed in prov/YQJKEX.jsonl.

"""Fuzzy c-means (Dunn 1973, Bezdek 1981): alternate the exact
minimization of J_m(U, V) = sum_i sum_j u_ij^m ||x_i - v_j||^2 over the
memberships U (rows on the probability simplex) and over the centers V.

The code works with floats or with Fractions; with Fractions and m = 2
every step is exact, because the exponent 1 / (m - 1) is then 1.
"""


def sqdist(p, q):
    return sum((a - b) ** 2 for a, b in zip(p, q))


def objective(points, U, V, m):
    return sum(U[i][j] ** m * sqdist(points[i], V[j]) for i in range(len(points)) for j in range(len(V)))


def memberships(points, V, m):
    """The membership step: the minimizer of J_m over U for fixed V."""
    c = len(V)
    U = []
    for x in points:
        D = [sqdist(x, v) for v in V]  # @line L4
        zero = [j for j in range(c) if D[j] == 0]
        if zero:  # @line L5
            row = [0] * c
            for j in zero:
                row[j] = type(D[0])(1) / len(zero)
            U.append(row)
            continue
        if m == 2:
            row = [1 / sum(D[j] / D[l] for l in range(c)) for j in range(c)]  # @line L6
        else:
            e = 1.0 / (m - 1)
            row = [1 / sum((D[j] / D[l]) ** e for l in range(c)) for j in range(c)]
        U.append(row)
    return U


def centers(points, U, m, old):
    """The center step: v_j = sum_i u_ij^m x_i / sum_i u_ij^m."""
    d = len(points[0])
    V = []
    for j in range(len(old)):
        w = [U[i][j] ** m for i in range(len(points))]
        s = sum(w)
        if s == 0:
            V.append(list(old[j]))
        else:
            V.append([sum(w[i] * points[i][t] for i in range(len(points))) / s for t in range(d)])  # @line L7
    return V


def fuzzy_c_means(points, c, m=2, rng=None, init=None, eps=1e-9, max_iter=300, trace=None):
    """Return (U, V). init: initial centers; if None, c distinct points
    chosen with rng (a random.Random). trace, if a list, receives the
    objective after each half step."""
    if m <= 1:
        raise ValueError("the fuzzifier m must be greater than 1")
    if init is None:
        init = [points[i] for i in rng.sample(range(len(points)), c)]  # @line L1
    V = [list(v) for v in init]
    U = None
    for _ in range(max_iter):  # @line L2
        newU = memberships(points, V, m)  # @line L3
        if trace is not None:
            trace.append(objective(points, newU, V, m))
        V = centers(points, newU, m, V)
        if trace is not None:
            trace.append(objective(points, newU, V, m))
        change = None if U is None else max(abs(a - b) for r, s in zip(U, newU) for a, b in zip(r, s))
        U = newU
        if change is not None and change <= eps:  # @line L8
            break
    return U, V  # @line L9
