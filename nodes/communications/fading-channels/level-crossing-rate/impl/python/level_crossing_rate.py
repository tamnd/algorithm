# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/level-crossing-rate/. The authors are listed in prov/Y8DDW4.jsonl.

"""Level crossing rate and average fade duration of a fading envelope.

rho = R / sqrt(Omega) is the level relative to the RMS envelope, f_d the maximum Doppler
frequency in Hz (Clarke's model) and sigma_nu the RMS Doppler spread in Hz (any even spectrum).
"""

import math
from typing import Sequence, Tuple


def lcr_afd_clarke(rho: float, f_d: float) -> Tuple[float, float]:
    """(N_R, t_R) in Clarke's model: crossings per second and mean fade length in seconds."""
    if rho <= 0 or f_d <= 0:
        raise ValueError("rho and f_d must be positive")
    n = math.sqrt(2 * math.pi) * f_d * rho * math.exp(-rho * rho)  # @line L1
    p = -math.expm1(-rho * rho)  # @line L2
    return n, p / n  # @line L3


def lcr_afd_rayleigh(rho: float, sigma_nu: float) -> Tuple[float, float]:
    """(N_R, t_R) for Rayleigh fading with an even Doppler spectrum of RMS width sigma_nu."""
    if rho <= 0 or sigma_nu <= 0:
        raise ValueError("rho and sigma_nu must be positive")
    n = 2 * math.sqrt(math.pi) * sigma_nu * rho * math.exp(-rho * rho)
    return n, -math.expm1(-rho * rho) / n


def count_crossings(r: Sequence[float], level: float, dt: float) -> Tuple[float, float]:
    """Estimates (N_R, t_R) from envelope samples r[k] = r(k dt)."""
    n = len(r)
    if n < 2 or dt <= 0:
        raise ValueError("need at least two samples and dt > 0")
    c = sum(1 for k in range(1, n) if r[k - 1] >= level > r[k])  # @line L4
    b = sum(1 for x in r if x < level)  # @line L5
    if c == 0:
        return 0.0, math.inf
    return c / (n * dt), b * dt / c  # @line L6
