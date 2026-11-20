# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cell-averaging-cfar/. The authors are listed in prov/AFY7TQ.jsonl.

"""Cell-averaging CFAR (Finn and Johnson, 1968) with a running sum.

The input x[0..n-1] is the output of a square-law detector along range, one
power value per cell. For the cell under test i, the reference window holds
h = N / 2 cells on each side, after G guard cells:

    lagging cells   i - G - h .. i - G - 1
    leading cells   i + G + 1 .. i + G + h

Z is the sum of the N reference cells, and the cell is declared a target when
x[i] > tau Z. In homogeneous noise with i.i.d. exponential cells of any mean,
the false alarm probability is (1 + tau)^(-N), so tau = Pfa^(-1/N) - 1.

The arithmetic is generic: with int or Fraction cells and a Fraction tau every
comparison is exact. Cells closer than G + h to either end have no full
window and are not tested.
"""

from fractions import Fraction
from typing import Sequence


def threshold_factor(n_ref: int, pfa: float) -> float:
    """tau = Pfa^(-1/N) - 1, the factor on the sum of the N reference cells. Cost: O(1)."""
    if n_ref < 1 or not 0.0 < pfa < 1.0:
        raise ValueError("need N >= 1 and 0 < Pfa < 1")
    return pfa ** (-1.0 / n_ref) - 1.0


def false_alarm_probability(n_ref: int, tau) -> float:
    """The closed form Pfa = (1 + tau)^(-N) for i.i.d. exponential cells."""
    return (1 + tau) ** (-n_ref)


def detection_probability_swerling1(n_ref: int, tau, snr) -> float:
    """Pd = (1 + tau / (1 + S))^(-N) for a Swerling 1 target of mean SNR S (a power ratio)."""
    return (1 + tau / (1 + snr)) ** (-n_ref)


def ca_cfar(x: Sequence, n_ref: int, guard: int, tau) -> tuple[list[int], list]:
    """Run CA-CFAR along x and return (detections, thresholds).

    n_ref is the even number N of reference cells, guard the number G of guard
    cells on each side, and tau the factor on the sum. thresholds[i] is tau Z
    for every cell with a full window, and None for the cells near the ends.
    detections lists the indices i with x[i] > tau Z, in increasing order.
    Cost: O(n) time for n cells (O(1) per cell after the first window), O(n)
    space for the output.
    """
    if n_ref < 2 or n_ref % 2 or guard < 0:
        raise ValueError("need an even N >= 2 and G >= 0")
    n = len(x)
    h = n_ref // 2  # @line L1
    thresholds: list = [None] * n
    detections: list[int] = []
    first, last = guard + h, n - 1 - guard - h
    if first > last:
        return detections, thresholds
    z = sum(x[first - guard - h:first - guard]) + sum(x[first + guard + 1:first + guard + h + 1])  # @line L2
    for i in range(first, last + 1):  # @line L3
        t = tau * z  # @line L4
        thresholds[i] = t
        if x[i] > t:  # @line L5
            detections.append(i)
        if i < last:
            z += x[i - guard] - x[i - guard - h]  # @line L6
            z += x[i + guard + h + 1] - x[i + guard + 1]  # @line L7
    return detections, thresholds


def ca_cfar_direct(x: Sequence, n_ref: int, guard: int, tau) -> tuple[list[int], list]:
    """The same detector with the window sum recomputed for every cell: O(n N) time."""
    n = len(x)
    h = n_ref // 2
    thresholds: list = [None] * n
    detections: list[int] = []
    for i in range(guard + h, n - guard - h):
        z = sum(x[i - guard - h:i - guard]) + sum(x[i + guard + 1:i + guard + h + 1])
        thresholds[i] = tau * z
        if x[i] > tau * z:
            detections.append(i)
    return detections, thresholds


def exact_tau(n_ref: int, pfa_root: Fraction) -> Fraction:
    """A rational tau for the design Pfa = pfa_root^N: tau = 1 / pfa_root - 1."""
    return 1 / Fraction(pfa_root) - 1
