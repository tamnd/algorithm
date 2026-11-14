# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shapiro-wilk-test/. The authors are listed in prov/F6R58F.jsonl.
"""The Shapiro-Wilk W test of normality, with Royston's approximations.

W = (sum a_i y_(i))^2 / sum (y_i - ybar)^2, where y_(1) <= ... <= y_(n) is
the sorted sample and a is proportional to V^(-1) m, with m and V the mean
vector and covariance matrix of standard normal order statistics, scaled
so that sum a_i^2 = 1. The coefficients a and the p-value use the
approximations of Royston (1992), in the form of Algorithm AS R94 (Royston
1995): the coefficients from m_i = Phi^(-1)((i - 3/8)/(n + 1/4)) with a
polynomial correction of the two largest, and a normalizing transform of
W whose upper tail is the p-value. For n = 3 the p-value is exact. For
n >= 4 the coefficients are within about 1e-3 of the exact ones for small
n (measured) and the p-value is an approximation.
The code is in this file and not in shapiro_wilk_test.py, because tools
treat a file whose name ends in _test.py as a test file.
"""

import math
from collections.abc import Sequence

from stdist import norm_ppf, norm_sf

# Royston's polynomials, coefficients in increasing powers.
_C1 = (0.0, 0.221157, -0.147981, -2.07119, 4.434685, -2.706056)  # a_n, in 1/sqrt(n)
_C2 = (0.0, 0.042981, -0.293762, -1.752461, 5.682633, -3.582633)  # a_(n-1), in 1/sqrt(n)
_C3 = (0.544, -0.39978, 0.025054, -6.714e-4)  # mean, n <= 11, in n
_C4 = (1.3822, -0.77857, 0.062767, -0.0020322)  # log sd, n <= 11, in n
_C5 = (-1.5861, -0.31082, -0.083751, 0.0038915)  # mean, n >= 12, in log n
_C6 = (-0.4803, -0.082676, 0.0030302)  # log sd, n >= 12, in log n


def _poly(c: Sequence[float], x: float) -> float:
    r = 0.0
    for v in reversed(c):
        r = r * x + v
    return r


def shapiro_wilk_coefficients(n: int) -> list[float]:
    """Royston's approximation of a = V^(-1) m / ||V^(-1) m||, for 3 <= n <= 5000."""
    if not 3 <= n <= 5000:
        raise ValueError("need 3 <= n <= 5000")
    if n == 3:
        return [-math.sqrt(0.5), 0.0, math.sqrt(0.5)]
    m = [norm_ppf((i - 0.375) / (n + 0.25)) for i in range(1, n + 1)]
    mm = math.fsum(v * v for v in m)
    u = 1.0 / math.sqrt(n)
    a = [0.0] * n
    an = _poly(_C1, u) + m[-1] / math.sqrt(mm)
    if n > 5:
        an1 = _poly(_C2, u) + m[-2] / math.sqrt(mm)
        phi = (mm - 2 * m[-1] ** 2 - 2 * m[-2] ** 2) / (1 - 2 * an ** 2 - 2 * an1 ** 2)
        a[0], a[1], a[-2], a[-1] = -an, -an1, an1, an
        lo, hi = 2, n - 2
    else:
        phi = (mm - 2 * m[-1] ** 2) / (1 - 2 * an ** 2)
        a[0], a[-1] = -an, an
        lo, hi = 1, n - 1
    for i in range(lo, hi):
        a[i] = m[i] / math.sqrt(phi)
    return a


def shapiro_wilk(x: Sequence[float]) -> tuple[float, float]:
    """Shapiro-Wilk test of normality; returns (W, p), with p small for non-normal data."""
    n = len(x)
    if not 3 <= n <= 5000:
        raise ValueError("need 3 <= n <= 5000")
    y = sorted(x)  # @line L1
    a = shapiro_wilk_coefficients(n)  # @line L2
    mean = math.fsum(y) / n  # @line L3
    ss = math.fsum((v - mean) ** 2 for v in y)
    if ss == 0.0:
        raise ValueError("all observations are equal")
    b = math.fsum(a[n - 1 - i] * (y[n - 1 - i] - y[i]) for i in range(n // 2))  # @line L4
    w = min(b * b / ss, 1.0)  # @line L5
    if n == 3:  # @line L6
        p = 6.0 / math.pi * (math.asin(math.sqrt(w)) - math.pi / 3.0)
        return w, min(max(p, 0.0), 1.0)
    w1 = math.log1p(-w) if w < 1.0 else -math.inf  # @line L7
    if n <= 11:
        gamma = -2.273 + 0.459 * n
        if w1 >= gamma:  # W below the range of the transform: p is negligible
            return w, 0.0
        t = -math.log(gamma - w1)
        mu, sd = _poly(_C3, n), math.exp(_poly(_C4, n))
    else:
        t = w1
        mu, sd = _poly(_C5, math.log(n)), math.exp(_poly(_C6, math.log(n)))
    z = (t - mu) / sd  # @line L8
    return w, norm_sf(z)  # @line L9
