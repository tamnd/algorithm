# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kalman-channel-tracking/. The authors are listed in prov/JMK6AT.jsonl.

"""Kalman tracking of a time-varying FIR channel with a first-order autoregressive model.

The channel has L taps h_k = (h_k[0], ..., h_k[L-1]) at symbol time k. The
state model is h_k = a h_(k-1) + v_k with v_k ~ CN(0, Q) and
Q = (1 - a^2) diag(P), where P[l] is the power of tap l. This keeps every tap
stationary with E|h_k[l]|^2 = P[l]. The observation is
y[k] = sum_l h_k[l] x[k-l] + w[k] = c_k h_k + w[k], with the row
c_k = (x[k], x[k-1], ..., x[k-L+1]) of known symbols (pilots, training or
decisions) and w[k] ~ CN(0, N0). Symbols before time 0 are taken as 0.
"""

import math
import random

import cbb


def bessel_j0(x: float) -> float:
    """J0(x) from its power series sum (-1)^m (x/2)^(2m) / (m!)^2; accurate for |x| <= 10."""
    t = 1.0
    s = 1.0
    q = (x / 2.0) ** 2
    m = 0
    while abs(t) > 1e-17 * max(1.0, abs(s)):
        m += 1
        t *= -q / (m * m)
        s += t
    return s


def ar1_coefficient(fd_t: float) -> float:
    """The lag-1 fit a = J0(2 pi f_D T) of a Clarke channel, for the normalized Doppler f_D T."""
    return bessel_j0(2.0 * math.pi * fd_t)


def regressor(x: list[complex], k: int, taps: int) -> list[complex]:
    """The row c_k = (x[k], x[k-1], ..., x[k-L+1]), with 0 before time 0."""
    return [complex(x[k - l]) if k - l >= 0 else 0j for l in range(taps)]


def kalman_track(y: list[complex], x: list[complex], a: float, p: list[float], n0: float) -> tuple[list[list[complex]], list[list[list[complex]]]]:
    """The filtered estimates E[h_k | y[0..k]] and their error covariances, for k = 0, ..., K-1."""
    taps = len(p)
    if len(x) != len(y):
        raise ValueError("x and y differ in length")
    if not 0.0 <= a <= 1.0 or n0 <= 0 or any(v < 0 for v in p):
        raise ValueError("need 0 <= a <= 1, N0 > 0 and P >= 0")
    q = [(1.0 - a * a) * v for v in p]
    h = [0j] * taps  # @line L1
    s = [[complex(p[i]) if i == j else 0j for j in range(taps)] for i in range(taps)]  # @line L1
    estimates, covariances = [], []
    for k in range(len(y)):  # @line L2
        h = [a * v for v in h]  # @line L3
        s = [[a * a * s[i][j] + (q[i] if i == j else 0.0) for j in range(taps)] for i in range(taps)]  # @line L3
        c = regressor(x, k, taps)  # @line L4
        sc = [sum(s[i][j] * c[j].conjugate() for j in range(taps)) for i in range(taps)]  # S c^H
        inn = sum(c[i] * sc[i] for i in range(taps)).real + n0  # @line L5
        g = [v / inn for v in sc]  # @line L6
        e = y[k] - sum(c[i] * h[i] for i in range(taps))
        h = [h[i] + g[i] * e for i in range(taps)]  # @line L7
        cs = [sum(c[i] * s[i][j] for i in range(taps)) for j in range(taps)]  # c S
        s = [[s[i][j] - g[i] * cs[j] for j in range(taps)] for i in range(taps)]  # @line L8
        s = [[0.5 * (s[i][j] + s[j][i].conjugate()) for j in range(taps)] for i in range(taps)]
        estimates.append(list(h))  # @line L9
        covariances.append([list(r) for r in s])
    return estimates, covariances


def ar1_channel(rng: random.Random, a: float, p: list[float], count: int) -> list[list[complex]]:
    """count channel vectors h_0, ..., h_(count-1) of the AR(1) model, started in the stationary law."""
    q = [(1.0 - a * a) * v for v in p]
    h = [cbb.cn(rng, v) for v in p]
    out = []
    for _ in range(count):
        out.append(list(h))
        h = [a * h[i] + cbb.cn(rng, q[i]) for i in range(len(p))]
    return out


def transmit(rng: random.Random, hs: list[list[complex]], x: list[complex], n0: float) -> list[complex]:
    """y[k] = c_k h_k + w[k] with w[k] ~ CN(0, N0)."""
    taps = len(hs[0])
    return [sum(c * v for c, v in zip(regressor(x, k, taps), hs[k])) + cbb.cn(rng, n0) for k in range(len(x))]
