# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smith-masking-shadowing-function/. The authors are listed in prov/0245JB.jsonl.

"""The Smith masking and shadowing functions for the GGX distribution.

Directions are in the local frame of the surface, with the normal as the
z axis. A cosine argument is n.w for a direction w. alpha is the parameter
of the GGX distribution itself.
"""

import math
import random

Vec = tuple[float, float, float]


def ggx_d(cos_m: float, alpha: float) -> float:
    """The GGX distribution, needed for the white furnace test."""
    if cos_m <= 0.0:
        return 0.0
    a2 = alpha * alpha
    t = cos_m * cos_m * (a2 - 1.0) + 1.0
    return a2 / (math.pi * t * t)


def lambda_ggx(cos_w: float, alpha: float) -> float:
    """Lambda(w) = (-1 + sqrt(1 + alpha^2 tan^2(theta))) / 2 for GGX."""
    if cos_w >= 1.0:
        return 0.0
    tan2 = (1.0 - cos_w * cos_w) / (cos_w * cos_w)
    return (-1.0 + math.sqrt(1.0 + alpha * alpha * tan2)) / 2.0


def g1(cos_w: float, alpha: float, cos_wm: float = 1.0) -> float:
    """G1(w, m) = chi(w.m) / (1 + Lambda(w)); cos_wm is w.m."""
    if cos_w <= 0.0 or cos_wm <= 0.0:
        return 0.0
    return 1.0 / (1.0 + lambda_ggx(cos_w, alpha))


def g2_separable(cos_l: float, cos_v: float, alpha: float) -> float:
    """G2 = G1(l) G1(v): masking and shadowing taken as independent."""
    return g1(cos_l, alpha) * g1(cos_v, alpha)


def g2_height_correlated(cos_l: float, cos_v: float, alpha: float) -> float:
    """G2 = 1 / (1 + Lambda(l) + Lambda(v)), Heitz 2014, Equation 99."""
    if cos_l <= 0.0 or cos_v <= 0.0:
        return 0.0
    return 1.0 / (1.0 + lambda_ggx(cos_l, alpha) + lambda_ggx(cos_v, alpha))


def g1_schlick_ggx(cos_w: float, k: float) -> float:
    """The fit n.w / ((n.w)(1 - k) + k); Karis 2013 uses k = alpha / 2."""
    if cos_w <= 0.0:
        return 0.0
    return cos_w / (cos_w * (1.0 - k) + k)


def sample_ggx_normal(rng: random.Random, alpha: float) -> Vec:
    """Sample m with the density D(m) (n.m)."""
    u = rng.random()
    phi = 2.0 * math.pi * rng.random()
    tan2 = alpha * alpha * u / (1.0 - u)
    c = 1.0 / math.sqrt(1.0 + tan2)
    s = math.sqrt(max(0.0, 1.0 - c * c))
    return (s * math.cos(phi), s * math.sin(phi), c)


def weak_furnace(theta_o: float, alpha: float, rng: random.Random, n: int) -> tuple[float, float]:
    """Monte Carlo estimate of the weak white furnace integral of Heitz 2014.

    The integral of G1(o, m) D(m) max(0, o.m) / (n.o) over all m is 1 for the
    Smith G1. With m sampled from D(m) (n.m), the weight is
    G1 max(0, o.m) / ((n.o)(n.m)). Returns the mean and its standard error.
    """
    o = (math.sin(theta_o), 0.0, math.cos(theta_o))
    vals = []
    for _ in range(n):
        m = sample_ggx_normal(rng, alpha)
        om = o[0] * m[0] + o[1] * m[1] + o[2] * m[2]
        w = g1(o[2], alpha, om) * max(0.0, om) / (o[2] * m[2])
        vals.append(w)
    mean = sum(vals) / n
    var = sum((x - mean) ** 2 for x in vals) / (n - 1)
    return mean, math.sqrt(var / n)
