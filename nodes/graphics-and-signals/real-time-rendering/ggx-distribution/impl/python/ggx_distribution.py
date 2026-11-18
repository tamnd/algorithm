# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ggx-distribution/. The authors are listed in prov/CCM8S7.jsonl.

"""The GGX (Trowbridge-Reitz) distribution of microfacet normals.

Directions are in the local frame of the surface: the normal n is the z
axis, and a unit vector h has cos(theta_h) = h[2]. alpha is the parameter of
the distribution itself, not a perceptual roughness. A renderer that exposes
a roughness r often sets alpha = r^2; that remap is a convention.
"""

import math
import random

Vec = tuple[float, float, float]


def ggx_d(cos_h: float, alpha: float) -> float:
    """D(h) = alpha^2 / (pi ((n.h)^2 (alpha^2 - 1) + 1)^2) for n.h > 0, else 0."""
    if cos_h <= 0.0:
        return 0.0
    a2 = alpha * alpha
    t = cos_h * cos_h * (a2 - 1.0) + 1.0
    return a2 / (math.pi * t * t)


def ggx_d_aniso(h: Vec, ax: float, ay: float) -> float:
    """The anisotropic form with alpha_x along the x axis and alpha_y along y."""
    if h[2] <= 0.0:
        return 0.0
    t = (h[0] / ax) ** 2 + (h[1] / ay) ** 2 + h[2] ** 2
    return 1.0 / (math.pi * ax * ay * t * t)


def ggx_d_slope(cos_h: float, alpha: float) -> float:
    """The same D written with the slope tan(theta_h), as in Walter et al. 2007."""
    if cos_h <= 0.0:
        return 0.0
    t2 = (1.0 - cos_h * cos_h) / (cos_h * cos_h)
    a2 = alpha * alpha
    return a2 / (math.pi * cos_h ** 4 * (a2 + t2) ** 2)


def beckmann_d(cos_h: float, alpha: float) -> float:
    """The Beckmann distribution, for comparison of the tails."""
    if cos_h <= 0.0:
        return 0.0
    t2 = (1.0 - cos_h * cos_h) / (cos_h * cos_h)
    return math.exp(-t2 / (alpha * alpha)) / (math.pi * alpha * alpha * cos_h ** 4)


def sample_ggx(rng: random.Random, alpha: float) -> Vec:
    """Sample h with the density D(h) (n.h) by inversion of its CDF.

    The CDF of theta_h is F = tan^2 / (alpha^2 + tan^2), so
    tan^2(theta_h) = alpha^2 u / (1 - u) for u uniform in [0, 1).
    """
    u = rng.random()
    phi = 2.0 * math.pi * rng.random()
    tan2 = alpha * alpha * u / (1.0 - u)
    cos_t = 1.0 / math.sqrt(1.0 + tan2)
    sin_t = math.sqrt(max(0.0, 1.0 - cos_t * cos_t))
    return (sin_t * math.cos(phi), sin_t * math.sin(phi), cos_t)


def cdf_theta(theta: float, alpha: float) -> float:
    """P(theta_h <= theta) for h drawn with the density D(h) (n.h)."""
    t2 = math.tan(theta) ** 2
    return t2 / (alpha * alpha + t2)
