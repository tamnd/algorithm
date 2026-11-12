# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smacof/. The authors are listed in prov/8BX53A.jsonl.

"""SMACOF for metric MDS with unit weights: the Guttman transform X+ = (1/n) B(X) X.

delta is a symmetric n x n matrix of dissimilarities, a configuration is a list of n
tuples. Each step never increases the raw stress, by the majorization argument.
"""

import math


def raw_stress(x, delta):
    n = len(x)
    return sum((math.dist(x[i], x[j]) - delta[i][j]) ** 2 for i in range(n) for j in range(i + 1, n))


def b_matrix(x, delta):
    n = len(x)
    b = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dij = math.dist(x[i], x[j])  # @line L3
                b[i][j] = -delta[i][j] / dij if dij > 0 else 0.0  # @line L4
        b[i][i] = -sum(b[i][j] for j in range(n) if j != i)  # @line L5
    return b


def guttman_transform(x, delta):
    n, k = len(x), len(x[0])
    b = b_matrix(x, delta)
    return [tuple(sum(b[i][j] * x[j][a] for j in range(n)) / n for a in range(k)) for i in range(n)]  # @line L6


def center(x):
    n, k = len(x), len(x[0])
    m = [sum(p[a] for p in x) / n for a in range(k)]
    return [tuple(p[a] - m[a] for a in range(k)) for p in x]


def smacof(delta, x0, eps=1e-12, max_iter=1000):
    """Return (x, history) with history[t] the raw stress after t Guttman transforms."""
    x = center([tuple(map(float, p)) for p in x0])
    s = raw_stress(x, delta)  # @line L1
    history = [s]
    for _ in range(max_iter):  # @line L2
        x = guttman_transform(x, delta)
        s_new = raw_stress(x, delta)  # @line L7
        history.append(s_new)
        if s - s_new < eps:  # @line L8
            break
        s = s_new  # @line L9
    return x, history  # @line L10


def majorizer(x, z, delta):
    """tau(X, Z) = sum delta^2 + tr X'VX - 2 tr X'B(Z)Z, an upper bound of the stress at X."""
    n, k = len(x), len(x[0])
    eta_delta = sum(delta[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
    eta_x = sum(math.dist(x[i], x[j]) ** 2 for i in range(n) for j in range(i + 1, n))
    b = b_matrix(z, delta)
    bz = [[sum(b[i][j] * z[j][a] for j in range(n)) for a in range(k)] for i in range(n)]
    rho = sum(x[i][a] * bz[i][a] for i in range(n) for a in range(k))
    return eta_delta + eta_x - 2 * rho
