# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viterbi-viterbi-phase-estimation/. The authors are listed in prov/VA0M3B.jsonl.

"""Viterbi and Viterbi (VV) feedforward carrier phase estimation for M-PSK.

Write each sample in polar form, r[k] = rho e^(j psi). Multiplying the angle
by M removes the M-PSK data, because M times a data angle 2 pi i / M + phase0
is M phase0 modulo 2 pi. The modulus is replaced by a nonlinearity F(rho) =
rho^p. The estimate is

  theta_hat = (arg(sum_k rho_k^p e^(j M psi_k)) - M phase0) / M,

wrapped to [-pi/M, pi/M). It has the M-fold ambiguity of the constellation:
it estimates theta modulo 2 pi / M. With p = M it is the plain Mth power
estimator arg(sum r^M) / M.
"""

import cmath
import math
from typing import Sequence


def wrap(x: float, period: float) -> float:
    """x reduced to [-period/2, period/2)."""
    return (x + period / 2.0) % period - period / 2.0


def vv_estimate(r: Sequence[complex], m: int, p: float = 2.0, phase0: float = 0.0) -> float:
    """The VV phase estimate for M-PSK with first point at angle phase0, F(rho) = rho^p."""
    s = 0j  # @line L1
    for x in r:  # @line L2
        rho, psi = abs(x), cmath.phase(x)  # @line L3
        s += rho**p * cmath.exp(1j * m * psi)  # @line L4
    theta = (cmath.phase(s) - m * phase0) / m  # @line L5
    return wrap(theta, 2.0 * math.pi / m)  # @line L6


def objective(r: Sequence[complex], m: int, phi: float, p: float = 2.0, phase0: float = 0.0) -> float:
    """sum_k rho_k^p cos(M (psi_k - phi - phase0)), the function that the VV estimate maximizes."""
    return sum(abs(x) ** p * math.cos(m * (cmath.phase(x) - phi - phase0)) for x in r)


def unwrap(estimates: Sequence[float], m: int) -> list[float]:
    """Unwrap block estimates: move each by a multiple of 2 pi / M to the one nearest the previous."""
    period = 2.0 * math.pi / m
    out: list[float] = []
    for t in estimates:
        if out:
            t = out[-1] + wrap(t - out[-1], period)
        out.append(t)
    return out
