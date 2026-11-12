# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vanishing-gradient-problem/. The authors are listed in prov/M6EW97.jsonl.
"""Measure how a backpropagated gradient shrinks through a product of Jacobians.

sigmoid_chain_derivative: the derivative dh_n/dh_0 of the scalar chain
h_i = sigmoid(w h_(i-1) + c), a product of n factors w * sigmoid'(.), each at
most |w| / 4 in absolute value.

log_norm_rate: push a vector back through n random m x m Jacobians with
independent N(0, s^2 / m) entries and return the mean of log(||v_i|| / ||v_(i-1)||).
predicted_rate gives its expected value
    lambda = log s + (psi(m / 2) - log(m / 2)) / 2,
since ||J v||^2 / ||v||^2 is (s^2 / m) times a chi-square variable with m
degrees of freedom, and E[log chi2_m] = psi(m / 2) + log 2.
"""

import math
import random

EULER_GAMMA = 0.5772156649015329


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_chain_derivative(w: float, c: float, n: int, h0: float) -> float:
    h, d = h0, 1.0
    for _ in range(n):
        s = sigmoid(w * h + c)
        d *= w * s * (1.0 - s)  # the factor dh_i / dh_(i-1)
        h = s
    return d


def digamma_half(m: int) -> float:
    """psi(m / 2) for a positive integer m, from the exact series."""
    if m % 2 == 0:
        k = m // 2
        return -EULER_GAMMA + sum(1.0 / j for j in range(1, k))
    k = (m - 1) // 2  # psi(k + 1/2)
    return -EULER_GAMMA - 2.0 * math.log(2.0) + sum(2.0 / (2 * j - 1) for j in range(1, k + 1))


def predicted_rate(m: int, s: float) -> float:
    return math.log(s) + 0.5 * (digamma_half(m) - math.log(m / 2.0))


def log_norm_rate(m: int, n: int, s: float, rng: random.Random) -> float:
    """Mean log growth per factor of ||J_n ... J_1 v|| for random Gaussian J_i."""
    v = [rng.gauss(0.0, 1.0) for _ in range(m)]
    norm = math.sqrt(sum(x * x for x in v))
    v = [x / norm for x in v]
    total = 0.0
    sd = s / math.sqrt(m)
    for _ in range(n):
        J = [[rng.gauss(0.0, sd) for _ in range(m)] for _ in range(m)]
        v = [sum(a * x for a, x in zip(row, v)) for row in J]
        norm = math.sqrt(sum(x * x for x in v))
        total += math.log(norm)
        v = [x / norm for x in v]  # renormalize to avoid underflow
    return total / n


def critical_scale(m: int) -> float:
    """The scale s at which the predicted rate is 0."""
    return math.exp(-0.5 * (digamma_half(m) - math.log(m / 2.0)))
