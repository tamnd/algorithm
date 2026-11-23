# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-mechanism/. The authors are listed in prov/12JV5Q.jsonl.
"""The two-sided geometric mechanism of Ghosh, Roughgarden and Sundararajan.

The noise Z = G1 - G2 is the difference of two independent geometric
variables with P(G = k) = (1 - alpha) alpha^k, so that
P(Z = d) = (1 - alpha) / (1 + alpha) alpha^|d|. With alpha = e^(-epsilon)
and an integer query of sensitivity 1, the output is epsilon-DP.

alpha is an exact rational in (0, 1), so every coin is exact and no float
is used on the sampling path. random.Random is used only so that the tests
are reproducible; a deployment needs a cryptographic source of randomness.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable, Optional, TypeVar, Union

Rational = Union[int, Fraction]
X = TypeVar("X")


def _check_alpha(alpha: Rational) -> Fraction:
    a = Fraction(alpha)
    if not 0 < a < 1:
        raise ValueError("alpha must be in (0, 1)")
    return a


def bernoulli(alpha: Fraction, rng: random.Random) -> bool:
    """True with probability exactly alpha. Cost: one uniform draw from {0, ..., den - 1}."""
    return rng.randrange(alpha.denominator) < alpha.numerator


def geometric_mechanism(
    x: X,
    f: Callable[[X], int],
    alpha: Rational,
    rng: random.Random,
    lo: Optional[int] = None,
    hi: Optional[int] = None,
) -> int:
    """Return f(x) + G1 - G2, clamped to [lo, hi] when the bounds are given.

    Precondition: f is integer valued with sensitivity 1 under the chosen
    neighbor relation, 0 < alpha < 1, and lo <= hi when both are given.
    The output is ln(1 / alpha)-DP; for sensitivity s, pass alpha = e^(-epsilon / s).
    Cost: expected 2 / (1 - alpha) Bernoulli draws and O(1) other word operations.
    """
    a = _check_alpha(alpha)
    if lo is not None and hi is not None and lo > hi:
        raise ValueError("need lo <= hi")
    v = f(x)  # @line L1
    g1 = 0  # @line L2
    while bernoulli(a, rng):  # @line L3
        g1 += 1
    g2 = 0  # @line L4
    while bernoulli(a, rng):  # @line L5
        g2 += 1
    z = v + g1 - g2  # @line L6
    if lo is not None and z < lo:  # @line L7
        z = lo
    if hi is not None and z > hi:  # @line L8
        z = hi
    return z  # @line L9


def noise_pmf(d: int, alpha: Rational) -> Fraction:
    """P(Z = d) = (1 - alpha) / (1 + alpha) alpha^|d| for the untruncated noise."""
    a = _check_alpha(alpha)
    return (1 - a) / (1 + a) * a ** abs(d)


def noise_tail(t: int, alpha: Rational) -> Fraction:
    """P(|Z| >= t) = 2 alpha^t / (1 + alpha) for an integer t >= 1."""
    a = _check_alpha(alpha)
    if t < 1:
        raise ValueError("need t >= 1")
    return 2 * a ** t / (1 + a)


def truncated_pmf(v: int, alpha: Rational, lo: int, hi: int) -> dict[int, Fraction]:
    """The exact pmf of the clamped output on {lo, ..., hi} when the true value is v.

    Precondition: lo <= v <= hi. The end points collect the tails:
    P(lo) = alpha^(v - lo) / (1 + alpha) and P(hi) = alpha^(hi - v) / (1 + alpha).
    If lo = hi, the output is lo with probability 1. Cost: O(hi - lo) exact operations.
    """
    a = _check_alpha(alpha)
    if not lo <= v <= hi:
        raise ValueError("need lo <= v <= hi")
    if lo == hi:
        return {lo: Fraction(1)}
    out = {z: (1 - a) / (1 + a) * a ** abs(z - v) for z in range(lo + 1, hi)}
    out[lo] = a ** (v - lo) / (1 + a)
    out[hi] = a ** (hi - v) / (1 + a)
    return out
