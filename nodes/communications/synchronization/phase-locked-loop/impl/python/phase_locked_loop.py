# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-locked-loop/. The authors are listed in prov/YWG207.jsonl.

"""A second-order digital phase-locked loop (PLL).

The input is one complex sample per symbol, r[k] = e^(j theta[k]) + w[k].
The loop has three parts:
  phase detector  e = Im(r[k] e^(-j phi)), which is sin(theta - phi) without noise
  loop filter     proportional gain kp plus an integrator with gain ki
  oscillator      phi <- phi + filter output (a numerically controlled oscillator)
The loop has two integrators (the filter and the oscillator), so it follows a
phase step and a frequency step with zero error in the steady state.

Linear model: closed-loop transfer from theta to phi
  H(z) = ((kp + ki) z - kp) / (z^2 + (kp + ki - 2) z + (1 - kp)).
The one-sided noise bandwidth is B_L T = (1/2) sum_n h[n]^2, and the phase error
variance in white noise is about B_L T / SNR for |r| = 1 and SNR = 1/N0.
"""

import cmath
import math
from typing import Sequence


def loop_gains(bl_t: float, zeta: float = 1.0 / math.sqrt(2.0), kd: float = 1.0) -> tuple[float, float]:
    """Gains (kp, ki) for a noise bandwidth B_L T and damping zeta.

    This is the usual design rule from the analog loop, accurate for small B_L T:
    omega_n T = 2 B_L T / (zeta + 1/(4 zeta)), kd kp = 2 zeta omega_n T, kd ki = (omega_n T)^2.
    noise_bandwidth() gives the exact B_L T of the digital loop.
    """
    wn_t = 2.0 * bl_t / (zeta + 1.0 / (4.0 * zeta))
    return 2.0 * zeta * wn_t / kd, wn_t * wn_t / kd


def pll(r: Sequence[complex], kp: float, ki: float, phi0: float = 0.0) -> list[float]:
    """Run the loop on r. Element k of the result is the phase estimate used on r[k].

    The estimate is not reduced modulo 2 pi, so it follows a phase ramp without jumps.
    """
    phi = phi0  # @line L1
    s = 0.0  # @line L1
    est = []
    for x in r:  # @line L2
        est.append(phi)  # @line L3
        e = (x * cmath.exp(-1j * phi)).imag  # @line L4
        s += ki * e  # @line L5
        phi += kp * e + s  # @line L6
    return est  # @line L7


def closed_loop(kp: float, ki: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """((b0, b1), (a1, a2)) of H(z) = (b0 z + b1) / (z^2 + a1 z + a2)."""
    return (kp + ki, -kp), (kp + ki - 2.0, 1.0 - kp)


def is_stable(kp: float, ki: float) -> bool:
    """Jury test of the linear loop: 0 < kp < 2, ki > 0 and 2 kp + ki < 4."""
    return 0.0 < kp < 2.0 and ki > 0.0 and 2.0 * kp + ki < 4.0


def noise_bandwidth(kp: float, ki: float) -> float:
    """B_L T = (1/2) sum_n h[n]^2 of the linear loop, in closed form.

    For H(z) = (b0 z + b1)/(z^2 + a1 z + a2) with both poles inside the unit circle,
    sum h^2 = ((b0^2 + b1^2)(1 + a2) - 2 b0 b1 a1) / ((1 - a2)((1 + a2)^2 - a1^2)).
    """
    if not is_stable(kp, ki):
        raise ValueError("the loop is not stable")
    (b0, b1), (a1, a2) = closed_loop(kp, ki)
    num = (b0 * b0 + b1 * b1) * (1.0 + a2) - 2.0 * b0 * b1 * a1
    den = (1.0 - a2) * ((1.0 + a2) ** 2 - a1 * a1)
    return 0.5 * num / den
