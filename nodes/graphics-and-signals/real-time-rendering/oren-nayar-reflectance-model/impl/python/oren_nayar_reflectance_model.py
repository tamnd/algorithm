# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oren-nayar-reflectance-model/. The authors are listed in prov/TGP977.jsonl.

"""The qualitative Oren-Nayar model of rough diffuse reflection.

sigma is the standard deviation of the facet slope angle, in radians. rho is
the albedo of each Lambertian facet. Angles are measured from the normal;
vectors point away from the surface.
"""

import math

Vec = tuple[float, float, float]


def coefficients(sigma: float) -> tuple[float, float]:
    """A = 1 - 0.5 s2 / (s2 + 0.33) and B = 0.45 s2 / (s2 + 0.09), s2 = sigma^2."""
    s2 = sigma * sigma
    return 1.0 - 0.5 * s2 / (s2 + 0.33), 0.45 * s2 / (s2 + 0.09)


def oren_nayar(theta_i: float, theta_r: float, cos_dphi: float, sigma: float, rho: float = 1.0) -> float:
    """The BRDF rho / pi (A + B max(0, cos dphi) sin(alpha) tan(beta)), in 1/sr.

    alpha = max(theta_i, theta_r), beta = min(theta_i, theta_r), and dphi is
    the difference of the azimuths of the two directions.
    """
    if theta_i >= math.pi / 2.0 or theta_r >= math.pi / 2.0:
        return 0.0
    a, b = coefficients(sigma)
    alpha = max(theta_i, theta_r)
    beta = min(theta_i, theta_r)
    return rho / math.pi * (a + b * max(0.0, cos_dphi) * math.sin(alpha) * math.tan(beta))


def dot(p: Vec, q: Vec) -> float:
    return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]


def oren_nayar_vectors(n: Vec, l: Vec, v: Vec, sigma: float, rho: float = 1.0) -> float:
    """The same BRDF from unit vectors, with no trigonometric calls but one sqrt.

    sin(alpha) tan(beta) = s_i s_r / max(c_i, c_r) for the sines s and cosines c,
    and cos dphi s_i s_r = l.v - c_i c_r.
    """
    ci, cr = dot(n, l), dot(n, v)
    if ci <= 0.0 or cr <= 0.0:
        return 0.0
    a, b = coefficients(sigma)
    g = dot(l, v) - ci * cr  # cos(dphi) sin(theta_i) sin(theta_r)
    return rho / math.pi * (a + b * max(0.0, g) / max(ci, cr))


def albedo(theta_i: float, sigma: float, rho: float = 1.0, nt: int = 600, npf: int = 64) -> float:
    """The directional albedo, the integral of f cos(theta_r) over the hemisphere."""
    total = 0.0
    dt = (math.pi / 2.0) / nt
    dp = math.pi / npf  # symmetric in dphi, so integrate over [0, pi] and double
    for i in range(nt):
        t = (i + 0.5) * dt
        w = math.cos(t) * math.sin(t)
        ring = 0.0
        for j in range(npf):
            p = (j + 0.5) * dp
            ring += oren_nayar(theta_i, t, math.cos(p), sigma, rho)
        total += ring * w
    return 2.0 * total * dt * dp


def sphere_lit_from_viewer(theta: float, sigma: float) -> float:
    """Radiance times pi / rho of a sphere point at angle theta, light at the eye.

    With l = v, theta_i = theta_r = theta and dphi = 0, so the value is
    cos(theta) (A + B sin(theta) tan(theta)) for unit irradiance at normal incidence.
    """
    a, b = coefficients(sigma)
    return math.cos(theta) * (a + b * math.sin(theta) * math.tan(theta))
