# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/early-late-gate-synchronizer/. The authors are listed in prov/Z897RY.jsonl.

"""The early-late gate symbol synchronizer, in its square-law (non-data-aided) form.

Times are in symbol periods T. The receiver has a sampler y(t) for the matched
filter output: an ADC with a controlled clock, or an interpolator on a fixed
sample grid. The symbols sit at t = k + tau for an unknown delay tau. For the
estimate tau_k, the gate takes the early sample y(k + tau_k - d) and the late
sample y(k + tau_k + d) and forms

    e_k = |y(k + tau_k + d)|^2 - |y(k + tau_k - d)|^2.

If the receiver samples too early (tau_k < tau), the late sample is nearer the
peak of the pulse and e_k > 0. A first- or second-order loop moves tau_k:

    s <- s + ki e_k,   tau_{k+1} = tau_k + kp e_k + s.

For raised cosine pulses with roll-off beta and i.i.d. zero-mean data with
E|a|^2 = 1, the mean of e_k is (beta/2) sin(2 pi d) sin(2 pi delta), where
delta = tau - tau_k. The slope at lock is pi beta sin(2 pi d): it is largest
at d = 1/4 and it is zero at d = 1/2.
"""

import math
from typing import Callable

Sampler = Callable[[float], complex]


def detector(sample: Sampler, t: float, d: float = 0.25) -> float:
    """The early-late error at the strobe time t, with the gate half-width d."""
    late = sample(t + d)  # @line L4
    early = sample(t - d)  # @line L3
    return abs(late) ** 2 - abs(early) ** 2  # @line L5


def s_curve(delta: float, beta: float, d: float = 0.25) -> float:
    """Mean detector output for raised cosine pulses and i.i.d. data, E|a|^2 = 1."""
    return 0.5 * beta * math.sin(2 * math.pi * d) * math.sin(2 * math.pi * delta)


def gain_for_bandwidth(bl_t: float, kd: float) -> float:
    """kp of a first-order loop with noise bandwidth B_L T for the detector slope kd."""
    return 4.0 * bl_t / ((1.0 + 2.0 * bl_t) * kd)


def early_late_gate(
    sample: Sampler,
    n: int,
    kp: float,
    ki: float = 0.0,
    tau0: float = 0.0,
    d: float = 0.25,
) -> tuple[list[float], list[complex]]:
    """Run the loop over n symbols. Return the estimates tau_k and the strobes y(k + tau_k)."""
    tau, s = tau0, 0.0  # @line L1
    taus: list[float] = []
    strobes: list[complex] = []
    for k in range(n):  # @line L2
        t = k + tau
        taus.append(tau)
        strobes.append(sample(t))  # @line L6
        e = detector(sample, t, d)  # @line L3
        s += ki * e  # @line L7
        tau += kp * e + s  # @line L8
    return taus, strobes  # @line L9
