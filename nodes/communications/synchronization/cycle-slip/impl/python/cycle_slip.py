# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-slip/. The authors are listed in prov/4GQF6S.jsonl.

"""Cycle slips of a first-order phase-locked loop: a closed form and a slip counter.

The first-order loop tracks an unmodulated carrier r[k] = e^(j theta) + w[k],
w[k] ~ CN(0, N0), with phi <- phi + K Im(r[k] e^(-j phi)). Its noise
bandwidth is B_L T = K / (2 (2 - K)), and its linear-model phase error
variance is B_L T / SNR = 1/rho, where rho is the loop SNR.

Viterbi's nonlinear analysis of the continuous-time first-order loop gives the
Tikhonov density exp(rho cos x) / (2 pi I0(rho)) for the phase error modulo
2 pi, and the mean time between slips

  T_slip = pi^2 rho I0(rho)^2 / (2 B_L)    (in seconds; divide by T for samples).

For the sampled loop with a small K this is a closed form under assumptions.
count_slips() measures the slips of the sampled loop by simulation.
"""

import cmath
import math
import random


def bessel_i0(x: float) -> float:
    """The modified Bessel function I0(x) = sum_k (x/2)^(2k) / (k!)^2."""
    term, total, k = 1.0, 1.0, 0
    while term > 1e-17 * total:
        k += 1
        term *= (x / 2.0) ** 2 / (k * k)
        total += term
    return total


def bessel_i1(x: float) -> float:
    """The modified Bessel function I1(x) = sum_k (x/2)^(2k+1) / (k! (k+1)!)."""
    term = x / 2.0
    total, k = term, 0
    while abs(term) > 1e-17 * abs(total) and term != 0.0:
        k += 1
        term *= (x / 2.0) ** 2 / (k * (k + 1))
        total += term
    return total


def first_order_bandwidth(k: float) -> float:
    """B_L T = K / (2 (2 - K)) of the loop phi <- phi + K e, for 0 < K < 2."""
    return k / (2.0 * (2.0 - k))


def mean_samples_between_slips(rho: float, bl_t: float) -> float:
    """Viterbi's closed form pi^2 rho I0(rho)^2 / (2 B_L T), in samples."""
    return math.pi**2 * rho * bessel_i0(rho) ** 2 / (2.0 * bl_t)


def simulate_errors(k: float, snr: float, n: int, seed: int) -> list[float]:
    """The unwrapped phase error theta - phi of the first-order loop over n samples, theta = 0."""
    rng = random.Random(seed)
    sd = math.sqrt(0.5 / snr)
    phi, out = 0.0, []
    for _ in range(n):
        r = complex(1.0 + rng.gauss(0, sd), rng.gauss(0, sd))
        e = (r * cmath.exp(-1j * phi)).imag
        phi += k * e
        out.append(-phi)
    return out


def count_slips(errors: list[float]) -> int:
    """Count slips with hysteresis: the loop must pass 3 pi/2 beyond its current lock point."""
    n, slips = 0, 0
    for x in errors:
        while x > 2.0 * math.pi * n + 1.5 * math.pi:
            n += 1
            slips += 1
        while x < 2.0 * math.pi * n - 1.5 * math.pi:
            n -= 1
            slips += 1
    return slips
