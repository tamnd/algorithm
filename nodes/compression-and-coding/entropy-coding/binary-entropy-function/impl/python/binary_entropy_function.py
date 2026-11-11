# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-entropy-function/. The authors are listed in prov/MA49SE.jsonl.
"""The binary entropy function h(p), its inverse on [0, 1/2], and the exact binomial estimate."""

from math import comb, log2


def h(p: float) -> float:
    """h(p) = -p log2 p - (1 - p) log2 (1 - p), with h(0) = h(1) = 0."""
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0, 1]")
    if p == 0.0 or p == 1.0:
        return 0.0
    return -p * log2(p) - (1.0 - p) * log2(1.0 - p)


def h_derivative(p: float) -> float:
    """h'(p) = log2((1 - p) / p) for 0 < p < 1."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    return log2((1.0 - p) / p)


def h_inverse(y: float, tol: float = 1e-15) -> float:
    """The unique p in [0, 1/2] with h(p) = y, for y in [0, 1], by bisection.

    h is continuous and strictly increasing on [0, 1/2], so bisection keeps
    h(lo) <= y <= h(hi) and halves the interval at each step.
    """
    if not 0.0 <= y <= 1.0:
        raise ValueError("y must be in [0, 1]")
    lo, hi = 0.0, 0.5
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if h(mid) < y:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def two_pow_n_h(n: int, k: int) -> tuple[int, int]:
    """2^(n h(k/n)) as an exact fraction (numerator, denominator) = (n^n, k^k (n - k)^(n - k)).

    The convention 0^0 = 1 covers k = 0 and k = n.
    """
    if not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n")
    return n ** n, k ** k * (n - k) ** (n - k)


def binomial_bounds_hold(n: int, k: int) -> bool:
    """Check 2^(n h(k/n)) / (n + 1) <= C(n, k) <= 2^(n h(k/n)) in exact integer arithmetic."""
    num, den = two_pow_n_h(n, k)
    c = comb(n, k)
    return num <= (n + 1) * c * den and c * den <= num
