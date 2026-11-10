# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/p-stable-distribution/. The authors are listed in prov/9QBY0D.jsonl.

"""Samplers and the characteristic function of the standard symmetric p-stable law.

The standard symmetric p-stable law, for 0 < p <= 2, has characteristic
function E[exp(i t X)] = exp(-|t|^p). For p = 1 it is the standard Cauchy
law, and for p = 2 it is the normal law with mean 0 and variance 2.
"""

import math
import random


def char_function(p: float, t: float) -> float:
    """exp(-|t|^p), the characteristic function of the standard law."""
    return math.exp(-abs(t) ** p)


def cms_transform(p: float, theta: float, w: float) -> float:
    """The Chambers-Mallows-Stuck map for theta in (-pi/2, pi/2) and w > 0.

    If theta is uniform on (-pi/2, pi/2) and w is exponential with mean 1,
    the result has the standard symmetric p-stable law.
    """
    if p == 1:
        return math.tan(theta)
    return (
        math.sin(p * theta)
        / math.cos(theta) ** (1 / p)
        * (math.cos((1 - p) * theta) / w) ** ((1 - p) / p)
    )


def sample(p: float, rng: random.Random) -> float:
    """One draw from the standard symmetric p-stable law, 0 < p <= 2."""
    if not 0 < p <= 2:
        raise ValueError("p must be in (0, 2]")
    theta = math.pi * (rng.random() - 0.5)
    while theta == -math.pi / 2:
        theta = math.pi * (rng.random() - 0.5)
    w = rng.expovariate(1.0)
    while w == 0.0:
        w = rng.expovariate(1.0)
    return cms_transform(p, theta, w)


def sample_cauchy(rng: random.Random) -> float:
    """A standard Cauchy draw, tan of a uniform angle (the case p = 1)."""
    theta = math.pi * (rng.random() - 0.5)
    while theta == -math.pi / 2:
        theta = math.pi * (rng.random() - 0.5)
    return math.tan(theta)


def empirical_char_function(xs: list[float], t: float) -> float:
    """The mean of cos(t x); the sine part is 0 in expectation for a symmetric law."""
    return sum(math.cos(t * x) for x in xs) / len(xs)
