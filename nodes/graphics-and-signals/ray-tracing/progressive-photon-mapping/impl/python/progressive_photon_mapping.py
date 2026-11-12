# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/progressive-photon-mapping/. The authors are listed in prov/N56HR0.jsonl.

"""Progressive photon mapping (Hachisuka, Ogaki and Jensen 2008).

Pass 1 (the eye pass) stores hit points. Each later pass traces M photons, adds the
photons that land within the radius of each hit point, and then shrinks the radius so
that the photon density is kept while only a fraction alpha of the new photons is kept:

    N' = N + alpha M,   R'^2 = R^2 (N + alpha M) / (N + M),   tau' = (tau + phi_M) R'^2 / R^2.

The radiance estimate after N_e emitted photons is tau / (pi R^2 N_e), times the BRDF.

The test scene is a point light of power phi at height h over the absorbing plane z = 0.
The hit points lie on the plane and the code estimates the irradiance there.
"""

import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction


@dataclass
class HitPoint:
    x: float
    y: float
    radius2: float  # R^2
    n: float = 0.0  # N, the photon count that is kept (not always an integer)
    tau: float = 0.0  # the flux that is kept, scaled with the radius


def shrink(n: float, m: int, radius2: float, tau: float, phi_m: float, alpha: float) -> tuple[float, float, float]:
    """The update of one hit point after a pass with m photons of total power phi_m in its disc."""
    if m == 0:
        return n, radius2, tau
    n_new = n + alpha * m  # @line L8
    r2_new = radius2 * n_new / (n + m)  # @line L9
    tau_new = (tau + phi_m) * r2_new / radius2  # @line L10
    return n_new, r2_new, tau_new


def _photons(m: int, phi: float, height: float, rng: random.Random) -> list[tuple[float, float]]:
    """Hits on the plane of m photons emitted by the isotropic point light at (0, 0, height)."""
    hits = []
    for _ in range(m):
        z = 1.0 - 2.0 * rng.random()
        a = 2.0 * math.pi * rng.random()
        if z >= 0.0:
            continue
        s = math.sqrt(max(0.0, 1.0 - z * z))
        t = -height / z
        hits.append((t * s * math.cos(a), t * s * math.sin(a)))
    return hits


def progressive_photon_mapping(
    points: Sequence[tuple[float, float]],
    radius: float,
    passes: int,
    photons_per_pass: int,
    phi: float,
    height: float,
    rng: random.Random,
    alpha: float = 0.7,
) -> tuple[list[float], list[HitPoint]]:
    """Return the irradiance estimate at each hit point after the given number of passes."""
    hps = [HitPoint(px, py, radius * radius) for px, py in points]  # @line L1
    power = phi / photons_per_pass
    for _ in range(passes):  # @line L2
        # Hash grid over the hit points, with cells as large as the largest radius.
        cell = math.sqrt(max(h.radius2 for h in hps))  # @line L3
        grid: dict[tuple[int, int], list[int]] = {}
        for i, h in enumerate(hps):
            grid.setdefault((math.floor(h.x / cell), math.floor(h.y / cell)), []).append(i)
        count = [0] * len(hps)
        flux = [0.0] * len(hps)
        for qx, qy in _photons(photons_per_pass, phi, height, rng):  # @line L4
            cx, cy = math.floor(qx / cell), math.floor(qy / cell)
            for dx in (-1, 0, 1):  # @line L5
                for dy in (-1, 0, 1):
                    for i in grid.get((cx + dx, cy + dy), ()):
                        h = hps[i]
                        if (qx - h.x) ** 2 + (qy - h.y) ** 2 < h.radius2:  # @line L6
                            count[i] += 1
                            flux[i] += power
        for i, h in enumerate(hps):  # @line L7
            h.n, h.radius2, h.tau = shrink(h.n, count[i], h.radius2, h.tau, flux[i], alpha)
    # The tau of each pass is power with weight phi / photons_per_pass, so divide by the passes.
    estimates = [h.tau / (math.pi * h.radius2 * passes) for h in hps]  # @line L11
    return estimates, hps


def density_is_kept(n: Fraction, m: int, radius2: Fraction, alpha: Fraction) -> bool:
    """Exact check that the update keeps the density of the kept photons:
    (N + alpha M) / R'^2 == (N + M) / R^2."""
    n_new = n + alpha * m
    r2_new = radius2 * n_new / (n + m)
    return n_new / r2_new == (n + m) / radius2


def knaus_zwicker_radius2(r1_squared: float, i: int, alpha: float) -> float:
    """The radius sequence of probabilistic progressive photon mapping: r_{j+1}^2 = r_j^2 (j + alpha) / (j + 1)."""
    r2 = r1_squared
    for j in range(1, i):
        r2 *= (j + alpha) / (j + 1)
    return r2


def irradiance(phi: float, height: float, s: float) -> float:
    """The exact irradiance on the plane at distance s from the foot of the light."""
    return phi * height / (4.0 * math.pi * (height * height + s * s) ** 1.5)


def disc_average(phi: float, height: float, radius: float) -> float:
    """The mean irradiance over the disc about the foot of the light."""
    return phi / (2.0 * math.pi * radius * radius) * (1.0 - height / math.sqrt(height * height + radius * radius))
