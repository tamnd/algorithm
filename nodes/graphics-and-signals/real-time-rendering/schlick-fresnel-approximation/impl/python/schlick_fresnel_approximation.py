# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schlick-fresnel-approximation/. The authors are listed in prov/W0ZH9M.jsonl.

"""Schlick's approximation of the Fresnel reflectance, and the exact Fresnel
equations that serve as its reference.

cos_i is the cosine of the angle between the incident direction and the
normal (for a microfacet BRDF, v.h). eta is the ratio n_t / n_i of the
refractive indices of the far side and the near side.
"""

import cmath
import math


def f0_from_ior(eta: float) -> float:
    """Reflectance at normal incidence, ((eta - 1) / (eta + 1))^2."""
    return ((eta - 1.0) / (eta + 1.0)) ** 2


def schlick(cos_i: float, f0: float, f90: float = 1.0) -> float:
    """F = f0 + (f90 - f0) (1 - cos_i)^5."""
    c = min(1.0, max(0.0, cos_i))  # @line L1
    m = 1.0 - c  # @line L2
    return f0 + (f90 - f0) * (m * m) * (m * m) * m  # @line L3


def schlick_dielectric(cos_i: float, eta: float) -> float:
    """Schlick for a dielectric on either side of the interface.

    When light leaves the denser medium (eta < 1), the cosine of the
    transmitted angle replaces cos_i, and past the critical angle the
    reflectance is 1 (total internal reflection).
    """
    f0 = f0_from_ior(eta)  # @line L4
    c = min(1.0, max(0.0, cos_i))
    if eta < 1.0:  # @line L5
        sin2_t = (1.0 - c * c) / (eta * eta)  # @line L6
        if sin2_t >= 1.0:  # @line L7
            return 1.0
        c = math.sqrt(1.0 - sin2_t)  # @line L8
    return schlick(c, f0)  # @line L9


def fresnel_dielectric(cos_i: float, eta: float) -> float:
    """Exact unpolarized Fresnel reflectance of a dielectric interface."""
    c = min(1.0, max(0.0, cos_i))
    sin2_t = (1.0 - c * c) / (eta * eta)
    if sin2_t >= 1.0:
        return 1.0
    ct = math.sqrt(1.0 - sin2_t)
    rs = (c - eta * ct) / (c + eta * ct)
    rp = (eta * c - ct) / (eta * c + ct)
    return 0.5 * (rs * rs + rp * rp)


def fresnel_conductor(cos_i: float, n: float, k: float) -> float:
    """Exact unpolarized Fresnel reflectance for the complex index n + i k,
    seen from a medium of index 1."""
    c = min(1.0, max(0.0, cos_i))
    eta = complex(n, k)
    s2 = 1.0 - c * c
    ct = cmath.sqrt(1.0 - s2 / (eta * eta))
    rs = (c - eta * ct) / (c + eta * ct)
    rp = (eta * c - ct) / (eta * c + ct)
    return 0.5 * (abs(rs) ** 2 + abs(rp) ** 2)


def f0_conductor(n: float, k: float) -> float:
    """((n - 1)^2 + k^2) / ((n + 1)^2 + k^2)."""
    return ((n - 1.0) ** 2 + k * k) / ((n + 1.0) ** 2 + k * k)
