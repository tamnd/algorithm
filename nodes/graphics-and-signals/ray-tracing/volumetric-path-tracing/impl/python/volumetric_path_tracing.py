# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volumetric-path-tracing/. The authors are listed in prov/C7K88C.jsonl.

"""Volumetric path tracing in a plane-parallel slab.

The slab holds a medium for depths 0 <= z <= Z (z grows downward). The extinction
sigma_t(z) can vary with depth, the single-scattering albedo omega is constant, and
the phase function is isotropic. A directional light with irradiance E (on a plane
normal to the beam) shines down into the slab with direction cosine mu0. Below the
slab and above it there is vacuum and nothing reflects.

volumetric_path_trace returns one sample of the radiance that leaves the top of the
slab upward with direction cosine mu. Free flights are sampled by delta tracking,
the light is sampled at each real collision (next event estimation), and the
transmittance to the light is estimated by ratio tracking.
"""

import math
import random
from collections.abc import Callable

Sigma = Callable[[float], float]
INV_4PI = 1.0 / (4.0 * math.pi)


def _segment_length(z: float, c: float, depth: float) -> float:
    """Length of the ray from depth z with direction cosine c (positive is downward) inside the slab."""
    if c > 0.0:
        return (depth - z) / c
    if c < 0.0:
        return z / (-c)
    return math.inf


def delta_track(sigma_t: Sigma, majorant: float, z: float, c: float, depth: float, rng: random.Random) -> float | None:
    """Free-flight distance along the ray from depth z with cosine c, or None if it leaves the slab."""
    t_max = _segment_length(z, c, depth)
    t = 0.0
    while True:
        t -= math.log(1.0 - rng.random()) / majorant
        if t >= t_max:
            return None
        if rng.random() * majorant < sigma_t(z + c * t):
            return t


def ratio_track(sigma_t: Sigma, majorant: float, z: float, c: float, depth: float, rng: random.Random) -> float:
    """Unbiased estimate of the transmittance from depth z to the slab boundary along cosine c."""
    t_max = _segment_length(z, c, depth)
    t = 0.0
    w = 1.0
    while True:
        t -= math.log(1.0 - rng.random()) / majorant
        if t >= t_max:
            return w
        w *= 1.0 - sigma_t(z + c * t) / majorant


def volumetric_path_trace(
    sigma_t: Sigma,
    majorant: float,
    depth: float,
    omega: float,
    irradiance: float,
    mu0: float,
    mu: float,
    rng: random.Random,
    max_bounces: int = 1000,
    roulette_after: int = 5,
) -> float:
    """One sample of the radiance leaving the top of the slab with cosine mu (0 < mu <= 1).

    max_bounces = 1 gives single scattering only.
    """
    z, c = 0.0, mu  # the camera ray enters at the top, going down
    throughput, radiance = 1.0, 0.0  # @line L1
    for bounce in range(1, max_bounces + 1):  # @line L2
        t = delta_track(sigma_t, majorant, z, c, depth, rng)  # @line L3
        if t is None:  # @line L4
            break  # the path leaves the slab; nothing is emitted or reflected there
        z += c * t  # @line L5
        throughput *= omega  # @line L6
        # Next event estimation toward the directional light (direction cosine -mu0, upward).
        tr = ratio_track(sigma_t, majorant, z, -mu0, depth, rng)
        radiance += throughput * INV_4PI * irradiance * tr  # @line L7
        c = 1.0 - 2.0 * rng.random()  # @line L8
        if bounce >= roulette_after:  # @line L9
            q = min(1.0, throughput)
            if rng.random() >= q:
                break
            throughput /= q
    return radiance  # @line L10


def render(sigma_t: Sigma, majorant: float, depth: float, omega: float, irradiance: float, mu0: float, mu: float, n: int, rng: random.Random, max_bounces: int = 1000) -> tuple[float, float]:
    """Mean of n samples and its standard error."""
    s = s2 = 0.0
    for _ in range(n):
        x = volumetric_path_trace(sigma_t, majorant, depth, omega, irradiance, mu0, mu, rng, max_bounces)
        s += x
        s2 += x * x
    mean = s / n
    var = max(s2 / n - mean * mean, 0.0) * n / (n - 1)
    return mean, math.sqrt(var / n)


# Reference answers.


def single_scattering(omega: float, irradiance: float, mu0: float, mu: float, tau: float) -> float:
    """Exact single-scattered radiance from a slab of total optical depth tau with constant albedo."""
    return omega * irradiance * INV_4PI * mu0 / (mu0 + mu) * (1.0 - math.exp(-tau * (1.0 / mu0 + 1.0 / mu)))


def gauss_legendre(n: int) -> tuple[list[float], list[float]]:
    """Nodes and weights of n-point Gauss-Legendre quadrature on [0, 1]."""
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        xs.append(0.5 * (1.0 - x))
        ws.append(1.0 / ((1.0 - x * x) * dp * dp))  # 2 / ((1 - x^2) P'^2), halved for [0, 1]
    return xs, ws


def chandrasekhar_h(omega: float, n: int = 64, iterations: int = 2000) -> Callable[[float], float]:
    """Chandrasekhar's H-function for isotropic scattering with albedo omega.

    It solves H(m) = 1 + (omega/2) m H(m) integral_0^1 H(m') / (m + m') dm'. The iteration
    uses the equivalent form 1/H(m) = sqrt(1 - omega) + (omega/2) integral_0^1 m' H(m') / (m + m') dm',
    which converges faster, and Gauss-Legendre quadrature for the integral.
    """
    if not 0.0 <= omega < 1.0:
        raise ValueError("this iteration needs 0 <= omega < 1")
    xs, ws = gauss_legendre(n)
    root = math.sqrt(1.0 - omega)
    h = [1.0] * n
    for _ in range(iterations):
        new = [1.0 / (root + 0.5 * omega * sum(w * xj * hj / (x + xj) for xj, w, hj in zip(xs, ws, h))) for x in xs]
        done = max(abs(a - b) for a, b in zip(new, h)) < 1e-14
        h = new
        if done:
            break

    def H(m: float) -> float:
        return 1.0 / (root + 0.5 * omega * sum(w * xj * hj / (m + xj) for xj, w, hj in zip(xs, ws, h)))

    return H


def semi_infinite_reflection(omega: float, irradiance: float, mu0: float, mu: float) -> float:
    """Exact radiance (all orders of scattering) reflected by a semi-infinite isotropic medium."""
    H = chandrasekhar_h(omega)
    return omega * irradiance * INV_4PI * mu0 / (mu0 + mu) * H(mu) * H(mu0)
