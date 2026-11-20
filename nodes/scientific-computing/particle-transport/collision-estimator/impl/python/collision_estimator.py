# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-estimator/. The authors are listed in prov/NDP0HX.jsonl.
"""Collision estimator of the scalar flux in a one-speed slab.

The slab is 0 <= x <= L with total and scattering cross sections sigma_t
and sigma_s (cm^-1) and isotropic scattering. It is cut into equal bins of
width dx. Each history starts one particle of weight 1 from a source and
follows it with analog Monte Carlo. At each collision in bin j the history
scores w / sigma_t into bin j. The flux estimate in bin j is

    phi_j = (sum of scores in bin j) / (N * dx),

which is the average flux over the bin per source particle. The standard
error comes from the variance of the per-history scores, because the
collisions inside one history are not independent.

The faces are "vacuum" (a particle that leaves is lost) or "reflect"
(specular reflection). A reflecting slab with a uniform source behaves
as an infinite medium.
"""

import math


def uniform_open(rng) -> float:
    return 1.0 - rng.random()


def beam_source(length, rng):
    """A normally incident beam on the left face."""
    return 0.0, 1.0


def uniform_isotropic_source(length, rng):
    """A source uniform in x on [0, L] and isotropic in direction."""
    return length * rng.random(), 2.0 * rng.random() - 1.0


def move(x, mu, s, length, faces):
    """Move a distance s from x along mu. Returns (x, mu, inside)."""
    x += s * mu
    if faces == "vacuum":
        return x, mu, 0.0 <= x <= length
    while x < 0.0 or x > length:  # unfold the path by mirror reflection
        if x < 0.0:
            x = -x
        else:
            x = 2.0 * length - x
        mu = -mu
    return x, mu, True


def collision_estimator(n, length, sigma_t, sigma_s, nbins, rng, source=beam_source, faces="vacuum"):
    """Returns (phi, se): flux per source particle in each bin, and its standard error."""
    dx = length / nbins
    p_abs = (sigma_t - sigma_s) / sigma_t
    total = [0.0] * nbins
    total_sq = [0.0] * nbins
    for _ in range(n):  # @line L1
        x, mu = source(length, rng)  # @line L2
        w = 1.0
        hist = {}
        while True:  # @line L3
            s = -math.log(uniform_open(rng)) / sigma_t
            x, mu, inside = move(x, mu, s, length, faces)
            if not inside:  # @line L4
                break
            j = min(int(x / dx), nbins - 1)  # @line L5
            hist[j] = hist.get(j, 0.0) + w / sigma_t  # @line L6
            if rng.random() < p_abs:  # @line L7
                break
            mu = 2.0 * rng.random() - 1.0  # @line L8
        for j, v in hist.items():  # @line L9
            total[j] += v
            total_sq[j] += v * v
    phi, se = [], []
    for j in range(nbins):  # @line L10
        mean = total[j] / n
        var = (total_sq[j] / n - mean * mean) * n / (n - 1)
        phi.append(mean / dx)
        se.append(math.sqrt(max(var, 0.0) / n) / dx)
    return phi, se
