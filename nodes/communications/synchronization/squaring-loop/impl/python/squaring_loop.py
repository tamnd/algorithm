# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/squaring-loop/. The authors are listed in prov/PVGB8C.jsonl.

"""The squaring loop and its generalization, the Mth-power loop, for M-PSK.

For an M-PSK symbol a = e^(j(phase0 + 2 pi m / M)), a^M = e^(j M phase0) for every m.
So y = r^M e^(-j M phase0) is a tone with phase M theta plus noise, and an ordinary
second-order PLL locks its phase psi to M theta. The carrier phase estimate is psi / M,
which is correct modulo 2 pi / M.

The loop runs on psi: e = Im(y e^(-j psi)), s <- s + ki e, psi <- psi + kp e + s.
Without noise e = sin(M theta - psi), so the detector gain on psi is 1. For M = 2
and phase0 = 0 the phase estimate equals that of the BPSK Costas loop with the same
gains.

In the linear model, the variance of the carrier phase estimate is
  (B_L T / M^2) sum_{n=1}^{M} C(M, n)^2 n! N0^n,
which is B_L T N0 (1 + N0/2) for M = 2 and B_L T N0 (1 + 4.5 N0 + 6 N0^2 + 1.5 N0^3) for M = 4.
"""

import cmath
import math
from typing import Sequence


def loop_gains(bl_t: float, zeta: float = 1.0 / math.sqrt(2.0)) -> tuple[float, float]:
    """(kp, ki) of the loop on psi for the noise bandwidth B_L T and damping zeta."""
    wn_t = 2.0 * bl_t / (zeta + 1.0 / (4.0 * zeta))
    return 2.0 * zeta * wn_t, wn_t * wn_t


def squaring_loop(r: Sequence[complex], m: int, kp: float, ki: float, phase0: float = 0.0, phi0: float = 0.0) -> list[float]:
    """Run the Mth-power loop on r. Element k is the carrier phase estimate used on r[k]."""
    rot = cmath.exp(-1j * m * phase0)
    psi = m * phi0  # @line L1
    s = 0.0  # @line L1
    est = []
    for x in r:  # @line L2
        est.append(psi / m)  # @line L3
        y = x**m * rot  # @line L4
        e = (y * cmath.exp(-1j * psi)).imag  # @line L5
        s += ki * e  # @line L6
        psi += kp * e + s  # @line L7
    return est  # @line L8


def variance_factor(m: int, n0: float) -> float:
    """sum_{n=1}^{M} C(M, n)^2 n! N0^n / M^2, the phase variance divided by B_L T."""
    return sum(math.comb(m, n) ** 2 * math.factorial(n) * n0**n for n in range(1, m + 1)) / (m * m)
