# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-spread/. The authors are listed in prov/T38XE2.jsonl.

"""Mean excess delay, RMS delay spread and maximum excess delay of a power delay profile.

A profile is a list of delays tau[l] and mean powers P[l] >= 0 in linear units (not dB).
The powers need not sum to 1; every moment is divided by their sum.
With int or Fraction inputs, delay_moments returns exact Fractions.
"""

import cmath
import math
from fractions import Fraction
from typing import Sequence, Tuple, Union

Number = Union[int, float, Fraction]


def _check(delays: Sequence[Number], powers: Sequence[Number]) -> None:
    if len(delays) != len(powers) or not delays:
        raise ValueError("delays and powers must be non-empty and of the same length")
    if any(p < 0 for p in powers) or sum(powers) <= 0:
        raise ValueError("powers must be non-negative with a positive sum")


def delay_moments(delays: Sequence[Number], powers: Sequence[Number]) -> Tuple[Number, Number]:
    """The mean excess delay and the variance sigma_tau^2 of the profile."""
    _check(delays, powers)
    s = sum(powers)  # @line L1
    if all(isinstance(x, (int, Fraction)) for x in list(delays) + list(powers)):
        s = Fraction(s)
    mu = sum(p * t for p, t in zip(powers, delays)) / s  # @line L2
    var = sum(p * (t - mu) ** 2 for p, t in zip(powers, delays)) / s  # @line L3
    return mu, var


def rms_delay_spread(delays: Sequence[Number], powers: Sequence[Number]) -> Tuple[float, float]:
    """The mean excess delay and the RMS delay spread sigma_tau."""
    mu, var = delay_moments(delays, powers)
    return float(mu), math.sqrt(var)  # @line L4


def max_excess_delay(delays: Sequence[Number], powers: Sequence[Number], x_db: float) -> Number:
    """The largest delay with power within x_db dB of the strongest tap, minus the first delay."""
    _check(delays, powers)
    t = max(powers) * 10 ** (-x_db / 10)  # @line L5
    return max(d for d, p in zip(delays, powers) if p >= t) - min(delays)  # @line L6


def frequency_correlation(delays: Sequence[float], powers: Sequence[float], df: float) -> complex:
    """R(df) = sum_l P_l exp(-j 2 pi df tau_l) / sum_l P_l, the normalized frequency correlation."""
    _check(delays, powers)
    s = float(sum(powers))
    return sum(p * cmath.exp(-2j * math.pi * df * t) for p, t in zip(powers, delays)) / s


def db_to_linear(powers_db: Sequence[float]) -> list:
    """Convert powers in dB to linear values."""
    return [10 ** (x / 10) for x in powers_db]
