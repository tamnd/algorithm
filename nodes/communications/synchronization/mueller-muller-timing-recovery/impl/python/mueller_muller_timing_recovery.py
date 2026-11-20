# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mueller-muller-timing-recovery/. The authors are listed in prov/BY94Z6.jsonl.

"""Mueller and Muller timing recovery (1976): a decision-directed loop at one sample per symbol.

Times are in symbol periods T. The receiver has a sampler y(t) for the matched
filter output, after carrier phase correction: an ADC whose clock the loop
controls, or an interpolator. At each symbol it takes one sample
y_k = y(k + tau_k), makes a decision a_k (or uses a known symbol) and forms

    e_k = Re{ conj(a_{k-1}) y_k - conj(a_k) y_{k-1} }.

With correct decisions and i.i.d. data with E|a|^2 = 1, the mean of e_k is
g(1 - delta) - g(1 + delta) for the overall pulse g and delta = tau - tau_k.
So the loop settles where the pulse samples one symbol before and one symbol
after the strobe are equal. For a symmetric pulse this is the peak. e_k > 0
when the receiver samples too early, and the loop moves tau up:

    s <- s + ki e_k,   tau_{k+1} = tau_k + kp e_k + s.
"""

import math
from typing import Callable, Optional, Sequence

Sampler = Callable[[float], complex]


def slicer(y: complex, points: Sequence[complex]) -> complex:
    """The nearest point of the constellation (minimum distance decision)."""
    return min(points, key=lambda p: abs(y - p))


def detector(prev_y: complex, prev_a: complex, y: complex, a: complex) -> float:
    """The Mueller and Muller error from two strobes and their symbols."""
    return (prev_a.conjugate() * y - a.conjugate() * prev_y).real  # @line L6


def slope_raised_cosine(beta: float) -> float:
    """Slope at lock, -2 g'(1), for a raised cosine pulse with roll-off beta."""
    if abs(beta - 0.5) < 1e-12:
        return math.pi / 2.0
    return 2.0 * math.cos(math.pi * beta) / (1.0 - 4.0 * beta * beta)


def gain_for_bandwidth(bl_t: float, kd: float) -> float:
    """kp of a first-order loop with noise bandwidth B_L T for the detector slope kd."""
    return 4.0 * bl_t / ((1.0 + 2.0 * bl_t) * kd)


def mueller_muller(
    sample: Sampler,
    n: int,
    kp: float,
    points: Sequence[complex],
    ki: float = 0.0,
    tau0: float = 0.0,
    known: Optional[Sequence[complex]] = None,
) -> tuple[list[float], list[complex], list[complex]]:
    """Run the loop over n symbols. With known symbols it is data-aided, else decision-directed.

    Return the estimates tau_k, the strobes y_k and the symbols a_k used.
    """
    tau, s = tau0, 0.0  # @line L1
    prev_y, prev_a = 0j, 0j
    taus: list[float] = []
    ys: list[complex] = []
    decisions: list[complex] = []
    for k in range(n):  # @line L2
        taus.append(tau)
        y = sample(k + tau)  # @line L3
        a = known[k] if known is not None else slicer(y, points)  # @line L4
        ys.append(y)
        decisions.append(a)
        if k > 0:  # @line L5
            e = detector(prev_y, prev_a, y, a)  # @line L6
            s += ki * e  # @line L7
            tau += kp * e + s  # @line L8
        prev_y, prev_a = y, a  # @line L9
    return taus, ys, decisions  # @line L10
