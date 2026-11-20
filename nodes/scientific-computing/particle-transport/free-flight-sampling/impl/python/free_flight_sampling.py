# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-flight-sampling/. The authors are listed in prov/21RHN1.jsonl.
"""Free-flight distance sampling for neutral particle transport.

In a uniform medium with total cross section sigma_t (in cm^-1), the
distance s to the next collision has the density sigma_t exp(-sigma_t s).
Inverse transform sampling gives s = -ln(xi) / sigma_t for xi uniform on
(0, 1].

In a slab made of regions with constant cross sections, the particle
draws one optical depth tau = -ln(xi) and spends it region by region: in
each region it either reaches the collision, or crosses the region and
subtracts the optical thickness of the part it crossed. This samples the
exact law P(S > s) = exp(-tau(s)), where tau(s) is the optical depth
along the path.
"""

import math


def uniform_open(rng) -> float:
    """A uniform number in (0, 1], so that its logarithm is finite."""
    return 1.0 - rng.random()


def sample_free_flight(sigma_t: float, rng) -> float:
    """Distance to the next collision in a uniform medium."""
    if sigma_t <= 0.0:
        return math.inf  # a void: the particle never collides
    xi = uniform_open(rng)  # @line L1
    return -math.log(xi) / sigma_t  # @line L2


def free_flight(x: float, mu: float, i: int, bounds: list[float], sigmas: list[float], xi: float):
    """Move a particle through a slab of regions to its next collision.

    The slab has regions 0, ..., M-1, region k is [bounds[k], bounds[k+1]]
    with total cross section sigmas[k]. The particle is at x in region i
    and moves with direction cosine mu. The number xi is uniform in (0, 1].

    Returns (x_new, i_new, event), where event is "collide" or "escape".
    On escape, i_new is -1 (left face) or M (right face) and x_new is
    the face.
    """
    m = len(sigmas)
    tau = -math.log(xi)  # @line L3
    while True:  # @line L4
        if mu > 0.0:  # @line L5
            d = (bounds[i + 1] - x) / mu
        elif mu < 0.0:
            d = (bounds[i] - x) / mu
        else:
            d = math.inf  # moves parallel to the faces
            if sigmas[i] <= 0.0:
                raise ValueError("a particle parallel to the faces of a void never collides")
        if sigmas[i] * d > tau:  # @line L6
            return x + mu * tau / sigmas[i], i, "collide"  # @line L7
        tau -= sigmas[i] * d  # @line L8
        if mu > 0.0:  # @line L9
            x, i = bounds[i + 1], i + 1
        else:
            x, i = bounds[i], i - 1
        if i < 0 or i >= m:  # @line L10
            return x, i, "escape"


def optical_depth(x0: float, x1: float, mu: float, bounds: list[float], sigmas: list[float]) -> float:
    """Optical depth along a straight path from x0 to x1 with direction cosine mu."""
    lo, hi = min(x0, x1), max(x0, x1)
    tau = 0.0
    for k, sig in enumerate(sigmas):
        a, b = max(lo, bounds[k]), min(hi, bounds[k + 1])
        if b > a:
            tau += sig * (b - a)
    return tau / abs(mu)


def region_of(x: float, bounds: list[float]) -> int:
    """Index k with bounds[k] <= x < bounds[k+1], for x inside the slab."""
    for k in range(len(bounds) - 1):
        if bounds[k] <= x < bounds[k + 1]:
            return k
    raise ValueError("x is outside the slab")
