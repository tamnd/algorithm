# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gardner-timing-error-detector/. The authors are listed in prov/9K1C0E.jsonl.

"""The Gardner timing error detector (F. M. Gardner, 1986) in a first- or second-order loop.

Times are in symbol periods T. The receiver has a sampler y(t) for the matched
filter output (an ADC with a controlled clock, or an interpolator). The loop
takes two samples per symbol: the strobe y(k + tau_k) and the midpoint
y(k - 1/2 + tau_k). The detector is

    e_k = Re{ conj(y(k - 1/2 + tau_k)) (y(k - 1 + tau_{k-1}) - y(k + tau_k)) },

which is positive when the receiver samples too early (tau_k < tau). It needs
no decisions and no carrier phase: a phase rotation of y cancels in the
product. For raised cosine pulses with roll-off beta and i.i.d. zero-mean data
with E|a|^2 = 1, the mean of e_k is A sin(2 pi delta) with
A = 4 sin(pi beta / 2) / (pi (4 - beta^2)) and delta = tau - tau_k.
(This sign convention makes tau grow when e > 0; Gardner's paper writes the
difference the other way and subtracts.)
"""

import math
from typing import Callable

Sampler = Callable[[float], complex]


def detector(prev: complex, mid: complex, cur: complex) -> float:
    """The Gardner error from the previous strobe, the midpoint and the current strobe."""
    return (mid.conjugate() * (prev - cur)).real  # @line L6


def s_curve_amplitude(beta: float) -> float:
    """A in E[e] = A sin(2 pi delta), for raised cosine pulses and i.i.d. data."""
    return 4.0 * math.sin(math.pi * beta / 2.0) / (math.pi * (4.0 - beta * beta))


def gain_for_bandwidth(bl_t: float, kd: float) -> float:
    """kp of a first-order loop with noise bandwidth B_L T for the detector slope kd."""
    return 4.0 * bl_t / ((1.0 + 2.0 * bl_t) * kd)


def gardner_loop(
    sample: Sampler,
    n: int,
    kp: float,
    ki: float = 0.0,
    tau0: float = 0.0,
) -> tuple[list[float], list[complex]]:
    """Run the loop over n symbols. Return the estimates tau_k and the strobes y(k + tau_k)."""
    tau, s = tau0, 0.0  # @line L1
    prev = sample(-1.0 + tau)  # @line L2
    taus: list[float] = []
    strobes: list[complex] = []
    for k in range(n):  # @line L3
        taus.append(tau)
        mid = sample(k - 0.5 + tau)  # @line L4
        cur = sample(k + tau)  # @line L5
        strobes.append(cur)
        e = detector(prev, mid, cur)  # @line L6
        s += ki * e  # @line L7
        tau += kp * e + s  # @line L8
        prev = cur  # @line L9
    return taus, strobes  # @line L10
