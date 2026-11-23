# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplace-mechanism/. The authors are listed in prov/ZJZCN9.jsonl.
"""The Laplace mechanism of Dwork, McSherry, Nissim and Smith (2006).

The code uses random.Random so that the tests are reproducible, and it adds
float noise. Both are fine for study and wrong for a deployment: a real
release needs a cryptographic source of randomness and an exact sampler,
because the float version leaks through its low-order bits (Mironov 2012).
"""

from __future__ import annotations

import math
import random
from typing import Callable, Sequence, TypeVar

D = TypeVar("D")


def laplace_scale(sensitivity: float, epsilon: float) -> float:
    """The noise scale b = sensitivity / epsilon. Precondition: both are positive."""
    if sensitivity <= 0 or epsilon <= 0:
        raise ValueError("sensitivity and epsilon must be positive")
    return sensitivity / epsilon


def laplace_from_uniform(u: float, b: float) -> float:
    """The Lap(b) quantile at u + 1/2, for u in the open interval (-1/2, 1/2).

    This is the inverse of the CDF F(z) = e^(z/b)/2 for z < 0 and
    1 - e^(-z/b)/2 for z >= 0. Cost: O(1).
    """
    if not -0.5 < u < 0.5:
        raise ValueError("u must be in (-1/2, 1/2)")
    s = (u > 0) - (u < 0)
    return -b * s * math.log(1.0 - 2.0 * abs(u))


def laplace_mechanism(
    x: D,
    f: Callable[[D], Sequence[float]],
    sensitivity: float,
    epsilon: float,
    rng: random.Random,
) -> list[float]:
    """Release f(x) plus independent Lap(sensitivity / epsilon) noise on each coordinate.

    Precondition: sensitivity is at least the l1 sensitivity of f under the
    neighbor relation that the caller uses, and epsilon > 0. Then the output
    is epsilon-differentially private for that relation.
    Cost: one evaluation of f, then O(k) time and k uniform draws for k coordinates.
    """
    b = laplace_scale(sensitivity, epsilon)  # @line L1
    v = list(f(x))  # @line L2
    y: list[float] = []
    for vi in v:  # @line L3
        u = rng.random() - 0.5  # @line L4
        while u == -0.5:  # the open interval excludes -1/2
            u = rng.random() - 0.5
        z = laplace_from_uniform(u, b)  # @line L5
        y.append(vi + z)  # @line L6
    return y  # @line L7


def laplace_log_density(y: Sequence[float], center: Sequence[float], b: float) -> float:
    """The log density at y of center plus k independent Lap(b) coordinates. Cost: O(k)."""
    return sum(-math.log(2.0 * b) - abs(yi - ci) / b for yi, ci in zip(y, center))


def laplace_tail(t: float, b: float) -> float:
    """P(|Z| > t) = e^(-t/b) for Z ~ Lap(b) and t >= 0."""
    return math.exp(-t / b)


def laplace_error_bound(k: int, b: float, beta: float) -> float:
    """The bound b ln(k / beta) on the largest error over k coordinates.

    With probability at least 1 - beta, every coordinate of the noise is at
    most this value in absolute value (a union bound over the k tails).
    """
    return b * math.log(k / beta)
