# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gibbs-phenomenon/. The authors are listed in prov/NNCRSC.jsonl.

"""Measure the Gibbs overshoot of Fourier partial sums.

The square wave is sign(sin t): +1 on (0, pi), -1 on (-pi, 0), jump 2 at t = 0.
Its Fourier series is (4/pi) times the sum of sin((2k - 1) t) / (2k - 1).
"""

import math


def sine_integral(x: float, terms: int = 60) -> float:
    """Return Si(x), the integral of sin(u)/u from 0 to x, by its power series."""
    total = 0.0
    term = x  # x^(2k+1) / (2k+1)! with alternating sign
    for k in range(terms):
        total += term / (2 * k + 1)
        term *= -x * x / ((2 * k + 2) * (2 * k + 3))
    return total


def gibbs_fraction() -> float:
    """Return the limiting overshoot as a fraction of the jump: Si(pi)/pi - 1/2."""
    return sine_integral(math.pi) / math.pi - 0.5


def square_wave_partial_sum(t: float, m: int) -> float:
    """Return the sum of the first m odd harmonics of the square wave at t."""
    return 4 / math.pi * sum(math.sin((2 * k - 1) * t) / (2 * k - 1) for k in range(1, m + 1))


def square_wave_fejer_mean(t: float, m: int) -> float:
    """Return the Cesaro (Fejer) mean of the partial sums S_0 .. S_(2m - 1).

    With M = 2m, harmonic j gets the weight 1 - j / M.
    """
    big_m = 2 * m
    return 4 / math.pi * sum((1 - j / big_m) * math.sin(j * t) / j for j in range(1, big_m, 2))


def peak_of_partial_sum(m: int, points: int = 400) -> tuple[float, float]:
    """Return (t, value) of the largest partial sum on a uniform grid of (0, pi/2]."""
    best_t, best_v = 0.0, -math.inf
    for j in range(1, points + 1):
        t = j * (math.pi / 2) / points
        v = square_wave_partial_sum(t, m)
        if v > best_v:
            best_t, best_v = t, v
    return best_t, best_v


def lowpass_partial_response(omega: float, cutoff: float, n_max: int) -> float:
    """Return the DTFT at omega of the ideal low-pass filter truncated to |n| <= n_max.

    h[0] = cutoff / pi and h[n] = sin(cutoff n) / (pi n); the response is real.
    """
    total = cutoff / math.pi
    for n in range(1, n_max + 1):
        total += 2 * math.sin(cutoff * n) / (math.pi * n) * math.cos(omega * n)
    return total
