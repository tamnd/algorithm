# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixture-sequential-probability-ratio-test/. The authors are listed in prov/7K0XX7.jsonl.
"""The mixture sequential probability ratio test (mSPRT) for a normal mean.

Data x_1, x_2, ... are i.i.d. N(theta, sigma^2) with sigma known. H0 is
theta = theta0. The likelihood ratio of N(theta, sigma^2) to N(theta0,
sigma^2) is mixed over theta ~ N(theta0, tau^2), which gives the closed form

    Lambda_n = sqrt(sigma^2 / (sigma^2 + n tau^2))
               * exp(tau^2 S_n^2 / (2 sigma^2 (sigma^2 + n tau^2))),

with S_n = sum (x_i - theta0). Lambda_n is a nonnegative martingale with mean 1
under H0, so rejecting at the first n with Lambda_n >= 1/alpha has level alpha
at every stopping time (Ville's inequality). The always valid p-value is
p_n = min(1, 1 / max_(k <= n) Lambda_k). Cost O(1) time and memory per item.
"""

import math
from collections.abc import Iterable
from fractions import Fraction


def msprt_ratio(n: int, s: float, sigma: float, tau: float) -> float:
    """Lambda_n from n and the centred sum s = sum (x_i - theta0)."""
    v = sigma * sigma + n * tau * tau
    return math.sqrt(sigma * sigma / v) * math.exp(tau * tau * s * s / (2.0 * sigma * sigma * v))


def msprt(stream: Iterable[float], theta0: float, sigma: float, tau: float,
          alpha: float) -> tuple[bool, int, float]:
    """Run the normal mSPRT. Returns (rejected, n, always valid p-value at stop).

    Precondition: sigma > 0, tau > 0, 0 < alpha < 1. The test stops at the
    first n with Lambda_n >= 1/alpha, or at the end of the stream.
    """
    if sigma <= 0 or tau <= 0 or not 0.0 < alpha < 1.0:
        raise ValueError("need sigma > 0, tau > 0, 0 < alpha < 1")
    s = 0.0  # @line L1
    n = 0  # @line L1
    p = 1.0  # @line L1
    for x in stream:  # @line L2
        n += 1  # @line L3
        s += x - theta0  # @line L3
        lam = msprt_ratio(n, s, sigma, tau)  # @line L4
        p = min(p, 1.0 / lam)  # @line L5
        if lam >= 1.0 / alpha:  # @line L6
            return True, n, p  # @line L6
    return False, n, p  # @line L7


def always_valid_p_values(xs: Iterable[float], theta0: float, sigma: float, tau: float) -> list[float]:
    """The sequence p_1, p_2, ... with p_n = min(1, 1 / max_(k <= n) Lambda_k)."""
    out = []
    s = 0.0
    p = 1.0
    for n, x in enumerate(xs, 1):
        s += x - theta0
        p = min(p, 1.0 / msprt_ratio(n, s, sigma, tau))
        out.append(p)
    return out


def _beta_fn(a: int, b: int) -> Fraction:
    return Fraction(math.factorial(a - 1) * math.factorial(b - 1), math.factorial(a + b - 1))


def beta_bernoulli_ratio(heads: int, tails: int, a: int, b: int, p0: Fraction) -> Fraction:
    """Exact mixture ratio for coin flips: Beta(a, b) mixture over p against the point p0.

    Lambda = B(a + heads, b + tails) / B(a, b) / (p0^heads (1 - p0)^tails).
    Precondition: a, b positive integers, 0 < p0 < 1.
    """
    return _beta_fn(a + heads, b + tails) / _beta_fn(a, b) / (p0 ** heads * (1 - p0) ** tails)
