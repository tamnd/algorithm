# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-directed-carrier-recovery/. The authors are listed in prov/EVQ8KF.jsonl.

"""Decision-directed (DD) carrier phase tracking with a second-order loop.

Each sample is rotated by the current phase estimate, z = r e^(-j phi), and
the nearest constellation point a_hat is decided. The phase detector is
  e = Im(z conj(a_hat)),
which is |a|^2 sin(theta - phi) without noise when the decision is right.
Averaged over unit-energy data its gain is E|a|^2 = 1. A second-order loop
filter and an oscillator close the loop, as in a phase-locked loop.

If the transmitted symbols are known (a preamble or pilots), pass them as
`known`: the detector then uses them instead of decisions. This is the
data-aided form of the same loop, and it has no phase ambiguity.
"""

import cmath
import math
from typing import Optional, Sequence


def loop_gains(bl_t: float, zeta: float = 1.0 / math.sqrt(2.0)) -> tuple[float, float]:
    """(kp, ki) for the noise bandwidth B_L T and damping zeta, with detector gain 1."""
    wn_t = 2.0 * bl_t / (zeta + 1.0 / (4.0 * zeta))
    return 2.0 * zeta * wn_t, wn_t * wn_t


def nearest(z: complex, points: Sequence[complex]) -> complex:
    """The point of the constellation closest to z (the first one on a tie)."""
    best, arg = math.inf, points[0]
    for p in points:
        d = abs(z - p) ** 2
        if d < best:
            best, arg = d, p
    return arg


def dd_detector(z: complex, points: Sequence[complex]) -> float:
    """The DD phase error Im(z conj(a_hat)) for a derotated sample z."""
    return (z * nearest(z, points).conjugate()).imag


def dd_loop(
    r: Sequence[complex],
    points: Sequence[complex],
    kp: float,
    ki: float,
    known: Optional[Sequence[complex]] = None,
    phi0: float = 0.0,
) -> tuple[list[float], list[complex]]:
    """Run the loop. Returns the phase estimate used on each r[k] and the decisions."""
    phi = phi0  # @line L1
    s = 0.0  # @line L1
    est, dec = [], []
    for k, x in enumerate(r):  # @line L2
        est.append(phi)  # @line L3
        z = x * cmath.exp(-1j * phi)  # @line L4
        a_hat = known[k] if known is not None else nearest(z, points)  # @line L5
        dec.append(a_hat)
        e = (z * a_hat.conjugate()).imag  # @line L6
        s += ki * e  # @line L7
        phi += kp * e + s  # @line L8
    return est, dec  # @line L9
