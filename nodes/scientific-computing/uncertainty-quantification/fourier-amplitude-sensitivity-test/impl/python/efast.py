# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fourier-amplitude-sensitivity-test/. The authors are listed in prov/VVPHQA.jsonl.
"""The Fourier amplitude sensitivity test in its extended form (eFAST, Saltelli, Tarantola and Chan 1999).

For each input i, all inputs move along one search curve in the unit cube,

    x_j(s) = 1/2 + arcsin(sin(omega_j s + phi_j)) / pi,   s in (-pi, pi),

with a high frequency omega_i for input i and low frequencies for the others.
Each x_j(s) is uniform on [0, 1] when s is uniform. The output y(s) = f(x(s))
is periodic in s, and its Fourier spectrum splits the variance: the power at
the harmonics q omega_i, q = 1..M, is the first order part D_i, and the power at
the frequencies up to omega_i / 2 belongs to the complementary inputs, so that
1 - D_(~i) / D is the total index. The phases phi_j are random, and the run is
repeated n_r times (resampling) to reduce the error from the curve.

The classic FAST of Cukier et al. 1973 uses one curve with a frequency set
for all inputs at once and gives the first order indices only.

The cost is d n_r n_s model runs, with n_s >= 2 M omega_max + 1 points per curve.
"""

import math
import random
from typing import Callable, Sequence

Model = Callable[[Sequence[float]], float]


def frequencies(d: int, i: int, omega_max: int, m: int) -> list[int]:
    """omega_i = omega_max, and the other inputs get frequencies in 1..floor(omega_max / (2 M)).

    If there is room, the d - 1 low frequencies are spread evenly over that range,
    else they cycle through it. Spread frequencies make the curve fill more of the
    subcube of the other inputs.
    """
    top = omega_max // (2 * m)
    if top < 1:
        raise ValueError("omega_max must be at least 2 M")
    rest = d - 1
    if rest == 1:
        low = [1]
    elif top >= rest:
        low = [1 + (top - 1) * k // (rest - 1) for k in range(rest)]
    else:
        low = [1 + k % top for k in range(rest)]
    out = list(low)
    out.insert(i, omega_max)
    return out


def search_points(omegas: Sequence[int], phases: Sequence[float], n_s: int) -> list[list[float]]:
    """The n_s points of the curve at s_k = pi (2k - n_s - 1) / n_s, k = 1..n_s, in the unit cube."""
    pts = []
    for k in range(1, n_s + 1):
        s = math.pi * (2 * k - n_s - 1) / n_s
        pts.append([0.5 + math.asin(math.sin(w * s + ph)) / math.pi for w, ph in zip(omegas, phases)])
    return pts


def spectrum(y: Sequence[float], n_s: int) -> list[float]:
    """The power Lambda_p = (A_p^2 + B_p^2) / 2 for p = 0..(n_s - 1) / 2 (Lambda_0 is unused).

    For odd n_s, the sum of Lambda_p over p >= 1 is the population variance of y (discrete Parseval).
    """
    half = (n_s - 1) // 2
    s = [math.pi * (2 * k - n_s - 1) / n_s for k in range(1, n_s + 1)]
    out = [0.0]
    for p in range(1, half + 1):
        a = 2.0 / n_s * sum(yk * math.cos(p * sk) for yk, sk in zip(y, s))
        b = 2.0 / n_s * sum(yk * math.sin(p * sk) for yk, sk in zip(y, s))
        out.append(0.5 * (a * a + b * b))
    return out


def efast(f: Model, d: int, omega_max: int, m: int, n_r: int, rng: random.Random, n_s: int = 0) -> dict:
    """First order and total indices of the d inputs of f on the unit cube [0, 1]^d."""
    if n_s == 0:
        n_s = 2 * m * omega_max + 1
    if n_s < 2 * m * omega_max + 1 or n_s % 2 == 0:
        raise ValueError("n_s must be odd and at least 2 M omega_max + 1")
    s_first, s_total, runs = [], [], 0
    for i in range(d):  # @line L1
        first = total = 0.0
        omegas = frequencies(d, i, omega_max, m)  # @line L2
        for _ in range(n_r):  # @line L3
            phases = [2 * math.pi * rng.random() for _ in range(d)]
            pts = search_points(omegas, phases, n_s)  # @line L4
            y = [f(x) for x in pts]  # @line L5
            runs += n_s
            lam = spectrum(y, n_s)  # @line L6
            var = sum(lam[1:])  # @line L7
            d_i = sum(lam[q * omega_max] for q in range(1, m + 1))  # @line L8
            d_rest = sum(lam[1 : omega_max // 2 + 1])  # @line L9
            first += d_i / var
            total += 1.0 - d_rest / var
        s_first.append(first / n_r)  # @line L10
        s_total.append(total / n_r)
    return {"S": s_first, "ST": s_total, "runs": runs, "n_s": n_s}
