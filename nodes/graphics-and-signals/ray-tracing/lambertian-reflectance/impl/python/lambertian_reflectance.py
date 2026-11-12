# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambertian-reflectance/. The authors are listed in prov/K8919H.jsonl.
"""The Lambertian BRDF f = rho / pi, cosine-weighted hemisphere sampling, and albedo estimates.

Directions are unit 3-tuples in the local frame of the surface, with the normal on the +z axis.
The BRDF costs O(1). The quadrature costs O(m k) for an m by k grid; the Monte Carlo estimate
costs O(N) for N samples. The random generator is a parameter, so runs repeat with a seed.
"""

import math
import random
from typing import Callable, Tuple

Vec = Tuple[float, float, float]
Brdf = Callable[[Vec, Vec], float]


def lambert(rho: float) -> Brdf:
    """Return the BRDF of a Lambertian surface with albedo rho, 0 <= rho <= 1."""
    value = rho / math.pi

    def f(wi: Vec, wo: Vec) -> float:
        if wi[2] <= 0.0 or wo[2] <= 0.0:
            return 0.0
        return value

    return f


def sample_cosine(rng: random.Random) -> Vec:
    """Draw a direction with the density cos(theta) / pi on the upper hemisphere (Malley's method).

    A point uniform on the unit disk, lifted to the hemisphere, has this density.
    """
    u1, u2 = rng.random(), rng.random()
    r = math.sqrt(u1)
    phi = 2.0 * math.pi * u2
    return (r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1.0 - u1)))


def sample_uniform(rng: random.Random) -> Vec:
    """Draw a direction with the density 1 / (2 pi) on the upper hemisphere."""
    z = rng.random()
    r = math.sqrt(max(0.0, 1.0 - z * z))
    phi = 2.0 * math.pi * rng.random()
    return (r * math.cos(phi), r * math.sin(phi), z)


def gauss_legendre(m: int) -> Tuple[list, list]:
    """Nodes and weights of the m-point Gauss-Legendre rule on [0, 1], by Newton's method."""
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
            if abs(step) < 1e-16:
                break
        p0, p1 = 1.0, x
        for j in range(2, m + 1):
            p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
        dp = m * (x * p1 - p0) / (x * x - 1.0)
        xs.append(0.5 * (x + 1.0))
        ws.append(1.0 / ((1.0 - x * x) * dp * dp))
    return xs, ws


def albedo_quadrature(f: Brdf, wo: Vec, m: int = 64, k: int = 64) -> float:
    """Directional albedo: the integral of f(wi, wo) cos(theta_i) over the hemisphere.

    In the variables mu = cos(theta_i) and phi the integral is the integral of f mu dmu dphi.
    The rule is m-point Gauss-Legendre in mu and the k-point midpoint rule in phi.
    """
    xs, ws = gauss_legendre(m)
    dp = 2.0 * math.pi / k
    total = 0.0
    for mu, w in zip(xs, ws):
        s = math.sqrt(max(0.0, 1.0 - mu * mu))
        row = 0.0
        for j in range(k):
            ph = (j + 0.5) * dp
            row += f((s * math.cos(ph), s * math.sin(ph), mu), wo)
        total += w * mu * row
    return total * dp


def albedo_monte_carlo(f: Brdf, wo: Vec, n: int, rng: random.Random,
                       cosine: bool = True) -> Tuple[float, float]:
    """Monte Carlo estimate of the directional albedo, and its standard error.

    Each sample is f cos(theta) / p for a direction drawn with the density p, either cos / pi
    (cosine=True) or 1 / (2 pi). The estimator is unbiased. Precondition: n >= 2.
    """
    s = s2 = 0.0
    for _ in range(n):
        if cosine:
            wi = sample_cosine(rng)
            pdf = wi[2] / math.pi
        else:
            wi = sample_uniform(rng)
            pdf = 1.0 / (2.0 * math.pi)
        x = f(wi, wo) * wi[2] / pdf if pdf > 0.0 else 0.0
        s += x
        s2 += x * x
    mean = s / n
    var = max(0.0, (s2 - n * mean * mean) / (n - 1))
    return mean, math.sqrt(var / n)


def radiance_point_light(rho: float, intensity: float, distance: float, cos_i: float) -> float:
    """Outgoing radiance of a Lambertian point lit by a point light: (rho / pi) I cos / d^2."""
    return rho / math.pi * intensity * max(0.0, cos_i) / (distance * distance)
