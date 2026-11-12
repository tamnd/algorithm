# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sammon-mapping/. The authors are listed in prov/HP4B32.jsonl.

"""Sammon's nonlinear mapping (1969) with the diagonal pseudo-Newton step.

delta is a symmetric n x n matrix of input distances, all positive off the diagonal.
A configuration is a list of n tuples. All coordinates move at once, from the values
of the previous iteration, as in the paper.
"""

import math


def sammon_stress(y, delta):
    n = len(y)
    c = sum(delta[i][j] for i in range(n) for j in range(i + 1, n))
    e = sum((delta[i][j] - math.dist(y[i], y[j])) ** 2 / delta[i][j] for i in range(n) for j in range(i + 1, n))
    return e / c


def derivatives(y, delta):
    """First and second partial derivatives of the stress, one pair per coordinate."""
    n, k = len(y), len(y[0])
    c = sum(delta[i][j] for i in range(n) for j in range(i + 1, n))
    g = [[0.0] * k for _ in range(n)]
    h = [[0.0] * k for _ in range(n)]
    for p in range(n):
        for j in range(n):
            if j == p:
                continue
            dpj = max(math.dist(y[p], y[j]), 1e-12)  # @line L3
            s = delta[p][j]
            for q in range(k):
                u = y[p][q] - y[j][q]
                g[p][q] += (s - dpj) / (s * dpj) * u  # @line L4
                h[p][q] += ((s - dpj) - u * u / dpj * (1 + (s - dpj) / dpj)) / (s * dpj)  # @line L5
    f = -2.0 / c
    return [[f * v for v in row] for row in g], [[f * v for v in row] for row in h]


def sammon_step(y, delta, magic=0.35):
    g, h = derivatives(y, delta)
    return [tuple(y[p][q] - magic * g[p][q] / max(abs(h[p][q]), 1e-12)  # @line L6
                  for q in range(len(y[p]))) for p in range(len(y))]


def sammon(delta, y0, iters=100, magic=0.35):
    """Return (y, history) with history[t] the stress after t iterations."""
    y = [tuple(map(float, p)) for p in y0]
    hist = [sammon_stress(y, delta)]  # @line L1
    for _ in range(iters):  # @line L2
        y = sammon_step(y, delta, magic)
        hist.append(sammon_stress(y, delta))  # @line L7
    return y, hist  # @line L8
