# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filtered-gaussian-fading-simulator/. The authors are listed in prov/K4JBF8.jsonl.

"""Rayleigh fading by filtering complex Gaussian noise in the frequency domain.

This is the IDFT method of Young and Beaulieu 2000. Independent CN(0, 1)
samples G[k] are weighted by a filter F[k] whose square follows the Doppler
spectrum of Clarke's model, 1 / sqrt(1 - (f / f_D)^2), and one inverse DFT
gives N correlated samples h[0..N-1]. The normalized Doppler is f_m = f_D / f_s,
and k_m = floor(N f_m) is the last bin inside the spectrum. The edge bin
k_m gets the area of the spectrum over that bin, so the infinite peak at f_D
does not break the filter. The output is scaled so that E|h[n]|^2 = Omega.

The inverse DFT is the direct sum of cbb.idft. An FFT gives the same result
in O(N log N) operations.
"""

import math
import random

import cbb


def doppler_filter(n: int, fm: float) -> list[float]:
    """The real filter F[0..N-1] of Young and Beaulieu for N bins and normalized Doppler f_m."""
    km = math.floor(n * fm)  # @line L1
    if km < 2 or 2 * km >= n:
        raise ValueError("need 2 <= floor(N f_m) < N / 2")
    f = [0.0] * n
    for k in range(1, km):
        f[k] = math.sqrt(1.0 / (2.0 * math.sqrt(1.0 - (k / (n * fm)) ** 2)))  # @line L2
    f[km] = math.sqrt((km / 2.0) * (math.pi / 2.0 - math.atan((km - 1) / math.sqrt(2.0 * km - 1))))  # @line L3
    for k in range(1, km + 1):
        f[n - k] = f[k]  # @line L4
    return f


def filtered_gaussian(n: int, fm: float, rng: random.Random, omega: float = 1.0, g: list[complex] | None = None) -> list[complex]:
    """N samples of correlated Rayleigh fading with E|h|^2 = Omega.

    g, if given, replaces the N random CN(0, 1) inputs; the map from g to h is linear.
    """
    f = doppler_filter(n, fm)
    if g is None:
        g = [cbb.cn(rng, 1.0) for _ in range(n)]
    if len(g) != n:
        raise ValueError("need N inputs")
    x = [f[k] * g[k] for k in range(n)]  # @line L5
    y = cbb.idft(x)  # @line L6
    c = n * math.sqrt(omega / sum(v * v for v in f))
    return [c * v for v in y]  # @line L7


def exact_autocorrelation(n: int, fm: float, d: int, omega: float = 1.0) -> float:
    """E[h[i + d] conj(h[i])] = Omega sum_k F[k]^2 cos(2 pi k d / N) / sum_k F[k]^2, for every i (circular)."""
    f = doppler_filter(n, fm)
    s = sum(v * v for v in f)
    return omega * sum(f[k] ** 2 * math.cos(2.0 * math.pi * k * d / n) for k in range(n)) / s


def j0(x: float, points: int = 2048) -> float:
    """J0(x) = (1 / 2 pi) integral over [0, 2 pi) of cos(x sin t) dt, by the trapezoid rule."""
    h = 2.0 * math.pi / points
    return sum(math.cos(x * math.sin(k * h)) for k in range(points)) / points
