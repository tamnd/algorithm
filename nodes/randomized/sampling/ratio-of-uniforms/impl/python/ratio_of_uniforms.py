# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ratio-of-uniforms/. The authors are listed in prov/3SHGH5.jsonl.

"""The ratio-of-uniforms method (Kinderman and Monahan, 1977).

For an integrable h >= 0, let C = {(u, v) : 0 < u <= sqrt(h(v / u))}. If
(U, V) is uniform on C, then X = V / U has density h / integral(h). C lies in
the box (0, a] x [bm, bp] with a = sup sqrt(h), bm = inf x sqrt(h(x)) and
bp = sup x sqrt(h(x)), so a uniform point in C comes from rejection from the
box. Exact for exact uniform reals and exact arithmetic.
"""

import math
import random
from typing import Callable, Tuple

SQRT_2_OVER_E = math.sqrt(2.0 / math.e)


def ratio_of_uniforms_counted(
    h: Callable[[float], float], a: float, bm: float, bp: float, rng: random.Random
) -> Tuple[float, int]:
    """Return (x, tries) with x drawn from the density proportional to h."""
    tries = 0
    while True:  # @line L1
        tries += 1
        u = a * (1.0 - rng.random())  # @line L2
        v = bm + (bp - bm) * rng.random()  # @line L2
        x = v / u  # @line L3
        if u * u <= h(x):  # @line L4
            return x, tries  # @line L5


def ratio_of_uniforms(h, a, bm, bp, rng) -> float:
    x, _ = ratio_of_uniforms_counted(h, a, bm, bp, rng)
    return x


def rou_normal_counted(rng: random.Random) -> Tuple[float, int]:
    """Standard normal: h(x) = exp(-x^2 / 2), a = 1, b = sqrt(2 / e).

    The test U^2 <= h(X) is written X^2 <= -4 ln U.
    """
    tries = 0
    while True:
        tries += 1
        u = 1.0 - rng.random()
        v = SQRT_2_OVER_E * (2.0 * rng.random() - 1.0)
        x = v / u
        if x * x <= -4.0 * math.log(u):
            return x, tries


def rou_normal(rng: random.Random) -> float:
    x, _ = rou_normal_counted(rng)
    return x


def rou_cauchy(rng: random.Random) -> float:
    """Standard Cauchy: h(x) = 1 / (1 + x^2). The region C is the half disk u^2 + v^2 <= 1."""
    while True:
        u = 1.0 - rng.random()
        v = 2.0 * rng.random() - 1.0
        if u * u + v * v <= 1.0:
            return v / u


def rou_exponential(rng: random.Random) -> float:
    """Standard exponential: h(x) = exp(-x) on x > 0, a = 1, bm = 0, bp = 2 / e."""
    return ratio_of_uniforms(
        lambda x: math.exp(-x) if x >= 0.0 else 0.0, 1.0, 0.0, 2.0 / math.e, rng
    )
