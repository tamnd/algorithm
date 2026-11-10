# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/importance-sampling/. The authors are listed in prov/ES82YY.jsonl.

"""Importance sampling.

To estimate mu = E_p[f(X)], draw X_1..X_n from a proposal q and average
w_j f(X_j) with w_j = p(X_j) / q(X_j). The estimate is unbiased when q > 0
wherever f p != 0. Self-normalized importance sampling divides by the sum
of the weights instead of n; it needs p only up to a constant and has a bias
of order 1 / n. The effective sample size (sum w)^2 / sum w^2 is Kong's
diagnostic.
"""

import math
import random
from fractions import Fraction
from typing import Callable, Dict, Sequence, Tuple


def is_estimate(
    f: Callable, p: Callable, q: Callable, q_sample: Callable, n: int, rng: random.Random
) -> float:
    """The plain importance sampling estimate of E_p[f]."""
    total = 0.0
    for _ in range(n):  # @line L1
        x = q_sample(rng)  # @line L1
        total += p(x) / q(x) * f(x)  # @line L1
    return total / n  # @line L2


def snis_estimate(
    f: Callable, p_tilde: Callable, q: Callable, q_sample: Callable, n: int, rng: random.Random
) -> Tuple[float, float]:
    """The self-normalized estimate of E_p[f] and the effective sample size.

    p_tilde is p up to an unknown constant factor.
    """
    sw = swf = sw2 = 0.0
    for _ in range(n):  # @line L3
        x = q_sample(rng)  # @line L3
        w = p_tilde(x) / q(x)  # @line L3
        sw += w
        swf += w * f(x)
        sw2 += w * w
    return swf / sw, sw * sw / sw2  # @line L4


def effective_sample_size(weights: Sequence[float]) -> float:
    """Kong's effective sample size (sum w)^2 / sum w^2."""
    s = sum(weights)
    return s * s / sum(w * w for w in weights)  # @line L5


# Exact forms on a finite space, with Fractions.

def exact_mean_and_variance(f: Dict, p: Dict, q: Dict) -> Tuple[Fraction, Fraction]:
    """E_q and Var_q of one term w f, with w = p / q. Returns (mean, variance)."""
    m1 = sum((q[x] * (p[x] / q[x]) * f[x] for x in q if q[x] > 0), Fraction(0))
    m2 = sum((q[x] * (p[x] / q[x] * f[x]) ** 2 for x in q if q[x] > 0), Fraction(0))
    return m1, m2 - m1 * m1


def optimal_proposal(f: Dict, p: Dict) -> Dict:
    """q* proportional to |f| p."""
    z = sum(abs(f[x]) * p[x] for x in p)
    return {x: abs(f[x]) * p[x] / z for x in p}


def rare_event_normal_tail(c: float, n: int, rng: random.Random) -> float:
    """Pr[Z > c] for Z ~ N(0, 1), with the shifted proposal N(c, 1).

    The weight is phi(x) / phi(x - c) = exp(-c x + c^2 / 2).
    """
    return is_estimate(
        lambda x: 1.0 if x > c else 0.0,
        lambda x: math.exp(-0.5 * x * x),
        lambda x: math.exp(-0.5 * (x - c) ** 2),
        lambda r: r.gauss(c, 1.0),
        n,
        rng,
    )
