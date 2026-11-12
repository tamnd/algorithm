# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-sne/. The authors are listed in prov/5T99ZY.jsonl.

"""Exact t-SNE (van der Maaten and Hinton 2008), O(n^2) work per step.

Input affinities: the SNE conditionals p_{j|i} with a bandwidth per point
found by bisection for a target perplexity, then p_ij = (p_{j|i} + p_{i|j}) / 2n.
Map affinities: q_ij proportional to (1 + |y_i - y_j|^2)^(-1) over all pairs.
Cost: KL(P || Q). Gradient: 4 sum_j (p_ij - q_ij)(y_i - y_j)(1 + |y_i - y_j|^2)^(-1).
Optimizer: gradient descent with momentum 0.5 then 0.8, early exaggeration of P,
and the adaptive gains of Jacobs (1988), as in Section 3.4 of the paper.
"""

import math


def squared_distances(points):
    n = len(points)
    return [[sum((a - b) ** 2 for a, b in zip(points[i], points[j])) for j in range(n)] for i in range(n)]


def _row(dist_row, i, beta):
    shift = min(dist_row[j] for j in range(len(dist_row)) if j != i)
    w = [0.0 if j == i else math.exp(-beta * (dist_row[j] - shift)) for j in range(len(dist_row))]
    z = sum(w)
    p = [v / z for v in w]
    return p, -sum(v * math.log2(v) for v in p if v > 0.0)


def conditional_row(dist_row, i, perplexity, tol=1e-5, max_iter=200):
    """Bisection on beta = 1 / (2 sigma_i^2) for perplexity 2^H(P_i). Returns the row p_{.|i}."""
    target = math.log2(perplexity)
    beta, lo, hi = 1.0, 0.0, math.inf
    for _ in range(max_iter):
        p, h = _row(dist_row, i, beta)
        if abs(h - target) <= tol:
            break
        if h > target:
            lo = beta
            beta = beta * 2.0 if hi == math.inf else (beta + hi) / 2.0
        else:
            hi = beta
            beta = (beta + lo) / 2.0
    return p


def joint_affinities(points, perplexity):
    """Symmetric P with p_ij = (p_{j|i} + p_{i|j}) / 2n; the entries sum to 1."""
    n = len(points)
    d = squared_distances(points)
    cond = [conditional_row(d[i], i, perplexity) for i in range(n)]  # @line L1
    return [[(cond[i][j] + cond[j][i]) / (2.0 * n) for j in range(n)] for i in range(n)]  # @line L2


def student_q(y):
    """Return (Q, W) with W[i][j] = (1 + |y_i - y_j|^2)^(-1) and Q = W / sum W (zero diagonal)."""
    n = len(y)
    d = squared_distances(y)
    w = [[0.0 if i == j else 1.0 / (1.0 + d[i][j]) for j in range(n)] for i in range(n)]
    z = sum(map(sum, w))
    return [[v / z for v in row] for row in w], w


def kl(p, y):
    """KL(P || Q) in nats."""
    q, _ = student_q(y)
    n = len(y)
    return sum(p[i][j] * math.log(p[i][j] / q[i][j]) for i in range(n) for j in range(n) if p[i][j] > 0.0)


def gradient(p, y, exaggeration=1.0):
    """4 sum_j (e p_ij - q_ij)(y_i - y_j) w_ij; for e = 1 this is the gradient of KL(P || Q)."""
    q, w = student_q(y)  # @line L6
    n, m = len(y), len(y[0])
    g = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                c = 4.0 * (exaggeration * p[i][j] - q[i][j]) * w[i][j]  # @line L7
                for t in range(m):
                    g[i][t] += c * (y[i][t] - y[j][t])
    return g


def tsne(points, rng, dim=2, perplexity=5.0, iters=500, eta=100.0, exaggeration=4.0, exag_iters=50, switch=250):
    """Fit a t-SNE map; rng is a random.Random. Returns (Y, P)."""
    n = len(points)
    p = joint_affinities(points, perplexity)
    y = [[rng.gauss(0.0, 1e-2) for _ in range(dim)] for _ in range(n)]  # @line L3
    vel = [[0.0] * dim for _ in range(n)]
    gain = [[1.0] * dim for _ in range(n)]
    for t in range(iters):  # @line L4
        e = exaggeration if t < exag_iters else 1.0  # @line L5
        g = gradient(p, y, e)
        alpha = 0.5 if t < switch else 0.8  # @line L8
        for i in range(n):
            for k in range(dim):
                # Jacobs gains: grow when the step keeps changing sign, shrink when it does not
                if (g[i][k] > 0.0) != (vel[i][k] > 0.0):  # @line L9
                    gain[i][k] += 0.2
                else:
                    gain[i][k] = max(gain[i][k] * 0.8, 0.01)
                vel[i][k] = alpha * vel[i][k] - eta * gain[i][k] * g[i][k]  # @line L10
                y[i][k] += vel[i][k]
    return y, p  # @line L11
