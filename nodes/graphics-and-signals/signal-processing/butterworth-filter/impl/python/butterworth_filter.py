# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/butterworth-filter/. The authors are listed in prov/VAFAXE.jsonl.

"""The analog Butterworth low-pass filter of order N and cutoff wc (radians per second).

|H(i W)|^2 = 1 / (1 + (W / wc)^(2N)). The poles are the N roots of
1 + (s / (i wc))^(2N) = 0 that lie in the left half plane.
"""

import cmath
import math


def butterworth_poles(order: int, wc: float = 1.0) -> list[complex]:
    """Return s_k = wc e^(i pi (2k + N - 1) / (2N)) for k = 1 .. N, all with real part < 0."""
    if order < 1:
        raise ValueError("the order must be at least 1")
    return [wc * cmath.exp(1j * math.pi * (2 * k + order - 1) / (2 * order)) for k in range(1, order + 1)]


def denominator(order: int, wc: float = 1.0) -> list[float]:
    """Return a[0..N] with D(s) = a[0] + a[1] s + ... + a[N] s^N = prod (s - s_k), a[N] = 1."""
    c = [1 + 0j]
    for p in butterworth_poles(order, wc):
        nxt = [0j] * (len(c) + 1)
        for i, v in enumerate(c):
            nxt[i + 1] += v
            nxt[i] -= p * v
        c = nxt
    return [v.real for v in c]


def response(order: int, wc: float, w: float) -> complex:
    """Return H(i w) = wc^N / D(i w), so that H(0) = 1."""
    a = denominator(order, wc)
    s = 1j * w
    d = 0j
    for v in reversed(a):
        d = d * s + v
    return wc ** order / d


def magnitude_squared(order: int, wc: float, w: float) -> float:
    """The closed formula 1 / (1 + (w / wc)^(2N))."""
    return 1.0 / (1.0 + (w / wc) ** (2 * order))


def minimum_order(wp: float, ws: float, ap_db: float, as_db: float) -> int:
    """Smallest N with attenuation at most ap_db at wp and at least as_db at ws, for wc chosen freely."""
    if not 0 < wp < ws or not 0 < ap_db < as_db:
        raise ValueError("need 0 < wp < ws and 0 < ap_db < as_db")
    ratio = (10 ** (as_db / 10) - 1) / (10 ** (ap_db / 10) - 1)
    return math.ceil(math.log(ratio) / (2 * math.log(ws / wp)) - 1e-12)


def cutoff_for_passband(order: int, wp: float, ap_db: float) -> float:
    """The cutoff that gives exactly ap_db attenuation at wp."""
    return wp / (10 ** (ap_db / 10) - 1) ** (1 / (2 * order))
