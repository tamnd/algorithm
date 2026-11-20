# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/analog-monte-carlo-transport/. The authors are listed in prov/W64KF5.jsonl.
"""Analog Monte Carlo transport of one-speed particles in a slab.

The slab is 0 <= x <= L (L = math.inf gives an infinite medium with no faces), with a
total cross section sigma_t and a scattering cross section sigma_s, both
in cm^-1, and isotropic scattering. Both faces are vacuum: a particle that
leaves does not come back. Each history follows one particle with weight
1 and samples every event from its physical probability:

- the distance to the next collision, s = -ln(xi) / sigma_t;
- at a collision, absorption with probability sigma_a / sigma_t,
  else scattering to a new direction cosine mu = 2 xi - 1.

The run counts transmitted, reflected and absorbed particles and the
collisions per history. Each count is an unbiased estimate, with a
standard error from the sample variance.
"""

import math

TRANSMITTED, REFLECTED, ABSORBED = "transmitted", "reflected", "absorbed"


def uniform_open(rng) -> float:
    """A uniform number in (0, 1]."""
    return 1.0 - rng.random()


def analog_history(x: float, mu: float, length: float, sigma_t: float, sigma_s: float, rng, max_collisions: int = 10**7):
    """Follow one particle from (x, mu). Returns (event, number of collisions)."""
    p_abs = (sigma_t - sigma_s) / sigma_t
    has_faces = not math.isinf(length)  # L = inf: an infinite medium with no faces
    k = 0  # @line L1
    while k < max_collisions:  # @line L2
        s = -math.log(uniform_open(rng)) / sigma_t  # @line L3
        x += s * mu  # @line L4
        if x > length:  # @line L5
            return TRANSMITTED, k
        if x < 0.0 and has_faces:  # @line L6
            return REFLECTED, k
        k += 1  # @line L7
        if rng.random() < p_abs:  # @line L8
            return ABSORBED, k
        mu = 2.0 * rng.random() - 1.0  # @line L9
    raise RuntimeError("history did not end; is sigma_s = sigma_t in an infinite medium?")


def beam_source(length, rng):
    """A normally incident beam on the left face."""
    return 0.0, 1.0


def isotropic_volume_source(length, rng):
    """A uniform isotropic source inside a finite slab, or at x = 0 in an infinite medium.

    In an infinite medium every point is the same, so one point stands for a uniform source."""
    x = 0.0 if math.isinf(length) else length * rng.random()
    return x, 2.0 * rng.random() - 1.0


def analog_monte_carlo(n: int, length: float, sigma_t: float, sigma_s: float, rng, source=beam_source):
    """Run n histories. Returns a dict of estimates and standard errors."""
    counts = {TRANSMITTED: 0, REFLECTED: 0, ABSORBED: 0}
    k_sum = k_sq = 0
    k0_transmitted = 0
    for _ in range(n):  # @line L10
        x, mu = source(length, rng)
        event, k = analog_history(x, mu, length, sigma_t, sigma_s, rng)
        counts[event] += 1  # @line L11
        k_sum += k
        k_sq += k * k
        if event == TRANSMITTED and k == 0:
            k0_transmitted += 1
    out = {"n": n, "counts": counts}
    for ev, c in counts.items():  # @line L12
        p = c / n
        out[ev] = (p, math.sqrt(p * (1.0 - p) / (n - 1)) if n > 1 else 0.0)
    mean_k = k_sum / n
    var_k = (k_sq - n * mean_k * mean_k) / (n - 1) if n > 1 else 0.0
    out["collisions"] = (mean_k, math.sqrt(max(var_k, 0.0) / n))
    p0 = k0_transmitted / n
    out["uncollided"] = (p0, math.sqrt(p0 * (1.0 - p0) / (n - 1)) if n > 1 else 0.0)
    return out
