# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-filter/. The authors are listed in prov/JZ7RY4.jsonl.

"""The histogram filter on a line (Thrun, Burgard and Fox 2005, Section 4.1).

A continuous state x in [a, b) is split into g cells of equal width h.
Cell k is [a + k h, a + (k + 1) h) and its center is c_k = a + (k + 1/2) h.
The belief is a list p of g probabilities, one per cell.

The motion model is x_t = x_(t-1) + u_t + noise, with noise N(0, sigma^2).
The probability to go from cell i to cell k is the mass of N(c_i + u, sigma^2)
on cell k. Mass that leaves [a, b) goes to the first or the last cell, as if
the robot stops at a wall. The measurement model is any density p(z | x),
read at the cell centers.
"""

import math


def _phi(x):
    """Return the standard normal distribution function at x."""
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def centers(a, b, g):
    """Return the g cell centers of [a, b)."""
    h = (b - a) / g
    return [a + (k + 0.5) * h for k in range(g)]


def gaussian_transition(a, b, g, u, sigma):
    """Return T with T[k][i] = P(cell k at time t | cell i at time t - 1, u).

    Each column of T sums to 1. sigma must be positive.
    """
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    h = (b - a) / g
    c = centers(a, b, g)
    t = [[0.0] * g for _ in range(g)]
    for i in range(g):
        m = c[i] + u
        # cdf[k] = P(x < left edge of cell k); the outer edges are -inf and +inf
        cdf = [0.0] + [_phi((a + k * h - m) / sigma) for k in range(1, g)] + [1.0]
        for k in range(g):
            t[k][i] = cdf[k + 1] - cdf[k]
    return t


def histogram_filter(p, trans, likelihood):
    """Return the belief after one motion and one measurement.

    p is the belief over the g cells, trans is a g by g matrix with
    trans[k][i] = P(k | u_t, i), or None for no motion, and likelihood is a
    list with likelihood[k] = p(z_t | x = c_k), or None for no measurement.
    """
    g = len(p)
    if trans is None:
        p_bar = list(p)
    else:
        p_bar = []
        for k in range(g):  # @line L1
            p_bar.append(sum(trans[k][i] * p[i] for i in range(g)))  # @line L2
    if likelihood is None:
        return p_bar
    q = [likelihood[k] * p_bar[k] for k in range(g)]  # @line L3
    total = sum(q)
    if total <= 0:
        raise ValueError("the measurement has probability zero under the predicted belief")
    eta = 1 / total  # @line L4 (stays exact for fractions.Fraction inputs)
    return [eta * x for x in q]  # @line L5


def mean_var(a, b, p):
    """Return the mean and the variance of the belief p on [a, b).

    The mass of each cell is spread uniformly over the cell, so the variance
    includes the term h^2 / 12 of a uniform distribution on one cell.
    """
    g = len(p)
    h = (b - a) / g
    c = centers(a, b, g)
    mean = sum(pk * ck for pk, ck in zip(p, c))
    var = sum(pk * (ck - mean) ** 2 for pk, ck in zip(p, c)) + h * h / 12.0
    return mean, var


def gaussian_prior(a, b, g, mu, sigma):
    """Return the mass of N(mu, sigma^2) on each cell, with the tails in the end cells."""
    h = (b - a) / g
    cdf = [0.0] + [_phi((a + k * h - mu) / sigma) for k in range(1, g)] + [1.0]
    return [cdf[k + 1] - cdf[k] for k in range(g)]
