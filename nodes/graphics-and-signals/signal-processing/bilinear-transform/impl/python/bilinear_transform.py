# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-transform/. The authors are listed in prov/CV28SZ.jsonl.

"""The bilinear transform s = (2/T)(1 - z^-1)/(1 + z^-1) from analog to digital filters.

Analog frequencies W are in radians per second, digital frequencies w in
radians per sample. An analog filter is H(s) = B(s)/A(s) with coefficient
lists in ascending powers of s. A digital filter is B(z)/A(z) with coefficient
lists in ascending powers of z^-1, normalized so that a[0] = 1.
"""

import cmath
import math
from typing import Sequence


def s_to_z(s: complex, t: float) -> complex:
    """The image z = (1 + s T/2) / (1 - s T/2) of a point s."""
    return (1 + s * t / 2) / (1 - s * t / 2)


def z_to_s(z: complex, t: float) -> complex:
    """The inverse map s = (2/T)(z - 1)/(z + 1)."""
    return (2 / t) * (z - 1) / (z + 1)


def warp(w: float, t: float) -> float:
    """The analog frequency (2/T) tan(w/2) that lands on the digital frequency w."""
    return (2 / t) * math.tan(w / 2)


def unwarp(big_w: float, t: float) -> float:
    """The digital frequency 2 arctan(W T / 2) where the analog frequency W lands."""
    return 2 * math.atan(big_w * t / 2)


def _poly_mul(p: list, q: list) -> list:
    r = [0] * (len(p) + len(q) - 1)
    for i, u in enumerate(p):
        for j, v in enumerate(q):
            r[i + j] += u * v
    return r


def _poly_pow(p: list, e: int) -> list:
    r = [1]
    for _ in range(e):
        r = _poly_mul(r, p)
    return r


def bilinear(b: Sequence, a: Sequence, t) -> tuple[list, list]:
    """Substitute s = (2/T)(1 - z^-1)/(1 + z^-1) into B(s)/A(s).

    Both sides are multiplied by (1 + z^-1)^n with n = max(deg B, deg A), which
    gives polynomials in z^-1. With Fraction input the result is exact.
    """
    n = max(len(a), len(b)) - 1
    k = 2 / t
    minus = [1, -1]  # 1 - z^-1
    plus = [1, 1]  # 1 + z^-1

    def substitute(c: Sequence) -> list:
        out = [0] * (n + 1)
        for j, cj in enumerate(c):  # @line L1
            term = _poly_mul(_poly_pow(minus, j), _poly_pow(plus, n - j))  # @line L2
            for i, v in enumerate(term):
                out[i] += cj * k ** j * v  # @line L3
        return out

    bz = substitute(b)
    az = substitute(a)
    a0 = az[0]  # @line L4
    if a0 == 0:
        raise ValueError("A(s) has a pole at s = 2/T, which maps to z = infinity")
    return [v / a0 for v in bz], [v / a0 for v in az]  # @line L5


def digital_response(b: Sequence, a: Sequence, w: float) -> complex:
    z1 = cmath.exp(-1j * w)
    num = sum(complex(v) * z1 ** i for i, v in enumerate(b))
    den = sum(complex(v) * z1 ** i for i, v in enumerate(a))
    return num / den


def analog_response(b: Sequence, a: Sequence, big_w: float) -> complex:
    s = 1j * big_w
    num = sum(complex(v) * s ** i for i, v in enumerate(b))
    den = sum(complex(v) * s ** i for i, v in enumerate(a))
    return num / den


def butterworth_lowpass(order: int, wc: float) -> tuple[list, list]:
    """A digital Butterworth low-pass filter with half power at wc (radians per sample).

    Prewarp wc to the analog cutoff (2/T) tan(wc/2). Once the cutoff is
    prewarped, every T gives the same digital filter, so T = 1 is used. Each
    analog pole maps to a digital pole, and the N zeros at s = infinity map
    to z = -1.
    """
    t = 1.0
    big_wc = warp(wc, t)
    poles = [big_wc * cmath.exp(1j * math.pi * (2 * k + order - 1) / (2 * order)) for k in range(1, order + 1)]
    zpoles = [s_to_z(p, t) for p in poles]
    a = [1 + 0j]
    for p in zpoles:
        a = _poly_mul(a, [1, -p])
    a = [v.real for v in a]
    b = _poly_pow([1, 1], order)
    gain = sum(a) / sum(b)  # H(z = 1) = 1
    return [v * gain for v in b], a
