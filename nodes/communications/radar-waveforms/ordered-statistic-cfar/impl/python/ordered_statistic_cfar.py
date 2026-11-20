# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordered-statistic-cfar/. The authors are listed in prov/3GCSWG.jsonl.

"""Ordered-statistic CFAR (Rohling, 1983) with a sliding sorted window.

The input x[0..n-1] is the output of a square-law detector along range. For
the cell under test i, the reference window holds h = N / 2 cells on each
side, after G guard cells. The N reference values are kept in a sorted list.
The k-th smallest of them, X_(k), estimates the noise level, and the cell is a
target when x[i] > T X_(k).

For i.i.d. exponential cells of any mean, the false alarm probability is

    Pfa(T) = prod over i = 0 .. k-1 of (N - i) / (N - i + T),

which falls strictly in T, so T for a design Pfa is found by bisection.

The sorted window is updated with bisect: two removals and two insertions per
cell, each O(N) for the list shifts. With int or Fraction cells and a Fraction
T every comparison is exact.
"""

from bisect import bisect_left, insort
from fractions import Fraction
from math import comb, factorial
from typing import Sequence


def false_alarm_probability(n_ref: int, k: int, t):
    """Pfa = prod_{i<k} (N - i) / (N - i + T). Exact for int or Fraction T."""
    p = Fraction(1) if isinstance(t, (int, Fraction)) else 1.0
    for i in range(k):
        p = p * (n_ref - i) / (n_ref - i + t)
    return p


def false_alarm_probability_rohling(n_ref: int, k: int, t: int) -> Fraction:
    """Rohling's equation (14) for an integer T: k C(N, k) (k-1)! (T + N - k)! / (T + N)!."""
    return Fraction(k * comb(n_ref, k) * factorial(k - 1) * factorial(t + n_ref - k), factorial(t + n_ref))


def threshold_factor(n_ref: int, k: int, pfa: float) -> float:
    """The T with Pfa(T) = pfa, by bisection (Pfa falls strictly in T). Cost: O(k) per step."""
    if not 1 <= k <= n_ref or not 0.0 < pfa < 1.0:
        raise ValueError("need 1 <= k <= N and 0 < Pfa < 1")
    lo, hi = 0.0, 1.0
    while false_alarm_probability(n_ref, k, hi) > pfa:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if false_alarm_probability(n_ref, k, mid) > pfa:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-13 * hi:
            break
    return 0.5 * (lo + hi)


def mean_order_statistic(n_ref: int, k: int) -> float:
    """E X_(k) / mu = sum_{j=1..k} 1 / (N - k + j) for i.i.d. exponential cells of mean mu."""
    return sum(1.0 / (n_ref - k + j) for j in range(1, k + 1))


def detection_probability_swerling1(n_ref: int, k: int, t, snr) -> float:
    """Pd for a Swerling 1 target of mean SNR S: Pfa with T replaced by T / (1 + S)."""
    return false_alarm_probability(n_ref, k, t / (1 + snr))


def _remove(w: list, v) -> None:
    del w[bisect_left(w, v)]


def os_cfar(x: Sequence, n_ref: int, guard: int, k: int, t) -> tuple[list[int], list]:
    """Run OS-CFAR along x and return (detections, thresholds).

    n_ref is the even number N of reference cells, guard the number G of guard
    cells on each side, k the rank (1 <= k <= N) and t the factor T. The
    threshold of cell i is T times the k-th smallest reference value, or None
    near the ends. Cost: O(n N) time with the sorted list, O(N) extra space.
    """
    if n_ref < 2 or n_ref % 2 or guard < 0 or not 1 <= k <= n_ref:
        raise ValueError("need an even N >= 2, G >= 0 and 1 <= k <= N")
    n = len(x)
    h = n_ref // 2
    thresholds: list = [None] * n
    detections: list[int] = []
    first, last = guard + h, n - 1 - guard - h
    if first > last:
        return detections, thresholds
    w = sorted(list(x[first - guard - h:first - guard]) + list(x[first + guard + 1:first + guard + h + 1]))  # @line L1
    for i in range(first, last + 1):  # @line L2
        z = w[k - 1]  # @line L3
        thresholds[i] = t * z  # @line L4
        if x[i] > t * z:  # @line L5
            detections.append(i)
        if i < last:
            _remove(w, x[i - guard - h])  # @line L6
            insort(w, x[i - guard])  # @line L6
            _remove(w, x[i + guard + 1])  # @line L7
            insort(w, x[i + guard + h + 1])  # @line L7
    return detections, thresholds


def os_cfar_direct(x: Sequence, n_ref: int, guard: int, k: int, t) -> tuple[list[int], list]:
    """The same detector with each window sorted from scratch: O(n N log N) time."""
    n = len(x)
    h = n_ref // 2
    thresholds: list = [None] * n
    detections: list[int] = []
    for i in range(guard + h, n - guard - h):
        w = sorted(list(x[i - guard - h:i - guard]) + list(x[i + guard + 1:i + guard + h + 1]))
        thresholds[i] = t * w[k - 1]
        if x[i] > thresholds[i]:
            detections.append(i)
    return detections, thresholds
