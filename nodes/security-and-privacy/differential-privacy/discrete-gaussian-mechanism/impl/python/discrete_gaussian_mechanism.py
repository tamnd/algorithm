# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-gaussian-mechanism/. The authors are listed in prov/70PG4J.jsonl.
"""The discrete Gaussian mechanism with the exact sampler of Canonne, Kamath
and Steinke (NeurIPS 2020).

The noise has P[Y = y] proportional to exp(-y^2 / (2 sigma^2)) on the
integers. The sampler uses only uniform random integers and exact rational
arithmetic (fractions.Fraction): no floats, no exp, no sqrt. It is
Algorithm 1 (Bernoulli(exp(-gamma))), Algorithm 2 (discrete Laplace) and
Algorithm 3 (discrete Gaussian by rejection) of their paper.

The tests pass a seeded random.Random so that each run repeats. That is for
study only. A deployment needs a cryptographic source of randomness, for
example secrets.SystemRandom(), which has the same randrange method, and it
needs exact sampling as here: float noise from a seeded generator leaks
through its low-order bits (Mironov 2012; Canonne, Kamath and Steinke 2020).
The code assumes the word RAM, with operations on rationals of moderate size.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Union

Rational = Union[int, Fraction]


def _as_positive_fraction(sigma2: Rational) -> Fraction:
    if isinstance(sigma2, bool) or not isinstance(sigma2, (int, Fraction)):
        raise TypeError("sigma2 must be an int or a Fraction, not a float")
    s = Fraction(sigma2)
    if s <= 0:
        raise ValueError("sigma2 must be positive")
    return s


def bernoulli(p: Fraction, rng: random.Random) -> int:
    """Return 1 with probability exactly p. Precondition: 0 <= p <= 1. Cost: O(1)."""
    if not 0 <= p <= 1:
        raise ValueError("p must be in [0, 1]")
    return 1 if rng.randrange(p.denominator) < p.numerator else 0


def _bernoulli_exp_neg_unit(gamma: Fraction, rng: random.Random) -> int:
    """Return 1 with probability exp(-gamma), for 0 <= gamma <= 1.

    Draw A_k ~ Bernoulli(gamma / k) for k = 1, 2, ... until the first 0; the
    index K of that 0 is odd with probability exp(-gamma).
    Cost: at most e expected draws.
    """
    k = 1
    while bernoulli(gamma / k, rng) == 1:
        k += 1
    return k % 2


def bernoulli_exp_neg(gamma: Rational, rng: random.Random) -> int:
    """Return 1 with probability exactly exp(-gamma). Algorithm 1 of CKS.

    Precondition: gamma >= 0 is rational. Cost: O(1) expected draws, since
    the loop stops at the first Bernoulli(exp(-1)) draw that is 0.
    """
    g = Fraction(gamma)
    if g < 0:
        raise ValueError("gamma must be non-negative")
    if g <= 1:
        return _bernoulli_exp_neg_unit(g, rng)
    whole = math.floor(g)
    for _ in range(whole):
        if _bernoulli_exp_neg_unit(Fraction(1), rng) == 0:
            return 0
    return _bernoulli_exp_neg_unit(g - whole, rng)


def discrete_laplace(t: int, rng: random.Random) -> int:
    """Return Y with P[Y = y] proportional to exp(-|y| / t). Algorithm 2 of CKS with s = 1.

    Precondition: t >= 1 is an integer. Cost: O(1) expected draws.
    """
    if t < 1:
        raise ValueError("t must be a positive integer")
    while True:
        u = rng.randrange(t)
        if bernoulli_exp_neg(Fraction(u, t), rng) == 0:
            continue
        v = 0
        while bernoulli_exp_neg(1, rng) == 1:
            v += 1
        magnitude = u + t * v  # geometric with ratio exp(-1/t)
        negative = bernoulli(Fraction(1, 2), rng)
        if negative == 1 and magnitude == 0:
            continue  # so that 0 is not counted twice
        return -magnitude if negative else magnitude


def laplace_scale_for(sigma2: Rational) -> int:
    """t = floor(sigma) + 1, the least integer t with t^2 > sigma^2. Cost: O(1)."""
    s = _as_positive_fraction(sigma2)
    t = math.isqrt(math.floor(s))
    while t * t <= s:
        t += 1
    return t


def acceptance_exponent(y: int, sigma2: Rational, t: int) -> Fraction:
    """gamma = (|y| - sigma^2 / t)^2 / (2 sigma^2), the exponent of line L4."""
    s = _as_positive_fraction(sigma2)
    d = abs(y) - s / t
    return d * d / (2 * s)


def discrete_gaussian_mechanism(value: int, sigma2: Rational, rng: random.Random) -> int:
    """Release value + Y with Y from the discrete Gaussian N_Z(0, sigma2).

    value is the true answer f(x) of an integer query. If f has sensitivity
    Delta, the release is (Delta^2 / (2 sigma2))-zCDP.
    Precondition: sigma2 > 0 rational. Cost: O(1) expected rounds of the
    loop (each round accepts with probability above 0.29).
    """
    s = _as_positive_fraction(sigma2)
    t = laplace_scale_for(s)  # @line L1
    while True:  # @line L2
        y = discrete_laplace(t, rng)  # @line L3
        gamma = acceptance_exponent(y, s, t)  # @line L4
        c = bernoulli_exp_neg(gamma, rng)  # @line L5
        if c == 1:  # @line L6
            return value + y


def discrete_gaussian(sigma2: Rational, rng: random.Random) -> int:
    """One sample of N_Z(0, sigma2). Same precondition and cost as the mechanism."""
    return discrete_gaussian_mechanism(0, sigma2, rng)


def discrete_gaussian_delta(epsilon: float, sigma2: Rational, sensitivity: int = 1) -> float:
    """The tight delta of the mechanism at epsilon, by Theorem 7 of CKS.

    delta = P[Y > epsilon sigma^2 / Delta - Delta / 2]
            - e^epsilon P[Y > epsilon sigma^2 / Delta + Delta / 2],
    with Y ~ N_Z(0, sigma^2). This is accounting, so it uses floats; the sums
    stop at |y| = 40 sigma + epsilon sigma^2 / Delta + Delta + 10, past which
    the terms are below exp(-800).
    Precondition: epsilon >= 0, sigma2 > 0, sensitivity >= 1.
    Cost: O(sigma + epsilon sigma^2) float operations.
    """
    s = float(_as_positive_fraction(sigma2))
    if epsilon < 0 or sensitivity < 1:
        raise ValueError("need epsilon >= 0 and sensitivity >= 1")
    shift = epsilon * s / sensitivity
    bound = int(40 * math.sqrt(s) + shift + sensitivity + 10)
    weights = [math.exp(-(y * y) / (2 * s)) for y in range(-bound, bound + 1)]
    total = math.fsum(weights)

    def tail(a: float) -> float:
        return math.fsum(w for y, w in zip(range(-bound, bound + 1), weights) if y > a) / total

    delta = tail(shift - sensitivity / 2) - math.exp(epsilon) * tail(shift + sensitivity / 2)
    return max(0.0, delta)
