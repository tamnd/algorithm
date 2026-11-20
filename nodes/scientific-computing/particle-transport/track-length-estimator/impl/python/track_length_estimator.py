# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/track-length-estimator/. The authors are listed in prov/QW4YNY.jsonl.
"""Track-length estimator of the scalar flux in a one-speed slab.

The slab is 0 <= x <= L with total and scattering cross sections sigma_t
and sigma_s (cm^-1) and isotropic scattering, cut into equal bins of
width dx. Each history follows one particle of weight 1 with analog Monte
Carlo. Every flight is a straight segment; the part of the segment that
lies in bin j has path length |overlap in x| / |mu|, and the history
scores w times that length into bin j. The estimate is

    phi_j = (sum of scores in bin j) / (N * dx),

the average flux over the bin per source particle. In one dimension the
bin "volume" is its width dx. The standard error comes from the variance
of the per-history scores.

The faces are "vacuum" or "reflect" (specular reflection). A flight that
reaches a vacuum face scores up to the face and ends the history.
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


def score_segment(a, b, mu, w, dx, nbins, hist):
    """Add w * (path length in bin j) for the x interval between a and b."""
    lo, hi = min(a, b), max(a, b)
    j = min(int(lo / dx), nbins - 1)
    while j < nbins and j * dx < hi:
        overlap = min(hi, (j + 1) * dx) - max(lo, j * dx)
        if overlap > 0.0:
            hist[j] = hist.get(j, 0.0) + w * overlap / abs(mu)
        j += 1


def fly(x, mu, s, length, faces, w, dx, nbins, hist):
    """Move a distance s and score every piece of the path. Returns (x, mu, inside)."""
    if mu == 0.0:  # a flight parallel to the faces stays in its bin
        j = min(int(x / dx), nbins - 1)
        hist[j] = hist.get(j, 0.0) + w * s
        return x, mu, True
    while True:
        face = length if mu > 0.0 else 0.0
        d = (face - x) / mu  # path length to the face
        if s <= d:
            x_new = x + s * mu
            score_segment(x, x_new, mu, w, dx, nbins, hist)
            return x_new, mu, True
        score_segment(x, face, mu, w, dx, nbins, hist)
        if faces == "vacuum":
            return face, mu, False
        s -= d
        x, mu = face, -mu


def track_length_estimator(n, length, sigma_t, sigma_s, nbins, rng, source=beam_source, faces="vacuum"):
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
            s = -math.log(uniform_open(rng)) / sigma_t  # @line L4
            x, mu, inside = fly(x, mu, s, length, faces, w, dx, nbins, hist)  # @line L5
            if not inside:  # @line L6
                break
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
