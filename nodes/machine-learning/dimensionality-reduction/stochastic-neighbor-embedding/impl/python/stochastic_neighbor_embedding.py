# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-neighbor-embedding/. The authors are listed in prov/WVHAJS.jsonl.

"""Stochastic neighbor embedding (Hinton and Roweis 2002), the exact O(n^2) form.

In the input space, p_{j|i} is a Gaussian kernel around x_i with its own
precision beta_i = 1 / (2 sigma_i^2), found by bisection so that the
perplexity 2^H(P_i) of row i equals a target. In the map, q_{j|i} uses a
Gaussian kernel with the fixed precision 1. The cost is the sum over i of
KL(P_i || Q_i), and the map is fitted by gradient descent with momentum and
optional Gaussian jitter that shrinks over time.
"""

import math


def squared_distances(points):
    n = len(points)
    return [[sum((a - b) ** 2 for a, b in zip(points[i], points[j])) for j in range(n)] for i in range(n)]


def conditional_row(dist_row, i, beta):
    """Return (p, entropy in bits) for the row of point i at precision beta."""
    others = [dist_row[j] for j in range(len(dist_row)) if j != i]
    shift = min(others)  # subtracting the smallest distance avoids underflow
    w = [0.0 if j == i else math.exp(-beta * (dist_row[j] - shift)) for j in range(len(dist_row))]
    z = sum(w)
    p = [v / z for v in w]
    h = -sum(v * math.log2(v) for v in p if v > 0.0)
    return p, h


def bandwidth_search(dist_row, i, perplexity, tol=1e-5, max_iter=200):
    """Bisection on beta so that |H(P_i) - log2(perplexity)| <= tol.

    H decreases strictly in beta when the distances from x_i are not all equal,
    so the target is met by one beta when it lies strictly between the number
    of tied nearest neighbors and n - 1. Returns (beta, row of p_{j|i}).
    """
    target = math.log2(perplexity)
    beta, lo, hi = 1.0, 0.0, math.inf  # @line L11
    for _ in range(max_iter):  # @line L12
        p, h = conditional_row(dist_row, i, beta)  # @line L13
        if abs(h - target) <= tol:  # @line L16
            break
        if h > target:  # @line L14
            lo = beta
            beta = beta * 2.0 if hi == math.inf else (beta + hi) / 2.0
        else:  # @line L15
            hi = beta
            beta = (beta + lo) / 2.0
    return beta, p  # @line L17


def input_affinities(points, perplexity, tol=1e-5):
    """Return (P, betas) with P[i][j] = p_{j|i}."""
    d = squared_distances(points)
    rows, betas = [], []
    for i in range(len(points)):  # @line L1
        beta, p = bandwidth_search(d[i], i, perplexity, tol)  # @line L2
        rows.append(p)  # @line L3
        betas.append(beta)
    return rows, betas


def map_affinities(y):
    """Return Q with Q[i][j] = q_{j|i} = exp(-|y_i - y_j|^2) / sum over k != i."""
    d = squared_distances(y)
    q = []
    for i in range(len(y)):
        row, _ = conditional_row(d[i], i, 1.0)
        q.append(row)
    return q


def cost(p, y):
    """C = sum_i KL(P_i || Q_i) in nats."""
    q = map_affinities(y)
    n = len(y)
    return sum(p[i][j] * math.log(p[i][j] / q[i][j]) for i in range(n) for j in range(n) if j != i and p[i][j] > 0.0)


def gradient(p, y):
    """dC/dy_i = 2 sum_j (p_{j|i} - q_{j|i} + p_{i|j} - q_{i|j}) (y_i - y_j)."""
    q = map_affinities(y)  # @line L6
    n, m = len(y), len(y[0])
    g = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            c = 2.0 * (p[i][j] - q[i][j] + p[j][i] - q[j][i])  # @line L7
            for t in range(m):
                g[i][t] += c * (y[i][t] - y[j][t])
    return g


def sne(points, rng, dim=2, perplexity=5.0, iters=300, eta=0.5, momentum=0.8, jitter=0.0):
    """Fit an SNE map. rng is a random.Random; jitter is the initial noise scale."""
    n = len(points)
    p, _ = input_affinities(points, perplexity)
    y = [[rng.gauss(0.0, 1e-2) for _ in range(dim)] for _ in range(n)]  # @line L4
    vel = [[0.0] * dim for _ in range(n)]
    for t in range(iters):  # @line L5
        g = gradient(p, y)
        noise = jitter * (1.0 - t / iters)
        for i in range(n):
            for k in range(dim):
                vel[i][k] = momentum * vel[i][k] - eta * g[i][k]  # @line L8
                y[i][k] += vel[i][k]
                if noise > 0.0:
                    y[i][k] += rng.gauss(0.0, noise)  # @line L9
    return y, p  # @line L10
