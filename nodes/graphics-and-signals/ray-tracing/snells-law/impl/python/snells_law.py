# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snells-law/. The authors are listed in prov/DYEFKR.jsonl.
"""Snell's law of refraction, n1 sin(theta1) = n2 sin(theta2), in angle form and vector form.

Directions are unit 3-tuples of float. The normal points to the side of the incident ray.
Every function costs O(1) time and O(1) extra space.
"""

import math
from typing import Optional, Tuple

Vec = Tuple[float, float, float]


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def refracted_angle(n1: float, n2: float, theta1: float) -> Optional[float]:
    """Return theta2 in radians with n1 sin(theta1) = n2 sin(theta2), or None for total internal reflection.

    Precondition: n1 > 0, n2 > 0 and 0 <= theta1 <= pi / 2.
    """
    s = n1 * math.sin(theta1) / n2
    if s > 1.0:
        return None
    return math.asin(s)


def critical_angle(n1: float, n2: float) -> Optional[float]:
    """Return the critical angle asin(n2 / n1) for light going from n1 into n2, or None if n1 <= n2."""
    if n1 <= n2:
        return None
    return math.asin(n2 / n1)


def refract(d: Vec, n: Vec, eta: float) -> Optional[Vec]:
    """Return the unit refracted direction t, or None for total internal reflection.

    Precondition: d and n are unit vectors with dot(n, d) <= 0, so n points to the incident side,
    and eta = n1 / n2 is the ratio of the index on the incident side to the index on the far side.
    The result is t = eta d + (eta c - sqrt(k)) n with c = -dot(n, d) and k = 1 - eta^2 (1 - c^2).
    """
    c = -dot(n, d)
    k = 1.0 - eta * eta * (1.0 - c * c)
    if k < 0.0:
        return None
    a = eta * c - math.sqrt(k)
    return (eta * d[0] + a * n[0], eta * d[1] + a * n[1], eta * d[2] + a * n[2])


def refract_at_surface(d: Vec, n: Vec, n_outside: float, n_inside: float) -> Optional[Vec]:
    """Refract d at a surface with the outward unit normal n, for a ray from either side.

    If dot(n, d) < 0 the ray comes from outside; otherwise it comes from inside, and the
    function flips the normal and swaps the two indices before it calls refract.
    """
    if dot(n, d) < 0.0:
        return refract(d, n, n_outside / n_inside)
    return refract(d, (-n[0], -n[1], -n[2]), n_inside / n_outside)
