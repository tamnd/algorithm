# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-distance-detector/. The authors are listed in prov/NW9AYJ.jsonl.

"""Minimum distance detection by slicing, in O(1) time per symbol.

The detectors return the label index i of the chosen point, so that
constel.pam(M)[i], constel.qam(M)[i] or constel.psk(M, phase0)[i] is the
decision and constel.bits(i, log2 M) are its bits. The received sample is
y = h x + w with a known complex gain h != 0. Since
|y - h p|^2 = |h|^2 |y/h - p|^2, the closest point to y in the scaled
constellation is the closest point to y/h in the unit-energy constellation.
"""

import cmath
import math


def gray(n: int) -> int:
    """n XOR (n >> 1), the same Gray code as constel.gray."""
    return n ^ (n >> 1)


def slice_axis(u: float, side: int) -> int:
    """Gray label of the nearest raw amplitude side - 1 - 2m (m = 0, ..., side - 1) to u."""
    m = math.floor((side - 1 - u) / 2.0 + 0.5)  # @line L1
    m = min(max(m, 0), side - 1)  # @line L2
    return gray(m)  # @line L3


def detect_pam(y: complex, m: int, h: complex = 1) -> int:
    """The label of the closest unit-energy M-PAM point to y/h."""
    u = (complex(y) / h).real * math.sqrt((m * m - 1) / 3.0)  # @line L4
    return slice_axis(u, m)  # @line L5


def detect_qam(y: complex, m: int, h: complex = 1) -> int:
    """The label of the closest unit-energy square M-QAM point to y/h."""
    side = math.isqrt(m)
    if side * side != m or side & (side - 1):
        raise ValueError("square QAM needs M = 4^k")
    z = complex(y) / h * math.sqrt(2.0 * (m - 1) / 3.0)  # @line L6
    return slice_axis(z.real, side) * side + slice_axis(z.imag, side)  # @line L7


def detect_psk(y: complex, m: int, h: complex = 1, phase0: float = 0.0) -> int:
    """The label of the closest unit-energy M-PSK point to y/h."""
    theta = cmath.phase(complex(y) / h) - phase0  # @line L8
    k = math.floor(m * theta / (2.0 * math.pi) + 0.5) % m  # @line L9
    return gray(k)  # @line L10


def detect(y: complex, scheme: str, m: int, h: complex = 1, phase0: float = 0.0) -> int:
    """Dispatch on scheme ('pam', 'qam' or 'psk')."""
    if h == 0:
        raise ValueError("h must not be zero")
    if scheme == "pam":
        return detect_pam(y, m, h)
    if scheme == "qam":
        return detect_qam(y, m, h)
    if scheme == "psk":
        return detect_psk(y, m, h, phase0)
    raise ValueError("unknown scheme")


def detect_general(y: complex, points: list[complex], h: complex = 1) -> int:
    """Minimum distance over an arbitrary point list: M distances, O(M) time."""
    best, arg = math.inf, -1
    for i, p in enumerate(points):
        d = abs(y - h * p) ** 2
        if d < best:
            best, arg = d, i
    return arg
