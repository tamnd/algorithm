# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/microfacet-brdf/. The authors are listed in prov/TTFZZ6.jsonl.
"""The Cook-Torrance microfacet BRDF f = D F G / (4 cos(theta_i) cos(theta_o)).

D is the GGX (Trowbridge-Reitz) or the Beckmann distribution of facet normals, G is the Smith
masking-shadowing function (separable or height-correlated), and F is the exact Fresnel
reflectance of a dielectric. Directions are unit 3-tuples in the local frame with the normal on +z.
Each evaluation costs O(1). The random generator is a parameter.
"""

import math
import random
from typing import Callable, Optional, Tuple

Vec = Tuple[float, float, float]


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def normalize(v: Vec) -> Vec:
    s = math.sqrt(dot(v, v))
    return (v[0] / s, v[1] / s, v[2] / s)


def tan2(w: Vec) -> float:
    c2 = w[2] * w[2]
    return max(0.0, 1.0 - c2) / c2


def d_ggx(h: Vec, alpha: float) -> float:
    """GGX distribution: alpha^2 / (pi ((n.h)^2 (alpha^2 - 1) + 1)^2) for n.h > 0, else 0."""
    c = h[2]
    if c <= 0.0:
        return 0.0
    a2 = alpha * alpha
    t = c * c * (a2 - 1.0) + 1.0
    return a2 / (math.pi * t * t)


def d_beckmann(h: Vec, alpha: float) -> float:
    """Beckmann distribution: exp(-tan^2 / alpha^2) / (pi alpha^2 cos^4) for n.h > 0, else 0."""
    c = h[2]
    if c <= 0.0:
        return 0.0
    return math.exp(-tan2(h) / (alpha * alpha)) / (math.pi * alpha * alpha * c ** 4)


def lambda_ggx(w: Vec, alpha: float) -> float:
    """Smith Lambda of GGX: (sqrt(1 + alpha^2 tan^2(theta)) - 1) / 2."""
    return 0.5 * (math.sqrt(1.0 + alpha * alpha * tan2(w)) - 1.0)


def g1_ggx(w: Vec, h: Vec, alpha: float) -> float:
    """Smith masking of one direction, 1 / (1 + Lambda), zero on the back of the facet."""
    if dot(w, h) <= 0.0 or w[2] <= 0.0:
        return 0.0
    return 1.0 / (1.0 + lambda_ggx(w, alpha))


def g2_ggx(wi: Vec, wo: Vec, h: Vec, alpha: float, correlated: bool = True) -> float:
    """Masking-shadowing: height-correlated 1 / (1 + L(i) + L(o)), or separable G1(i) G1(o)."""
    if dot(wi, h) <= 0.0 or dot(wo, h) <= 0.0 or wi[2] <= 0.0 or wo[2] <= 0.0:
        return 0.0
    if correlated:
        return 1.0 / (1.0 + lambda_ggx(wi, alpha) + lambda_ggx(wo, alpha))
    return g1_ggx(wi, h, alpha) * g1_ggx(wo, h, alpha)


def fresnel_dielectric(cos_i: float, eta: float) -> float:
    """Unpolarized Fresnel reflectance from air into a dielectric of index eta, for 0 <= cos_i <= 1."""
    s2 = (1.0 - cos_i * cos_i) / (eta * eta)
    ct = math.sqrt(max(0.0, 1.0 - s2))
    rs = (cos_i - eta * ct) / (cos_i + eta * ct)
    rp = (eta * cos_i - ct) / (eta * cos_i + ct)
    return 0.5 * (rs * rs + rp * rp)


def cook_torrance(wi: Vec, wo: Vec, alpha: float, eta: Optional[float] = 1.5,
                  correlated: bool = True) -> float:
    """The microfacet BRDF value for the GGX distribution.

    eta is the index of the dielectric; eta=None sets F = 1, a perfect reflector, which is
    the case for the energy test. Precondition: alpha > 0.
    """
    if wi[2] <= 0.0 or wo[2] <= 0.0:
        return 0.0
    h = normalize((wi[0] + wo[0], wi[1] + wo[1], wi[2] + wo[2]))
    f = 1.0 if eta is None else fresnel_dielectric(dot(wi, h), eta)
    return d_ggx(h, alpha) * f * g2_ggx(wi, wo, h, alpha, correlated) / (4.0 * wi[2] * wo[2])


