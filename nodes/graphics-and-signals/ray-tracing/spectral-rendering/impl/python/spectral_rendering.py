# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-rendering/. The authors are listed in prov/F2PT3X.jsonl.

"""Spectral rendering in miniature.

A spectrum is a function from a wavelength in nanometers to a nonnegative number. The module
turns spectra into CIE XYZ by quadrature or by Monte Carlo sampling of wavelengths, either one
wavelength per sample or a hero wavelength with C - 1 companions (Wilkie et al. 2014). It also
has the Cauchy dispersion formula and the refraction angle per wavelength.

The color matching functions are the multi-lobe fit of Wyman, Sloan and Shirley (2013) to the
CIE 1931 2 degree observer. It is within a few percent of the tabulated functions, which is
enough for the examples, and it needs no data table.
"""

import math
import random
from typing import Callable, List, Tuple

Spectrum = Callable[[float], float]
Vec3 = Tuple[float, float, float]

LAMBDA_MIN = 360.0
LAMBDA_MAX = 830.0

# Linear sRGB from XYZ, for the D65 white point of sRGB (IEC 61966-2-1).
_XYZ_TO_SRGB = (
    (3.2404542, -1.5371385, -0.4985314),
    (-0.9692660, 1.8760108, 0.0415560),
    (0.0556434, -0.2040259, 1.0572252),
)


def _lobe(lam: float, mu: float, s_left: float, s_right: float) -> float:
    t = (lam - mu) / (s_left if lam < mu else s_right)
    return math.exp(-0.5 * t * t)


def cmf_xyz(lam: float) -> Vec3:
    """The CIE 1931 color matching functions at the wavelength lam, in nanometers.

    Fit of Wyman, Sloan and Shirley (2013), a sum of piecewise Gaussians. Cost O(1).
    """
    x = (1.056 * _lobe(lam, 599.8, 37.9, 31.0)
         + 0.362 * _lobe(lam, 442.0, 16.0, 26.7)
         - 0.065 * _lobe(lam, 501.1, 20.4, 26.2))
    y = 0.821 * _lobe(lam, 568.8, 46.9, 40.5) + 0.286 * _lobe(lam, 530.9, 16.3, 31.1)
    z = 1.217 * _lobe(lam, 437.0, 11.8, 36.0) + 0.681 * _lobe(lam, 459.0, 26.0, 13.8)
    return (x, y, z)


def spectrum_to_xyz(s: Spectrum, m: int = 4700) -> Vec3:
    """Integral of s times the color matching functions over [LAMBDA_MIN, LAMBDA_MAX].

    Midpoint rule with m panels; m must be positive. Cost O(m) evaluations of s.
    """
    h = (LAMBDA_MAX - LAMBDA_MIN) / m
    sx = sy = sz = 0.0
    for i in range(m):
        lam = LAMBDA_MIN + (i + 0.5) * h
        v = s(lam)
        cx, cy, cz = cmf_xyz(lam)
        sx += cx * v
        sy += cy * v
        sz += cz * v
    return (sx * h, sy * h, sz * h)


def xyz_to_linear_srgb(c: Vec3) -> Vec3:
    """Linear sRGB of the XYZ color c. Values outside [0, 1] are out of gamut. Cost O(1)."""
    return tuple(sum(_XYZ_TO_SRGB[i][j] * c[j] for j in range(3)) for i in range(3))


def hero_wavelengths(u: float, count: int,
                     lo: float = LAMBDA_MIN, hi: float = LAMBDA_MAX) -> List[float]:
    """The hero wavelength for u in [0, 1) and its count - 1 companions.

    The hero is lo + u (hi - lo); companion j is the hero moved by j (hi - lo) / count, wrapped
    into [lo, hi). Each wavelength is uniform on [lo, hi) when u is. Cost O(count).
    """
    width = hi - lo
    hero = lo + u * width
    return [lo + ((hero - lo + j * width / count) % width) for j in range(count)]


def estimate_xyz(s: Spectrum, rng: random.Random, samples: int, count: int = 4) -> Vec3:
    """Monte Carlo estimate of spectrum_to_xyz(s) with hero wavelength sampling.

    Each of the samples draws one hero wavelength and uses count wavelengths in all; count = 1
    is plain single wavelength sampling. Every wavelength has the density 1 / (hi - lo), so the
    balance heuristic of multiple importance sampling gives each the weight 1 / count, and the
    estimate is unbiased. Requires samples >= 1 and count >= 1. Cost O(samples * count).
    """
    width = LAMBDA_MAX - LAMBDA_MIN
    sx = sy = sz = 0.0
    for _ in range(samples):
        for lam in hero_wavelengths(rng.random(), count):
            v = s(lam)
            cx, cy, cz = cmf_xyz(lam)
            sx += cx * v
            sy += cy * v
            sz += cz * v
    k = width / (samples * count)
    return (sx * k, sy * k, sz * k)


def cauchy_index(lam: float, a: float = 1.5046, b: float = 0.00420) -> float:
    """Cauchy's dispersion formula n = a + b / lambda^2, with lambda in micrometers.

    The defaults fit the crown glass BK7 in the visible range. lam is in nanometers, lam > 0.
    Cost O(1).
    """
    mu = lam / 1000.0
    return a + b / (mu * mu)


def refraction_angle(theta_i: float, n1: float, n2: float) -> float:
    """Angle of the refracted ray by Snell's law, in radians, or nan for total internal reflection.

    Requires 0 <= theta_i <= pi / 2 and positive indices. Cost O(1).
    """
    s = n1 * math.sin(theta_i) / n2
    if s > 1.0:
        return float("nan")
    return math.asin(s)
