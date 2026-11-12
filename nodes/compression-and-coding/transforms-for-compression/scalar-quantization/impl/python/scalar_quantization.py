# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scalar-quantization/. The authors are listed in prov/E3908F.jsonl.

"""Scalar quantizers: a general quantizer given by thresholds and levels,
uniform midtread and midrise quantizers, a dead-zone quantizer, and the
Lloyd-Max design (Lloyd's Method I) for a density given by its partial
moments.

A quantizer with N cells has thresholds t[0] < ... < t[N-2] and levels
y[0] < ... < y[N-1]. Cell i is (t[i-1], t[i]] with t[-1] = -inf and
t[N-1] = +inf. Encoding costs O(log N) comparisons by binary search.
"""

import bisect
import math
from typing import Callable, List, Sequence, Tuple


def encode(x: float, t: Sequence[float]) -> int:
    """Index of the cell of x: the number of thresholds below x."""
    return bisect.bisect_left(t, x)  # @line L1


def decode(i: int, y: Sequence[float]) -> float:
    """Level of cell i."""
    return y[i]  # @line L2


def midtread(x: float, step: float) -> float:
    """Uniform quantizer with a level at 0: step * round(x / step), halves away from 0."""
    k = math.floor(abs(x) / step + 0.5)
    return math.copysign(k * step, x) if k else 0.0


def midrise(x: float, step: float) -> float:
    """Uniform quantizer with a threshold at 0: levels at (k + 1/2) step."""
    return (math.floor(x / step) + 0.5) * step


def deadzone_index(x: float, step: float) -> int:
    """Dead-zone index sign(x) floor(|x| / step), as in JPEG 2000 Part 1.

    The zero cell is (-step, step), twice as wide as the other cells.
    """
    k = int(abs(x) // step)
    return k if x >= 0 else -k


def deadzone_value(q: int, step: float, r: float = 0.5) -> float:
    """Reconstruction (|q| + r) step with the sign of q, and 0 for q = 0."""
    if q == 0:
        return 0.0
    return math.copysign((abs(q) + r) * step, q)


# A density is given by three functions of an interval (a, b]: its mass,
# its first moment and its second moment. Closed forms avoid numerical
# integration, so the design is exact up to the iteration.
Moments = Tuple[Callable[[float, float], float], Callable[[float, float], float], Callable[[float, float], float]]


def _phi(x: float) -> float:
    return 0.0 if math.isinf(x) else math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _xphi(x: float) -> float:
    return 0.0 if math.isinf(x) else x * _phi(x)


GAUSSIAN: Moments = (
    lambda a, b: _cdf(b) - _cdf(a),
    lambda a, b: _phi(a) - _phi(b),
    lambda a, b: (_cdf(b) - _cdf(a)) - (_xphi(b) - _xphi(a)),
)


def uniform_moments(lo: float, hi: float) -> Moments:
    """The uniform density on [lo, hi]."""
    w = hi - lo

    def clip(a: float, b: float) -> Tuple[float, float]:
        return max(a, lo), min(b, hi)

    def m0(a: float, b: float) -> float:
        a, b = clip(a, b)
        return max(0.0, b - a) / w

    def m1(a: float, b: float) -> float:
        a, b = clip(a, b)
        return (b * b - a * a) / (2 * w) if b > a else 0.0

    def m2(a: float, b: float) -> float:
        a, b = clip(a, b)
        return (b ** 3 - a ** 3) / (3 * w) if b > a else 0.0

    return m0, m1, m2


def cells(t: Sequence[float]) -> List[Tuple[float, float]]:
    """The cells (a, b] of the thresholds t, with infinite ends."""
    edges = [-math.inf] + list(t) + [math.inf]
    return list(zip(edges, edges[1:]))


def distortion(t: Sequence[float], y: Sequence[float], dens: Moments) -> float:
    """Mean squared error of the quantizer (t, y) on the density."""
    m0, m1, m2 = dens
    total = 0.0
    for (a, b), v in zip(cells(t), y):
        total += m2(a, b) - 2 * v * m1(a, b) + v * v * m0(a, b)
    return total


def lloyd_max(y0: Sequence[float], dens: Moments, iters: int = 10000, tol: float = 1e-13) -> Tuple[List[float], List[float], List[float]]:
    """Lloyd's Method I from the start levels y0 (sorted, distinct).

    Returns (t, y, history) where history holds the distortion after each
    iteration; it never increases. Each iteration costs O(N) evaluations
    of the moment functions.
    """
    m0, m1, _ = dens
    y = list(y0)
    history: List[float] = []
    for _ in range(iters):  # @line L3
        t = [(y[i] + y[i + 1]) / 2 for i in range(len(y) - 1)]  # @line L4
        new_y = []
        for (a, b), old in zip(cells(t), y):
            mass = m0(a, b)
            new_y.append(m1(a, b) / mass if mass > 0 else old)  # @line L5
        change = max(abs(u - v) for u, v in zip(new_y, y))
        y = new_y
        history.append(distortion(t, y, dens))  # @line L6
        if change < tol:  # @line L7
            break
    t = [(y[i] + y[i + 1]) / 2 for i in range(len(y) - 1)]
    return t, y, history  # @line L8


def uniform_quantizer(levels: int, step: float) -> Tuple[List[float], List[float]]:
    """A symmetric uniform quantizer with the given number of levels and step."""
    y = [(i - (levels - 1) / 2) * step for i in range(levels)]
    t = [(y[i] + y[i + 1]) / 2 for i in range(levels - 1)]
    return t, y