def sample_ggx_normal(rng: random.Random, alpha: float) -> Vec:
    """Draw a facet normal with the density D(h) cos(theta_h) (Walter et al. 2007).

    tan^2(theta_h) = alpha^2 u / (1 - u) inverts the distribution function u of theta_h.
    """
    u, v = rng.random(), rng.random()
    t2 = alpha * alpha * u / (1.0 - u)
    c = 1.0 / math.sqrt(1.0 + t2)
    s = math.sqrt(max(0.0, 1.0 - c * c))
    phi = 2.0 * math.pi * v
    return (s * math.cos(phi), s * math.sin(phi), c)


def reflect(w: Vec, h: Vec) -> Vec:
    k = 2.0 * dot(w, h)
    return (k * h[0] - w[0], k * h[1] - w[1], k * h[2] - w[2])


def albedo_monte_carlo(wo: Vec, alpha: float, n: int, rng: random.Random,
                       eta: Optional[float] = None) -> Tuple[float, float]:
    """Estimate the directional albedo by sampling h with D cos and reflecting wo about it.

    The density of wi is D(h) cos(theta_h) / (4 |wo . h|). The estimator f cos / p is unbiased.
    Returns the mean and its standard error. Precondition: n >= 2 and wo[2] > 0.
    """
    s = s2 = 0.0
    for _ in range(n):
        h = sample_ggx_normal(rng, alpha)
        wi = reflect(wo, h)
        x = 0.0
        if wi[2] > 0.0 and dot(wo, h) > 0.0:
            pdf = d_ggx(h, alpha) * h[2] / (4.0 * dot(wo, h))
            x = cook_torrance(wi, wo, alpha, eta) * wi[2] / pdf
        s += x
        s2 += x * x
    mean = s / n
    var = max(0.0, (s2 - n * mean * mean) / (n - 1))
    return mean, math.sqrt(var / n)


def gauss_legendre(m: int, a: float, b: float) -> Tuple[list, list]:
    """Nodes and weights of the m-point Gauss-Legendre rule on [a, b], by Newton's method."""
    xs, ws = [], []
    for i in range(1, m + 1):
        x = math.cos(math.pi * (i - 0.25) / (m + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for j in range(2, m + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = m * (x * p1 - p0) / (x * x - 1.0)
            step = p1 / dp
            x -= step
            if abs(step) < 1e-15:
                break
        p0, p1 = 1.0, x
        for j in range(2, m + 1):
            p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
        dp = m * (x * p1 - p0) / (x * x - 1.0)
        xs.append(0.5 * (b - a) * x + 0.5 * (a + b))
        ws.append((b - a) / ((1.0 - x * x) * dp * dp))
    return xs, ws


def hemisphere_integral(g: Callable[[Vec], float], m: int = 200, k: int = 200) -> float:
    """The integral of g over the upper hemisphere: Gauss-Legendre in theta, midpoint in phi."""
    ts, ws = gauss_legendre(m, 0.0, 0.5 * math.pi)
    dp = 2.0 * math.pi / k
    total = 0.0
    for th, w in zip(ts, ws):
        st, ct = math.sin(th), math.cos(th)
        row = 0.0
        for j in range(k):
            ph = (j + 0.5) * dp
            row += g((st * math.cos(ph), st * math.sin(ph), ct))
        total += w * st * row
    return total * dp


def albedo_quadrature(wo: Vec, alpha: float, eta: Optional[float] = None,
                      correlated: bool = True, m: int = 200, k: int = 200) -> float:
    """Directional albedo, the integral of f(wi, wo) cos(theta_i) over the hemisphere."""
    return hemisphere_integral(lambda wi: cook_torrance(wi, wo, alpha, eta, correlated) * wi[2], m, k)
