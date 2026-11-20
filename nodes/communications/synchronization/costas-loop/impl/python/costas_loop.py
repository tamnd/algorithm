# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/costas-loop/. The authors are listed in prov/J5XYD4.jsonl.

"""The Costas loop for BPSK and QPSK, in digital form at one sample per symbol.

Each sample is rotated by the current phase estimate, z = r e^(-j phi). The
in-phase arm is I = Re z and the quadrature arm is Q = Im z. The detector
removes the data:
  BPSK: e = I Q, which is (1/2) sin(2 delta) without noise (gain 1)
  QPSK: e = sgn(I) Q - sgn(Q) I, which is sqrt(2) sin(delta) for |delta| < pi/4
        without noise (gain sqrt(2)); this is the hard-limited Costas detector.
Here delta = theta - phi is the phase error. The loop filter and the oscillator
are those of a second-order PLL: s <- s + ki e, phi <- phi + kp e + s.
The loop locks to theta modulo pi (BPSK) or modulo pi/2 (QPSK).
"""

import cmath
import math
from typing import Sequence

GAIN = {"bpsk": 1.0, "qpsk": math.sqrt(2.0)}


def loop_gains(bl_t: float, mod: str, zeta: float = 1.0 / math.sqrt(2.0)) -> tuple[float, float]:
    """(kp, ki) for the noise bandwidth B_L T and damping zeta, divided by the detector gain."""
    wn_t = 2.0 * bl_t / (zeta + 1.0 / (4.0 * zeta))
    kd = GAIN[mod]
    return 2.0 * zeta * wn_t / kd, wn_t * wn_t / kd


def sgn(x: float) -> float:
    return 1.0 if x >= 0.0 else -1.0


def detector(z: complex, mod: str) -> float:
    """The Costas error from the two arms I = Re z and Q = Im z."""
    i, q = z.real, z.imag
    if mod == "bpsk":
        return i * q  # @line L5
    if mod == "qpsk":
        return sgn(i) * q - sgn(q) * i  # @line L5
    raise ValueError("mod must be 'bpsk' or 'qpsk'")


def costas(r: Sequence[complex], kp: float, ki: float, mod: str = "bpsk", phi0: float = 0.0) -> list[float]:
    """Run the loop on r. Element k of the result is the phase estimate used on r[k]."""
    phi = phi0  # @line L1
    s = 0.0  # @line L1
    est = []
    for x in r:  # @line L2
        est.append(phi)  # @line L3
        z = x * cmath.exp(-1j * phi)  # @line L4
        e = detector(z, mod)  # @line L5
        s += ki * e  # @line L6
        phi += kp * e + s  # @line L7
    return est  # @line L8
