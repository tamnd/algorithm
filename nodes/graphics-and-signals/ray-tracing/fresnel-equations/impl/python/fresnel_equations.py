# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fresnel-equations/. The authors are listed in prov/S05FMF.jsonl.
"""Fresnel equations for a smooth boundary between two dielectrics, and Schlick's approximation.

Amplitude coefficients use the convention of Born and Wolf for the s (TE) and p (TM) waves:
  rs = (n1 c1 - n2 c2) / (n1 c1 + n2 c2),  ts = 2 n1 c1 / (n1 c1 + n2 c2),
  rp = (n2 c1 - n1 c2) / (n2 c1 + n1 c2),  tp = 2 n1 c1 / (n2 c1 + n1 c2),
with c1 = cos(theta1) and c2 = cos(theta2) from Snell's law. Every function costs O(1).
"""

import math
from typing import NamedTuple, Optional


class Fresnel(NamedTuple):
    rs: float
    rp: float
    ts: float
    tp: float
    Rs: float
    Rp: float
    Ts: float
    Tp: float


def cos_transmitted(n1: float, n2: float, cos1: float) -> Optional[float]:
    """Return cos(theta2) by Snell's law, or None for total internal reflection."""
    k = 1.0 - (n1 / n2) ** 2 * (1.0 - cos1 * cos1)
    if k < 0.0:
        return None
    return math.sqrt(k)


def fresnel(n1: float, n2: float, cos1: float) -> Fresnel:
    """Amplitude and power coefficients for light from index n1 into index n2.

    Precondition: n1 > 0, n2 > 0 and 0 <= cos1 <= 1. Under total internal reflection the
    reflectances are 1 and the transmittances are 0 (the reflected amplitudes are then complex
    with modulus 1, and the function returns rs = rp = 1 as their modulus).
    """
    cos2 = cos_transmitted(n1, n2, cos1)
    if cos2 is None:
        return Fresnel(1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0)
    a, b = n1 * cos1, n2 * cos2
    p, q = n2 * cos1, n1 * cos2
    rs = (a - b) / (a + b)
    rp = (p - q) / (p + q)
    ts = 2.0 * a / (a + b)
    tp = 2.0 * a / (p + q)
    # Transmittance is a ratio of powers: the beam changes its cross section and the wave its speed.
    f = b / a if a > 0.0 else 0.0
    return Fresnel(rs, rp, ts, tp, rs * rs, rp * rp, f * ts * ts, f * tp * tp)


def reflectance(n1: float, n2: float, cos1: float) -> float:
    """Reflectance of unpolarized light, (Rs + Rp) / 2."""
    f = fresnel(n1, n2, cos1)
    return 0.5 * (f.Rs + f.Rp)


def schlick(n1: float, n2: float, cos1: float) -> float:
    """Schlick's approximation R0 + (1 - R0) (1 - c)^5 with R0 = ((n1 - n2) / (n1 + n2))^2.

    For n1 > n2 the cosine c is the cosine on the side of the smaller index, cos(theta2), and the
    function returns 1 under total internal reflection. For n1 <= n2, c = cos1.
    """
    r0 = ((n1 - n2) / (n1 + n2)) ** 2
    c = cos1
    if n1 > n2:
        c2 = cos_transmitted(n1, n2, cos1)
        if c2 is None:
            return 1.0
        c = c2
    return r0 + (1.0 - r0) * (1.0 - c) ** 5
