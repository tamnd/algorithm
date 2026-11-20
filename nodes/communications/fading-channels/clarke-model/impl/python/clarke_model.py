# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clarke-model/. The authors are listed in prov/2J0WV7.jsonl.

"""Clarke's model: the autocorrelation Omega J0(2 pi f_D tau) and the U-shaped Doppler spectrum.

f_D = v f_c / c is the maximum Doppler frequency in hertz and Omega the mean power E|h|^2.
"""

import math

SPEED_OF_LIGHT = 299_792_458.0


def max_doppler(speed: float, carrier: float) -> float:
    """f_D = v f_c / c for a speed in m/s and a carrier in Hz."""
    return speed * carrier / SPEED_OF_LIGHT


def bessel_j0(x: float) -> float:
    """J0(x) as the mean of cos(x cos theta) over N midpoints of [0, pi]."""
    n = 32 + math.ceil(abs(x))  # @line L2
    s = math.fsum(math.cos(x * math.cos(math.pi * (k + 0.5) / n)) for k in range(n))  # @line L3
    return s / n


def clarke_correlation(tau: float, f_d: float, omega: float = 1.0) -> float:
    """R(tau) = E[h(t + tau) h*(t)] = Omega J0(2 pi f_D tau)."""
    x = 2 * math.pi * f_d * tau  # @line L1
    return omega * bessel_j0(x)  # @line L4


def doppler_spectrum(f: float, f_d: float, omega: float = 1.0) -> float:
    """S(f) = Omega / (pi f_D sqrt(1 - (f/f_D)^2)) for |f| < f_D, and 0 outside."""
    if f_d <= 0:
        raise ValueError("f_d must be positive")
    if abs(f) >= f_d:  # @line L5
        return 0.0
    return omega / (math.pi * f_d * math.sqrt(1 - (f / f_d) ** 2))  # @line L6


def rms_doppler_spread(f_d: float) -> float:
    """The RMS width of Clarke's spectrum, f_D / sqrt(2)."""
    return f_d / math.sqrt(2)
