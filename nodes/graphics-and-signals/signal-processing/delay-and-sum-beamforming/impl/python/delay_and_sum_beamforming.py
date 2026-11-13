# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-and-sum-beamforming/. The authors are listed in prov/HE5XFQ.jsonl.

"""Delay-and-sum beamforming for a linear array.

Sensor m sits at the position p_m along the array axis. A plane wave from the
direction with u = sin(theta) reaches sensor m later than the origin by
p_m * u / c seconds. Delay-and-sum undoes these delays for a look direction
u0 and averages the sensors, so a wave from u0 adds in phase.

The time-domain form works with whole-sample delays. The narrowband form uses
the weights w = a(u0) / M with the steering vector
a_m(u) = exp(-i 2 pi (d / lambda) m u) of a uniform linear array; its beam
pattern |w^H a(u)| is the Dirichlet kernel |sin(M psi / 2) / (M sin(psi / 2))|
with psi = 2 pi (d / lambda) (u - u0).
"""

import cmath
import math
from fractions import Fraction
from typing import Sequence


def arrival_delays(positions: Sequence[float], u0: float, speed: float, rate: float) -> list[int]:
    """The arrival delay of a wave from u0 at each sensor, rounded to whole samples."""
    return [round(Fraction(rate) * Fraction(p) * Fraction(u0) / Fraction(speed))  # @line L1
            for p in positions]


def delay_and_sum(signals: Sequence[Sequence], delays: Sequence[int]) -> list:
    """y[t] = (1/M) sum_m x_m[t + tau_m - tau_min], for every t where all samples exist.

    The arithmetic follows the input: integers or Fractions give an exact result.
    """
    m_count = len(signals)
    if m_count == 0 or len(delays) != m_count:
        raise ValueError("need one delay per sensor and at least one sensor")
    length = min(len(x) for x in signals)
    base = min(delays)  # @line L2
    span = max(delays) - base
    out = []
    for t in range(length - span):  # @line L3
        acc = 0  # @line L4
        for m in range(m_count):  # @line L5
            acc = acc + signals[m][t + delays[m] - base]  # @line L6
        out.append(Fraction(acc, m_count) if isinstance(acc, int) else acc / m_count)  # @line L7
    return out  # @line L8


def steering_vector(m_count: int, spacing: float, u: float) -> list[complex]:
    """a_m(u) = exp(-i 2 pi spacing m u), with spacing = d / lambda."""
    return [cmath.exp(-2j * math.pi * float(spacing) * m * float(u)) for m in range(m_count)]


def das_weights(m_count: int, spacing: float, u0: float) -> list[complex]:
    """The narrowband delay-and-sum weights a(u0) / M."""
    return [a / m_count for a in steering_vector(m_count, spacing, u0)]


def beam_pattern(weights: Sequence[complex], spacing: float, u: float) -> float:
    """|w^H a(u)|, computed by the defining sum."""
    a = steering_vector(len(weights), spacing, u)
    return abs(sum(w.conjugate() * x for w, x in zip(weights, a)))


def dirichlet_pattern(m_count: int, spacing: float, u0: float, u: float) -> float:
    """The closed form |sin(M psi / 2) / (M sin(psi / 2))|, equal to 1 where psi is a multiple of 2 pi."""
    frac = Fraction(spacing) * (Fraction(u) - Fraction(u0))
    if frac.denominator == 1:
        return 1.0
    psi = 2 * math.pi * float(frac)
    return abs(math.sin(m_count * psi / 2) / (m_count * math.sin(psi / 2)))


def grating_lobes(spacing: Fraction, u0: Fraction) -> list[Fraction]:
    """All u in [-1, 1] other than u0 where the pattern equals 1, in exact arithmetic.

    They are the solutions of spacing * (u - u0) = k for a nonzero integer k.
    """
    spacing, u0 = Fraction(spacing), Fraction(u0)
    if spacing <= 0:
        raise ValueError("spacing must be positive")
    lobes = []
    k_max = math.floor(2 * spacing) + 1
    for k in range(-k_max, k_max + 1):
        u = u0 + Fraction(k) / spacing
        if k != 0 and -1 <= u <= 1:
            lobes.append(u)
    return lobes
