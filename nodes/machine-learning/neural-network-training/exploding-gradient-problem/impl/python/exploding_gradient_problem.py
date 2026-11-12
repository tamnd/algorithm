# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exploding-gradient-problem/. The authors are listed in prov/7ABN4Y.jsonl.
"""Measure how a backpropagated gradient grows through a product of Jacobians.

log_norm_rate: the mean log growth per factor of ||J_n ... J_1 v|| for random
m x m Jacobians with N(0, s^2 / m) entries; predicted_rate gives its exact
expected value log s + (psi(m / 2) - log(m / 2)) / 2.

power_rate: the mean log growth per step of ||W^n v|| for one fixed matrix W,
the case of a linear recurrent network. It tends to log rho(W), the log of the
spectral radius, for a generic start vector v.

tanh_rnn: the state h_T and the derivative dh_T/dh_0 of the scalar recurrent
network h_t = tanh(w h_(t-1) + b), which shows a gradient cliff.
"""

import math
import random

EULER_GAMMA = 0.5772156649015329


def digamma_half(m: int) -> float:
    """psi(m / 2) for a positive integer m, from the exact series."""
    if m % 2 == 0:
        return -EULER_GAMMA + sum(1.0 / j for j in range(1, m // 2))
    k = (m - 1) // 2
    return -EULER_GAMMA - 2.0 * math.log(2.0) + sum(2.0 / (2 * j - 1) for j in range(1, k + 1))


def predicted_rate(m: int, s: float) -> float:
    return math.log(s) + 0.5 * (digamma_half(m) - math.log(m / 2.0))


def _normalize(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v], n


def log_norm_rate(m: int, n: int, s: float, rng: random.Random) -> float:
    v, _ = _normalize([rng.gauss(0.0, 1.0) for _ in range(m)])
    sd = s / math.sqrt(m)
    total = 0.0
    for _ in range(n):
        J = [[rng.gauss(0.0, sd) for _ in range(m)] for _ in range(m)]
        v, norm = _normalize([sum(a * x for a, x in zip(row, v)) for row in J])
        total += math.log(norm)
    return total / n


def power_rate(W, v, n: int) -> float:
    v, _ = _normalize(list(v))
    total = 0.0
    for _ in range(n):
        v, norm = _normalize([sum(a * x for a, x in zip(row, v)) for row in W])
        total += math.log(norm)
    return total / n


def power_norms(W, n: int) -> list[float]:
    """Frobenius norms of W, W^2, ..., W^n."""
    m = len(W)
    P = [row[:] for row in W]
    out = []
    for _ in range(n):
        out.append(math.sqrt(sum(x * x for row in P for x in row)))
        P = [[sum(P[i][k] * W[k][j] for k in range(m)) for j in range(m)] for i in range(m)]
    return out


def tanh_rnn(w: float, b: float, T: int, h0: float):
    h, d = h0, 1.0
    for _ in range(T):
        h = math.tanh(w * h + b)
        d *= w * (1.0 - h * h)
    return h, d
