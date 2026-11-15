# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranking-svm/. The authors are listed in prov/VTCXN6.jsonl.

"""Ranking SVM: a linear scorer from pairwise preferences.

For every query and every pair of its documents with y_i > y_j, let
z = x_i - x_j. With P such pairs, the objective is

    J(w) = (lambda / 2) ||w||^2 + (1 / P) sum over pairs of max(0, 1 - w . z).

The solver is the projected subgradient method with the step 1 / (lambda t)
and the projection onto the ball of radius sqrt(2 / lambda), which holds
the minimizer because J(w*) <= J(0) = 1. It returns the best iterate. A
dual coordinate ascent gives a lower bound D(alpha) <= J(w*) for tests.
"""

import math


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def pairs(queries):
    """The difference vectors x_i - x_j for y_i > y_j inside each query."""
    out = []
    for xs, y in queries:
        for i in range(len(xs)):
            for j in range(len(xs)):
                if y[i] > y[j]:
                    out.append([a - b for a, b in zip(xs[i], xs[j])])
    return out


def objective(w, zs, lam):
    return lam / 2 * dot(w, w) + sum(max(0.0, 1.0 - dot(w, z)) for z in zs) / len(zs)


def subgradient(w, zs, lam):
    """lambda w - (1 / P) sum of z over the pairs with w . z < 1."""
    g = [lam * a for a in w]
    for z in zs:
        if dot(w, z) < 1.0:
            for c in range(len(w)):
                g[c] -= z[c] / len(zs)
    return g


def radius(lam):
    return math.sqrt(2.0 / lam)


def train(queries, lam, steps):
    """Projected subgradient method. Returns the best w and the best J after each step."""
    zs = pairs(queries)                                          # @line L1
    d = len(zs[0])
    w = [0.0] * d                                                # @line L2
    best, best_j = list(w), objective(w, zs, lam)
    r = radius(lam)
    history = [best_j]
    for t in range(1, steps + 1):                                # @line L3
        g = subgradient(w, zs, lam)                              # @line L4
        w = [a - b / (lam * t) for a, b in zip(w, g)]            # @line L5
        n = norm(w)
        if n > r:                                                # @line L6
            w = [a * r / n for a in w]
        j = objective(w, zs, lam)
        if j < best_j:                                           # @line L7
            best, best_j = list(w), j
        history.append(best_j)
    return best, history                                         # @line L8


def bound(zs, lam, steps):
    """G^2 (1 + ln T) / (2 lambda T), with G = lambda R + max ||z||."""
    g = lam * radius(lam) + max(norm(z) for z in zs)
    return g * g * (1.0 + math.log(steps)) / (2.0 * lam * steps)


def dual(alpha, zs, lam):
    p = len(zs)
    v = [0.0] * len(zs[0])
    for a, z in zip(alpha, zs):
        for c in range(len(v)):
            v[c] += a * z[c]
    return sum(alpha) / p - dot(v, v) / (2.0 * lam * p * p)


def dual_coordinate_ascent(zs, lam, sweeps):
    """Exact maximization of D over one alpha_k at a time, alpha_k in [0, 1].

    Returns alpha and w = (1 / (lambda P)) sum alpha_k z_k.
    """
    p = len(zs)
    alpha = [0.0] * p
    v = [0.0] * len(zs[0])
    for _ in range(sweeps):
        for k, z in enumerate(zs):
            zz = dot(z, z)
            if zz == 0:
                continue
            new = min(1.0, max(0.0, alpha[k] + (lam * p - dot(z, v)) / zz))
            delta = new - alpha[k]
            if delta != 0.0:
                alpha[k] = new
                for c in range(len(v)):
                    v[c] += delta * z[c]
    return alpha, [a / (lam * p) for a in v]


def ranking(s):
    return sorted(range(len(s)), key=lambda i: (-s[i], i))


def misordered_pairs(w, queries):
    """The number of pairs with y_i > y_j and w . x_i <= w . x_j."""
    return sum(1 for z in pairs(queries) if dot(w, z) <= 0)
